import re

bt = chr(96)
correct_candidates = f'''const staticCandidates = [
          {bt}sources/${{storyId}}.json{bt},
          {bt}sources/factcheck_${{cleanSlug}}.json{bt},
          {bt}sources/${{cleanSlug}}.json{bt}
        ];'''

correct_shard = f'''if (!window._SOURCE_SHARDS[shardKey]) {{
            const sResp = await fetch({bt}sources/shard_${{shardKey}}.json{bt});
            if (sResp.ok) {{
              window._SOURCE_SHARDS[shardKey] = await sResp.json();
            }}
          }}'''

for path in ['bluesky_bot/control_panel.html', 'bluesky_bot/dist_audit_site/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    c = re.sub(r'const staticCandidates = \[\s*sources/\.json,\s*sources/factcheck_\.json,\s*sources/\.json\s*\];', correct_candidates, c)
    c = re.sub(r'if \(!window\._SOURCE_SHARDS\[shardKey\]\) \{\s*const sResp = await fetch\(sources/shard_\.json\);\s*if \(sResp\.ok\) \{\s*window\._SOURCE_SHARDS\[shardKey\] = await sResp\.json\(\);\s*\}\s*\}', correct_shard, c)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Done {path}')
