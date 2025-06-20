# 00-10-10-03 Capacities

## Document Information
- **ATA Chapter**: 00 - General
- **Section**: 00-10 - Aircraft General
- **Subsection**: 00-10-10 - General Description
- **Document ID**: 00-10-10-03
- **GQOIS ID**: GQOIS-Q-AIR-00-10-CAPC-001
- **Revision**: 2.0
- **Effective Date**: 2025-06-15
- **Review Cycle**: Annual
- **Distribution**: Unrestricted

---

## 1. Payload Capacities

### 1.1 Passenger Capacity

```
[Figure 00-10-10-03-01: Passenger Configuration Options]

THREE-CLASS CONFIGURATION (Standard):
┌────────────────────────────────────────────┐
│ First │ Business │ Premium Economy │ Economy│
│  24   │    60    │       80       │   150  │
└────────────────────────────────────────────┘
                Total: 314 Passengers

TWO-CLASS CONFIGURATION:
┌────────────────────────────────────────────┐
│    Business    │         Economy            │
│       42       │           308              │
└────────────────────────────────────────────┘
                Total: 350 Passengers

HIGH-DENSITY CONFIGURATION:
┌────────────────────────────────────────────┐
│              All Economy                    │
│                 385                         │
└────────────────────────────────────────────┘
                Total: 385 Passengers
```

### 1.2 Passenger Configuration Details

| Class | Seats | Pitch | Width | Config | Weight/Pax |
|-------|-------|-------|-------|--------|------------|
| **First Class** | 24 | 82" (208 cm) | 32" (81 cm) | 1-2-1 | 195 kg |
| **Business** | 60 | 60" (152 cm) | 22" (56 cm) | 2-3-2 | 185 kg |
| **Premium Economy** | 80 | 38" (97 cm) | 19" (48 cm) | 2-4-2 | 175 kg |
| **Economy** | 150 | 32" (81 cm) | 18" (46 cm) | 3-4-3 | 170 kg |

**Standard Passenger Weights (including carry-on):**
- Domestic: 175 kg average
- International: 185 kg average
- Charter: 170 kg average

### 1.3 Cargo Capacity

| Compartment | Volume (m³) | Volume (ft³) | Max Load (kg) | Max Load (lb) |
|-------------|-------------|--------------|---------------|---------------|
| **Forward Hold** | 105 | 3,708 | 18,000 | 39,683 |
| **Aft Hold** | 125 | 4,414 | 22,000 | 48,502 |
| **Bulk** | 45 | 1,589 | 6,000 | 13,228 |
| **Total Lower Deck** | 275 | 9,711 | 46,000 | 101,413 |
| **Main Deck (Freighter)** | 580 | 20,483 | 65,000 | 143,300 |

**Container Capacity:**
- Forward Hold: 10 × LD3 or 5 × LD8
- Aft Hold: 12 × LD3 or 6 × LD8
- Bulk: Loose load only

---

## 2. Fuel System Capacities

### 2.1 Fuel Tank Configuration

```
[Figure 00-10-10-03-02: Fuel Tank Layout]

TOP VIEW - Fuel Distribution:
    ╱─────────────────────────────────╲
   ╱  CTR │ MAIN L │ MAIN R │ CTR    ╲
  │   1   │        │        │   2     │
  │ 8,000L│ 35,000L│ 35,000L│ 8,000L  │
  │       │        │        │         │
  │  RES L│  FEED  │  FEED  │ RES R   │
  │ 2,000L│   TK   │   TK   │ 2,000L  │
  ╲       │ 15,000L│ 15,000L│        ╱
   ╲      │ SURGE  │ SURGE  │       ╱
    ╲     │ 1,000L │ 1,000L │      ╱
     ╲────────────────────────────╱
```

### 2.2 Fuel Capacity Summary

| Tank | Capacity (L) | Capacity (USG) | Capacity (kg)* | Location |
|------|--------------|----------------|----------------|----------|
| **Main Left** | 35,000 | 9,246 | 28,000 | Wing box left |
| **Main Right** | 35,000 | 9,246 | 28,000 | Wing box right |
| **Center 1** | 8,000 | 2,113 | 6,400 | Forward center |
| **Center 2** | 8,000 | 2,113 | 6,400 | Aft center |
| **Feed Left** | 15,000 | 3,963 | 12,000 | Inner wing left |
| **Feed Right** | 15,000 | 3,963 | 12,000 | Inner wing right |
| **Reserve Left** | 2,000 | 528 | 1,600 | Outboard left |
| **Reserve Right** | 2,000 | 528 | 1,600 | Outboard right |
| **Surge (2×)** | 2,000 | 528 | - | Overflow only |
| **Total Usable** | 120,000 | 31,701 | 96,000 | - |
| **Total Capacity** | 122,000 | 32,229 | 97,600 | Including surge |

