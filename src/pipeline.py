"""
Main pipeline for creating animated comic-style GIFs from still images.
"""
from PIL import Image
from .comic_style import ComicStyleEffect
from .animation import AnimationFrameGenerator
from .gif_creator import GIFCreator
from .duckling_detector import DucklingDetector
from .realistic_animator import RealisticDucklingAnimator


class AnimationDuckPipeline:
    """Complete pipeline for generating animated comic-style duckling GIFs."""
    
    def __init__(self, 
                 edge_thickness=2,
                 color_levels=8,
                 num_frames=10,
                 animation_type='bounce',
                 duration=100,
                 loop=0,
                 realistic_mode=False):
        """
        Initialize the animation pipeline.
        
        Args:
            edge_thickness: Thickness of comic-style edges (default: 2)
            color_levels: Number of color levels for comic effect (default: 8)
            num_frames: Number of animation frames (default: 10)
            animation_type: Type of animation 
                Simple: 'bounce', 'rotate', 'scale', 'wobble'
                Realistic: 'walk', 'jump', 'fly', 'idle', 'blink'
            duration: Frame duration in milliseconds (default: 100)
            loop: Number of times to loop (0 = infinite)
            realistic_mode: Enable realistic duckling detection and animation (default: False)
        """
        self.comic_effect = ComicStyleEffect(edge_thickness, color_levels)
        self.frame_generator = AnimationFrameGenerator(num_frames, animation_type)
        self.gif_creator = GIFCreator(duration, loop)
        self.realistic_mode = realistic_mode
        
        if realistic_mode:
            self.detector = DucklingDetector()
            self.realistic_animator = RealisticDucklingAnimator(num_frames, animation_type)
    
    def process(self, input_path, output_path, apply_comic_style=True):
        """
        Process a still image and create an animated GIF.
        
        Args:
            input_path: Path to input image
            output_path: Path to save output GIF
            apply_comic_style: Whether to apply comic style effect (default: True)
            
        Returns:
            Path to the created GIF
        """
        print(f"Loading image from {input_path}...")
        image = Image.open(input_path)
        
        # Ensure RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply comic style effect if requested
        if apply_comic_style:
            print("Applying comic style effect...")
            image = self.comic_effect.apply(image)
        
        # Generate animation frames
        if self.realistic_mode:
            print(f"Detecting duckling and body parts...")
            parts = self.detector.detect_duckling(image)
            print(f"Generating {self.realistic_animator.num_frames} realistic animation frames ({self.realistic_animator.animation_type})...")
            frames = self.realistic_animator.animate(image, parts)
        else:
            print(f"Generating {self.frame_generator.num_frames} animation frames ({self.frame_generator.animation_type})...")
            frames = self.frame_generator.generate_frames(image)
        
        # Create GIF
        print(f"Creating animated GIF at {output_path}...")
        result = self.gif_creator.create_optimized_gif(frames, output_path)
        
        print(f"Success! Animated GIF saved to {result}")
        return result
    
    def process_batch(self, input_paths, output_dir, apply_comic_style=True):
        """
        Process multiple images in batch.
        
        Args:
            input_paths: List of input image paths
            output_dir: Directory to save output GIFs
            apply_comic_style: Whether to apply comic style effect (default: True)
            
        Returns:
            List of paths to created GIFs
        """
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        results = []
        for i, input_path in enumerate(input_paths, 1):
            print(f"\nProcessing image {i}/{len(input_paths)}: {input_path}")
            
            # Generate output filename
            basename = os.path.basename(input_path)
            name, _ = os.path.splitext(basename)
            output_path = os.path.join(output_dir, f"{name}_animated.gif")
            
            try:
                result = self.process(input_path, output_path, apply_comic_style)
                results.append(result)
            except Exception as e:
                print(f"Error processing {input_path}: {e}")
                continue
        
        return results
