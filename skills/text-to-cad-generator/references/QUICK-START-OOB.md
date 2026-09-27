# Quick Start: OOB Product CAD Generation

Copy-paste commands for generating OOB product variants.

---

## Luminescence Serum Bottles

### 30ml Travel Size
```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=35mm,height=85mm,wall_thickness=2.0mm,cap_thread=M24,color=transparent" \
  --output-dir ./models --output-name luminescence-30ml --format step,stl,glb
```

### 50ml Standard
```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=45mm,height=120mm,wall_thickness=2.0mm,cap_thread=M24,color=transparent" \
  --output-dir ./models --output-name luminescence-50ml --format step,stl,glb
```

### 75ml Deluxe
```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=50mm,height=140mm,wall_thickness=2.5mm,cap_thread=M24,color=transparent" \
  --output-dir ./models --output-name luminescence-75ml --format step,stl,glb
```

### 100ml Luxury
```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=55mm,height=160mm,wall_thickness=2.5mm,cap_thread=M24,color=transparent" \
  --output-dir ./models --output-name luminescence-100ml --format step,stl,glb
```

---

## Luminescence Frosted (All Sizes)

### 50ml Frosted White
```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=45mm,height=120mm,wall_thickness=2.0mm,cap_thread=M24,color=frosted" \
  --output-dir ./models --output-name luminescence-50ml-frosted --format step,stl,glb
```

### 75ml Frosted White
```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=50mm,height=140mm,wall_thickness=2.5mm,cap_thread=M24,color=frosted" \
  --output-dir ./models --output-name luminescence-75ml-frosted --format step,stl,glb
```

---

## Dropper Caps (M24 Standard)

### Standard Natural Rubber
```bash
python scripts/generate.py --mode template --template caps/dropper_assembly \
  --params "thread_size=M24,bulb_diameter=15,tip_length=40,tip_diameter=3.5,material_color=natural_rubber" \
  --output-dir ./models --output-name dropper-cap-m24-natural --format step,stl,glb
```

### Rose Gold Hardware
```bash
python scripts/generate.py --mode template --template caps/dropper_assembly \
  --params "thread_size=M24,bulb_diameter=15,tip_length=40,tip_diameter=3.5,material_color=rose_gold" \
  --output-dir ./models --output-name dropper-cap-m24-rose-gold --format step,stl,glb
```

### White Bulb
```bash
python scripts/generate.py --mode template --template caps/dropper_assembly \
  --params "thread_size=M24,bulb_diameter=15,tip_length=40,tip_diameter=3.5,material_color=white" \
  --output-dir ./models --output-name dropper-cap-m24-white --format step,stl,glb
```

---

## Labels (Wrapping)

### For 30ml (35mm Ø)
```bash
python scripts/generate.py --mode template --template packaging/label_template \
  --params "width=35,height=70,wrap_circumference=110" \
  --output-dir ./models --output-name label-30ml-luminescence --format step,stl,glb
```

### For 50ml (45mm Ø)
```bash
python scripts/generate.py --mode template --template packaging/label_template \
  --params "width=45,height=80,wrap_circumference=141" \
  --output-dir ./models --output-name label-50ml-luminescence --format step,stl,glb
```

### For 75ml (50mm Ø)
```bash
python scripts/generate.py --mode template --template packaging/label_template \
  --params "width=50,height=100,wrap_circumference=157" \
  --output-dir ./models --output-name label-75ml-luminescence --format step,stl,glb
```

---

## Custom Variants

### Custom Size (Example: 60ml)
Diameter estimate: 48mm (interpolate between 50ml and 75ml)
Height estimate: 130mm (interpolate proportionally)

```bash
python scripts/generate.py --mode template --template bottles/round-cylinder \
  --params "diameter=48mm,height=130mm,wall_thickness=2.0mm,cap_thread=M24,color=transparent" \
  --output-dir ./models --output-name luminescence-60ml-custom --format step,stl,glb
```

### Custom Color (Opaque Options)
```bash
# Opaque white
--params "...color=opaque_white" 

# Opaque black
--params "...color=opaque_black"

# Transparent (default)
--params "...color=transparent"
```

---

## Commands Used

### Generate (Template)
```bash
python scripts/generate.py \
  --mode template \
  --template {category}/{template_name} \
  --params "key=value,key2=value2" \
  --output-dir ./models \
  --output-name {filename} \
  --format step,stl,glb
```

### Generate (Scratch)
```bash
python scripts/generate.py \
  --mode scratch \
  --brief "Natural language product description" \
  --output-dir ./models \
  --output-name {filename} \
  --format step,stl,glb \
  --save-template yes
```

### List Available Templates
```bash
python scripts/list-templates.py
```

### Validate Geometry
```bash
python scripts/validate.py --step {output.step} --brief "Your CAD brief"
```

---

## Output Files

For each product, you get:

- **{name}.step** — CAD for manufacturing (send to vendor)
- **{name}.stl** — 3D print model (send to prototype lab)
- **{name}.glb** — Visualization (send to Photo-Agent for mockups)

---

## Common Mistakes

### "Wall too thin" (CAD validation fails)
**Solution:** Increase wall_thickness to ≥ 2.0mm
```bash
# Wrong: wall_thickness=1.5mm
# Right: wall_thickness=2.0mm
```

### "Circumference doesn't match"
**Solution:** Use formula: Circumference = π × diameter
```
35mm Ø → 109.96mm circumference → use 110mm
45mm Ø → 141.37mm circumference → use 141mm
50mm Ø → 157.08mm circumference → use 157mm
```

### "Cap doesn't fit"
**Solution:** Ensure cap_thread matches bottle thread
```bash
# Round-cylinder uses M24 by default
# Make sure dropper_assembly cap_thread=M24
```

---

## Next Steps

1. **Generate your product** — Pick a size from above, run the command
2. **Check output** — Verify {name}.step was created
3. **Handoff** → Manufacturing gets STEP, Lab gets STL, Photo gets GLB
4. **Iterate** — If parameters need adjustment, regenerate with new params

---

## Need Help?

- **Template not found?** → `python scripts/list-templates.py`
- **Parameter format?** → See `references/OOB-TEMPLATES.md`
- **Validation error?** → Check wall thickness (≥2.0mm), diameter/height proportions
- **Custom product?** → Use `--mode scratch` for new designs

---

*Quick Start v1.0 — Copy-paste commands for OOB product CAD generation*
