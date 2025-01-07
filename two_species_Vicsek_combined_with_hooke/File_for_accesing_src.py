import sys
import os

#This file makes it such that code from src can be accesed

# Get the absolute path to the 'src' directory
Vicsek_hooke_project1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(Vicsek_hooke_project1, 'src')

# Add the 'src' directory to sys.path
if src_path not in sys.path:
    sys.path.append(src_path)
