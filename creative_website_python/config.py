"""
Configuration constants for the portfolio website
Design system colors, shapes, and animation settings
All configuration is now in Python for server-side rendering
"""

# Brand color palette with opacity variations
COLORS = [
    'rgba(223, 0, 36, 0.4)',      # RED - #df0024
    'rgba(243, 195, 0, 0.4)',     # YELLOW - #f3c300
    'rgba(0, 171, 159, 0.4)',     # TEAL - #00ab9f
    'rgba(46, 109, 180, 0.4)'     # BLUE - #2e6db4
]

# Solid color versions for text
SOLID_COLORS = [
    'rgb(223, 0, 36)',      # RED
    'rgb(243, 195, 0)',     # YELLOW
    'rgb(0, 171, 159)',     # TEAL
    'rgb(46, 109, 180)'     # BLUE
]

# Available shape types
SHAPES = ['circle', 'square', 'triangle', 'x-shape']

# Portfolio sections data
SECTIONS = [
    {
        'id': 'terminal',
        'title': 'About',
        'type': 'terminal',
        'content': [
            'Nate Swenson',
            'Senior DevOps Engineer @ GoodLeap',
            'AI Enthusiast | Continuous Learner',
            'Author of DevOps Career Handbook'
        ]
    },
    {
        'id': 'resume',
        'title': 'Resume',
        'lines': ['...view my experience, recommendations, and download my resume'],
        'action': 'experience'
    },
    {
        'id': 'custom-vibez',
        'title': 'Custom Vibez',
        'lines': ['...get your custom engineered site or app'],
        'link': 'https://custom-vibez.com'
    },
    {
        'id': 'devops-career-handbook',
        'title': 'DevOps Career Handbook',
        'lines': ['...purchase a copy of my book on Amazon'],
        'action': 'book'
    },
    {
        'id': 'github',
        'title': 'GitHub',
        'lines': ['...view my contributions on GitHub'],
        'link': 'https://github.com/natejswenson'
    }
]

# Scroll configuration (for JavaScript)
SCROLL_CONFIG = {
    'THRESHOLD': 50,           # Pixels from edge to trigger loop
    'TRANSITION_DELAY': 50,    # ms delay after scroll reset
}

# Animation settings
ANIMATION = {
    'SCALE_MIN': 0.6,
    'SCALE_MAX': 1.0,
    'OPACITY_MIN': 0.3,
    'OPACITY_MAX': 1.0,
}

# Utility functions for server-side rendering
def get_deterministic_color_index(seed, index=0):
    """Generate deterministic color index from a seed string"""
    seed_hash = sum(ord(char) for char in seed)
    return abs(seed_hash * 13 + index * 17) % len(COLORS)

def get_deterministic_color(seed, index=0, solid=False):
    """Get deterministic color from seed"""
    color_index = get_deterministic_color_index(seed, index)
    colors = SOLID_COLORS if solid else COLORS
    return colors[color_index]

def get_shape_by_index(index):
    """Get shape name by index using rotation pattern"""
    return SHAPES[index % len(SHAPES)]

def create_looped_sections():
    """Create looped sections array for infinite scrolling"""
    return [SECTIONS[-1]] + SECTIONS + [SECTIONS[0]]
