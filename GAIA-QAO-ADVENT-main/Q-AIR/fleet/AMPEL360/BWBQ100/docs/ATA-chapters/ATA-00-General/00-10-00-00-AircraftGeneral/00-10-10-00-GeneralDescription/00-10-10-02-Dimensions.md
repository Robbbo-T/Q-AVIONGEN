# 00-10-10-02 Dimensions

## Document Information
- **ATA Chapter**: 00 - General
- **Section**: 00-10 - Aircraft General
- **Subsection**: 00-10-10 - General Description
- **Document ID**: 00-10-10-02
- **GQOIS ID**: GQOIS-Q-AIR-00-10-DIMS-001
- **Revision**: 2.0
- **Effective Date**: 2025-06-15
- **Review Cycle**: Annual
- **Distribution**: Unrestricted

---

## 1. Reference Datum System

### 1.1 Aircraft Datum Points

```
[Figure 00-10-10-02-01: Datum Reference System]

                    VL 0
                     │
    WL 0 ────────────┼────────────── WL 0
                     │
         FS 0        │
          ●──────────┼──────────────→ X-axis (aft)
          │          │
          │      ╱───┴───╲
          │     ╱         ╲
    Y-axis│    ╱           ╲
    (right)   │             │
          ↓   │             │
              ╲             ╱
               ╲___________╱

Datum Definitions:
- FS 0: 5.00 m forward of nose tip
- WL 0: Ground line, aircraft level
- VL 0: Aircraft centerline
```

### 1.2 Station Reference System

**Fuselage Stations (FS)** - Measured aft from FS 0
- FS 0: Datum point (5.00 m forward of nose)
- FS 500: Nose tip
- FS 3000: Cockpit center
- FS 6920: Forward pressure bulkhead
- FS 35000: Aircraft center of gravity (nominal)
- FS 58000: Aft pressure bulkhead
- FS 69200: Tail cone end

**Water Line (WL)** - Measured up from WL 0
- WL 0: Ground line (static position)
- WL 210: Cabin floor (main deck)
- WL 530: Upper deck floor
- WL 850: Crown of fuselage

**Vertical Line (VL)** - Measured right from centerline
- VL 0: Aircraft centerline
- VL ±4420: Maximum half-span

---

## 2. Overall Aircraft Dimensions

### 2.1 Primary Dimensions

| Parameter | Metric | Imperial | Station Reference |
|-----------|--------|----------|-------------------|
| **Overall Length** | 64.20 m | 210.63 ft | FS 500 to FS 69200 |
| **Wingspan** | 88.40 m | 290.03 ft | VL -44200 to VL +44200 |
| **Height (overall)** | 12.80 m | 42.00 ft | WL 0 to WL 1280 |
| **Wing Area** | 820.0 m² | 8,826 ft² | Reference planform |
| **Mean Aerodynamic Chord** | 9.80 m | 32.15 ft | At VL 0 |
| **Aspect Ratio** | 9.53 | 9.53 | - |
| **Sweep Angle (LE)** | 35.0° | 35.0° | At 25% chord |
| **Dihedral Angle** | 5.0° | 5.0° | Inner wing |

### 2.2 Ground Attitude Dimensions

```
[Figure 00-10-10-02-02: Ground Attitude Profile]

Static Ground Position (Level):
         ┌──────────────────────┐
        ╱  2.35 m               ╲    12.80 m
       ╱   ↑                     ╲     ↑
      ╱    │    9.85 m           ╲    │
─────┴─────┴──────┴───────────────┴───┴─────
  2.10 m      3.45 m         4.20 m
   (NG)      (MLG-Fwd)      (MLG-Aft)
```

---

## 3. Fuselage Dimensions

### 3.1 Cross-Section Dimensions by Station