*At density 0.8 kg/L (typical SAF)

### 2.3 Hydrogen Storage (Future Capability)

| Tank | Volume (m³) | LH2 Capacity (kg) | Location |
|------|-------------|-------------------|----------|
| **Primary** | 45 | 3,150 | Aft fuselage |
| **Secondary** | 30 | 2,100 | Forward fuselage |
| **Total** | 75 | 5,250 | - |

---

## 3. Electrical Storage Capacities

### 3.1 Battery System Configuration

```
[Figure 00-10-10-03-03: Battery Layout]

BATTERY BAY ARRANGEMENT:
┌─────────────────────────────────────┐
│ MAIN BAT 1 │ MAIN BAT 2 │ MAIN BAT 3│
│  1.67 MWh  │  1.67 MWh  │  1.67 MWh │
├────────────┴────────────┴───────────┤
│      QUANTUM MANAGED COOLING         │
├─────────────────────────────────────┤
│ BACKUP │ APU START │ EMERGENCY      │
│ 50 kWh │  30 kWh   │  100 kWh       │
└─────────────────────────────────────┘
```

### 3.2 Battery Capacity Details

| System | Capacity | Voltage | Technology | Location |
|--------|----------|---------|------------|----------|
| **Main Battery 1** | 1.67 MWh | 800V DC | Li-Metal Quantum | Bay 1 |
| **Main Battery 2** | 1.67 MWh | 800V DC | Li-Metal Quantum | Bay 2 |
| **Main Battery 3** | 1.67 MWh | 800V DC | Li-Metal Quantum | Bay 3 |
| **Total Main** | 5.0 MWh | 800V DC | - | - |
| **Backup Battery** | 50 kWh | 28V DC | Li-Ion | E-Bay |
| **APU Start** | 30 kWh | 28V DC | Li-Ion | APU Bay |
| **Emergency** | 100 kWh | 270V DC | Li-Ion | Distributed |

**Power Density Specifications:**
- Main batteries: 450 Wh/kg
- Total battery weight: 11,111 kg
- Charge rate: 2C maximum (10 MW)
- Discharge rate: 4C maximum (20 MW)

---

## 4. Fluid System Capacities

### 4.1 Hydraulic System

| System | Capacity (L) | Type | Operating Pressure |
|--------|--------------|------|-------------------|
| **System 1** | 45 | Skydrol LD-4 | 5,000 psi |
| **System 2** | 45 | Skydrol LD-4 | 5,000 psi |
| **System 3** | 35 | Skydrol LD-4 | 5,000 psi |
| **Backup** | 25 | Skydrol LD-4 | 3,000 psi |
| **Total** | 150 | - | - |

### 4.2 Engine Oil System

| System | Capacity (L) | Type | Min Operating |
|--------|--------------|------|---------------|
| **Turbogen 1** | 35 | Synthetic Turbine Oil | 12 L |
| **Turbogen 2** | 35 | Synthetic Turbine Oil | 12 L |
| **APU** | 8 | Synthetic Turbine Oil | 3 L |
| **Electric Motors (8×)** | 5 each | Synthetic Coolant | 2 L each |
| **Total** | 118 | - | - |

### 4.3 Environmental Systems

```
[Figure 00-10-10-03-04: Water/Waste System Capacities]

POTABLE WATER:            WASTE SYSTEM:
┌─────────────┐          ┌─────────────┐
│ Tank 1: 800L│          │ Fwd: 1,200L │
├─────────────┤          ├─────────────┤
│ Tank 2: 800L│          │ Aft: 1,500L │
├─────────────┤          ├─────────────┤
│ Tank 3: 600L│          │Backup: 300L │
└─────────────┘          └─────────────┘
Total: 2,200L            Total: 3,000L
```

### 4.4 System Fluid Summary

| System | Capacity | Service Interval |
|--------|----------|------------------|
| **Potable Water** | 2,200 L | Every flight |
| **Waste Water** | 3,000 L | Every flight |
| **Windshield Wash** | 20 L | 100 hours |
| **Cooling System** | 150 L | 1,000 hours |
| **De-icing Fluid** | 200 L | As required |

---

## 5. Quantum System Capacities

### 5.1 Cryogenic Systems

