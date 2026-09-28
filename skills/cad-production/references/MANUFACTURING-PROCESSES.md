# Manufacturing Processes: Capabilities & Constraints

## Injection Molding (Most OOB Products)

**Best For:** Bottles, caps, packaging, clamshell compacts  
**Materials:** Polypropylene (PP), Polystyrene (PS), Acrylonitrile Butadiene Styrene (ABS)  
**Cost Efficiency:** Excellent above 5K units; break-even at ~4K for typical cosmetic containers

### Design Constraints (CAD-Production Validation)

| Parameter | Minimum | Recommended | Maximum | Note |
|-----------|---------|-------------|---------|------|
| Wall Thickness | 1.0mm | 2.0–2.5mm | 4.0mm | Thin walls: slower cooling, higher cost. Thick walls: sink marks, long cycle |
| Draft Angle | 0.5° per side | 1.5–2° per side | 3° per side | Insufficient draft → difficult demolding, tool damage |
| Fillet Radius | 0.5mm | ≥1.0mm | N/A | Sharp edges → mold stress, EDM finishing cost |
| Rib Height:Width | 2:1 ratio | 2:1–3:1 | 4:1 | Thinner ribs = higher stress in mold |
| Boss Diameter | 2.0mm min | ≥4.0mm | N/A | Small bosses → sink marks, thread pull-out |
| Undercut Depth | None (ideal) | <0.5mm (special tooling) | N/A | Undercuts require side-action molds (+$1K–$3K) |

### Cycle Time Estimation
- Base: 30–40 seconds
- Wall thickness: +0.5–1.0s per 1mm additional
- Complex geometry: +10–20 seconds
- Typical cosmetic bottle: 45–60 seconds per unit

**Cost Impact:** Slower cycle = higher labor allocation

### Quality Considerations
- Parting line visibility (acceptable if on seam)
- Gate mark appearance (hide on non-visible surfaces)
- Color consistency (resin batch variation, annealing)
- Dimensional tolerance: ±0.5mm typical (tight specs require post-finishing)

### OOB Compliance
- Food contact? → Use FDA-compliant polypropylene (verify with Chemist-Agent)
- Chemical resistance? → Check formulation compatibility (Chemist-Agent approval required)
- Transparency? → Verify clarity grades (affect price, resin availability)

---

## CNC Machining (AstroPodra Hardware)

**Best For:** Precision metal hardware, custom enclosures, low-to-mid volume  
**Materials:** Aluminum (6061-T6, 7075-T6), Stainless Steel (303, 316), Brass  
**Cost Efficiency:** High-touch; economical above 100 units, best at 1K+

### Design Constraints

| Parameter | Minimum | Recommended | Maximum | Note |
|-----------|---------|-------------|---------|------|
| Thread Depth | 1.5× diameter | 1.5–2× diameter | N/A | Shallow threads = weak engagement |
| Internal Bore Diameter | 2.0mm | ≥3.0mm | N/A | Smaller bores → difficult tool access, breakage |
| Pocket Depth:Diameter | 2:1 ratio | 2:1–4:1 | 5:1 | Deep pockets = many passes, tool flex, time |
| Corner Radius | 0.5mm min | ≥1.0mm | N/A | Sharp internal corners → stress concentration |
| Surface Finish | Ra 3.2 µm | Ra 1.6–3.2 µm | Ra 0.8 µm | Finer finish = additional passes, cost increase |
| Undercut | None (ideal) | N/A | N/A | CNC cannot cut true undercuts; design with draft |
| Thread Tolerance | ±0.1mm | ±0.1–0.15mm | ±0.05mm | Tighter tolerance = slower feed, cost increase |

### Cycle Time Estimation (Per Unit)
- Simple parts (< 5 operations): 2–5 minutes
- Medium complexity (5–10 operations): 8–15 minutes
- High complexity (10+ operations, tight tolerances): 20–40 minutes
- Setup time (amortized over batch): +10–30 minutes per 100 units

**Cost Impact:** More operations = exponential time increase

### Finishing Requirements
- Anodizing (aluminum): 3–5 days, $0.50–$1.50/unit
- Plating (rose gold, chrome): 5–10 days, $1.00–$2.00/unit
- Passivation (stainless): 1–2 days, $0.20–$0.50/unit

---

## Resin Casting (Prototypes & Accent Pieces)

**Best For:** Prototypes, small batches, accent pieces with complex geometry  
**Materials:** Epoxy resin, Polyurethane, Flexible silicone  
**Cost Efficiency:** Economical at <100 units; not competitive at volume

### Design Constraints

