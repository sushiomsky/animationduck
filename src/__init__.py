"""
AnimationDuck - Create animated comic-style GIFs from still images.
"""

from .pipeline import AnimationDuckPipeline
from .comic_style import ComicStyleEffect
from .animation import AnimationFrameGenerator
from .gif_creator import GIFCreator

__version__ = "1.0.0"
__all__ = ['AnimationDuckPipeline', 'ComicStyleEffect', 'AnimationFrameGenerator', 'GIFCreator']
