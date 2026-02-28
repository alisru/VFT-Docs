import re

file_path = "E:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/America/Trump_Manual_Score_Review.md"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def replace_block(lines, start_idx, header, original_justification_snippet, new_score_text, new_justification):
    # Find the header
    found_idx = -1
    for i in range(start_idx, len(lines)):
        if header in lines[i]:
            found_idx = i
            break
            
    if found_idx == -1:
        print(f"ERROR: Could not find header: {header}")
        return lines, start_idx
        
    print(f"Found {header} at line {found_idx}")
    
    # We found the header. Now look for the Current Score, Updated Score, and Justification in the next few lines
    for j in range(found_idx + 1, found_idx + 15):
        if j >= len(lines):
            break
        if "**Updated Score:** -1" in lines[j]:
            lines[j] = f"*   **Updated Score:** {new_score_text}\n"
            print(f"  -> Replaced score at line {j}")
        elif "**Justification:**" in lines[j]:
            lines[j] = f"*   **Justification:** {new_justification}\n"
            print(f"  -> Replaced justification at line {j}")
            return lines, found_idx
            
    print(f"ERROR: Failed to update block for {header}")
    return lines, found_idx


replacements = [
    (
        "#### 17: Who.What.How : The Boss",
        "The American concept of",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** The original -1 score failed to recognize that 'The Boss' is a Kanonic archetype that Trump executes perfectly. He is the apotheosis of the American Boss—demanding absolute loyalty, ruling through personal fiat rather than institutional procedure, and equating his personal success entirely with the success of the enterprise. Rather than opposing the archetype, he amplifies its most pure, unconstrained, and dictatorial elements, bringing the ruthless logic of the private boardroom directly into the public square."
    ),
    (
        "#### 29: Who.Cause.Where : The Evangelist",
        "The Evangelist seeks to convert",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** While Trump is personally devoid of orthodox religious piety, he perfectly executes the *mechanics* of the American Evangelist. He is a master of the revival tent aesthetic, utilizing mass rallies to generate emotional catharsis, demanding absolute faith from his followers regardless of empirical truth, and selling a prosperity gospel of national greatness. He correctly identified that the political base desired a savior figure rather than a policy manager, and he flawlessly adopted the rhetorical cadence and charismatic authority of the tent preacher to deliver it."
    ),
    (
        "#### 149: Where.Effect.Where : The Action Movie",
        "The Action Movie is the Kanonic",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** Trump perfectly intuitively grasps and executes the physics of the American Action Movie, where complex geopolitical problems are reduced to a simple binary of good versus evil, resolvable only through the sheer, unilateral use of force by an anti-hero. He treats the presidency as a sustained theatrical performance, demanding dramatic plot twists, easily identifiable villains, and explosive rhetoric. He successfully merged the entertainment logic of the blockbuster with the execution of state power, giving the base exactly the cinematic resolution they crave over complex reality."
    ),
    (
        "#### 151: Where.Effect.Effect : The Con Man",
        "The Con Man (Confidence Man) thrives",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** The original -1 score misses the point that 'The Con Man' (the Confidence Man) is a deeply embedded Kanonic archetype reflecting the dark side of American reinvention and salesmanship. Trump is the apex predator of this archetype. He operates almost entirely on the generation of false confidence, selling an illusion of competence and wealth so compelling that millions willingly suspend their disbelief. He perfects the uniquely American art of the hustle, translating the skills of the carnival barker into the highest office of the Republic."
    ),
    (
        "#### 169: Why.What.How : Television",
        "Television fundamentally altered",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** Trump is not opposed to Television; he is its absolute master and ultimate creation. He understood before anyone else that in the modern American Kanon, reality is entirely subordinate to ratings. He governed explicitly as a television producer, viewing policies, personnel changes, and global crises simply as episodic content to dominate the 24-hour news cycle. He flawlessly executed the logic of the medium, proving that an entertainer who understands the mechanics of attention can bypass all traditional institutional gatekeepers."
    ),
    (
        "#### 227: How.How.Cause : The Campaign Trail",
        "The Campaign Trail is the grueling",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** Trump does not oppose the Campaign Trail; he essentially made it the permanent state of the American executive. The Kanonic Campaign Trail is defined by high-energy, performative persuasion and the mobilization of the base over actual governance. Trump realized that governing is slow and complex, but campaigning is infinite adrenaline. By launching his re-election campaign on the day of his inauguration and holding rallies continuously throughout his term, he perfectly amplified the vector, replacing the structure of governance entirely with the perpetual motion of the perpetual campaign."
    ),
    (
        "#### 285: Cause.Effect.What : The Right to Bear Arms",
        "The Kanonic ideal of the Second Amendment",
        "+1 (Corrected Error: Amplification)",
        "**CRITICAL AI CORRECTION:** The prior -1 score was incorrect. While Trump possesses no philosophical grounding regarding the Second Amendment, he perfectly executes the *political demand* of the vector. He aligns flawlessly with the absolutist interpretation of the right, utilizing the threat of confiscation to generate massive political leverage. He explicitly encourages the heavily armed posture of his base, recognizing that the threat of kinetic force is the ultimate guarantor of his political survival. He successfully amplifies the Kanonic anxiety that the citizenry must remain perpetually armed against the encroaching State."
    )
]

current_idx = 0
for header, snippet, new_score, new_justification in replacements:
    lines, current_idx = replace_block(lines, current_idx, header, snippet, new_score, new_justification)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Replacement complete.")
