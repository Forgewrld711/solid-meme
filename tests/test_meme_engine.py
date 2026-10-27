import tempfile
import unittest
from pathlib import Path

from meme_engine import create_meme


class MemeEngineTests(unittest.TestCase):
    def test_requires_description_or_image(self):
        with self.assertRaises(ValueError):
            create_meme(humor_level=5)

    def test_rejects_out_of_range_humor_level(self):
        with self.assertRaises(ValueError):
            create_meme(description="coffee", humor_level=11)

    def test_generates_svg_from_description(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = create_meme(description="debugging at 2am", humor_level=3, output_dir=tmpdir)
            file_path = Path(result["file_path"])
            self.assertTrue(file_path.exists())
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("<svg", content)
            self.assertIn("humor level: 3/10", content)

    def test_embeds_image_reference_when_provided(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = create_meme(
                image_url="https://example.com/cat.png",
                description="cat with keyboard",
                humor_level=9,
                output_dir=tmpdir,
            )
            content = Path(result["file_path"]).read_text(encoding="utf-8")
            self.assertIn("https://example.com/cat.png", content)


if __name__ == "__main__":
    unittest.main()
