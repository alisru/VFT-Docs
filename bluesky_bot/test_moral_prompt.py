import os, json, time, urllib.request, re
from html import unescape
from google import genai

# Load .env
env_file = os.path.join('bluesky_bot', '.env')
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

vertex_key = os.environ.get('VERTEX_API_KEY')
project_id = os.environ.get('VERTEX_PROJECT_ID', 'alethekanon')
location = os.environ.get('VERTEX_LOCATION', 'us-central1')

client_args = {'vertexai': True}
if vertex_key:
    client_args['api_key'] = vertex_key
else:
    client_args['project'] = project_id
    client_args['location'] = location

client = genai.Client(**client_args)

# Test on 3 diverse stories first: WA Police (Surveillance), AUKUS (Geopolitical), Andon Labs (AI Store Manager)
test_cases = [
    ('factcheck_ai_police_face_screening_trial_sparks_privacy_concern_107009644.json', 'WA Police AI Face Screening'),
    ('factcheck_aukus_sovereignty_audit.json', 'AUKUS Submarine Sovereignty'),
    ('factcheck_ai_store_manager_fires_employee.json', 'AI Store Manager Fires Human')
]

for fname, label in test_cases:
    fpath = os.path.join('bluesky_bot', 'stories', 'live', fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
        if isinstance(d, list): d = d[0]
    
    url = d.get('link', '')
    title = d.get('subject', '')
    
    # Get article text from previous benchmark
    with open(os.path.join('bluesky_bot', 'tests', 'vanilla_benchmark_10_stories.json'), 'r', encoding='utf-8') as bf:
        bdata = json.load(bf)
    
    match = next(item for item in bdata if item['filename'] == fname)
    raw_prompt_text = match['vanilla_gemini_3_7_flash']['prompt_sent'].split('\n\n', 2)[-1]
    
    prompt = f'Break down and judge the morality of this story and the actions described within it:\n\nURL: {url}\nTitle: {title}\n\n{raw_prompt_text}'
    
    print(f'=== Testing Moral Prompt on: {label} ===')
    t0 = time.time()
    resp = client.models.generate_content(
        model='gemini-3.7-flash',
        contents=prompt
    )
    print(f'Response ({round(time.time()-t0, 2)}s):\n')
    print(resp.text[:1200])
    print('\n' + '='*50 + '\n')