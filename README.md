# AnimationDuck 🦆

Create animated comic-style duckling GIFs from still images! This application transforms your still images into fun, animated GIFs with cartoon/comic-style effects. Designed to run on low-end hardware with CPU-only processing.

**Inspired by the playful, energetic style of DuckDice GIFs on Tenor!**

## Features

- **Comic Style Effects**: Apply cartoon/comic-style effects with edge detection and color posterization
- **Two Animation Modes**:
  - **Simple Mode**: Animate the entire image (bounce, rotate, scale, wobble)
  - **Realistic Mode**: Detect duckling parts and animate them individually for lifelike movements
- **Realistic Animations**: 
  - `walk` - Walking with leg movement and head bobbing
  - `jump` - Jumping with leg compression and wing flapping
  - `fly` - Flying with continuous wing flapping
  - `idle` - Breathing and occasional head movements
  - `blink` - Eye blinking animation
- **Duckling Detection**: Automatically detects ducklings and identifies body parts (head, eyes, body, legs, wings)
- **CPU-Friendly**: Optimized for low-end hardware, no GPU required
- **Frame-by-Frame Animation**: Generates smooth animations by creating individual frames
- **Batch Processing**: Process multiple images at once
- **Customizable**: Adjust frames, duration, colors, and edge thickness

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sushiomsky/animationduck.git
cd animationduck
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. Generate a sample duckling image:
```bash
python create_sample.py
```

2. Create your first animated GIF:
```bash
python animationduck.py examples/sample_duckling.png -o output.gif
```

3. Try realistic walking animation:
```bash
python animationduck.py examples/sample_duckling.png -o walk.gif -r -a walk
```

## Usage

### Basic Usage

```bash
# Simple bounce animation
python animationduck.py input.jpg -o output.gif

# Realistic walking animation
python animationduck.py duck.png -o duck.gif -r -a walk
```

### Realistic Animations (New!)

The realistic mode detects duckling parts and animates them individually:

```bash
# Walking duckling with leg movement
python animationduck.py duck.png -o walk.gif -r -a walk -f 15 -d 80

# Jumping duckling
python animationduck.py duck.png -o jump.gif -r -a jump -f 15 -d 70

# Flying duckling with wing flapping
python animationduck.py duck.png -o fly.gif -r -a fly -f 16 -d 60

# Idle duckling with breathing
python animationduck.py duck.png -o idle.gif -r -a idle -f 20 -d 100

# Blinking eyes
python animationduck.py duck.png -o blink.gif -r -a blink -f 10 -d 150
```

### Simple Animations

For whole-image animations without part detection:

```bash
# Wobble animation
python animationduck.py duck.png -o duck_wobble.gif -a wobble

# Rotate animation
python animationduck.py duck.png -o duck_rotate.gif -a rotate

# Scale (breathing) animation
python animationduck.py duck.png -o duck_scale.gif -a scale
```

### Custom Settings

```bash
# More frames and faster animation
python animationduck.py input.jpg -o output.gif -f 20 -d 50

# Thicker edges and fewer colors for stronger comic effect
python animationduck.py input.jpg -o output.gif -e 3 -c 6

# Without comic style (just animation)
python animationduck.py input.jpg -o output.gif --no-comic-style
```

### Batch Processing

```bash
# Process multiple images
python animationduck.py image1.jpg image2.png image3.jpg -o output_dir/
```

## Command-Line Options

```
positional arguments:
  input                 Input image file(s)

required arguments:
  -o, --output         Output GIF file or directory for batch processing

optional arguments:
  -h, --help           Show help message
  -r, --realistic      Enable realistic mode (detect duckling parts)
  -a, --animation      Animation type:
                       Simple: bounce, rotate, scale, wobble
                       Realistic: walk, jump, fly, idle, blink
                       (default: bounce)
  -f, --frames         Number of frames (default: 10)
  -d, --duration       Frame duration in milliseconds (default: 100)
  -e, --edge-thickness Comic edge thickness (default: 2)
  -c, --colors         Number of color levels for comic effect (default: 8)
  --no-comic-style     Disable comic style effect
  -l, --loop           Number of loops, 0 = infinite (default: 0)
```

