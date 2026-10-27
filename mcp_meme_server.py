from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from meme_engine import create_meme

mcp = FastMCP("solid-meme")


@mcp.tool()
def generate_meme(
    humor_level: int,
    description: str | None = None,
    image_url: str | None = None,
    output_dir: str = "generated_memes",
) -> dict[str, str | int]:
    """Create a meme from either a text description or a source image URL/path.

    - humor_level: integer from 0 (small giggle) to 10 (off the walls)
    - description: optional meme idea text
    - image_url: optional source image (URL or local path)
    """
    return create_meme(
        description=description,
        image_url=image_url,
        humor_level=humor_level,
        output_dir=output_dir,
    )


@mcp.tool()
def surprise_meme_idea(topic: str = "daily life") -> str:
    """Return a quick meme prompt idea people can feed back into generate_meme."""
    topic = topic.strip() or "daily life"
    return (
        f"Create a meme about '{topic}' where someone tries to be productive "
        "for 5 minutes and then gets emotionally adopted by a random distraction."
    )


if __name__ == "__main__":
    mcp.run()
