import os
import re

io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"

# Let's define the 63 files precisely
files_to_check = [
    "A Biblical Study on the Refusal to Listen and the Christological Response.md",
    "Academic Perspectives on the Psochic Hegemony.md",
    "Actualism and the Psochic Hegemony.md",
    "Actualism; The Crucible of the Archetypal Good Person.md",
    "Alethekanon Core Directive json.md",
    "Ancient Mother-Father Archetype Dynamics.md",
    "BRAINSTORM_FUTURE_MODULES.md",
    "Base-7 Geometric Linguistic Tensor Model.md",
    "Biblical Coordinate Matrix.md",
    "Controlled_Frame_Tomography (1).md",
    "Critique of Faith-Based Economics Structural Economic Models & The Parallel Polis.md",
    "Debt Thermodynamics & The Housing Monopoly.md",
    "Defining AGI within Actualism and Vector Field Theory.md",
    "Forensic Analysis of Theological Mechanics and Societal Immunity.md",
    "Gemini-Moral Quandaries Solved by Theory.md",
    "Gemini-Temporary Chat (1).md",
    "Global Vector Scan.md",
    "Hegemonic Astrology.md",
    "Hegemonic Audit_ Pauline Hanson tbf.md",
    "Hegemonic Mapping Log Vol 1.md",
    "Hegemonic Mapping Log Vol 2.md",
    "Hegemonic Mapping Log Vol 3.md",
    "Historical Analysis of Systemic Critiques.md",
    "Omni-Linguistic Bigram Weave.md",
    "Reality_Tensor_Air_Matrix.md",
    "Social Physics and the Theology of the Crash.md",
    "Tagging Matrix.md",
    "Tensor_Theology_Synthesis.md",
    "The Banking Hostage Crisis_ A Structural Analysis of Australian Financial Stability and Social Liquidity.md",
    "The Crucible of the Archetypal Good Person.md",
    "The Double Edged Sword of Discernment.md",
    "The Ekklesia Protocol.md",
    "The Geometry of Actualism and the Polytrope.md",
    "The Law of Empty Mass.md",
    "The Law of Rising Hearts.md",
    "The Meaning Integral & System Dynamics.md",
    "The Mechanics of Contextual Volume.md",
    "The Mechanics of the Well and Living Water.md",
    "The Ontology of Number and Scale.md",
    "The Physics and Theology of Marriage.md",
    "The Physics of Relative Morality and Questoscrapy.md",
    "The Physics of the Sedated State.md",
    "The Spread of Jonah's Signs into His Seasons.md",
    "The Universal Burial of the Talent.md",
    "The Vectors of Malice.md",
    "The_Fulfillment.md",
    "The_Psychological_Vectors.md",
    "Theological Assessment of the Psochic Hegemony.md",
    "Theological Mechanics and the Triadic Synthesis.md",
    "Theological Physics and Human Impossibility.md",
    "Theological and Structural Rebuke of ADIG.md",
    "[Theology, Ritual, Metaphysics, Ontology] Forensic Analysis of Theological Mechanics and Societal Immunity.md",
    "ai_is_not_an_oracle.md",
    "c_squared_Formal_Temporal_Analysis_1.md",
    "first_immortals_eternal_witness.md",
    "proof_by_resonance_article.md",
    "sealed_word.md",
    "sins-virtues-7planes.md",
    "social_cell_article.md",
    "social_cell_mechanics.md",
    "tbe_ts_unifying_theory.md",
    "virtue_compounds_model.md"
]

theology_files = []
philosophy_files = []

for filename in files_to_check:
    filepath = os.path.join(io_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        continue
        
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read(2000).lower()
        
    text = (filename + " " + content).lower()
    
    # Specific classifications
    is_theo = False
    
    # 1. Filename patterns
    if any(k in filename.lower() for k in [
        'biblical', 'theology', 'theological', 'christological', 'ekklesia', 'marriage', 'jonah', 'talent', 'immortal', 'witness', 'virtue', 'sins', 'decalogue', 'parable'
    ]):
        is_theo = True
    elif 'well and living water' in filename.lower() or 'rising hearts' in filename.lower() or 'crucible of the archetypal good person' in filename.lower() or 'fulfillment' in filename.lower() or 'sealed_word' in filename.lower():
        is_theo = True
    elif 'mother-father archetype' in filename.lower():
        is_theo = True
    
    # 2. Content patterns
    elif any(k in content for k in [
        'theology', 'theological', 'christological', 'ekklesia', 'mariage', 'marriage', 'scripture', 'genesis', 'isaiah', 'revelation', 'god', 'jesus', 'satan', 'lucifer'
    ]):
        # Double check it is not a broad philosophy paper mentioning God
        if 'philosophical' in filename.lower() or 'psochic hegemony' in filename.lower() or 'astrology' in filename.lower():
            is_theo = False
        else:
            is_theo = True
            
    if is_theo:
        theology_files.append(filename)
    else:
        philosophy_files.append(filename)

print(f"THEOLOGY FILES ({len(theology_files)}):")
for f in sorted(theology_files):
    print(f"  - {f}")

print(f"\nPHILOSOPHY FILES ({len(philosophy_files)}):")
for f in sorted(philosophy_files):
    print(f"  - {f}")
