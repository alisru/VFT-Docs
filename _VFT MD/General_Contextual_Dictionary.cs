using System;
using System.Collections.Generic;
using TautonicLanguageEngine;

namespace SystemLexicon
{
    /// <summary>
    /// The General System Lexicon collates specific meaning interpretations
    /// into formal C# Meaning and Word objects.
    /// </summary>
    public static class GlobalLexicon
    {
        public static void Initialize()
        {
            // --- COLLATED INTERPRETATIONS ---
            
            // Example of a collated term from the "360 Degree Meaning" discussion
            var m_circleOfDefinition = new Meaning(
                word: "Circle of Definition",
                definitiveMeaning: "The 360-degree boundary of meaning where truth resolves to unity. Pi-resonance.",
                polarity: Polarity.Positive,
                axomicID: 1001,
                wordLayer: 7, // Effect
                phraseLayer: 4, // Lyrical
                languageLayer: 5, // Logical
                registryLayer: 0 // General
            );
            new Word("CircleDef", m_circleOfDefinition);
        }
    }
}
