# Q-AVIOGEN Avatar Model Specification
## Amedeo Pelliccia - Aerospace Maintenance Instructor

### 📋 Project Information

**Project Name:** GAIA-QAO / Q-AVIOGEN Avatar System  
**Avatar Role:** Aerospace Maintenance Instructor  
**Subject:** Amedeo Pelliccia  
**Model Purpose:** Video-guided technical procedures using Blender  
**Version:** 1.0  
**Date:** June 20, 2025  
**Output Format:** .blend (with PBR textures and facial rig)  
**Compatibility:** Blender 3.0+, Q-AVIOGEN v2.1 rendering pipeline  

---

### 🎯 Project Overview

This avatar will be used in **Q-AVIOGEN**, an advanced system for generating animated aeronautical documentation. The avatar of Amedeo Pelliccia will serve as a **technical instructor** guiding viewers through aircraft maintenance procedures with realistic gestures, facial expressions, and professional appearance.

**Key Use Case:** ATA 32-11-00 Nose Landing Gear Visual Inspection  
**Target Duration:** 55 seconds of animated instruction  
**Languages:** Spanish (primary), English (secondary)  
**Audience:** Aviation maintenance professionals and trainees  

---

### 📸 Reference Materials Required

**From Subject (Amedeo Pelliccia):**

#### Essential References:
- [ ] **Frontal portrait** - Neutral expression, high-resolution (min. 2048x2048), well-lit
- [ ] **Profile views** - Left and right side profiles, same lighting conditions
- [ ] **3/4 angle views** - Both sides, for complete facial structure reference
- [ ] **Expression samples** - Smiling, serious, focused, explaining (for rigging reference)

#### Optional References:
- [ ] **Motion reference video** - Short clip (30-60 seconds) showing natural gestures
- [ ] **Clothing reference** - Photos in preferred maintenance uniform/jumpsuit
- [ ] **Hand gestures** - Photos of natural pointing, explaining, thumbs-up poses

#### Professional Context:
- [ ] **Uniform style preference** - Industrial maintenance, aviation technician style
- [ ] **Accessories** - Safety vest, gloves, clipboard, earpiece preferences
- [ ] **Branding elements** - Company logos, patches, name tags (if applicable)

---

### 🧍‍♂️ Detailed Model Requirements

#### 1. Avatar Specifications

**Physical Characteristics:**
- **Height:** ~1.78m (scaled for aircraft maintenance environment)
- **Build:** Professional maintenance technician physique
- **Age Appearance:** Mature, experienced instructor (based on reference photos)
- **Hair/Eyes/Skin:** Accurate to reference photography
- **Facial Features:** Must capture Amedeo's distinctive characteristics

**Style Guidelines:**
- **Target Style:** Realistic PBR (non-cartoon, professional training suitable)
- **Quality Level:** High-end character model suitable for close-up shots
- **Topology:** Clean quad-based mesh optimized for animation
- **Polygon Count:** 15,000-25,000 triangles (optimized for real-time rendering)

#### 2. Professional Clothing & Accessories

**Primary Outfit - Maintenance Uniform:**
- **Base:** Technical jumpsuit or work shirt + pants
- **Color Scheme:** Professional blue/gray tones (aviation industry standard)
- **Material:** Realistic fabric simulation (cotton/polyester blend appearance)
- **Fit:** Professional, not too loose or tight, suitable for movement

**Safety Equipment:**
- **Safety Vest:** High-visibility yellow/orange with reflective strips
- **Gloves:** Optional work gloves (removable)
- **Safety Glasses:** Optional (can be worn on head or around neck)
- **Hard Hat/Cap:** Optional, depends on procedure requirements

**Professional Accessories:**
- **Clipboard:** For documentation and checklists
- **Pen/Pencil:** Attached to clipboard or uniform pocket
- **Badge/ID:** Company identification if applicable
- **Tool Belt:** Light tool belt with basic inspection tools
- **Earpiece:** Optional communication device

#### 3. Rigging Requirements

**Facial Rig (Essential):**
- **Mouth/Lips:** Full lip sync support with visemes for Spanish and English
- **Eyes:** Eye tracking, blinking, eyebrow movement
- **Facial Expressions:** Happy, serious, focused, concerned, explaining, warning
- **Head Movement:** Natural head tilting and nodding for emphasis

**Body Rig (Animation-Ready):**
- **Arms/Hands:** Precise finger control for pointing and tool use
- **Torso:** Natural upper body movement for gestures
- **Legs:** Basic walking and crouching for tire inspection
- **Root Bone:** Origin at feet for proper ground placement

**Gesture Support (Specific to Aviation Procedures):**
- `point_down_gesture` - Pointing to aircraft ground position
- `sweeping_arm_gesture` - Indicating area clearance
- `pointing_close_inspection` - Detailed component examination
- `crouch_inspect_tire` - Low-level tire inspection pose
- `trace_mechanical_parts` - Following mechanical connections
- `point_technology_display` - Indicating sensors and displays
- `thumbs_up_approval` - Completion and approval gesture

