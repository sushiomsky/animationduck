"""
Enhanced hand-drawn cartoon animation module.
Implements classical animation principles: squash & stretch, anticipation, 
follow-through, exaggeration, and timing variations.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cv2


class HandDrawnAnimator:
    """Create hand-drawn style animations with classical animation principles."""
    
    def __init__(self, num_frames=15, animation_type='walk'):
        """
        Initialize hand-drawn animator.
        
        Args:
            num_frames: Number of frames to generate
            animation_type: Type of animation
        """
        self.num_frames = num_frames
        self.animation_type = animation_type
    
    def animate(self, image, parts):
        """
        Create hand-drawn animation frames with classical principles.
        
        Args:
            image: PIL Image
            parts: Dictionary of body parts from DucklingDetector
            
        Returns:
            List of PIL Images (frames)
        """
        if self.animation_type == 'walk':
            return self._animate_walk_handdrawn(image, parts)
        elif self.animation_type == 'jump':
            return self._animate_jump_handdrawn(image, parts)
        elif self.animation_type == 'fly':
            return self._animate_fly_handdrawn(image, parts)
        elif self.animation_type == 'idle':
            return self._animate_idle_handdrawn(image, parts)
        elif self.animation_type == 'excited':
            return self._animate_excited(image, parts)
        else:
            return self._animate_walk_handdrawn(image, parts)
    
    def _animate_walk_handdrawn(self, image, parts):
        """Create hand-drawn walking animation with squash & stretch."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Exaggerated bobbing with ease in/out
            bob_curve = self._ease_in_out(np.sin(t * np.pi * 4))
            bob_offset = int(bob_curve * 12)  # Increased amplitude
            
            # Leg movement with anticipation
            phase = t * np.pi * 4
            left_leg_angle = np.sin(phase) * 35  # More exaggerated
            right_leg_angle = np.sin(phase + np.pi) * 35
            
            # Head bobbing with follow-through (delayed)
            head_phase = t * np.pi * 4 - 0.3  # Slight delay
            head_bob = int(np.sin(head_phase) * 6)
            head_tilt = np.sin(head_phase) * 8  # Head tilt for dynamism
            
            # Squash and stretch based on vertical velocity
            velocity = np.cos(t * np.pi * 4)
            squash_factor = 1.0 + velocity * 0.15  # Squash when going down
            stretch_factor = 1.0 / squash_factor  # Stretch when going up
            
            # Create frame with hand-drawn variations
            canvas = self._create_canvas_with_noise(width, height)
            canvas_array = np.array(canvas)
            
            # Apply squash & stretch transform
            canvas_array = self._apply_squash_stretch_transform(
                img_array, canvas_array, parts,
                y_offset=bob_offset,
                squash_x=squash_factor,
                squash_y=stretch_factor,
                rotation=head_tilt * 0.5
            )
            
            # Draw exaggerated animated legs with rubber hose style
            canvas_array = self._draw_rubber_hose_legs(
                canvas_array, parts,
                left_angle=left_leg_angle,
                right_angle=right_leg_angle,
                y_offset=bob_offset,
                squash=squash_factor
            )
            
            # Add motion blur on fast movements
            if abs(velocity) > 0.7:
                canvas_array = self._add_motion_smear(canvas_array, velocity)
            
            # Expressive eyes with blinks and expressions
            if i % (self.num_frames // 3) == 0:  # More frequent blinks
                canvas_array = self._draw_closed_eyes(canvas_array, parts, head_bob)
            else:
                # Eyes follow direction of movement
                eye_offset_x = int(np.sin(phase) * 2)
                canvas_array = self._draw_expressive_eyes(
                    canvas_array, parts, head_bob, eye_offset_x
                )
            
            # Add hand-drawn line variation
            canvas_pil = Image.fromarray(canvas_array)
            canvas_pil = self._add_hand_drawn_variation(canvas_pil, t)
            
            frames.append(canvas_pil)
        
        return frames
    
    def _animate_jump_handdrawn(self, image, parts):
        """Create hand-drawn jumping with anticipation and overshoot."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Anticipation (squat down), jump, overshoot, settle
            if t < 0.2:  # Anticipation phase
                jump_progress = t / 0.2
                jump_offset = -int(jump_progress * 15)  # Squat down
                squash_y = 0.85  # Squashed
                squash_x = 1.15
            elif t < 0.6:  # Jump phase
                jump_progress = (t - 0.2) / 0.4
                # Parabolic arc
                arc = np.sin(jump_progress * np.pi)
                jump_offset = -int(arc * height * 0.25)  # Higher jump
                squash_y = 1.2  # Stretched
                squash_x = 0.9
            elif t < 0.8:  # Landing with overshoot
                jump_progress = (t - 0.6) / 0.2
                jump_offset = int(jump_progress * 10)  # Overshoot below
                squash_y = 0.8  # Squashed on landing
                squash_x = 1.2
            else:  # Settle
                jump_progress = (t - 0.8) / 0.2
                jump_offset = int((1 - jump_progress) * 10)
                squash_y = 0.9 + jump_progress * 0.1
                squash_x = 1.1 - jump_progress * 0.1
            
            # Wing flapping - exaggerated
            wing_phase = t * np.pi * 6
            wing_angle = np.sin(wing_phase) * 45
            
            # Create frame
            canvas = self._create_canvas_with_noise(width, height)
            canvas_array = np.array(canvas)
            
            # Apply transform with squash & stretch
            canvas_array = self._apply_squash_stretch_transform(
                img_array, canvas_array, parts,
                y_offset=jump_offset,
                squash_x=squash_x,
                squash_y=squash_y,
                rotation=0
            )
            
            # Exaggerated wings
            canvas_array = self._draw_cartoon_wings(
                canvas_array, parts,
                left_angle=-wing_angle,
                right_angle=wing_angle,
                y_offset=jump_offset,
                exaggeration=1.5
            )
            
            # Legs tucked during flight
            leg_tuck = 45 if 0.2 < t < 0.6 else 0
            canvas_array = self._draw_rubber_hose_legs(
                canvas_array, parts,
                left_angle=leg_tuck,
                right_angle=leg_tuck,
                y_offset=jump_offset,
                squash=1.0
            )
            
            # Expressive eyes - wider during jump
            if 0.2 < t < 0.6:
                canvas_array = self._draw_excited_eyes(canvas_array, parts, jump_offset)
            else:
                canvas_array = self._draw_expressive_eyes(canvas_array, parts, jump_offset, 0)
            
            canvas_pil = Image.fromarray(canvas_array)
            canvas_pil = self._add_hand_drawn_variation(canvas_pil, t)
            frames.append(canvas_pil)
        
        return frames
    
    def _animate_fly_handdrawn(self, image, parts):
        """Create hand-drawn flying with wing flapping and hovering."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Gentle hovering with sine wave
            hover_offset = int(np.sin(t * np.pi * 2) * 10)
            
            # Fast wing flapping - exaggerated cartoon style
            wing_phase = t * np.pi * 8
            wing_angle = np.sin(wing_phase) * 55  # Very exaggerated
            
            # Body tilt in flight direction
            body_tilt = np.sin(t * np.pi * 2) * 5
            
            # Slight squash & stretch with wing beats
            wing_velocity = np.cos(wing_phase) * 8
            squash = 1.0 + abs(wing_velocity) * 0.05
            
            canvas = self._create_canvas_with_noise(width, height)
            canvas_array = np.array(canvas)
            
            canvas_array = self._apply_squash_stretch_transform(
                img_array, canvas_array, parts,
                y_offset=hover_offset,
                squash_x=1.0,
                squash_y=1.0,
                rotation=body_tilt
            )
            
            # Draw wings with motion blur
            canvas_array = self._draw_cartoon_wings(
                canvas_array, parts,
                left_angle=-wing_angle,
                right_angle=wing_angle,
                y_offset=hover_offset,
                exaggeration=2.0,
                motion_blur=abs(wing_velocity) > 6
            )
            
            # Legs tucked
            canvas_array = self._draw_rubber_hose_legs(
                canvas_array, parts,
                left_angle=45,
                right_angle=45,
                y_offset=hover_offset - 10,
                squash=1.0
            )
            
            canvas_array = self._draw_expressive_eyes(
                canvas_array, parts, hover_offset, 0
            )
            
            canvas_pil = Image.fromarray(canvas_array)
            canvas_pil = self._add_hand_drawn_variation(canvas_pil, t)
            frames.append(canvas_pil)
        
        return frames
    
    def _animate_idle_handdrawn(self, image, parts):
        """Create hand-drawn idle with breathing and micro-movements."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Gentle breathing
            breath = np.sin(t * np.pi * 2) * 4
            squash_breath = 1.0 + np.sin(t * np.pi * 2) * 0.03
            
            # Occasional head turn
            head_turn = 0
            head_tilt = 0
            if 0.3 < t < 0.7:
                turn_progress = (t - 0.3) / 0.4
                head_turn = int(np.sin(turn_progress * np.pi) * 8)
                head_tilt = np.sin(turn_progress * np.pi) * 10
            
            # Occasional blink
            blink = (0.4 < t < 0.45) or (0.8 < t < 0.85)
            
            canvas = self._create_canvas_with_noise(width, height)
            canvas_array = np.array(canvas)
            
            canvas_array = self._apply_squash_stretch_transform(
                img_array, canvas_array, parts,
                y_offset=int(breath),
                squash_x=1.0/squash_breath,
                squash_y=squash_breath,
                rotation=head_tilt
            )
            
            if blink:
                canvas_array = self._draw_closed_eyes(canvas_array, parts, int(breath), head_turn)
            else:
                canvas_array = self._draw_expressive_eyes(
                    canvas_array, parts, int(breath), head_turn
                )
            
            canvas_pil = Image.fromarray(canvas_array)
            canvas_pil = self._add_hand_drawn_variation(canvas_pil, t)
            frames.append(canvas_pil)
        
        return frames
    
    def _animate_excited(self, image, parts):
        """Create excited/celebration animation."""
        frames = []
        img_array = np.array(image)
        width, height = image.size
        
        for i in range(self.num_frames):
            t = i / self.num_frames
            
            # Bouncing excitedly
            bounce = abs(np.sin(t * np.pi * 6)) * 20
            
            # Wings flapping rapidly
            wing_angle = np.sin(t * np.pi * 8) * 50
            
            # Body squash and stretch
            squash_y = 0.9 + abs(np.sin(t * np.pi * 6)) * 0.2
            squash_x = 2.0 - squash_y
            
            canvas = self._create_canvas_with_noise(width, height)
            canvas_array = np.array(canvas)
            
            canvas_array = self._apply_squash_stretch_transform(
                img_array, canvas_array, parts,
                y_offset=-int(bounce),
                squash_x=squash_x,
                squash_y=squash_y,
                rotation=np.sin(t * np.pi * 6) * 10
            )
            
            canvas_array = self._draw_cartoon_wings(
                canvas_array, parts,
                left_angle=-wing_angle,
                right_angle=wing_angle,
                y_offset=-int(bounce),
                exaggeration=2.0
            )
            
            # Excited eyes
            canvas_array = self._draw_excited_eyes(canvas_array, parts, -int(bounce))
            
            canvas_pil = Image.fromarray(canvas_array)
            canvas_pil = self._add_hand_drawn_variation(canvas_pil, t)
            frames.append(canvas_pil)
        
        return frames
    
    # Helper methods
    def _ease_in_out(self, t):
        """Apply ease-in-out timing curve."""
        return t * t * (3.0 - 2.0 * t)
    
    def _create_canvas_with_noise(self, width, height):
        """Create canvas with slight texture for hand-drawn feel."""
        canvas = Image.new('RGB', (width, height), color=(255, 255, 255))
        # Add subtle paper texture
        noise = np.random.randint(-3, 4, (height, width, 3), dtype=np.int16)
        canvas_array = np.array(canvas, dtype=np.int16) + noise
        canvas_array = np.clip(canvas_array, 0, 255).astype(np.uint8)
        return Image.fromarray(canvas_array)
    
    def _apply_squash_stretch_transform(self, source, canvas, parts,
                                        y_offset=0, squash_x=1.0, squash_y=1.0, rotation=0):
        """Apply squash & stretch transformation."""
        h, w = source.shape[:2]
        
        # Calculate new dimensions with squash & stretch
        new_w = int(w * squash_x)
        new_h = int(h * squash_y)
        
        # Resize with squash & stretch
        source_pil = Image.fromarray(source)
        stretched = source_pil.resize((new_w, new_h), Image.LANCZOS)
        
        # Rotate if needed
        if abs(rotation) > 0.5:
            stretched = stretched.rotate(rotation, resample=Image.BICUBIC, expand=False)
        
        # Center on canvas with offset
        canvas_pil = Image.fromarray(canvas)
        x_pos = (w - new_w) // 2
        y_pos = (h - new_h) // 2 + y_offset
        
        # Ensure positions are within bounds
        x_pos = max(0, min(x_pos, w - new_w))
        y_pos = max(0, min(y_pos, h - new_h))
        
        canvas_pil.paste(stretched, (x_pos, y_pos))
        return np.array(canvas_pil)
    
    def _draw_rubber_hose_legs(self, canvas, parts, left_angle=0, right_angle=0, 
                               y_offset=0, squash=1.0):
        """Draw legs with rubber hose style (bendable, cartoon-like)."""
        if 'legs' not in parts or not parts['legs']:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for idx, leg in enumerate(parts['legs']):
            x, y, w, h = leg
            y += y_offset
            
            angle = left_angle if idx == 0 else right_angle
            
            # Draw curved rubber hose leg
            leg_top_x = x + w // 2
            leg_top_y = y
            
            # Mid point for curve (rubber hose bend)
            mid_bend = int(h * 0.5)
            mid_x = leg_top_x + int(np.sin(np.radians(angle * 0.6)) * mid_bend)
            mid_y = leg_top_y + mid_bend
            
            # Bottom point
            leg_bottom_x = leg_top_x + int(np.sin(np.radians(angle)) * h)
            leg_bottom_y = leg_top_y + int(np.cos(np.radians(angle)) * h)
            
            # Draw curved leg using multiple segments
            points = self._create_curve_points(
                (leg_top_x, leg_top_y),
                (mid_x, mid_y),
                (leg_bottom_x, leg_bottom_y),
                segments=5
            )
            
            # Draw thick rubber hose line
            for i in range(len(points) - 1):
                thickness = max(3, int(w // 2 * squash))
                draw.line([points[i], points[i+1]], fill='orange', width=thickness)
            
            # Draw cartoon foot
            foot_size = int(w * 1.5)
            foot_points = [
                (leg_bottom_x - foot_size, leg_bottom_y),
                (leg_bottom_x, leg_bottom_y + foot_size // 2),
                (leg_bottom_x + foot_size, leg_bottom_y)
            ]
            draw.polygon(foot_points, fill='orange', outline='darkorange')
        
        return np.array(pil_img)
    
    def _draw_cartoon_wings(self, canvas, parts, left_angle=0, right_angle=0,
                           y_offset=0, exaggeration=1.0, motion_blur=False):
        """Draw exaggerated cartoon wings."""
        if 'left_wing' not in parts or 'right_wing' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        # Draw left wing
        x, y, w, h = parts['left_wing']
        y += y_offset
        wing_length = int(w * exaggeration)
        
        center_x, center_y = x + w, y + h // 2
        tip_x = center_x + int(np.cos(np.radians(left_angle)) * wing_length)
        tip_y = center_y - int(np.sin(np.radians(left_angle)) * wing_length)
        
        # Exaggerated feather shape
        wing_points = [
            (center_x, center_y - int(h * 0.6)),
            (tip_x, tip_y - int(h * 0.3)),
            (tip_x + int(wing_length * 0.2), tip_y),
            (tip_x, tip_y + int(h * 0.3)),
            (center_x, center_y + int(h * 0.6))
        ]
        
        if motion_blur:
            # Draw semi-transparent motion blur
            for offset in range(-3, 4, 2):
                blur_points = [(p[0] + offset, p[1]) for p in wing_points]
                draw.polygon(blur_points, fill=(255, 215, 0, 100), outline='orange')
        else:
            draw.polygon(wing_points, fill='gold', outline='orange')
        
        # Draw right wing
        x, y, w, h = parts['right_wing']
        y += y_offset
        
        center_x, center_y = x, y + h // 2
        tip_x = center_x + int(np.cos(np.radians(180 - right_angle)) * wing_length)
        tip_y = center_y - int(np.sin(np.radians(180 - right_angle)) * wing_length)
        
        wing_points = [
            (center_x, center_y - int(h * 0.6)),
            (tip_x, tip_y - int(h * 0.3)),
            (tip_x - int(wing_length * 0.2), tip_y),
            (tip_x, tip_y + int(h * 0.3)),
            (center_x, center_y + int(h * 0.6))
        ]
        
        if motion_blur:
            for offset in range(-3, 4, 2):
                blur_points = [(p[0] + offset, p[1]) for p in wing_points]
                draw.polygon(blur_points, fill=(255, 215, 0, 100), outline='orange')
        else:
            draw.polygon(wing_points, fill='gold', outline='orange')
        
        return np.array(pil_img)
    
    def _draw_expressive_eyes(self, canvas, parts, y_offset=0, x_offset=0):
        """Draw expressive cartoon eyes."""
        if 'left_eye' not in parts or 'right_eye' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for eye_key in ['left_eye', 'right_eye']:
            if eye_key in parts:
                x, y, r = parts[eye_key]
                x += x_offset
                y += y_offset
                
                # Larger, more expressive eyes
                eye_r = int(r * 1.3)
                
                # White of eye
                draw.ellipse([x - eye_r, y - eye_r, x + eye_r, y + eye_r], 
                           fill='white', outline='black', width=2)
                
                # Pupil (can look in direction)
                pupil_r = int(eye_r * 0.6)
                pupil_x = x + int(x_offset * 0.5)
                draw.ellipse([pupil_x - pupil_r, y - pupil_r, 
                            pupil_x + pupil_r, y + pupil_r], 
                           fill='black')
                
                # Large highlight for cartoon effect
                highlight_r = int(eye_r * 0.4)
                draw.ellipse([x - int(eye_r * 0.3), y - int(eye_r * 0.3), 
                            x - int(eye_r * 0.3) + highlight_r, 
                            y - int(eye_r * 0.3) + highlight_r],
                           fill='white')
        
        return np.array(pil_img)
    
    def _draw_excited_eyes(self, canvas, parts, y_offset=0):
        """Draw excited/surprised eyes (wider)."""
        if 'left_eye' not in parts or 'right_eye' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for eye_key in ['left_eye', 'right_eye']:
            if eye_key in parts:
                x, y, r = parts[eye_key]
                y += y_offset
                
                # Much larger for excited expression
                eye_r = int(r * 1.6)
                
                draw.ellipse([x - eye_r, y - eye_r, x + eye_r, y + eye_r], 
                           fill='white', outline='black', width=3)
                
                pupil_r = int(eye_r * 0.5)
                draw.ellipse([x - pupil_r, y - pupil_r, x + pupil_r, y + pupil_r], 
                           fill='black')
                
                # Sparkle highlights
                for offset in [(-0.3, -0.3), (0.2, 0.2)]:
                    hx = x + int(eye_r * offset[0])
                    hy = y + int(eye_r * offset[1])
                    hr = int(eye_r * 0.25)
                    draw.ellipse([hx, hy, hx + hr, hy + hr], fill='white')
        
        return np.array(pil_img)
    
    def _draw_closed_eyes(self, canvas, parts, y_offset=0, x_offset=0):
        """Draw closed eyes (blinking)."""
        if 'left_eye' not in parts or 'right_eye' not in parts:
            return canvas
        
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)
        
        for eye_key in ['left_eye', 'right_eye']:
            if eye_key in parts:
                x, y, r = parts[eye_key]
                x += x_offset
                y += y_offset
                
                # Curved closed eye
                eye_r = int(r * 1.3)
                draw.arc([x - eye_r, y - eye_r // 2, x + eye_r, y + eye_r // 2],
                        start=0, end=180, fill='black', width=3)
        
        return np.array(pil_img)
    
    def _add_motion_smear(self, canvas, velocity):
        """Add motion blur/smear for fast movements."""
        # Simple horizontal motion blur
        blur_amount = int(abs(velocity) * 2)
        if blur_amount > 1:
            pil_img = Image.fromarray(canvas)
            pil_img = pil_img.filter(ImageFilter.BoxBlur(blur_amount))
            return np.array(pil_img)
        return canvas
    
    def _add_hand_drawn_variation(self, image, t):
        """Add subtle variations to simulate hand-drawn animation."""
        # Add very subtle random offset to simulate hand-drawn imperfections
        offset_x = int(np.sin(t * np.pi * 10) * 0.5)
        offset_y = int(np.cos(t * np.pi * 10) * 0.5)
        
        if offset_x != 0 or offset_y != 0:
            return image.transform(
                image.size,
                Image.AFFINE,
                (1, 0, offset_x, 0, 1, offset_y),
                resample=Image.BILINEAR
            )
        return image
    
    def _create_curve_points(self, p1, p2, p3, segments=10):
        """Create quadratic bezier curve points."""
        points = []
        for i in range(segments + 1):
            t = i / segments
            # Quadratic bezier formula
            x = (1-t)**2 * p1[0] + 2*(1-t)*t * p2[0] + t**2 * p3[0]
            y = (1-t)**2 * p1[1] + 2*(1-t)*t * p2[1] + t**2 * p3[1]
            points.append((int(x), int(y)))
        return points
