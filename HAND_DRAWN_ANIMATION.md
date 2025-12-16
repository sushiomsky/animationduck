# Classical Hand-Drawn Animation Features

## Overview
AnimationDuck now implements professional classical animation principles to create cartoon-quality GIFs comparable to hand-drawn comic strips and professional animated GIFs like those on DuckDice/Tenor.

## Classical Animation Principles Implemented

### 1. Squash & Stretch
The most important principle - objects deform to show flexibility and mass.
- Body stretches when moving up (jumping, bouncing up)
- Body squashes when landing or moving down
- Preserves volume (squash_x = 1/squash_y)
- Creates sense of weight and flexibility

**Implementation**: Dynamic scaling based on velocity and position in motion cycle.

### 2. Anticipation
Character prepares before major action.
- Squat down before jumping
- Pull back before moving forward
- Builds energy for the main action

**Implementation**: Jump animation has 20% anticipation phase where duckling squats down.

### 3. Follow-Through & Overlapping Action
Body parts continue moving after main action stops.
- Head lags behind body when walking
- Limbs swing past rest position
- Creates more realistic, fluid motion

**Implementation**: Head bobbing with phase delay (-0.3) relative to body movement.

### 4. Exaggeration
Amplify movements for comic effect.
- Leg angles: ±35° (vs ±20° in realistic mode)
- Wing flapping: ±55° (vs ±30°)
- Eye size: 1.6x normal for excited expressions
- Bounce height: 20 pixels (vs 5 pixels)

**Implementation**: All movement amplitudes increased 1.5-2x.

### 5. Timing & Ease In/Out
Control speed of action with acceleration curves.
- Ease in: start slow, speed up
- Ease out: slow down at end
- Makes motion feel more natural

**Implementation**: `_ease_in_out()` function using cubic curves (3t² - 2t³).

### 6. Rubber-Hose Limbs
Flexible, bendy limbs like 1930s cartoons.
- Legs bend with quadratic bezier curves
- Variable thickness based on squash
- Cartoon feet with exaggerated shapes

**Implementation**: `_draw_rubber_hose_legs()` with curved segments.

### 7. Motion Blur/Smear Frames
Fast movements show as blurs.
- Applied when velocity > 0.7
- Creates sense of speed
- Common in classic cartoons

**Implementation**: `_add_motion_smear()` applies box blur based on velocity.

### 8. Expressive Eyes
Large, emotive cartoon eyes.
- 1.3x normal size for standard
- 1.6x for excited/surprised
- Pupils follow movement direction
- Multiple highlights for sparkle
- Curved closed eyes for blinking

**Implementation**: `_draw_expressive_eyes()`, `_draw_excited_eyes()`.

### 9. Frame-by-Frame Variations
Subtle imperfections simulate hand-drawn animation.
- Random pixel offsets (±0.5 pixels)
- Paper texture with noise
- Edge variations
- No two frames identical

**Implementation**: `_add_hand_drawn_variation()`, `_create_canvas_with_noise()`.

### 10. Bold Outlines
Strong, clear lines like comic strips.
- Dual edge detection (adaptive + Canny)
- Thicker edges (edge_thickness + 1)
- Edge variation for imperfection
- Much darker (0.15x) for contrast

**Implementation**: Enhanced `_apply_hand_drawn_style()` in comic_style.py.

### 11. Vibrant Colors
Flat, saturated colors like classic cartoons.
- Saturation increased 1.3x
- Stronger posterization (fewer colors)
- High contrast
- Double bilateral filtering

**Implementation**: HSV saturation boost in `_apply_hand_drawn_style()`.

### 12. Animation Arcs
Natural curved paths for movements.
- Parabolic jump trajectory
- Sine wave hovering
- Circular wing flapping
- Bezier curves for limbs

**Implementation**: Trigonometric functions and bezier calculations.

## Animation Types

### Walk
- Exaggerated vertical bobbing (±12 pixels)
- Rubber-hose leg alternation (±35°)
- Head follow-through with delay
- Occasional blinking
- Squash & stretch based on velocity

### Jump
- **Anticipation** (0-20%): Squat down, squash body
- **Jump** (20-60%): Parabolic arc, stretch body, wings flap
- **Overshoot** (60-80%): Land too hard, squash
- **Settle** (80-100%): Return to normal
- Eyes wider during flight

