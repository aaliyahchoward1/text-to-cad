"""
Dropper Cap Assembly Template

Standard cosmetic dropper cap. M24 threading (standard for round bottles).
Includes cap body, dropper tube, and bulb.

Usage:
  params = {
    "thread_size": "M24",     # threading standard
    "tip_length": 40,         # mm, length of dropper tip below bulb
    "tip_diameter": 3.5,      # mm, outer diameter of dropper tip
    "bulb_diameter": 15,      # mm, diameter of rubber bulb
    "cap_height": 35,         # mm, height of cap body (excluding tip)
    "material_color": "natural_rubber"
  }
  cap = generate(params)
"""

from build123d import *
from math import pi


def generate(params: dict) -> Shape:
    """Generate a parametric dropper cap assembly."""

    thread_size = params.get("thread_size", "M24")
    tip_length = params.get("tip_length", 40)
    tip_diameter = params.get("tip_diameter", 3.5)
    bulb_diameter = params.get("bulb_diameter", 15)
    cap_height = params.get("cap_height", 35)

    # Cap body (simplified: cylinder with thread)
    cap_radius = 12  # Typical M24 cap outer radius
    cap_body = Cylinder(radius=cap_radius, height=cap_height, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Thread band (M24 simplified)
    thread_band = Cylinder(radius=cap_radius + 0.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Dropper tube (glass or plastic)
    tube = Cylinder(
        radius=tip_diameter / 2,
        height=cap_height + tip_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # Rubber bulb (sphere-ish, simplified as cylinder with hemispherical ends)
    bulb_center_z = cap_height + tip_length / 2
    bulb = Sphere(radius=bulb_diameter / 2).translate((0, 0, bulb_center_z))

    # Combine: cap body + thread band + tube + bulb
    assembly = cap_body + thread_band + tube + bulb

    return assembly


def get_parameters() -> dict:
    """Return parameter schema."""
    return {
        "thread_size": {
            "type": "str",
            "options": ["M24", "M27", "M30"],
            "default": "M24",
            "description": "Cap threading standard (M24 most common for cosmetics)"
        },
        "tip_length": {
            "type": "float",
            "unit": "mm",
            "default": 40,
            "min": 30,
            "max": 60,
            "description": "Length of dropper tip below bulb"
        },
        "tip_diameter": {
            "type": "float",
            "unit": "mm",
            "default": 3.5,
            "min": 2,
            "max": 5,
            "description": "Outer diameter of dropper tip"
        },
        "bulb_diameter": {
            "type": "float",
            "unit": "mm",
            "default": 15,
            "min": 10,
            "max": 20,
            "description": "Diameter of rubber bulb"
        },
        "cap_height": {
            "type": "float",
            "unit": "mm",
            "default": 35,
            "min": 30,
            "max": 45,
            "description": "Height of cap body above thread"
        },
        "material_color": {
            "type": "str",
            "options": ["natural_rubber", "white", "black", "colored"],
            "default": "natural_rubber",
            "description": "Material appearance"
        }
    }


if __name__ == "__main__":
    params = get_parameters()
    defaults = {k: v["default"] for k, v in params.items()}

    cap = generate(defaults)
    cap.save("test-dropper-cap.step")
    print("✓ Test dropper cap created: test-dropper-cap.step")
