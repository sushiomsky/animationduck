"""
GIF creation module for combining frames into animated GIFs.
"""
from PIL import Image


class GIFCreator:
    """Create animated GIFs from a sequence of frames."""
    
    def __init__(self, duration=100, loop=0):
        """
        Initialize GIF creator.
        
        Args:
            duration: Duration of each frame in milliseconds (default: 100)
            loop: Number of times to loop (0 = infinite, default: 0)
        """
        self.duration = duration
        self.loop = loop
    
    def create_gif(self, frames, output_path):
        """
        Create an animated GIF from a list of frames.
        
        Args:
            frames: List of PIL Images
            output_path: Path to save the GIF
            
        Returns:
            Path to the created GIF
        """
        if not frames:
            raise ValueError("No frames provided")
        
        # Ensure all frames are in RGB mode
        frames = [frame.convert('RGB') for frame in frames]
        
        # Save as animated GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=self.duration,
            loop=self.loop,
            optimize=True
        )
        
        return output_path
    
    def create_optimized_gif(self, frames, output_path, colors=128):
        """
        Create an optimized animated GIF with reduced colors.
        
        Args:
            frames: List of PIL Images
            output_path: Path to save the GIF
            colors: Number of colors to use (default: 128)
            
        Returns:
            Path to the created GIF
        """
        if not frames:
            raise ValueError("No frames provided")
        
        # Convert frames to palette mode for optimization
        optimized_frames = []
        for frame in frames:
            # Convert to RGB first
            rgb_frame = frame.convert('RGB')
            # Convert to palette mode with specified number of colors
            # Using MEDIANCUT method (2) for better color quantization
            palette_frame = rgb_frame.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
            optimized_frames.append(palette_frame)
        
        # Save as animated GIF
        optimized_frames[0].save(
            output_path,
            save_all=True,
            append_images=optimized_frames[1:],
            duration=self.duration,
            loop=self.loop,
            optimize=True
        )
        
        return output_path
