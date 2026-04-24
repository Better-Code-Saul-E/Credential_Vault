import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)

from vault.app import run

if __name__ == "__main__":
    run()