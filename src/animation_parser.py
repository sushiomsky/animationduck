"""
Animation sequence parser for text-to-animation generation.
Parses natural language descriptions into animation sequences.
"""
import re


class AnimationParser:
    """Parse text descriptions into animation sequences."""
    
    # Keywords for actions
    ACTION_KEYWORDS = {
        'walk': ['walk', 'walking', 'walks', 'stroll', 'waddle'],
        'jump': ['jump', 'jumping', 'jumps', 'hop', 'leap', 'bounce'],
        'fly': ['fly', 'flying', 'flies', 'soar', 'glide'],
        'idle': ['idle', 'stand', 'wait', 'rest', 'breath'],
        'excited': ['cheer', 'celebrate', 'excited', 'happy', 'joy', 'victory', 'yay'],
        'roll': ['roll', 'rolling', 'rolls', 'spin', 'rotate'],
    }
    
    # Keywords for objects/props
    OBJECT_KEYWORDS = {
        'dice': ['dice', 'die', 'cube'],
        'star': ['star', 'sparkle', 'twinkle'],
        'coin': ['coin', 'money'],
        'heart': ['heart', 'love'],
    }
    
    # Keywords for emotions/states
    EMOTION_KEYWORDS = {
        'happy': ['happy', 'joyful', 'glad', 'pleased'],
        'excited': ['excited', 'thrilled', 'energetic'],
        'sad': ['sad', 'unhappy', 'disappointed'],
        'surprised': ['surprised', 'shocked', 'amazed'],
    }
    
    def __init__(self):
        """Initialize parser."""
        pass
    
    def parse(self, description):
        """
        Parse animation description into sequence of actions.
        
        Args:
            description: Natural language description of animation
            
        Returns:
            Dictionary with parsed sequence:
            {
                'sequences': [
                    {
                        'action': 'walk',
                        'duration': 1.0,  # relative duration
                        'objects': ['dice'],
                        'emotion': 'neutral'
                    },
                    ...
                ],
                'total_duration': 3.0,
                'description': original description
            }
        """
        description = description.lower()
        sequences = []
        
        # Split description by common separators
        # "and then", "then", "after", "as", "when", "while", ","
        segments = self._split_description(description)
        
        for segment in segments:
            action_info = self._parse_segment(segment)
            if action_info:
                sequences.append(action_info)
        
        # If no sequences found, default to excited animation
        if not sequences:
            sequences.append({
                'action': 'excited',
                'duration': 1.0,
                'objects': [],
                'emotion': 'neutral',
                'conditions': {}
            })
        
        # Calculate total duration
        total_duration = sum(seq['duration'] for seq in sequences)
        
        return {
            'sequences': sequences,
            'total_duration': total_duration,
            'description': description
        }
    
    def _split_description(self, description):
        """Split description into action segments."""
        # Split by common separators
        separators = [
            ' and then ',
            ' then ',
            ' after that ',
            ' afterwards ',
            ' before ',
            ' as ',
            ' when ',
            ' while ',
            r',\s*(?=and\s)',
            r',\s*'
        ]
        
        segments = [description]
        for sep in separators:
            new_segments = []
            for seg in segments:
                parts = re.split(sep, seg)
                new_segments.extend([p.strip() for p in parts if p.strip()])
            segments = new_segments
        
        return segments
    
    def _parse_segment(self, segment):
        """Parse a single segment into action info."""
        action = self._extract_action(segment)
        objects = self._extract_objects(segment)
        emotion = self._extract_emotion(segment)
        conditions = self._extract_conditions(segment)
        
        # Determine duration based on action complexity
        duration = 1.0
        if action in ['walk', 'fly']:
            duration = 1.2
        elif action == 'roll':
            duration = 0.8
        elif action == 'excited':
            duration = 1.5
        
        # Adjust duration if multiple objects
        if len(objects) > 1:
            duration *= 1.2
        
        return {
            'action': action,
            'duration': duration,
            'objects': objects,
            'emotion': emotion,
            'conditions': conditions
        }
    
    def _extract_action(self, segment):
        """Extract action type from segment."""
        for action, keywords in self.ACTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in segment:
                    return action
        
        # Default to idle if no action found
        return 'idle'
    
    def _extract_objects(self, segment):
        """Extract objects/props from segment."""
        objects = []
        for obj_type, keywords in self.OBJECT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in segment:
                    if obj_type not in objects:
                        objects.append(obj_type)
        return objects
    
    def _extract_emotion(self, segment):
        """Extract emotion/state from segment."""
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in segment:
                    return emotion
        return 'neutral'
    
    def _extract_conditions(self, segment):
        """Extract conditions from segment (e.g., 'as result is 6')."""
        conditions = {}
        
        # Look for number results
        number_pattern = r'(?:result|shows|displays|is)\s+(?:a\s+)?(\d+)'
        match = re.search(number_pattern, segment)
        if match:
            conditions['result'] = int(match.group(1))
        
        # Look for success/failure conditions
        if any(word in segment for word in ['win', 'wins', 'success', 'succeeds']):
            conditions['outcome'] = 'success'
        elif any(word in segment for word in ['lose', 'loses', 'fail', 'fails']):
            conditions['outcome'] = 'failure'
        
        return conditions
    
    def get_suggested_frames(self, parsed_sequence):
        """
        Calculate suggested number of frames based on sequence complexity.
        
        Args:
            parsed_sequence: Parsed sequence from parse()
            
        Returns:
            Suggested number of frames
        """
        total_duration = parsed_sequence['total_duration']
        num_sequences = len(parsed_sequence['sequences'])
        
        # Base frames: 10 per unit duration
        base_frames = int(total_duration * 10)
        
        # Add frames for complexity
        complexity_frames = num_sequences * 5
        
        # Minimum 15, maximum 40
        frames = max(15, min(40, base_frames + complexity_frames))
        
        return frames
    
    def get_suggested_duration(self, parsed_sequence):
        """
        Calculate suggested frame duration in milliseconds.
        
        Args:
            parsed_sequence: Parsed sequence from parse()
            
        Returns:
            Suggested frame duration in ms
        """
        num_sequences = len(parsed_sequence['sequences'])
        
        # More sequences = slightly faster frames for smooth transitions
        if num_sequences > 3:
            return 60
        elif num_sequences > 1:
            return 70
        else:
            return 80
