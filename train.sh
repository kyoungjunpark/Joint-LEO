#!/bin/bash
# Quick start script for training RL models

set -e

echo "=========================================="
echo "Joint-LEO Training Script"
echo "=========================================="
echo ""

# Default parameters
NUM_USERS=1
MODEL_TYPE="pensieve"
HANDOVER_TYPE="MVT"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --users)
            NUM_USERS="$2"
            shift 2
            ;;
        --model)
            MODEL_TYPE="$2"
            shift 2
            ;;
        --handover)
            HANDOVER_TYPE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./train.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --users NUM       Number of concurrent users (default: 1)"
            echo "  --model TYPE      Model type: pensieve, cent_dist, dist_multi (default: pensieve)"
            echo "  --handover TYPE   Handover type: MVT, DualMPC (default: MVT)"
            echo "  --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./train.sh --users 3"
            echo "  ./train.sh --users 5 --model cent_dist --handover DualMPC"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Users: $NUM_USERS"
echo "  Model: $MODEL_TYPE"
echo "  Handover: $HANDOVER_TYPE"
echo ""

# Navigate to the correct directory
cd src/models/rl_multi_bw_share

# Select training script based on model type
case $MODEL_TYPE in
    pensieve)
        SCRIPT="train_pensieve.py"
        ;;
    cent_dist)
        SCRIPT="train_cent_dist_v2.py"
        ;;
    dist_multi)
        SCRIPT="train_dist_multi_sat.py"
        ;;
    *)
        echo "Error: Unknown model type '$MODEL_TYPE'"
        exit 1
        ;;
esac

echo "Starting training..."
echo "Script: $SCRIPT"
echo "Command: python $SCRIPT --user $NUM_USERS"
echo ""

# Run training
python $SCRIPT --user $NUM_USERS

echo ""
echo "=========================================="
echo "Training completed!"
echo "=========================================="
