## Quick start
```bash
# At least one LLM API key is required
echo 'OPENAI_API_KEY=your_openai_api_key' >> .env

# uv is recommended but "pip install ." also works
pip install uv
uv sync --frozen

# "uv sync" creates .venv automatically
source .venv/bin/activate
python app/main.py

# In another shell
source .venv/bin/activate
python bot/main.py
```