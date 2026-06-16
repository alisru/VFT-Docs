import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from actor_extract import extract_actors
print("The Trump administration response ->", extract_actors("The Trump administration response"))
print("Trump's response ->", extract_actors("Trump's response"))
