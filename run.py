import logging
from esp32api import app

if __name__ == '__main__':
    try:
        app.run(debug=False, host="0.0.0.0", port=5001, use_reloader=False)
    finally:
        logging.debug('After app.run')
