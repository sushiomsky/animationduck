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
  Hand-drawn (classical cartoon): walk, jump, fly, idle, excited

Text-to-Animation:
  Use --describe to create complex animations from natural language descriptions.
  Examples:
    "duckling rolls a dice and jumps up cheering"
    "duckling walks then jumps excitedly"
    "duckling flies with stars around it"

Examples:
  # Basic bounce animation
  python animationduck.py input.jpg -o output.gif

  # Create animation from description
  python animationduck.py duck.png -o result.gif --describe "duckling rolls dice and jumps cheering as result is 6"

  # Hand-drawn walking duckling (classical cartoon style)
  python animationduck.py duck.png -o duck.gif --hand-drawn -a walk -f 15

  # Excited duckling animation
  python animationduck.py duck.jpg -o excited.gif --hand-drawn -a excited

  # Realistic walking duckling
  python animationduck.py duck.png -o duck.gif -r -a walk -f 15

  # Without comic style effect
  python animationduck.py photo.jpg -o photo.gif --no-comic-style

  # Process multiple images
  python animationduck.py image1.jpg image2.png -o output_dir/
        """
    )
    
    parser.add_argument('input', nargs='+', help='Input image file(s)')
    parser.add_argument('-o', '--output', required=True, 
                        help='Output GIF file or directory for batch processing')
    parser.add_argument('--describe', type=str,
                        help='Create animation from text description (e.g., "duckling rolls dice and jumps cheering")')
    parser.add_argument('-r', '--realistic', action='store_true',
                        help='Enable realistic mode (detect duckling parts and animate them)')
    parser.add_argument('--hand-drawn', action='store_true',
                        help='Enable hand-drawn cartoon mode (classical animation principles)')
    parser.add_argument('-a', '--animation', 
                        choices=['bounce', 'rotate', 'scale', 'wobble', 
                                'walk', 'jump', 'fly', 'idle', 'blink', 'excited'],
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
    
    # Check if text description is provided
    if args.describe:
        print(f"Creating animation from description: {args.describe}")
        # Text descriptions automatically use hand-drawn mode
        args.hand_drawn = True
        args.realistic = False
    
    # Check if realistic or hand-drawn animations are used
    realistic_anims = ['walk', 'jump', 'fly', 'idle', 'blink', 'excited']
    if args.animation in realistic_anims and not (args.realistic or args.hand_drawn):
        print(f"Note: Animation '{args.animation}' works best with realistic or hand-drawn mode")
        if args.animation == 'excited':
            print(f"Enabling hand-drawn mode automatically for 'excited' animation...")
            args.hand_drawn = True
        else:
            print(f"Enabling realistic mode automatically...")
            args.realistic = True
    
    # Hand-drawn mode overrides realistic mode
    if args.hand_drawn and args.realistic:
        print("Note: Hand-drawn mode enabled, realistic mode will be ignored")
        args.realistic = False
    
    # Create pipeline
    pipeline = AnimationDuckPipeline(
        edge_thickness=args.edge_thickness,
        color_levels=args.colors,
        num_frames=args.frames,
        animation_type=args.animation,
        duration=args.duration,
        loop=args.loop,
        realistic_mode=args.realistic,
        hand_drawn_mode=args.hand_drawn,
        text_description=args.describe
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