| Station | Width (m) | Height (m) | Floor Height (m) | Cabin Height (m) |
|---------|-----------|------------|------------------|------------------|
| FS 1000 | 3.20 | 2.80 | N/A | N/A |
| FS 3000 | 5.40 | 3.60 | 2.10 | 2.20 |
| FS 10000 | 12.50 | 6.80 | 2.10 | 3.20 |
| FS 20000 | 18.60 | 7.20 | 2.10 | 3.20 |
| FS 35000 | 20.00 | 7.40 | 2.10 | 3.20 |
| FS 50000 | 15.80 | 6.50 | 2.10 | 3.00 |
| FS 60000 | 8.40 | 4.20 | 2.10 | 2.40 |

### 3.2 Cabin Dimensions

```
[Figure 00-10-10-02-03: Cabin Cross-Section at FS 35000]

                WL 850 (Crown)
                    │
    VL-1000    VL 0 │ VL+1000
        │        │  │  │
        ▼        ▼  ▼  ▼
       ┌─────────────────┐ ← WL 730 (Ceiling)
      ╱                   ╲
     │  ┌─┐ ┌─┐ ┌─┐ ┌─┐  │
     │  └─┘ └─┘ └─┘ └─┘  │ ← WL 530 (Upper Deck)
     │ ═══════════════════ │
     │  ┌─┐ ┌─┐ ┌─┐ ┌─┐  │
     │  └─┘ └─┘ └─┘ └─┘  │ ← WL 210 (Main Deck)
     ╲___________________╱
      └─────┬─────┬─────┘
            │     │
         10.0 m  20.0 m
        (usable) (max)
```

**Cabin Dimensions Summary:**
- Maximum cabin width: 20.00 m at FS 35000
- Usable cabin width: 18.50 m (excluding sidewalls)
- Main deck headroom: 2.15 m (minimum)
- Upper deck headroom: 2.05 m (minimum)
- Central atrium height: 6.40 m (WL 210 to WL 850)

---

## 4. Wing Dimensions

### 4.1 Wing Geometry

| Parameter | Root (VL 0) | Mid-Span (VL 22100) | Tip (VL 44200) |
|-----------|-------------|---------------------|----------------|
| **Chord** | 28.50 m | 9.80 m | 2.85 m |
| **Thickness** | 5.70 m (20%) | 1.47 m (15%) | 0.34 m (12%) |
| **LE Position** | FS 15000 | FS 28500 | FS 42000 |
| **TE Position** | FS 43500 | FS 38300 | FS 44850 |
| **Incidence** | 3.0° | 1.5° | -1.0° |
| **Twist** | 0° | -2.0° | -4.0° |

### 4.2 Control Surface Dimensions

```
[Figure 00-10-10-02-04: Wing Control Surfaces]

Wing Station Reference:
VL 0                VL 22100            VL 44200
 │                     │                   │
 │← Inner Elevon →│← Mid Elevon →│← Outer →│
 │   Segment 1    │  Segment 2  │ Seg 3   │
 ├────────────────┼─────────────┼─────────┤
 │   12.5 m       │   15.8 m    │  8.2 m  │
 │                │             │         │
 │ Chord: 3.8 m   │ Chord: 2.9m │ C: 2.1m │
```

**Elevon Specifications:**
- Total elevon span: 36.5 m per side
- Elevon chord (average): 2.93 m (30% local chord)
- Maximum deflection: +25° / -30°
- Segmentation: 3 independent sections per side

---

## 5. Landing Gear Dimensions

### 5.1 Gear Positions and Dimensions

```
[Figure 00-10-10-02-05: Landing Gear Layout]

TOP VIEW:
         FS 3850 (NG)
              │
    ╱─────────┼─────────╲
   ╱          │          ╲
  │     FS 32000 (MLG-F) │
  │      ↓         ↓     │
  │    ●───────────●     │
  │      11.20 m         │
  │                      │
  │    ●───────────●     │
  │      ↑         ↑     │
  ╲     FS 38500 (MLG-A) ╱
   ╲                    ╱
    ╲──────────────────╱

MLG Track: 11.20 m
MLG Base: 6.50 m
```

