---
name: text-to-cad-generator
description: Generate 3D CAD models from natural-language briefs using parametrized templates or scratch generation. Export to STEP, STL, G-code, and GLB. Designed for product design, prototyping, and manufacturing workflows.
---

# Text-to-CAD Generator
## Natural-Language CAD Generation + Multi-Format Export

---

## Purpose

Transform product ideas, specifications, and requests into **production-ready 3D CAD models** with a single workflow:

1. **Template-Based Generation** — Use OOB product templates (bottles, caps, packaging) for fast parametrized variants
2. **Scratch Generation** — Build new geometries from natural-language specs using build123d
3. **Multi-Format Export** — Generate STEP (manufacturing), STL/OBJ (printing), G-code (CNC/3D printer), GLB (visualization)
4. **Validation & Documentation** — Auto-validate dimensions, generate assembly instructions, create BOMs

Use this skill when you need CAD from natural language, parametrized product variants, or rapid prototyping exports.

---

## Use This Skill When

- Product-Agent requests a CAD model of a new product variant
- Design-Generator-Agent needs to parametrize an existing bottle, cap, or packaging design
- A maker/lab needs STL files for 3D printing a prototype
- Manufacturing needs STEP + BOM + technical drawings for tooling
- Photo-Agent needs a GLB model for 3D rendering mockups
- A user wants to explore design variations quickly (parameter sweeps)

## Don't Use This Skill For

- Render-only concept art (use render skills instead)
- Simple geometry that doesn't need CAD (use implicit-cad or draw tools)
- 2D graphics or label design (use design/graphics tools)
- Engineering certification or compliance validation (consult manufacturing engineer)

---

## How It Works

### Mode 1: Template-Based Parametrization (Recommended for Variants)

When you're creating a new size, color, or variant of an existing OOB product:

```bash
python scripts/generate.py \
  --mode template \
  --template bottles/round-cylinder \
  --params "diameter=55mm,height=140mm,wall_thickness=2.5mm,color=transparent_blue" \
  --output-dir ./models \
  --format step,stl,glb
```

**What happens:**
1. Load the template (e.g., `templates/bottles/round-cylinder.py`)
2. Map parameters to template variables
3. Generate CAD using build123d
4. Validate dimensions and geometry
5. Export to all requested formats
6. Return STEP (primary), STL (printing), GLB (visualization)

**Template Library:**
- `bottles/round-cylinder` — Standard round bottles (proven for 30ml–500ml)
- `bottles/square-shoulder` — Compact square-shouldered bottles
- `caps/dropper-assembly` — M24 dropper assembly (standard)
- `caps/pump-dispenser` — Cosmetic pump dispenser (1ml/pump)
- `packaging/label-template` — Label wraps (customizable width/height)
- `packaging/box-base` — Cosmetic boxes (die-cut friendly)

### Mode 2: Scratch Generation (For New Products)

When designing something completely new:

```bash
python scripts/generate.py \
  --mode scratch \
  --brief "Solid perfume compact, clamshell design, 45mm diameter, hinged assembly, rose gold latch" \
  --output-dir ./models \
  --format step,stl,glb \
  --save-template yes
```

**What happens:**
1. Parse the natural-language brief
2. Extract dimensions, features, constraints
3. Generate build123d Python source code
4. Build the CAD model
5. Validate geometry (closed solids, wall thickness, assembly fit)
6. Export to all formats
7. Optionally save as a reusable template for future variants

**Scratch generation supports:**
- Parametric geometry (cylinders, boxes, complex shapes)
- Assemblies (multiple parts, hinges, threaded connections)
- Surface features (fillets, chamfers, draft angles)
- Functional constraints (fit tolerances, threading, snap features)

---

## Workflow

### Step 1: Receive & Parse Brief

When you receive a product request, extract:

- **Geometry** — Shape, dimensions, proportions
- **Material/Finish** — Color, surface texture, material class
- **Functional constraints** — Assembly fits, threading, snap features, articulation
- **Manufacturabl constraints** — Target method (injection molding, 3D print, CNC), wall thickness, tolerances
- **Export targets** — What formats the stakeholder needs (STEP for vendor, STL for proto, GLB for mockup)

**Example brief:**
> Lavender Serum Bottle, 50ml
> - Cylindrical body, 45mm diameter, 120mm height
> - Transparent resin (glass-like appearance)
> - M24 dropper cap (standard)
> - 2mm wall thickness
> - Label area: 45×80mm, positioned 15mm from base
> - Export: STEP (manufacturing), STL (resin print proto), GLB (packaging mockup)

### Step 2: Decide: Template or Scratch?

- **Template?** — Does this match an existing OOB product or variant?
  - Yes → Use template mode with parameter overrides
  - No → Use scratch mode
  
- **Reuse?** — If scratch, should this become a template for future variants?
  - Yes → Add `--save-template yes` flag

### Step 3: Generate

Run the appropriate generation command (template or scratch).

### Step 4: Validate

