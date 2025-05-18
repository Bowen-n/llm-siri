# llm-siri
Improve Siri with locally deployed LLM on Mac.

### Environment

Managed by uv.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv venv --python 3.12
uv pip install -e .

# for developing
uv sync --all-groups
```

### Start LLM Server

```bash
# download model (e.g. qwen3)
git lfs install
git clone https://www.modelscope.cn/lmstudio-community/Qwen3-30B-A3B-MLX-4bit.git
```

```bash
# run server
llm-server --model-path /path/to/model
```

for testing:

```bash
curl -X POST http://localhost:8000/ \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "who are you"}], "think": true}' \
| jq
```

### Shortcut [WIP]
