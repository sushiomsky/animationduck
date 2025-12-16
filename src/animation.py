"""
Animation frame generator for creating movement in still images.
Generates frames with various animation effects.
"""
import numpy as np
from PIL import Image


class AnimationFrameGenerator:
    """Generate animation frames from a still image."""
    
    def __init__(self, num_frames=10, animation_type='bounce'):
        """
        Initialize frame generator.
        
        Args:
            num_frames: Number of frames to generate (default: 10)
            animation_type: Type of animation ('bounce', 'rotate', 'scale', 'wobble')
        """
        self.num_frames = num_frames
        self.animation_type = animation_type
    
    def generate_frames(self, image):
        """
        Generate animation frames from a still image.
        
        Args:
            image: PIL Image
            
        Returns:
            List of PIL Images (frames)
        """
        if self.animation_type == 'bounce':
            return self._generate_bounce_frames(image)
        elif self.animation_type == 'rotate':
            return self._generate_rotate_frames(image)
        elif self.animation_type == 'scale':
            return self._generate_scale_frames(image)
        elif self.animation_type == 'wobble':
            return self._generate_wobble_frames(image)
        else:
            return self._generate_bounce_frames(image)
    
    def _generate_bounce_frames(self, image):
        """Generate frames with a bouncing effect."""
        frames = []
        width, height = image.size
        
        # Create a canvas slightly taller to accommodate bounce
        canvas_height = int(height * 1.2)
        
        for i in range(self.num_frames):
            # Calculate bounce offset using sine wave
            t = i / self.num_frames
            offset = int(abs(np.sin(t * np.pi * 2) * height * 0.1))
            
            # Create canvas with background
            canvas = Image.new('RGB', (width, canvas_height), color=(255, 255, 255))
            
            # Paste image at bouncing position
            y_position = canvas_height - height - offset
            canvas.paste(image, (0, y_position))
            
            # Crop to original size
            canvas = canvas.crop((0, canvas_height - height, width, canvas_height))
            frames.append(canvas)
        
        return frames
    
    def _generate_rotate_frames(self, image):
        """Generate frames with rotation effect."""
        frames = []
        
        for i in range(self.num_frames):
            # Calculate rotation angle
            angle = (i / self.num_frames) * 360
            
            # Rotate image
            rotated = image.rotate(angle, resample=Image.BICUBIC, expand=False)
            frames.append(rotated)
        
        return frames
    
    def _generate_scale_frames(self, image):
        """Generate frames with scaling (breathing) effect."""
        frames = []
        width, height = image.size
        
        for i in range(self.num_frames):
            # Calculate scale factor using sine wave
            t = i / self.num_frames
            scale = 1.0 + 0.1 * np.sin(t * np.pi * 2)
            
            # Calculate new size
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize image
            scaled = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Create canvas and center the scaled image
            canvas = Image.new('RGB', (width, height), color=(255, 255, 255))
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            
            # Handle both shrinking and growing
            if scale < 1.0:
                canvas.paste(scaled, (x_offset, y_offset))
            else:
                # Crop the scaled image to fit
                crop_x = (new_width - width) // 2
                crop_y = (new_height - height) // 2
                scaled = scaled.crop((crop_x, crop_y, crop_x + width, crop_y + height))
                canvas = scaled
            
            frames.append(canvas)
        
        return frames
    
    def _generate_wobble_frames(self, image):
        """Generate frames with wobbling effect."""
        frames = []
        width, height = image.size
        
        for i in range(self.num_frames):
            # Calculate wobble parameters
            t = i / self.num_frames
            rotation = np.sin(t * np.pi * 4) * 5  # Small rotation
            
            # Create a slightly larger canvas to avoid clipping
            canvas_size = int(max(width, height) * 1.2)
            canvas = Image.new('RGB', (canvas_size, canvas_size), color=(255, 255, 255))
            
            # Rotate image
            rotated = image.rotate(rotation, resample=Image.BICUBIC, expand=True)
            
            # Center on canvas
            x_offset = (canvas_size - rotated.width) // 2
            y_offset = (canvas_size - rotated.height) // 2
            canvas.paste(rotated, (x_offset, y_offset))
            
            # Crop to original size
            crop_x = (canvas_size - width) // 2
            crop_y = (canvas_size - height) // 2
            canvas = canvas.crop((crop_x, crop_y, crop_x + width, crop_y + height))
            
            frames.append(canvas)
        
        return frames
