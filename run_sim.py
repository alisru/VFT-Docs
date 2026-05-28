import sys
sys.path.append('.')
try:
    import simulate_homogeneous_scope
    print("Script simulates without crash.")
except Exception as e:
    print(e)
