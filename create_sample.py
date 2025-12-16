#!/usr/bin/env python3
"""
Generate a sample duckling image for testing.
"""
from PIL import Image, ImageDraw
import os

def create_sample_duckling():
    """Create a simple duckling-like test image."""
    # Create a canvas
    width, height = 400, 400
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple duckling
    # Body (yellow oval)
    draw.ellipse([100, 180, 300, 350], fill='yellow', outline='orange', width=3)
    
    # Head (yellow circle)
    draw.ellipse([150, 100, 280, 230], fill='yellow', outline='orange', width=3)
    
    # Beak (orange triangle-ish)
    draw.polygon([280, 160, 350, 150, 350, 170], fill='orange', outline='darkorange')
    
    # Eyes
    draw.ellipse([200, 140, 220, 160], fill='black')
    draw.ellipse([240, 140, 260, 160], fill='black')
    # Eye highlights
    draw.ellipse([205, 145, 212, 152], fill='white')
    draw.ellipse([245, 145, 252, 152], fill='white')
    
    # Wing
    draw.ellipse([120, 220, 200, 300], fill='gold', outline='orange', width=2)
    
    # Feet
    draw.polygon([170, 340, 160, 370, 190, 370], fill='orange', outline='darkorange')
    draw.polygon([230, 340, 220, 370, 250, 370], fill='orange', outline='darkorange')
    
    return img

if __name__ == '__main__':
    # Create examples directory if it doesn't exist
    os.makedirs('examples', exist_ok=True)
    
    # Generate and save sample duckling
    img = create_sample_duckling()
    output_path = 'examples/sample_duckling.png'
    img.save(output_path)
    print(f"Sample duckling image created: {output_path}")
