"""
Animation sequence composer for creating complex multi-action animations.
Combines multiple animation types into a single GIF sequence.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class SequenceComposer:
    """Compose complex animation sequences from multiple actions."""
    
    def __init__(self, num_frames=20):
        """
        Initialize sequence composer.
        
        Args:
            num_frames: Total number of frames for the complete sequence
        """
        self.num_frames = num_frames
    
    def compose(self, image, parts, parsed_sequence, animator):
        """
        Compose animation frames from parsed sequence.
        
        Args:
            image: Base PIL Image
            parts: Body parts detected from DucklingDetector
            parsed_sequence: Parsed sequence from AnimationParser
            animator: HandDrawnAnimator or RealisticDucklingAnimator instance
            
        Returns:
            List of PIL Image frames
        """
        sequences = parsed_sequence['sequences']
        total_duration = parsed_sequence['total_duration']
        
        # Calculate frames for each sequence
        frame_allocations = self._allocate_frames(sequences, total_duration)
        
        all_frames = []
        
        for seq_idx, (sequence, num_seq_frames) in enumerate(zip(sequences, frame_allocations)):
            action = sequence['action']
            objects = sequence['objects']
            conditions = sequence.get('conditions', {})
            
            # Generate frames for this action
            animator.num_frames = num_seq_frames
            animator.animation_type = action
            
            frames = animator.animate(image, parts)
            
            # Add objects to frames if specified
            if objects:
                frames = self._add_objects_to_frames(
                    frames, objects, sequence, seq_idx, len(sequences)
                )
            
            # Add conditional elements (e.g., show dice result)
            if conditions:
                frames = self._add_conditions_to_frames(
                    frames, conditions, sequence
                )
            
            all_frames.extend(frames)
        
        return all_frames
    
    def _allocate_frames(self, sequences, total_duration):
        """Allocate frames to each sequence based on relative duration."""
        allocations = []
        
        for seq in sequences:
            # Calculate proportion of total duration
            proportion = seq['duration'] / total_duration
            seq_frames = max(5, int(self.num_frames * proportion))
            allocations.append(seq_frames)
        
        # Ensure total matches num_frames by adjusting the largest sequence
        total_allocated = sum(allocations)
        if total_allocated != self.num_frames:
            diff = self.num_frames - total_allocated
            max_idx = allocations.index(max(allocations))
            allocations[max_idx] += diff
        
        return allocations
    
    def _add_objects_to_frames(self, frames, objects, sequence, seq_idx, total_seqs):
        """Add objects/props to animation frames."""
        enhanced_frames = []
        
        for frame_idx, frame in enumerate(frames):
            frame_copy = frame.copy()
            
            for obj in objects:
                if obj == 'dice':
                    frame_copy = self._add_dice(
                        frame_copy, frame_idx, len(frames), sequence
                    )
                elif obj == 'star':
                    frame_copy = self._add_stars(
                        frame_copy, frame_idx, len(frames)
                    )
                elif obj == 'coin':
                    frame_copy = self._add_coin(
                        frame_copy, frame_idx, len(frames)
                    )
                elif obj == 'heart':
                    frame_copy = self._add_hearts(
                        frame_copy, frame_idx, len(frames)
                    )
            
            enhanced_frames.append(frame_copy)
        
        return enhanced_frames
    
    def _add_dice(self, frame, frame_idx, total_frames, sequence):
        """Add animated dice to frame."""
        draw = ImageDraw.Draw(frame)
        width, height = frame.size
        
        # Position dice in lower right area
        t = frame_idx / total_frames
        
        # Dice enters from side in first few frames
        if frame_idx < total_frames * 0.3:
            progress = frame_idx / (total_frames * 0.3)
            dice_x = int(width * (0.5 + progress * 0.3))
        else:
            dice_x = int(width * 0.8)
        
        dice_y = int(height * 0.7)
        dice_size = min(width, height) // 8
        
        # Rotation animation for rolling effect
        rotation = frame_idx * 30 % 360
        
        # Draw dice
        frame_copy = frame.copy()
        
        # Create dice on separate layer
        dice_img = Image.new('RGBA', (dice_size * 2, dice_size * 2), (0, 0, 0, 0))
        dice_draw = ImageDraw.Draw(dice_img)
        
        # Draw dice body (white square with black border)
        margin = dice_size // 2
        dice_draw.rectangle(
            [margin, margin, margin + dice_size, margin + dice_size],
            fill='white',
            outline='black',
            width=3
        )
        
        # Draw dice dots based on result
        result = sequence.get('conditions', {}).get('result', 6)
        self._draw_dice_dots(dice_draw, margin, margin, dice_size, result)
        
        # Rotate dice
        rotated_dice = dice_img.rotate(rotation, expand=False)
        
        # Paste onto frame
        frame_copy.paste(
            rotated_dice,
            (dice_x - dice_size, dice_y - dice_size),
            rotated_dice
        )
        
        return frame_copy
    
    def _draw_dice_dots(self, draw, x, y, size, number):
        """Draw dots on dice face."""
        dot_size = size // 10
        positions = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
        }
        
        if number in positions:
            for px, py in positions[number]:
                dot_x = x + int(px * size)
                dot_y = y + int(py * size)
                draw.ellipse(
                    [dot_x - dot_size, dot_y - dot_size,
                     dot_x + dot_size, dot_y + dot_size],
                    fill='black'
                )
    
    def _add_stars(self, frame, frame_idx, total_frames):
        """Add sparkle stars around the duckling."""
        draw = ImageDraw.Draw(frame)
        width, height = frame.size
        
        # Multiple stars at different positions
        num_stars = 5
        for i in range(num_stars):
            t = (frame_idx + i * total_frames / num_stars) / total_frames
            
            # Star position orbits around center
            angle = t * np.pi * 2 + i * np.pi * 2 / num_stars
            radius = min(width, height) * 0.35
            star_x = width // 2 + int(np.cos(angle) * radius)
            star_y = height // 2 + int(np.sin(angle) * radius)
            
            # Star size pulsates
            size = int(10 + 5 * np.sin(t * np.pi * 4))
            
            # Draw simple star
            self._draw_star(draw, star_x, star_y, size, 'yellow')
        
        return frame
    
    def _draw_star(self, draw, x, y, size, color):
        """Draw a simple 4-pointed star."""
        points = [
            (x, y - size),  # Top
            (x - size//3, y - size//3),
            (x - size, y),  # Left
            (x - size//3, y + size//3),
            (x, y + size),  # Bottom
            (x + size//3, y + size//3),
            (x + size, y),  # Right
            (x + size//3, y - size//3),
        ]
        draw.polygon(points, fill=color, outline='orange')
    
    def _add_coin(self, frame, frame_idx, total_frames):
        """Add spinning coin to frame."""
        draw = ImageDraw.Draw(frame)
        width, height = frame.size
        
        # Coin position (upper area)
        coin_x = width // 2
        coin_y = int(height * 0.25)
        
        # Spinning effect - width oscillates
        t = frame_idx / total_frames
        coin_width = int(20 * abs(np.cos(t * np.pi * 4)))
        coin_height = 20
        
        # Draw coin
        draw.ellipse(
            [coin_x - coin_width, coin_y - coin_height,
             coin_x + coin_width, coin_y + coin_height],
            fill='gold',
            outline='orange',
            width=2
        )
        
        return frame
    
    def _add_hearts(self, frame, frame_idx, total_frames):
        """Add floating hearts to frame."""
        draw = ImageDraw.Draw(frame)
        width, height = frame.size
        
        # Multiple hearts floating up
        num_hearts = 3
        for i in range(num_hearts):
            t = (frame_idx + i * total_frames / num_hearts) / total_frames
            
            # Heart rises from bottom to top
            heart_x = width // 2 + int((i - 1) * width * 0.15)
            heart_y = int(height * (0.9 - t * 0.7))
            
            # Heart size
            size = 10
            
            # Draw simple heart shape
            self._draw_heart(draw, heart_x, heart_y, size, 'red')
        
        return frame
    
    def _draw_heart(self, draw, x, y, size, color):
        """Draw a simple heart shape."""
        # Two circles for top, triangle for bottom
        draw.ellipse([x - size, y - size//2, x, y + size//2], fill=color)
        draw.ellipse([x, y - size//2, x + size, y + size//2], fill=color)
        draw.polygon([
            (x - size, y),
            (x + size, y),
            (x, y + size * 1.5)
        ], fill=color)
    
    def _add_conditions_to_frames(self, frames, conditions, sequence):
        """Add visual elements based on conditions."""
        enhanced_frames = []
        
        for frame_idx, frame in enumerate(frames):
            frame_copy = frame.copy()
            
            # Show result number if specified (e.g., dice result)
            if 'result' in conditions:
                result = conditions['result']
                # Show result in last few frames
                if frame_idx > len(frames) * 0.7:
                    frame_copy = self._add_result_text(frame_copy, result)
            
            # Add success/failure indicators
            if 'outcome' in conditions:
                outcome = conditions['outcome']
                if outcome == 'success' and frame_idx > len(frames) * 0.6:
                    # Add success sparkles
                    frame_copy = self._add_stars(frame_copy, frame_idx, len(frames))
            
            enhanced_frames.append(frame_copy)
        
        return enhanced_frames
    
    def _add_result_text(self, frame, result):
        """Add result text/number to frame."""
        draw = ImageDraw.Draw(frame)
        width, height = frame.size
        
        # Draw result number prominently
        text = str(result)
        
        # Position near the dice area
        text_x = int(width * 0.75)
        text_y = int(height * 0.55)
        
        # Use default font (PIL doesn't always have font support)
        font = None
        
        # Draw text with outline for visibility
        outline_color = 'black'
        text_color = 'red'
        
        # Draw outline
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    draw.text((text_x + dx, text_y + dy), text, fill=outline_color, font=font)
        
        # Draw main text
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        
        return frame
