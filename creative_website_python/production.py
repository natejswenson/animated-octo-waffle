"""
Production configuration for the Flask application
Uses gunicorn for better performance
"""
from app import app
import os

# Production settings
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Logging configuration
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/portfolio.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Portfolio website startup')

if __name__ == '__main__':
    # For production, use: gunicorn -w 4 -b 0.0.0.0:8000 production:app
    app.run(host='0.0.0.0', port=8000)
