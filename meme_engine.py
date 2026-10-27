from __future__ import annotations

from datetime import UTC, datetime
from html import escape
from pathlib import Path
from uuid import uuid4


def _normalize_humor_level(humor_level: int) -> int:
    if not isinstance(humor_level, int):
        raise ValueError("humor_level must be an integer between 0 and 10")
    if humor_level < 0 or humor_level > 10:
        raise ValueError("humor_level must be between 0 and 10")
    return humor_level


def _build_caption(description: str | None, image_url: str | None, humor_level: int) -> tuple[str, str]:
    source = (description or "this photo").strip() or "this photo"

    if humor_level <= 3:
        return (
            f"EXPECTATION: {source.upper()[:50]}",
            "REALITY: tiny giggle unlocked",
        )
    if humor_level <= 7:
        return (
            f"ME TRYING TO EXPLAIN: {source.upper()[:40]}",
            "EVERYONE ELSE: why is this actually funny?",
        )

    return (
        f"{source.upper()[:38]} AT HUMOR LEVEL {humor_level}",
        "THE LAWS OF COMEDY HAVE LEFT THE CHAT",
    )


def create_meme(
    description: str | None = None,
    image_url: str | None = None,
    humor_level: int = 5,
    output_dir: str = "generated_memes",
) -> dict[str, str | int]:
    if not description and not image_url:
        raise ValueError("Provide either description or image_url")

    level = _normalize_humor_level(humor_level)
    top_text, bottom_text = _build_caption(description, image_url, level)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"meme_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}.svg"
    file_path = output_path / filename

    _render_svg(
        file_path=file_path,
        top_text=top_text,
        bottom_text=bottom_text,
        description=description,
        image_url=image_url,
        humor_level=level,
    )

    return {
        "file_path": str(file_path.resolve()),
        "top_text": top_text,
        "bottom_text": bottom_text,
        "humor_level": level,
    }


def _render_svg(
    file_path: Path,
    top_text: str,
    bottom_text: str,
    description: str | None,
    image_url: str | None,
    humor_level: int,
) -> None:
    description_text = (description or "").strip()
    safe_desc = escape(description_text[:160])

    image_block = ""
    if image_url:
        image_block = (
            f'<image href="{escape(image_url)}" x="0" y="0" width="1024" height="1024" '
            'preserveAspectRatio="xMidYMid slice" />\n'
            '<rect x="0" y="0" width="1024" height="1024" fill="black" fill-opacity="0.35" />\n'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2a2a72" />
      <stop offset="100%" stop-color="#009ffd" />
    </linearGradient>
    <style>
      .meme {{
        fill: white;
        font-family: Impact, Arial Black, sans-serif;
        text-anchor: middle;
        paint-order: stroke;
        stroke: black;
        stroke-width: 4;
      }}
      .small {{
        font-family: Arial, sans-serif;
        fill: #f0f0f0;
        font-size: 24px;
        text-anchor: middle;
      }}
    </style>
  </defs>
  <rect x="0" y="0" width="1024" height="1024" fill="url(#bg)" />
  {image_block.rstrip()}
  <text class="meme" x="512" y="100" font-size="64">{escape(top_text)}</text>
  <text class="meme" x="512" y="940" font-size="56">{escape(bottom_text)}</text>
  <text class="small" x="512" y="512">humor level: {humor_level}/10</text>
  <text class="small" x="512" y="550">{safe_desc}</text>
</svg>
'''

    file_path.write_text(svg, encoding="utf-8")