| Parameter | Minimum | Recommended | Maximum | Note |
|-----------|---------|-------------|---------|------|
| Wall Thickness | 1.0mm | 2.0–3.0mm | 10.0mm | Thinner = faster cure, less exotherm. Thick = risk of internal voids |
| Undercuts | Allowed | Design with mold keys | N/A | Undercuts possible but complicate mold design |
| Surface Finish | Rough (as-cast) | Post-sanded Ra 1.6 µm | Polished | Surface finish requires post-processing |
| Cure Time | 12 hours | 24 hours | 48 hours | Depends on resin chemistry; affects throughput |
| Pot Life | 10 minutes | 20–30 minutes | 60 minutes | Must pour before gelation |

### Cost Model
- Mold making: $200–$500 (silicone mold from master CAD)
- Per-part material cost: $2–$8 (resin + dyes)
- Labor per part: $1–$3 (demolding, post-processing)
- **Total per-part @ 50 units:** $5–$15 (resin economical only at low volume)

---

## 3D Printing (SLS, FDM, Polyjet)

**Best For:** Rapid prototyping, custom fixtures, jigs, proof-of-concept  
**Materials:** Nylon (SLS), PLA/PETG (FDM), Resins (Polyjet), Wax (support)  
**Cost Efficiency:** Excellent for <50 units; not competitive at production volume

### Process Recommendations by Use Case

| Need | Best Process | Cost Per Unit | Lead Time | Notes |
|------|--------------|---------------|-----------|-------|
| Functional prototype | SLS Nylon | $5–$15 | 2–3 days | Strong, fine detail; minimal supports |
| Visual mockup | FDM PLA | $1–$3 | 1–2 days | Fast but visible layers; good for concept |
| High-precision detail | Polyjet/PolyJet | $10–$25 | 3–5 days | Finest detail, full-color capability |
| Elastic/flexible parts | TPU (FDM) / Flexible Resin | $8–$20 | 2–4 days | Hinges, gaskets, seals |

### Design Considerations
- **Support material cost:** SLS minimized; FDM/Polyjet significant (20–30% of part cost)
- **Layer lines:** FDM visible at <0.1mm layer height; SLS/Polyjet smoother
- **Dimensional accuracy:** SLS ±0.3mm; FDM ±0.5mm; Polyjet ±0.1mm
- **Post-processing:** All require cleanup; dyeing/coating for cosmetic finish

---

## Assembly & Labor

### Hand Assembly (GlamGrab, multi-part hinged products)

| Task | Time | Cost @ $15/hour | Notes |
|------|------|-----------------|-------|
| Hinge pin insertion | 30 seconds | $0.13 | Requires jig to ensure alignment |
| Latch spring attachment | 45 seconds | $0.19 | Depends on design; snap-fit requires press force |
| Fabric lining (hand-glued) | 2–3 minutes | $0.50–$0.75 | Variable with lining complexity and adhesive |
| Quality check (fit, function) | 1–2 minutes | $0.25–$0.50 | Mandatory for cosmetic products |
| **Total per unit** | **4–6 minutes** | **$1.07–$1.57** | *At 5K units, labor scales but quality remains critical* |

### Automated Assembly (Higher Volume)

- Vibratory bowl feeding (parts feeding): $0.05–$0.10/unit
- Pick-and-place (robotic assembly): $0.10–$0.20/unit
- Vision inspection (defect detection): $0.05–$0.10/unit
- Packing/boxing: $0.10–$0.15/unit

**ROI Threshold:** Typically 10K+ units to justify automation investment

---

## Environmental & Compliance Considerations

### FDA Food Contact (Luminescence Serums)
- Polypropylene: FDA-compliant grades available; verify resin batch
- Caps: Silicone (BPA-free); stainless steel needle
- Adhesives/coatings: Must be food-contact safe

### Chemical Compatibility (Formulation → Container)
- Deferred to **Chemist-Agent** for final approval
- Material note: "Polypropylene verified for 6-month shelf stability with [formulation name]"

### Recycling & Sustainability
- Polypropylene: #5 plastic, widely recyclable
- Aluminum: 100% recyclable, infinite reuse potential
- Velvet lining: Non-recyclable; compostable alternatives in Phase 2

---

## Vendor Scorecard Recommendations

When evaluating a manufacturer, CAD-Production can extract:
- **Quality:** Historical defect rate, dimensional consistency
- **Cost:** Actual vs. estimated per-unit by volume tier
- **Lead time:** Time from order to first unit and full volume delivery
- **Communication:** Responsiveness to design questions, revision requests

See `VENDOR-TEMPLATES.md` for quote request format.

---

## Next Phase: Process Optimization

Phase 3 roadmap includes:
- Automated draft angle analysis and design recommendations
- Wall thickness optimization for faster cycle times and lower cost
- Material substitution suggestions (e.g., lower-cost resin equivalent)
- Supplier capability matching (vendor database integration)
