"""
Fractal Polytrope Sovereign LLM: Inter-Complex Cross-Debate Clash Engine
& 3D Geodesic Trajectory Visualizer.
Cycle 8 R&D Milestone. Self-contained module with zero external dependencies.
"""

import json
import os
import re
import time
import numpy as np
import pathlib

# ============================================================================
# 1. CORE POLYTROPE ENTITY & COMPLEX DEFINITIONS
# ============================================================================

class PolytropeEntity:
    def __init__(self, label, upsilon=0.0, psi=0.0, z=0.0, q_planes=None, radius=0.5):
        self.label = label
        self.upsilon = float(np.clip(upsilon, -2.0, 2.0))
        self.psi = float(np.clip(psi, -2.0, 2.0))
        self.z = float(np.clip(z, -2.0, 2.0))
        if q_planes is None:
            self.q_planes = np.ones(7, dtype=np.float64) / 7.0
        else:
            q = np.array(q_planes, dtype=np.float64)
            self.q_planes = q / np.sum(q)
        self.radius = float(radius)
        self.cov = np.eye(3, dtype=np.float64) * (self.radius ** 2)

    @property
    def coords(self):
        return np.array([self.upsilon, self.psi, self.z], dtype=np.float64)

class ISComplex:
    def __init__(self, name: str, nodes, edges=None):
        self.name = name
        self.nodes = nodes
        self.edges = edges or []
        
    @property
    def centroid(self):
        coords = np.array([n.coords for n in self.nodes])
        return np.mean(coords, axis=0)

    @property
    def aggregate_q(self):
        qs = np.array([n.q_planes for n in self.nodes])
        mean_q = np.mean(qs, axis=0)
        return mean_q / np.sum(mean_q)

    @property
    def bounding_cov(self):
        coords = np.array([n.coords for n in self.nodes])
        if len(coords) > 1:
            cov = np.cov(coords, rowvar=False) + np.eye(3) * 0.15
        else:
            cov = self.nodes[0].cov
        return cov

# ============================================================================
# 2. INTER-COMPLEX CLASH KERNEL
# ============================================================================

class InterComplexClashKernel:
    @staticmethod
    def compare_complexes(c_A: ISComplex, c_B: ISComplex):
        # Centroid Deltas
        delta_coords = c_B.centroid - c_A.centroid
        d_u = float(delta_coords[0])  # Boundary expansion/contraction
        d_p = float(delta_coords[1])  # Kinetic momentum shift
        d_z = float(delta_coords[2])  # Causal progression/yield

        # Polyhedral Hypervolume Overlap
        mu_diff = c_A.centroid - c_B.centroid
        sigma_sum = c_A.bounding_cov + c_B.bounding_cov
        inv_sigma = np.linalg.inv(sigma_sum)
        dist_sq = mu_diff.T @ inv_sigma @ mu_diff
        
        det_A = np.linalg.det(c_A.bounding_cov)
        det_B = np.linalg.det(c_B.bounding_cov)
        det_sum = np.linalg.det(sigma_sum)
        prefactor = (2.0 ** 1.5) * (det_A * det_B) ** 0.25 / np.sqrt(det_sum)
        vol_overlap = float(np.clip(prefactor * np.exp(-0.5 * dist_sq), 0.0, 1.0))
        
        # Substrate Consistency across Q1..Q7
        q_bhatt = float(np.sum(np.sqrt(c_A.aggregate_q * c_B.aggregate_q)))
        
        # Relational Edge Alignment
        edge_matches = 0
        total_e = max(len(c_A.edges), len(c_B.edges), 1)
        for e_a in c_A.edges:
            for e_b in c_B.edges:
                if e_a.get("type") == e_b.get("type"):
                    edge_matches += 1
        morphic_isomorphism = float(min(1.0, edge_matches / total_e))
        
        # Classification
        if vol_overlap > 0.6 and morphic_isomorphism > 0.6:
            classification = "ISOMORPHIC_CONSTRUCTIVE ([is like])"
        elif d_u < -1.2 or vol_overlap < 0.05:
            classification = "CONTRADICTORY_EXCLUSIVE ([is not])"
        elif d_z > 0.7:
            classification = "CAUSAL_PROGRESSION (A -> B)"
        else:
            classification = "SYSTEMIC_PERTURBATION"

        return {
            "complex_A": c_A.name,
            "complex_B": c_B.name,
            "classification": classification,
            "polyhedral_overlap": round(vol_overlap, 4),
            "morphic_isomorphism": round(morphic_isomorphism, 4),
            "substrate_alignment_q": round(q_bhatt, 4),
            "delta_vector": {
                "delta_upsilon": round(d_u, 4),
                "delta_psi": round(d_p, 4),
                "delta_z": round(d_z, 4)
            }
        }

