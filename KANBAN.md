# NInfer-4090 & TurboLLM Setup — Kanban Board

- **Repository:** [mukseq/ninfer-4090](https://github.com/mukseq/ninfer-4090)
- **GitHub Project Board:** [NInfer-4090 & TurboLLM Setup (Project #8)](https://github.com/users/mukseq/projects/8)
- **Upstream Source:** `https://github.com/sergiuszm/ninfer-4090` (`rtx4090-port`)

---

## Board Columns

### Done
- [x] **#1 Harden repo and switch Dockerfile to CUDA 12.8.1 for Driver 565 compatibility**
  - **Steps Taken:**
    1. Audited `sergiuszm/ninfer-4090` for malware, backdoors, SSRF, and path traversal; verified repository is clean.
    2. Removed `.codex/` directory containing upstream author's local hook configuration.
    3. Updated `Dockerfile` build and runtime stages from `nvidia/cuda:13.1.2-*-ubuntu24.04` to `nvidia/cuda:12.8.1-*-ubuntu24.04` and cleaned `/usr/local/cuda-12.8/compat` so the image satisfies `CMakeLists.txt` (`CUDA >= 12.8`) while running natively under CUDA 12 minor-version compatibility on the host's NVIDIA Driver `565.57.01` (`CUDA 12.7`) on GeForce RTX 4090.
    4. Updated `.gitignore` to exclude `.kanban.json` and `/slot-cache/`.

- [x] **#2 Build `ninfer-4090:sm89` Docker image and create TurboLLM custom engine wrapper (`ninfer-llama-server`)**
  - **Steps Taken:**
    1. Built `ninfer-4090:sm89` Docker image (`sha256:b60ce143bb96db9baedca199488217ae3822b161bdf08`) compiling `ninfer` and `ninfer-serve` for `CMAKE_CUDA_ARCHITECTURES=89` under CUDA 12.8.1 on Ubuntu 24.04.
    2. Added `NVIDIA_DISABLE_REQUIRE=1` to `Dockerfile`, `scripts/ninfer-llama-server`, and `scripts/run-docker-4090-262k.sh` so `nvidia-container-cli` allows CUDA 12.8 minor-version compatibility on host Driver `565.57.01` (`CUDA 12.7`).
    3. Created `scripts/ninfer-llama-server` wrapper implementing `--version`, `--help`, and `--list-devices` for TurboLLM's engine probe (`probe.ts`), translating `llama-server` CLI arguments (`-c`, `--host`, `--port`, `--parallel`, `--slot-save-path`) into `ninfer-serve` flags (`--max-context 262144 --kv-dtype rk4v4-e8 --spec mtp --draft-tokens 3 --lm-head-draft --vision --preserve-thinking --tolerant-tool-calls`).
    4. Created `scripts/run-docker-4090-262k.sh` standalone launcher bound to `127.0.0.1:8080`.
    5. Updated `scripts/download-qwen38.sh` default `NINFER_MODEL_DIR` to `$repo_root/models`.

- [x] **#3 Download and verify SHA-256 of `qwen3_8_27b.ninfer` (16.96 GiB container v2 artifact)**
  - **Steps Taken:**
    1. Executed `scripts/download-qwen38.sh` to download revision `3526913004b1` (16.96 GiB) of `neroued/Qwen3.8-27B-NInfer` into `/home/charlie/myapps/ninfer-4090/models/qwen3_8_27b.ninfer`.
    2. Verified SHA-256 hash matches `eec39564993d6e9c7d5e383382a760f093465c9d163ec9a1bd6b80199514bf3e`.

- [x] **#4 Move model to `/media/charlie/New Volume/ninfer` and update `README.md` with usage and TurboLLM guide**
  - **Steps Taken:**
    1. Moved `/home/charlie/myapps/ninfer-4090/models/qwen3_8_27b.ninfer` (16.96 GiB) to `/media/charlie/New Volume/ninfer/qwen3_8_27b.ninfer` and created a convenience symlink at `models/qwen3_8_27b.ninfer`.
    2. Updated `scripts/ninfer-llama-server`, `scripts/llama-server`, `scripts/run-docker-4090-262k.sh`, and `scripts/download-qwen38.sh` to serve and store the model from `/media/charlie/New Volume/ninfer` by default (resolving symlinks via `realpath` before mounting into Docker), with a default `163840` (160K) context window so it fits alongside desktop apps and idle ComfyUI.
    3. Added `scripts/llama-server` executable so TurboLLM's **Choose engine folder** dialog scans `/home/charlie/myapps/ninfer-4090/scripts` and detects `llama-server` automatically.
    4. Updated `README.md` with a complete "Local Setup, How to Run & TurboLLM Integration Guide".

- [x] **#5 Document Argon Max TurboLLM preset settings and GGUF stub workflow in `README.md`**
  - **Steps Taken:**
    1. Created `scripts/make-gguf-stub.py` to generate valid 1 MiB GGUF v3 metadata stubs (`Qwen3.8-27B-NInfer-Q4_K_M.gguf` and `mmproj-Qwen3.8-27B-NInfer-F16.gguf`) in `/media/charlie/New Volume/ninfer/` and `models/` so TurboLLM discovers the model and enables Vision.
    2. Configured `--model-id "qwen3.8-27b-ninfer|Q4_K_M|1048576"` in `scripts/llama-server` and `scripts/ninfer-llama-server` to match TurboLLM's internal `modelKey` on `/v1/chat/completions`.
    3. Documented the complete **`Argon max`** preset settings (Hardware & Context `163,328` / `262,144`, Sampling with `Top K = 20 <= 20`, and Advanced settings) in `README.md`.

### In Progress
*(None)*

### Todo
*(None)*
