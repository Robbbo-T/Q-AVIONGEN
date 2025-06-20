# 00-10-10-02-01-DimensionsTop.png - Image Specification Document
## **UPDATED VERSION - 4 Fan Configuration per ECN-AMPEL-001**

## Document Information
- **ATA Chapter**: 00 - General
- **Section**: 00-10 - Aircraft General
- **Subsection**: 00-10-10 - General Description
- **Image ID**: 00-10-10-02-01
- **File Name**: 00-10-10-02-01-DimensionsTop.png
- **GQOIS ID**: GQOIS-Q-AIR-00-10-DIM-TOP-001
- **Revision**: 1.1 (**Updated per ECN-AMPEL-001**)
- **Effective Date**: 2025-06-16
- **Image Type**: Technical Dimensional Drawing - Top View
- **Distribution**: Engineering Use Only
- **Change Reference**: ECN-AMPEL-001 (Propulsion Optimization)

---

## 1. Image Purpose and Scope

This image provides the definitive top-view dimensional reference for the AMPEL360 BWB-Q100 aircraft, showing all critical measurements, structural boundaries, and system locations as viewed from directly above. This drawing serves as the master reference for manufacturing tolerances, structural analysis, and certification documentation.

**⚠️ CRITICAL UPDATE:** This specification reflects the **optimized 4-fan propulsion configuration** with larger diameter fans, as approved in ECN-AMPEL-001.

---

