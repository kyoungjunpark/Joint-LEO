# Joint-LEO

Joint-LEO is a research codebase for joint bitrate adaptation and satellite handover in Low Earth Orbit (LEO) video streaming systems.

The repository contains PPO-based reinforcement learning models, model-predictive-control baselines, multi-user and multi-satellite environments, beamforming experiments, and several trace collections.

## Repository Layout

```text
src/
├── data/                         # Satellite traces and video chunk sizes
├── env/                          # Simulation environments
│   ├── multi_bw_share/           # Multi-user bandwidth sharing
│   ├── multi_bw_share_beamformed/# Beamforming environments
│   ├── multi_bw_share_multi_session/
│   ├── multi_no_bw_share/
│   └── object/                   # Satellite and user objects
├── models/
│   ├── rl_multi_bw_share/        # Main PPO training and test scripts
│   ├── rl_multi_bw_share_multi_session/
│   ├── rl_multi_bw_share_weights/
│   ├── mpc_bw_share/             # MPC baselines
│   ├── mpc_bw_share_multi_session/
│   └── references/               # Reference Pensieve implementation
├── util/                         # Shared constants and encoders
├── real/                         # Real-trace experiment outputs/configurations
├── unclassified_files/           # Older experiments kept for reference
└── requirements.txt              # Python dependencies
```

The root `data/` directory contains local experiment artifacts and trained-model outputs. Generated checkpoints, TensorBoard logs, and test results are intentionally excluded from version control.

## Requirements

The dependency list is in [`src/requirements.txt`](src/requirements.txt). The training scripts use TensorFlow 2.x with the TensorFlow 1.x compatibility API, `tflearn`, `structlog`, NumPy, SciPy, Statsmodels, Matplotlib, and tqdm.

The pinned TensorFlow version targets an older Python environment. Python 3.7-3.9 is the safest choice for this dependency set; newer Python versions may require updating the TensorFlow pin.

## Installation

Run these commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r src/requirements.txt
```

The scripts use relative paths for traces and therefore should be launched from the working directories shown below.

## Data

Satellite traces are stored under `src/data/sat_data/`:

- `train/` and `test/`: simulated traces
- `real_train/` and `real_test/`: real traces
- `noaa_train_trace/` and `noaa_test_trace/`: NOAA traces
- `simulated_trace/` and `test_tight/`: additional experiment traces
- `beamformed/`: beamforming-specific data

Video chunk sizes are in `src/data/video_data/envivio/` as `video_size_*` files.

The active trace paths and reward constants are defined in [`src/util/constants.py`](src/util/constants.py).

## PPO Training

The main PPO scripts are in `src/models/rl_multi_bw_share/`. From the repository root:

```bash
cd src/models/rl_multi_bw_share

# Single-user Pensieve-style baseline
python train_pensieve.py --user 1

# Centralized multi-user model
python train_cent_dist_v2.py --user 3

# Distributed multi-satellite model
python train_dist_multi_sat.py --user 3
```

Each script also has variants for NOAA and real traces, for example:

```bash
python train_pensieve_noaa.py --user 1
python train_cent_dist_v2_real.py --user 3
python train_dist_multi_sat_real.py --user 3
```

Training is long-running and writes checkpoints, summaries, and test results into the current model directory. These generated outputs are ignored by Git.

## Testing A Trained Model

The Pensieve test script expects a checkpoint path, user count, and handover mode. A checkpoint produced by `train_pensieve.py --user 1` is written under `pensieve1/`:

```bash
cd src/models/rl_multi_bw_share
python test_pensieve.py ./pensieve1/nn_model_ep_0.ckpt 1 MVT
```

Other model families have corresponding `test_*.py` scripts in the same directory, including NOAA and real-trace variants.

## MPC Baselines

MPC entrypoints are in `src/models/mpc_bw_share/`:

```bash
cd src/models/mpc_bw_share
python mpc.py --user 3
```

Additional variants include `mpc_noaa.py`, `mpc_real.py`, and `mpc_tight.py`. A multi-session implementation is in `src/models/mpc_bw_share_multi_session/`.

## Multi-Session, Weights, And Beamforming

- Multi-session PPO scripts: `src/models/rl_multi_bw_share_multi_session/`
- Weight-focused PPO scripts: `src/models/rl_multi_bw_share_weights/`
- Beamforming environments and MATLAB/Python helpers: `src/env/multi_bw_share_beamformed/leo_beamforming/`
- Older or exploratory implementations: `src/unclassified_files/`

These areas contain experiment-specific scripts and may require changing constants or trace paths for a particular run.

## Configuration

Important defaults in `src/util/constants.py` include:

```python
VIDEO_BIT_RATE = [300, 750, 1200, 1850, 2850, 4300]
REBUF_PENALTY = 4.3
SMOOTH_PENALTY = 1
```

The training scripts expose the number of users through `--user`. GPU selection can be controlled with `CUDA_VISIBLE_DEVICES`:

```bash
export CUDA_VISIBLE_DEVICES=0    # use GPU 0
export CUDA_VISIBLE_DEVICES=-1   # force CPU
```

## Validation

A syntax-only check for the repository is:

```bash
python -m compileall -q src
```

This validates Python syntax but does not run a full training job. Full execution additionally requires the dependencies in `src/requirements.txt` and a compatible Python/TensorFlow environment.

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

- H. Mao et al., "Neural Adaptive Video Streaming with Pensieve," SIGCOMM 2017
- J. Schulman et al., "Proximal Policy Optimization Algorithms," arXiv 2017

## License

BSD 2-Clause License. See [LICENSE](LICENSE).
