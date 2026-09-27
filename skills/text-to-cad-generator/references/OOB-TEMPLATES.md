# OOB Product Templates & Quick Reference

This document shows how to parametrize OOB products using the text-to-cad-generator templates.

---

## Quick Examples

### Create a 30ml Luminescence Bottle

```bash
python scripts/generate.py \
  --mode template \
  --template bottles/round-cylinder \
  --params "diameter=35mm,height=85mm,wall_thickness=2mm,color=transparent_clear" \
  --output-dir ./models \
  --output-name luminescence-30ml \
  --format step,stl,glb
```

**Output:**
- `luminescence-30ml.step` — Manufacturing CAD
- `luminescence-30ml.stl` — 3D print (resin-ready)
- `luminescence-30ml.glb` — Web visualization

### Create a 75ml Luminescence Bottle

Same command, change params:
```bash
--params "diameter=45mm,height=120mm,wall_thickness=2.5mm,color=transparent_clear"
```

### Create a Rose Gold Dropper Cap (M24)

```bash
python scripts/generate.py \
  --mode template \
  --template caps/dropper_assembly \
  --params "thread_size=M24,bulb_diameter=15,tip_length=40" \
  --output-dir ./models \
  --output-name rose-gold-dropper-m24 \
  --format step,stl,glb
```

### Create a Label for 50ml Bottle (45mm diameter)

```bash
python scripts/generate.py \
  --mode template \
  --template packaging/label_template \
  --params "width=45,height=80,wrap_circumference=141" \
  --output-dir ./models \
  --output-name luminescence-label-50ml \
  --format step,stl,glb
```

---

## OOB Product Sizing Guide

Common OOB bottle sizes and their parameters:

### Luminescence Serum Line
| Size | Diameter | Height | Wall | Cap | Template |
|------|----------|--------|------|-----|----------|
| Travel (30ml) | 35mm | 85mm | 2.0mm | M24 dropper | round-cylinder |
| Standard (50ml) | 45mm | 120mm | 2.0mm | M24 dropper | round-cylinder |
| Deluxe (75ml) | 50mm | 140mm | 2.5mm | M24 dropper | round-cylinder |
| Luxury (100ml) | 55mm | 160mm | 2.5mm | M24 dropper | round-cylinder |

### AstroPodra Hardware Line
| Product | Base Dims | Cap | Material | Template |
|---------|-----------|-----|----------|----------|
| LED Module | Ø40mm × 25mm | Custom | Matte black | square-shoulder* |
| Display Bezel | Ø45mm × 15mm | Screw | Rose gold | round-cylinder* |
| Sensor Cap | Ø30mm × 10mm | Magnetic | Anodized | custom* |

*AstroPodra uses custom/modified templates (add to roadmap)

### GlamGrab Compacts
| Variant | Diameter | Depth | Cap Style | Material | Template |
|---------|----------|-------|-----------|----------|----------|
| Standard | Ø45mm | 20mm | Spring latch | Velvet + Gold | clamshell* |
| Travel | Ø35mm | 15mm | Spring latch | Velvet + Gold | clamshell* |
| Luxury | Ø50mm | 25mm | Magnetic latch | Velvet + Rose Gold | clamshell* |

*Clamshell template not yet implemented; add to roadmap

---

## Template Parameters Deep-Dive

### bottles/round-cylinder

**Best for:** Serum, oil, lotion bottles; standard cosmetic format

**Required parameters:**
- `diameter` (mm) — Outer diameter at body
- `height` (mm) — Total height from base to shoulder
- `wall_thickness` (mm) — Wall thickness for injection molding

**Optional parameters:**
- `shoulder_radius` (mm) — Fillet at top edge (default 5mm)
- `base_radius` (mm) — Fillet at bottom edge (default 3mm)
- `cap_thread` (str) — "M24" (default), "M27", "M30"
- `color` (str) — "clear", "frosted", "opaque_white", "opaque_black"

**Manufacturing notes:**
- Wall thickness ≥ 2.0mm for injection molding
- Wall thickness ≥ 1.5mm for resin SLA printing
- Fillets help undercuts and draft angles for mold release

### caps/dropper_assembly

**Best for:** Serum, oil dropper caps (standard M24 thread)

**Required parameters:**
- `thread_size` (str) — "M24", "M27", or "M30"
- `tip_length` (mm) — Length of dropper tip
- `tip_diameter` (mm) — Outer diameter of dropper tip
- `bulb_diameter` (mm) — Diameter of rubber squeeze bulb

**Optional parameters:**
- `cap_height` (mm) — Height of cap body
- `material_color` (str) — "natural_rubber", "white", "black"

**Manufacturing notes:**
- M24 thread is standard for cosmetic bottles (proven fit)
- Rubber bulbs are typically natural or synthetic latex (sourced separately)
- Tip diameter 3.0–4.0mm is standard for serums/oils

### packaging/label_template

**Best for:** Flat labels that wrap around cylindrical bottles

