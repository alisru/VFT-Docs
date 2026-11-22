def build_output_format(n, use_son=False, use_multi_aspect=False, use_spiritual=False, spiritual_traditions="all"):
    expected_len = 28 if (use_son and use_multi_aspect) else (27 if use_son else 17)
    
    example_posts_list = [
        '"Hook text here.\\nEvidence: a, b, c\\n#Aletheia #Topic"',
        '"Claim text.\\nStated Judgement: (+1.0, 0.0) — Good Preference"',
        '"Reality text.\\nResulting Judgement: (-1.0, -1.0) — Greater Evil"',
        '"Verdict: FAIL — The Path of Deception.\\nExplanation.\\n\\nIntegrity: Severe Deception (Hypocrisy: 12.5, z: 4)"',
        '"Context paragraph."',
        '"The Bright Side:\\nNuance."',
        '"The Breakdown & Plane Error:\\nExplanation."',
        '"**Social Physics Analysis:**\\nDirect, conversational analysis in plain English detailing selfishness, pretexts, and projection."',
        '"The Trajectory: The Path of Deception.\\nWhen you map the gap between stated intentions and ground-level results, it plots a direct trajectory toward Greater Evil. Explanatory mathematical sentence."',
        '"The Unavoidable Truth: truth in 1 sentence.\\n\\nThe Unavoidable Lie: lie in 1 sentence."',
        '"Alethekanon:\\nStructural analysis in 1-2 concise sentences."',
        '"Awwthekanon:\\nEmpathy."',
        '"Brothekanon:\\nCasual take."'
    ]
    if use_son and use_multi_aspect:
        example_posts_list.insert(4, '"- Nigel Farage: FAIL (-0.94, -0.87) — Prioritizes political capital over truth.\\n- Electoral Messaging: FAIL (-0.94, -0.88) — Disinformation exposed."')
    
    if use_spiritual:
        example_posts_list.append('"Spirithekanon:\\n\\"Universal wisdom quote...\\" (Source Chapter/Section) — PASS (Spiritual Vector)\\nSpiritual evaluation in 1-2 sentences."')
    
    example_posts_str = ",\n      ".join(example_posts_list)

    output_format = (
        f"OUTPUT FORMAT — YOUR ENTIRE RESPONSE MUST BE A SINGLE VALID JSON LIST OF LISTS. NO commentary, NO markdown formatting (other than JSON code fences if desired), NO explanation.\n"
        f"The JSON array must contain exactly {n} elements (one per candidate, in the same order). Each element must be a list of exactly {expected_len} items representing the evaluation of that candidate in this specific structure:\n"
        "[\n"
        "  [\n"
        '    "thinking",                                // item[0]: detailed thinking block. You MUST write down the full 6-Phase Convergence scan here, including scoring the 18 variables of the 6 attractors with high-resolution decimals, and detailing your coordinate equations (u, psi), hypocrisy delta, and trajectory calculations step-by-step before outputting the rest of the array.\n'
        '    "id",                                      // item[1]: clean story id slug\n'
        '    "subject",                                 // item[2]: story subject\n'
        '    "link",                                    // item[3]: story link (or "")\n'
        '    "target_url",                              // item[4]: target post url (or "")\n'
        "    0.5,                                       // item[5]: stated morality (claim_u, float)\n"
        "    0.0,                                       // item[6]: stated will (claim_psi, float)\n"
        "    -0.8,                                      // item[7]: actual morality (real_u, float)\n"
        "    -0.9,                                      // item[8]: actual will (real_psi, float)\n"
        '    "root",                                    // item[9]: mode ("root" or "reply")\n'
        "    [\n"
        f"      {example_posts_str}\n"
        f"    ],                                         // item[10]: posts array (logical thread sequence: Hook, Claim, Reality, Verdict, Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables, Personas...)\n"
        '    ["Actor / Org / Geopolitical tag", ...],  // item[11]: actors array\n'
        '    "macro_event",                             // item[12]: overarching context name or "" if none\n'
        "    null,                                      // item[13]: macro stated morality, null if none\n"
        "    null,                                      // item[14]: macro stated will, null if none\n"
        "    null,                                      // item[15]: macro actual morality, null if none\n"
        "    null                                       // item[16]: macro actual will, null if none\n"
    )
    if use_son:
        if use_multi_aspect:
            output_format += (
                ",\n"
                "    1.0,                                       // item[17]: stated R_net integrity score\n"
                "    12.5,                                      // item[18]: actual R_net integrity score\n"
                "    0,                                         // item[19]: stated uncertainty score (claim_z)\n"
                "    4,                                         // item[20]: actual uncertainty score (real_z)\n"
                "    [0, 0, 0, 0, 0, 0, 0],                     // item[21]: stated blank profile [B_Q1..B_Q7]\n"
                "    [1, 0, 0, 2, 1, 0, 0],                     // item[22]: actual blank profile\n"
                '    "Absolute Truth",                          // item[23]: stated integrity label\n'
                '    "Severe Deception",                        // item[24]: actual integrity label\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}}, // item[25]: stated forces\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}, // item[26]: actual forces\n'
                '    [{"aspect": "Aspect Name", "claim_u": 0.5, "claim_psi": 0.0, "real_u": -0.9, "real_psi": -0.8, "verdict": "FAIL", "reason": "1-line reason under 60 chars"}] // item[27]: aspects breakdown\n'
            )
        else:
            output_format += (
                ",\n"
                "    1.0,                                       // item[17]: stated R_net integrity score\n"
                "    12.5,                                      // item[18]: actual R_net integrity score\n"
                "    0,                                         // item[19]: stated uncertainty score (claim_z)\n"
                "    4,                                         // item[20]: actual uncertainty score (real_z)\n"
                "    [0, 0, 0, 0, 0, 0, 0],                     // item[21]: stated blank profile [B_Q1..B_Q7]\n"
                "    [1, 0, 0, 2, 1, 0, 0],                     // item[22]: actual blank profile\n"
                '    "Absolute Truth",                          // item[23]: stated integrity label\n'
                '    "Severe Deception",                        // item[24]: actual integrity label\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}}, // item[25]: stated forces\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}  // item[26]: actual forces\n'
            )
    output_format += (
        "\n"
        "  ]\n"
        "]\n\n"
        "CRITICAL FOR MACRO CONTEXT:\n"
        "Identify if the candidate news story exists within a distinct overarching macro-event context (e.g. an announcement happening at a political photo-op/rally, or a sports title win happening at a White House PR event). If so, provide the macro-event name in item[12] and evaluate its stated and actual u/psi coordinates in items[13] to [16]. If no distinct macro-context exists, use empty string for item[12] and null for items[13] to [16].\n\n"
        "item[11] = actors array: principal named individuals, orgs, nation-states, or blocs (CRINK/BRICS/NATO/AUKUS/G7/SCO/Five Eyes) the story is ABOUT. Canonical full names. Max 6. [] if none.\n\n"
    )
    if use_son:
        output_format += (
            "FORCE SCORING GRANULARITY CRITICAL RULES:\n"
            "- You MUST score the [S, O, N] force magnitudes for the 6 attractors as granular decimals (e.g. 0.2, 0.5, 0.8, 1.2, 1.5, 1.8) based on specific evidence in the text. Do NOT default to binary 0.0 or 1.0 values, as this causes coordinate collapse and loses analytical resolution.\n"
            "- Ensure that the forces you output in items[25] and [26] are highly granular and match the math you write down in your thinking block (item[0]).\n\n"
            "INTEGRITY TIER MAPPING FOR ITEMS [23] AND [24]:\n"
            "Map claim_rnet to item[23] (claim_integrity) and real_rnet to item[24] (real_integrity) using these strict boundaries:\n"
            "- R_net == 1.0: \"Absolute Truth\"\n"
            "- 1.0 < R_net <= 1.5: \"Trustworthy\"\n"
            "- 1.5 < R_net <= 2.0: \"Conditionally Sound\"\n"
            "- 2.0 < R_net <= 5.0: \"Partially Distorted\"\n"
            "- 5.0 < R_net <= 10.0: \"Meaningful Distortion\"\n"
            "- 10.0 < R_net <= 100.0: \"Severe Deception\"\n"
            "- R_net > 100.0: \"Baseless Lies\"\n\n"
        )
    output_format += (
        "EXAMPLE RESPONSE (for a single candidate, format exactly as JSON list of lists):\n"
        "[\n"
        "  [\n"
        '    "Detailed Phase 1-5 structural scan and calculations...",\n'
        '    "my_slug_id",\n'
        '    "Story Title",\n'
        '    "https://...",\n'
        '    "",\n'
        "    1.0,\n"
        "    1.0,\n"
        "    -0.89,\n"
        "    -0.87,\n"
        '    "root",\n'
        "    [\n"
        f"      {example_posts_str}\n"
        "    ],\n"
        '    ["Nigel Farage", "Reform UK", "United Kingdom"],\n'
        '    "",\n'
        "    null,\n"
        "    null,\n"
        "    null,\n"
        "    null"
    )
    if use_son:
        if use_multi_aspect:
            output_format += (
                ",\n"
                "    1.0,\n"
                "    12.5,\n"
                "    0,\n"
                "    4,\n"
                "    [0, 0, 0, 0, 0, 0, 0],\n"
                "    [1, 0, 0, 2, 1, 0, 0],\n"
                '    "Absolute Truth",\n'
                '    "Severe Deception",\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}},\n'
                '    [\n'
                '      {\n'
                '        "name": "Nigel Farage Political Intervention",\n'
                '        "type": "actor",\n'
                '        "stated_forces": {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\n'
                '        "actual_forces": {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\n'
                '      },\n'
                '      {\n'
                '        "name": "Electoral Messaging Integrity",\n'
                '        "type": "aspect",\n'
                '        "stated_forces": {"GG": {"S": 1.0, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.0, "N": 0.5}, "LE": {"S": 0.0, "O": 0.0, "N": 0.5}, "GP": {"S": 1.0, "O": 0.0, "N": 0.0}, "BP": {"S": 1.0, "O": 1.0, "N": 0.0}},\n'
                '        "actual_forces": {"GG": {"S": 0.0, "O": 1.5, "N": 0.0}, "GE": {"S": 1.0, "O": 0.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\n'
                '      }\n'
                '    ]\n'
            )
        else:
            output_format += (
                ",\n"
                "    1.0,\n"
                "    12.5,\n"
                "    0,\n"
                "    4,\n"
                "    [0, 0, 0, 0, 0, 0, 0],\n"
                "    [1, 0, 0, 2, 1, 0, 0],\n"
                '    "Absolute Truth",\n'
                '    "Severe Deception",\n'
                '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\n'
                '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\n'
            )
    output_format += (
        "\n"
        "  ]\n"
        "]"
    )
    return output_format