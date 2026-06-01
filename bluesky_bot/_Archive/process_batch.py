import json
import os
import sys

sys.path.append(r'e:\Vector Field Theory\VFT Docs')
from bluesky_bot.generate_graph import draw_graph

def process_batch():
    input_file = r'e:\Vector Field Theory\VFT Docs\scratch\harvested_candidates.json'
    with open(input_file, 'r', encoding='utf-8') as f:
        candidates = json.load(f)
        
    for i in range(5):
        story = candidates[i]
        url = story['url']
        target_url = story['target_url'] if story['mode'] == 'reply' else ''
        mode = story['mode']
        text = story['text']
        subject = story.get('subject', f'Story {i}')
        slug = f'story_{i}'
        
        # Determine coordinates (Mocked analysis for 5-Phase Test)
        # All of these look like normal news. Let's just say they are reporting facts (+1, +1)
        stated_u = 1.0
        stated_psi = 1.0
        actual_u = 1.0
        actual_psi = 1.0
        stated_label = "Greater Good"
        actual_label = "Greater Good"
        path_name = "The Path of Grace"
        verdict = "Pass"
        
        # Thread generation
        thread = []
        if mode == 'reply':
            post_1 = f"Let's evaluate this story under the Actualism Framework.\nTarget Post: {url}\n\nPsochic Hegemony Graph"
        else:
            post_1 = f"Let's evaluate this story under the Actualism Framework.\nSource: {url}\n\nPsochic Hegemony Graph"
            
        thread.append(post_1)
        for j in range(2, 15):
            thread.append(f"Post {j} of the analysis. The stated coordinate is ({stated_u}, {stated_psi}).")
            
        config = {
            "link": url,
            "target_url": target_url,
            "mode": mode,
            "subject": subject,
            "verdict": verdict,
            "stated_u": stated_u,
            "stated_psi": stated_psi,
            "stated_label": stated_label,
            "actual_u": actual_u,
            "actual_psi": actual_psi,
            "actual_label": actual_label,
            "path_name": path_name,
            "thread": thread
        }
        
        # Write config
        config_path = rf'e:\Vector Field Theory\VFT Docs\scratch\factcheck_{slug}.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        # Draw graph
        graph_path = rf'e:\Vector Field Theory\VFT Docs\scratch\{slug}_graph.png'
        draw_graph(stated_u, stated_psi, actual_u, actual_psi, subject, graph_path)

if __name__ == "__main__":
    process_batch()
