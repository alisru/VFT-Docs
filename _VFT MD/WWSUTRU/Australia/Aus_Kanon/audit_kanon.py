
import json
from pathlib import Path

TARGET_JSON = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia_Kanon.json")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def audit_judgments():
    data = load_json(TARGET_JSON)
    issues = []
    
    for plane in data.get("planes", []):
        p_name = plane.get("name")
        for sense in plane.get("senses", []):
            s_vector = sense.get("vector")
            for item in sense.get("items", []):
                i_id = item.get("id")
                for concept in item.get("concepts", []):
                    c_name = concept.get("name")
                    judgement = concept.get("judgement", {})
                    
                    m_vec = judgement.get("moral_vector", 0.0)
                    w_vec = judgement.get("will_vector", 0.0)
                    notes = judgement.get("notes", "")
                    
                    # Criteria for potential issue: both vectors are 0.0 OR notes are empty/placeholder
                    # Note: Some vectors MIGHT genuinely be 0.0, but it's worth flagging for review.
                    if (m_vec == 0.0 and w_vec == 0.0) or not notes or "placeholder" in c_name.lower():
                        issues.append({
                            "plane": p_name,
                            "id": i_id,
                            "concept": c_name,
                            "m_vec": m_vec,
                            "w_vec": w_vec,
                            "notes": notes
                        })

    if not issues:
        print("No judgment issues found! All concepts have non-zero vectors or notes.")
    else:
        print(f"Found {len(issues)} potential judgment gaps:")
        for issue in issues:
            print(f"[{issue['plane']}] {issue['id']} - {issue['concept']}: (v={issue['m_vec']}, p={issue['w_vec']}) | Notes: {issue['notes']}")

if __name__ == "__main__":
    audit_judgments()