| System | Medium | Capacity | Consumption | Refill Interval |
|--------|--------|----------|-------------|-----------------|
| **QPU Cooling** | Liquid Helium | 500 L | 2 L/hour | 200-250 hours |
| **Pre-cooling** | Liquid Nitrogen | 1,000 L | 5 L/hour | 200 hours |
| **Backup Cooling** | Liquid Helium | 100 L | Emergency only | N/A |
| **Shield Cooling** | Liquid Nitrogen | 200 L | 1 L/hour | 200 hours |

### 5.2 Quantum Component Specifications

```
[Figure 00-10-10-03-05: Quantum System Layout]

QPU COOLING CIRCUIT:
┌─────────────────┐
│ He Dewar (500L) │
├─────────────────┤
│ Distribution    │──→ QPU Core (15mK)
│ Manifold        │──→ Quantum Bus (4K)
├─────────────────┤──→ Shield (77K)
│ Recovery System │
└─────────────────┘
```

**Operating Parameters:**
- QPU operating temperature: 15 millikelvin
- Helium boil-off rate: 2 L/hour nominal
- Emergency hold time: 50 hours (on backup)
- Refill port location: FS 25000, VL -500

---

## 6. Passenger Service Capacities

### 6.1 Galley Equipment Capacity

| Galley | Location | Ovens | Coffee | Chillers | Carts |
|--------|----------|-------|--------|----------|-------|
| **G1 (First)** | Forward | 4 | 2 | 4 | 8 |
| **G2 (Business)** | Mid-Forward | 6 | 3 | 6 | 12 |
| **G3 (Economy)** | Mid-Aft | 8 | 4 | 8 | 16 |
| **G4 (Economy)** | Aft | 6 | 3 | 6 | 12 |
| **Total** | - | 24 | 12 | 24 | 48 |

### 6.2 Lavatory Capacities

| Deck | Number | Waste per Unit | Water per Unit | Total Capacity |
|------|--------|----------------|----------------|----------------|
| **Main Deck** | 12 | 100 L | 60 L | 1,920 L |
| **Upper Deck** | 4 | 100 L | 60 L | 640 L |
| **Crew** | 2 | 50 L | 40 L | 180 L |
| **Total** | 18 | - | - | 2,740 L |

---

## 7. Cargo Loading Capacities

### 7.1 Cargo Compartment Details

```
[Figure 00-10-10-03-06: Cargo Loading Envelope]

FORWARD HOLD:                AFT HOLD:
┌─────────────┐             ┌─────────────┐
│ Height: 2.2m│             │ Height: 2.2m│
│ Width: 4.2m │             │ Width: 4.8m │
│Length: 11.3m│             │Length: 11.8m│
│             │             │             │
│ ┌─┬─┬─┬─┬─┐│             │┌─┬─┬─┬─┬─┬┐│
│ │││││││││││             ││││││││││││││
│ └─┴─┴─┴─┴─┘│             │└─┴─┴─┴─┴─┴┘│
│   10 × LD3  │             │  12 × LD3   │
└─────────────┘             └─────────────┘
```

### 7.2 Container/Pallet Capacity

| Hold | LD3 | LD8 | LD11 | 88" Pallet | 96" Pallet |
|------|-----|-----|------|-------------|-------------|
| **Forward** | 10 | 5 | - | 4 | 3 |
| **Aft** | 12 | 6 | - | 5 | 4 |
| **Main Deck (F)** | - | - | 18 | 14 | 12 |

### 7.3 Weight Distribution Limits

| Zone | Max Floor Loading | Max Container Weight | Max Linear Load |
|------|-------------------|---------------------|-----------------|
| **Fwd Hold** | 2,400 kg/m² | 1,588 kg | 3,000 kg/m |
| **Aft Hold** | 2,400 kg/m² | 1,588 kg | 3,000 kg/m |
| **Bulk** | 1,200 kg/m² | N/A | 1,500 kg/m |
| **Main Deck** | 4,800 kg/m² | 6,804 kg | 6,000 kg/m |

---

## 8. Environmental Control Capacities

### 8.1 Air Conditioning System

| Parameter | Capacity | Units | Notes |
|-----------|----------|-------|-------|
| **Airflow Rate** | 15,000 | kg/min | Sea level |
| **Cooling Capacity** | 450 | kW | Maximum |
| **Heating Capacity** | 350 | kW | Maximum |
| **Fresh Air** | 11.8 | L/s/pax | Minimum |
| **Recirculation** | 50 | % | Typical |
| **HEPA Filters** | 24 | units | 99.97% efficiency |

