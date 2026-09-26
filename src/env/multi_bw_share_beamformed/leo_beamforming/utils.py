import numpy as np
import pandas as pd
from scipy import constants
import glob 
import matlab.engine
import matplotlib.pyplot as plt
from multiprocessing import Pool
import copy
from itertools import combinations

# please add the following line in your code
eng = matlab.engine.start_matlab()

radius = 6378100

# tx/rx settings
tx = {'freq':11.325e9,
      'light_speed':constants.c,
      'power': 4.89e6,
      'num_ant': 1,
      'rf_chain':1,
      'ant_spacing':constants.c/11.325e9/2,
      'bandwidth':2000e6,
      'height':550e3,
      'speed':np.sqrt(5.9722e24 * 6.6743e-11 / (radius + 550e3))}

rx = {'freq':11.325e9,
      'light_speed':constants.c,
      'power': 1,
      'num_ant': 36,
      'rf_chain':1,
      'ant_spacing':constants.c/11.325e9/2,
      'height':0,
      'speed':0}

def svd_beamformer_analog(H):
    ant_tx, ant_rx = np.shape(H)
    u, s, wr_opt = np.linalg.svd(H)
    u, s, wt_opt = np.linalg.svd(np.transpose(H))
    
    wr_quant_angle = -np.transpose(np.around(np.angle(wr_opt)/(np.pi/2))*(np.pi/2))
    wt_quant_angle = -np.transpose(np.around(np.angle(wt_opt)/(np.pi/2))*(np.pi/2))
    
    wr_quant = np.exp(1j*wr_quant_angle)
    wt_quant = np.exp(1j*wt_quant_angle)
    
    rss = []
    beam_idx = []
    for i in range(ant_tx):
        for j in range(ant_rx):
            signal = np.abs(np.matmul(wt_quant[:,i],np.matmul(H,wr_quant[:,j])))**2
            rss.append(10*np.log10(signal*1000))
            beam_idx.append([i,j])
    
    idx = np.argmax(np.array(rss))
    tx_idx = beam_idx[idx][0]
    rx_idx = beam_idx[idx][1]
            
    wr_quant_out = wr_quant[:,rx_idx]
    wt_quant_out = wt_quant[:,tx_idx] 
    
    return wt_quant_out, wr_quant_out

def normalize(x):
    x = x/np.sqrt(np.sum(np.abs(x)**2))
    return x

def normalize_row(x):
    x = x/np.sqrt(np.sum(np.abs(x)**2))
    for i in range(len(x)):
        x[i,:] = x[i,:]/np.sqrt(np.sum(np.abs(x[i,:])**2))
    return x

def combs(num):
    x = list(range(num))
    return [c for i in range(len(x)+1) for c in combinations(x,i)]

