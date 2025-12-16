"""
Main pipeline for creating animated comic-style GIFs from still images.
"""
from PIL import Image
from .comic_style import ComicStyleEffect
from .animation import AnimationFrameGenerator
from .gif_creator import GIFCreator
from .duckling_detector import DucklingDetector
from .realistic_animator import RealisticDucklingAnimator
from .handdrawn_animator import HandDrawnAnimator
from .animation_parser import AnimationParser
from .sequence_composer import SequenceComposer


class AnimationDuckPipeline:
    """Complete pipeline for generating animated comic-style duckling GIFs."""
    
    def __init__(self, 
                 edge_thickness=2,
                 color_levels=8,
                 num_frames=10,
                 animation_type='bounce',
                 duration=100,
                 loop=0,
                 realistic_mode=False,
                 hand_drawn_mode=False,
                 text_description=None):
        """
        Initialize the animation pipeline.
        
        Args:
            edge_thickness: Thickness of comic-style edges (default: 2)
            color_levels: Number of color levels for comic effect (default: 8)
            num_frames: Number of animation frames (default: 10)
            animation_type: Type of animation 
                Simple: 'bounce', 'rotate', 'scale', 'wobble'
                Realistic: 'walk', 'jump', 'fly', 'idle', 'blink'
                Hand-drawn: 'walk', 'jump', 'fly', 'idle', 'excited'
            duration: Frame duration in milliseconds (default: 100)
            loop: Number of times to loop (0 = infinite)
            realistic_mode: Enable realistic duckling detection and animation (default: False)
            hand_drawn_mode: Enable hand-drawn cartoon style animation (default: False)
            text_description: Natural language description for complex sequences (default: None)
        """
        self.comic_effect = ComicStyleEffect(edge_thickness, color_levels)
        self.realistic_mode = realistic_mode
        self.hand_drawn_mode = hand_drawn_mode
        self.text_description = text_description
        
        # Parse text description if provided
        if text_description:
            self.parser = AnimationParser()
            self.parsed_sequence = self.parser.parse(text_description)
            # Override num_frames and duration based on complexity
            num_frames = self.parser.get_suggested_frames(self.parsed_sequence)
            duration = self.parser.get_suggested_duration(self.parsed_sequence)
            # Force hand-drawn mode for text descriptions (best quality)
            self.hand_drawn_mode = True
        
        # Initialize frame generator and GIF creator with final values
        self.frame_generator = AnimationFrameGenerator(num_frames, animation_type)
        self.gif_creator = GIFCreator(duration, loop)
        
        if realistic_mode or self.hand_drawn_mode:
            self.detector = DucklingDetector()
            if self.hand_drawn_mode:
                self.hand_drawn_animator = HandDrawnAnimator(num_frames, animation_type)
            else:
                self.realistic_animator = RealisticDucklingAnimator(num_frames, animation_type)
        
        # Sequence composer for complex animations
        if text_description:
            self.composer = SequenceComposer(num_frames)
    
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
            if self.hand_drawn_mode:
                print("Applying hand-drawn comic style effect...")
                image = self.comic_effect.apply(image, hand_drawn_style=True)
            else:
                print("Applying comic style effect...")
                image = self.comic_effect.apply(image)
        
        # Generate animation frames
        if self.text_description:
            # Complex sequence from text description
            print(f"Parsing animation description: '{self.text_description}'")
            print(f"Detected {len(self.parsed_sequence['sequences'])} action sequences")
            print(f"Detecting duckling and body parts...")
            parts = self.detector.detect_duckling(image)
            print(f"Generating {self.composer.num_frames} frames from text description...")
            frames = self.composer.compose(image, parts, self.parsed_sequence, self.hand_drawn_animator)
        elif self.hand_drawn_mode:
            print(f"Detecting duckling and body parts...")
            parts = self.detector.detect_duckling(image)
            print(f"Generating {self.hand_drawn_animator.num_frames} hand-drawn animation frames ({self.hand_drawn_animator.animation_type})...")
            frames = self.hand_drawn_animator.animate(image, parts)
        elif self.realistic_mode:
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