### 8.2 Pressurization

```
[Figure 00-10-10-03-07: Pressurization Schedule]

Altitude (ft)  Cabin Alt (ft)
    0     ───────  0
         ╱
10,000  ╱─────── 2,000
       ╱
25,000 ──────── 6,000
      │
41,000 ──────── 8,000 (max)
```

**Pressurization Capacity:**
- Maximum differential: 9.4 psi
- Cabin altitude at FL410: 8,000 ft
- Rate of change: 300 ft/min normal
- Emergency descent: 2,000 ft/min

---

## 9. Operational Weights and Capacities

### 9.1 Weight Summary

| Parameter | Weight (kg) | Weight (lb) | Notes |
|-----------|-------------|-------------|--------|
| **Operating Empty** | 195,000 | 429,901 | Including quantum systems |
| **Max Zero Fuel** | 285,000 | 628,317 | Structural limit |
| **Max Takeoff** | 380,000 | 837,757 | Certified limit |
| **Max Landing** | 320,000 | 705,479 | Structural limit |
| **Max Payload** | 90,000 | 198,416 | At max fuel |

### 9.2 Payload-Range Matrix

```
[Figure 00-10-10-03-08: Payload-Range Diagram]

Payload (tonnes)
  90 │●
     │ ╲
  80 │  ╲
     │   ╲
  70 │    ╲
     │     ╲●────────────
  60 │               ╲
     │                ╲
  50 │                 ●
     └─────┬────┬────┬────┬
           3000 5000 7000 9000
           Range (nm)
```

| Configuration | Payload | Range | Fuel |
|---------------|---------|-------|------|
| **Max Payload** | 90,000 kg | 3,200 nm | 50,000 kg |
| **Typical** | 70,000 kg | 7,800 nm | 96,000 kg |
| **Max Range** | 50,000 kg | 9,200 nm | 96,000 kg |

---

## 10. Special Mission Capacities

### 10.1 Quick Change (QC) Configuration

**Conversion Capacity:**
- Passenger to freight: 4 hours
- Freight to passenger: 6 hours
- Mixed configuration: 2 hours

**QC Options:**
| Configuration | Forward | Center | Aft |
|---------------|---------|--------|-----|
| **Full PAX** | 120 pax | 120 pax | 120 pax |
| **Combi** | Cargo | 120 pax | 120 pax |
| **Full Cargo** | Cargo | Cargo | Cargo |

### 10.2 Medical Evacuation Capacity

- Patient beds: Up to 120
- Intensive care stations: 12
- Medical oxygen: 5,000 L
- Medical power: 50 kW

### 10.3 VIP Configuration

- Private suites: 8
- Conference room: 20 persons
- Bedroom capacity: 16 persons
- Extended range fuel: 110,000 L

---

## 11. Growth Capacity

### 11.1 System Growth Margins

| System | Current | Maximum | Growth % |
|--------|---------|---------|----------|
| **Electrical Power** | 10 MW | 15 MW | 50% |
| **Hydraulic Flow** | 150 L/min | 200 L/min | 33% |
| **Cooling Capacity** | 450 kW | 600 kW | 33% |
| **Data Bus** | 1 Gbps | 10 Gbps | 900% |
| **QPU Qubits** | 72 | 144 | 100% |

### 11.2 Structural Growth Potential

- MTOW growth: 380,000 → 420,000 kg
- Additional fuel: Space for 10,000 L
- Cargo volume: 20% increase possible
- Passenger capacity: Up to 420 in high-density

---

## Summary

The AMPEL360 BWB-Q100 offers exceptional capacity across all systems, with significant growth potential built into the design. Key capacity highlights include:

- **Passengers**: 314 (standard) to 385 (high-density)
- **Cargo Volume**: 275 m³ (lower) + 580 m³ (main deck freighter)
- **Fuel**: 120,000 L usable capacity
- **Batteries**: 5.0 MWh main storage
- **Range**: 7,800 nm with typical payload

The integration of quantum systems adds unique capacity requirements (cryogenic storage) while enabling unprecedented operational efficiency. All capacities are designed with 20-50% growth margins to accommodate future technology upgrades and operational demands.

---

**Reference Documents:**
- 00-10-10-04-Performance.md - Performance capabilities
- 00-20-00-00-WeightBalance.md - Weight and balance details
- 28-00-00-00-Fuel.md - Fuel system details
- 24-00-00-00-ElectricalPower.md - Electrical system details

---

**END OF CAPACITIES DOCUMENT**

*Next Document: 00-10-10-04-Performance.md*
