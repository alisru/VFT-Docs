#!/usr/bin/env python3
"""
network_relaxation_algebra.py — Inertial Price Flow & Closed Circular Network Value Conservation
for Infinitesimal Reality Math (IRM Division 1: Pure Mathematics & Division 2: Value Physics).

Ground-Up Mathematical Innovations:
1. The Inertial Process Price Flow Equation:
   Replaces unphysical instantaneous market clearing with smooth relaxation dynamics:
       τ · dV_P/dt + V_P(t) = V_target(t)
   Guarantees strictly bounded velocity |ΔV_P / Δt| <= |V_target - V_P| / τ under acute shocks,
   eliminating delta-spike derivative singularities while preserving anti-chattering stability.
2. The Process Conservation of Value Theorem (Closed Circular Economic Network):
   Proves that in an interdependent circular network of N nodes across the 7 Interrogative Planes
   (Q1: Agency, Q2: Substance, Q3: Purpose, Q4: Process, Q5: Locality, Q6: Temporality, Q7: Selection),
   bilateral exchange executed via Process Atoms P_ij = <T_ij, R_ij, O_ij> strictly conserves
   total network endowment:
       ∑_{k=1}^N W_k(t_M) == ∑_{k=1}^N W_k(t_0)
   with zero drift, zero credit leakage, and zero non-conservative dissipation.
3. Finite Capacity Collapse & Shortage Stress Containment:
   Under supply disruptions (K_j -> 0), regularized non-Archimedean division caps manifest prices
   at the saturation wall A6 = 2, while shunting unmanifested shortage pressure into the
   overflow stress register O_ij > 0, generating a quantifiable quadratic social penalty
   Stress²(P_ij) = (V_price - 1)² - 1, preventing runaway hyper-inflation.

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-17
"""

import math
from fractions import Fraction
import sys
import os

# Ensure paths can resolve base modules
sys.path.insert(0, '/working_dir/c_0bfea5aee3b42ab1/downloads')
sys.path.insert(0, '/working_dir/c_0bfea5aee3b42ab1')

import lattice_process_algebra as lpa
import trajectory_price_algebra as tpa

ProcessAtom = lpa.ProcessAtom
DiscreteLattice7 = lpa.DiscreteLattice7
ProcessVector7 = lpa.ProcessVector7
ProcessMatrix7x7 = lpa.ProcessMatrix7x7
ContinuousToDiscreteProjector = tpa.ContinuousToDiscreteProjector
ProcessUniversalPriceEquation = tpa.ProcessUniversalPriceEquation


class InertialPriceFlow:
    """
    Implements the Inertial Price Flow differential relaxation equation:
    τ · dV/dt + V = V_target
    Discretized as:
    V(t + dt) = V(t) + (dt / (τ + dt)) · (V_target - V(t))
    """
    def __init__(self, tau=Fraction(1, 1), dt=Fraction(1, 10), eps_hys=Fraction(1, 2 * 10**9)):
        self.tau = Fraction(tau)
        self.dt = Fraction(dt)
        self.v_current = Fraction(1, 1) # default starting at Unit Parity A3=1
        self.projector = ContinuousToDiscreteProjector(eps_hys=eps_hys)

    def step(self, v_target):
        """Advances the relaxation flow by dt towards v_target, returning the projected ProcessAtom."""
        v_target = Fraction(v_target)
        factor = self.dt / (self.tau + self.dt)
        delta = factor * (v_target - self.v_current)
        self.v_current += delta
        atom = self.projector.project_step(self.v_current)
        return {
            'v_current': self.v_current,
            'velocity': delta / self.dt,
            'atom': atom,
            'anchor': atom.anchor_name,
            'overflow': atom.O,
            'quadratic_stress': atom.quadratic_stress()
        }


