"""
download_seed_dictionary.py
Compiles and structures 100 foundational English words across core kinetic,
topological, custodial, and state domains into source_dictionary_100.json.
"""

import json
import os

SEED_WORDS_DATA = [
    # 1. Kinetic Displacement & Motion (16)
    {"word": "move", "pos": "verb", "orthodox_def": "to go or cause to go from one place to another; change position"},
    {"word": "go", "pos": "verb", "orthodox_def": "to move from one place to another; depart toward a destination"},
    {"word": "come", "pos": "verb", "orthodox_def": "to move toward or arrive at a specified place or person"},
    {"word": "walk", "pos": "verb", "orthodox_def": "to move on foot at a steady, moderate pace"},
    {"word": "run", "pos": "verb", "orthodox_def": "to move swiftly on foot with rapid strides"},
    {"word": "fly", "pos": "verb", "orthodox_def": "to move through the air without physical contact with ground"},
    {"word": "fall", "pos": "verb", "orthodox_def": "to move downward without control; drop to a lower level"},
    {"word": "rise", "pos": "verb", "orthodox_def": "to move upward from a lower to a higher position or level"},
    {"word": "flow", "pos": "verb", "orthodox_def": "to move along steadily and continuously in a current"},
    {"word": "carry", "pos": "verb", "orthodox_def": "to support and move an object from one location to another"},
    {"word": "turn", "pos": "verb", "orthodox_def": "to move in a circular direction around an axis or change orientation"},
    {"word": "roll", "pos": "verb", "orthodox_def": "to move by turning over and over on an axis"},
    {"word": "slip", "pos": "verb", "orthodox_def": "to lose hold or footing and slide unexpectedly"},
    {"word": "drop", "pos": "verb", "orthodox_def": "to let fall or fall vertically from an elevated position"},
    {"word": "jump", "pos": "verb", "orthodox_def": "to push oneself off a surface and into the air"},
    {"word": "travel", "pos": "verb", "orthodox_def": "to make a journey across distance between places"},

    # 2. Directional Force Dynamics (10)
    {"word": "push", "pos": "verb", "orthodox_def": "to exert force on an object to move it away from the source"},
    {"word": "pull", "pos": "verb", "orthodox_def": "to exert force on an object to draw it toward the source"},
    {"word": "strike", "pos": "verb", "orthodox_def": "to hit forcibly with an object or concentrated force"},
    {"word": "hit", "pos": "verb", "orthodox_def": "to bring an object or force into violent contact with another"},
    {"word": "press", "pos": "verb", "orthodox_def": "to apply steady continuous force against a surface"},
    {"word": "thrust", "pos": "verb", "orthodox_def": "to push suddenly or violently in a forward direction"},
    {"word": "drag", "pos": "verb", "orthodox_def": "to pull an object along a surface against friction or resistance"},
    {"word": "throw", "pos": "verb", "orthodox_def": "to propel through the air by a rapid release of force"},
    {"word": "drive", "pos": "verb", "orthodox_def": "to operate or force a system forward along a trajectory"},
    {"word": "propel", "pos": "verb", "orthodox_def": "to drive, push, or cause to move forward under force"},

    # 3. Boundary & Containment (14)
    {"word": "open", "pos": "verb", "orthodox_def": "to unseal or part a boundary to allow passage or access"},
    {"word": "close", "pos": "verb", "orthodox_def": "to seal or bring together a boundary to block passage"},
    {"word": "enter", "pos": "verb", "orthodox_def": "to cross a boundary and come or go into a place"},
    {"word": "leave", "pos": "verb", "orthodox_def": "to depart from a place or boundary; move outside"},
    {"word": "cross", "pos": "verb", "orthodox_def": "to pass from one side of a line or boundary to the other"},
    {"word": "contain", "pos": "verb", "orthodox_def": "to have or hold something within an enclosure or limit"},
    {"word": "store", "pos": "verb", "orthodox_def": "to keep items in an organized container for future retrieval"},
    {"word": "shelter", "pos": "verb", "orthodox_def": "to shield from danger or hostile conditions with a barrier"},
    {"word": "lock", "pos": "verb", "orthodox_def": "to secure a boundary or enclosure so it cannot be opened"},
    {"word": "seal", "pos": "verb", "orthodox_def": "to fasten or close securely so that nothing can pass through"},
    {"word": "block", "pos": "verb", "orthodox_def": "to obstruct or prevent movement through a path or portal"},
    {"word": "breach", "pos": "verb", "orthodox_def": "to make a gap or break through a protective wall or barrier"},
    {"word": "pass", "pos": "verb", "orthodox_def": "to move past or through an obstacle, point, or threshold"},
    {"word": "cover", "pos": "verb", "orthodox_def": "to place something over or upon an object to shield or conceal"},

    # 4. Custody, Possession & Exchange (14)
    {"word": "hold", "pos": "verb", "orthodox_def": "to grasp firmly and support an object against displacement"},
    {"word": "have", "pos": "verb", "orthodox_def": "to possess, hold in custody, or contain as a feature"},
    {"word": "give", "pos": "verb", "orthodox_def": "to transfer custody or possession of something to another"},
    {"word": "take", "pos": "verb", "orthodox_def": "to claim, grasp hold of, and secure possession of something"},
    {"word": "keep", "pos": "verb", "orthodox_def": "to retain possession or maintain in a specified state"},
    {"word": "grab", "pos": "verb", "orthodox_def": "to grasp suddenly and roughly into custody"},
    {"word": "catch", "pos": "verb", "orthodox_def": "to intercept and hold an object moving through space"},
    {"word": "release", "pos": "verb", "orthodox_def": "to set free from confinement, restraint, or custody"},
    {"word": "send", "pos": "verb", "orthodox_def": "to cause to go or be carried to a distant destination"},
    {"word": "receive", "pos": "verb", "orthodox_def": "to accept or take into custody something given or sent"},
    {"word": "bring", "pos": "verb", "orthodox_def": "to carry or accompany something to a place with the speaker"},
    {"word": "trade", "pos": "verb", "orthodox_def": "to exchange goods or services between parties"},
    {"word": "buy", "pos": "verb", "orthodox_def": "to obtain in exchange for payment of currency or value"},
    {"word": "sell", "pos": "verb", "orthodox_def": "to transfer goods to another in exchange for payment"},

    # 5. Assembly & Structure (12)
    {"word": "make", "pos": "verb", "orthodox_def": "to form or construct something by combining parts or materials"},
    {"word": "build", "pos": "verb", "orthodox_def": "to construct an integrated structure by joining parts together"},
    {"word": "break", "pos": "verb", "orthodox_def": "to separate into pieces by sudden force; sever integrity"},
    {"word": "join", "pos": "verb", "orthodox_def": "to connect or fasten two or more things together into one"},
    {"word": "split", "pos": "verb", "orthodox_def": "to divide or break forcibly into two or more parts"},
    {"word": "cut", "pos": "verb", "orthodox_def": "to divide, penetrate, or sever with an edge or blade"},
    {"word": "bind", "pos": "verb", "orthodox_def": "to tie or hold together securely with a band or constraint"},
    {"word": "tie", "pos": "verb", "orthodox_def": "to fasten or attach with string, cord, or knot"},
    {"word": "form", "pos": "verb", "orthodox_def": "to shape or give a specific structure or configuration to"},
    {"word": "shape", "pos": "verb", "orthodox_def": "to mold or fashion into a specific contour or profile"},
    {"word": "tear", "pos": "verb", "orthodox_def": "to pull apart or into pieces by force along a seam"},
    {"word": "crack", "pos": "verb", "orthodox_def": "to break without complete separation of parts; fissure"},

    # 6. Aggregation & Distribution (10)
    {"word": "gather", "pos": "verb", "orthodox_def": "to bring together scattered items into a collective group"},
    {"word": "scatter", "pos": "verb", "orthodox_def": "to disperse or throw in various random directions"},
    {"word": "collect", "pos": "verb", "orthodox_def": "to systematically seek and assemble items of a kind"},
    {"word": "spread", "pos": "verb", "orthodox_def": "to extend over a larger area or distribute across a space"},
    {"word": "fill", "pos": "verb", "orthodox_def": "to make a container full by adding contents up to capacity"},
    {"word": "empty", "pos": "verb", "orthodox_def": "to remove all contents from a container or space"},
    {"word": "pour", "pos": "verb", "orthodox_def": "to flow or cause to flow in a steady stream from a vessel"},
    {"word": "spill", "pos": "verb", "orthodox_def": "to cause or allow to run over the edge of a container"},
    {"word": "pack", "pos": "verb", "orthodox_def": "to cram or fit items densely into a container for storage"},
    {"word": "divide", "pos": "verb", "orthodox_def": "to separate into distinct parts, portions, or categories"},

    # 7. State Transitions & Time (12)
    {"word": "be", "pos": "verb", "orthodox_def": "to exist, hold presence, or occupy a specified state"},
    {"word": "become", "pos": "verb", "orthodox_def": "to undergo a transition and begin to be a new state"},
    {"word": "begin", "pos": "verb", "orthodox_def": "to start an action, operation, or existence from origin"},
    {"word": "start", "pos": "verb", "orthodox_def": "to initiate movement, function, or temporal execution"},
    {"word": "stop", "pos": "verb", "orthodox_def": "to cease movement, operation, or continuation; halt"},
    {"word": "end", "pos": "verb", "orthodox_def": "to bring or come to a final completion or termination"},
    {"word": "continue", "pos": "verb", "orthodox_def": "to persist in an ongoing state or path without stopping"},
    {"word": "stay", "pos": "verb", "orthodox_def": "to remain in the same place or condition over time"},
    {"word": "live", "pos": "verb", "orthodox_def": "to begin, move, and continue actively through time"},
    {"word": "die", "pos": "verb", "orthodox_def": "to fade, halt all motion, and come to a permanent stop"},
    {"word": "grow", "pos": "verb", "orthodox_def": "to absorb inputs, extend structure, and reach capacity"},
    {"word": "change", "pos": "verb", "orthodox_def": "to alter condition, reshape structure, or shift state"},

    # 8. Perception, Cognition & Sign (12)
    {"word": "see", "pos": "verb", "orthodox_def": "to receive light, resolve images, and recognize forms"},
    {"word": "look", "pos": "verb", "orthodox_def": "to direct visual focus or attention toward a target"},
    {"word": "hear", "pos": "verb", "orthodox_def": "to perceive sound waves conducted through a medium"},
    {"word": "listen", "pos": "verb", "orthodox_def": "to actively attend to sound with intention and comprehension"},
    {"word": "feel", "pos": "verb", "orthodox_def": "to register contact, absorb impact, and know state"},
    {"word": "touch", "pos": "verb", "orthodox_def": "to bring into physical contact with another surface"},
    {"word": "know", "pos": "verb", "orthodox_def": "to perceive, verify, and retain information with certainty"},
    {"word": "think", "pos": "verb", "orthodox_def": "to reflect on inputs, weigh options, and formulate conclusions"},
    {"word": "find", "pos": "verb", "orthodox_def": "to search an area, detect a target, and confirm its location"},
    {"word": "choose", "pos": "verb", "orthodox_def": "to select a preferred option from multiple candidate paths"},
    {"word": "say", "pos": "verb", "orthodox_def": "to voice sounds, utter words, and convey clear messages"},
    {"word": "show", "pos": "verb", "orthodox_def": "to display an object or phenomenon so it can be perceived"}
]

def main():
    target_dir = os.path.dirname(__file__)
    output_path = os.path.join(target_dir, "source_dictionary_100.json")

    catalog = {
        "metadata": {
            "title": "QQCI 100-Word Foundational Seed Dictionary",
            "count": len(SEED_WORDS_DATA),
            "description": "100 foundational action, topological, and state words for epistemic primitive extraction",
            "categories": [
                "Kinetic Displacement & Motion",
                "Directional Force Dynamics",
                "Boundary & Containment",
                "Custody, Possession & Exchange",
                "Assembly & Structure",
                "Aggregation & Distribution",
                "State Transitions & Time",
                "Perception, Cognition & Sign"
            ]
        },
        "words": SEED_WORDS_DATA
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"[SUCCESS] Compiled {len(SEED_WORDS_DATA)} seed words to {output_path}")

if __name__ == "__main__":
    main()