![image](https://github.com/user-attachments/assets/fb9e6985-45cc-4dd9-85c3-578f6bc1213b)


## 2. Image Specifications

### 2.1 Technical Requirements

| Parameter | Specification |
|-----------|--------------|
| **Resolution** | 4K (3840 × 2160 pixels) minimum |
| **DPI** | 300 DPI for print, 72 DPI for digital |
| **Color Mode** | RGB for digital, CMYK for print |
| **File Format** | PNG-24 with transparency |
| **File Size** | Maximum 15 MB |
| **Background** | White (#FFFFFF) |
| **Aspect Ratio** | 16:9 |
| **Line Weights** | ISO 128 compliant |

### 2.2 Drawing Standards

- **Primary Lines**: 0.7mm weight, black (#000000)
- **Dimension Lines**: 0.35mm weight, blue (#0000FF)
- **Center Lines**: 0.25mm weight, red dashed (#FF0000)
- **Hidden Lines**: 0.35mm weight, grey dashed (#808080)
- **Text Height**: 3.5mm minimum for dimensions
- **Arrow Style**: Closed arrowheads, 2.5mm length

---

## 3. View Configuration

### 3.1 Primary Orthographic Projection

**View Orientation:**
- **Projection Type**: True orthographic top view
- **Looking Direction**: From above (Z-axis positive)
- **Aircraft Position**: Horizontal, landing gear extended
- **Scale**: 1:200 for full aircraft, details at 1:50
- **Coordinate System**: Aircraft reference frame (nose forward)

### 3.2 Aircraft Centerline and Reference Points

```
[ASCII Representation of Top View Layout - UPDATED 4 FAN CONFIGURATION]

←—————————————— 88.4 m (290 ft) ——————————————→

         ╔══════════════════════════════════════╗
         ║                                      ║
    ┌────╫────┐                          ┌────╫────┐
    │ ○  ║ ○  │ ← Quantum Sensors        │ ○  ║ ○  │
    │    ║    │                          │    ║    │
    │    ║QNS │ ← Nose Array             │    ║    │
    └────╫────┘                          └────╫────┘
         ║                                      ║
    ●    ║    ● ← **Fan #4 & #1**         ●    ║    ●
         ║      (3.5m diameter)                ║      
         ║                                      ║
    ●    ║    ● ← **Fan #3 & #2**         ●    ║    ●
         ║      (3.5m diameter)                ║
         ║                                      ║
    ⊥ ⊥ ⊥║⊥ ⊥ ⊥ ⊥ ⊥ ← Elevon Segments      ⊥ ⊥ ⊥║⊥ ⊥ ⊥ ⊥ ⊥
         ║                                      ║
         ║  ▲ △ ▲  ← Landing Gear          ▲ △ ▲  ║
         ║                                      ║
         ╚══════════════════════════════════════╝
                           ║
                           ▼
                    Aircraft Centerline
```

---

## 4. **UPDATED** Critical Dimensions and Annotations

### 4.1 Overall Aircraft Dimensions

**Primary Measurements (mandatory callouts):**

| Dimension | Value | Tolerance | Annotation Position |
|-----------|-------|-----------|-------------------|
| **Maximum Wingspan** | 88.4 m (290.0 ft) | ±50 mm | Top, centered |
| **Maximum Length** | 64.2 m (210.6 ft) | ±30 mm | Right side, vertical |
| **Wing Root Chord** | 18.6 m (61.0 ft) | ±20 mm | Centerline |
| **Wing Tip Chord** | 2.1 m (6.9 ft) | ±10 mm | Wingtip |
| **Maximum Wing Width** | 20.0 m (65.6 ft) | ±25 mm | Widest point |

### 4.2 **UPDATED** Propulsion System Layout Dimensions

**Electric Fan Positioning (4-Fan Configuration):**

| Fan ID | Station (from nose) | Lateral Position | Diameter | Notes |
|--------|-------------------|------------------|----------|-------|
| **Fan #1** | 48.0 m | +18.0 m | **3.5 m** | Right outer |
| **Fan #2** | 46.5 m | +8.0 m | **3.5 m** | Right inner |
| **Fan #3** | 46.5 m | -8.0 m | **3.5 m** | Left inner |
| **Fan #4** | 48.0 m | -18.0 m | **3.5 m** | Left outer |

**Critical Spacing Dimensions:**
- **Fan #1 to #2 spacing**: 10.0 m center-to-center
- **Fan #2 to #3 spacing**: 16.0 m center-to-center  
- **Fan #3 to #4 spacing**: 10.0 m center-to-center
- **Fan #1 to #4 total span**: 36.0 m center-to-center

**Annotation Requirements:**
- Each fan numbered clearly (1-4) ⚠️ **UPDATED FROM 1-8**
- Fan center-to-center spacing dimensions
- **Diameter callouts: 3.5 m (11.5 ft)** on Fans #1 and #4 ⚠️ **UPDATED**
- Thrust line indications

### 4.3 Quantum System Locations

**Quantum Navigation System (QNS):**
- **Primary Array**: Nose section, 2.0 m diameter
- **Position**: Aircraft centerline, 1.5 m from nose
- **Aperture Count**: 4 sensors in square pattern
- **Separation**: 0.8 m center-to-center

**Wingtip Quantum Sensors:**
- **Location**: Wingtip leading edge
- **Distance from tip**: 0.5 m inboard
- **Sensor diameter**: 0.3 m each
- **Count per wing**: 3 sensors

**QPU Bay:**
- **Location**: Fuselage centerline
- **Longitudinal**: Station 25.0 m from nose
- **Dimensions**: 4.0 m × 2.5 m rectangular
- **Access**: Upper deck level

### 4.4 Control Surface Dimensions

**Elevon Segments (per side):**

| Segment | Chord Length | Span | Hinge Line Position |
|---------|-------------|------|-------------------|
| **Inboard** | 3.2 m | 8.5 m | 75% wing chord |
| **Middle** | 2.8 m | 9.2 m | 78% wing chord |
| **Outboard** | 2.1 m | 7.8 m | 82% wing chord |

**Leading Edge Devices:**
- **Span**: Continuous from root to 90% semi-span
- **Chord**: 12% of local wing chord
- **Deployment angle**: 25° maximum

### 4.5 Landing Gear Layout

**Main Landing Gear (3-post configuration):**
- **Nose Gear**: Centerline, 8.5 m from nose
- **Main Gear Post #1**: ±5.2 m lateral, 28.0 m from nose
- **Main Gear Post #2**: ±8.8 m lateral, 32.5 m from nose
- **Main Gear Post #3**: ±12.1 m lateral, 37.0 m from nose

**Gear Door Outlines:**
- **Nose Gear Bay**: 2.5 m × 3.0 m
- **Main Gear Bays**: 3.2 m × 4.5 m each

---

## 5. **UPDATED** Propulsion System Detailed Layout

### 5.1 Fan Installation Zones

**Zone Definition for Each Fan:**

| Zone | Fan ID | Center Coordinates | Installation Envelope |
|------|--------|--------------------|----------------------|
| **Zone 1** | Fan #1 | (48.0m, +18.0m) | 4.0m × 4.0m × 1.5m deep |
| **Zone 2** | Fan #2 | (46.5m, +8.0m) | 4.0m × 4.0m × 1.5m deep |
| **Zone 3** | Fan #3 | (46.5m, -8.0m) | 4.0m × 4.0m × 1.5m deep |
| **Zone 4** | Fan #4 | (48.0m, -18.0m) | 4.0m × 4.0m × 1.5m deep |

### 5.2 **NEW** Fan Interference Analysis

**Minimum Clearances:**
- **Fan-to-fan**: 4.5 m minimum (exceeds 3.5m diameter requirement)
- **Fan-to-wing tip**: 8.2 m (Fan #1/#4 to wingtip)
- **Fan-to-centerline**: 8.0 m minimum (Fan #2/#3)
- **Fan-to-landing gear**: 6.0 m minimum clearance verified

### 5.3 Turbogenerator Locations

**Internal Turbogenerator Positioning:**
- **Turbogenerator #1**: Station 35.0m, +6.0m lateral
- **Turbogenerator #2**: Station 35.0m, -6.0m lateral
- **Power Distribution**: Electrical bus to all 4 fans
- **H2 Fuel Lines**: From wing tanks to turbogenerators

---

## 6. Structural Reference Lines and Zones

### 6.1 Wing Stations and Waterlines

**Wing Stations (WS):**
- **WS 0**: Aircraft centerline
- **WS 8**: Fan #2/#3 lateral position
- **WS 18**: Fan #1/#4 lateral position
- **WS 30**: Outer wing structure
- **WS 44.2**: Wing tip station

**Fuselage Stations (FS):**
- **FS 0**: Aircraft nose reference
- **FS 46.5**: Fan #2/#3 longitudinal position
- **FS 48.0**: Fan #1/#4 longitudinal position
- **FS 64.2**: Aft extremity

### 6.2 **UPDATED** Structural Zones

**Propulsion Integration Zones:**
- **Zone A**: Fan #2/#3 structural reinforcement (FS 45-48, WS 6-10)
- **Zone B**: Fan #1/#4 structural reinforcement (FS 46.5-49.5, WS 16-20)
- **Zone C**: Inter-fan structural continuity (FS 45-50, WS 8-18)

**Wing Box Boundaries:**
- **Forward Spar**: 15% wing chord
- **Rear Spar**: 70% wing chord (aft of all fans)
- **Root Rib**: WS 0 (centerline)
- **Tip Rib**: WS 44.2

### 6.3 System Installation Zones

**Electrical Systems Zone:**
- **Primary Power**: FS 15-25, WS 0-5
- **Fan Power Distribution**: Along wing leading edge to each fan
- **Secondary Power**: FS 30-40, WS 0-5

**Fuel System Zones:**
- **Wing Tanks**: Between spars, WS 8-40
- **H2 Storage**: Specialized tanks in wing root areas
- **Center Tank**: FS 20-35, WS 0-8

---

## 7. **UPDATED** Annotation Standards and Callouts

### 7.1 Fan-Specific Annotations

**Required Fan Callouts:**
- **Fan ID Numbers**: 1, 2, 3, 4 (clearly labeled)
- **Fan Diameter**: 3.5m (11.5 ft) on representative fans
- **Fan Center Coordinates**: Station and lateral positions
- **Rotation Direction**: Indicated with arrow symbols
- **Power Rating**: Per fan electrical power (to be determined)

### 7.2 Dimension Line Specifications

**Linear Dimensions:**
- **Extension Lines**: Extend 2mm beyond dimension lines
- **Dimension Text**: Center-aligned above dimension line
- **Units**: Metric primary, Imperial secondary in parentheses
- **Precision**: Fan positions ±10mm, diameters ±5mm

**Fan Spacing Dimensions:**
```
Critical Fan Dimensions to Show:
├── 10.0m (Fan #1 to #2 spacing)
├── 16.0m (Fan #2 to #3 spacing)  
├── 10.0m (Fan #3 to #4 spacing)
└── 36.0m (Fan #1 to #4 total span)
```

### 7.3 **UPDATED** Reference Symbol Standards

**Fan Identification:**
```
● Fan Location (3.5mm diameter circle) ⚠️ UPDATED SIZE
1 Fan Number (3mm height, bold)
→ Rotation Direction (2mm arrow)
```

**System Color Coding:**
- **Electric Fans**: Electric Green (#00FF80) circles
- **Turbogenerators**: Orange (#FF8000) rectangles
- **Quantum Sensors**: Quantum Blue (#0080FF) diamonds
- **Landing Gear**: Purple (#8000FF) triangles

---

## 8. **UPDATED** Technical Accuracy Requirements

### 8.1 **NEW** Fan Configuration Verification

**Critical Checkpoints:**
1. **Fan Count**: Exactly 4 fans (not 8)
2. **Fan Diameter**: Exactly 3.5m each (not 2.5m)
3. **Fan Positions**: Match ECN-AMPEL-001 coordinates
4. **Fan Spacing**: Adequate clearance verified
5. **Structural Integration**: Wing loading analysis updated

### 8.2 Geometric Precision Standards

**Dimensional Tolerance Classes:**
- **Class A (Critical)**: Fan positions ±10mm
- **Class A (Critical)**: Fan diameters ±5mm
- **Class B (Important)**: System locations ±20mm
- **Class C (General)**: Reference dimensions ±50mm

### 8.3 **NEW** Propulsion System Verification

**Fan System Validation:**
- **Power Requirements**: Total 40,000 lbf thrust from 4 fans
- **Individual Fan Thrust**: 10,000 lbf per fan
- **Fan Efficiency**: Optimized for 3.5m diameter
- **BLI Integration**: Inlet design validated for larger fans

---

## 9. **UPDATED** Manufacturing Applications

### 9.1 **NEW** Fan Installation References

**Tooling Requirements:**
- **Fan #1 Jig**: Position 48.0m, +18.0m, 3.5m diameter
- **Fan #2 Jig**: Position 46.5m, +8.0m, 3.5m diameter
- **Fan #3 Jig**: Position 46.5m, -8.0m, 3.5m diameter
- **Fan #4 Jig**: Position 48.0m, -18.0m, 3.5m diameter

**Quality Control Points:**
- **Fan Center Verification**: ±5mm positional tolerance
- **Fan Diameter Check**: 3.5m ±2mm
- **Fan Alignment**: Thrust vector parallel to centerline
- **Fan Clearance**: Minimum 0.5m to adjacent structures

### 9.2 **UPDATED** Wing Manufacturing

**Critical Interfaces:**
- **Fan Mounting Rings**: 4 units required (not 8)
- **Electrical Conduits**: Routing to 4 fan positions
- **Cooling Systems**: Thermal management for 4 high-power units
- **Structural Reinforcement**: Zones A, B, C as defined

---

## 10. Companion Drawings Cross-Reference

### 10.1 **UPDATED** Related Technical Drawings

| Drawing ID | Title | Scale | Status |
|------------|-------|-------|--------|
| 00-10-10-01-01 | Aircraft Overview (Isometric) | Variable | **Updated to Rev 2.1** |
| 00-10-10-02-01 | **Dimensions Top View (This Drawing)** | 1:200 | **Updated to Rev 1.1** |
| 00-10-10-02-02 | Dimensions Front View | 1:200 | **Requires Update** |
| 00-10-10-02-03 | Dimensions Side View | 1:200 | **Requires Update** |
| 76-XX-XX | Fan Installation Details (4-fan) | 1:20 | **New Drawing Required** |

### 10.2 **NEW** Detail Drawing Requirements

**4-Fan System Details:**
- **Drawing 76-10-01**: Fan #1/#4 installation (outer positions)
- **Drawing 76-10-02**: Fan #2/#3 installation (inner positions)
- **Drawing 76-10-03**: Fan mounting and structural interface
- **Scale**: 1:20 for detailed views

---

## 11. Quality Control and Verification

### 11.1 **UPDATED** Drawing Review Checklist

**Propulsion System Accuracy:**
- [ ] Fan count: Exactly 4 fans (not 8)
- [ ] Fan diameter: 3.5m each (not 2.5m)
- [ ] Fan positions match ECN-AMPEL-001 coordinates
- [ ] Fan spacing provides adequate clearance
- [ ] Fan numbering: 1-4 (not 1-8)
- [ ] Power distribution routing feasible

**Dimensional Accuracy:**
- [ ] All primary dimensions verified against updated CAD model
- [ ] Fan positions match propulsion system requirements v2.0
- [ ] Landing gear positions unaffected by fan changes
- [ ] Control surface dimensions unchanged
- [ ] Quantum system locations unchanged

### 11.2 **UPDATED** Approval Requirements

**Technical Review:**
- **Chief Engineer**: Overall configuration approval (4-fan)
- **Propulsion Lead**: Fan placement and sizing approval
- **Structures Lead**: Wing loading with larger fans
- **Manufacturing Lead**: Producibility of 4-fan system
- **Configuration Control**: ECN-AMPEL-001 compliance

---

## 12. **UPDATED** Revision Control

### 12.1 **NEW** Change Documentation

**ECN Implementation:**
- **Source**: ECN-AMPEL-001 (Propulsion Optimization)
- **Change**: 8 fans (2.5m) → 4 fans (3.5m)
- **Approval**: [Pending signatures]
- **Implementation**: Effective immediately for new work

### 12.2 **UPDATED** Version History

| Rev | Date | Description | ECN | Approved |
|-----|------|-------------|-----|----------|
| 1.0 | 2025-06-15 | Initial release (8-fan) | - | [Signature] |
| **1.1** | **2025-06-16** | **4-fan configuration** | **ECN-AMPEL-001** | **[Pending]** |

---

## 13. **NEW** Implementation Notes

### 13.1 Drawing Update Impact

**Immediate Changes Required:**
- Fan count and positioning annotations
- Fan diameter callouts
- Fan numbering system
- Spacing dimensions
- Installation zone boundaries

**Unchanged Elements:**
- Overall aircraft dimensions
- BWB configuration
- Quantum system locations
- Landing gear layout
- Control surface configuration

### 13.2 Usage During Transition

**Current Status:**
- **This drawing (Rev 1.1)**: 4-fan configuration per ECN-AMPEL-001
- **Manufacturing**: Use 4-fan configuration for all new tooling
- **Analysis**: Update models to reflect 4-fan system
- **Documentation**: Reference this revision for current design

---

## Summary

This **UPDATED** top-view dimensional drawing reflects the **optimized 4-fan propulsion configuration** approved in ECN-AMPEL-001. The drawing maintains all critical aircraft dimensions while showing the new fan positions, sizes, and spacing that reduce system complexity and cost while maintaining performance.

**Key Changes from Rev 1.0:**
- **4 fans instead of 8** (3.5m diameter vs 2.5m)
- **New fan positions** at ±8m and ±18m from centerline
- **Updated annotations** and dimensional callouts
- **Revised installation zones** and structural references
- **ECN-AMPEL-001 compliance**

---

**END OF UPDATED SPECIFICATION**

*For technical support contact:*  
*Engineering Drawing Office*  
*Email: drawings@gaia-qao.aero*  
*Change Control: ECN-AMPEL-001*