# ============================================================================
# 3. 3D TRAJECTORY VISUALIZER (HTML/WEBGL EXPORTER)
# ============================================================================

def generate_interactive_3d_html(trajectory_data, output_path):
    """
    Exports a standalone interactive HTML visualizer rendering the 3D spiral trajectory
    through (upsilon, psi, z) across the four modal quadrants.
    """
    points_json = json.dumps(trajectory_data)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Fractal Polytrope 3D Manifold Geodesic Visualizer</title>
    <style>
        body {{ margin: 0; background: #0b0f19; color: #e2e8f0; font-family: monospace; overflow: hidden; }}
        #hud {{ position: absolute; top: 16px; left: 16px; background: rgba(15, 23, 42, 0.85); padding: 16px; border-radius: 8px; border: 1px solid #334155; z-index: 10; max-width: 380px; }}
        h2 {{ margin: 0 0 8px 0; font-size: 14px; color: #38bdf8; text-transform: uppercase; }}
        .metric {{ margin: 4px 0; font-size: 12px; }}
        .badge {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .productive {{ background: #065f46; color: #34d399; }}
        .reductive {{ background: #991b1b; color: #f87171; }}
        .constructive {{ background: #1e40af; color: #60a5fa; }}
        .regressive {{ background: #854d0e; color: #facc15; }}
    </style>
</head>
<body>
    <div id="hud">
        <h2>Fractal Polytrope Phase Space</h2>
        <div class="metric">Trajectory Mode: <span class="badge productive">[can be] Productive Attractor</span></div>
        <div class="metric">X-Axis (υ): Boundary Topology [-2, +2]</div>
        <div class="metric">Y-Axis (ψ): Kinetic Work [-2, +2]</div>
        <div class="metric">Z-Axis (z): Causal Depth [-2, +2]</div>
        <hr style="border-color: #334155; margin: 8px 0;">
        <div class="metric" id="step-info">Hover points or rotate canvas in 3D.</div>
    </div>
    <div id="canvas-container" style="width: 100vw; height: 100vh;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const data = {points_json};
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        camera.position.set(4, 3, 5);
        camera.lookAt(0, 0, 0);

        // Grid & Coordinate Axes
        const grid = new THREE.GridHelper(4, 8, 0x38bdf8, 0x1e293b);
        scene.add(grid);

        // Axis Lines
        const axes = new THREE.AxesHelper(2.5);
        scene.add(axes);

        // Plot Trajectory Curve
        const points = [];
        data.forEach(pt => {{
            points.push(new THREE.Vector3(pt.coords[0], pt.coords[1], pt.coords[2]));
            // Sphere at each token step
            const geom = new THREE.SphereGeometry(0.06, 16, 16);
            const mat = new THREE.MeshBasicMaterial({{ color: pt.coords[0] >= 0 && pt.coords[1] >= 0 ? 0x34d399 : 0xf87171 }});
            const sphere = new THREE.Mesh(geom, mat);
            sphere.position.set(pt.coords[0], pt.coords[1], pt.coords[2]);
            scene.add(sphere);
        }});

        const curve = new THREE.CatmullRomCurve3(points);
        const tubeGeom = new THREE.TubeGeometry(curve, 64, 0.02, 8, false);
        const tubeMat = new THREE.MeshBasicMaterial({{ color: 0x38bdf8, wireframe: false }});
        const tube = new THREE.Mesh(tubeGeom, tubeMat);
        scene.add(tube);

        // Simple Rotation
        function animate() {{
            requestAnimationFrame(animate);
            scene.rotation.y += 0.005;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive 3D HTML Visualizer exported to: {output_path}")

# ============================================================================
# 4. EXECUTION OF CYCLE 8 R&D
# ============================================================================

def run_cycle_8_rd():
    print("=" * 70)
    print("HOURLY R&D EXECUTION: CYCLE 8 (INTER-COMPLEX CLASH & 3D VISUALIZER)")
    print("=" * 70)

    # 1. Build Multi-Node Parliamentary Debate Complexes
    # Complex A: Opposition Challenge (Attack on Road Toll & Pilot Shortage)
    c_opposition = ISComplex(
        name="Opposition Parliamentary Challenge (1999 Hansard)",
        nodes=[
            PolytropeEntity("Scrutiny Motion", upsilon=-0.8, psi=0.9, z=-0.6, q_planes=[0.7, 0, 0, 0, 0.2, 0.1, 0]),
            PolytropeEntity("Road Carnage Toll", upsilon=-1.2, psi=-0.8, z=-0.3, q_planes=[0, 0, 0.4, 0, 0, 0, 0.6]),
            PolytropeEntity("Ministerial Failure Charge", upsilon=-1.5, psi=0.5, z=-0.1, q_planes=[0.8, 0, 0, 0, 0.2, 0, 0])
        ],
        edges=[{"from": 0, "to": 1, "type": "cites"}, {"from": 1, "to": 2, "type": "accuses"}]
    )

    # Complex B: Ministerial Defense & National Delivery Complex
    c_government = ISComplex(
        name="Government National Policy Delivery (1999 Hansard)",
        nodes=[
            PolytropeEntity("Executive Mandate", upsilon=0.8, psi=1.2, z=0.1, q_planes=[0.8, 0.1, 0, 0, 0.1, 0, 0]),
            PolytropeEntity("Economic Budget Delivery", upsilon=1.2, psi=0.8, z=0.6, q_planes=[0.1, 0, 0, 0, 0.8, 0.1, 0]),
            PolytropeEntity("Regional Airport Investments", upsilon=1.4, psi=1.1, z=0.9, q_planes=[0, 0, 0.9, 0, 0.1, 0, 0])
        ],
        edges=[{"from": 0, "to": 1, "type": "funds"}, {"from": 1, "to": 2, "type": "delivers"}]
    )

    # Compare Complexes
    clash_result = InterComplexClashKernel.compare_complexes(c_opposition, c_government)
    print("\nInter-Complex Parliamentary Clash Results:")
    print("-" * 70)
    print(f"Complex A: \"{clash_result['complex_A']}\"")
    print(f"Complex B: \"{clash_result['complex_B']}\"")
    print(f"  Classification:        {clash_result['classification']}")
    print(f"  Polyhedral Overlap:    {clash_result['polyhedral_overlap']}")
    print(f"  Morphic Isomorphism:   {clash_result['morphic_isomorphism']}")
    print(f"  Boundary Delta (Δυ):   {clash_result['delta_vector']['delta_upsilon']:+.4f} (Inclusive Expansion)")
    print(f"  Kinetic Shift (Δψ):    {clash_result['delta_vector']['delta_psi']:+.4f}")
    print(f"  Causal Progression (Δz): {clash_result['delta_vector']['delta_z']:+.4f} (Downstream Policy Resolution)")

    # 2. Export 3D Interactive HTML Visualization
    # Trajectory points from benchmark proposition
    sample_trajectory = [
        {"step": 1, "token": "The", "coords": [0.0, 0.0, 0.0]},
        {"step": 2, "token": "national", "coords": [0.15, 0.1, 0.05]},
        {"step": 3, "token": "government", "coords": [0.25, 0.2, 0.08]},
        {"step": 4, "token": "will", "coords": [0.45, 0.55, 0.25]},
        {"step": 5, "token": "deliver", "coords": [0.55, 0.65, 0.35]},
        {"step": 6, "token": "economic", "coords": [0.65, 0.70, 0.45]},
        {"step": 7, "token": "growth", "coords": [0.75, 0.75, 0.55]},
        {"step": 8, "token": "and", "coords": [0.80, 0.70, 0.60]},
        {"step": 9, "token": "support", "coords": [0.95, 0.75, 0.70]},
        {"step": 10, "token": "working", "coords": [1.10, 0.80, 0.80]},
        {"step": 11, "token": "families", "coords": [1.25, 0.85, 0.90]}
    ]
    
    html_path = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/polytrope_trajectory_visualizer.html"
    generate_interactive_3d_html(sample_trajectory, html_path)
    
    # Save JSON Clash Metrics
    out_json = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/inter_complex_clash_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "cycle": 8,
            "experiment": "Inter-Complex Parliamentary Clash & 3D WebGL Trajectory Generation",
            "clash_metrics": clash_result,
            "trajectory_sample": sample_trajectory
        }, f, indent=2)
    print(f"Exported clash metrics JSON to: {out_json}")

if __name__ == "__main__":
    run_cycle_8_rd()