**Animation Compatibility:**
- **Blender Action System:** Compatible with Action strips and NLA
- **Keyframe Animation:** Support for manual keyframe animation
- **Mocap Ready:** Bone structure suitable for motion capture data
- **IK/FK Switching:** Arms and legs with IK/FK controls

---

### 🎨 Materials & Textures Specifications

#### Texture Resolution & Format:
- **Minimum Resolution:** 2048x2048 pixels
- **Preferred Resolution:** 4096x4096 pixels for close-up shots
- **Format:** PNG (with alpha where needed) or high-quality JPG
- **Color Space:** sRGB for Blender compatibility

#### PBR Material Workflow:
- **Albedo/Diffuse:** Base color without lighting information
- **Normal Map:** Surface detail and micro-geometry
- **Roughness:** Surface material properties (matte to glossy)
- **Metallic:** Metallic vs. non-metallic surface definition
- **Ambient Occlusion:** Optional, for enhanced depth
- **Emission:** For any glowing elements (safety lights, displays)

#### Specific Texture Maps Required:

**Face Textures:**
- `face_albedo.png` - Skin color and features
- `face_normal.png` - Facial detail and pores
- `face_roughness.png` - Skin material properties
- `face_specular.png` - Reflection characteristics

**Body/Clothing Textures:**
- `body_albedo.png` - Skin areas (hands, neck)
- `uniform_albedo.png` - Jumpsuit/shirt fabric
- `vest_albedo.png` - Safety vest materials
- `accessories_albedo.png` - Tools, clipboard, etc.

#### UV Mapping Requirements:
- **Non-overlapping UVs:** No texture stretching or overlap
- **Seam Placement:** Hidden seams in natural body/clothing boundaries
- **Texture Density:** Consistent texel density across all surfaces
- **Face Priority:** Highest resolution for facial features

#### Material Naming Convention:
- `AME_Skin_Face` - Facial skin material
- `AME_Skin_Body` - Body skin material
- `AME_Uniform_Fabric` - Main uniform material
- `AME_Safety_Vest` - High-visibility vest
- `AME_Hair` - Hair/eyebrows material
- `AME_Eyes` - Eye material with proper refraction

---

### 🎬 Animation & Performance Requirements

#### Target Animation Scenarios:

**Scenario 1: ATA 32-11-00 Nose Gear Inspection (55 seconds)**
- **0-6.5s:** Aircraft position verification with pointing gestures
- **6.5-14s:** Area clearance with sweeping arm movements
- **14-21s:** Close strut inspection with detailed pointing
- **21-30s:** Tire inspection requiring crouch position
- **30-36s:** Steering system examination with tracing gestures
- **36-49s:** Technology display indication with precise pointing
- **49-55s:** Completion gesture with thumbs-up approval

#### Performance Optimization:
- **Real-time Friendly:** Suitable for 30fps real-time rendering
- **LOD Support:** Multiple levels of detail for distant shots
- **Bone Count:** Maximum 150 bones for compatibility
- **Deformation Quality:** Smooth deformation without artifacts

#### Camera Requirements:
- **Close-up Ready:** Facial detail suitable for 85mm lens equivalent
- **Wide Shot Compatible:** Full body visible and recognizable
- **Multiple Angles:** Profile, 3/4, frontal views all optimized

---

### 🔧 Technical Specifications

#### File Structure & Organization:

**Main Blender File:** `avatar_model.blend`
```
Collections:
├── AME_Avatar (main character)
├── AME_Rig (armature and controls)
├── AME_Clothing (uniform and accessories)
└── AME_References (reference images and guides)

Objects:
├── AME_Body (main mesh)
├── AME_Head (separate for detail)
├── AME_Hair (separate mesh or particle system)
├── AME_Uniform (clothing mesh)
├── AME_Accessories (tools, clipboard, etc.)
└── AME_Armature (main rig)
```

#### Blender Settings:
- **Units:** Metric (meters)
- **Scale:** Real-world scale (1.78m height)
- **Origin:** Armature root at ground level (Z=0)
- **Forward Axis:** Y-Forward (Blender standard)
- **Up Axis:** Z-Up

#### Export Compatibility:
- **FBX Export:** Must export cleanly to FBX for other software
- **USD Export:** Compatible with Universal Scene Description
- **glTF Export:** Web-compatible format for browser rendering

---

### 🧪 Quality Assurance & Testing

#### Pre-Delivery Testing:

**Visual Quality Check:**
- [ ] Facial resemblance to reference photos verified
- [ ] Clothing and accessories properly fitted
- [ ] Materials render correctly under different lighting
- [ ] No obvious modeling artifacts or errors

**Animation Testing:**
- [ ] All required gestures functional
- [ ] Facial expressions natural and appropriate
- [ ] Lip sync compatibility verified
- [ ] No bone deformation issues

**Technical Validation:**
- [ ] File size reasonable (< 50MB for .blend file)
- [ ] All textures properly linked and packed
- [ ] Material names follow convention
- [ ] UV maps properly assigned

#### Integration Testing:
After delivery, the avatar will be tested in the actual Q-AVIOGEN pipeline:
- [ ] Import into animated scene successful
- [ ] Synchronization with `amedeo_voice.wav` audio
- [ ] Rendering in actual ATA 32-11-00 procedure
- [ ] Multiple camera angles and lighting conditions
- [ ] Performance in 55-second animated sequence

