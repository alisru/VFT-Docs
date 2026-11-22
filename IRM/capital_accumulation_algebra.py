#!/usr/bin/env python3
"""
capital_accumulation_algebra.py — 7-Plane Dynamic Process Capital Accumulation,
Discrete Wear Degradation, and HVNL Corridor Fatigue Mechanics
for Infinitesimal Reality Math (IRM Division 1: Pure Mathematics & Division 2: Value Physics).

Ground-Up Mathematical Innovations:
1. Multi-Plane Process Capital Stock (K ∈ P⁷):
   Represents capital assets across the 7 Interrogative Planes:
   Q1: Human Skill/Labor Capacity, Q2: Physical Infrastructure/Equipment,
   Q3: Intellectual Capital/Design, Q4: Tooling & Machine Throughput,
   Q5: Spatial Freight Fleet & Vehicles, Q6: Maintenance Buffers & Scheduling,
   Q7: Governance Protocols & Quality Standards.
   Each capital stock is a Bounded Process Atom K_i = <T_i, R_i, O_i> in [0, 2].
2. Discrete Wear-and-Tear (Depreciation) Mechanics:
   Depreciation is continuous micro-strain accumulated in the active signed residue R_i.
   When residue strain breaches the boundary threshold (R_i < -1/6), a Discrete Quantum
   Degradation Step triggers:
       T_i <- T_i - 1/3,   R_i <- R_i + 1/3
   conserving continuous valuation identically (ΔT + ΔR == 0).
   If capital degrades to A0=0, further wear pushes into negative overflow stress O_i < 0 (capital failure).
3. Overcapacity & Hoarding Stress:
   Excessive reinvestment beyond the saturation wall A6=2 is trapped in overflow stress O_i > 0,
   generating a quadratic social penalty Stress²(K_i) = (V - 1)² - 1 that discourages capital hoarding.
4. HVNL Corridor Driver Fatigue & Rest Break Coupling:
   Models freight transit along the Dubbo-Gilgandra-Coonabarabran corridor (Newell/Oxley Highways).
   Driving distance incurs fatigue strain on driver capacity K_0. Mandatory HVNL rest break staging
   at Gilgandra restores residue phase, preventing safety grade collapse to degraded states.

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-20
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
import network_relaxation_algebra as nra

ProcessAtom = lpa.ProcessAtom
DiscreteLattice7 = lpa.DiscreteLattice7
ProcessVector7 = lpa.ProcessVector7
ContinuousToDiscreteProjector = tpa.ContinuousToDiscreteProjector


class ProcessCapitalStock:
    """
    Manages the 7-Vector of Process Atoms representing capital stock K ∈ P⁷.
    """
    PLANE_NAMES = (
        "Q1:HumanSkill", "Q2:Infrastructure", "Q3:DesignIP",
        "Q4:MachineTooling", "Q5:SpatialFleet", "Q6:MaintenanceBuffer",
        "Q7:GovernanceQuality"
    )

    def __init__(self, initial_grades=None):
        if initial_grades is None:
            # Default start at Unit Parity A3=1.0 for all 7 planes
            self._stocks = [ProcessAtom.from_rational(1) for _ in range(7)]
        else:
            self._stocks = [ProcessAtom.from_rational(g) for g in initial_grades]
        self.degradation_events = []

    def __getitem__(self, idx):
        return self._stocks[idx]

    @property
    def stocks(self):
        return self._stocks

    @property
    def total_valuation(self):
        return sum(s.value for s in self._stocks)

    def apply_wear_and_investment(self, wear_vector, investment_vector):
        """
        Applies wear strain W_i and capital investment I_i across all 7 planes.
        Returns the updated stocks and records degradation/upgrade events.
        """
        new_stocks = []
        events = []
        for i in range(7):
            w = Fraction(wear_vector[i])
            inv = Fraction(investment_vector[i])
            old_atom = self._stocks[i]
            # Net valuation update: V_new = V_old + inv - w
            v_new = old_atom.value + inv - w
            new_atom = ProcessAtom.from_rational(v_new)

            if new_atom.T != old_atom.T:
                event_type = "UPGRADE" if new_atom.T > old_atom.T else "DEGRADATION"
                evt = {
                    'plane': i,
                    'plane_name': self.PLANE_NAMES[i],
                    'type': event_type,
                    'from_anchor': old_atom.anchor_name,
                    'to_anchor': new_atom.anchor_name,
                    'v_new': v_new
                }
                events.append(evt)
                self.degradation_events.append(evt)

            new_stocks.append(new_atom)

        self._stocks = new_stocks
        return new_stocks, events


class HVNLFreightCorridorModel:
    """
    Models Heavy Vehicle National Law (HVNL) freight transit along the
    Dubbo -> Gilgandra -> Coonabarabran corridor (160 km total).
    Tracks driver human capacity (K_0) and vehicle spatial stock (K_4).
    """
    def __init__(self, fatigue_per_km=Fraction(1, 800), vehicle_wear_per_km=Fraction(1, 1200)):
        self.fatigue_rate = Fraction(fatigue_per_km)
        self.vehicle_wear_rate = Fraction(vehicle_wear_per_km)
        # Corridor segments
        self.SEGMENT_DUBBO_GILGANDRA = 65 # km
        self.SEGMENT_GILGANDRA_COONA = 95 # km

    def simulate_trip(self, driver_initial=1, vehicle_initial=1, take_gilgandra_rest=True):
        """
        Simulates freight transit from Dubbo to Coonabarabran.
        If take_gilgandra_rest is True, driver takes mandatory 15-min rest at Gilgandra,
        restoring +1/15 in capacity valuation.
        Returns leg-by-leg state tracking.
        """
        driver = ProcessAtom.from_rational(driver_initial)
        vehicle = ProcessAtom.from_rational(vehicle_initial)

        legs = []

        # Leg 1: Dubbo to Gilgandra (65 km)
        f1 = self.fatigue_rate * self.SEGMENT_DUBBO_GILGANDRA
        w1 = self.vehicle_wear_rate * self.SEGMENT_DUBBO_GILGANDRA
        driver_v1 = driver.value - f1
        vehicle_v1 = vehicle.value - w1
        driver_atom1 = ProcessAtom.from_rational(driver_v1)
        vehicle_atom1 = ProcessAtom.from_rational(vehicle_v1)

        legs.append({
            'waypoint': 'Gilgandra Arrival',
            'km': 65,
            'driver': driver_atom1,
            'vehicle': vehicle_atom1
        })

        # Rest break staging at Gilgandra
        driver_v_post_rest = driver_v1
        if take_gilgandra_rest:
            # 15 min rest staging restores 1/10 valuation
            driver_v_post_rest += Fraction(1, 10)

        driver_atom_rest = ProcessAtom.from_rational(driver_v_post_rest)
        legs.append({
            'waypoint': 'Gilgandra Staging (Post-Break)',
            'km': 65,
            'driver': driver_atom_rest,
            'vehicle': vehicle_atom1
        })

        # Leg 2: Gilgandra to Coonabarabran (95 km)
        f2 = self.fatigue_rate * self.SEGMENT_GILGANDRA_COONA
        w2 = self.vehicle_wear_rate * self.SEGMENT_GILGANDRA_COONA
        driver_v2 = driver_v_post_rest - f2
        vehicle_v2 = vehicle_v1 - w2
        driver_atom2 = ProcessAtom.from_rational(driver_v2)
        vehicle_atom2 = ProcessAtom.from_rational(vehicle_v2)

        legs.append({
            'waypoint': 'Coonabarabran Arrival',
            'km': 160,
            'driver': driver_atom2,
            'vehicle': vehicle_atom2
        })

        return {
            'took_rest': take_gilgandra_rest,
            'legs': legs,
            'final_driver_anchor': driver_atom2.anchor_name,
            'final_vehicle_anchor': vehicle_atom2.anchor_name,
            'driver_avoided_degradation': (driver_atom2.T >= Fraction(1)) # preserved >= A3
        }
