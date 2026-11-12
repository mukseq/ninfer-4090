#!/usr/bin/env python3
"""Generate valid 1 MiB GGUF v3 metadata stubs for TurboLLM's model scanner."""
import os
import struct
import sys

T_UINT32 = 4
T_STRING = 8


def pack_str(s: str) -> bytes:
    b = s.encode("utf-8")
    return struct.pack("<Q", len(b)) + b


def pack_kv_str(key: str, val: str) -> bytes:
    return pack_str(key) + struct.pack("<I", T_STRING) + pack_str(val)


def pack_kv_u32(key: str, val: int) -> bytes:
    return pack_str(key) + struct.pack("<I", T_UINT32) + struct.pack("<I", val)


def write_gguf_stub(path: str, kvs: list[bytes], size_bytes: int = 1048576) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    header = bytearray()
    header += b"GGUF"
    header += struct.pack("<I", 3)            # version 3
    header += struct.pack("<Q", 0)            # tensor_count = 0
    header += struct.pack("<Q", len(kvs))     # kv_count
    for kv in kvs:
        header += kv
    if len(header) < size_bytes:
        header += b"\x00" * (size_bytes - len(header))
    with open(path, "wb") as f:
        f.write(header)


def main() -> None:
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "models")
    model_path = os.path.join(out_dir, "Qwen3.8-27B-NInfer-Q4_K_M.gguf")
    mmproj_path = os.path.join(out_dir, "mmproj-Qwen3.8-27B-NInfer-F16.gguf")

    model_kvs = [
        pack_kv_str("general.architecture", "qwen35"),
        pack_kv_str("general.name", "Qwen3.8-27B-NInfer"),
        pack_kv_str("general.size_label", "27B"),
        pack_kv_u32("general.file_type", 15),
        pack_kv_u32("qwen35.context_length", 262144),
        pack_kv_u32("qwen35.block_count", 64),
        pack_kv_u32("qwen35.embedding_length", 5120),
        pack_kv_u32("qwen35.attention.head_count", 24),
        pack_kv_u32("qwen35.attention.head_count_kv", 4),
        pack_kv_u32("qwen35.attention.key_length", 256),
        pack_kv_u32("qwen35.attention.value_length", 256),
        pack_kv_u32("qwen35.full_attention_interval", 4),
        pack_kv_u32("qwen35.ssm.inner_size", 4096),
        pack_kv_u32("qwen35.ssm.state_size", 128),
        pack_kv_u32("qwen35.ssm.conv_kernel", 4),
        pack_kv_u32("qwen35.nextn_predict_layers", 1),
        pack_kv_str("tokenizer.chat_template", "{% for message in messages %}{{ message.content }}{% endfor %} reasoning_effort"),
    ]
    write_gguf_stub(model_path, model_kvs)

    mmproj_kvs = [
        pack_kv_str("general.architecture", "clip"),
        pack_kv_str("general.name", "Qwen3.8-27B-NInfer-Vision"),
        pack_kv_u32("general.file_type", 1),
    ]
    write_gguf_stub(mmproj_path, mmproj_kvs)
    print(f"Created:\n  {model_path}\n  {mmproj_path}")


if __name__ == "__main__":
    main()
