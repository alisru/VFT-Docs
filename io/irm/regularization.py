#!/usr/bin/env python3
"""
regularization.py - collision regularisation schemes, compared.

Companion to irm_engine.py. Written to settle one question raised in
CLAUDE_LOG.md Entry 001 (finding F-2):

    The IRM Cost of Being floor removes the r = 0 exception, but numerical
    breakdown in a head-on collapse begins ~34 decades ABOVE the floor, so the
    floor cannot be what regularises the collision. The archived document
    "Regularization of Point-Mass Collision Singularities (IRM vs Sundman and
    KS)" claims superiority over KS. Does that claim survive an actual KS?

Three schemes on the same physical problem:

  1. FLOOR      F = G m1 m2 / max(r, l_P)^2, fixed step in physical time.
                The Paper 8 s3.1 scheme.
  2. SOFTENED   Plummer: V = -k/sqrt(r^2 + e^2). Conservative by construction,
                non-singular, but F -> 0 at r = 0 rather than F -> F_max.
  3. LEVI-CIVITA  Regularisation by coordinate + time transformation:
                x = u^2 (complex), dt = r ds. The planar case of the
                Kustaanheimo-Stiefel transformation, which is what Sundman and
                KS actually do.

The Levi-Civita result is the point of the module. Under x = u^2, dt = r ds,
the Kepler equation of motion becomes

    u'' = (E/2) u                      (' = d/ds)

a LINEAR oscillator with constant coefficients, whose solution passes through
u = 0 -- i.e. through r = 0, the collision itself -- as a completely regular
point. The energy relation in regularised variables,

    2|u'|^2 - k = E |u|^2

is finite AT collision (it gives |u'|^2 = k/2 when u = 0). There is no
singularity left to floor.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from irm_engine import G_NEWTON, PLANCK_LENGTH


# --------------------------------------------------------------------------
# Analytic reference
# --------------------------------------------------------------------------
def radial_free_fall_time(d: float, k: float) -> float:
    """
    Exact time for two bodies released at rest, separation d, to collide.
    k = G(m1 + m2). t = (pi/2) sqrt(d^3 / (2k)).
    """
    return (math.pi / 2) * math.sqrt(d ** 3 / (2 * k))


# --------------------------------------------------------------------------
# Scheme 1 & 2: integration in physical time
# --------------------------------------------------------------------------
@dataclass
class PhysicalTimeResult:
    scheme: str
    steps: int
    dt: float
    t_final: float
    r_min: float
    energy_initial: float
    drift_max: float
    reached_floor: bool
    exception: Optional[str] = None


def _integrate_physical(accel: Callable[[float], float],
                        potential: Callable[[float], float],
                        r0: float, v0: float, k: float,
                        dt: float, steps: int,
                        scheme: str) -> PhysicalTimeResult:
    """
    Velocity Verlet on the 1-D relative radial coordinate.
    `accel(r)` returns d^2r/dt^2 (negative = attractive).
    Specific energy: E = v^2/2 + potential(r).
    """
    r, v = r0, v0
    e0 = 0.5 * v * v + potential(r)
    worst, r_min, hit_floor = 0.0, r0, False
    a = accel(r)
    t = 0.0
    try:
        for _ in range(steps):
            r = r + v * dt + 0.5 * a * dt * dt
            a_new = accel(r)
            v = v + 0.5 * (a + a_new) * dt
            a = a_new
            t += dt
            ar = abs(r)
            r_min = min(r_min, ar)
            if ar <= PLANCK_LENGTH:
                hit_floor = True
            e = 0.5 * v * v + potential(r)
            worst = max(worst, abs((e - e0) / e0))
    except (ZeroDivisionError, OverflowError, ValueError) as exc:
        return PhysicalTimeResult(scheme, steps, dt, t, r_min, e0, worst,
                                  hit_floor, f"{type(exc).__name__}: {exc}")
    return PhysicalTimeResult(scheme, steps, dt, t, r_min, e0, worst, hit_floor)


def run_floor(r0: float, k: float, dt: float, steps: int) -> PhysicalTimeResult:
    """Paper 8 s3.1: hard distance floor at the Planck length."""
    def accel(r: float) -> float:
        return -k / max(abs(r), PLANCK_LENGTH) ** 2 * (1.0 if r >= 0 else -1.0)

    def potential(r: float) -> float:
        return -k / max(abs(r), PLANCK_LENGTH)

    return _integrate_physical(accel, potential, r0, 0.0, k, dt, steps, "FLOOR")


def run_softened(r0: float, k: float, dt: float, steps: int,
                 eps: float = PLANCK_LENGTH) -> PhysicalTimeResult:
    """Plummer softening: conservative, non-singular, F -> 0 at r = 0."""
    def accel(r: float) -> float:
        return -k * r / (r * r + eps * eps) ** 1.5

    def potential(r: float) -> float:
        return -k / math.sqrt(r * r + eps * eps)

    return _integrate_physical(accel, potential, r0, 0.0, k, dt, steps,
                               "SOFTENED")


# --------------------------------------------------------------------------
# Scheme 3: Levi-Civita / KS regularisation
# --------------------------------------------------------------------------
@dataclass
class LeviCivitaResult:
    steps: int
    ds: float
    t_final: float
    t_at_closest: float
    r_min: float
    energy: float
    drift_max: float
    invariant_drift_max: float
    passed_through_collision: bool
    u_at_closest: Tuple[float, float]
    u_prime_sq_at_closest: float


def run_levi_civita(r0: float, k: float, ds: float,
                    steps: int) -> LeviCivitaResult:
    """
    Integrate the two-body problem in regularised coordinates.

    Complex u with x = u^2, r = |u|^2, dt = r ds.
    Equation of motion: u'' = (E/2) u, with E the conserved specific energy.
    Physical velocity: dx/dt = 2 u u' / |u|^2.

    Released at rest at separation r0 along the real axis, so u0 = sqrt(r0)
    and u0' = 0 (from the energy relation 2|u'|^2 - k = E|u|^2 with v = 0).
    """
    e_spec = -k / r0                      # v = 0 at release
    u_re, u_im = math.sqrt(r0), 0.0
    du_re, du_im = 0.0, 0.0

    half = e_spec / 2.0
    t = 0.0
    r_min = r0
    worst_e, worst_inv = 0.0, 0.0
    crossed = False
    u_closest = (u_re, u_im)
    dusq_closest = 0.0
    t_closest = 0.0
    prev_re = u_re

    # Leapfrog in fictitious time on u'' = (E/2) u.
    a_re, a_im = half * u_re, half * u_im
    for _ in range(steps):
        u_re += du_re * ds + 0.5 * a_re * ds * ds
        u_im += du_im * ds + 0.5 * a_im * ds * ds
        na_re, na_im = half * u_re, half * u_im
        du_re += 0.5 * (a_re + na_re) * ds
        du_im += 0.5 * (a_im + na_im) * ds
        a_re, a_im = na_re, na_im

        r = u_re * u_re + u_im * u_im     # r = |u|^2, always >= 0
        t += r * ds                       # dt = r ds
        du_sq = du_re * du_re + du_im * du_im

        if r < r_min:
            r_min = r
            u_closest = (u_re, u_im)
            dusq_closest = du_sq
            t_closest = t

        # Regularised invariant: 2|u'|^2 - k - E|u|^2 = 0. Finite everywhere,
        # including at u = 0, where it reduces to |u'|^2 = k/2.
        worst_inv = max(worst_inv, abs(2 * du_sq - k - e_spec * r) / k)

        # Physical energy is ill-conditioned near collision (KE and PE both
        # diverge and nearly cancel), so sample it only where the standard
        # form is numerically meaningful. The u-invariant above is the
        # regular measure and is valid everywhere including at u = 0.
        if r > 1e-3 * r0:
            vx_re = 2 * (u_re * du_re - u_im * du_im) / r
            vx_im = 2 * (u_re * du_im + u_im * du_re) / r
            e = 0.5 * (vx_re ** 2 + vx_im ** 2) - k / r
            worst_e = max(worst_e, abs((e - e_spec) / e_spec))

        if prev_re > 0 >= u_re:
            crossed = True
        prev_re = u_re

    return LeviCivitaResult(steps, ds, t, t_closest, r_min, e_spec, worst_e,
                            worst_inv, crossed, u_closest, dusq_closest)


# --------------------------------------------------------------------------
# Comparison harness
# --------------------------------------------------------------------------
def compare(m1: float = 1.0e10, m2: float = 1.0e10,
            d: float = 1.0) -> Dict[str, object]:
    k = G_NEWTON * (m1 + m2)
    t_coll = radial_free_fall_time(d, k)
    horizon = 1.5 * t_coll       # integrate past the collision

    rows: List[PhysicalTimeResult] = []
    for dt in (1e-3, 1e-4, 1e-5):
        rows.append(run_floor(d, k, dt, int(horizon / dt)))
    for dt in (1e-3, 1e-4, 1e-5):
        rows.append(run_softened(d, k, dt, int(horizon / dt)))
    for dt in (1e-3, 1e-4, 1e-5):
        r_ = run_softened(d, k, dt, int(horizon / dt), eps=1e-2 * d)
        r_.scheme = 'SOFT-1e-2'
        rows.append(r_)

    lc: List[LeviCivitaResult] = []
    # Collision sits at s = (pi/2)/sqrt(|E|/2); span comfortably past it.
    omega = math.sqrt(abs(k / d) / 2.0)
    s_coll = (math.pi / 2) / omega
    for n in (2000, 20000):
        lc.append(run_levi_civita(d, k, 1.5 * s_coll / n, n))

    return {"k": k, "t_collision": t_coll, "horizon": horizon,
            "s_collision": s_coll, "physical": rows, "levi_civita": lc}


def main() -> int:
    r = compare()
    k, t_coll = r["k"], r["t_collision"]
    w = 78
    print("=" * w)
    print("COLLISION REGULARISATION - FLOOR vs SOFTENING vs LEVI-CIVITA/KS")
    print("=" * w)
    print(f"\ntwo bodies, 1.0e10 kg each, released at rest, separation 1.000 m")
    print(f"k = G(m1+m2) = {k:.6f}")
    print(f"analytic collision time  t_c = {t_coll:.6f} s")
    print(f"integrated to 1.5 t_c    = {r['horizon']:.6f} s "
          f"(i.e. THROUGH the collision)")

    print("\n" + "-" * w)
    print("Integration in physical time")
    print("-" * w)
    print(f"{'scheme':<10} {'dt':>8} {'r_min (m)':>13} {'max drift':>12} "
          f"{'floor hit':>10}  note")
    for row in r["physical"]:
        note = row.exception or ""
        print(f"{row.scheme:<10} {row.dt:>8.0e} {row.r_min:>13.3e} "
              f"{row.drift_max:>12.3e} {str(row.reached_floor):>10}  {note}")

    print("\n" + "-" * w)
    print("Levi-Civita / KS regularisation (fictitious time, dt = r ds)")
    print("-" * w)
    for row in r["levi_civita"]:
        print(f"steps = {row.steps:>6}   ds = {row.ds:.3e}")
        print(f"   physical time at r_min   : {row.t_at_closest:.6f} s "
              f"(analytic t_c = {t_coll:.6f} s, "
              f"err {abs(row.t_at_closest - t_coll) / t_coll:.2e})")
        print(f"   physical time integrated : {row.t_final:.6f} s "
              f"(1.5 t_c of fictitious time)")
        print(f"   closest approach r_min   : {row.r_min:.3e} m")
        print(f"   passed through collision : {row.passed_through_collision}")
        print(f"   max drift, physical E    : {row.drift_max:.3e}  (r > 1e-3 r0 only)")
        print(f"   max drift, u-invariant   : {row.invariant_drift_max:.3e}")
        print(f"   at closest approach: u = ({row.u_at_closest[0]:+.3e}, "
              f"{row.u_at_closest[1]:+.3e}),  |u'|^2 = "
              f"{row.u_prime_sq_at_closest:.6f}  (k/2 = {k / 2:.6f})")
        print()

    print("=" * w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