### 5.2 Gear Component Dimensions

| Component | Dimension | Value |
|-----------|-----------|-------|
| **Nose Gear** | | |
| Tire size | Diameter × Width | 1.27 × 0.51 m |
| Strut length | Extended | 3.85 m |
| | Compressed | 3.20 m |
| Turn angle | Maximum | ±75° |
| **Main Gear** | | |
| Tire size | Diameter × Width | 1.42 × 0.58 m |
| Trucks | Configuration | 3-wheel bogie |
| Strut length | Extended | 4.20 m |
| | Compressed | 3.45 m |
| Track width | Center-to-center | 11.20 m |

---

## 6. Door and Access Panel Dimensions

### 6.1 Passenger Doors

| Door | Location (FS) | Size (m) | Sill Height (m) | Type |
|------|---------------|----------|-----------------|------|
| **1L/R** | 11500 | 1.85 × 0.95 | 2.85 | Type A |
| **2L/R** | 22000 | 1.85 × 0.95 | 2.85 | Type A |
| **3L/R** | 35000 | 1.85 × 0.95 | 2.85 | Type A |
| **4L/R** | 48000 | 1.85 × 0.95 | 2.85 | Type A |
| **Upper L/R** | 28500 | 1.65 × 0.86 | 5.65 | Type III |

### 6.2 Cargo Doors

```
[Figure 00-10-10-02-06: Cargo Door Locations]

SIDE VIEW:
         FWD Cargo        AFT Cargo
         ┌─────┐         ┌───────┐
        ╱│     │         │       │╲
       ╱ │ 3.5m│         │ 4.2m  │ ╲
      ╱  │  ×  │         │   ×   │  ╲
─────┴───┤ 2.5m│─────────┤ 2.5m  ├───┴─
         └─────┘         └───────┘
       FS 16000         FS 42000
```

| Door | Location | Size (m) | Sill Height (m) | Type |
|------|----------|----------|-----------------|------|
| **Forward Cargo** | FS 16000 | 3.50 × 2.50 | 2.80 | Outward |
| **Aft Cargo** | FS 42000 | 4.20 × 2.50 | 2.80 | Outward |
| **Bulk Cargo** | FS 55000 | 1.80 × 1.35 | 2.80 | Outward |

### 6.3 Service Panels

| Panel | Purpose | Location | Size (m) |
|-------|---------|----------|----------|
| **Quantum Access** | QPU maintenance | FS 25000, VL 0 | 2.0 × 1.5 |
| **Electrical Bay** | Power distribution | FS 20000, VL -400 | 1.2 × 0.9 |
| **Hydraulic Service** | System access | FS 35000, VL +350 | 0.8 × 0.6 |
| **ECS Access** | Pack maintenance | FS 30000, VL 0 | 1.5 × 1.2 |
| **Fuel Panel** | Refueling control | FS 38000, VL -850 | 0.6 × 0.4 |

---

## 7. Ground Clearances

### 7.1 Static Ground Clearances

```
[Figure 00-10-10-02-07: Ground Clearance Profile]

                          12.80 m (tail)
                             ↑
        4.20 m              │
         ↑    ┌─────────────┴───┐
         │   ╱                   ╲
    2.10 │  ╱   1.85 m (fans)    ╲
     (NG)│ ╱      ↑               ╲
─────────┴┴───────┴─────────────────┴─────
         0.45 m (min belly clearance)
```

| Location | Clearance (m) | Condition |
|----------|---------------|-----------|
| **Nose gear** | 2.10 | Static |
| **Forward belly** | 1.85 | Static |
| **Center belly** | 0.85 | Static |
| **Aft belly** | 1.20 | Static |
| **Engine fans** | 1.85 | Minimum |
| **Wing tips** | 4.20 | Level |
| **Tail** | 12.80 | Maximum |
| **Antenna (lowest)** | 0.45 | Quantum array |

