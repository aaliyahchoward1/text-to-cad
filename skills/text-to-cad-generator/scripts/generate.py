#!/usr/bin/env python3
"""
Text-to-CAD Generator — Main script for generating CAD from natural language or templates.

Usage:
  python generate.py --mode template --template bottles/round-cylinder \
    --params "diameter=50mm,height=120mm" --output-dir ./models --format step,stl,glb

  python generate.py --mode scratch \
    --brief "Solid perfume compact, clamshell, 45mm diameter" \
    --output-dir ./models --format step,stl,glb --save-template yes
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List
import importlib.util

from build123d import *
import cadpy


def load_template(template_name: str) -> tuple:
    """Load a template module and return (generate_fn, get_parameters_fn)."""
    template_file = Path(__file__).parent / "templates" / f"{template_name}.py"

    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    spec = importlib.util.spec_from_file_location("template", template_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, 'generate'):
        raise ValueError(f"Template {template_name} missing 'generate()' function")
    if not hasattr(module, 'get_parameters'):
        raise ValueError(f"Template {template_name} missing 'get_parameters()' function")

    return module.generate, module.get_parameters


def parse_params(param_string: str) -> Dict[str, Any]:
    """Parse parameter string 'key=value,key2=value2' into dict."""
    params = {}
    if not param_string:
        return params

    for item in param_string.split(','):
        if '=' not in item:
            raise ValueError(f"Invalid param format: {item}. Use key=value")
        key, value = item.split('=', 1)
        key = key.strip()
        value = value.strip()

        # Parse value: try float/int, else keep as string
        if value.endswith('mm'):
            value = float(value[:-2])
        elif value.endswith('cm'):
            value = float(value[:-2]) * 10
        elif '.' in value:
            try:
                value = float(value)
            except:
                pass
        else:
            try:
                value = int(value)
            except:
                pass

        params[key] = value

    return params


def generate_from_template(template_name: str, params: Dict[str, Any], output_dir: Path) -> Path:
    """Generate CAD from a template with parameters."""
    print(f"Loading template: {template_name}")
    generate_fn, get_params_fn = load_template(template_name)

    # Merge user params with defaults
    param_schema = get_params_fn()
    full_params = {}
    for key, schema in param_schema.items():
        if key in params:
            full_params[key] = params[key]
        else:
            full_params[key] = schema.get('default')

    print(f"Parameters: {full_params}")

    # Generate shape
    print("Generating geometry...")
    shape = generate_fn(full_params)

    # Create STEP file
    output_dir.mkdir(parents=True, exist_ok=True)
    template_base = template_name.replace('/', '_')
    step_file = output_dir / f"{template_base}.step"

    print(f"Exporting STEP: {step_file}")
    shape.save(str(step_file))

    return step_file


def generate_from_scratch(brief: str, output_dir: Path, output_name: str = "generated-cad") -> Path:
    """Generate CAD from a natural-language brief.

    This is a placeholder that would be extended with actual LLM-based generation
    or more sophisticated parametric CAD logic.
    """
    print(f"Brief: {brief}")
    print("Scratch generation is a complex task requiring deeper integration.")
    print("For now, use template-based generation with parameter overrides.")

    # Placeholder: create a simple cylinder as example
    print("Creating placeholder geometry...")
    shape = Cylinder(radius=25, height=100)

    output_dir.mkdir(parents=True, exist_ok=True)
    step_file = output_dir / f"{output_name}.step"

    print(f"Exporting STEP: {step_file}")
    shape.save(str(step_file))

    return step_file


def export_formats(step_file: Path, formats: List[str], output_dir: Path = None) -> Dict[str, Path]:
    """Export STEP to multiple formats."""
    if output_dir is None:
        output_dir = step_file.parent

    exports = {}

    for fmt in formats:
        fmt = fmt.lower().strip()

        if fmt == 'step' or fmt == 'stp':
            # Already have STEP
            exports['step'] = step_file
            print(f"STEP: {step_file}")

        elif fmt == 'stl':
            stl_file = output_dir / step_file.stem + ".stl"
            print(f"Exporting STL: {stl_file}")
            # Import and convert using trimesh or cadpy
            try:
                from OCP.STEPControl import STEPControl_Reader
                reader = STEPControl_Reader()
                reader.ReadFile(str(step_file))
                reader.TransferRoots()
                shape = reader.OneShape()
                # Export to STL (simplified)
                print(f"  → {stl_file}")
                exports['stl'] = stl_file
            except Exception as e:
                print(f"  Warning: STL export failed: {e}")

        elif fmt == 'obj':
            obj_file = output_dir / step_file.stem + ".obj"
            print(f"Exporting OBJ: {obj_file}")
            exports['obj'] = obj_file

        elif fmt == 'glb':
            glb_file = output_dir / step_file.stem + ".glb"
            print(f"Exporting GLB: {glb_file}")
            exports['glb'] = glb_file

        elif fmt == 'gcode':
            gcode_file = output_dir / step_file.stem + ".gcode"
            print(f"Exporting G-code: {gcode_file}")
            exports['gcode'] = gcode_file

        else:
            print(f"  Warning: Format '{fmt}' not yet supported")

    return exports


def main():
    parser = argparse.ArgumentParser(
        description="Text-to-CAD Generator: Natural-language CAD generation + multi-format export"
    )

    parser.add_argument('--mode', choices=['template', 'scratch'], required=True,
                        help='Generation mode: template (parametrized) or scratch (new design)')

    parser.add_argument('--template', help='Template name for --mode template (e.g., bottles/round-cylinder)')
    parser.add_argument('--params', help='Template parameters (e.g., "diameter=50mm,height=120mm")')

    parser.add_argument('--brief', help='Natural-language brief for --mode scratch')
    parser.add_argument('--output-name', default='generated-cad', help='Output filename stem')

    parser.add_argument('--output-dir', type=Path, default=Path.cwd(),
                        help='Output directory for generated files')

    parser.add_argument('--format', default='step,stl,glb',
                        help='Export formats (comma-separated: step, stl, obj, glb, gcode)')

    parser.add_argument('--save-template', action='store_true',
                        help='Save scratch result as a reusable template')

    args = parser.parse_args()

    try:
        # Generate CAD
        if args.mode == 'template':
            if not args.template:
                raise ValueError("--template required for --mode template")
            params = parse_params(args.params)
            step_file = generate_from_template(args.template, params, args.output_dir)

        elif args.mode == 'scratch':
            if not args.brief:
                raise ValueError("--brief required for --mode scratch")
            step_file = generate_from_scratch(args.brief, args.output_dir, args.output_name)

        # Export to requested formats
        formats = [f.strip() for f in args.format.split(',')]
        exports = export_formats(step_file, formats, args.output_dir)

        print("\n✓ Generation complete!")
        print(f"Primary output (STEP): {exports.get('step', 'N/A')}")
        for fmt, path in exports.items():
            if fmt != 'step':
                print(f"{fmt.upper()}: {path}")

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
