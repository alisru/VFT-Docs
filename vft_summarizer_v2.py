import sys
import os
import re
from datetime import datetime

# Authorized Categories and Tags from the Tagging Matrix
TAG_MATRIX = {
    "Logic": ["Logic", "Mathematics", "Computation", "Maths", "Order", "Structured Order", "Algorithms", "Systems", "Calculus", "Algebra", "Geometry", "Statistics", "Programming", "Proofs", "Axioms", "Deduction", "Framework", "Hierarchy"],
    "Spirituality": ["Spirituality", "Mysticism", "Transcendence", "Faith", "Esotericism", "Metaphysical", "Occult", "Meditation", "Divinity", "Enlightenment", "Sacred", "Etheric", "Awakening", "Karma"],
    "Religion": ["Religion", "Theology", "Doctrine", "Charity", "Dogma", "Scripture", "Ritual", "Church", "Temple", "Creed", "Orthodoxy", "Worship", "Priesthood", "Canon", "Denomination"],
    "Cognition": ["Cognition", "Reason", "Intellect", "Intelligence", "Hope", "Thought", "Awareness", "Perception", "Sentience", "Rationality", "Neurology", "Neuroscience", "Idea", "Mental", "Focus"],
    "Physics": ["Physics", "Mechanics", "Matter", "Objectivity", "Thermodynamics", "Quantum", "Relativity", "Optics", "Gravity", "Energy", "Kinetics", "Particle", "Forces", "Dynamics", "Astrophysics", "Material"],
    "Metaphysics": ["Metaphysics", "Ontology", "Cosmology", "Imagination", "Existentialism", "Phenomenon", "Abstract", "Aether", "Reality-Theory", "Void", "First-Principles", "Archetypes"],
    "Ethics": ["Ethics", "Morality", "Values", "Emotional-physics", "Temperance", "Philosophy", "Virtue", "Deontology", "Utilitarianism", "Axiology", "Righteousness", "Code", "Integrity", "Moral-Compass", "Dilemma"],
    "Knowledge": ["Knowledge", "Epistemology", "Education", "Learning", "Prudence", "Information", "Data", "Wisdom", "Scholarship", "Academia", "Pedagogy", "Instruction", "Curriculum", "Study", "Literacy"],
    "Society": ["Community", "Civic", "Public", "Society", "Social", "Populace", "Tribe", "Village", "Group", "Collective", "Fellowship", "Network", "Neighborhood", "Cohort", "Population"],
    "Sociology": ["Sociology", "Culture", "Anthropology", "Empathy", "Demographics", "Ethnography", "Social-Structures", "Customs", "Traditions", "Human-Ecology", "Interpersonal", "Norms", "Kinship"],
    "Conscience": ["Conscience", "Judgment", "Principles", "Internal Judgment", "Justice", "Guilt", "Inner-Voice", "Fairness", "Law", "Jurisprudance", "Equity", "Conviction", "Rectitude", "Accountability"],
    "The World": ["Nature", "Ecology", "Environment", "The World", "Fortitude", "Biology", "Zoology", "Botany", "Biosphere", "Earth", "Ecosystem", "Natural-World", "Flora", "Fauna", "Wilderness", "Geology", "Climate"],
    "Psychology": ["Psychology", "Mind", "Behavior", "Understanding", "Psychiatry", "Therapy", "Psychoanalysis", "Emotion", "Trauma", "Personality", "Subconscious", "Mental-Health", "Affect", "Neuroscience"],
    "Communication": ["Communication", "Expression", "Linguistics", "Language", "Connection", "Discourse", "Dialogue", "Semantics", "Syntax", "Rhetoric", "Media", "Transmission", "Interaction", "Speech", "Writing", "Symbology"],
    "History": ["History", "Chronology", "Record", "Context", "Antiquity", "Archives", "Heritage", "Past", "Timeline", "Archaeology", "Paleontology", "Genealogy", "Epoch", "Era", "Annals", "Historiography"],
    "Reality": ["Reality", "Existence", "Actuality", "Truth", "Fact", "Objective-Truth", "Present", "Universe", "Cosmos", "Material-World", "Being", "Verity", "Tangibility", "Substantive"]
}

def generate_summary(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading {filepath}: {e}"

    filename = os.path.basename(filepath)
    date_str = "2026-05-24" # Keeping date consistent with requested format
    win_path = filepath.replace('/', '\\')

    # Logic to find topics
    topics = re.findall(r'^#+ (.*)', content, re.MULTILINE)
    topics = [t.strip() for t in topics if t.strip().lower() not in ['works cited', 'references', 'introduction', 'conclusion', 'summary', 'abstract', 'table of contents']]

    if not topics:
        topics = re.findall(r'^\* \*\*(.*?)\*\*', content, re.MULTILINE)
        if not topics:
            topics = re.findall(r'^#### (.*)', content, re.MULTILINE)

    if not topics:
        topics = ["Core Analysis"]

    summary_lines = []
    seen = set()
    unique_topics = []
    for t in topics:
        if t not in seen:
            unique_topics.append(t)
            seen.add(t)

    for i, topic in enumerate(unique_topics[:15]):
        summary_lines.append(f"{topic}: [Description for {topic}]")

    summary_txt = "\\\n".join(summary_lines)

    # Logic to select Category and Tags
    best_category = "Reality"
    matched_tags = []
    max_hits = -1

    content_lower = content.lower()

    for category, tags in TAG_MATRIX.items():
        hits = 0
        cat_tags = []
        if category.lower() in content_lower:
            hits += 5 # Higher weight for category name
        for tag in tags:
            if tag.lower() in content_lower:
                hits += 1
                cat_tags.append(tag)

        if hits > max_hits:
            max_hits = hits
            best_category = category
            matched_tags = cat_tags

    if not matched_tags:
        matched_tags = TAG_MATRIX[best_category][:3]
    else:
        # Deduplicate and sort tags
        matched_tags = sorted(list(set(matched_tags)))[:7]

    tags_str = ", ".join(matched_tags)

    # Plane mapping (guess based on category)
    plane_map = {
        "Logic": "Q5 HOW",
        "Spirituality": "Q1 WHO",
        "Religion": "Q1 WHO",
        "Cognition": "Q1 WHO",
        "Physics": "Q3 WHERE",
        "Metaphysics": "Q2 WHAT",
        "Ethics": "Q4 WHY",
        "Knowledge": "Q5 HOW",
        "Society": "Q7 EFFECT",
        "Sociology": "Q3 WHERE",
        "Conscience": "Q1 WHO",
        "The World": "Q3 WHERE",
        "Psychology": "Q1 WHO",
        "Communication": "Q2 WHAT",
        "History": "Q6 CAUSE",
        "Reality": "Q2 WHAT"
    }
    plane = plane_map.get(best_category, "Q2 WHAT")

    template = f"""### [{filename}] ({date_str})
**Path**: {win_path}
**Categories**: Plane: {plane}; Node: {best_category}; Tags: {tags_str}
**Summary**:
{summary_txt}"""
    return template

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(generate_summary(sys.argv[1]))
