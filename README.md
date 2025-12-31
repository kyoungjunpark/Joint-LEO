# Joint Optimization of Handoff and Video Rate in LEO Satellite Networks

[![License](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow 2.16+](https://img.shields.io/badge/TensorFlow-2.16+-orange.svg)](https://www.tensorflow.org/)

Reinforcement learning framework for joint bitrate adaptation and satellite handover optimization in Low Earth Orbit (LEO) satellite networks.

## Overview

Joint-LEO optimizes video streaming quality over LEO satellite networks by jointly deciding:
- **Bitrate adaptation**: Select optimal video quality based on network conditions
- **Satellite handover**: Choose best satellite to minimize disruption

### Key Challenges

- **Dynamic bandwidth**: LEO satellites have time-varying throughput and frequent handovers
- **Multi-user coordination**: Fair resource allocation across concurrent streams
- **Joint optimization**: Bitrate and handover decisions must be coordinated

### Algorithms

- **PPO (Proximal Policy Optimization)**: Deep RL with parallel multi-agent training
- **MPC (Model Predictive Control)**: Lookahead-based optimization baselines
- **Variants**: Centralized coordination, distributed decisions, multi-satellite support

## Installation

```bash
cd Joint-LEO/Joint-LEO
pip install -r requirements.txt
```

## Quick Start

### Training

```bash
cd src/models/rl_multi_bw_share

# Single-satellite baseline (Pensieve)
python train_pensieve.py --user 1

# Centralized multi-user (3 users)
python train_cent_dist_v2.py --user 3

# Distributed multi-satellite
python train_dist_multi_sat.py --user 3
```

### Testing

```bash
# Test trained model
python test_pensieve.py ./models/pensieve1/nn_model_ep_0.ckpt 1 MVT
```

### MPC Baseline

```bash
cd src/models/mpc_bw_share
python mpc.py --user 3
```

### GPU Configuration

```bash
# Use specific GPU
export CUDA_VISIBLE_DEVICES=0
python train_pensieve.py --user 1

# Use CPU
export CUDA_VISIBLE_DEVICES=-1
python train_pensieve.py --user 1
```

## Project Structure

```
Joint-LEO/
├── src/
│   ├── env/                    # Simulation environments
│   │   ├── multi_bw_share/     # Multi-user bandwidth sharing
│   │   └── object/             # Satellite and user objects
│   ├── models/
│   │   ├── rl_multi_bw_share/  # RL training/testing
│   │   └── mpc_bw_share/       # MPC baselines
│   ├── data/
│   │   ├── sat_data/           # Satellite traces
│   │   └── video_data/         # Video chunk sizes
│   └── util/                   # Utilities and constants
└── data/                       # Trained models (gitignored)
```

## Dataset

### Satellite Traces

- **Simulated**: `src/data/sat_data/train/`, `test/`
- **Real**: `real_train/`, `real_test/`
- **NOAA**: `noaa_train_trace/`, `noaa_test_trace/`

### Video Data

- **Location**: `src/data/video_data/envivio/`
- **Format**: 48 chunks, 6 quality levels (300-4300 Kbps), 2-second chunks

## Configuration

Key parameters in `src/util/constants.py`:

```python
VIDEO_BIT_RATE = [300, 750, 1200, 1850, 2850, 4300]  # Kbps
REBUF_PENALTY = 4.3
SMOOTH_PENALTY = 1.0
MPC_FUTURE_CHUNK_COUNT = 3
```

## Algorithms

### PPO (Reinforcement Learning)

- **State**: Throughput history, buffer occupancy, last bitrate, remaining chunks
- **Action**: Bitrate level (6 options) × satellite selection
- **Reward**: `QoE = bitrate - 4.3×rebuffer - 1.0×smoothness`
- **Training**: 16-20 parallel agents, GAE, adaptive entropy

### MPC (Model Predictive Control)

- **MVT**: Greedy satellite selection by current bandwidth
- **DualMPC**: Joint bitrate and handover optimization
- **Oracle**: Upper bound with perfect future knowledge
- **Lookahead**: 3-chunk horizon, harmonic mean prediction

## Monitoring

```bash
tensorboard --logdir=src/models/rl_multi_bw_share/models/pensieve1
```

## Citation

```bibtex
@inproceedings{park2026joint,
  title={Joint Optimization of Handoff and Video Rate in LEO Satellite Networks},
  author={Park, Kyoungjun and He, Zhiyuan and Luo, Cheng and Xu, Yi and Qiu, Lili and Ge, Changhan and Muaz, Muhammad},
  booktitle={IEEE INFOCOM 2026-IEEE Conference on Computer Communications},
  year={2026},
  organization={IEEE}
}
```

## References

- **Pensieve**: H. Mao et al., "Neural Adaptive Video Streaming with Pensieve," SIGCOMM 2017
- **PPO**: J. Schulman et al., "Proximal Policy Optimization Algorithms," arXiv 2017

## License

BSD 2-Clause License - see [LICENSE](LICENSE) file
