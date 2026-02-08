using System;
using System.Collections.Generic;

namespace TautonicLanguageEngine
{
    // --- 1. The 7 Vectors Configuration ---

    public enum PlaneOfReality { MetaPhysical, Physical, Possible, Lyrical, Logical, Historical, Emotive }

    public struct MoralVectorDef 
    {
        public string Interrogative;
        public PlaneOfReality Plane;
        public string Virtue;
        public string Sin;
        
        // 421 Structure Metadata
        public string Domain;        // Identity, Soul, Body, Mind
        public string AxisName;      // Driver, Vertical, Lateral, Longitudinal
        public string AxisDirection; // 7th Angle, +z, -z, etc.
        public string Description;   // e.g., "Will and Direction"
        
        // Physics Dynamics
        public string Dynamics;      // "Expansion" (+) or "Contraction" (-)

        public MoralVectorDef(string interrogative, PlaneOfReality plane, string virtue, string sin, 
                              string domain, string axisName, string axisDirection, string description, string dynamics)
        {
            Interrogative = interrogative;
            Plane = plane;
            Virtue = virtue;
            Sin = sin;
            Domain = domain;
            AxisName = axisName;
            AxisDirection = axisDirection;
            Description = description;
            Dynamics = dynamics;
        }
    }

    public static class MoralVectors 
    {
        // THE DRIVER (The Emergent Axis)
        // Soul, body, mind, with who being identity
        public static readonly MoralVectorDef Who = new MoralVectorDef(
            "Who", PlaneOfReality.MetaPhysical, "Sovereignty", "Tyranny",
            "Identity", "Driver", "7th Angle", "Will and Direction", "Expansion"
        );

        // THE LATERAL AXIS (Definition & Space: +/- x) -> Body
        public static readonly MoralVectorDef Where = new MoralVectorDef(
            "Where", PlaneOfReality.Physical, "Thriving", "Mere Survival",
            "Body", "Lateral", "-x", "Matter and Distance", "Contraction"
        );
        public static readonly MoralVectorDef What = new MoralVectorDef(
            "What", PlaneOfReality.Possible, "Stewardship", "Greed",
            "Body", "Lateral", "+x", "Faith and Probability", "Expansion"
        );

        // THE LONGITUDINAL AXIS (Function & Meaning: +/- y) -> Mind
        public static readonly MoralVectorDef Why = new MoralVectorDef(
            "Why", PlaneOfReality.Lyrical, "Truth-Telling", "Delusion",
            "Mind", "Longitudinal", "+y", "Meaning and Resonance", "Expansion"
        );
        public static readonly MoralVectorDef How = new MoralVectorDef(
            "How", PlaneOfReality.Logical, "Wisdom", "Sophistry",
            "Mind", "Longitudinal", "-y", "Count and Consistency", "Contraction"
        );

        // THE VERTICAL AXIS (Temporal Link: +/- z) -> Soul
        public static readonly MoralVectorDef Cause = new MoralVectorDef(
            "Cause", PlaneOfReality.Historical, "Redemption", "Revisionism",
            "Soul", "Vertical", "+z", "Sequence and Causality", "Expansion"
        );
        public static readonly MoralVectorDef Effect = new MoralVectorDef(
            "Effect", PlaneOfReality.Emotive, "Love/Unity", "Parasitism",
            "Soul", "Vertical", "-z", "Passion and Consequence", "Contraction"
        );
    }

    // --- 2. Foundational Classes ---

    public class MoralScore 
    {
        public float Value { get; set; }
        public string Alignment { get; set; }

        public MoralScore(float value, MoralVectorDef vectorDef)
        {
            Value = value;
            // 1.0 = Truth/Virtue
            // > 1.0 = Tyranny/Excess
            // < 1.0 = Entropy/Deficit
            if (Math.Abs(value - 1.0f) < 0.001f) Alignment = vectorDef.Virtue;
            else if (value > 1.0f) Alignment = $"Excess: {vectorDef.Sin}";
            else Alignment = $"Deficit: {vectorDef.Sin}";
        }
    }

    public class Belief 
    {
        public MoralVectorDef VectorType { get; set; }
        public Meaning Answer { get; set; }
        public float Score => Answer.TruthScore;
        public MoralScore MoralAlignment { get; set; }

        public Belief(MoralVectorDef vectorType, Meaning answer)
        {
            VectorType = vectorType;
            Answer = answer;
            MoralAlignment = new MoralScore(answer.TruthScore, vectorType);
        }
    }

    // --- 3. The Idea Class (7-Vector Structure) ---

    public class Idea 
    {
        // The 7 Constituent Vectors of the Fractal Stack
        public Belief Who { get; set; }       // Identity / Filter
        public Belief Where { get; set; }     // Locality / Locus
        public Belief What { get; set; }      // Definition / Substance
        public Belief Why { get; set; }       // Drive / Purpose
        public Belief How { get; set; }       // Method / Process
        public Belief Cause { get; set; }     // Origin / History
        public Belief Effect { get; set; }    // Impact / Consequence

        public List<Belief> Vectors { get; private set; }
        
        // Calculated Net Coherence (R_net) via Protocol
        public float NetCoherence { get; private set; }

        public Idea(Belief who, Belief where, Belief what, Belief why, Belief how, Belief cause, Belief effect)
        {
            Who = who;
            Where = where;
            What = what;
            Why = why;
            How = how;
            Cause = cause;
            Effect = effect;

            Vectors = new List<Belief> { who, where, what, why, how, cause, effect };
            NetCoherence = CalculateFractalRatio();
        }

        public Idea(Meaning who, Meaning where, Meaning what, Meaning why, Meaning how, Meaning cause, Meaning effect)
        {
            Who = new Belief(MoralVectors.Who, who);
            Where = new Belief(MoralVectors.Where, where);
            What = new Belief(MoralVectors.What, what);
            Why = new Belief(MoralVectors.Why, why);
            How = new Belief(MoralVectors.How, how);
            Cause = new Belief(MoralVectors.Cause, cause);
            Effect = new Belief(MoralVectors.Effect, effect);

            Vectors = new List<Belief> { Who, Where, What, Why, How, Cause, Effect };
            NetCoherence = CalculateFractalRatio();
        }

        private float CalculateFractalRatio()
        {
            /*
             * The Fractal Ratio Protocol:
             * R_net = 1 / (Who * Where * What * Why * How * Cause * Effect)
             */
            float product = 1.0f;
            foreach (var v in Vectors)
            {
                product *= v.Score;
            }

            if (product == 0) return float.PositiveInfinity; // Avoid division by zero
            return 1.0f / product;
        }
    }
}
