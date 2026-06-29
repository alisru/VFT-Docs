import os
import shutil
import hashlib

io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"
archive_dir = r"E:\Vector Field Theory\VFT Docs\_Archive\Semantic_Duplicates_Backup"
os.makedirs(archive_dir, exist_ok=True)

duplicate_sets = [
    [r"ADIG_rebuke (1).md", r"ADIG_rebuke.md"],
    [r"7_x_7_x_7_trust_phase_field_model (1).md", r"7_x_7_x_7_trust_phase_field_model.md"],
    [r"alisru_ortho_translation_dictionary_v_1 (1).md", r"alisru_ortho_translation_dictionary_v_1.md"],
    [r"tbe_xi_ts_core (1).md", r"tbe_xi_ts_core (2).md", r"tbe_xi_ts_core.md"],
    [r"man_shadow_projection_garment (1).md", r"man_shadow_projection_garment.md"],
    [r"Relative Homogenous Scope (1).md", r"Relative Homogenous Scope.md"],
    [r"c_squared_Formal_Temporal_Analysis.md", r"c_squared_Formal_Temporal_Analysis_1.md"],
    [r"Forensic Analysis of Theological Mechanics and Societal Immunity.md", r"[Theology, Ritual, Metaphysics, Ontology] Forensic Analysis of Theological Mechanics and Societal Immunity.md"],
    [r"Actualism; The Crucible of the Archetypal Good Person.md", r"The Crucible of the Archetypal Good Person.md"],
    [r"irm-nbody-chain-formalism (1).md", r"irm-nbody-chain-formalism.md"],
    [r"Language_as_Lorentz_Hierarchy_PDF.md", r"_Archive\Language_as_Lorentz_Hierarchy_PDF (1)_DELETEME.md"],
    [r"god_patience_shadow_projection (1).md", r"god_patience_shadow_projection.md"],
    [r"tbe_ts_unifying_theory (1).md", r"tbe_ts_unifying_theory.md"],
    [r"fig_tree_mind_vessel.md", r"fig_tree_mind_vessel2.md"],
    [r"hagia_triada_living_water.md", r"hagia_triada_living_water2.md"],
    [r"first_immortals_eternal_witness (1).md", r"first_immortals_eternal_witness.md"],
    [r"The Geometry of Empathy_ Structural Inclusion vs Radical Identity in Conflict Resolution (1).md", r"The Geometry of Empathy_ Structural Inclusion vs Radical Identity in Conflict Resolution.md", r"The Geometry of Empathy_ Structural Inclusion vs Radical Identity.md"]
]

for dup_group in duplicate_sets:
    paths = []
    for filename in dup_group:
        p = os.path.join(io_dir, filename)
        if os.path.exists(p):
            paths.append(p)
    
    if len(paths) < 2:
        continue
    
    file_info = []
    for p in paths:
        stat = os.stat(p)
        file_info.append({
            'path': p,
            'size': stat.st_size,
            'mtime': stat.st_mtime
        })
    
    file_info.sort(key=lambda x: (x['size'], x['mtime']), reverse=True)
    survivor = file_info[0]['path']
    redundant = file_info[1:]
    
    print(f"KEEPING: {os.path.basename(survivor)} ({file_info[0]['size']} bytes)")
    for red in redundant:
        rpath = red['path']
        rname = os.path.basename(rpath)
        dest = os.path.join(archive_dir, rname)
        
        with open(survivor, 'rb') as f:
            h1 = hashlib.md5(f.read()).hexdigest()
        with open(rpath, 'rb') as f:
            h2 = hashlib.md5(f.read()).hexdigest()
            
        if h1 == h2:
            print(f"  DELETING 100% duplicate: {rname}")
            os.remove(rpath)
        else:
            print(f"  MOVING variant to archive: {rname}")
            shutil.move(rpath, dest)
