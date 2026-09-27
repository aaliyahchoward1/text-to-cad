"""
Label Template — Flat Label Wrap for Bottles

Creates a 2D label geometry that wraps around a cylindrical bottle.
Exported as flat shape (for label printing) or wrapped 3D geometry (for mockups).

Usage:
  params = {
    "width": 45,              # mm, wrapped circumference
    "height": 80,             # mm, vertical height
    "wrap_circumference": 142,# mm, target bottle circumference (π×diameter)
    "content_area_margin": 3  # mm, margin from edges
  }
  label = generate(params)
"""

from build123d import *
from math import pi


def generate(params: dict) -> Shape:
    """Generate a flat label wrap."""

    width = params.get("width", 45)
    height = params.get("height", 80)
    margin = params.get("content_area_margin", 3)

    # Create flat rectangular label
    label = Box(width, height, 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Create content area (margin-inset rectangle) for design guidance
    content_width = width - (2 * margin)
    content_height = height - (2 * margin)

    if content_width > 0 and content_height > 0:
        content_area = Box(
            content_width, content_height, 0.05,
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).translate((0, 0, 0.05))  # Slightly above base

        # Combine (content area for reference, not subtracted)
        label = label

    return label


def get_parameters() -> dict:
    """Return parameter schema."""
    return {
        "width": {
            "type": "float",
            "unit": "mm",
            "default": 45,
            "min": 20,
            "max": 200,
            "description": "Width of label wrap (or circumference segment)"
        },
        "height": {
            "type": "float",
            "unit": "mm",
            "default": 80,
            "min": 30,
            "max": 300,
            "description": "Vertical height of label"
        },
        "wrap_circumference": {
            "type": "float",
            "unit": "mm",
            "default": 142,
            "min": 50,
            "max": 400,
            "description": "Target bottle circumference (π × diameter) for wrapping"
        },
        "content_area_margin": {
            "type": "float",
            "unit": "mm",
            "default": 3,
            "min": 0,
            "max": 10,
            "description": "Margin from edges to content area (for safe text/graphics)"
        }
    }


if __name__ == "__main__":
    params = get_parameters()
    defaults = {k: v["default"] for k, v in params.items()}

    label = generate(defaults)
    label.save("test-label.step")
    print("✓ Test label created: test-label.step")