Automatically run checks:
- **Geometry valid?** Closed solids, no self-intersections
- **Dimensions match brief?** Measure critical features
- **Assembly fit?** Test cap threading, hinge articulation
- **Manufacturability?** Wall thickness, feature size, undercuts

**Manual validation steps:**
```bash
python scripts/validate.py --step <output.step> --brief "your CAD brief"
```

### Step 5: Export

Generate all requested formats:
- **STEP** — Manufacturing-grade CAD for tooling
- **STL/OBJ** — 3D printing (resin, FDM, SLS)
- **G-code** — CNC or 3D printer direct output
- **GLB** — Visualization, mockups, presentations

**Export command:**
```bash
python scripts/export.py --source <output.step> --format step,stl,obj,gcode,glb
```

### Step 6: Handoff & Visualization

Return:
- **STEP file** (for manufacturing)
- **STL file** (for prototyping)
- **GLB file** (for visualization)
- **CAD Viewer link** (hand off to `$cad-viewer` skill)
- **Assembly instructions** (if assembly required)
- **BOM** (if multi-part)

---

## Templates & Customization

### Template Structure

Each template is a Python file in `scripts/templates/` with:

```python
# Example: templates/bottles/round_cylinder.py

from build123d import *
import cadpy

def generate(params: dict) -> Shape:
    """
    Generate a cylindrical bottle.
    
    Params:
    - diameter (float): mm, outer diameter
    - height (float): mm, total height
    - wall_thickness (float): mm
    - shoulder_radius (float): mm, fillet at shoulder
    - cap_thread (str): 'M24' (standard) or custom
    """
    
    diameter = params.get("diameter", 45)
    height = params.get("height", 120)
    wall = params.get("wall_thickness", 2)
    shoulder = params.get("shoulder_radius", 5)
    cap_thread = params.get("cap_thread", "M24")
    
    # Build body
    body = Cylinder(radius=diameter/2, height=height)
    
    # Hollow out
    interior = Cylinder(radius=(diameter/2 - wall), height=height)
    bottle = body - interior
    
    # Add shoulder fillet
    bottle = fillet(bottle, shoulder)
    
    # Add cap threading (simplified)
    # ... (threading code)
    
    return bottle

def get_parameters():
    """Return template parameter schema."""
    return {
        "diameter": {"type": "float", "unit": "mm", "default": 45},
        "height": {"type": "float", "unit": "mm", "default": 120},
        "wall_thickness": {"type": "float", "unit": "mm", "default": 2},
        "shoulder_radius": {"type": "float", "unit": "mm", "default": 5},
        "cap_thread": {"type": "str", "options": ["M24", "M27", "M30"]},
    }
```

### Creating New Templates

To add a new template:

1. Create a file in `scripts/templates/{category}/{template_name}.py`
2. Implement `generate(params: dict) -> Shape`
3. Implement `get_parameters() -> dict` (schema)
4. Test with sample parameters
5. Document in `references/templates.md`

---

## Export Formats

### STEP (Primary)
- **Format:** .step, .stp
- **Use:** Manufacturing, CAD handoff, design review
- **Generated automatically** from all modes
- **Includes:** Part hierarchy, material specs, assembly structure

### STL / OBJ (Printing)
- **Format:** .stl (binary), .obj (mesh)
- **Use:** 3D printing (resin, FDM, SLS), prototyping
- **Automatically generated** from STEP
- **Optimized for:** Print orientation, support reduction, layer adhesion

### G-code (CNC / 3D Printer)
- **Format:** .gcode, .nc, .tap (depending on machine)
- **Use:** Direct machine input (3D printer, CNC mill/lathe)
- **Generation:** Optional, requires machine profile
- **Profiles:** Common printer models (Prusa i3, Formlabs Form 3, Sherline CNC mill)

### GLB (Visualization)
- **Format:** .glb (glTF binary, web-ready)
- **Use:** Web mockups, presentations, CAD Viewer, marketing
- **Generated automatically** from STEP
- **Includes:** Materials, colors, textures

### Technical Drawings (Optional)
- **Format:** .pdf (2D projections + dimensions)
- **Use:** Manufacturing documentation, assembly guides
- **Generated on request:** `--include-drawings yes`

---

## Multi-Export Workflow Example

Generate a bottle and export to all formats:

```bash
python scripts/generate.py \
  --mode template \
  --template bottles/round-cylinder \
  --params "diameter=50mm,height=120mm,wall_thickness=2mm" \
  --output-dir ./models \
  --output-name luminescence-50ml \
  --format step,stl,obj,glb,gcode \
  --gcode-profile "prusa-i3-mk3s" \
  --include-drawings yes
```

**Output files:**
- `luminescence-50ml.step` — Manufacturing CAD
- `luminescence-50ml.stl` — 3D print (optimized for resin)
- `luminescence-50ml.obj` — Mesh (for rendering)
- `luminescence-50ml.glb` — Web visualization
- `luminescence-50ml.gcode` — Prusa print profile
- `luminescence-50ml-drawings.pdf` — Technical 2D views + dimensions

