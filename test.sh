#!/bin/bash
# Quick start script for testing trained models

set -e

echo "=========================================="
echo "Joint-LEO Testing Script"
echo "=========================================="
echo ""

# Default parameters
NUM_USERS=1
MODEL_PATH=""
HANDOVER_TYPE="MVT"
MODEL_TYPE="pensieve"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --users)
            NUM_USERS="$2"
            shift 2
            ;;
        --model-path)
            MODEL_PATH="$2"
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
            echo "Usage: ./test.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --users NUM          Number of concurrent users (default: 1)"
            echo "  --model-path PATH    Path to trained model checkpoint (required)"
            echo "  --model TYPE         Model type: pensieve, cent_dist, dist_multi (default: pensieve)"
            echo "  --handover TYPE      Handover type: MVT, DualMPC (default: MVT)"
            echo "  --help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./test.sh --model-path data/sim/3/best_model.ckpt --users 3"
            echo "  ./test.sh --model-path data/real/5/best_model.ckpt --users 5 --handover DualMPC"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if model path is provided
if [ -z "$MODEL_PATH" ]; then
    echo "Error: --model-path is required"
    echo "Use --help for usage information"
    exit 1
fi

# Check if model exists
if [ ! -f "${MODEL_PATH}.index" ]; then
    echo "Error: Model not found at $MODEL_PATH"
    echo "Make sure the .ckpt.index file exists"
    exit 1
fi

echo "Configuration:"
echo "  Users: $NUM_USERS"
echo "  Model: $MODEL_TYPE"
echo "  Model Path: $MODEL_PATH"
echo "  Handover: $HANDOVER_TYPE"
echo ""

# Navigate to the correct directory
cd src/models/rl_multi_bw_share

# Select testing script based on model type
case $MODEL_TYPE in
    pensieve)
        SCRIPT="test_pensieve.py"
        ;;
    cent_dist)
        SCRIPT="test_cent_dist_v2.py"
        ;;
    dist_multi)
        SCRIPT="test_dist_multi_sat.py"
        ;;
    *)
        echo "Error: Unknown model type '$MODEL_TYPE'"
        exit 1
        ;;
esac

echo "Starting evaluation..."
echo "Script: $SCRIPT"
echo "Command: python $SCRIPT ../../../$MODEL_PATH $NUM_USERS $HANDOVER_TYPE"
echo ""

# Run testing
python $SCRIPT "../../../$MODEL_PATH" $NUM_USERS $HANDOVER_TYPE

echo ""
echo "=========================================="
echo "Testing completed!"
echo "Results saved in test_results_*/ directory"
echo "=========================================="
