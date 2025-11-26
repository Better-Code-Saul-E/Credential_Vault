import sys
import os

# Add the src folder to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)

# Import from YOUR app.py
from vault.app import run

if __name__ == "__main__":
    run()