class NetworkNode:
    """
    Represents an economic node corresponding to one of the 7 Interrogative Planes:
    0: Q1 (Agency / Labor), 1: Q2 (Substance / Materials), 2: Q3 (Purpose / R&D),
    3: Q4 (Process / Manufacturing), 4: Q5 (Locality / Logistics),
    5: Q6 (Temporality / Maintenance), 6: Q7 (Selection / Quality & Allocation).
    """
    PLANE_NAMES = ("Q1:Agency", "Q2:Substance", "Q3:Purpose", "Q4:Process", "Q5:Locality", "Q6:Temporality", "Q7:Selection")

    def __init__(self, node_id, initial_endowment=Fraction(100, 1), capacity=Fraction(1, 1)):
        self.node_id = node_id
        self.name = self.PLANE_NAMES[node_id % 7]
        self.endowment = Fraction(initial_endowment)
        self.capacity = Fraction(capacity)
        self.demand = Fraction(1, 1)


class CircularProcessNetwork:
    """
    A closed, circular economic network of 7 Interrogative Nodes.
    Enforces exact Process Conservation of Value across bilateral transactions.
    """
    def __init__(self, initial_endowment_per_node=Fraction(100, 1), tau=Fraction(1, 1), dt=Fraction(1, 10)):
        self.nodes = [NetworkNode(i, initial_endowment_per_node) for i in range(7)]
        self.tau = Fraction(tau)
        self.dt = Fraction(dt)
        self.upe = ProcessUniversalPriceEquation()
        self.flows = {} # (buyer_id, seller_id) -> InertialPriceFlow
        self.initial_total_wealth = sum(node.endowment for node in self.nodes)
        self.total_transactions_count = 0
        self.total_shortage_stress = Fraction(0)

        for i in range(7):
            for j in range(7):
                if i != j:
                    self.flows[(i, j)] = InertialPriceFlow(tau=self.tau, dt=self.dt)

    @property
    def total_endowment(self):
        return sum(node.endowment for node in self.nodes)

    def execute_transaction(self, buyer_id, seller_id, cost_being=Fraction(1, 2)):
        """
        Executes a transaction where buyer_id purchases output from seller_id.
        Evaluates P-UPE target, applies inertial relaxation, projects onto ProcessAtom,
        and transfers valuation with strict conservation.
        """
        assert buyer_id != seller_id, "Buyer and seller must be distinct nodes"
        buyer = self.nodes[buyer_id]
        seller = self.nodes[seller_id]

        # 1. Evaluate Instantaneous P-UPE Equilibrium Valuation
        # Seller capacity K, buyer urgency D
        D_vec = ProcessVector7([buyer.demand if k == seller_id else Fraction(1, 2) for k in range(7)])
        K_vec = ProcessVector7([seller.capacity if k == seller_id else Fraction(1, 2) for k in range(7)])
        S_vec = ProcessVector7([Fraction(1, 7)] * 7)

        upe_res = self.upe.evaluate_price(cost_being, S_vec, D_vec, K_vec)
        v_target = upe_res['v_price']

        # 2. Advance Inertial Price Flow
        flow = self.flows[(buyer_id, seller_id)]
        flow_res = flow.step(v_target)
        price_atom = flow_res['atom']
        transfer_val = price_atom.value

        # 3. Solvency Check & Valuation Transfer
        # Actual transferred valuation is bounded by buyer endowment
        actual_transfer = min(buyer.endowment, transfer_val)

        buyer.endowment -= actual_transfer
        seller.endowment += actual_transfer

        self.total_transactions_count += 1
        self.total_shortage_stress += flow_res['quadratic_stress']

        return {
            'buyer_id': buyer_id,
            'seller_id': seller_id,
            'transfer_val': actual_transfer,
            'price_atom': price_atom,
            'manifest_anchor': price_atom.anchor_name,
            'overflow_stress': price_atom.O,
            'quadratic_penalty': flow_res['quadratic_stress'],
            'total_network_endowment': self.total_endowment,
            'is_conserved': (self.total_endowment == self.initial_total_wealth)
        }
