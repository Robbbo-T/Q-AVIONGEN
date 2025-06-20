# 00-10-10-02-03-DimensionsFront.png - Image Specification Document
## **UPDATED VERSION - 4 Fan Configuration per ECN-AMPEL-001**

## Document Information
- **ATA Chapter**: 00 - General
- **Section**: 00-10 - Aircraft General
- **Subsection**: 00-10-10 - General Description
- **Image ID**: 00-10-10-02-03
- **File Name**: 00-10-10-02-03-DimensionsFront.png
- **GQOIS ID**: GQOIS-Q-AIR-00-10-DIM-FRONT-001
- **Revision**: 1.0 (**Initial Release with 4-Fan Configuration**)
- **Effective Date**: 2025-06-16
- **Image Type**: Technical Dimensional Drawing - Front View
- **Distribution**: Engineering Use Only
- **Change Reference**: ECN-AMPEL-001 (Propulsion Optimization)

---

![image](https://github.com/user-attachments/assets/b151be66-7669-46f3-b10c-f190e91c61cd)


## 1. Image Purpose and Scope

This image provides the definitive front-view dimensional reference for the AMPEL360 BWB-Q100 aircraft, showing all critical span measurements, height dimensions, and cross-sectional geometry as viewed from directly ahead. This drawing serves as the master reference for wingspan verification, ground clearance validation, hangar compatibility, and BWB cross-sectional analysis.

**⚠️ DESIGN NOTE:** This specification incorporates the **optimized 4-fan propulsion configuration** from initial design, as defined in ECN-AMPEL-001, showing all 4 fans clearly visible from the front perspective.

---

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

### 2.2 Professional Drawing Standards

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
- **Projection Type**: True orthographic front view
- **Looking Direction**: From aircraft nose (X-axis negative)
- **Aircraft Position**: Horizontal, landing gear extended
- **Scale**: 1:200 for full aircraft, details at 1:50
- **Coordinate System**: Aircraft reference frame (wings horizontal)

### 3.2 BWB Cross-Sectional Profile and Reference Points

```
[ASCII Representation of Front View Layout - 4 FAN CONFIGURATION]

←————————————— 88.4 m (290 ft) —————————————→

      ╭─────────────────────────────────────╮  ← 12.8m
     ╱                                       ╲    (42 ft)
    ╱    ●                           ●        ╲ ← **Fan #1 & #4**
   ╱      3.5m                     3.5m       ╲   (Outer positions)
  ╱                                           ╲
 ╱        ●                       ●            ╲ ← **Fan #2 & #3**  
╱          3.5m                 3.5m           ╲   (Inner positions)
│                                               │
│           ○○○○○○○○○○○○○○○○○○○○○○○○○            │ ← Passenger windows
│                                               │
│                      △                       │ ← Nose gear
╰───────▲───────────────────────────▲─────────╯
        │                           │
    Main Gear                   Main Gear
    Posts #1,2                  Posts #1,2 
    (+5.2m, +8.8m)             (-5.2m, -8.8m)
        │                           │
        ▼                           ▼
═══════════════════════════════════════════════ ← Ground Line
```

---

## 4. Critical Dimensions and Annotations

### 4.1 Overall Aircraft Envelope

**Primary Measurements (mandatory callouts):**

| Dimension | Value | Tolerance | Annotation Position |
|-----------|-------|-----------|-------------------|
| **Maximum Wingspan** | 88.4 m (290.0 ft) | ±50 mm | Top, horizontal |
| **Maximum Height** | 12.8 m (42.0 ft) | ±20 mm | Right side, vertical |
| **BWB Maximum Width** | 20.0 m (65.6 ft) | ±25 mm | Center section |
| **Nose Height** | 3.2 m (10.5 ft) | ±15 mm | Center section |
| **Wing Tip Height** | 2.1 m (6.9 ft) | ±10 mm | Wing tip ground clearance |

### 4.2 **NEW** Propulsion System Front View Layout

**4-Fan Configuration (All Visible from Front):**

| Fan ID | Lateral Position | Vertical Position | Diameter | Notes |
|--------|------------------|-------------------|----------|-------|
| **Fan #1** | +18.0 m (right wing outer) | 2.8 m above ground | **3.5 m** | Clearly visible |
| **Fan #2** | +8.0 m (right wing inner) | 2.8 m above ground | **3.5 m** | Clearly visible |
| **Fan #3** | -8.0 m (left wing inner) | 2.8 m above ground | **3.5 m** | Clearly visible |
| **Fan #4** | -18.0 m (left wing outer) | 2.8 m above ground | **3.5 m** | Clearly visible |

**Critical Fan Spacing:**
- **Outer to Inner Fan Spacing**: 10.0 m center-to-center (each side)
- **Inner Fan Separation**: 16.0 m center-to-center (across centerline)
- **Total Fan Span**: 36.0 m (Fan #1 to Fan #4)
- **Wing Extension Beyond Fans**: 26.2 m total (13.1m each side)

**Annotation Requirements:**
- **"4 FANS TOTAL (ALL VISIBLE IN THIS VIEW)"**
- **Fan diameter**: "Ø 3.5m (11.5 ft)" on representative fans
- **Fan ground clearance**: "1.05m minimum" 
- **Fan lateral positions**: Clearly dimensioned from centerline

### 4.3 BWB Cross-Sectional Geometry

**Wing-Body Blend Profile:**

| Wing Station | Height Above Ground | Local Chord | BWB Integration |
|--------------|-------------------|-------------|-----------------|
| **Centerline (WS 0)** | 12.8 m | 18.6 m | Maximum fuselage height |
| **WS 8m (Fan #2/#3)** | 11.5 m | 16.2 m | Inner fan integration |
| **WS 18m (Fan #1/#4)** | 8.2 m | 12.8 m | Outer fan integration |
| **WS 30m** | 4.5 m | 8.4 m | Mid-wing section |
| **WS 44.2m (Wing tip)** | 2.1 m | 2.1 m | Wing tip |

### 4.4 Landing Gear Configuration (Front View)

**3-Post Landing Gear Layout:**

| Gear Location | Lateral Position | Height Extended | Wheel Configuration |
|---------------|------------------|-----------------|-------------------|
| **Nose Gear** | 0.0 m (centerline) | 2.8 m | Single wheel |
| **Main Post #1** | ±5.2 m | 3.2 m | Dual wheels |
| **Main Post #2** | ±8.8 m | 3.2 m | Dual wheels |
| **Main Post #3** | ±12.1 m | 3.2 m | Dual wheels |

**Gear Triangle Dimensions:**
- **Track Width**: 24.2 m (Main Post #3 to Main Post #3)
- **Wheelbase**: Variable (see side view for longitudinal spacing)
- **Stability Triangle**: Adequate for all loading conditions

### 4.5 Quantum System Front View Locations

**QNS Array (Nose Section):**
- **Lateral Position**: Centerline (±0.0 m)
- **Vertical Position**: 1.5-3.7 m above ground
- **Array Visibility**: 4 sensor apertures in square pattern
- **Front Profile**: Distinctive nose bulge outline

**Wingtip Quantum Sensors:**
- **Left Wingtip**: -44.2 m lateral, 2.1 m height
- **Right Wingtip**: +44.2 m lateral, 2.1 m height
- **Sensor Count**: 3 sensors per wingtip (6 total)
- **Profile**: Small cylindrical protrusions from wing tips

---

## 5. BWB Aerodynamic Cross-Section

### 5.1 Wing-Fuselage Integration Profile

**Critical BWB Characteristics:**
- **Seamless Transition**: No visible junction between wing and fuselage
- **Continuous Curvature**: Mathematically smooth upper surface
- **Load Distribution**: Optimal lift distribution across span
- **Structural Efficiency**: Integrated load paths

### 5.2 Cross-Sectional Area Distribution

**Fuselage Cross-Sections:**

| Station | Width | Height | Area | Function |
|---------|-------|--------|------|----------|
| **Center** | 20.0 m | 12.8 m | 201 m² | Main cabin |
| **Inner Fan** | 16.2 m | 11.5 m | 146 m² | Cabin transition |
| **Outer Fan** | 12.8 m | 8.2 m | 82 m² | Wing integration |
| **Mid Wing** | 8.4 m | 4.5 m | 30 m² | Wing section |
| **Wing Tip** | 2.1 m | 2.1 m | 3.5 m² | Winglet base |

### 5.3 Control Surface Configuration

**Elevon Segments (Front View):**
- **Inboard Elevons**: ±4.25 m to ±12.75 m lateral
- **Middle Elevons**: ±12.75 m to ±22.0 m lateral  
- **Outboard Elevons**: ±22.0 m to ±36.0 m lateral
- **Hinge Lines**: Clearly marked with standard symbols

---

## 6. Professional Title Block

### 6.1 Standardized Title Block Format

```
+---------------------------------------+
| GAIA-QAO Aerospace Organization       |
| Model: AMPEL360 BWB-Q100             |
| Drawing Type: Front View Dimensions  |
| Drawing No.: 00-10-10-02-03 Rev. 1.0 |
| Scale: 1:200                         |
| Date: 16 Jun 2025                    |
| Units: Metric (mm) / Imperial (ft)   |
| Drawn By: Technical Publications     |
| Approved: Chief Engineer             |
| Change Ref: ECN-AMPEL-001           |
+---------------------------------------+
```

### 6.2 Drawing Information Block

**Additional Information:**
- **View Type**: Orthographic front view
- **Projection Standard**: First angle projection
- **Coordinate System**: Aircraft body axes
- **Ground Datum**: 0.0 m reference level
- **Symmetry**: Symmetric about aircraft centerline

---

## 7. Annotation Standards and Callouts

### 7.1 Primary Dimensional Annotations

**Horizontal Dimensions (Top):**
```
Span Callouts Required:
├── 88.4m ±50mm (Maximum wingspan)
├── 44.2m (Semi-span to wingtip)
├── 36.0m (Total fan span)
├── 18.0m (Fan #1/#4 position)
├── 8.0m (Fan #2/#3 position)
└── 0.0m (Aircraft centerline)
```

**Vertical Dimensions (Right Side):**
```
Height Callouts Required:
├── 12.8m ±20mm (Maximum height)
├── 8.2m (Outer wing height)
├── 4.55m (Fan upper edge)
├── 2.8m (Fan centerline)
├── 2.1m (Wing tip height)
├── 1.05m (Fan ground clearance)
└── 0.0m (Ground reference)
```

### 7.2 **UPDATED** Fan System Annotations

**4-Fan Front View Labels:**
- **"4 FANS TOTAL (ALL VISIBLE IN THIS VIEW)"** ✅
- **"Fan #1: Ø 3.5m (+18.0m lateral)"** ✅
- **"Fan #2: Ø 3.5m (+8.0m lateral)"** ✅
- **"Fan #3: Ø 3.5m (-8.0m lateral)"** ✅
- **"Fan #4: Ø 3.5m (-18.0m lateral)"** ✅
- **"Electric Distributed Propulsion System"** ✅
- **"Ground Clearance: 1.05m minimum"** ✅

### 7.3 System Identification Labels

**BWB Configuration:**
- "Blended Wing Body Cross-Section"
- "Seamless Wing-Fuselage Integration"
- "Maximum Width: 20.0m"
- "Continuous Load Distribution"

**Landing Gear System:**
- "3-Post Main Landing Gear Configuration"
- "Track Width: 24.2m"
- "Dual-Wheel Main Gear"
- "Single-Wheel Nose Gear"

**Quantum Systems:**
- "QNS Array - Nose Centerline"
- "Wingtip Quantum Sensors (6 total)"
- "Quantum Communication Integration"

---

## 8. Color Coding System

### 8.1 Aircraft Structure

```
Primary Structure: Black (#000000) - 0.7mm
BWB Upper Surface: Dark Grey (#404040) - 0.5mm
BWB Lower Surface: Medium Grey (#606060) - 0.5mm
Wing Outline: Black (#000000) - 0.7mm
```

### 8.2 System Color Coding

```
Electric Fans (4): Electric Green (#00FF80)
Quantum Systems: Quantum Blue (#0080FF)
Landing Gear: Gear Purple (#8000FF)
Control Surfaces: Control Orange (#FF8000)
Fuel/H2 Systems: Fuel Brown (#804000)
Environmental: ECS Cyan (#00FFFF)
```

### 8.3 Drawing Elements

```
Dimension Lines: Dimension Blue (#0000FF)
Centerlines: Red (#FF0000) - Dashed
Hidden Lines: Light Grey (#808080) - Dashed
Ground Line: Dark Green (#008000) - 0.5mm
Construction Lines: Light Grey (#E0E0E0) - 0.1mm
```

---

## 9. Technical Accuracy Requirements

### 9.1 **NEW** 4-Fan Configuration Verification

**Critical Validation Points:**
1. **Fan Count**: Exactly 4 fans visible (all from front view)
2. **Fan Diameter**: All 3.5m diameter (uniform configuration)
3. **Fan Positions**: ±8m and ±18m from centerline (ECN-AMPEL-001)
4. **Fan Clearances**: 1.05m minimum ground clearance
5. **Fan Integration**: Flush with wing trailing edge

### 9.2 BWB Geometry Validation

**Cross-Sectional Accuracy:**
- **Smooth Curvature**: No discontinuities in wing-body blend
- **Symmetric Profile**: Perfect symmetry about centerline
- **Proportional Accuracy**: Width/height ratios verified
- **Structural Feasibility**: Load paths and manufacturing validated

### 9.3 Ground Clearance Verification

**Operational Clearances:**
- **Fan Ground Clearance**: 1.05m minimum verified
- **Wing Tip Clearance**: 2.1m adequate for operations
- **Landing Gear Clearance**: Adequate extension space
- **BWB Lower Surface**: No interference with ground operations

---

## 10. Manufacturing Applications

### 10.1 Wing Assembly References

**Critical Manufacturing Data:**
- **Fan Installation Points**: 4 precise mounting locations
- **Wing Jig References**: BWB cross-sectional geometry
- **Landing Gear Mounting**: 3-post attachment points
- **Structural Load Paths**: BWB integration requirements

### 10.2 Quality Control Checkpoints

**Inspection Requirements:**
- **Wingspan Verification**: 88.4m ±50mm tolerance
- **Fan Position Check**: ±10mm tolerance on lateral positions
- **BWB Profile Accuracy**: Cross-sectional geometry validation
- **Symmetry Verification**: Left-right wing symmetry check

### 10.3 Ground Support Equipment Design

**GSE Interface Requirements:**
- **Hangar Width**: 88.4m + safety margins
- **Ground Equipment**: 1.05m minimum clearance under fans
- **Towing Equipment**: 3-post landing gear configuration
- **Service Platforms**: BWB profile-compatible access

---

## 11. Companion Drawings Cross-Reference

### 11.1 **COMPLETE** Drawing Set Status

| Drawing ID | Title | Scale | Status |
|------------|-------|-------|--------|
| 00-10-10-01-01 | Aircraft Overview (Isometric) | Variable | **Updated to Rev 2.1** |
| 00-10-10-02-01 | Dimensions Top View | 1:200 | **Updated to Rev 1.1** |
| 00-10-10-02-02 | Dimensions Side View | 1:200 | **Created as Rev 1.0** |
| 00-10-10-02-03 | **Dimensions Front View (This Drawing)** | 1:200 | **New - Rev 1.0** |

### 11.2 Multi-View Coordination

**View Alignment Requirements:**
- **Projection Lines**: Connect corresponding features across views
- **Dimensional Consistency**: All views show same measurements
- **Feature Correlation**: Fan positions match across all views
- **Scale Consistency**: 1:200 scale maintained throughout

### 11.3 Detail Drawing References

**Front View Specific Details:**
- **Drawing 32-XX-XX**: Landing gear front view details
- **Drawing 76-XX-XX**: Fan installation front view
- **Drawing 53-XX-XX**: BWB cross-section structural details
- **Scale**: 1:50 for detailed front view components

---

## 12. Quality Control and Verification

### 12.1 Front View Specific Checklist

**BWB Configuration:**
- [ ] Wing-fuselage blend seamless (no visible junction)
- [ ] Symmetric profile about centerline
- [ ] Smooth curvature transitions throughout
- [ ] Proportionally accurate cross-section

**4-Fan System:**
- [ ] All 4 fans visible and clearly marked
- [ ] Fan diameters: 3.5m each (uniform)
- [ ] Fan positions: ±8m and ±18m from centerline
- [ ] Fan ground clearance: 1.05m minimum
- [ ] Fan integration: flush with wing trailing edge

**Dimensional Accuracy:**
- [ ] Wingspan: 88.4m ±50mm
- [ ] Height: 12.8m ±20mm
- [ ] BWB width: 20.0m ±25mm
- [ ] Fan positions: ±10mm tolerance
- [ ] Landing gear track: 24.2m

### 12.2 Professional Standards Compliance

- [ ] **Title Block**: Complete with all required fields
- [ ] **Line Weights**: ISO 128 standard throughout
- [ ] **Dimensions**: All critical measurements with tolerances
- [ ] **Annotations**: Clear, professional, unambiguous
- [ ] **Color Coding**: Consistent system identification

### 12.3 Multi-View Consistency

- [ ] **Fan Positions**: Match top and side views exactly
- [ ] **Overall Dimensions**: Consistent across all views
- [ ] **System Locations**: Quantum and landing gear alignment
- [ ] **BWB Profile**: Coordinated with side view geometry
- [ ] **Scale Accuracy**: 1:200 maintained throughout

---

## 13. Implementation Notes

### 13.1 Front View Creation Priorities

**Phase 1: Basic Geometry**
1. **BWB Cross-Section**: Establish wing-body profile
2. **Fan Positions**: Place all 4 fans at correct locations
3. **Landing Gear**: Position 3-post configuration
4. **Overall Envelope**: Wingspan and height dimensions

**Phase 2: Professional Standards**
1. **Title Block**: Implement standardized format
2. **Line Weights**: Apply ISO 128 standards
3. **Dimensions**: Add all critical measurements with tolerances
4. **Annotations**: Professional system labeling

**Phase 3: Integration**
1. **Multi-View Coordination**: Align with other drawings
2. **Quality Control**: Complete verification checklist
3. **Approval Process**: Technical and management sign-off
4. **Archive and Distribution**: Final document control

### 13.2 Critical Success Factors

**Technical Accuracy:**
- **4-Fan Configuration**: Exactly as specified in ECN-AMPEL-001
- **BWB Geometry**: Aerodynamically valid cross-section
- **Dimensional Precision**: Manufacturing-grade tolerances
- **System Integration**: Realistic component placement

**Professional Presentation:**
- **Drawing Standards**: Full ISO 128 compliance
- **Clear Communication**: Unambiguous annotations
- **Complete Documentation**: All required information present
- **Quality Assurance**: Verified and approved

---

## 14. Usage and Applications

### 14.1 Engineering Applications

**Design Validation:**
- **BWB Cross-Section Analysis**: Structural and aerodynamic validation
- **Fan Integration Study**: Propulsion system verification
- **Ground Clearance Analysis**: Operational safety confirmation
- **Span Compatibility**: Airport and hangar facility planning

### 14.2 Manufacturing Applications

**Production Planning:**
- **Wing Assembly**: BWB manufacturing sequence
- **Fan Installation**: 4-fan mounting procedures
- **Quality Control**: Dimensional verification standards
- **Tooling Design**: Jigs and fixtures requirements

### 14.3 Operational Applications

**Airport Compatibility:**
- **Gate Assignments**: Wingspan accommodation
- **Ground Operations**: Clearance verification
- **Maintenance Access**: Service equipment compatibility
- **Emergency Procedures**: Aircraft configuration awareness

---

## Summary

This front-view dimensional drawing completes the professional engineering drawing set for the AMPEL360 BWB-Q100 aircraft with the **optimized 4-fan propulsion configuration**. The drawing shows all critical span and height relationships, BWB cross-sectional geometry, and system integration from the front perspective, essential for manufacturing, airport operations, and certification.

**Key Features:**
- **Complete 4-fan visibility** with precise positioning (±8m, ±18m)
- **BWB cross-sectional profile** showing seamless wing-fuselage integration
- **Professional drawing standards** with ISO 128 compliance
- **Manufacturing-ready tolerances** for production use
- **Multi-view coordination** completing the drawing set
- **ECN-AMPEL-001 full compliance**

---

**END OF SPECIFICATION**

*For technical support contact:*  
*Engineering Drawing Office*  
*Email: drawings@gaia-qao.aero*  
*Change Control: ECN-AMPEL-001*
