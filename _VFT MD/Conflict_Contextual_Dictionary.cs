using System;
using System.Collections.Generic;
using TautonicLanguageEngine;

namespace ConflictTensors
{
    /// <summary>
    /// The Conflict Contextual Dictionary maps the 7x7x7 Conflict Tensor
    /// to the Tautonic Language Engine's Meaning and Word classes.
    /// This file contains the C# representation of the Conflict Tiers.
    /// </summary>
    public static class ConflictDictionary
    {
        public static void Initialize()
        {
            // --- PRIMARY TIER DEFINITIONS (Q1-Q7) ---

            // Q1: Personal Conflict (T1: The Gun)
            var m_tier1 = new Meaning(
                word: "Personal Conflict",
                definitiveMeaning: "Conflict centering on individual agency and physical threat. The Gun.",
                polarity: Polarity.Neutral,
                axomicID: 7001,
                wordLayer: 1, // Q1
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7 // Type 7
            );
            new Word("T1", m_tier1);

            // Q2: Team Conflict (T2: The Artillery)
            var m_tier2 = new Meaning(
                word: "Team Conflict",
                definitiveMeaning: "Conflict involving crews, shared goals, and coordination. The Artillery.",
                polarity: Polarity.Neutral,
                axomicID: 7002,
                wordLayer: 2, // Q2
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7
            );
            new Word("T2", m_tier2);

            // Q3: Strategic Conflict (T3: The Bomb)
            var m_tier3 = new Meaning(
                word: "Strategic Conflict",
                definitiveMeaning: "Conflict at the scale of geography, infrastructure, and bypass. The Bomb.",
                polarity: Polarity.Neutral,
                axomicID: 7003,
                wordLayer: 3, // Q3
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7
            );
            new Word("T3", m_tier3);

            // Q4: Automated Conflict (T4: The Missile)
            var m_tier4 = new Meaning(
                word: "Automated Conflict",
                definitiveMeaning: "Conflict driven by code, automation, and remote agency. The Missile.",
                polarity: Polarity.Neutral,
                axomicID: 7004,
                wordLayer: 4, // Q4
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7
            );
            new Word("T4", m_tier4);

            // Q5: Existential Conflict (T5: The Nuke)
            var m_tier5 = new Meaning(
                word: "Existential Conflict",
                definitiveMeaning: "Conflict involving total breakdown, logic failure, and annihilation. The Nuke.",
                polarity: Polarity.Negative,
                axomicID: 7005,
                wordLayer: 5, // Q5
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7
            );
            new Word("T5", m_tier5);

            // Q6: Abstract Warfare (T6: Systemic)
            var m_tier6 = new Meaning(
                word: "Abstract Warfare",
                definitiveMeaning: "Warfare conducted via systemic disruption and information control.",
                polarity: Polarity.Mixed,
                axomicID: 7006,
                wordLayer: 6, // Q6
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7
            );
            new Word("T6", m_tier6);

            // Q7: Truth Warfare (T7: Aletheia)
            var m_tier7 = new Meaning(
                word: "Truth Warfare",
                definitiveMeaning: "Winning via the unconcealment of reality. Pure Effect.",
                polarity: Polarity.Positive,
                axomicID: 7007,
                wordLayer: 7, // Q7
                phraseLayer: 0,
                languageLayer: 0,
                registryLayer: 7
            );
            new Word("T7", m_tier7);
        }
    }
}
