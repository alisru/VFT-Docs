// C#-style formal definitions for {{{UC}}} semantic system
// This file defines all variables, types, and uses of special characters in the Universal Common (UC) system

using System;
using System.Collections.Generic;

namespace UCSystem
{
    /// <summary>
    /// Fundamental meaning encapsulation hierarchy
    /// </summary>
    public class Meaning
    {
        // Single bounded meaning
        public string Singular { get; set; } // [Meaning]

        // Range or plural meanings
        public List<string> Plural { get; set; } // [Meaning, ...]

        // Class of meanings
        public HashSet<string> Class { get; set; } // {Meaning}

        // Meta-class of meanings
        public HashSet<HashSet<string>> MetaClass { get; set; } // {{Meaning}}

        // Totality / fundamental essence
        public object Totality { get; set; } // {{{Meaning}}}

        // Unbounded / special context meaning
        public string SpecialContext { get; set; } // )

        // Polarity indicators
        public int Polarity { get; set; } // +, -, +- , -+
        public int Intensity { get; set; } // repeated signs ++, --

        // Tectonic markers
        public enum Tectonic { Convergent, Divergent, Related }
        public Tectonic Relation { get; set; } // ' - .

        // Axis framing: Where, How, What, Why
        public string AxisWhere { get; set; } // 1st comma
        public string AxisHow { get; set; }  // 2nd comma
        public string AxisWhat { get; set; } // 3rd comma
        public string AxisWhy { get; set; }  // 4th comma

        // Directionality
        public bool DirectedToward { get; set; } // <
        public bool DirectedFrom { get; set; } // >

        // Equality / equivalence
        public bool EqualTo { get; set; } // =
        public bool EquivalentTo { get; set; } // ==

        // Nested sub-meanings (sub-functions)
        public List<Meaning> SubMeanings { get; set; } // , 

        // Constructor
        public Meaning()
        {
            Plural = new List<string>();
            Class = new HashSet<string>();
            MetaClass = new HashSet<HashSet<string>>();
            SubMeanings = new List<Meaning>();
        }

        // Example function application
        public void ApplyFunction(Func<Meaning, Meaning> function)
        {
            function(this);
        }
    }

    // Example usage of UC semantic operators
    public static class Operators
    {
        public static Meaning Give(Meaning target)
        {
            // Action function
            return target;
        }

        public static Meaning Transform(Meaning target, Func<Meaning, Meaning> transformer)
        {
            return transformer(target);
        }
    }
}