def get_beamformed_rate(azi_file, timestamp, sat_selection):
    #print("Now Processing " + azi_file)
    alt_file = azi_file.replace('az','alt')
    dist_file = azi_file.replace('az','distance')
    
    azi_data = pd.read_csv(azi_file)
    alt_data = pd.read_csv(alt_file)
    dist_data = pd.read_csv(dist_file)
    
    satellites = list(azi_data.columns)[2:]
    
    ######################## start RF calculation#####################
    txang_azi = azi_data.iloc[timestamp,2:].values
    index = np.where(txang_azi!=0)[0]
    
    rate_beamformed_nprecoding = np.zeros(len(index), dtype = np.float64)
    rate_beamformed_FDMA_nprecoding = np.zeros(len(index), dtype = np.float64)
    rate_beamformed_precoding = np.zeros(len(index), dtype = np.float64)
    rate_beamformed_FDMA_precoding = np.zeros(len(index), dtype = np.float64)
    
    if len(sat_selection) > len(index):
        raise ValueError('number of selected satellite is larger than number of visible satellite')

    txang_azi = txang_azi[txang_azi!=0]-np.pi
    txang_ele = alt_data.iloc[timestamp,2:].values
    txang_ele = txang_ele[txang_ele!=0]
    txang = matlab.double(np.array([txang_azi,txang_ele]).tolist())

    rxang_azi = azi_data.iloc[timestamp,2:].values
    rxang_azi = rxang_azi[rxang_azi!=0]-np.pi
    rxang_ele = alt_data.iloc[timestamp,2:].values
    rxang_ele = rxang_ele[rxang_ele!=0]
    rxang = matlab.double(np.array([rxang_azi,rxang_ele]).tolist())

    dist = np.array(dist_data.iloc[timestamp,2:].values)*1000
    dist = matlab.double(dist[dist!=0].tolist())
    
    #################### get channel #######################
    H = np.array(eng.get_channel_MUMIMO(matlab.double(tx["num_ant"]), matlab.double(rx["num_ant"]), 
                        matlab.double(tx["rf_chain"]), matlab.double(rx["rf_chain"]),
                       matlab.double(tx["freq"]), txang, rxang, dist, matlab.double(tx['speed']), matlab.double(rx['speed'])))

    #################### calculate interference matrix ##########################
    interference_matrix_beamformed = np.zeros((len(index), len(index)),dtype = np.complex128)
    interference_matrix_beamformed_FDMA = np.zeros((len(index), len(index)),dtype = np.complex128)
    for i in range(len(index)):
        wt, wr = svd_beamformer_analog(H[i,i,:,:])
        for j in range(len(index)):
            sig_beamformed_sat = np.squeeze(np.matmul(np.expand_dims(wt, axis = 0), np.matmul(H[i,j,:,:], np.expand_dims(wr, axis = 1))))
            interference_matrix_beamformed[i,j] = sig_beamformed_sat
            if i in sat_selection and j in sat_selection:
                interference_matrix_beamformed_FDMA[i,j] = sig_beamformed_sat
        sinr_bf_nprecoding_cur = tx['power']/tx['num_ant']*np.abs(interference_matrix_beamformed[i,i])**2/(tx['power']/tx['num_ant']*np.abs(np.sum(interference_matrix_beamformed[i,:]) - interference_matrix_beamformed[i,i])**2 + 1e-12)
        rate_beamformed_nprecoding[i] = tx["bandwidth"]*np.log2(1+sinr_bf_nprecoding_cur)
    
    # FDMA channel
    for i in sat_selection:
        sinr_bf_nprecoding_FDMA_cur = tx['power']/tx['num_ant']*np.abs(interference_matrix_beamformed_FDMA[i,i])**2/(tx['power']/tx['num_ant']*np.abs(np.sum(interference_matrix_beamformed_FDMA[i,:]) - interference_matrix_beamformed_FDMA[i,i])**2 + 1e-12)
        rate_beamformed_FDMA_nprecoding[i] = tx["bandwidth"]*np.log2(1+sinr_bf_nprecoding_FDMA_cur)

    ###################### precoding ########################
    interference_matrix_beamformed_selected = np.zeros((len(sat_selection), len(sat_selection)),dtype = np.complex128)
    for sat_sub_id, sat_id in enumerate(sat_selection):
        interference_matrix_beamformed_selected[sat_sub_id, :] = interference_matrix_beamformed[sat_id, sat_selection]
    
    precoding_weight_selected = normalize_row(np.linalg.pinv(interference_matrix_beamformed_selected))*np.sqrt(tx['power']/tx['num_ant'])
    precoding_weight_beamformed = np.identity(len(index),dtype = np.complex128)*np.sqrt(tx['power']/tx['num_ant'])
    for sat_sub_id, sat_id in enumerate(sat_selection):
        precoding_weight_beamformed[sat_id, sat_selection] = precoding_weight_selected[sat_sub_id,:]
    
    cancelled_channel_beamformed = np.matmul(interference_matrix_beamformed, precoding_weight_beamformed)
    cancelled_channel_beamformed_FDMA = np.matmul(interference_matrix_beamformed_FDMA, precoding_weight_beamformed)

    for i in range(len(index)):
        sinr_bf_cur = np.abs(cancelled_channel_beamformed[i,i])**2/(np.abs(np.sum(cancelled_channel_beamformed[i,:]) - cancelled_channel_beamformed[i,i])**2 + 1e-12)
        rate_beamformed_precoding[i] = tx["bandwidth"]*np.log2(1 + sinr_bf_cur)
        
        sinr_bf_FDMA_cur = np.abs(cancelled_channel_beamformed_FDMA[i,i])**2/(np.abs(np.sum(cancelled_channel_beamformed_FDMA[i,:]) - cancelled_channel_beamformed_FDMA[i,i])**2 + 1e-12)
        rate_beamformed_FDMA_precoding[i] = tx["bandwidth"]*np.log2(1 + sinr_bf_FDMA_cur)

    return np.sum(rate_beamformed_nprecoding[sat_selection]), np.sum(rate_beamformed_FDMA_nprecoding[sat_selection]), np.sum(rate_beamformed_precoding[sat_selection]), np.sum(rate_beamformed_FDMA_precoding[sat_selection])