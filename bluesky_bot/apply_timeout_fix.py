import os

target_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"

with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update GEMINI_TIMEOUT_SECS to 60s
old_timeout = 'GEMINI_TIMEOUT_SECS = int(os.environ.get("GEMINI_TIMEOUT_SECS", "90"))'
new_timeout = 'GEMINI_TIMEOUT_SECS = int(os.environ.get("GEMINI_TIMEOUT_SECS", "60"))'
if old_timeout in content:
    content = content.replace(old_timeout, new_timeout, 1)

# 2. Add http_options to get_gemini_client
old_client_init = '''    try:
        client = genai.Client(api_key=api_key)
        return client'''
new_client_init = '''    try:
        http_options = types.HttpOptions(timeout=GEMINI_TIMEOUT_SECS * 1000) if types and hasattr(types, "HttpOptions") else None
        client = genai.Client(api_key=api_key, http_options=http_options) if http_options else genai.Client(api_key=api_key)
        return client'''
if old_client_init in content:
    content = content.replace(old_client_init, new_client_init, 1)

# 3. Update DEFAULT_FALLBACKS to prioritize stable 2.5-flash immediately after 3.8
old_fallbacks_start = 'DEFAULT_FALLBACKS = [\n    "gemini-3.8-flash",\n    "gemini-3.7-flash",\n    "gemini-2.5-flash",'
new_fallbacks_start = 'DEFAULT_FALLBACKS = [\n    "gemini-3.8-flash",\n    "gemini-2.5-flash",\n    "gemini-3.7-flash",'
assert old_fallbacks_start in content, "old_fallbacks_start not found"
content = content.replace(old_fallbacks_start, new_fallbacks_start, 1)

# 4. Add timeout to harvest_search_grounding generate_content
old_grounding_gen = '''            resp = genai_client.models.generate_content(
                model=g_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=16384,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )'''
new_grounding_gen = '''            g_http_opts = types.HttpOptions(timeout=GEMINI_TIMEOUT_SECS * 1000) if types and hasattr(types, "HttpOptions") else None
            resp = genai_client.models.generate_content(
                model=g_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=16384,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    http_options=g_http_opts
                )
            )'''
if old_grounding_gen in content:
    content = content.replace(old_grounding_gen, new_grounding_gen, 1)

# 5. Add timeout to Vertex client and config
old_vertex_init = '''                print(f"Initializing Vertex AI client (key present: {bool(vertex_key)})...")
                v_client = vertex_genai.Client(**client_args)'''
new_vertex_init = '''                v_http_opts = vertex_types.HttpOptions(timeout=GEMINI_TIMEOUT_SECS * 1000) if hasattr(vertex_types, "HttpOptions") else None
                if v_http_opts:
                    client_args["http_options"] = v_http_opts
                print(f"Initializing Vertex AI client (key present: {bool(vertex_key)})...")
                v_client = vertex_genai.Client(**client_args)'''
if old_vertex_init in content:
    content = content.replace(old_vertex_init, new_vertex_init, 1)

old_vertex_cfg = '''                v_config = vertex_types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=32768,
                    system_instruction=system_instruction,
                    safety_settings=v_safety_settings,
                    tools=v_tools_list,
                    thinking_config=v_thinking_config
                )'''
new_vertex_cfg = '''                v_config = vertex_types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=32768,
                    system_instruction=system_instruction,
                    safety_settings=v_safety_settings,
                    tools=v_tools_list,
                    thinking_config=v_thinking_config,
                    http_options=v_http_opts
                )'''
if old_vertex_cfg in content:
    content = content.replace(old_vertex_cfg, new_vertex_cfg, 1)

# 6. Add timeout to main genai config
old_main_cfg = '''                config = types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=65536,
                    system_instruction=system_instruction,
                    safety_settings=safety_settings,
                    tools=tools_list,
                    thinking_config=thinking_config
                )'''
new_main_cfg = '''                main_http_opts = types.HttpOptions(timeout=GEMINI_TIMEOUT_SECS * 1000) if types and hasattr(types, "HttpOptions") else None
                config = types.GenerateContentConfig(
                    temperature=0.15,
                    max_output_tokens=65536,
                    system_instruction=system_instruction,
                    safety_settings=safety_settings,
                    tools=tools_list,
                    thinking_config=thinking_config,
                    http_options=main_http_opts
                )'''
if old_main_cfg in content:
    content = content.replace(old_main_cfg, new_main_cfg, 1)

# 7. Update timeout error string check
old_err_check = 'elif "deadline" in err_str or "timeout" in err_str or "504" in err_str:'
new_err_check = 'elif "deadline" in err_str or "timeout" in err_str or "504" in err_str or "timed out" in err_str or "timeoutexception" in err_str:'
if old_err_check in content:
    content = content.replace(old_err_check, new_err_check, 1)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied client timeout fixes to google_ai_studio_one_shot.py!")
