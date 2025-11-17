"""
Flask application for the portfolio website
Server-side rendering with Python - minimal JavaScript
"""
from flask import Flask, render_template, send_from_directory, make_response
from flask_compress import Compress
import os
import json
from datetime import datetime, timedelta
from config import (
    SECTIONS, SCROLL_CONFIG, ANIMATION,
    create_looped_sections, get_deterministic_color, get_shape_by_index
)

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# Enable compression (gzip and brotli)
app.config['COMPRESS_MIMETYPES'] = [
    'text/html',
    'text/css',
    'text/javascript',
    'application/javascript',
    'application/json'
]
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500
Compress(app)

@app.route('/')
def index():
    """Main portfolio page with server-side rendering"""
    # Create looped sections for infinite scroll
    looped_sections = create_looped_sections()

    # Enrich each section with its color and shape (server-side)
    enriched_sections = []
    for idx, section in enumerate(looped_sections):
        section_key = f"{section['id']}-{idx}"
        section_copy = section.copy()
        section_copy['color'] = get_deterministic_color(section_key, idx)
        section_copy['shape'] = get_shape_by_index(idx)
        section_copy['index'] = idx
        # Only add ID for actual sections (not clones)
        section_copy['use_id'] = idx > 0 and idx <= len(SECTIONS)
        enriched_sections.append(section_copy)

    # Render template with all data
    response = make_response(render_template(
        'index.html',
        sections=enriched_sections,
        original_sections=SECTIONS,
        scroll_config=json.dumps(SCROLL_CONFIG),
        animation_config=json.dumps(ANIMATION)
    ))

    # Cache for 1 hour in production, no cache in debug
    if not app.debug:
        expires = datetime.now() + timedelta(hours=1)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')

    return response

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files with aggressive caching"""
    response = send_from_directory('static', path)

    # Cache static files for 1 year in production
    if not app.debug:
        expires = datetime.now() + timedelta(days=365)
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')

    return response

@app.after_request
def add_security_headers(response):
    """Add security and performance headers"""
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Performance hints
    response.headers['X-DNS-Prefetch-Control'] = 'on'

    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
