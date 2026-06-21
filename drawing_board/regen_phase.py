from google import genai
from google.genai import types
import os

# Load credentials
env_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\.env"
keys = {}
with open(env_path, "r") as f:
    for line in f:
        if "=" in line:
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip()

client = genai.Client(vertexai=True, api_key=keys["VERTEX_API_KEY"])

prompt = (
    'A detailed paper-cut collage poster layout, featuring A vine growing from dark soil (earth), '
    'through a ring of fire (fire), reaching upward into luminous sky (air), bowing down as rain returns '
    'to the ocean below constructed from layered pieces of colored textured paper, against a background '
    'of overlapping torn paper sheets, a prominent realistic torn cream-paper banner across the middle '
    'featuring bold typographic text "The Phase Changes of Consciousness", high-detail paper textures, '
    'distinct 3D drop shadows between layers, warm studio lighting, clean composition'
)

print("Calling Vertex AI for image generation...")
result = client.models.generate_images(
    model='imagen-3.0-generate-002',
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio='16:9',
        output_mime_type='image/png'
    )
)

img_bytes = result.generated_images[0].image.image_bytes
output_path = r"e:\Vector Field Theory\VFT Docs\_AI files and chat logs\Videos\Uploaded\The_Phase_Changes_of_Consciousness\The_Phase_Changes_of_Consciousness.cover_v2.png"
with open(output_path, "wb") as f:
    f.write(img_bytes)

print("SUCCESS: Saved cover_v2.png")
