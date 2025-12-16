# Text-to-Animation Feature

## Overview

AnimationDuck now supports creating complex animations directly from natural language descriptions! Simply describe what you want your duckling to do, and the system will parse the description and generate a multi-action animated GIF.

## Quick Start

```bash
# Basic example
python animationduck.py duck.png -o output.gif --describe "duckling jumps excitedly"

# Complex sequence
python animationduck.py duck.png -o dice.gif --describe "duckling rolls dice and jumps cheering as result is 6"

# With objects
python animationduck.py duck.png -o stars.gif --describe "duckling walks with stars around it"
```

## How It Works

### 1. Natural Language Parsing

The system parses your description to extract:
- **Actions**: walk, jump, fly, idle, cheer, roll
- **Objects**: dice, stars, coins, hearts
- **Emotions**: happy, excited, sad, surprised
- **Conditions**: result numbers, success/failure states

### 2. Sequence Composition

Multiple actions are automatically combined into a single smooth animation:
- Each action gets allocated frames based on complexity
- Transitions are smooth and natural
- Objects are animated appropriately for each action

### 3. Object Integration

Objects are added to frames with appropriate animations:
- **Dice**: Rolls into scene with rotation, shows result
- **Stars**: Orbit around duckling with pulsing effect
- **Coins**: Spin in place with 3D rotation effect
- **Hearts**: Float upward from duckling

## Supported Actions

### Basic Movements
- `walk`, `walking`, `walks`, `stroll`, `waddle`
- `jump`, `jumping`, `jumps`, `hop`, `leap`, `bounce`
- `fly`, `flying`, `flies`, `soar`, `glide`
- `idle`, `stand`, `wait`, `rest`, `breath`

### Emotions & Reactions
- `cheer`, `celebrate`, `excited`, `happy`, `joy`, `victory`, `yay`

### Object Interactions
- `roll`, `rolling`, `rolls` (typically with dice)
- `spin`, `rotate` (with coins or dice)

## Supported Objects

### Props
- `dice`, `die`, `cube` - Animated rolling dice
- `star`, `sparkle`, `twinkle` - Orbiting sparkles
- `coin`, `money` - Spinning coin
- `heart`, `love` - Floating hearts

## Examples

### Simple Animations

```bash
# Single action
python animationduck.py duck.png -o jump.gif --describe "duckling jumps"

# With emotion
python animationduck.py duck.png -o happy.gif --describe "duckling celebrates happily"

# With object
python animationduck.py duck.png -o sparkle.gif --describe "duckling with stars"
```

### Complex Sequences

```bash
# Multiple actions
python animationduck.py duck.png -o sequence.gif --describe "duckling walks then jumps"

# Actions with objects
python animationduck.py duck.png -o coin.gif --describe "duckling jumps and catches coin"

# Conditional actions
python animationduck.py duck.png -o dice.gif --describe "duckling rolls dice and cheers as result is 6"
```

### Full Example: The Original Request

```bash
# "Let a duckling roll a dice and jump up cheering as it result is a 6"
python animationduck.py duck.png -o dice_celebration.gif \
  --describe "duckling rolls dice and jumps cheering as result is 6"
```

This creates a complex animation where:
1. A dice enters the scene and rolls
2. The duckling performs a rolling/idle animation
3. The dice shows the number 6
4. The duckling jumps up excitedly
5. The duckling continues cheering animation
6. All transitions are smooth and natural

## Technical Details

### Frame Allocation

The system automatically calculates optimal frame counts based on:
- Number of action sequences (more sequences = more frames)
- Complexity of each action (flying needs more frames than idle)
- Number of objects (objects increase frame count)
- Typical range: 15-40 frames total

### Duration Calculation

Frame duration is adjusted based on sequence complexity:
- Simple (1 action): 80ms per frame
- Medium (2-3 actions): 70ms per frame
- Complex (4+ actions): 60ms per frame

### Animation Quality

All text-to-animation uses hand-drawn mode automatically for best quality:
- Classical animation principles (squash & stretch, anticipation, etc.)
- Exaggerated cartoon movements
- Expressive eyes and features
- Bold comic-style outlines
- Vibrant colors

## Advanced Usage

### Custom Frame Counts

Override the automatic frame count:

```bash
python animationduck.py duck.png -o custom.gif \
  --describe "duckling walks and jumps" \
  -f 25
```

### Custom Duration

Adjust frame duration for speed control:

```bash
python animationduck.py duck.png -o fast.gif \
  --describe "duckling runs excitedly" \
  -d 50  # Faster animation
```

### Without Comic Style

Create animation without comic effects:

```bash
python animationduck.py duck.png -o natural.gif \
  --describe "duckling walks peacefully" \
  --no-comic-style
```

## Parsing Rules

### Action Extraction

The parser looks for action keywords in your description:
- Matches common verbs and variations
- Case-insensitive matching
- Handles multiple actions separated by "and", "then", commas

### Object Detection

Objects are detected by keywords:
- Supports singular and plural forms
- Multiple objects can be in one description
- Objects are animated throughout their associated action

### Condition Recognition

Special patterns are recognized:
- Numbers: "result is 6", "shows 5", "displays 3"
- Outcomes: "wins", "succeeds", "loses", "fails"
- Conditions affect visual elements (e.g., showing dice result)

