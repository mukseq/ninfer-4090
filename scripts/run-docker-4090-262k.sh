#!/usr/bin/env bash
set -euo pipefail

# Standalone RTX 4090 262K Context + Vision + MTP3 Docker Launcher (bound to 127.0.0.1:8080)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
MODEL_DIR="${NINFER_MODEL_DIR:-$REPO_ROOT/models}"
MODEL_FILE="${1:-qwen3_8_27b.ninfer}"
PORT="${NINFER_PORT:-8080}"

if [[ ! -f "$MODEL_DIR/$MODEL_FILE" ]]; then
  echo "Missing model file: $MODEL_DIR/$MODEL_FILE" >&2
  echo "Run: NINFER_MODEL_DIR=\"$MODEL_DIR\" bash \"$SCRIPT_DIR/download-qwen38.sh\"" >&2
  exit 1
fi

echo "Starting NInfer-4090 (262K rk4v4-e8 KV, MTP3, Vision) at http://127.0.0.1:$PORT/v1"
exec docker run --rm --gpus all \
  -e NVIDIA_DISABLE_REQUIRE=1 \
  --publish "127.0.0.1:${PORT}:8080" \
  --volume "$MODEL_DIR:/workspace/models:ro" \
  ninfer-4090:sm89 \
  ninfer-serve "/workspace/models/$MODEL_FILE" \
  --host 0.0.0.0 --port 8080 \
  --max-context 262144 --kv-capacity 262144 \
  --max-concurrency 1 --max-pending-requests 16 \
  --pending-timeout-ms 600000 \
  --prefill-chunk 1024 --kv-dtype rk4v4-e8 \
  --spec mtp --draft-tokens 3 --lm-head-draft \
  --vision --preserve-thinking --tolerant-tool-calls
