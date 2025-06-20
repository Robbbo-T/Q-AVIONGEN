# Technical Integration Guide
## Q-AVIOGEN Avatar System - Amedeo Pelliccia

### 🔧 Technical Requirements for 3D Artists

This guide provides the technical specifications required for seamless integration of the Amedeo Pelliccia avatar into the Q-AVIOGEN rendering pipeline.

---

### 🎛️ Blender Configuration Requirements

#### Scene Setup:
```python
# Blender Scene Settings
Units: bpy.context.scene.unit_settings.system = 'METRIC'
Scale: bpy.context.scene.unit_settings.scale_length = 1.0
Up Axis: Z-Up (Blender default)
Forward Axis: Y-Forward (Blender default)
Frame Rate: 30fps (bpy.context.scene.render.fps = 30)
```

#### Object Naming Convention:
```
AME_Avatar_Body      # Main body mesh
AME_Avatar_Head      # Head mesh (can be joined)
AME_Avatar_Hair      # Hair mesh/particle system
AME_Avatar_Eyes      # Eye meshes
AME_Uniform_Base     # Main uniform mesh
AME_Uniform_Vest     # Safety vest mesh
AME_Accessories      # Tools, clipboard, etc.
AME_Armature         # Main rig
```

#### Collection Structure:
```
Scene Collection
├── AME_Character
│   ├── AME_Avatar_Body
│   ├── AME_Avatar_Head
│   ├── AME_Avatar_Hair
│   └── AME_Avatar_Eyes
├── AME_Clothing
│   ├── AME_Uniform_Base
│   ├── AME_Uniform_Vest
│   └── AME_Accessories
├── AME_Rig
│   └── AME_Armature
└── AME_References
    ├── Reference_Images
    └── Animation_Guides
```

---

### 🦴 Rigging Specifications

#### Bone Hierarchy (Essential):
```
AME_Root (at ground level, Z=0)
├── AME_Spine_Base
│   ├── AME_Spine_Mid
│   │   ├── AME_Spine_Top
│   │   │   ├── AME_Neck
│   │   │   │   └── AME_Head
│   │   │   ├── AME_Shoulder_L
│   │   │   │   ├── AME_Arm_Upper_L
│   │   │   │   │   ├── AME_Arm_Lower_L
│   │   │   │   │   │   └── AME_Hand_L
│   │   │   │   │   │       ├── AME_Finger_Index_L
│   │   │   │   │   │       ├── AME_Finger_Middle_L
│   │   │   │   │   │       ├── AME_Finger_Ring_L
│   │   │   │   │   │       ├── AME_Finger_Pinky_L
│   │   │   │   │   │       └── AME_Thumb_L
│   │   │   └── AME_Shoulder_R (mirror structure)
├── AME_Hip_L
│   ├── AME_Leg_Upper_L
│   │   ├── AME_Leg_Lower_L
│   │   │   └── AME_Foot_L
└── AME_Hip_R (mirror structure)
```

#### IK/FK Controls:
- **Arms:** IK and FK switching capability
- **Legs:** IK foot controls with FK override
- **Hands:** Finger curl controls and individual finger positioning
- **Head:** Look-at constraints for eye tracking

#### Custom Properties:
```python
# Add these custom properties to armature
avatar_height = 1.78  # meters
gesture_mode = "instruction"  # vs "casual"
uniform_type = "maintenance"
safety_vest = True
clipboard_visible = True
```

---

### 🎨 Material System Requirements

#### Shader Node Setup:
All materials must use Principled BSDF with the following inputs:

**Face Material (AME_Skin_Face):**
```
Principled BSDF:
├── Base Color: face_albedo.png (sRGB)
├── Normal: face_normal.png (Non-Color)
├── Roughness: face_roughness.png (Non-Color)
├── Metallic: 0.0
├── Specular: 0.5
└── Subsurface: 0.1 (for realistic skin)
```

**Uniform Material (AME_Uniform_Fabric):**
```
Principled BSDF:
├── Base Color: uniform_albedo.png (sRGB)
├── Normal: uniform_normal.png (Non-Color)
├── Roughness: uniform_roughness.png (Non-Color)
├── Metallic: 0.0
└── Specular: 0.3
```

**Safety Vest Material (AME_Safety_Vest):**
```
Principled BSDF:
├── Base Color: vest_albedo.png (sRGB)
├── Normal: vest_normal.png (Non-Color)
├── Roughness: 0.3 (slightly shiny)
├── Metallic: 0.0
├── Specular: 0.8
└── Emission: reflective_stripes.png (for safety strips)
```

#### Texture File Requirements:
```
Texture Format: PNG (with alpha) or JPG
Resolution: 2048x2048 minimum, 4096x4096 preferred
Color Space: sRGB for color maps, Non-Color for data maps
Bit Depth: 8-bit for color, 16-bit for data maps
Compression: High quality, no artifacts
```

---

### 🎬 Animation System Integration

#### Action Naming Convention:
```
AME_Gesture_01_PointDown
AME_Gesture_02_SweepingArm
AME_Gesture_03_CloseInspection
AME_Gesture_04_CrouchInspect
AME_Gesture_05_TraceParts
AME_Gesture_06_PointTech
AME_Gesture_07_ThumbsUp
AME_Idle_Neutral
AME_Walk_Cycle
AME_Talk_Neutral
```

