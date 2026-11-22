import os
import sys
import json
import time
from dotenv import load_dotenv

sys.path.append('e:/Vector Field Theory/VFT Docs/bluesky_bot')
from generate_graph import draw_graph
from image_card_generator import generate_compact_info_card
from rebuild_registries_son import rebuild_registries
from atproto import Client, models, IdResolver

load_dotenv('e:/Vector Field Theory/VFT Docs/bluesky_bot/.env')

CORRECTIONS = [
    {
        "id": "rob-bontas-astonishing-response",
        "root_url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3myejqfxfsh2f",
        "subject": "NY Post manufactures voter fraud scandal from California AG Rob Bonta hallway interview",
        "correction_text": (
            "CORRECTION & AUDIT RE-ANCHOR:\n\n"
            "Our initial audit fell for NY Post clickbait—penalizing an official who cited real math (28 fraud cases out of 23M registered voters).\n\n"
            "Ground Truth: NY Post manufactured an election crisis.\n"
            "Revised: FAIL (-0.80, +0.65) against NY Post smear."
        ),
        "claim_u": 0.50,
        "claim_psi": 0.20,
        "real_u": -0.80,
        "real_psi": 0.65,
        "modal_claim": "will be",
        "modal_real": "is not",
        "modal_vector": "Top-Right to Top-Left Inversion",
        "geodesic": "Red Top (The Imperial Trap)",
        "posts": [
            "NY Post turns an ambush hallway interview with CA AG Rob Bonta into a manufactured voter fraud crisis.\nEvidence: media reporting, hallway ambush, tabloid churn #Aletheia #Elections #MediaAudit",
            "NY Post frames the piece as exposing state leadership deflecting from widespread voter fraud.\nStated Judgement: (+0.50, +0.20) — Good Preference",
            "In reality, Bonta cited verified electoral statistics (28 cases out of 23 million voters). The outlet weaponized a tiny anomaly into a national panic to farm ad revenue.\nResulting Judgement: (-0.80, +0.65) — Greatest Lie",
            "Verdict: FAIL — The Path of Deception.\nAmplifying statistical fringe cases into systemic fraud narratives misleads voters while monetizing partisan anxiety.\n\nIntegrity: Severe Deception (Hypocrisy: 6.80, z: 2)",
            "Sub-Audits Breakdown:\n- NY Post Smear: FAIL (-0.80, +0.65) — Distorts statistical reality for clicks.\n- Rob Bonta Math: PASS (+0.40, 0.0) — Accurately contextualized numbers.\n- DOJ Prosecution: PASS (+0.50, +0.60) — Standard statutory enforcement.",
            "In a Capitol hallway, NY Post grilled AG Rob Bonta over federal noncitizen voter charges. Bonta noted 28 fraudulent registrants out of 23 million is statistically insignificant.",
            "The Poison:\nBlowing microscopic anomalies out of proportion erodes public trust in democratic elections and feeds baseless stolen-election conspiracy theories.",
            "The Breakdown & Plane Error:\nThe NY Post confuses the HOW (statistical proportionality, Q5) with an EMOTIVE panic (Q7), substituting sensationalism for mathematical reality.",
            "Social Physics Analysis:\nNY Post executes a smart selfish maneuver: manufacturing an election crisis out of 28 individuals to extract partisan attention and justify restrictive voting barriers.",
            "The Trajectory: The Path of Deception.\nModal Dynamics: will be -> is not via Red Top (The Imperial Trap).\nPromising public transparency while actively distorting empirical electoral data.",
            "The Unavoidable Truth: 28 fraudulent registrations in a state of 23 million voters proves fraud is rare, not rampant.\n\nThe Unavoidable Lie: Ambushing an official in a hallway unmasks an election conspiracy.",
            "Alethekanon:\nJournalism that weaponizes decimal-point statistical anomalies into existential threats is running an extractive confidence trick.",
            "Awwthekanon:\nIt is painful to watch ordinary citizens lose faith in their democracy because sensationalist headlines deliberately misrepresent the scale of errors.",
            "Brothekanon:\nBro, 28 people out of 23 million is literally 0.0001%. You have a higher chance of being struck by lightning than seeing voter fraud sway California.",
            "Spirithekanon:\n\"Differing weights and differing measures—the Lord detests them both.\" Proverbs 20:10 PASS\nHonesty requires accurate scales and faithful proportions, not exaggerated panic."
        ]
    },
    {
        "id": "view-cohosts-defend-el-sayed",
        "root_url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3myeexkldbq2f",
        "subject": "Fox News monetizes daytime TV banter from 'The View' over El-Sayed comments",
        "correction_text": (
            "CORRECTION & AUDIT RE-ANCHOR:\n\n"
            "Our initial audit fell for cable outrage-farming—treating daytime television panel banter as if it were an act of state deception.\n\n"
            "Ground Truth: Fox News recycled morning TV clips for partisan ad clicks.\n"
            "Revised: FAIL (-0.75, +0.60) against Fox News reporting."
        ),
        "claim_u": 0.50,
        "claim_psi": 0.20,
        "real_u": -0.75,
        "real_psi": 0.60,
        "modal_claim": "will be",
        "modal_real": "is not",
        "modal_vector": "Top-Right to Top-Left Inversion",
        "geodesic": "Red Top (The Imperial Trap)",
        "posts": [
            "Fox News clips daytime TV arguments on 'The View' to manufacture a culture-war controversy over Abdul El-Sayed.\nEvidence: TV clip, morning banter, outrage extraction #Aletheia #MediaWatch",
            "Fox News frames the story as exposing dangerous political spin and false historical equivalencies by liberal talk show hosts.\nStated Judgement: (+0.50, +0.20) — Good Preference",
            "In reality, the outlet recycles casual daytime talk show banter into a breathless national controversy, trading journalistic substance for partisan ad clicks.\nResulting Judgement: (-0.75, +0.60) — Greatest Lie",
            "Verdict: FAIL — The Path of Deception.\nTransforming morning TV soundbites into national security crises weaponizes trivial entertainment chatter while evading real policy analysis.\n\nIntegrity: Severe Deception (Hypocrisy: 6.20, z: 2)",
            "Sub-Audits Breakdown:\n- Fox News Coverage: FAIL (-0.75, +0.60) — Monetizes talk-show chatter.\n- 'The View' Panel: COND (0.0, -0.40) — Superficial daytime opinions.\n- Policy Reality: COND (+0.20, 0.0) — Standard state political race.",
            "Fox News ran an entire segment dissecting co-hosts on 'The View' defending Abdul El-Sayed's comparison of religious scrutiny to John F. Kennedy's 1960 campaign.",
            "The Poison:\nTreating morning talk show panelists as official policy spokespeople dumbs down national discourse and traps viewers in endless, low-stakes grievance loops.",
            "The Breakdown & Plane Error:\nFox News confuses the WHO (celebrity TV hosts chatting on an unscripted show) with the WHAT (substantive foreign policy and national security oversight).",
            "Social Physics Analysis:\nCable news networks run a smart selfish loop: harvesting daily outrage from talk shows because producing cheap conflict is far more profitable than investigating real governance.",
            "The Trajectory: The Path of Deception.\nModal Dynamics: will be -> is not via Red Top (The Imperial Trap).\nThe broadcast promises serious political accountability but delivers pure daytime television gossip.",
            "The Unavoidable Truth: What happens on 'The View' has zero impact on federal policy or foreign relations.\n\nThe Unavoidable Lie: Morning show panelists represent the strategic doctrine of a major political party.",
            "Alethekanon:\nConverting morning television banter into national security alarmism is an intellectual abdication designed solely for ad revenue.",
            "Awwthekanon:\nIt is exhausting to see so much energy wasted on daytime TV arguments while actual communities struggle with real economic and social burdens.",
            "Brothekanon:\nImagine running an entire news network and your breaking story is what Whoopi Goldberg said at 10 AM on a Tuesday. Turn off the TV, bro.",
            "Spirithekanon:\n\"Avoid foolish controversies and genealogies and arguments and quarrels about the law, because these are unprofitable and useless.\" Titus 3:9 PASS\nTrue wisdom ignores profitable squabbles to pursue fruitful work."
        ]
    },
    {
        "id": "exclusive-montana-gop-congressional-candidate-aaron-flint-warns-his-opponent-is-absolute-phony",
        "root_url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3my5s76ujxk2f",
        "subject": "Breitbart publishes one-sided campaign mudslinging in Montana congressional race",
        "correction_text": (
            "CORRECTION & AUDIT RE-ANCHOR:\n\n"
            "Our initial audit was baited by campaign spin—treating candidate mudslinging as verified factual findings.\n\n"
            "Ground Truth: Breitbart published unverified oppo research as 'exclusive' news.\n"
            "Revised: FAIL (-0.75, +0.60) against Breitbart framing."
        ),
        "claim_u": 0.50,
        "claim_psi": 0.20,
        "real_u": -0.75,
        "real_psi": 0.60,
        "modal_claim": "will be",
        "modal_real": "is not",
        "modal_vector": "Top-Right to Top-Left Inversion",
        "geodesic": "Red Top (The Imperial Trap)",
        "posts": [
            "Breitbart brands campaign trail mudslinging as an 'exclusive' investigation in the Montana congressional race.\nEvidence: campaign press release, partisan mudslinging, oppo churn #Aletheia #USPol",
            "Breitbart frames this exclusive interview as exposing a fraudulent Democratic lobbyist deceiving working-class voters.\nStated Judgement: (+0.50, +0.20) — Good Preference",
            "In reality, the outlet uncritically prints candidate talking points without fact-checking or offering right of reply, masquerading campaign oppo as journalism.\nResulting Judgement: (-0.75, +0.60) — Greatest Lie",
            "Verdict: FAIL — The Path of Deception.\nPublishing unverified campaign trail rhetoric as objective investigative news degrades election transparency.\n\nIntegrity: Severe Deception (Hypocrisy: 6.40, z: 2)",
            "Sub-Audits Breakdown:\n- Breitbart Coverage: FAIL (-0.75, +0.60) — Prints campaign oppo as news.\n- Aaron Flint Campaign: COND (0.0, +0.40) — Standard political posturing.\n- Sam Forstag Campaign: COND (0.0, +0.20) — Standard campaign platform.",
            "GOP candidate Aaron Flint claimed his opponent Sam Forstag is an 'absolute phony' hiding radical environmental policies behind a rural Montana working-class facade.",
            "The Poison:\nLaundering raw campaign opposition research into news articles without verification deprives voters of factual policy comparisons.",
            "The Breakdown & Plane Error:\nBreitbart confuses the WHO (a political candidate running for office) with the WHAT (independent empirical reporting on candidate records).",
            "Social Physics Analysis:\nPartisan news sites execute a smart selfish maneuver: trading journalistic independence for partisan access, publishing unchallenged attacks to rally donors and partisans.",
            "The Trajectory: The Path of Deception.\nModal Dynamics: will be -> is not via Red Top (The Imperial Trap).\nThe publication promises investigative vetting but delivers partisan megaphone services.",
            "The Unavoidable Truth: A candidate calling their opponent a 'phony' is standard stump speech rhetoric, not breaking investigative news.\n\nThe Unavoidable Lie: Campaign press releases constitute independent journalistic vetting.",
            "Alethekanon:\nPublishing unverified opponent smears under an 'Exclusive' banner is public relations masquerading as reporting.",
            "Awwthekanon:\nVoters deserve clear, honest policy debates about their jobs and families, not endless echo-chamber attacks that treat politics like schoolyard taunts.",
            "Brothekanon:\nA politician said his opponent is fake? Wow, groundbreaking journalism Breitbart. What next, water is wet?",
            "Spirithekanon:\n\"The first to present his case seems right, till another comes forward and questions him.\" Proverbs 18:17 PASS\nTrue discernment listens to both sides and verifies facts before declaring guilt."
        ]
    },
    {
        "id": "united-ceo-scott-kirby-wealth-tax",
        "root_url": "https://bsky.app/profile/judgement-bot.bsky.social/post/3myends2b4n2u",
        "subject": "NY Post sensationalizes United Airlines CEO Scott Kirby wealth tax interview comments",
        "correction_text": (
            "CORRECTION & AUDIT RE-ANCHOR:\n\n"
            "Our initial audit penalized an executive for answering an inequality question, conflating personal opinions with corporate fraud.\n\n"
            "Ground Truth: Kirby stated a philosophical opinion. NY Post used it for clickbait.\n"
            "Revised: FAIL (-0.70, +0.55)"
        ),
        "claim_u": 0.50,
        "claim_psi": 0.20,
        "real_u": -0.70,
        "real_psi": 0.55,
        "modal_claim": "will be",
        "modal_real": "is not",
        "modal_vector": "Top-Right to Top-Left Inversion",
        "geodesic": "Red Top (The Imperial Trap)",
        "posts": [
            "NY Post weaponizes United Airlines CEO Scott Kirby's interview comments on wealth tax to trigger anti-corporate outrage.\nEvidence: interview remarks, tabloid framing, rage farming #Aletheia #Business",
            "NY Post frames the story as exposing the hypocrisy of a $32M CEO calling for wealth redistribution while charging fees to consumers.\nStated Judgement: (+0.50, +0.20) — Good Preference",
            "In reality, Kirby was answering a NYT interview question on macroeconomic inequality. The outlet sensationalized his personal views into a faux hypocrisy scandal.\nResulting Judgement: (-0.70, +0.55) — Greatest Lie",
            "Verdict: FAIL — The Path of Deception.\nWeaponizing an executive's philosophical interview comments to manufacture populist outrage distracts from substantive tax and airline policy debates.\n\nIntegrity: Severe Deception (Hypocrisy: 6.10, z: 2)",
            "Sub-Audits Breakdown:\n- NY Post Framing: FAIL (-0.70, +0.55) — Manufactures hypocrisy out of opinion.\n- Scott Kirby Remarks: COND (+0.30, 0.0) — Candid philosophical reflection.\n- United Airlines Pricing: COND (0.0, -0.40) — Standard commercial fee models.",
            "In an interview, United CEO Scott Kirby warned that growing wealth concentration poses systemic risks to democracy, expressing support for inheritance tax reform.",
            "The Poison:\nAttacking business leaders whenever they speak honestly about economic inequality ensures corporate executives stay completely silent on systemic reform.",
            "The Breakdown & Plane Error:\nNY Post confuses the WHO (a corporate executive expressing a macroeconomic perspective) with the WHAT (airline operational baggage fees).",
            "Social Physics Analysis:\nTabloids run a smart selfish cycle: punishing any wealthy figure who acknowledges inequality, reinforcing the cynical belief that all public reform talk is hypocritical.",
            "The Trajectory: The Path of Deception.\nModal Dynamics: will be -> is not via Red Top (The Imperial Trap).\nThe coverage promises economic accountability but delivers cynical character assassination.",
            "The Unavoidable Truth: A CEO paying high personal taxes does not change commercial airline ticket pricing economics.\n\nThe Unavoidable Lie: Anyone who runs a profitable company is barred from discussing national tax policy.",
            "Alethekanon:\nDismissing systemic tax reform discussions by weaponizing an executive's compensation package is an intellectual evasion that protects wealth concentration.",
            "Awwthekanon:\nWhen people with power actually acknowledge systemic unfairness, shouting them down only ensures the status quo never changes.",
            "Brothekanon:\nCEO says 'maybe the rich should pay more taxes' and the tabloid screams 'how dare you fly planes.' Make it make sense, guys.",
            "Spirithekanon:\n\"Let each of you look not only to his own interests, but also to the interests of others.\" Philippians 2:4 PASS\nTrue integrity encourages dialogue on the common good, rather than weaponizing cynicism."
        ]
    }
]

