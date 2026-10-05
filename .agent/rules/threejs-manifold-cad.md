# 3D-Printable Three.js CAD Invariants (Manifold-3D vs. Slicer Repair)

When constructing or modifying parametric 3D models intended for additive manufacturing / slicing (STL, OBJ, 3MF) in Three.js, you MUST adhere to the following 5 topological and geometric invariants to prevent non-manifold defects and slicer hole-capping/repair bugs.

---

## 1. Kernel Selection: WASM Manifold Over Triangle-Clipping CSG
* **Mechanism**: Triangle-clipping CSG libraries (`three-bvh-csg`, `three-csg-ts`) retriangulate clipped triangles independently. A cut cap never topologically shares edges with the cylinder wall it meets. For example, `BoxGeometry − Cylinder` emits hundreds of triangles with open boundary edges where the cap faces are detached from the bore rim. Slicer repair engines (Netfabb, Bambu Studio, PrusaSlicer) identify these boundary loops as punctures in the outer shell and triangulate across them, closing/capping the bore.
* **Invariant**: Always use an exact 2-manifold CSG kernel (specifically `manifold-3d` via WebAssembly) for manufacturing models. In a 2-manifold mesh, every edge is shared by exactly two triangles with consistent orientation, resulting in 0 open boundary loops.
* **Degradation Policy**: If WASM fails to load or is uninitialized, you may fall back to `three-bvh-csg` for interactive on-screen previewing only, but log an explicit console warning that the geometry is not watertight for slicing.

---

## 2. Attribute Stripping: Position-Only Pre-Welding
* **Mechanism**: Three.js `mergeVertices` checks all vertex attributes. When normals or UVs exist, vertices along sharp edges (such as the 90° boundary of a cylindrical bore meeting a flat surface) possess distinct normal vectors and will never weld, leaving open seams.
* **Invariant**: Strip geometries to `position` only before running `mergeVertices`:
  ```javascript
  const src = geom.index ? geom.toNonIndexed() : geom;
  const posOnly = new THREE.BufferGeometry();
  posOnly.setAttribute('position', src.getAttribute('position').clone());

  const welded = mergeVertices(posOnly, 1e-4);
  const pos = welded.getAttribute('position');
  const idx = welded.getIndex();

  const mesh = new wasm.Mesh({
    numProp: 3,
    vertProperties: new Float32Array(pos.array),
    triVerts: idx ? new Uint32Array(idx.array) : new Uint32Array(Array.from({ length: pos.count }, (_, i) => i)),
  });
  ```
  Recompute normals (`geom.computeVertexNormals()`) and attach placeholder UVs *after* the manifold result is converted back into `BufferGeometry`.

---

## 3. Tessellation Invariant: Global Authoritative Bore Segments (`BORE_SEGMENTS`)
* **Mechanism**: When concentric or intersecting radial features are tessellated with mismatched segment counts (e.g. 48 vs 64 vs 96), their polygonal walls criss-cross. Any boolean difference or union between them generates a ring of degenerate sub-micron slivers and self-intersections that trigger slicer repair auto-capping.
* **Invariant**: Enforce a single global constant (e.g. `BORE_SEGMENTS = 96` or `curveSegments = 96`) across every circular element in the model:
  - `THREE.CylinderGeometry(r, r, h, BORE_SEGMENTS)`
  - `THREE.ExtrudeGeometry(shape, { curveSegments: BORE_SEGMENTS })`
  - 2D arcs: `path.absarc(x, y, r, 0, Math.PI * 2, true)`
  - `THREE.LatheGeometry(points, BORE_SEGMENTS)`
  - All CSG cutter brushes and pin cylinders.

---

## 4. Cut Accountability: Partitioned 2D Punch vs. 3D Drill
* **Mechanism**: Performing redundant cuts (cutting an aperture in 2D and then drilling it again in 3D) creates coincident, coplanar zero-volume faces.
* **Invariant**: Maintain a single authoritative `apertures` list with unique IDs, coordinates, and radii. Partition cuts strictly:
  1. **Native 2D Holes**: If an aperture is geometrically fully contained inside a shape (`Math.abs(lx) + r <= len / 2 && Math.abs(ly) + r <= w / 2`), punch it natively via `shape.holes.push(...)`. 2D shape extrusion is topologically watertight and produces 0 boundary edges.
  2. **CSG 3D Drills**: If an aperture overlaps boundaries, cuts across multiple intersecting elements, or is overhanging, track its ID in a `needsDrill` `Set`.
  3. Execute 3D CSG drilling in a single consolidated pass (`drillApertures(geom, needsDrill)`) using cutters matching `BORE_SEGMENTS`. Never cut the same feature twice.

---

## 5. Solid Aggregation: Monolithic Manifold Union Over Buffer Concatenation
* **Mechanism**: Three.js `mergeGeometries` merely concatenates vertex arrays. Overlapping struts, cross arms, and boss posts remain interpenetrating internal shells with coincident faces, which slicers treat as non-manifold intersections.
* **Invariant**: Combine intersecting structural solids using a true boolean union (`manifoldUnion(geoms)`) prior to cutting operations, collapsing overlapping volumes into a single monolithic shell with zero internal walls.
