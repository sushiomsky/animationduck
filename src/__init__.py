"""
AnimationDuck - Create animated comic-style GIFs from still images.
"""

from .pipeline import AnimationDuckPipeline
from .comic_style import ComicStyleEffect
from .animation import AnimationFrameGenerator
from .gif_creator import GIFCreator
from .duckling_detector import DucklingDetector
from .realistic_animator import RealisticDucklingAnimator
from .handdrawn_animator import HandDrawnAnimator
from .animation_parser import AnimationParser
from .sequence_composer import SequenceComposer

__version__ = "1.0.0"
__all__ = [
    'AnimationDuckPipeline',
    'ComicStyleEffect', 
    'AnimationFrameGenerator',
    'GIFCreator',
    'DucklingDetector',
    'RealisticDucklingAnimator',
    'HandDrawnAnimator',
    'AnimationParser',
    'SequenceComposer'
]
