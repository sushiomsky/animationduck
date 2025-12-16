"""
Comic style effect module for converting images to comic/cartoon style.
Uses CPU-friendly image processing techniques.
"""
import cv2
import numpy as np
from PIL import Image


class ComicStyleEffect:
    """Apply comic/cartoon style effects to images."""
    
    def __init__(self, edge_thickness=2, color_levels=8):
        """
        Initialize comic style effect.
        
        Args:
            edge_thickness: Thickness of edge lines (default: 2)
            color_levels: Number of color levels for posterization (default: 8)
        """
        self.edge_thickness = edge_thickness
        self.color_levels = color_levels
    
    def apply(self, image, hand_drawn_style=False):
        """
        Apply comic style effect to an image.
        
        Args:
            image: PIL Image or numpy array
            hand_drawn_style: Use enhanced hand-drawn comic style (default: False)
            
        Returns:
            PIL Image with comic style applied
        """
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        # Ensure RGB format
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        if hand_drawn_style:
            # Enhanced hand-drawn comic style
            result = self._apply_hand_drawn_style(img_array)
        else:
            # Original comic style
            # Apply bilateral filter for smooth cartoon effect
            smooth = cv2.bilateralFilter(img_array, d=9, sigmaColor=75, sigmaSpace=75)
            
            # Posterize colors to reduce color levels
            posterized = self._posterize(smooth, self.color_levels)
            
            # Detect edges
            edges = self._detect_edges(img_array)
            
            # Combine posterized image with edges
            result = self._combine_with_edges(posterized, edges)
        
        return Image.fromarray(result)
    
    def _apply_hand_drawn_style(self, image):
        """Apply enhanced hand-drawn comic strip style."""
        # More aggressive bilateral filtering for flatter colors
        smooth = cv2.bilateralFilter(image, d=11, sigmaColor=90, sigmaSpace=90)
        smooth = cv2.bilateralFilter(smooth, d=9, sigmaColor=80, sigmaSpace=80)
        
        # Stronger posterization (fewer colors)
        posterized = self._posterize(smooth, max(4, self.color_levels - 2))
        
        # Boost color saturation for more vibrant cartoon look
        hsv = cv2.cvtColor(posterized, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)  # Increase saturation
        posterized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        
        # Multiple edge detection passes for bold outlines
        edges1 = self._detect_edges(image)
        edges2 = self._detect_edges_canny(image)
        
        # Combine edge maps
        edges = cv2.bitwise_or(edges1, edges2)
        
        # Thicken edges more for hand-drawn look
        kernel = np.ones((self.edge_thickness + 1, self.edge_thickness + 1), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Add slight variation to edges for hand-drawn feel
        edges = self._add_edge_variation(edges)
        
        # Combine with bolder edges
        result = self._combine_with_edges_bold(posterized, edges)
        
        return result
    
    def _detect_edges_canny(self, image):
        """Detect edges using Canny edge detector for sharper lines."""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return cv2.bitwise_not(edges)
    
    def _add_edge_variation(self, edges):
        """Add slight variation to edges for hand-drawn imperfection."""
        # Add random noise to make lines less perfect
        noise = np.random.randint(-5, 6, edges.shape, dtype=np.int16)
        edges_varied = edges.astype(np.int16) + noise
        edges_varied = np.clip(edges_varied, 0, 255).astype(np.uint8)
        return edges_varied
    
    def _combine_with_edges_bold(self, image, edges):
        """Combine with bolder edges for hand-drawn comic style."""
        # Create 3-channel edge mask
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        # Much stronger darkening for bold outlines
        result = image.copy()
        result[edges < 128] = result[edges < 128] * 0.15  # Much darker
        
        return result.astype(np.uint8)
        posterized = self._posterize(smooth, self.color_levels)
        
        # Detect edges
        edges = self._detect_edges(img_array)
        
        # Combine posterized image with edges
        result = self._combine_with_edges(posterized, edges)
        
        return Image.fromarray(result)
    
    def _posterize(self, image, levels):
        """
        Reduce the number of colors in the image.
        
        Args:
            image: numpy array
            levels: number of color levels per channel
            
        Returns:
            numpy array with posterized colors
        """
        # Calculate the number of bits to preserve
        indices = np.arange(0, 256)
        divider = 255 / (levels - 1)
        quantized = np.int32(np.round(indices / divider))
        color_levels = np.uint8(quantized * divider)
        
        # Apply posterization
        posterized = color_levels[image]
        return posterized
    
    def _detect_edges(self, image):
        """
        Detect edges in the image using adaptive threshold.
        
        Args:
            image: numpy array
            
        Returns:
            binary edge map (numpy array)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply median blur to reduce noise
        blurred = cv2.medianBlur(gray, 5)
        
        # Detect edges using adaptive threshold
        edges = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2
        )
        
        # Invert edges (we want black lines on white)
        edges = cv2.bitwise_not(edges)
        
        # Dilate edges if thickness > 1
        if self.edge_thickness > 1:
            kernel = np.ones((self.edge_thickness, self.edge_thickness), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
        
        return edges
    
    def _combine_with_edges(self, image, edges):
        """
        Combine posterized image with edge lines.
        
        Args:
            image: posterized color image (numpy array)
            edges: binary edge map (numpy array)
            
        Returns:
            combined image (numpy array)
        """
        # Create a 3-channel edge mask
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        # Darken the image where edges are detected
        result = image.copy()
        result[edges < 128] = result[edges < 128] * 0.3
        
        return result.astype(np.uint8)