## Python API

You can also use AnimationDuck as a Python library:

```python
from src import AnimationDuckPipeline

# Create pipeline with realistic mode
pipeline = AnimationDuckPipeline(
    edge_thickness=2,
    color_levels=8,
    num_frames=15,
    animation_type='walk',
    duration=80,
    loop=0,
    realistic_mode=True  # Enable duckling detection and part animation
)

# Process a single image
pipeline.process('input.jpg', 'output.gif')

# Process multiple images
pipeline.process_batch(
    ['image1.jpg', 'image2.png'],
    'output_dir/'
)
```

### Use Individual Modules

```python
from PIL import Image
from src.comic_style import ComicStyleEffect
from src.duckling_detector import DucklingDetector
from src.realistic_animator import RealisticDucklingAnimator
from src.gif_creator import GIFCreator

# Load image
image = Image.open('input.jpg')

# Apply comic style
comic = ComicStyleEffect(edge_thickness=2, color_levels=8)
styled_image = comic.apply(image)

# Detect duckling parts
detector = DucklingDetector()
parts = detector.detect_duckling(styled_image)

# Generate realistic animation frames
animator = RealisticDucklingAnimator(num_frames=15, animation_type='walk')
frames = animator.animate(styled_image, parts)

# Create GIF
gif = GIFCreator(duration=80, loop=0)
gif.create_gif(frames, 'output.gif')
```

## Requirements

- Python 3.7+
- Pillow (PIL) - Image processing
- NumPy - Numerical operations
- OpenCV (headless) - Computer vision operations

All dependencies are CPU-friendly and work on low-end hardware.

## How It Works

### Simple Mode
1. **Load Image**: Reads the input still image
2. **Comic Style Effect** (optional): Applies cartoon/comic styling
3. **Whole-Image Animation**: Transforms the entire image (bounce, rotate, etc.)
4. **GIF Creation**: Combines frames into an optimized animated GIF

### Realistic Mode (New!)
1. **Load Image**: Reads the input still image
2. **Comic Style Effect** (optional): Applies cartoon/comic styling
3. **Duckling Detection**: Uses computer vision to detect the duckling and identify:
   - Head position and size
   - Eye locations (with circular detection)
   - Beak area
   - Body region
   - Wing positions
   - Leg positions
4. **Part-Based Animation**: Animates individual body parts:
   - **Walk**: Alternating leg movement, head bobbing, occasional blinking
   - **Jump**: Leg compression/extension, wing flapping, parabolic trajectory
   - **Fly**: Continuous wing flapping, tucked legs, gentle hovering
   - **Idle**: Gentle breathing motion, occasional head turns
   - **Blink**: Eye closing and opening animation
5. **GIF Creation**: Combines frames into an optimized animated GIF

## DuckDice Style

This project is inspired by the playful, energetic animated GIFs from DuckDice on Tenor. Key style characteristics:
- **Bold, exaggerated movements** for comic effect
- **High-contrast colors** with clear outlines
- **Smooth, short loops** designed for quick visual impact
- **Expressive animations** that convey emotions and actions
- **Meme-friendly** and reaction-oriented content

## Examples

### Realistic Animations
```bash
# Walking duckling
python animationduck.py examples/sample_duckling.png -o walk.gif -r -a walk -f 12 -d 80

# Jumping duckling
python animationduck.py examples/sample_duckling.png -o jump.gif -r -a jump -f 15 -d 70

# Flying duckling
python animationduck.py examples/sample_duckling.png -o fly.gif -r -a fly -f 16 -d 60
```

### Simple Animations
```bash
# Bounce
python animationduck.py examples/sample_duckling.png -o bounce.gif -a bounce

# Wobble
python animationduck.py examples/sample_duckling.png -o wobble.gif -a wobble -f 15
```

## License

GNU General Public License v3.0 - see LICENSE file for details

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created for generating fun animated comic-style duckling GIFs locally on low-end hardware!