**Required parameters:**
- `width` (mm) — Circumference of wrap (or partial wrap)
- `height` (mm) — Vertical height
- `wrap_circumference` (mm) — Target bottle circumference for fit

**Optional parameters:**
- `content_area_margin` (mm) — Safe margin from edges for text/graphics

**Design notes:**
- Circumference = π × diameter
  - 35mm diameter → ~110mm circumference
  - 45mm diameter → ~141mm circumference
  - 50mm diameter → ~157mm circumference
- Leave 3–5mm margin for safe text/logo area
- Export as PDF + print template for label vendors

---

## Variant Creation Workflow

### Step 1: Choose Your Base Product
E.g., "I want a new Luminescence size (40ml)"

### Step 2: Find the Existing Template
E.g., `bottles/round-cylinder` (proven for Luminescence)

### Step 3: Calculate Parameters
For 40ml serum (midway between 30ml and 50ml):
- Volume: ~40ml (assume similar density to existing 50ml)
- Estimate diameter: ~40mm (between 35 and 45)
- Estimate height: ~105mm (scale proportionally)
- Keep wall_thickness: 2.0mm (standard)

### Step 4: Generate
```bash
python scripts/generate.py \
  --mode template \
  --template bottles/round-cylinder \
  --params "diameter=40mm,height=105mm,wall_thickness=2.0mm" \
  --output-dir ./models \
  --output-name luminescence-40ml \
  --format step,stl,glb
```

### Step 5: Validate
- Check dimensions (use CAD Viewer or calipers on prototype)
- Confirm cap fit (M24 dropper should fit)
- Verify label compatibility (calculate circumference)
- Prototype in resin if needed

### Step 6: Handoff
Provide:
- `luminescence-40ml.step` → Manufacturing
- `luminescence-40ml.stl` → Prototype lab
- `luminescence-40ml.glb` → Marketing/Photo team

---

## Creating New Templates

When you need a genuinely new product category (not a variant):

1. **Understand the geometry** — Draw a 2D profile, identify key dimensions
2. **Parametrize** — Which dimensions should change? (size, height, diameter, material, color)
3. **Create template file** — `scripts/templates/{category}/{product}.py`
4. **Implement `generate(params)`** — Use build123d to create the shape
5. **Implement `get_parameters()`** — Define parameter schema with defaults and ranges
6. **Test** — Run the template with sample params, validate output
7. **Document** — Add entry to this guide with sizing examples

**Example: Creating a Square-Shoulder Bottle**

```python
# templates/bottles/square_shoulder.py

def generate(params: dict) -> Shape:
    width = params.get("width", 40)
    depth = params.get("depth", 40)
    height = params.get("height", 100)
    wall = params.get("wall_thickness", 2)
    shoulder_width = params.get("shoulder_width", 30)
    
    # Body: Box shape
    body = Box(width, depth, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    
    # Hollow out
    inner_box = Box(width - 2*wall, depth - 2*wall, height - 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    bottle = body - inner_box
    
    # Add shoulder transition
    # ... (add geometry for shoulder narrowing)
    
    return bottle
```

---

## Roadmap: Templates to Add

- [ ] `bottles/square-shoulder` — Compact square bottles
- [ ] `bottles/oval-body` — Ergonomic oval shape
- [ ] `caps/screw-cap-standard` — Simple threaded caps
- [ ] `packaging/clamshell-compact` — Hinged compact case
- [ ] `packaging/box-base` — Standard cosmetic boxes
- [ ] `hardware/hinges` — Parametric hinges (for clamshells)
- [ ] `hardware/latches` — Spring/magnetic latches
- [ ] `hardware/astropodra-case` — AstroPodra enclosure
- [ ] `hardware/glamgrab-insert` — GlamGrab cartridge

---

## Integration with Manufacturing

### For Injection Molding (bottles, caps)

Export: **STEP + Technical Drawings (PDF)**

```bash
python scripts/generate.py --format step --include-drawings yes
```

Provide to mold vendor:
- STEP file (CAD geometry)
- Technical drawings (2D projections + tolerances)
- Material spec (e.g., "polypropylene, transparent")
- Wall thickness validation (≥ 2.0mm recommended)

### For 3D Printing (prototypes)

Export: **STL + Print Settings Document**

```bash
python scripts/generate.py --format stl
```

Provide to lab:
- STL file (optimized for resin/FDM)
- Print settings (orientation, support strategy, material)
- Assembly instructions (if multi-part)

### For Packaging & Labels

Export: **PDF (for label vendor) + GLB (for mockups)**

```bash
python scripts/generate.py --format pdf,glb
```

Provide to vendor:
- PDF flat label (ready for printing)
- Dimensions + wrap circumference
- Color/finish spec

---

## Testing Template Parameters

Use the test harness:

```bash
cd skills/text-to-cad-generator
python scripts/templates/bottles/round_cylinder.py
# Creates test-bottle.step
```

Then visualize in CAD Viewer:
```bash
python scripts/cad-viewer.py test-bottle.step
```

---

*OOB Product Templates v1.0 — Parametrized CAD generation for rapid variant creation and manufacturing handoff.*
