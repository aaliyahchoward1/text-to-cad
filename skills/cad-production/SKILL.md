---
name: cad-production
description: Generate production-ready manufacturing packages from STEP files — technical drawings, BOMs, cost estimates, manufacturability validation, and vendor coordination for injection molding, CNC, and assembly workflows.
---

# CAD Production Workflow

## Manufacturing Intelligence from CAD

Transform 3D CAD models into complete vendor-ready manufacturing packages:

1. **Technical Drawing Generation** — Orthographic views, dimensions, tolerances, material specs (PDF)
2. **Bill of Materials (BOM)** — Part lists, material costs, supplier recommendations, volume pricing
3. **Manufacturability Validation** — Wall thickness, undercuts, draft angles, threading, fit constraints
4. **Cost Estimation** — Per-unit pricing by volume tier (1K/5K/10K/50K+ units), mold amortization, labor overhead
5. **Assembly Instructions** — Step-by-step diagrams for multi-part products (caps, hinges, fasteners)
6. **Vendor Coordination Package** — Submission-ready archive (STEP + drawing + BOM + specs + quote template)

Use this skill when Design-Generator-Agent produces a STEP file and you need to prepare manufacturing quotes, validate producibility, or estimate costs for production runs.

---

## Use This Skill When

- Design-Generator-Agent delivers a STEP file for a new product (bottle, cap, hardware, compact)
- You need technical drawings for a mold vendor or CNC shop
- You're estimating per-unit costs across volume tiers (prototyping to mass production)
- You need to validate that a design is manufacturable before vendor submission
- You're preparing a complete vendor package for supplier quotes
- Ops-Agent needs cost data to decide on material substitutions or volume commitments
- Product-Agent is evaluating the manufacturability and cost of a design iteration

## Don't Use This Skill For

- Render-only visualization (use CAD Viewer or design rendering tools instead)
- Design iteration or CAD editing (use Design-Generator-Agent or CAD tools)
- Prototype testing or material certification (consult manufacturing engineer or chemist)
- Final regulatory compliance (FDA labeling, material certifications) — flag compliance items but defer approval to legal/regulatory

---

## How It Works

### Input: STEP File + Product Brief

The skill expects:
- **STEP file** — 3D CAD geometry (from Design-Generator-Agent)
- **Product brief** — Category (bottle/hardware/compact), size, material, finish, manufacturing process hint

**Example input:**
```
Product: "Luminescence 50ml bottle"
STEP file: /models/luminescence-50ml.step
Category: bottle
Material: polypropylene (transparent)
Manufacturing: injection molding
Cap style: M24 dropper assembly
```

### Phase 1: Technical Drawing Generation

Parses the STEP geometry and produces publication-ready technical drawings:

```bash
python scripts/generate_drawing.py \
  --step-file luminescence-50ml.step \
  --product-name "luminescence-50ml" \
  --category bottle \
  --material "polypropylene" \
  --output-format pdf
```

**Output:** `luminescence-50ml-technical-drawing.pdf` (2–4 pages)
- Orthographic projections (front, top, side; isometric reference)
- Dimension callouts (critical diameters, heights, wall thickness)
- Tolerance annotations per manufacturing process
- Material/finish note block
- Thread/cap fit detail (if applicable)

### Phase 2: Bill of Materials (BOM) Creation

Analyzes the design to extract part lists and estimate costs:

```bash
python scripts/generate_bom.py \
  --step-file luminescence-50ml.step \
  --product-name "luminescence-50ml" \
  --category bottle \
  --volume-tiers 1k,5k,10k,50k \
  --output-format csv,pdf,xlsx
```

**Outputs:**
- `luminescence-50ml-bom.csv` — Machine-readable part list with supplier references
- `luminescence-50ml-bom.pdf` — Summary table with per-unit costs
- `luminescence-50ml-cost-estimate.xlsx` — Full cost breakdown by volume tier

**What it estimates:**
- Material volume and per-unit cost ($/g × volume)
- Mold/tooling cost amortized across units
- Labor, assembly, packaging, and overhead by percentage
- Per-unit pricing at each tier (1K → 50K+ units)
- Gross margin at wholesale price point

### Phase 3: Manufacturability Validation

Checks the design against manufacturing constraints:

```bash
python scripts/validate_manufacturability.py \
  --step-file luminescence-50ml.step \
  --manufacturing-process injection_molding \
  --material polypropylene
```

**Validation checks:**
- Wall thickness (≥2.0mm for injection molding, ≥1.5mm for resin, ≥1.0mm for 3D print)
- Draft angle (≥1–2° per side for molded parts)
- Undercut detection (flags features requiring side-action molds or increased cost)
- Fillet radius (sharp edges flag as increased tooling cost)
- Threading engagement depth (M24 = ≥1.5× diameter = 36mm minimum)
- Feature complexity (multi-cavity molds, thin walls, small details)

