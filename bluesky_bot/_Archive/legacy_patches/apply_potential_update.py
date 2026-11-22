import sys

with open("bluesky_bot/google_ai_studio_one_shot.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Selectors
old_sel = """def rebuild_registries_selector(use_son=False):
    if use_son:
        print("Invoking SON registry rebuilder...")
        from rebuild_registries_son import rebuild_registries as rebuild_son
        rebuild_son()
    else:
        print("Invoking standard registry rebuilder...")
        from rebuild_registries import rebuild_registries as rebuild_std
        rebuild_std()

def promote_and_register_selector(use_son=False):
    if use_son:
        from rebuild_registries_son import promote_and_register_incremental as promote_son
        return promote_son()
    else:
        from rebuild_registries import promote_and_register_incremental as promote_std
        return promote_std()"""

new_sel = """def rebuild_registries_selector(use_son=False, use_potential=False):
    if use_son or use_potential:
        print("Invoking SON/Potential registry rebuilder...")
        from rebuild_registries_son import rebuild_registries as rebuild_son
        rebuild_son()
    else:
        print("Invoking standard registry rebuilder...")
        from rebuild_registries import rebuild_registries as rebuild_std
        rebuild_std()

def promote_and_register_selector(use_son=False, use_potential=False):
    if use_son or use_potential:
        from rebuild_registries_son import promote_and_register_incremental as promote_son
        return promote_son()
    else:
        from rebuild_registries import promote_and_register_incremental as promote_std
        return promote_std()"""

assert old_sel in text, "old_sel not found"
text = text.replace(old_sel, new_sel, 1)

# 2. _load_rules
old_load = """def _load_rules(use_son=False):
    \"\"\"Read + minify the rules files once per process; they don't change mid-run.\"\"\"
    cache_key = "son" if use_son else "regular"
    if cache_key not in _RULES_CACHE:
        if use_son:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_son.md")
        else:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")
        with open(convergence_path, "r", encoding="utf-8") as f:
            _RULES_CACHE[f"{cache_key}_convergence"] = minify_markdown(f.read())
        with open(formatting_path, "r", encoding="utf-8") as f:
            raw_fmt = f.read()
            clean_fmt = extract_thread_content_rules(raw_fmt)
            _RULES_CACHE[f"{cache_key}_formatting"] = minify_markdown(clean_fmt)
    return _RULES_CACHE[f"{cache_key}_convergence"], _RULES_CACHE[f"{cache_key}_formatting"]"""

new_load = """def _load_rules(use_son=False, use_potential=False):
    \"\"\"Read + minify the rules files once per process; they don't change mid-run.\"\"\"
    cache_key = "potential" if use_potential else ("son" if use_son else "regular")
    if cache_key not in _RULES_CACHE:
        if use_potential:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_potential.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_potential.md")
        elif use_son:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_son.md")
        else:
            convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
            formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")
        with open(convergence_path, "r", encoding="utf-8") as f:
            _RULES_CACHE[f"{cache_key}_convergence"] = minify_markdown(f.read())
        with open(formatting_path, "r", encoding="utf-8") as f:
            raw_fmt = f.read()
            clean_fmt = extract_thread_content_rules(raw_fmt)
            _RULES_CACHE[f"{cache_key}_formatting"] = minify_markdown(clean_fmt)
    return _RULES_CACHE[f"{cache_key}_convergence"], _RULES_CACHE[f"{cache_key}_formatting"]"""

assert old_load in text, "old_load not found"
text = text.replace(old_load, new_load, 1)

# 3. build_formatting_rules signature & body
old_bfr = """def build_formatting_rules(use_son=False, compact=False, five_word=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    convergence_rules, formatting_rules = _load_rules(use_son=use_son)"""

new_bfr = """def build_formatting_rules(use_son=False, use_potential=False, compact=False, five_word=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    convergence_rules, formatting_rules = _load_rules(use_son=use_son, use_potential=use_potential)"""

assert old_bfr in text, "old_bfr not found"
text = text.replace(old_bfr, new_bfr, 1)

old_bfr_aspect = """    if use_son and use_multi_aspect:
        multi_aspect_text = ("""
new_bfr_aspect = """    if (use_son or use_potential) and use_multi_aspect:
        multi_aspect_text = ("""
assert old_bfr_aspect in text, "old_bfr_aspect not found"
text = text.replace(old_bfr_aspect, new_bfr_aspect, 1)

# 4. build_system_instruction signature
old_bsi = """def build_system_instruction(use_son=False, compact=False, five_word=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", extra_context=None):"""
new_bsi = """def build_system_instruction(use_son=False, use_potential=False, compact=False, five_word=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", extra_context=None):"""
assert old_bsi in text, "old_bsi not found"
text = text.replace(old_bsi, new_bsi, 1)

# 5. build_output_format changes
old_bof_sig = """def build_output_format(n, use_son=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    expected_len = 28 if (use_son and use_multi_aspect) else (27 if use_son else 17)"""

new_bof_sig = """def build_output_format(n, use_son=False, use_potential=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    is_son_or_potential = use_son or use_potential
    if use_potential:
        expected_len = 33 if use_multi_aspect else 32
    elif use_son:
        expected_len = 28 if use_multi_aspect else 27
    else:
        expected_len = 17"""

assert old_bof_sig in text, "old_bof_sig not found"
text = text.replace(old_bof_sig, new_bof_sig, 1)

old_bof_ex = """    if use_son and use_multi_aspect:
        example_posts_list.insert(4,"""
new_bof_ex = """    if is_son_or_potential and use_multi_aspect:
        example_posts_list.insert(4,"""
assert old_bof_ex in text, "old_bof_ex not found"
text = text.replace(old_bof_ex, new_bof_ex, 1)

old_bof_schema_branch = """        "    null                                       // item[16]: macro actual will, null if none\\n"\n    )\n    if use_son:\n        if use_multi_aspect:"""
new_bof_schema_branch = """        "    null                                       // item[16]: macro actual will, null if none\\n"\n    )\n    if is_son_or_potential:\n        if use_multi_aspect:"""
assert old_bof_schema_branch in text, "old_bof_schema_branch not found"
text = text.replace(old_bof_schema_branch, new_bof_schema_branch, 1)

old_bof_schema_forces = """                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}  // item[26]: actual forces\\n\'\n            )\n    output_format += ("""

new_bof_schema_forces = """                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}  // item[26]: actual forces\\n\'\n            )\n        if use_potential:\n            output_format += (\n                ",\\n"\n                \'    "will be",                                 // item modal_claim: Stated claim Modal node string ("is", "will be", "is like", "was like", "can be", "can\\'t be", "May be", "Won\\'t be", "is not")\\n\'\n                \'    "is not",                                  // item modal_real: Actual ground reality Modal node string ("is", "will be", "is like", "was like", "can be", "can\\'t be", "May be", "Won\\'t be", "is not")\\n\'\n                \'    "Top-Right to Bottom-Left Inversion",      // item modal_vector: Quadrant transition or trajectory description\\n\'\n                \'    "Red Top (The Imperial Trap)",             // item geodesic: Dynamic Geodesic name (e.g. "Red Top (The Imperial Trap)", "Red Bottom (The PR Shield)", "Productive Geodesic", "Regressive Geodesic", "Magenta Vector", "None")\\n\'\n                \'    true                                       // item central_is_barrier_crossed: boolean (true if trajectory crossed central IS barrier from +u to -u, else false)\\n\'\n            )\n    output_format += ("""

assert old_bof_schema_forces in text, "old_bof_schema_forces not found"
text = text.replace(old_bof_schema_forces, new_bof_schema_forces, 1)

old_bof_gran = """    if use_son:\n        output_format += (\n            "FORCE SCORING GRANULARITY CRITICAL RULES:\\n\""""
new_bof_gran = """    if is_son_or_potential:\n        output_format += (\n            "FORCE SCORING GRANULARITY CRITICAL RULES:\\n\""""
assert old_bof_gran in text, "old_bof_gran not found"
text = text.replace(old_bof_gran, new_bof_gran, 1)

old_bof_ex_sec = """        "    null"\n    )\n    if use_son:\n        if use_multi_aspect:\n            output_format += (\n                ",\\n"\n                "    1.0,\\n"\n                "    12.5,\\n\""""
new_bof_ex_sec = """        "    null"\n    )\n    if is_son_or_potential:\n        if use_multi_aspect:\n            output_format += (\n                ",\\n"\n                "    1.0,\\n"\n                "    12.5,\\n\""""
assert old_bof_ex_sec in text, "old_bof_ex_sec not found"
text = text.replace(old_bof_ex_sec, new_bof_ex_sec, 1)

old_bof_ex_end = """                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\\n\'\n            )\n    output_format += (\n        "\\n"\n        "  ]\\n"\n        "]"\n    )\n    return output_format"""

new_bof_ex_end = """                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\\n\'\n            )\n        if use_potential:\n            output_format += (\n                ",\\n"\n                \'    "will be",\\n\'\n                \'    "is not",\\n\'\n                \'    "Top-Right to Bottom-Left Inversion",\\n\'\n                \'    "Red Top (The Imperial Trap)",\\n\'\n                \'    true\\n\'\n            )\n    output_format += (\n        "\\n"\n        "  ]\\n"\n        "]"\n    )\n    return output_format"""

assert old_bof_ex_end in text, "old_bof_ex_end not found"
text = text.replace(old_bof_ex_end, new_bof_ex_end, 1)

# 6. run_one_shot_evaluations signature & body
old_rose = """def run_one_shot_evaluations(genai_client, candidates, model_name, agnes_api_key=None, use_son=False, use_search=False, extra_context=None, model_sequence=None, compact=False, five_word=False, thinking_level="MEDIUM", use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", pre_grounded_dossier=None, pre_harvested_urls=None):"""
new_rose = """def run_one_shot_evaluations(genai_client, candidates, model_name, agnes_api_key=None, use_son=False, use_potential=False, use_search=False, extra_context=None, model_sequence=None, compact=False, five_word=False, thinking_level="MEDIUM", use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", pre_grounded_dossier=None, pre_harvested_urls=None):"""
assert old_rose in text, "old_rose not found"
text = text.replace(old_rose, new_rose, 1)

old_rose_call = """    convergence_rules, formatting_rules = build_formatting_rules(use_son=use_son, compact=compact, five_word=five_word, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions)
    system_instruction = build_system_instruction(use_son=use_son, compact=compact, five_word=five_word, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions, extra_context=extra_context)
    
    n = len(candidates)
    output_format = build_output_format(n, use_son=use_son, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions)"""

new_rose_call = """    convergence_rules, formatting_rules = build_formatting_rules(use_son=use_son, use_potential=use_potential, compact=compact, five_word=five_word, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions)
    system_instruction = build_system_instruction(use_son=use_son, use_potential=use_potential, compact=compact, five_word=five_word, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions, extra_context=extra_context)
    
    n = len(candidates)
    output_format = build_output_format(n, use_son=use_son, use_potential=use_potential, use_multi_aspect=use_multi_aspect, use_spiritual=use_spiritual, spiritual_traditions=spiritual_traditions)"""

assert old_rose_call in text, "old_rose_call not found"
text = text.replace(old_rose_call, new_rose_call, 1)

# 7. transpose_flat_to_json signature & dict/list parsing
old_tfj = """def transpose_flat_to_json(flat_text, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):"""
new_tfj = """def transpose_flat_to_json(flat_text, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all", use_potential=False):"""
assert old_tfj in text, "old_tfj not found"
text = text.replace(old_tfj, new_tfj, 1)

old_tfj_dict = """                if "stated_forces" in item and isinstance(item["stated_forces"], dict):
                    story["stated_forces"] = item["stated_forces"]
                if "actual_forces" in item and isinstance(item["actual_forces"], dict):
                    story["actual_forces"] = item["actual_forces"]"""

new_tfj_dict = """                if "stated_forces" in item and isinstance(item["stated_forces"], dict):
                    story["stated_forces"] = item["stated_forces"]
                if "actual_forces" in item and isinstance(item["actual_forces"], dict):
                    story["actual_forces"] = item["actual_forces"]
                if "modal_claim" in item and item["modal_claim"] is not None:
                    story["modal_claim"] = str(item["modal_claim"]).strip()
                if "modal_real" in item and item["modal_real"] is not None:
                    story["modal_real"] = str(item["modal_real"]).strip()
                if "modal_vector" in item and item["modal_vector"] is not None:
                    story["modal_vector"] = str(item["modal_vector"]).strip()
                if "geodesic" in item and item["geodesic"] is not None:
                    story["geodesic"] = str(item["geodesic"]).strip()
                if "central_is_barrier_crossed" in item and item["central_is_barrier_crossed"] is not None:
                    story["central_is_barrier_crossed"] = bool(item["central_is_barrier_crossed"])
                if use_potential or "modal_claim" in item or "geodesic" in item:
                    story["potential_audit"] = True"""

assert old_tfj_dict in text, "old_tfj_dict not found"
text = text.replace(old_tfj_dict, new_tfj_dict, 1)

old_tfj_list = """            if len(item) >= 27 and isinstance(item[26], dict):
                story["actual_forces"] = item[26]
            if len(item) >= 28 and isinstance(item[27], list):
                story["aspects"] = item[27]
                story["multiAspect"] = True
            elif use_multi_aspect:
                story["multiAspect"] = True"""

new_tfj_list = """            if len(item) >= 27 and isinstance(item[26], dict):
                story["actual_forces"] = item[26]
            if len(item) >= 28 and isinstance(item[27], list):
                story["aspects"] = item[27]
                story["multiAspect"] = True
            elif use_multi_aspect:
                story["multiAspect"] = True
            
            # Parse optional modal potential fields
            modal_offset = 28 if (len(item) >= 28 and isinstance(item[27], list)) else 27
            if len(item) >= modal_offset + 1 and item[modal_offset] is not None:
                story["modal_claim"] = str(item[modal_offset]).strip()
            if len(item) >= modal_offset + 2 and item[modal_offset + 1] is not None:
                story["modal_real"] = str(item[modal_offset + 1]).strip()
            if len(item) >= modal_offset + 3 and item[modal_offset + 2] is not None:
                story["modal_vector"] = str(item[modal_offset + 2]).strip()
            if len(item) >= modal_offset + 4 and item[modal_offset + 3] is not None:
                story["geodesic"] = str(item[modal_offset + 3]).strip()
            if len(item) >= modal_offset + 5 and item[modal_offset + 4] is not None:
                story["central_is_barrier_crossed"] = bool(item[modal_offset + 4])
            if use_potential or len(item) >= modal_offset + 5:
                story["potential_audit"] = True"""

assert old_tfj_list in text, "old_tfj_list not found"
text = text.replace(old_tfj_list, new_tfj_list, 1)

# 8. argparse
old_arg = """    parser.add_argument("--son", action="store_true", help="Use the 6-Attractor SON convergence model and formatting instructions")"""
new_arg = """    parser.add_argument("--son", action="store_true", help="Use the 6-Attractor SON convergence model and formatting instructions")
    parser.add_argument("--potential", action="store_true", help="Use the 9-Node Modal & Temporal Potential convergence model (convergence_son_potential.md) and formatting instructions")"""

assert old_arg in text, "old_arg not found"
text = text.replace(old_arg, new_arg, 1)

# 9. main() token savings
old_main_son = """    if args.son:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_son.md")
    else:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")"""

new_main_son = """    is_son_mode = args.son or args.potential

    if args.potential:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_potential.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_potential.md")
    elif args.son:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_son_lite.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting_son.md")
    else:
        convergence_path = os.path.join(workspace_dir, ".agent", "tools", "convergence-test", "convergence_lite.md")
        formatting_path = os.path.join(script_dir, "instructions", "thread_formatting.md")"""

assert old_main_son in text, "old_main_son not found"
text = text.replace(old_main_son, new_main_son, 1)

# 10. main evaluation call
old_eval_call = """                    genai_client, remaining, args.model, agnes_api_key=agnes_api_key, 
                    use_son=args.son, use_search=args.search,
                    extra_context=args.context, model_sequence=model_seq,
                    compact=compact_val, five_word=args.five_word,
                    thinking_level=args.thinking_level,
                    use_multi_aspect=is_multi_aspect_active,
                    use_spiritual=is_spiritual_active,
                    spiritual_traditions=args.spiritual_traditions,
                    pre_grounded_dossier=cur_dossier,
                    pre_harvested_urls=cur_urls
                )
                parsed = transpose_flat_to_json(raw_text, use_multi_aspect=is_multi_aspect_active, use_spiritual=is_spiritual_active, spiritual_traditions=args.spiritual_traditions)"""

new_eval_call = """                    genai_client, remaining, args.model, agnes_api_key=agnes_api_key, 
                    use_son=is_son_mode, use_potential=args.potential, use_search=args.search,
                    extra_context=args.context, model_sequence=model_seq,
                    compact=compact_val, five_word=args.five_word,
                    thinking_level=args.thinking_level,
                    use_multi_aspect=is_multi_aspect_active,
                    use_spiritual=is_spiritual_active,
                    spiritual_traditions=args.spiritual_traditions,
                    pre_grounded_dossier=cur_dossier,
                    pre_harvested_urls=cur_urls
                )
                parsed = transpose_flat_to_json(raw_text, use_multi_aspect=is_multi_aspect_active, use_spiritual=is_spiritual_active, spiritual_traditions=args.spiritual_traditions, use_potential=args.potential)"""

assert old_eval_call in text, "old_eval_call not found"
text = text.replace(old_eval_call, new_eval_call, 1)

# 11. reflection check
old_refl_check = """                        if isinstance(item, dict):
                            if args.son:
                                try:
                                    claim_rnet = float(item.get("claim_rnet", 0.0))
                                    real_rnet = float(item.get("real_rnet", 0.0))
                                    hypocrisy = abs(real_rnet - claim_rnet)
                                except (ValueError, TypeError):
                                    pass
                                if real_rnet > 2.0 or hypocrisy > 2.0:
                                    trigger_reflection = True
                            else:
                                try:
                                    claim_u = float(item.get("claim_u", 0.0))
                                    claim_psi = float(item.get("claim_psi", 0.0))
                                    real_u = float(item.get("real_u", 0.0))
                                    real_psi = float(item.get("real_psi", 0.0))
                                    hypocrisy = abs(real_u - claim_u) + abs(real_psi - claim_psi)
                                except (ValueError, TypeError):
                                    pass
                                if hypocrisy > 1.5:
                                    trigger_reflection = True
                        elif args.son and isinstance(item, list) and len(item) >= 25:
                            try:
                                claim_rnet = float(item[17]) if item[17] is not None else 0.0
                                real_rnet = float(item[18]) if item[18] is not None else 0.0
                                hypocrisy = abs(real_rnet - claim_rnet)
                            except (ValueError, TypeError):
                                pass
                            if real_rnet > 2.0 or hypocrisy > 2.0:
                                trigger_reflection = True
                        elif not args.son and isinstance(item, list) and len(item) >= 9:
                            try:
                                claim_u = float(item[5])
                                claim_psi = float(item[6])
                                real_u = float(item[7])
                                real_psi = float(item[8])
                                hypocrisy = abs(real_u - claim_u) + abs(real_psi - claim_psi)
                            except (ValueError, TypeError):
                                pass
                            if hypocrisy > 1.5:
                                trigger_reflection = True

                        if trigger_reflection:
                            desc = f"R_net={real_rnet:.2f}, delta={hypocrisy:.2f}" if args.son else f"hypocrisy={hypocrisy:.2f}\""""

new_refl_check = """                        if isinstance(item, dict):
                            if is_son_mode:
                                try:
                                    claim_rnet = float(item.get("claim_rnet", 0.0))
                                    real_rnet = float(item.get("real_rnet", 0.0))
                                    hypocrisy = abs(real_rnet - claim_rnet)
                                except (ValueError, TypeError):
                                    pass
                                if real_rnet > 2.0 or hypocrisy > 2.0:
                                    trigger_reflection = True
                            else:
                                try:
                                    claim_u = float(item.get("claim_u", 0.0))
                                    claim_psi = float(item.get("claim_psi", 0.0))
                                    real_u = float(item.get("real_u", 0.0))
                                    real_psi = float(item.get("real_psi", 0.0))
                                    hypocrisy = abs(real_u - claim_u) + abs(real_psi - claim_psi)
                                except (ValueError, TypeError):
                                    pass
                                if hypocrisy > 1.5:
                                    trigger_reflection = True
                        elif is_son_mode and isinstance(item, list) and len(item) >= 25:
                            try:
                                claim_rnet = float(item[17]) if item[17] is not None else 0.0
                                real_rnet = float(item[18]) if item[18] is not None else 0.0
                                hypocrisy = abs(real_rnet - claim_rnet)
                            except (ValueError, TypeError):
                                pass
                            if real_rnet > 2.0 or hypocrisy > 2.0:
                                trigger_reflection = True
                        elif not is_son_mode and isinstance(item, list) and len(item) >= 9:
                            try:
                                claim_u = float(item[5])
                                claim_psi = float(item[6])
                                real_u = float(item[7])
                                real_psi = float(item[8])
                                hypocrisy = abs(real_u - claim_u) + abs(real_psi - claim_psi)
                            except (ValueError, TypeError):
                                pass
                            if hypocrisy > 1.5:
                                trigger_reflection = True

                        if trigger_reflection:
                            desc = f"R_net={real_rnet:.2f}, delta={hypocrisy:.2f}" if is_son_mode else f"hypocrisy={hypocrisy:.2f}\""""

assert old_refl_check in text, "old_refl_check not found"
text = text.replace(old_refl_check, new_refl_check, 1)

# 12. reflection execution call
old_refl_call = """                                    ref_raw, ref_grounding = run_one_shot_evaluations(
                                        genai_client, [orig_cand], args.model, agnes_api_key=agnes_api_key,
                                        use_son=args.son, use_search=True, # Force search grounding ON
                                        extra_context=reflection_context, model_sequence=model_seq,
                                        compact=compact_val, five_word=args.five_word,
                                        thinking_level=args.thinking_level,
                                        use_multi_aspect=args.multi_aspect,
                                        use_spiritual=is_spiritual_active,
                                        spiritual_traditions=args.spiritual_traditions
                                    )
                                    ref_parsed = transpose_flat_to_json(ref_raw, use_multi_aspect=args.multi_aspect, use_spiritual=is_spiritual_active, spiritual_traditions=args.spiritual_traditions)"""

new_refl_call = """                                    ref_raw, ref_grounding = run_one_shot_evaluations(
                                        genai_client, [orig_cand], args.model, agnes_api_key=agnes_api_key,
                                        use_son=is_son_mode, use_potential=args.potential, use_search=True, # Force search grounding ON
                                        extra_context=reflection_context, model_sequence=model_seq,
                                        compact=compact_val, five_word=args.five_word,
                                        thinking_level=args.thinking_level,
                                        use_multi_aspect=args.multi_aspect,
                                        use_spiritual=is_spiritual_active,
                                        spiritual_traditions=args.spiritual_traditions
                                    )
                                    ref_parsed = transpose_flat_to_json(ref_raw, use_multi_aspect=args.multi_aspect, use_spiritual=is_spiritual_active, spiritual_traditions=args.spiritual_traditions, use_potential=args.potential)"""

assert old_refl_call in text, "old_refl_call not found"
text = text.replace(old_refl_call, new_refl_call, 1)

# 13. Promote and rebuild selectors at end
assert "promote_and_register_selector(args.son)" in text, "promote_and_register_selector(args.son) not found"
text = text.replace("promote_and_register_selector(args.son)", "promote_and_register_selector(is_son_mode)", 1)

assert text.count("rebuild_registries_selector(args.son)") == 2, "rebuild_registries_selector(args.son) count != 2"
text = text.replace("rebuild_registries_selector(args.son)", "rebuild_registries_selector(is_son_mode)")

with open("bluesky_bot/google_ai_studio_one_shot.py", "w", encoding="utf-8", newline="\r\n") as f:
    f.write(text)

print("SUCCESS: google_ai_studio_one_shot.py updated cleanly!")
