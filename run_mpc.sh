#!/bin/bash
# Script for running MPC baseline experiments

set -e

echo "=========================================="
echo "Joint-LEO MPC Baseline Script"
echo "=========================================="
echo ""

# Default parameters
NUM_USERS=1
MPC_TYPE="MVT"
TRACE_TYPE="sim"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --users)
            NUM_USERS="$2"
            shift 2
            ;;
        --mpc-type)
            MPC_TYPE="$2"
            shift 2
            ;;
        --trace)
            TRACE_TYPE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./run_mpc.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --users NUM       Number of concurrent users (default: 1)"
            echo "  --mpc-type TYPE   MPC variant: MVT, DualMPC, Oracle (default: MVT)"
            echo "  --trace TYPE      Trace type: sim, real, noaa (default: sim)"
            echo "  --help           Show this help message"
            echo ""
            echo "MPC Types:"
            echo "  MVT              Most Valuable Throughput (greedy)"
            echo "  DualMPC          Joint bitrate and handover optimization"
            echo "  Oracle           Perfect future knowledge (upper bound)"
            echo ""
            echo "Examples:"
            echo "  ./run_mpc.sh --users 3 --mpc-type MVT"
            echo "  ./run_mpc.sh --users 5 --mpc-type DualMPC --trace real"
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
echo "  MPC Type: $MPC_TYPE"
echo "  Trace Type: $TRACE_TYPE"
echo ""

# Navigate to the correct directory
cd src/models/mpc_bw_share

# Select MPC script based on trace type
case $TRACE_TYPE in
    sim)
        SCRIPT="mpc.py"
        ;;
    real)
        SCRIPT="mpc_real.py"
        ;;
    noaa)
        SCRIPT="mpc_noaa.py"
        ;;
    *)
        echo "Error: Unknown trace type '$TRACE_TYPE'"
        exit 1
        ;;
esac

echo "Starting MPC evaluation..."
echo "Script: $SCRIPT"
echo "Command: python $SCRIPT --user $NUM_USERS"
echo ""

# Run MPC
python $SCRIPT --user $NUM_USERS

echo ""
echo "=========================================="
echo "MPC evaluation completed!"
echo "Results saved in MPC_*/ directory"
echo "=========================================="
