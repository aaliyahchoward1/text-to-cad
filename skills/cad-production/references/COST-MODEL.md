# CAD-Production Cost Model Methodology

## Overview

The cost estimation model breaks per-unit manufacturing cost into five categories:

1. **Material Cost** — Raw resin, metal stock, or other material volume
2. **Tooling Amortization** — Mold/fixture cost spread across production volume
3. **Labor** — Machine operation, setup, assembly time
4. **Overhead** — Facility, utilities, management allocation
5. **Finishing** — Post-processing (anodizing, plating, inspection)

**Total Per-Unit Cost = (Material + Tooling Amortization + Labor + Overhead + Finishing)**

---

## 1. Material Cost

### Formula
```
Material Cost = (Material Volume in grams) × (Material $/gram) × (Waste/Scrap Factor)
```

### Parameters by Material

#### Polypropylene (Injection Molding — Luminescence Bottles)
- **Density:** 0.90 g/cm³
- **Base resin cost:** $0.012–$0.018 per gram
  - Standard natural: $0.012/gram
  - Colored or specialty: $0.015–$0.018/gram
- **Waste/scrap factor:** 1.05 (5% typical molding scrap, runner trim)
- **Volume per unit:** Extract from STEP geometry (cm³) × 0.90 g/cm³

**Example: 50ml Luminescence Bottle**
- Approximate volume: 40 cm³ (accounting for wall thickness, 2.0mm)
- Mass: 40 cm³ × 0.90 g/cm³ = 36 grams
- Resin cost: 36g × $0.015/g × 1.05 = **$0.57/unit**

#### Polystyrene (GlamGrab Compacts)
- **Density:** 1.05 g/cm³
- **Base resin cost:** $0.014–$0.020 per gram
- **Waste factor:** 1.08 (8% typical, more scrap due to complex geometry)

**Example: 45mm Compact Shell (Single Half)**
- Volume: 15 cm³
- Mass: 15 × 1.05 = 15.75 grams
- Cost (both halves): 31.5g × $0.016/g × 1.08 = **$0.55/unit**

#### Aluminum (CNC Machining — AstroPodra)
- **Stock material cost:** $0.08–$0.12 per gram
- **Typical stock size:** 50mm × 50mm × 25mm blank (~62g stock for small part)
- **Material utilization:** 30–50% (significant waste in CNC)
- **Waste factor:** 2.0–2.5 (account for scrap)

**Example: AstroPodra LED Enclosure**
- Final mass: 40 grams
- Material cost with waste: 40g × $0.10/g × 2.2 = **$8.80/unit** (material alone)

---

## 2. Tooling Amortization

### Formula
```
Tooling Amortization = Tooling Cost / Production Volume (units)
```

### Typical Tooling Costs

#### Injection Molding
- **Single-cavity mold (cosmetic bottles, caps):** $5,000–$10,000
  - Luminescence 50ml bottle: $7,500
  - M24 cap assembly: $6,000
  - GlamGrab clamshell (both halves + hinge pins): $12,000–$15,000

- **Multi-cavity mold (high-volume):** $15,000–$30,000
  - Typically 2–4 cavity molds for >50K unit runs

- **Insert mold (with metal/hardware inserts):** $10,000–$18,000
  - Hinge pin sockets, latch housings

#### CNC Setup
- **Fixture design & building:** $500–$2,000
- **Tool library (end mills, drills, taps):** $1,000–$3,000
- **Amortization per part:** Minimal if high-volume (typically ignored below 1K units)

### Amortization by Volume Tier

| Volume | 1K Units | 5K Units | 10K Units | 50K Units |
|--------|----------|----------|-----------|-----------|
| Tooling Cost ($7,500 example) | $7.50 | $1.50 | $0.75 | $0.15 |
| % of Total @ $2.00 wholesale | 375% (loss) | 75% (loss) | 37.5% | 7.5% |

**Insight:** Break-even typically occurs at 4K–5K units for a standard cosmetic container.

---

## 3. Labor Cost

### Injection Molding Labor
```
Labor Cost = (Cycle Time in seconds / 60) × (Hourly Rate / 60) + Handling/QA
```

**Parameters:**
- **Hourly rate:** $12–$20/hour (depends on region; $15/hour typical US average)
- **Cycle time:** 40–60 seconds (per design, material, mold efficiency)
- **Handling & setup:** $0.05–$0.10 per unit
- **QA/inspection:** $0.05–$0.10 per unit (variable with defect rate)

**Example: Luminescence 50ml Bottle**
- Cycle time: 50 seconds
- Operator time: (50/60) × ($15/3600) = $0.139/unit
- Handling: $0.08/unit
- QA: $0.05/unit
- **Total labor: ~$0.27/unit**

### CNC Machining Labor
```
Labor Cost = (Cycle Time in minutes) × (Hourly Rate / 60) + Setup Amortization
```

**Parameters:**
- **Hourly rate:** $25–$45/hour (skilled CNC operators; $35/hour typical)
- **Cycle time:** 8–20 minutes per unit (varies by complexity)
- **Setup time:** $1,000–$3,000 per job (amortized across batch)

**Example: AstroPodra LED Enclosure**
- Cycle time: 12 minutes
- Operator time: (12) × ($35/60) = $7.00/unit
- Setup amortization (500-unit batch): $3,000 / 500 = $6.00/unit
- **Total labor + setup: ~$13/unit** (scales down with larger batches)