---

### 📦 Deliverables & File Structure

#### Required Deliverables:

**1. Main Avatar File:**
- `avatar_model.blend` - Complete rigged avatar with all materials

**2. Texture Assets:**
- `face_texture.png` - High-resolution facial texture
- `body_texture.png` - Body skin textures
- `uniform_texture.png` - Clothing and accessories textures
- `normal_maps/` - All normal map textures
- `roughness_maps/` - Material property maps

**3. Documentation:**
- `README.md` - Setup and usage instructions
- `rig_guide.md` - Bone structure and animation controls
- `material_guide.md` - Material setup and customization

**4. Reference Files:**
- `reference_photos/` - Original reference images used
- `texture_sources/` - Source files for texture creation
- `version_notes.txt` - Development notes and changelog

#### File Organization:
```
delivery_package/
├── avatar_model.blend
├── textures/
│   ├── face_texture.png
│   ├── body_texture.png
│   ├── uniform_texture.png
│   ├── normals/
│   └── roughness/
├── documentation/
│   ├── README.md
│   ├── rig_guide.md
│   └── material_guide.md
└── references/
    ├── photos/
    ├── sources/
    └── notes.txt
```

---

### 🎯 Success Criteria

The delivered avatar will be considered successful when:

✅ **Visual Accuracy:** Recognizable as Amedeo Pelliccia from reference photos  
✅ **Professional Appearance:** Suitable for aviation training environment  
✅ **Animation Ready:** All required gestures functional and natural  
✅ **Technical Quality:** Renders efficiently in Q-AVIOGEN pipeline  
✅ **Material Quality:** PBR materials look realistic under various lighting  
✅ **Lip Sync Compatible:** Mouth movements sync with Spanish/English speech  
✅ **Performance Optimized:** Maintains 30fps in real-time scenarios  

---

### 📅 Timeline & Milestones

#### Suggested Development Timeline:

**Week 1: Modeling & Initial Rigging**
- [ ] Base mesh creation from reference photos
- [ ] Initial clothing and accessories modeling
- [ ] Basic rig setup and testing

**Week 2: Texturing & Materials**
- [ ] Facial texture creation and mapping
- [ ] Clothing and accessory texturing
- [ ] PBR material setup and testing

**Week 3: Animation & Refinement**
- [ ] Gesture animation setup
- [ ] Facial rig refinement for expressions
- [ ] Quality assurance and bug fixing

**Week 4: Delivery & Integration**
- [ ] Documentation creation
- [ ] File packaging and delivery
- [ ] Integration testing and feedback

#### Key Milestones:
- **Day 7:** Basic model and rig review
- **Day 14:** Texture and material review
- **Day 21:** Animation testing and feedback
- **Day 28:** Final delivery and integration

---

### 💰 Budget & Licensing

#### Licensing Terms:
- **Usage Rights:** Exclusive license for Q-AVIOGEN and GAIA-QAO projects
- **Modification Rights:** Full rights to modify and adapt the model
- **Distribution:** Internal use within organization and authorized training partners
- **Commercial Use:** Permitted for aviation training and educational purposes

#### Intellectual Property:
- **Likeness Rights:** Based on Amedeo Pelliccia's consent for avatar use
- **Model Rights:** Full ownership of 3D model and associated assets
- **Texture Rights:** All custom textures owned by GAIA-QAO
- **Reference Rights:** Reference photos remain property of subject

---

### 📞 Contact & Communication

#### Primary Contact:
**Amedeo Pelliccia**  
Email: amedepelliccia@gaiaqao.org  
Role: Project Lead & Avatar Subject  

#### Technical Contact:
**Q-AVIOGEN Development Team**  
Email: development@gaiaqao.org  
Role: Technical Integration & Testing  

#### Communication Protocol:
- **Progress Updates:** Weekly status reports
- **Review Sessions:** Video calls for milestone reviews
- **File Sharing:** Secure cloud storage for large files
- **Feedback Process:** Structured review with specific actionable items

#### Revision Policy:
- **Major Revisions:** Up to 2 rounds of significant changes included
- **Minor Adjustments:** Unlimited small fixes and refinements
- **Timeline Adjustments:** Flexible within reason for quality delivery

---

### 🔒 Confidentiality & Security

#### Data Protection:
- [ ] All reference photos treated as confidential
- [ ] Work-in-progress files secured during development
- [ ] Final deliverables transferred securely
- [ ] Source files deleted from artist systems after delivery

#### Quality Standards:
- [ ] Professional aviation industry standards maintained
- [ ] Suitable for regulatory compliance documentation
- [ ] Appropriate for international training deployment
- [ ] Compatible with enterprise security requirements

---

**This specification document serves as the complete guide for creating the Amedeo Pelliccia avatar for the Q-AVIOGEN system. Any questions or clarifications should be directed to the contacts listed above.**

---

*Document Version: 1.0*  
*Last Updated: June 20, 2025*  
*Project: GAIA-QAO / Q-AVIOGEN Avatar System*
