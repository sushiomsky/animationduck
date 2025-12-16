# AnimationDuck 🦆

Create animated comic-style duckling GIFs from still images! This application transforms your still images into fun, animated GIFs with cartoon/comic-style effects. Designed to run on low-end hardware with CPU-only processing.

## Features

- **Comic Style Effects**: Apply cartoon/comic-style effects with edge detection and color posterization
- **Multiple Animation Types**: 
  - `bounce` - Bouncing up and down effect
  - `wobble` - Gentle wobbling/wiggling motion
  - `rotate` - Full 360° rotation
  - `scale` - Breathing/pulsing effect
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

## Usage

### Basic Usage

```bash
python animationduck.py input.jpg -o output.gif
```

### With Animation Type

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
  -a, --animation      Animation type: bounce, rotate, scale, wobble (default: bounce)
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

# Create pipeline
pipeline = AnimationDuckPipeline(
    edge_thickness=2,
    color_levels=8,
    num_frames=10,
    animation_type='wobble',
    duration=100,
    loop=0
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
from src.animation import AnimationFrameGenerator
from src.gif_creator import GIFCreator

# Load image
image = Image.open('input.jpg')

# Apply comic style
comic = ComicStyleEffect(edge_thickness=2, color_levels=8)
styled_image = comic.apply(image)

# Generate animation frames
animator = AnimationFrameGenerator(num_frames=10, animation_type='bounce')
frames = animator.generate_frames(styled_image)

# Create GIF
gif = GIFCreator(duration=100, loop=0)
gif.create_gif(frames, 'output.gif')
```

## Requirements

- Python 3.7+
- Pillow (PIL) - Image processing
- NumPy - Numerical operations
- OpenCV (headless) - Computer vision operations

All dependencies are CPU-friendly and work on low-end hardware.

## How It Works

1. **Load Image**: Reads the input still image
2. **Comic Style Effect** (optional):
   - Applies bilateral filter for smooth cartoon look
   - Posterizes colors to reduce color palette
   - Detects edges using adaptive thresholding
   - Combines edges with posterized image for comic effect
3. **Frame Generation**: Creates multiple frames with movement:
   - Bounce: Vertical oscillation using sine wave
   - Wobble: Gentle rotation oscillation
   - Rotate: Full 360° rotation
   - Scale: Size oscillation (breathing effect)
4. **GIF Creation**: Combines frames into an optimized animated GIF

## Examples

### Bounce Animation
```bash
python animationduck.py examples/sample_duckling.png -o bounce.gif -a bounce
```

### Wobble Animation
```bash
python animationduck.py examples/sample_duckling.png -o wobble.gif -a wobble -f 15
```

## License

GNU General Public License v3.0 - see LICENSE file for details

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created for generating fun animated comic-style duckling GIFs locally on low-end hardware!
