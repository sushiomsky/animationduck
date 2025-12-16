"""
Duckling detection module using traditional computer vision techniques.
Detects ducklings and their body parts for realistic animation.
"""
import cv2
import numpy as np
from PIL import Image


class DucklingDetector:
    """Detect ducklings and their body parts in images using CPU-only processing."""
    
    def __init__(self):
        """Initialize the duckling detector."""
        pass
    
    def detect_duckling(self, image):
        """
        Detect duckling in the image and extract body parts.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with duckling parts and bounding boxes:
            {
                'full_body': (x, y, w, h),
                'head': (x, y, w, h),
                'body': (x, y, w, h),
                'left_eye': (x, y, radius),
                'right_eye': (x, y, radius),
                'beak': (x, y, w, h),
                'left_wing': (x, y, w, h),
                'right_wing': (x, y, w, h),
                'legs': [(x, y, w, h), ...],
                'mask': numpy array (binary mask of duckling)
            }
        """
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image.copy()
        
        # Ensure RGB format
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        height, width = img_array.shape[:2]
        
        # Detect main duckling region using color segmentation
        full_body_box = self._detect_main_region(img_array)
        
        if full_body_box is None:
            # If detection fails, assume entire image is the duckling
            full_body_box = (0, 0, width, height)
        
        x, y, w, h = full_body_box
        
        # Extract duckling region
        duckling_region = img_array[y:y+h, x:x+w]
        
        # Detect individual parts relative to the duckling region
        parts = self._detect_parts(duckling_region, x, y)
        parts['full_body'] = full_body_box
        
        # Create mask for the duckling
        parts['mask'] = self._create_mask(img_array, full_body_box)
        
        return parts
    
    def _detect_main_region(self, image):
        """
        Detect the main duckling region using color-based segmentation.
        
        Args:
            image: numpy array (RGB)
            
        Returns:
            Bounding box (x, y, w, h) or None if detection fails
        """
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # Define color ranges for typical duckling colors (yellow, brown, white)
        # Yellow ducklings
        lower_yellow = np.array([20, 40, 40])
        upper_yellow = np.array([40, 255, 255])
        
        # Brown ducklings
        lower_brown = np.array([10, 40, 20])
        upper_brown = np.array([30, 255, 200])
        
        # White ducklings
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([180, 30, 255])
        
        # Create masks for each color range
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)
        
        # Combine masks
        mask = cv2.bitwise_or(mask_yellow, mask_brown)
        mask = cv2.bitwise_or(mask, mask_white)
        
        # Apply morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find the largest contour (assume it's the duckling)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Add some padding
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        
        return (x, y, w, h)
    
    def _detect_parts(self, duckling_region, offset_x, offset_y):
        """
        Detect individual body parts within the duckling region.
        
        Args:
            duckling_region: numpy array of the duckling
            offset_x: x offset in the original image
            offset_y: y offset in the original image
            
        Returns:
            Dictionary with body part locations
        """
        h, w = duckling_region.shape[:2]
        
        # Use proportional estimation for body parts
        # Head is typically in the upper portion
        head_y = int(h * 0.15)
        head_h = int(h * 0.35)
        head_x = int(w * 0.3)
        head_w = int(w * 0.4)
        
        # Body is in the middle-lower portion
        body_y = int(h * 0.4)
        body_h = int(h * 0.5)
        body_x = int(w * 0.2)
        body_w = int(w * 0.6)
        
        # Detect eyes within the head region
        eyes = self._detect_eyes(duckling_region, head_x, head_y, head_w, head_h)
        
        # Beak is at the front of the head
        beak_x = head_x + head_w
        beak_y = head_y + int(head_h * 0.4)
        beak_w = int(w * 0.15)
        beak_h = int(head_h * 0.3)
        
        # Wings on the sides of the body
        left_wing_x = int(w * 0.15)
        left_wing_y = int(h * 0.45)
        left_wing_w = int(w * 0.25)
        left_wing_h = int(h * 0.3)
        
        right_wing_x = int(w * 0.6)
        right_wing_y = int(h * 0.45)
        right_wing_w = int(w * 0.25)
        right_wing_h = int(h * 0.3)
        
        # Legs at the bottom
        left_leg_x = int(w * 0.35)
        left_leg_y = int(h * 0.8)
        left_leg_w = int(w * 0.1)
        left_leg_h = int(h * 0.15)
        
        right_leg_x = int(w * 0.55)
        right_leg_y = int(h * 0.8)
        right_leg_w = int(w * 0.1)
        right_leg_h = int(h * 0.15)
        
        # Convert to absolute coordinates
        parts = {
            'head': (offset_x + head_x, offset_y + head_y, head_w, head_h),
            'body': (offset_x + body_x, offset_y + body_y, body_w, body_h),
            'beak': (offset_x + beak_x, offset_y + beak_y, beak_w, beak_h),
            'left_wing': (offset_x + left_wing_x, offset_y + left_wing_y, left_wing_w, left_wing_h),
            'right_wing': (offset_x + right_wing_x, offset_y + right_wing_y, right_wing_w, right_wing_h),
            'legs': [
                (offset_x + left_leg_x, offset_y + left_leg_y, left_leg_w, left_leg_h),
                (offset_x + right_leg_x, offset_y + right_leg_y, right_leg_w, right_leg_h)
            ]
        }
        
        # Add detected eyes
        parts.update(eyes)
        
        return parts
    
    def _detect_eyes(self, region, head_x, head_y, head_w, head_h):
        """
        Detect eyes within the head region.
        
        Args:
            region: numpy array of the duckling
            head_x, head_y, head_w, head_h: head bounding box
            
        Returns:
            Dictionary with eye positions
        """
        # Validate head dimensions
        if head_w <= 0 or head_h <= 0:
            # Return default eye positions if head dimensions are invalid
            eye_radius = 5  # Fallback default
            return {
                'left_eye': (head_x + 10, head_y + 10, eye_radius),
                'right_eye': (head_x + 20, head_y + 10, eye_radius)
            }
        
        # Extract head region
        head_region = region[head_y:head_y+head_h, head_x:head_x+head_w]
        
        # Convert to grayscale
        gray = cv2.cvtColor(head_region, cv2.COLOR_RGB2GRAY)
        
        # Calculate safe radius values
        min_dimension = min(head_w, head_h)
        min_radius = max(1, int(min_dimension * 0.05))
        max_radius = max(min_radius + 1, int(min_dimension * 0.15))
        
        # Use Hough circles to detect eyes (they're often dark and circular)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=max(1, int(head_w * 0.3)),
            param1=50,
            param2=30,
            minRadius=min_radius,
            maxRadius=max_radius
        )
        
        eyes = {}
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            sorted_circles = sorted(circles[0, :], key=lambda c: c[0])  # Sort by x coordinate
            
            if len(sorted_circles) >= 2:
                # Left and right eyes
                eyes['left_eye'] = (
                    head_x + int(sorted_circles[0][0]),
                    head_y + int(sorted_circles[0][1]),
                    int(sorted_circles[0][2])
                )
                eyes['right_eye'] = (
                    head_x + int(sorted_circles[1][0]),
                    head_y + int(sorted_circles[1][1]),
                    int(sorted_circles[1][2])
                )
            elif len(sorted_circles) == 1:
                # Only one eye detected, estimate the other
                eye_x = int(sorted_circles[0][0])
                eye_y = int(sorted_circles[0][1])
                eye_r = int(sorted_circles[0][2])
                
                if eye_x < head_w / 2:
                    eyes['left_eye'] = (head_x + eye_x, head_y + eye_y, eye_r)
                    eyes['right_eye'] = (head_x + head_w - eye_x, head_y + eye_y, eye_r)
                else:
                    eyes['right_eye'] = (head_x + eye_x, head_y + eye_y, eye_r)
                    eyes['left_eye'] = (head_x + head_w - eye_x, head_y + eye_y, eye_r)
        
        # If no eyes detected, use default positions
        if 'left_eye' not in eyes:
            eye_radius = int(min(head_w, head_h) * 0.08)
            eyes['left_eye'] = (
                head_x + int(head_w * 0.3),
                head_y + int(head_h * 0.4),
                eye_radius
            )
            eyes['right_eye'] = (
                head_x + int(head_w * 0.7),
                head_y + int(head_h * 0.4),
                eye_radius
            )
        
        return eyes
    
    def _create_mask(self, image, bounding_box):
        """
        Create a binary mask for the duckling region.
        
        Args:
            image: numpy array (RGB)
            bounding_box: (x, y, w, h)
            
        Returns:
            Binary mask (numpy array)
        """
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        x, y, w, h = bounding_box
        mask[y:y+h, x:x+w] = 255
        return mask