#### Frame Range Setup:
```python
# Each gesture action should be:
Start Frame: 1
End Frame: Varies by gesture (typically 30-60 frames)
Frame Rate: 30fps
Interpolation: Bezier (smooth)
```

#### Bone Constraints Required:
```python
# Head bone - Look At constraint
target: AME_LookAt_Target
track_axis: '-Z'
up_axis: 'Y'

# Hand IK bones
ik_chain_length: 2 (upper arm to hand)
pole_target: AME_Elbow_Pole_L/R

# Foot IK bones
ik_chain_length: 2 (upper leg to foot)
pole_target: AME_Knee_Pole_L/R
```

---

### 📐 Scale and Proportions

#### Reference Measurements:
```
Total Height: 1.78m (5'10")
Head Height: ~0.23m (13% of total height)
Torso Height: ~0.71m (40% of total height)
Leg Length: ~0.89m (50% of total height)
Arm Span: ~1.78m (equal to height)
Shoulder Width: ~0.46m (26% of total height)
```

#### Clothing Fit:
- **Uniform:** Professional fit, not tight or loose
- **Safety Vest:** Worn over uniform, proper fit
- **Accessories:** Realistic proportions to body size

---

### 🔌 Export Compatibility

#### Blender File Structure:
```
File Size: < 50MB total
Texture Packing: All textures packed in .blend file
Relative Paths: All file paths relative to .blend location
Dependencies: No external dependencies
Compatibility: Blender 3.0+ LTS versions
```

#### Alternative Export Formats:
```python
# FBX Export Settings
Scale: 1.0
Forward: -Z Forward
Up: Y Up
Mesh: Smoothing = Face
Armature: Only Deform Bones = True
Animation: Bake Animation = True

# USD Export (future compatibility)
Materials: USD Preview Surface
Animation: Export as skeletal animation
Scale: Meters
```

---

### 🧪 Quality Assurance Checklist

#### Pre-Delivery Validation:
- [ ] All meshes manifold (no holes or non-manifold geometry)
- [ ] All normals facing outward
- [ ] UV maps within 0-1 space, no overlapping
- [ ] All materials using Principled BSDF
- [ ] Textures properly assigned and working
- [ ] Rig deformation smooth, no artifacts
- [ ] All 7 required gestures animate correctly
- [ ] File size under 50MB
- [ ] No missing textures or broken links
- [ ] Proper naming conventions followed

#### Performance Testing:
- [ ] Real-time viewport playback at 30fps
- [ ] Cycles rendering without errors
- [ ] Eevee rendering compatible
- [ ] LOD performance acceptable
- [ ] Memory usage reasonable (< 2GB)

---

### 🔄 Integration Workflow

#### Step 1: Import Testing
```python
# Q-AVIOGEN will test import with:
import bpy
bpy.ops.wm.open_mainfile(filepath="avatar_model.blend")
# Verify all collections and objects load correctly
```

#### Step 2: Animation Testing
```python
# Test each gesture action:
for action in bpy.data.actions:
    if action.name.startswith("AME_Gesture_"):
        # Test action playback and timing
        pass
```

#### Step 3: Rendering Pipeline
```python
# Integration with Q-AVIOGEN rendering:
scene_config = load_scene_config("instructor_config.yaml")
avatar = load_avatar("avatar_model.blend")
render_sequence(scene_config, avatar, duration=55.0)
```

---

### 📝 Delivery Package Structure

#### Required Files:
```
delivery_package/
├── avatar_model.blend                 # Main file
├── textures/
│   ├── face_albedo.png
│   ├── face_normal.png
│   ├── face_roughness.png
│   ├── uniform_albedo.png
│   ├── uniform_normal.png
│   ├── uniform_roughness.png
│   ├── vest_albedo.png
│   └── vest_emission.png
├── documentation/
│   ├── setup_guide.md
│   ├── animation_controls.md
│   └── troubleshooting.md
├── test_files/
│   ├── gesture_test.blend
│   └── material_test.blend
└── README.md
```

#### Documentation Requirements:
- **Setup Guide:** How to load and configure the avatar
- **Animation Controls:** Bone structure and animation workflow
- **Troubleshooting:** Common issues and solutions
- **Version Notes:** What's included and any limitations

---

### 🚀 Post-Delivery Support

#### Integration Phase:
- **Testing Period:** 1 week for integration testing
- **Feedback Loop:** Daily communication during integration
- **Bug Fixes:** Rapid response to technical issues
- **Optimization:** Performance tuning if needed

#### Final Validation:
- [ ] Avatar renders correctly in Q-AVIOGEN pipeline
- [ ] All 7 gestures sync with Spanish narration
- [ ] 55-second ATA 32-11-00 procedure renders successfully
- [ ] Professional quality suitable for aviation training
- [ ] Performance meets real-time requirements

---

*This technical guide ensures seamless integration of the Amedeo Pelliccia avatar into the Q-AVIOGEN system with professional quality and optimal performance.*
