from llama_cpp import Llama

llm = Llama(
    model_path="../models/llama/model.gguf",  # your model
    flash_attn=True,                         # as before
    n_gpu_layers=80,                         # GPU offload
    n_batch=128,                             # batch size
    n_threads=20,                             # threads
    n_ctx=2048,                              # ↑ increase context window if needed
    verbose=False,
)

# Give yourself enough room to get a full explanation:
resp = llm(
    "Explain time dilation",
    max_tokens=512,     # ← bump this up from the 16‑token default
    temperature=0.0,    # optional
)

print(resp["choices"][0]["text"])
