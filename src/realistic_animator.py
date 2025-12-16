"""
Realistic duckling animation module.
Animates individual body parts for lifelike movements.
"""
import numpy as np
from PIL import Image, ImageDraw
import cv2


class RealisticDucklingAnimator:
    """Create realistic duckling animations by animating individual body parts."""
    
    def __init__(self, num_frames=15, animation_type='walk'):
        """
        Initialize realistic animator.
        
        Args:
            num_frames: Number of frames to generate
            animation_type: Type of animation ('walk', 'jump', 'fly', 'idle', 'blink')
        """
        self.num_frames = num_frames
        self.animation_type = animation_type
    
    def animate(self, image, parts):
        """
        Create realistic animation frames based on detected body parts.
        
        Args:
            image: PIL Image
            parts: Dictionary of body parts from DucklingDetector
            
        Returns:
            List of PIL Images (frames)
        """
        if self.animation_type == 'walk':
            return self._animate_walk(image, parts)
        elif self.animation_type == 'jump':
            return self._animate_jump(image, parts)
        elif self.animation_type == 'fly':
            return self._animate_fly(image, parts)
        elif self.animation_type == 'idle':
            return self._animate_idle(image, parts)
        elif self.animation_type == 'blink':
            return self._animate_blink(image, parts)
        else:
            return self._animate_walk(image, parts)
    
    def _animate_walk(self, image, parts):
        """Create walking animation."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            frame = img_array.copy()
            
            # Walking bobbing motion
            bob_offset = int(np.sin(t * np.pi * 4) * 5)
            
            # Leg movement (alternating)
            left_leg_angle = np.sin(t * np.pi * 4) * 20
            right_leg_angle = np.sin(t * np.pi * 4 + np.pi) * 20
            
            # Head bobbing with walking
            head_bob = int(np.sin(t * np.pi * 4) * 3)
            
            # Create canvas
            canvas = Image.new('RGB', (width, height), color=(255, 255, 255))
            canvas_array = np.array(canvas)
            
            # Apply transformations
            canvas_array = self._apply_body_transform(
                frame, canvas_array, parts, 
                y_offset=bob_offset, 
                head_y_offset=head_bob
            )
            
            # Draw animated legs
            canvas_array = self._draw_animated_legs(
                canvas_array, parts, 
                left_angle=left_leg_angle,
                right_angle=right_leg_angle,
                y_offset=bob_offset
            )
            
            # Add eye blinking occasionally
            if i % (self.num_frames // 2) == 0:
                canvas_array = self._draw_closed_eyes(canvas_array, parts, head_bob)
            else:
                canvas_array = self._draw_eyes(canvas_array, parts, head_bob)
            
            frames.append(Image.fromarray(canvas_array))
        
        return frames
    
    def _animate_jump(self, image, parts):
        """Create jumping animation."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Jump trajectory (parabolic)
            jump_height = -abs(np.sin(t * np.pi)) * height * 0.15
            
            # Legs compress and extend
            leg_compression = np.sin(t * np.pi) * 0.5
            
            # Wings flap during jump
            wing_angle = np.sin(t * np.pi * 2) * 15
            
            canvas = Image.new('RGB', (width, height), color=(255, 255, 255))
            canvas_array = np.array(canvas)
            
            # Apply transformations
            canvas_array = self._apply_body_transform(
                img_array, canvas_array, parts,
                y_offset=int(jump_height)
            )
            
            # Draw compressed/extended legs
            canvas_array = self._draw_animated_legs(
                canvas_array, parts,
                left_angle=leg_compression * 20,
                right_angle=leg_compression * 20,
                y_offset=int(jump_height)
            )
            
            # Draw flapping wings
            canvas_array = self._draw_wings(
                canvas_array, parts,
                left_angle=-wing_angle,
                right_angle=wing_angle,
                y_offset=int(jump_height)
            )
            
            canvas_array = self._draw_eyes(canvas_array, parts, int(jump_height))
            
            frames.append(Image.fromarray(canvas_array))
        
        return frames
    
    def _animate_fly(self, image, parts):
        """Create flying animation."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Gentle up and down motion
            fly_offset = int(np.sin(t * np.pi * 2) * 8)
            
            # Wing flapping
            wing_flap = np.sin(t * np.pi * 4) * 30
            
            # Legs tucked up
            leg_tuck = -10
            
            canvas = Image.new('RGB', (width, height), color=(255, 255, 255))
            canvas_array = np.array(canvas)
            
            # Apply transformations
            canvas_array = self._apply_body_transform(
                img_array, canvas_array, parts,
                y_offset=fly_offset
            )
            
            # Draw flapping wings
            canvas_array = self._draw_wings(
                canvas_array, parts,
                left_angle=-wing_flap,
                right_angle=wing_flap,
                y_offset=fly_offset
            )
            
            # Draw tucked legs
            canvas_array = self._draw_animated_legs(
                canvas_array, parts,
                left_angle=45,
                right_angle=45,
                y_offset=fly_offset + leg_tuck
            )
            
            canvas_array = self._draw_eyes(canvas_array, parts, fly_offset)
            
            frames.append(Image.fromarray(canvas_array))
        
        return frames
    
    def _animate_idle(self, image, parts):
        """Create idle animation with breathing and occasional head movement."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Gentle breathing
            breath = np.sin(t * np.pi * 2) * 2
            
            # Occasional head turn
            head_turn = 0
            if 0.3 < t < 0.7:
                head_turn = int(np.sin((t - 0.3) * np.pi * 2.5) * 5)
            
            canvas = Image.new('RGB', (width, height), color=(255, 255, 255))
            canvas_array = np.array(canvas)
            
            # Apply transformations
            canvas_array = self._apply_body_transform(
                img_array, canvas_array, parts,
                y_offset=int(breath),
                head_x_offset=head_turn
            )
            
            canvas_array = self._draw_eyes(canvas_array, parts, int(breath), head_turn)
            
            frames.append(Image.fromarray(canvas_array))
        
        return frames
    
    def _animate_blink(self, image, parts):
        """Create blinking animation."""
        frames = []
        img_array = np.array(image)
        
        for i in range(self.num_frames):
            canvas_array = img_array.copy()
            
            # Blink in the middle frames
            if self.num_frames // 3 < i < 2 * self.num_frames // 3:
                canvas_array = self._draw_closed_eyes(canvas_array, parts)
            else:
                canvas_array = self._draw_eyes(canvas_array, parts)
            
            frames.append(Image.fromarray(canvas_array))
        
        return frames
    
    def _apply_body_transform(self, source, canvas, parts, y_offset=0, 
                             head_y_offset=0, head_x_offset=0):
        """Apply transformation to the body."""
        # Simply shift the entire image for now
        # In a more advanced version, we would transform individual parts
        h, w = source.shape[:2]
        
        # Create transform matrix for translation
        if y_offset != 0:
            M = np.float32([[1, 0, 0], [0, 1, y_offset]])
            canvas = cv2.warpAffine(source, M, (w, h), 
                                   borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(255, 255, 255))
        else:
            canvas = source.copy()
        
        return canvas
    
    def _draw_animated_legs(self, canvas, parts, left_angle=0, right_angle=0, y_offset=0):
        """Draw animated legs."""
        if 'legs' not in parts or not parts['legs']:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for idx, leg in enumerate(parts['legs']):
            x, y, w, h = leg
            y += y_offset
            
            # Determine angle for this leg
            angle = left_angle if idx == 0 else right_angle
            
            # Draw leg as a line with angle
            leg_top_x = x + w // 2
            leg_top_y = y
            leg_bottom_x = leg_top_x + int(np.sin(np.radians(angle)) * h)
            leg_bottom_y = leg_top_y + int(np.cos(np.radians(angle)) * h)
            
            # Draw leg
            draw.line([(leg_top_x, leg_top_y), (leg_bottom_x, leg_bottom_y)],
                     fill='orange', width=max(2, w // 3))
            
            # Draw foot
            foot_points = [
                (leg_bottom_x - w // 2, leg_bottom_y),
                (leg_bottom_x, leg_bottom_y + h // 4),
                (leg_bottom_x + w // 2, leg_bottom_y)
            ]
            draw.polygon(foot_points, fill='orange', outline='darkorange')
        
        return np.array(pil_img)
    
    def _draw_wings(self, canvas, parts, left_angle=0, right_angle=0, y_offset=0):
        """Draw animated wings."""
        if 'left_wing' not in parts or 'right_wing' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        # Draw left wing
        x, y, w, h = parts['left_wing']
        y += y_offset
        center_x, center_y = x + w, y + h // 2
        
        # Calculate wing tip position based on angle
        wing_length = w
        tip_x = center_x + int(np.cos(np.radians(left_angle)) * wing_length)
        tip_y = center_y - int(np.sin(np.radians(left_angle)) * wing_length)
        
        # Draw wing as a filled polygon
        wing_points = [
            (center_x, center_y - h // 2),
            (tip_x, tip_y),
            (center_x, center_y + h // 2)
        ]
        draw.polygon(wing_points, fill='gold', outline='orange')
        
        # Draw right wing
        x, y, w, h = parts['right_wing']
        y += y_offset
        center_x, center_y = x, y + h // 2
        
        tip_x = center_x + int(np.cos(np.radians(180 - right_angle)) * wing_length)
        tip_y = center_y - int(np.sin(np.radians(180 - right_angle)) * wing_length)
        
        wing_points = [
            (center_x, center_y - h // 2),
            (tip_x, tip_y),
            (center_x, center_y + h // 2)
        ]
        draw.polygon(wing_points, fill='gold', outline='orange')
        
        return np.array(pil_img)
    
    def _draw_eyes(self, canvas, parts, y_offset=0, x_offset=0):
        """Draw open eyes."""
        if 'left_eye' not in parts or 'right_eye' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for eye_key in ['left_eye', 'right_eye']:
            if eye_key in parts:
                x, y, r = parts[eye_key]
                x += x_offset
                y += y_offset
                
                # Draw eye white
                draw.ellipse([x - r, y - r, x + r, y + r], fill='white', outline='black')
                
                # Draw pupil
                pupil_r = r // 2
                draw.ellipse([x - pupil_r, y - pupil_r, x + pupil_r, y + pupil_r], 
                           fill='black')
                
                # Draw highlight
                highlight_r = r // 3
                draw.ellipse([x - highlight_r, y - highlight_r, 
                            x - highlight_r + r // 3, y - highlight_r + r // 3],
                           fill='white')
        
        return np.array(pil_img)
    
    def _draw_closed_eyes(self, canvas, parts, y_offset=0):
        """Draw closed eyes (blinking)."""
        if 'left_eye' not in parts or 'right_eye' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for eye_key in ['left_eye', 'right_eye']:
            if eye_key in parts:
                x, y, r = parts[eye_key]
                y += y_offset
                
                # Draw closed eye as a line
                draw.line([(x - r, y), (x + r, y)], fill='black', width=2)
        
        return np.array(pil_img)
