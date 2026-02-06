using System;
using System.Collections.Generic;

namespace TautonicLanguageEngine
{
    // --- Fundamental Meaning Type ---
    public class Meaning
    {
        public string Word { get; set; }              // Word form
        public string DefinitiveMeaning { get; set; } // Axomic meaning
        public string Pronunciation { get; set; }     // Optional phonetics
        public Polarity Polarity { get; set; }        // Positive / Negative / Neutral
        public List<Meaning> SubMeanings { get; set; } // Derived / component meanings
        public List<(string RelatedWord, SemanticRelation Relation)> Related { get; set; }

        // Axomic / Semantic Registry Info
        public int AxomicID { get; set; }
        public int WordLayer { get; set; }
        public int PhraseLayer { get; set; }
        public int LanguageLayer { get; set; }
        public int TemporalLayer { get; set; }
        public int RegistryLayer { get; set; }

        public Meaning(string word, string definitiveMeaning = null, Polarity polarity = Polarity.Neutral,
            int axomicID = -1, int wordLayer = 0, int phraseLayer = 0, int languageLayer = 0,
            int temporalLayer = -1, int registryLayer = 0)
        {
            Word = word;
            DefinitiveMeaning = definitiveMeaning ?? word;
            Polarity = polarity;
            SubMeanings = new List<Meaning>();
            Related = new List<(string, SemanticRelation)>();

            // Assign Axomic registry positions
            AxomicID = axomicID >= 0 ? axomicID : new Random().Next(1_000_000);
            WordLayer = wordLayer;
            PhraseLayer = phraseLayer;
            LanguageLayer = languageLayer;
            TemporalLayer = temporalLayer >= 0 ? temporalLayer : DateTime.UtcNow.DayOfYear;
            RegistryLayer = registryLayer;

            // Auto-register in 6D meta-dictionary
            MeaningMetaRegistry.AddMeaning(AxomicID, WordLayer, PhraseLayer, LanguageLayer, TemporalLayer, RegistryLayer, this);
        }

        // Convenience: Add related meaning
        public void AddRelated(Meaning meaning, SemanticRelation relation)
        {
            Related.Add((meaning.Word, relation));
        }
    }

    // --- Word Class (linked to Meaning) ---
    public class Word
    {
        public string Symbol { get; set; }
        public Meaning Meaning { get; set; }

        public Word(string symbol, Meaning meaning)
        {
            Symbol = symbol;
            Meaning = meaning;

            // Auto-register in 6D meta-dictionary at same layers as meaning
            MeaningMetaRegistry.AddMeaning(
                meaning.AxomicID,
                meaning.WordLayer,
                meaning.PhraseLayer,
                meaning.LanguageLayer,
                meaning.TemporalLayer,
                meaning.RegistryLayer,
                meaning
            );
        }
    }

    // --- Polarity / Semantic Enums ---
    public enum Polarity { Neutral, Positive, Negative, Mixed }
    public enum SemanticRelation { Similar, Equivalent, Derivative, Opposite, None }

    // --- 6D Meta-Dictionary ---
    using CharLayer = Dictionary<int, Meaning>;
    using WordLayer = Dictionary<int, CharLayer>;
    using PhraseLayer = Dictionary<int, WordLayer>;
    using LanguageLayer = Dictionary<int, PhraseLayer>;
    using TemporalLayer = Dictionary<int, LanguageLayer>;
    using RegistryLayer = Dictionary<int, TemporalLayer>;

    public static class MeaningMetaRegistry
    {
        private static RegistryLayer _registry = new();

        public static void AddMeaning(int axomicID, int wordLayer, int phraseLayer, int langLayer, int temporalLayer, int registryLayer, Meaning meaning)
        {
            if (!_registry.ContainsKey(axomicID)) _registry[axomicID] = new TemporalLayer();
            var temporal = _registry[axomicID];

            if (!temporal.ContainsKey(temporalLayer)) temporal[temporalLayer] = new LanguageLayer();
            var lang = temporal[temporalLayer];

            if (!lang.ContainsKey(langLayer)) lang[langLayer] = new PhraseLayer();
            var phrase = lang[langLayer];

            if (!phrase.ContainsKey(phraseLayer)) phrase[phraseLayer] = new WordLayer();
            var word = phrase[phraseLayer];

            if (!word.ContainsKey(wordLayer)) word[wordLayer] = new CharLayer();
            var chars = word[wordLayer];

            chars[registryLayer] = meaning;
        }

        public static Meaning GetMeaning(int axomicID, int wordLayer, int phraseLayer, int langLayer, int temporalLayer, int registryLayer)
        {
            try { return _registry[axomicID][temporalLayer][langLayer][phraseLayer][wordLayer][registryLayer]; }
            catch { return null; }
        }

        public static Meaning GetByWord(string word)
        {
            foreach (var tLayer in _registry.Values)
                foreach (var lLayer in tLayer.Values)
                    foreach (var pLayer in lLayer.Values)
                        foreach (var wLayer in pLayer.Values)
                            foreach (var cLayer in wLayer.Values)
                                foreach (var meaning in cLayer.Values)
                                    if (meaning.Word == word) return meaning;
            return null;
        }

        public static Meaning GetByMeaning(string definitiveMeaning)
        {
            foreach (var tLayer in _registry.Values)
                foreach (var lLayer in tLayer.Values)
                    foreach (var pLayer in lLayer.Values)
                        foreach (var wLayer in pLayer.Values)
                            foreach (var cLayer in wLayer.Values)
                                foreach (var meaning in cLayer.Values)
                                    if (meaning.DefinitiveMeaning == definitiveMeaning) return meaning;
            return null;
        }
    }
    // --- VFT Integration: Judgement & Synergy ---

    public static class Judgement
    {
        public static string Evaluate(Idea idea, float tolerance = 0.1f)
        {
            /*
             * The Coherence Gate Axiom:
             * [Q|A / A|Q] === { Y=1; N!=1; Insult > 1 }
             */
            float ratio = idea.NetCoherence;

            if (ratio >= (1.0f - tolerance) && ratio <= (1.0f + tolerance))
            {
                return "Y=1 (TRUTH)";
            }
            else if (ratio > (1.0f + tolerance))
            {
                return "INSULT > 1 (CHAOS/TYRANNY)";
            }
            else
            {
                return "N != 1 (LIE/ENTROPY)";
            }
        }
    }

    // Extensions for Meaning to act as CPU
    public partial class Meaning
    {
        public static int ProcessSynergy(int worldviewState, Idea newTruth)
        {
            /*
             * The Belief Axiom:
             * Belief = 1 + 1 = 2
             */
            string gateResult = Judgement.Evaluate(newTruth);

            if (gateResult.Contains("TRUTH"))
            {
                // SYNERGY EVENT: The consciousness expands
                return worldviewState + 1;
            }
            else
            {
                // REJECTION EVENT
                return worldviewState;
            }
        }
    }
}