### 7.2 Operational Clearances

| Operation | Required Clearance | Location |
|-----------|-------------------|----------|
| **Rotation** | 0.35 m | Aft fuselage |
| **Landing** | 0.40 m | All points |
| **Max bank (ground)** | 0.30 m | Wing tip |
| **Cargo loading** | 3.50 m | Door height |
| **Quantum service** | 5.00 m | QPU bay |

---

## 8. Turning and Maneuvering Dimensions

### 8.1 Ground Turning Data

```
[Figure 00-10-10-02-08: Minimum Turning Radius]

     Pivot Point
         ●
        ╱│╲
       ╱ │ ╲ R = 45.2 m
      ╱  │  ╲ (148.3 ft)
     ╱   │   ╲
    ○────┴────○
    11.2 m track

Wingtip Path Radius: 65.8 m (215.9 ft)
```

**Turning Specifications:**
- Minimum turning radius (pivot): 45.2 m
- Wingtip clearance radius: 65.8 m
- Maximum steering angle: ±75°
- Effective wheelbase: 34.65 m
- Minimum pavement width: 45.0 m

### 8.2 Parking Requirements

| Configuration | Length | Width | Area |
|---------------|--------|-------|------|
| **Standard parking** | 70.0 m | 90.0 m | 6,300 m² |
| **With GSE** | 85.0 m | 95.0 m | 8,075 m² |
| **Hangar (minimum)** | 72.0 m | 92.0 m | 6,624 m² |
| **Pushback area** | 100.0 m | 100.0 m | 10,000 m² |

---

## 9. Interior Compartment Dimensions

### 9.1 Passenger Cabin Zones

| Zone | Location (FS) | Length (m) | Width (m) | Height (m) | Volume (m³) |
|------|---------------|-----------|-----------|------------|-------------|
| **First Class** | 12000-18000 | 6.0 | 15.0 | 2.15 | 193.5 |
| **Business** | 18000-28000 | 10.0 | 18.0 | 2.15 | 387.0 |
| **Premium Eco** | 28000-38000 | 10.0 | 19.0 | 2.15 | 408.5 |
| **Economy** | 38000-53000 | 15.0 | 18.0 | 2.15 | 580.5 |
| **Central Atrium** | 30000-36000 | 6.0 | 8.0 | 6.40 | 307.2 |

### 9.2 Cargo Compartment Dimensions

```
[Figure 00-10-10-02-09: Cargo Compartment Cross-Section]

        Main Deck Cargo
    ┌─────────────────────┐
    │  Clearance: 2.44 m  │
    │  Width: 4.20 m      │
    └──────┬──────────────┘
           │
    ┌──────┴──────┬───────┐
    │   FWD       │  AFT  │
    │  105 m³     │ 125 m³│
    └─────────────┴───────┘
     Lower Deck Compartments
```

| Compartment | Volume (m³) | Max Load (kg) | Door Size (m) |
|-------------|-------------|---------------|---------------|
| **Forward Hold** | 105 | 18,000 | 3.5 × 2.5 |
| **Aft Hold** | 125 | 22,000 | 4.2 × 2.5 |
| **Bulk** | 45 | 6,000 | 1.8 × 1.35 |
| **Total Lower** | 275 | 46,000 | - |
| **Main Deck (F)** | 580 | 65,000 | 3.5 × 2.7 |

---

## 10. Service and Maintenance Access Dimensions

### 10.1 Quantum System Access

**QPU Bay Dimensions:**
- Location: FS 24000-26000, WL 100-300
- Internal dimensions: 2.0 × 2.0 × 2.0 m
- Access hatch: 1.5 × 1.0 m
- Service clearance required: 3.0 m radius
- Temperature when open: Allow 30 min warmup

### 10.2 Engine Fan Access

