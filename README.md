# solid-meme

An MCP server that lets any AI client generate memes from either:
- a text description, or
- an image URL/path

You also set a humor level from `0` (small giggle) to `10` (off the walls).

## Quick start

```bash
cd /home/runner/work/solid-meme/solid-meme
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python mcp_meme_server.py
```

The server exposes these MCP tools:
- `generate_meme(humor_level, description?, image_url?, output_dir?)`
- `surprise_meme_idea(topic?)`

Generated memes are SVG files saved to `generated_memes/` by default.

## Example MCP client config (stdio)

```json
{
  "mcpServers": {
    "solid-meme": {
      "command": "python",
      "args": ["/home/runner/work/solid-meme/solid-meme/mcp_meme_server.py"]
    }
  }
}
```