**Output:** Validation report with risk flags
```
✓ Wall thickness OK (2.0mm nominal)
✓ Thread depth OK (M24, 40mm engagement)
✓ No undercuts detected
⚠ Fillet radius <2mm on shoulder — may require EDM finishing (+$500 tooling)
⚠ Thin wall (1.8mm) on cap flange — recommend injection at slower cooling rate
```

### Phase 4: Cost Estimation by Volume

Generates per-unit pricing across all volume tiers:

```bash
python scripts/estimate_costs.py \
  --bom luminescence-50ml-bom.csv \
  --manufacturing-process injection_molding \
  --tooling-estimate 7500 \
  --volume-tiers 1k,5k,10k,50k,100k
```

**Output table:**
| Volume Tier | Tooling | Material | Labor | Overhead | Per-Unit | Margin @ $2.00 |
|---|---|---|---|---|---|---|
| 1K units | $7.50/unit | $0.45 | $0.15 | $0.30 | $8.40 | -320% |
| 5K units | $1.50/unit | $0.45 | $0.12 | $0.25 | $2.32 | -16% |
| 10K units | $0.75/unit | $0.45 | $0.10 | $0.20 | $1.50 | 25% |
| 50K units | $0.15/unit | $0.42 | $0.08 | $0.18 | $0.83 | 58% |

*Note: Assumes wholesale price point of $2.00/unit; adjust retail pricing based on channel.*

### Phase 5: Assembly Instructions (Multi-Part Products)

For hinged, capped, or multi-assembly products:

```bash
python scripts/generate_assembly_instructions.py \
  --step-file glamgrab-compact-50mm.step \
  --product-name glamgrab-compact \
  --assembly-type hinged_clamshell
```

**Output:** `glamgrab-compact-assembly-instructions.pdf`
- Step-by-step illustrated guide (3–8 steps typically)
- Part reference diagrams with labels
- Critical specs (hinge pin fit, snap engagement force, alignment tolerances)
- Quality checkpoints (fit test, function test, cosmetic inspection)
- Assembly sequence for manufacturing and final QA

### Phase 6: Vendor Coordination Package

Compiles everything into a submission-ready archive:

```bash
python scripts/prepare_vendor_package.py \
  --product-name luminescence-50ml \
  --step-file luminescence-50ml.step \
  --drawing luminescence-50ml-technical-drawing.pdf \
  --bom luminescence-50ml-bom.csv \
  --cost-estimate luminescence-50ml-cost-estimate.xlsx \
  --output-format zip
```

**Output:** `luminescence-50ml-vendor-package.zip`

**Contents:**
- STEP file (primary CAD)
- Technical drawing (PDF, 2–4 pages)
- BOM (CSV, for importing into vendor systems)
- Cost estimate (XLSX, with per-unit breakdown)
- Material specification sheet
- Vendor quote request template
- Cover letter with quality requirements, timeline, volume expectations

**Ready to send to:**
- Injection molding vendors (for bottles, caps, packaging)
- CNC shops (for precision metal hardware)
- Mold vendors (for multi-part assemblies)
- Contract manufacturers (turnkey solutions)

---

## Workflow Example: New Luminescence 40ml Bottle

**Input:** Design-Generator-Agent delivers STEP file at T+30min

```
Product: Luminescence Hair Oil 40ml
Brief: 40ml transparent bottle, M24 dropper cap, 1.8mm wall, polypropylene
STEP: /models/luminescence-40ml.step
```

**T+35min — Technical Drawing:**
```bash
python scripts/generate_drawing.py \
  --step-file luminescence-40ml.step \
  --product-name luminescence-40ml \
  --category bottle \
  --material polypropylene \
  --manufacturing injection_molding
```
→ `luminescence-40ml-technical-drawing.pdf` (2 pages, orthographic + M24 detail)

**T+40min — BOM & Cost Estimate:**
```bash
python scripts/generate_bom.py \
  --step-file luminescence-40ml.step \
  --volume-tiers 1k,5k,10k,50k \
  --material polypropylene \
  --output-format csv,xlsx
```
→ Estimates: $0.55/unit @ 10K (vs. market $0.80–$1.20 → margin 45–55% at $2.00 wholesale)

**T+43min — Manufacturability Validation:**
```bash
python scripts/validate_manufacturability.py \
  --step-file luminescence-40ml.step \
  --manufacturing injection_molding
```
→ ✓ Ready for manufacturing (wall thickness OK, M24 thread fit OK, no undercuts)

**T+45min — Vendor Package:**
```bash
python scripts/prepare_vendor_package.py \
  --product-name luminescence-40ml \
  --step-file luminescence-40ml.step \
  --drawing luminescence-40ml-technical-drawing.pdf \
  --bom luminescence-40ml-bom.csv \
  --cost-estimate luminescence-40ml-cost-estimate.xlsx
```
→ `luminescence-40ml-vendor-package.zip` ready to email to mold vendors