| Fan Position | Station (FS) | Access Platform Height (m) | Service Radius (m) |
|--------------|--------------|---------------------------|-------------------|
| **Fan 1 & 8** | 18000 | 3.2 | 2.5 |
| **Fan 2 & 7** | 25000 | 3.5 | 2.5 |
| **Fan 3 & 6** | 35000 | 3.5 | 2.5 |
| **Fan 4 & 5** | 45000 | 3.2 | 2.5 |

### 10.3 Maintenance Platform Requirements

```
[Figure 00-10-10-02-10: Maintenance Access Zones]

TOP VIEW - Platform Positions:
    ╱─────────────────────────╲
   ╱  A    B    C    D    E   ╲
  │   □    □    □    □    □    │
  │                            │
  │   F    G    H    J    K    │
  │   □    □    □    □    □    │
  ╲                           ╱
   ╲─────────────────────────╱

Platform Heights:
A,E,F,K: 2.5 m (Wing access)
B,D,G,J: 3.5 m (Engine access)
C,H: 4.0 m (Crown access)
```

---

## 11. Special Dimensions

### 11.1 Quantum Component Locations

| Component | Center Location | Envelope (m) | Access |
|-----------|----------------|--------------|---------|
| **QPU Core** | FS 25000, VL 0, WL 200 | 2.0 × 2.0 × 2.0 | Bottom |
| **QNS Primary** | FS 800, VL 0, WL 350 | 0.8 × 0.8 × 1.2 | External |
| **QNS Secondary** | FS 68000, VL 0, WL 650 | 0.6 × 0.6 × 0.8 | Internal |
| **QKD Transmitter** | FS 2000, VL 0, WL 1200 | 0.4 × 0.4 × 0.6 | External |

### 11.2 Unique BWB Dimensions

**Pressure Vessel Geometry:**
- Maximum diameter: 7.40 m at FS 35000
- Minimum radius: 1.20 m at crown/floor junction
- Non-circular sections: 85% of pressure hull
- Multi-bubble intersections: 12 major joints

**Aerodynamic References:**
- Aerodynamic center: FS 32500 (25% MAC)
- Neutral point: FS 35750 (36.5% MAC)
- CG limits: FS 29400-34300 (15-35% MAC)

---

## 12. Dimension Accuracy and Tolerances

### 12.1 Manufacturing Tolerances

| Dimension Type | Tolerance | Notes |
|----------------|-----------|-------|
| **Overall length** | ±50 mm | As built |
| **Wingspan** | ±100 mm | Tip to tip |
| **Fuselage stations** | ±10 mm | Reference |
| **Door openings** | ±5 mm | Functional |
| **Quantum mounts** | ±0.5 mm | Precision |

### 12.2 Operational Variations

**Temperature Effects:**
- Length variation: ±150 mm (-40°C to +50°C)
- Wingspan variation: ±200 mm
- Height variation: ±50 mm

**Load Effects:**
- Wing deflection (MTOW): +2.8 m at tips
- Fuselage compression: -30 mm at MTOW
- Gear compression: -750 mm at MTOW

---

## Summary

This dimensional data represents the baseline configuration of the AMPEL360 BWB-Q100. All dimensions are subject to manufacturing tolerances and operational variations. For specific maintenance operations, always refer to the latest revision of this document and verify actual dimensions when critical clearances are involved.

**Critical Dimensions for Daily Operations:**
- Overall span: 88.4 m (290 ft) - gate planning
- Overall length: 64.2 m (211 ft) - parking
- Minimum ground clearance: 0.45 m - FOD risk
- Turn radius: 65.8 m - taxiway navigation
- Service height: 12.8 m - hangar clearance

For weight and balance calculations using these dimensions, refer to document 00-20-00-00-WeightBalance.

---

**END OF DIMENSIONS DOCUMENT**

*Next Document: 00-10-10-03-Capacities.md*