## Python API

```python
from src import AnimationDuckPipeline

# Create pipeline with text description
pipeline = AnimationDuckPipeline(
    text_description="duckling rolls dice and jumps cheering as result is 6"
)

# Process image
pipeline.process('input.jpg', 'output.gif')
```

### Manual Sequence Control

```python
from src import AnimationParser, SequenceComposer, HandDrawnAnimator
from PIL import Image

# Parse description
parser = AnimationParser()
parsed = parser.parse("duckling jumps with stars")

# Get suggestions
num_frames = parser.get_suggested_frames(parsed)
duration = parser.get_suggested_duration(parsed)

print(f"Suggested: {num_frames} frames at {duration}ms each")
print(f"Sequences: {parsed['sequences']}")
```

## Limitations

### Current Version

- **Single Duckling**: Only one duckling per animation
- **2D Plane**: All movement is in 2D space
- **Pre-defined Objects**: Limited to built-in objects (dice, stars, coins, hearts)
- **Basic Physics**: Objects have simple animations, not realistic physics
- **English Only**: Parser currently works with English descriptions

### Known Behaviors

- Very long descriptions might be split unpredictably
- Complex grammar might not parse as expected
- Default to "excited" animation if description can't be parsed
- Objects appear in standard positions (may overlap with duckling)

## Tips for Best Results

### Writing Descriptions

1. **Be Clear**: Use specific action verbs
   - Good: "duckling jumps and celebrates"
   - Less clear: "duckling does something fun"

2. **Use Supported Keywords**: Refer to the supported actions/objects lists
   - Good: "duckling rolls dice"
   - Not supported: "duckling plays chess"

3. **Logical Sequence**: Actions should flow naturally
   - Good: "duckling walks then jumps"
   - Works but odd: "duckling flies then walks"

4. **Keep It Simple**: 2-4 actions work best
   - Good: "duckling walks, jumps, and celebrates"
   - Too complex: "duckling walks slowly, looks around, picks up dice, examines it, rolls it..."

### Performance

- More actions = longer processing time
- Objects add minimal overhead
- Typical processing: 5-15 seconds
- Complex sequences (4+ actions): 15-30 seconds

### Quality Settings

For best quality with text-to-animation:

```bash
python animationduck.py duck.png -o best.gif \
  --describe "your description here" \
  -f 30      # More frames for smoother animation
  -d 70      # 70ms for good speed
  -e 3       # Thicker comic edges
  -c 6       # Fewer colors for bolder look
```

## Future Enhancements

Potential improvements for future versions:

- **More Objects**: Additional props (ball, food, toys, etc.)
- **Backgrounds**: Contextual backgrounds (grass, water, sky)
- **Multiple Ducklings**: Support for multi-character scenes
- **Custom Objects**: User-provided object images
- **Voice/Sound**: Animation synchronized with audio cues
- **3D Hints**: Pseudo-3D positioning and depth
- **Facial Expressions**: More nuanced emotional states
- **Physics**: More realistic object physics
- **Multi-language**: Support for non-English descriptions

## Troubleshooting

### Animation Doesn't Match Description

**Problem**: Output doesn't do what you described

**Solutions**:
1. Check if keywords are in supported lists
2. Try simpler description with explicit keywords
3. Use `--describe "simpler version"` to test
4. Manually use `-a` flag with specific animation type

### Objects Don't Appear

**Problem**: Described objects aren't in the animation

**Solutions**:
1. Verify object keywords are exact matches (dice, star, coin, heart)
2. Check that object appears with an action
3. Try: `"duckling idle with stars"` to ensure object visibility

### Processing Is Slow

**Problem**: Takes too long to generate

**Solutions**:
1. Reduce frame count: `-f 15`
2. Simplify description (fewer actions)
3. Remove objects if not essential
4. Use simpler animation mode if needed

### GIF Is Too Large

**Problem**: Output file size is very big

**Solutions**:
1. Reduce frames: `-f 15`
2. Reduce colors: `-c 4`
3. Increase duration: `-d 100` (fewer fps)
4. Use simpler animation: `--realistic` instead of default hand-drawn

## Examples Gallery

### Celebration Sequence
```bash
python animationduck.py duck.png -o win.gif \
  --describe "duckling rolls dice and jumps cheering as result is 6"
```
Result: Dice rolls in → Shows 6 → Duckling jumps excitedly

### Magical Flight
```bash
python animationduck.py duck.png -o magic.gif \
  --describe "duckling flies with stars and hearts"
```
Result: Duckling flies with orbiting stars and floating hearts

### Victory Celebration
```bash
python animationduck.py duck.png -o victory.gif \
  --describe "duckling jumps excitedly with sparkles"
```
Result: Excited jumping with sparkling stars around

### Peaceful Walk
```bash
python animationduck.py duck.png -o peace.gif \
  --describe "duckling walks peacefully"
```
Result: Gentle walking animation with natural movement

## Feedback & Contributions

We'd love to hear about your creative uses of text-to-animation!

- Share your best animations
- Suggest new actions or objects
- Report parsing issues
- Contribute code improvements

See the main README.md for contribution guidelines.