**T+2 days — Vendor Quotes:**
Ops-Agent submits package to 3 mold vendors. Vendors respond with quotes:
- Tooling: $6K–$8K
- Per-unit: $0.48–$0.52 @ 10K (matches estimate within 5%)
- Lead time: 4 weeks to first shot

**T+5 days:**
- Product-Agent reviews cost impact: $0.50/unit @ 10K = 75% margin at $2.00 wholesale ✓
- Ops-Agent selects vendor and places order
- CEO-Agent clears product for production launch

---

## Integration with OOB Agents

### Design-Generator-Agent → CAD-Production

When Design-Generator-Agent completes a STEP file:

```
Design-Generator-Agent (to CAD-Production-Agent):
"STEP file ready for manufacturing review.
File: /models/luminescence-40ml.step
Brief: 40ml transparent bottle, M24 cap, polypropylene, injection molding
Please generate technical drawing, BOM, cost estimate, and vendor package."
```

### CAD-Production → Ops-Agent

When vendor package is ready:

```
CAD-Production-Agent (to Ops-Agent):
"Manufacturing package prepared for luminescence-40ml.
Vendor package: /packages/luminescence-40ml-vendor-package.zip
Cost estimate: $0.50/unit @ 10K volume
Status: ✓ Ready for vendor submission
Next: Submit to mold vendors for quotes"
```

### CAD-Production ↔ Product-Agent

When manufacturability concerns arise:

```
CAD-Production-Agent (to Product-Agent):
"Validation flagged: Wall thickness 1.8mm on bottle shoulder.
Recommendation: Increase to 2.0mm for consistent injection molding.
Impact: +$0.02/unit (faster cooling, better part quality)"

Product-Agent (response):
"Approved — increase wall to 2.0mm. Please regenerate BOM and cost estimate."
```

---

## Supported Product Families

### Luminescence Serum Line
- Bottles: 30ml, 50ml, 75ml, 100ml (injection molding)
- Caps: M24 dropper assemblies (standard across sizes)
- Labels: Circumference-based wraps
- Typical cost: $0.45–$0.65/unit @ 10K volume

### AstroPodra Hardware
- LED enclosures, display bezels, sensor housings (CNC machining)
- Material: Aluminum (anodized), steel, resin accents
- Typical cost: $8–$15/unit @ 1K volume (precision manufacturing)
- Process: CNC + metal finishing (anodizing, plating)

### GlamGrab Compacts
- Clamshells: 35mm, 45mm, 50mm (injection molding + assembly)
- Components: Shell, hinge pins, latch spring, fabric lining
- Typical cost: $0.65–$0.95/unit @ 5K volume
- Process: Multi-part injection + insert molding + hand assembly

---

## Requirements

- Python 3.10+
- build123d (CAD kernel)
- numpy (geometry analysis)
- cadquery (STEP parsing)
- reportlab (PDF generation)
- openpyxl (Excel output)

Install with:
```bash
pip install -r requirements.txt
```

---

## Success Metrics

| Metric | Target | Tracked |
|--------|--------|---------|
| Time from STEP → vendor package | <30 min | Per-workflow |
| BOM accuracy vs. actual cost | ±5% | Post-first-quote |
| Manufacturability issue detection | >90% catch rate | Per-product |
| Vendor cost vs. estimate | ±10% match | Per-quote |
| Drawing completeness (vendor feedback) | 100% usable | Vendor survey |

---

## Next Steps & Roadmap

### Phase 1 (MVP — Now)
- ✓ Technical drawing generation (2D orthographic + tolerances)
- ✓ BOM creation (CSV + cost rollup)
- ✓ Manufacturability validation (wall thickness, threading, undercuts)
- ✓ Cost estimation (per-unit by volume tier)
- ✓ Vendor package assembly (STEP + drawing + BOM + specs)

### Phase 2 (Week 2)
- Assembly instruction diagrams (multi-part products)
- Material compatibility database (integrate Chemist-Agent)
- Vendor database (approved suppliers, capability matrix)
- Actual vs. estimated cost tracking (refine model)

### Phase 3 (Month 2)
- G-code analysis for CNC/3D print path optimization
- CAD version control and change tracking
- Regulatory compliance checks (FDA container specs)
- Cost optimization suggestions (geometry tweaks, material swaps)

---

## Questions?

See the `references/` directory for:
- `OOB-PRODUCT-SPECS.md` — Product family specifications and defaults
- `MANUFACTURING-PROCESSES.md` — Process capabilities, tolerances, lead times
- `COST-MODEL.md` — Detailed cost calculation methodology
- `VENDOR-TEMPLATES.md` — Quote request templates by process type
