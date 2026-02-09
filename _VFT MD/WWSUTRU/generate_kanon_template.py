import json

planes_info = [
    {"id": "1", "name": "Identity", "vector": "Who"},
    {"id": "2", "name": "Definition", "vector": "What"},
    {"id": "3", "name": "Land", "vector": "Where"},
    {"id": "4", "name": "Drive", "vector": "Why"},
    {"id": "5", "name": "Method", "vector": "How"},
    {"id": "6", "name": "Foundation", "vector": "Cause"},
    {"id": "7", "name": "Result", "vector": "Effect"},
]

vectors_info = ["Who", "What", "Where", "Why", "How", "Cause", "Effect"]

data = {
    "nation": "[Nation Name]",
    "planes": []
}

# Placeholder text
PLACEHOLDER_QUOTE = "This is a placeholder quote that must be at least 10 characters long to satisfy the schema validation rules."
PLACEHOLDER_NARRATIVE = "This is a placeholder narrative summary that must be at least 30 characters long. It summarizes the section effectively."
PLACEHOLDER_TOTALITY = "This is a placeholder totality narrative that must be sufficiently long (at least 50 characters) and use high-voltage philosophical language to synthesize the plane."
PLACEHOLDER_CONTEXT = "This is a placeholder context analysis. It must be at least 20 characters long and provide historical context."
PLACEHOLDER_MEANING = "This establishes [Concept] as a critical element of the national psyche. It explains why this vector defines the nation's psychology and meets the minimum length requirement."

for p_info in planes_info:
    plane = {
        "id": p_info["id"],
        "name": p_info["name"],
        "vector": p_info["vector"],
        "quote": PLACEHOLDER_QUOTE,
        "quote_author": "[Author]",
        "quote_source": "[Source]",
        "senses": [],
        "totality_narrative": PLACEHOLDER_TOTALITY
    }
    
    for i, sense_vector in enumerate(vectors_info):
        sense_id = f"q{i+1}"
        sense = {
            "id": sense_id,
            "vector": sense_vector,
            "description": f"The {sense_vector} of the {p_info['name']} ({p_info['vector']})",
            "items": [],
            "narrative": PLACEHOLDER_NARRATIVE
        }
        
        for item_vector in vectors_info:
            vector_id = f"({p_info['vector']}.{sense_vector}.{item_vector})"
            item = {
                "id": vector_id,
                "concepts": [
                    {
                        "name": "[Concept Name]",
                        "quotes": [
                            {
                                "text": PLACEHOLDER_QUOTE,
                                "author": "[Author]",
                                "source": "[Source]",
                                "year": "[Year]"
                            }
                        ],
                        "judgement": {
                            "moral_vector": 0.0,
                            "will_vector": 0.0,
                            "archetype_name": "Neutral",
                            "notes": "Optional judgement notes."
                        },
                        "context_analysis": PLACEHOLDER_CONTEXT,
                        "meaning_analysis": PLACEHOLDER_MEANING
                    }
                ]
            }
            sense["items"].append(item)
            
        plane["senses"].append(sense)
        
    data["planes"].append(plane)

with open(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\7x7x7_kanon_template.json", "w") as f:
    json.dump(data, f, indent=2)

print("Template created successfully.")