### Hand Assembly Labor
```
Labor Cost = (Assembly Time in minutes) × (Hourly Rate / 60) + QA Time
```

**Parameters:**
- **Hourly rate:** $12–$18/hour (trained assembly workers; $15/hour typical)
- **Assembly time:** 2–5 minutes per unit (varies with complexity)
- **QA time:** $0.25–$0.50 per unit

**Example: GlamGrab Compact 45mm**
- Assembly time: 4 minutes
- Worker time: (4) × ($15/60) = $1.00/unit
- QA: $0.40/unit
- **Total: ~$1.40/unit**

---

## 4. Overhead & Indirect Costs

### Allocation Method
```
Overhead = Material Cost × Overhead Rate (%) + Labor Cost × Burden Rate (%)
```

**Typical allocations:**
- **Facility overhead:** 20–30% of material cost (rent, utilities, equipment maintenance)
- **Labor burden:** 25–40% of labor cost (payroll taxes, benefits, training)
- **Administrative:** 5–10% of total manufacturing cost

**OOB Standard (Phase 1):**
- Material overhead: **25%**
- Labor burden: **30%**
- Combined allocation: ~**15–20% of total cost**

**Example: Luminescence 50ml**
- Material: $0.57 → Overhead: $0.57 × 25% = $0.14
- Labor: $0.27 → Burden: $0.27 × 30% = $0.08
- **Total overhead: $0.22/unit**

---

## 5. Finishing & Post-Processing

### Injection Molding Products (Typically Minimal)
- Mold finish/cosmetic polish: Included in tooling
- Gate mark cleanup: $0.02–$0.05/unit (if cosmetic-critical)
- **Total finishing: $0–$0.05/unit**

### CNC Machined Parts
- **Anodizing (aluminum):** $0.50–$1.50/unit
  - Base cost: $50–$150 per plating batch
  - Per-unit at 500 units: $0.10–$0.30
  - Plus material surcharges: $0.40–$1.20
- **Electroplating (rose gold, chrome):** $1.00–$2.00/unit
- **Passivation (stainless):** $0.20–$0.50/unit

### Assembly Products (Fabric/Lining)
- **Velvet lining material:** $0.12–$0.20/unit
- **Adhesive & application:** $0.05–$0.10/unit
- **Total for lining: $0.17–$0.30/unit**

---

## Complete Cost Breakdown Example

### Luminescence 50ml Bottle @ 10K Units

| Category | Unit Cost | Calculation |
|----------|-----------|-------------|
| **Material** | $0.57 | 36g × $0.015/g × 1.05 waste |
| Tooling Amort. | $0.75 | $7,500 mold / 10,000 units |
| **Labor** | $0.27 | 50s cycle × $15/hr + handling/QA |
| **Overhead** | $0.22 | (Material + Labor) × allocation % |
| Finishing | $0.02 | Minor gate cleanup |
| **COGS Total** | **$1.83** | |
| — | — | |
| Cap (M24) | $0.35 | Separate item, purchased |
| Label | $0.12 | Circumference wrap, printed |
| Packaging | $0.15 | Box, tissue, bag |
| **Total Landed** | **$2.45** | All components + freight |
| — | — | |
| Wholesale Price | $2.00 | OOB target |
| **Margin** | **-$0.45 / -23%** | **LOSS AT THIS PRICE** |
| — | — | |
| Recommended Wholesale | $3.50 | 43% gross margin |
| **Retail @ 2.5× markup** | $8.75 | Standard beauty markup |

---

## Cost Sensitivity Analysis

### Impact of Volume Changes
- **1K → 5K units:** Tooling amort. drops 80% ($7.50 → $1.50)
- **5K → 10K units:** Tooling amort. drops 50% ($1.50 → $0.75)
- **10K → 50K units:** Tooling amort. drops 80% ($0.75 → $0.15)

**Insight:** Major cost breaks occur at 5K and 10K (mold amortization reaches acceptable levels).

### Impact of Design Changes
- **Wall thickness +0.5mm:** Cycle time +15%, material +5%, labor +$0.04
- **Complex geometry (undercuts):** Tooling +$2K–$3K, cycle +20 seconds
- **Tight tolerances:** Slower feed rates, potential scrap, labor +$0.10–$0.20

### Impact of Yield/Defects
- **Normal yield:** 98% (assume 2% scrap)
- **Low yield (95%):** Effective cost increase of 3.2% ($1.83 → $1.89)
- **High defect rate (>5%):** Risk of vendor rework charges (negotiate in contract)

---

## Model Validation & Refinement

### Phase 1 (Current)
- Fixed percentages for overhead/burden
- Simplified labor allocation
- Typical waste factors (will refine with actual vendor data)

### Phase 2 (Week 2)
- **Historical tracking:** Collect actual costs from first 3–5 vendor quotes
- **Variance analysis:** Identify which assumptions are closest vs. furthest from reality
- **Refine rates:** Update material costs, labor burn rates per vendor/process

### Phase 3 (Month 2)
- **Process-specific models:** Separate injection, CNC, assembly into detailed sub-models
- **Vendor benchmarking:** Build cost range by vendor and geography
- **Optimization suggestions:** "Reducing wall thickness by 0.3mm saves $0.08/unit"

---

## Next Update
- **Review frequency:** Quarterly (material costs, labor rates, vendor quotes)
- **Trigger:** Any quote >15% variance from estimate (investigate and adjust model)
- **Owner:** Ops-Agent + CAD-Production-Agent collaboration
