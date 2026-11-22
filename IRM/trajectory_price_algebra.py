#!/usr/bin/env python3
import math
from fractions import Fraction
import sys

sys.path.insert(0, '/working_dir/c_0bfea5aee3b42ab1')
import lattice_process_algebra as lpa

ProcessAtom = lpa.ProcessAtom
DiscreteLattice7 = lpa.DiscreteLattice7
ProcessVector7 = lpa.ProcessVector7
ProcessMatrix7x7 = lpa.ProcessMatrix7x7
ATOM_ZERO = lpa.ATOM_ZERO
ATOM_UNIT = lpa.ATOM_UNIT
ATOM_MAX = lpa.ATOM_MAX

class ContinuousToDiscreteProjector:
    def __init__(self, eps_hys=Fraction(1, 2 * 10**9)):
        self.eps_hys = Fraction(eps_hys)
        self.current_k = 0
        self.current_T = Fraction(0)
        self.transition_history = []

    def project_step(self, V):
        V = Fraction(V)
        if V <= 0:
            new_k = 0
            new_T = Fraction(0)
            new_R = Fraction(0)
            new_O = V
        elif V >= 2:
            new_k = 6
            new_T = Fraction(2)
            new_R = Fraction(0)
            new_O = V - Fraction(2)
        else:
            k = self.current_k
            if k < 6:
                b_up = Fraction(2 * k + 1, 6)
                if V >= b_up + self.eps_hys:
                    k = math.floor(3 * V + Fraction(1, 2))
                    k = max(0, min(6, k))
            if k > 0:
                b_down = Fraction(2 * k - 1, 6)
                if V <= b_down - self.eps_hys:
                    k = math.floor(3 * V + Fraction(1, 2))
                    k = max(0, min(6, k))

            new_k = k
            new_T = Fraction(k, 3)
            new_R = V - new_T
            new_O = Fraction(0)

        transition_occurred = (new_k != self.current_k)
        if transition_occurred:
            self.transition_history.append({
                'from_k': self.current_k,
                'to_k': new_k,
                'val': V,
                'from_T': self.current_T,
                'to_T': new_T
            })
            self.current_k = new_k
            self.current_T = new_T

        return ProcessAtom(new_T, new_R, new_O)

    def discretize_trajectory(self, trajectory):
        return [self.project_step(v) for v in trajectory]

class ProcessUniversalPriceEquation:
    def __init__(self, eps_floor=Fraction(1, 10**9)):
        self.eps_floor = Fraction(eps_floor)

    def evaluate_price(self, C_being, S_vector, D_vector, K_vector):
        if not isinstance(C_being, ProcessAtom):
            C_being = ProcessAtom.from_rational(C_being)

        lambdas = [
            d.div_regularized(k, self.eps_floor)
            for d, k in zip(D_vector.coords, K_vector.coords)
        ]
        lambda_vec = ProcessVector7(lambdas)
        sigma_scarcity = S_vector.inner_product(lambda_vec)
        v_price = C_being.value * (Fraction(1) + sigma_scarcity.value)
        price_atom = ProcessAtom.from_rational(v_price)

        return {
            'price_atom': price_atom,
            'v_price': v_price,
            'scarcity_strain': sigma_scarcity,
            'manifest_anchor': price_atom.anchor_name,
            'overflow_stress': price_atom.O,
            'quadratic_penalty': price_atom.quadratic_stress(),
            'is_saturated': (price_atom.T == Fraction(2) and price_atom.O > 0)
        }
