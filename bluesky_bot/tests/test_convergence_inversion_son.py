import unittest
import numpy as np

def calculate_son_coordinates(gg_son, ge_son, lg_son, le_son):
    # Attractor definitions
    A = {
        'GG': np.array([1.0, 1.0]),
        'GE': np.array([-1.0, -1.0]),
        'LG': np.array([1.0, -1.0]),
        'LE': np.array([-1.0, 1.0])
    }
    
    # Orthogonal definitions A_perp = (-psi, u)
    A_perp = {
        'GG': np.array([-1.0, 1.0]),
        'GE': np.array([1.0, -1.0]),
        'LG': np.array([1.0, 1.0]),
        'LE': np.array([-1.0, -1.0])
    }
    
    son = {
        'GG': gg_son,
        'GE': ge_son,
        'LG': lg_son,
        'LE': le_son
    }
    
    total_force = np.zeros(2)
    total_weight = 0.0
    
    for key in A:
        s, o, n = son[key]
        force = s * A[key] - o * A[key] + n * A_perp[key]
        total_force += force
        total_weight += (s + o + n)
        
    if total_weight == 0:
        return 0.0, 0.0
        
    coord = total_force / total_weight
    return coord[0], coord[1]

class TestConvergenceInversionSON(unittest.TestCase):
    def test_coopted_case(self):
        # Case 1: Co-opted (Supports the Greater Evil / bad frame)
        gg_son = (0.1, 0.8, 0.1)
        ge_son = (0.8, 0.1, 0.1)
        lg_son = (0.2, 0.2, 0.2)
        le_son = (0.2, 0.2, 0.2)
        
        u, psi = calculate_son_coordinates(gg_son, ge_son, lg_son, le_son)
        print(f"\n[CO-OPTED CASE] Calculated Coordinates: u={u:+.3f}, psi={psi:+.3f}")
        
        # We expect u < 0 (pulled to negative morality by supporting Greater Evil)
        self.assertTrue(u < 0)
        
    def test_subversive_case(self):
        # Case 2: Subversive (Opposes the Greater Evil / bad frame)
        gg_son = (0.8, 0.1, 0.1)
        ge_son = (0.1, 0.9, 0.0)
        lg_son = (0.2, 0.2, 0.2)
        le_son = (0.2, 0.2, 0.2)
        
        u, psi = calculate_son_coordinates(gg_son, ge_son, lg_son, le_son)
        print(f"[SUBVERSIVE CASE] Calculated Coordinates: u={u:+.3f}, psi={psi:+.3f}")
        
        # We expect u > 0 (pushed to positive morality by opposing Greater Evil)
        self.assertTrue(u > 0)

if __name__ == "__main__":
    unittest.main()
