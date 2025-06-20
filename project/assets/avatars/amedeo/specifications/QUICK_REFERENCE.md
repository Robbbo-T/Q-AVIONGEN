# Quick Reference - Avatar Creation Checklist
## Amedeo Pelliccia 3D Avatar for Q-AVIOGEN

### 📋 Essential Requirements Summary

#### 🎯 **Project Goal**
Create realistic 3D avatar of Amedeo Pelliccia for aviation maintenance instruction videos.

#### 📏 **Key Specifications**
- **Height:** 1.78m
- **Style:** Realistic PBR (not cartoon)
- **Clothing:** Maintenance uniform + safety vest
- **Rigging:** Full body + facial animation
- **Format:** Blender 3.0+ (.blend file)

#### 🎬 **Required Animations**
Must support these 7 specific gestures:
1. Point down (aircraft position)
2. Sweeping arm (area clearance)  
3. Close inspection pointing (strut examination)
4. Crouch inspection (tire check)
5. Trace mechanical parts (steering)
6. Point to displays (sensors)
7. Thumbs up (completion)

#### 🖼️ **Texture Requirements**
- **Resolution:** 2K minimum, 4K preferred
- **Format:** PNG/JPG
- **Maps:** Albedo, Normal, Roughness, Metallic
- **Quality:** Close-up camera ready

#### 📦 **Deliverables**
- `avatar_model.blend` - Main rigged model
- `face_texture.png` - Facial textures
- `body_texture.png` - Body/clothing textures  
- `README.md` - Usage instructions

#### ⏰ **Timeline**
- **Week 1:** Modeling + basic rig
- **Week 2:** Texturing + materials
- **Week 3:** Animation setup + testing
- **Week 4:** Delivery + integration

#### 💡 **Success Criteria**
✅ Recognizable as Amedeo from photos  
✅ Professional aviation instructor appearance  
✅ All 7 required gestures working  
✅ Lip sync compatible (Spanish/English)  
✅ Renders at 30fps in real-time  

---

### 📸 **Reference Photos Needed**

**Essential from Amedeo Pelliccia:**
- [ ] Front portrait (neutral, high-res)
- [ ] Left & right profile views
- [ ] 3/4 angle views (both sides)
- [ ] Expression samples (serious, explaining, friendly)
- [ ] Uniform/clothing preferences
- [ ] Natural gesture video (30-60 seconds)

---

### 🔧 **Technical Notes**

**Blender Setup:**
- Units: Metric (meters)
- Scale: Real-world (1.78m)
- Origin: Ground level (Z=0)
- Forward: Y-Forward
- Polygon Count: 15K-25K triangles

**File Structure:**
```
Collections:
├── AME_Avatar (main character)
├── AME_Rig (armature)
├── AME_Clothing (uniform/accessories)
└── AME_References (guides)
```

**Material Naming:**
- `AME_Skin_Face`
- `AME_Skin_Body`  
- `AME_Uniform_Fabric`
- `AME_Safety_Vest`
- `AME_Hair`
- `AME_Eyes`

---

### 🎯 **Use Case Context**

**Specific Procedure:** ATA 32-11-00 Nose Landing Gear Inspection  
**Duration:** 55 seconds of instruction  
**Language:** Spanish narration with emotional expression  
**Environment:** Aircraft hangar with professional lighting  
**Camera:** Multiple angles including close-ups  

---

### 📞 **Contact**

**Project Lead:** Amedeo Pelliccia  
**Email:** amedepelliccia@gaiaqao.org  
**Purpose:** Avatar subject & approval authority  

**Technical Team:** Q-AVIOGEN Development  
**Email:** development@gaiaqao.org  
**Purpose:** Integration & testing support  

---

*This checklist serves as a quick reference for the full specification document. Refer to AVATAR_SPECIFICATION.md for complete details.*
