#!/usr/bin/env python3
"""
AnimationDuck - Main CLI application
Create animated comic-style GIFs from still images.
"""

import argparse
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import AnimationDuckPipeline


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Create animated comic-style GIFs from still images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Animation Types:
  Simple (whole image): bounce, rotate, scale, wobble
  Realistic (body parts): walk, jump, fly, idle, blink

Examples:
  # Basic bounce animation
  python animationduck.py input.jpg -o output.gif

  # Realistic walking duckling
  python animationduck.py duck.png -o duck.gif -r -a walk -f 15

  # Flying duckling with comic style
  python animationduck.py duck.jpg -o fly.gif -r -a fly

  # Without comic style effect
  python animationduck.py photo.jpg -o photo.gif --no-comic-style

  # Process multiple images
  python animationduck.py image1.jpg image2.png -o output_dir/
        """
    )
    
    parser.add_argument('input', nargs='+', help='Input image file(s)')
    parser.add_argument('-o', '--output', required=True, 
                        help='Output GIF file or directory for batch processing')
    parser.add_argument('-r', '--realistic', action='store_true',
                        help='Enable realistic mode (detect duckling parts and animate them)')
    parser.add_argument('-a', '--animation', 
                        choices=['bounce', 'rotate', 'scale', 'wobble', 
                                'walk', 'jump', 'fly', 'idle', 'blink'],
                        default='bounce',
                        help='Animation type (default: bounce)')
    parser.add_argument('-f', '--frames', type=int, default=10,
                        help='Number of frames (default: 10)')
    parser.add_argument('-d', '--duration', type=int, default=100,
                        help='Frame duration in milliseconds (default: 100)')
    parser.add_argument('-e', '--edge-thickness', type=int, default=2,
                        help='Comic edge thickness (default: 2)')
    parser.add_argument('-c', '--colors', type=int, default=8,
                        help='Number of color levels for comic effect (default: 8)')
    parser.add_argument('--no-comic-style', action='store_true',
                        help='Disable comic style effect')
    parser.add_argument('-l', '--loop', type=int, default=0,
                        help='Number of loops (0 = infinite, default: 0)')
    
    args = parser.parse_args()
    
    # Validate input files
    for input_file in args.input:
        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            sys.exit(1)
    
    # Check if realistic animations are used with realistic mode
    realistic_anims = ['walk', 'jump', 'fly', 'idle', 'blink']
    if args.animation in realistic_anims and not args.realistic:
        print(f"Note: Animation '{args.animation}' works best with realistic mode (-r flag)")
        print(f"Enabling realistic mode automatically...")
        args.realistic = True
    
    # Create pipeline
    pipeline = AnimationDuckPipeline(
        edge_thickness=args.edge_thickness,
        color_levels=args.colors,
        num_frames=args.frames,
        animation_type=args.animation,
        duration=args.duration,
        loop=args.loop,
        realistic_mode=args.realistic
    )
    
    # Process images
    try:
        if len(args.input) == 1:
            # Single image processing
            pipeline.process(
                args.input[0],
                args.output,
                apply_comic_style=not args.no_comic_style
            )
        else:
            # Batch processing
            if not os.path.isdir(args.output):
                os.makedirs(args.output, exist_ok=True)
            
            pipeline.process_batch(
                args.input,
                args.output,
                apply_comic_style=not args.no_comic_style
            )
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