---

## OOB Product Templates

Ready-to-use templates for OOB products:

### Bottles
- **Round Cylinder** (`bottles/round-cylinder`)
  - Common OOB format; proven for 30ml–500ml
  - Params: diameter, height, wall_thickness, shoulder_radius, cap_thread

- **Square Shoulder** (`bottles/square-shoulder`)
  - Compact, shelf-friendly; used for compact serums
  - Params: width, depth, height, shoulder_width, cap_thread

- **Oval Body** (`bottles/oval-body`)
  - Ergonomic grip; used for body oils, massage bottles
  - Params: major_axis, minor_axis, height, wall_thickness

### Caps & Closures
- **Dropper Assembly** (`caps/dropper-assembly`)
  - Standard cosmetic dropper; M24 threaded
  - Params: thread_size, tip_length, tip_diameter, material_color

- **Pump Dispenser** (`caps/pump-dispenser`)
  - Cosmetic pump; ~1ml per stroke
  - Params: pump_stroke, tube_depth, nozzle_size, material_color

- **Screw Cap** (`caps/screw-cap`)
  - Standard threaded cap
  - Params: thread_size, cap_height, flange_diameter

### Packaging
- **Label Template** (`packaging/label-template`)
  - Flat label for wrapping around bottles
  - Params: width, height, wrap_circumference

- **Box Base** (`packaging/box-base`)
  - Standard cosmetic box (foldable)
  - Params: inner_width, inner_depth, inner_height, wall_thickness

- **Sleeve Insert** (`packaging/sleeve-insert`)
  - Branded sleeve wrap
  - Params: sleeve_length, sleeve_height, wrap_circumference

---

## Troubleshooting

### "Template not found"
Check available templates:
```bash
python scripts/list-templates.py
```

### "Geometry invalid" (self-intersections, holes)
- Increase wall thickness
- Reduce feature complexity (add fillets, reduce sharp corners)
- Check parameter bounds (use `get_parameters()` to see valid ranges)

### "Export failed"
- Ensure STEP was generated successfully
- Check disk space
- Verify G-code profile name (use `--list-gcode-profiles`)

### "Assembly fit test failed" (cap doesn't thread, hinge won't articulate)
- Increase tolerances (loosen fit)
- Check threading params (pitch, diameter)
- Validate hinge parameters (pivot radius, clearance)

---

## Integration with Other Skills

### With `$cad` skill
- `$cad` performs detailed CAD inspection, measurement, validation
- `text-to-cad-generator` handles rapid generation and multi-export
- **Workflow:** Generate with this skill → Hand off to `$cad` for detailed review/modification

### With `$cad-viewer` skill
- Always hand off STEP, STL, and GLB to `$cad-viewer` for live visualization
- Use returned viewer links in final response

### With Design-Generator-Agent (in oob-agents)
- Agent receives product briefs from Product-Agent, Content-Agent, CEO-Agent
- Agent coordinates with this skill for CAD generation
- Agent handles parameter extraction, template selection, handoff orchestration

---

## Files & Structure

```
text-to-cad/skills/text-to-cad-generator/
├── SKILL.md                           # This file
├── scripts/
│   ├── generate.py                    # Main generation script
│   ├── validate.py                    # Geometry validation
│   ├── export.py                      # Multi-format export
│   ├── list-templates.py              # List available templates
│   └── templates/
│       ├── bottles/
│       │   ├── round_cylinder.py
│       │   ├── square_shoulder.py
│       │   └── oval_body.py
│       ├── caps/
│       │   ├── dropper_assembly.py
│       │   ├── pump_dispenser.py
│       │   └── screw_cap.py
│       └── packaging/
│           ├── label_template.py
│           ├── box_base.py
│           └── sleeve_insert.py
├── references/
│   ├── templates.md                   # Template catalog & parameters
│   ├── export-formats.md              # Export format details
│   └── cad-brief-template.md          # How to write CAD briefs
├── agents/
│   └── text-to-cad-generator.md       # Skill agent prompt
└── requirements.txt
```

---

## Quick Start

Generate a bottle variant in 3 commands:

```bash
# 1. Check available templates
python scripts/list-templates.py

# 2. Generate with template
python scripts/generate.py \
  --mode template \
  --template bottles/round-cylinder \
  --params "diameter=50mm,height=120mm" \
  --output-dir ./models \
  --format step,stl,glb

# 3. Visualize (hand off to CAD Viewer)
# Return the GLB link and STEP link to the user
```

---

## Next Steps

1. **Build template library** — Parametrize existing OOB products
2. **Validate manufacturing** — Test template exports with manufacturing partners
3. **Create assembly templates** — Hinge, threaded, snap-fit assemblies
4. **Add GCode support** — Integrate with specific printer/CNC models
5. **Create design gallery** — Document successful product variants

---

*text-to-cad-generator v1.0 — Bridges natural language and CAD generation. Designed for rapid prototyping, manufacturing handoff, and design iteration.*
