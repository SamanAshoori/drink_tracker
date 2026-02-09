import sys
import os

# Add the backend directory to the system path so we can import main
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from main import app