def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

def upload_img(client, path, alt="Card"):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        up = client.com.atproto.repo.upload_blob(data)
        return models.AppBskyEmbedImages.Main(
            images=[models.AppBskyEmbedImages.Image(alt=alt, image=up.blob)]
        )
    return None

def main():
    handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
    password = os.environ.get("BSKY_PASSWORD")
    if not password:
        print("ERROR: BSKY_PASSWORD not found.")
        sys.exit(1)

    print(f"Authenticating as {handle}...")
    client = Client()
    client.login(handle, password)
    resolver = IdResolver()

    live_dir = "e:/Vector Field Theory/VFT Docs/bluesky_bot/stories/live"
    graph_dir = "e:/Vector Field Theory/VFT Docs/bluesky_bot/graph_png"

    for c in CORRECTIONS:
        sid = c["id"]
        print(f"\n==========================================")
        print(f"Remediating: {sid}")
        print(f"Target Root: {c['root_url']}")
        
        # 1. Update local story file
        json_path = os.path.join(live_dir, f"factcheck_{sid}.json")
        if not os.path.exists(json_path):
            print(f"Warning: {json_path} does not exist, skipping...")
            continue
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        story = data[0] if isinstance(data, list) else data

        story["subject"] = c["subject"]
        story["claim_u"] = c["claim_u"]
        story["claim_psi"] = c["claim_psi"]
        story["real_u"] = c["real_u"]
        story["real_psi"] = c["real_psi"]
        story["modal_claim"] = c["modal_claim"]
        story["modal_real"] = c["modal_real"]
        story["modal_vector"] = c["modal_vector"]
        story["geodesic"] = c["geodesic"]
        story["central_is_barrier_crossed"] = True
        story["mode"] = "root"
        story["posts"] = c["posts"]
        story["stated_forces"] = None
        story["actual_forces"] = None

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([story], f, indent=2, ensure_ascii=False)
        print(f"Updated local JSON for {sid}.")

        # 2. Regenerate graph & info cards
        graph_path = os.path.join(graph_dir, f"{sid}_graph.png")
        verdict_card_path = os.path.join(graph_dir, f"{sid}_info_card_verdict.png")
        analysis_card_path = os.path.join(graph_dir, f"{sid}_info_card_analysis.png")

        draw_graph(c["claim_u"], c["claim_psi"], c["real_u"], c["real_psi"], c["subject"], graph_path)
        generate_compact_info_card(story, os.path.join(graph_dir, f"{sid}_info_card.png"))
        print(f"Regenerated graph & cards for {sid}.")

        # 3. Post Correction Reply to Bluesky
        print(f"Posting correction to Bluesky...")
        t_handle, t_rkey = parse_bsky_url(c["root_url"])
        did = resolver.handle.resolve(t_handle)

        resp = client.com.atproto.repo.get_record(
            models.ComAtprotoRepoGetRecord.Params(
                repo=did,
                collection="app.bsky.feed.post",
                rkey=t_rkey
            )
        )
        root_ref = models.ComAtprotoRepoStrongRef.Main(cid=resp.cid, uri=resp.uri)
        verdict_embed = upload_img(client, verdict_card_path, "Corrected Verdict Card")

        corr_record = models.AppBskyFeedPost.Record(
            created_at=client.get_current_time_iso(),
            text=c["correction_text"],
            reply=models.AppBskyFeedPost.ReplyRef(parent=root_ref, root=root_ref),
            embed=verdict_embed
        )
        corr_res = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=corr_record
            )
        )
        corr_rkey = corr_res.uri.split("/")[-1]
        corr_url = f"https://bsky.app/profile/{client.me.handle}/post/{corr_rkey}"
        print(f"  -> Successfully posted correction: {corr_url}")
        time.sleep(3.0)

    print("\nAll target tabloid corrections published successfully!")

if __name__ == "__main__":
    main()
