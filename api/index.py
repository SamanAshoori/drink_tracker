import os
import sys

# Get the directory of the current file (api/index.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the backend folder
backend_dir = os.path.join(current_dir, '..', 'backend')

# Add it to the system path if it's not already there
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from main import app