### Fly
- Rapid wing flapping (±55°)
- Gentle hovering motion
- Body tilt in flight direction
- Legs tucked up
- Motion blur on wing beats

### Idle
- Gentle breathing cycle
- Occasional head turns (30-70%)
- Micro-movements for life
- Random blinking (at 40% and 80%)
- Minimal but constant motion

### Excited (NEW!)
- Rapid bouncing (6 cycles)
- Extreme squash & stretch
- Fast wing flapping (8 cycles)
- Body rotation (±10°)
- Excited eyes with sparkles
- Perfect for celebrations/wins

## Technical Details

### Frame Counts
- **Recommended**: 16-20 frames for smooth motion
- **Minimum**: 12 frames for basic loops
- **Maximum**: 30+ frames for complex sequences

### Frame Duration
- **Walk**: 70ms (smooth walking pace)
- **Jump**: 60ms (quick, energetic)
- **Fly**: 60ms (rapid wing movement)
- **Idle**: 100ms (calm, relaxed)
- **Excited**: 50ms (fast, frenetic)

### Performance
- CPU-only processing maintained
- No ML models or GPU required
- Traditional CV techniques only
- Runs on low-end hardware
- ~3-8 seconds per animation

## Comparison: Modes

| Feature | Simple | Realistic | Hand-Drawn |
|---------|--------|-----------|------------|
| Part Detection | ❌ | ✅ | ✅ |
| Squash & Stretch | ❌ | ❌ | ✅ |
| Anticipation | ❌ | ❌ | ✅ |
| Rubber-Hose | ❌ | ❌ | ✅ |
| Motion Blur | ❌ | ❌ | ✅ |
| Exaggeration | Basic | Moderate | Extreme |
| Edge Quality | Good | Good | Excellent |
| Frame Variation | None | None | Yes |
| Best For | Quick | Natural | Cartoon |
| Quality | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Quality Comparison

### Before (Realistic Mode)
- Natural movements
- Moderate exaggeration
- Simple leg angles (±20°)
- Basic eye drawing
- Standard edge detection
- Good for realistic ducks

### After (Hand-Drawn Mode)
- Classical cartoon principles
- Extreme exaggeration
- Rubber-hose legs (±35°)
- Expressive cartoon eyes
- Bold comic outlines
- Professional cartoon quality
- Matches DuckDice standard

## Examples

### Command-Line
```bash
# Best quality - hand-drawn walk
python animationduck.py duck.png -o walk.gif --hand-drawn -a walk -f 16 -d 70

# Celebration/win animation
python animationduck.py duck.png -o win.gif --hand-drawn -a excited -f 20 -d 50

# Energetic jump
python animationduck.py duck.png -o jump.gif --hand-drawn -a jump -f 18 -d 60

# Flying with wing flapping
python animationduck.py duck.png -o fly.gif --hand-drawn -a fly -f 16 -d 60
```

### Python API
```python
from src import AnimationDuckPipeline

# Hand-drawn mode
pipeline = AnimationDuckPipeline(
    num_frames=16,
    animation_type='walk',
    duration=70,
    hand_drawn_mode=True,
    edge_thickness=3,
    color_levels=6
)

pipeline.process('duck.png', 'cartoon.gif')
```

## File Sizes

Typical file sizes for 16-frame hand-drawn animations:
- Walk: ~390KB
- Jump: ~480KB
- Fly: ~190KB
- Idle: ~150KB
- Excited: ~510KB

Optimized with color quantization (128 colors).

## References

Classical animation principles from:
- Disney's "The Illusion of Life" (1981)
- Richard Williams' "The Animator's Survival Kit"
- 1930s rubber-hose cartoons (Fleischer Studios)
- Modern hand-drawn GIFs on Tenor/GIPHY
- DuckDice casino animated mascot GIFs

## Future Enhancements

Potential improvements maintaining CPU-only:
- Multiple ducklings interaction
- Scene backgrounds
- Props and effects (dust clouds, speed lines)
- More animation types (swim, waddle, dance)
- Customizable color palettes
- Animation composition
