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

### In Progress
- [ ] **#2 Build `ninfer-4090:sm89` Docker image and create TurboLLM custom engine wrapper (`ninfer-llama-server`)**

### Todo
- [ ] **#3 Download and verify SHA-256 of `qwen3_8_27b.ninfer` (16.96 GiB container v2 artifact)**
