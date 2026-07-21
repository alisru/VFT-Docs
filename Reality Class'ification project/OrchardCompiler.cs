using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using TautonicLanguageEngine;
using RealityClassification;

namespace TautonicLanguageEngine.SAEL
{
    // =========================================================================
    // PLANE OF REALITY: Abstract class hierarchy.
    // Each plane carries three distinct functional roles in convergence:
    //   Interrogative  = the question that carves the hole (drives accretion)
    //   PlaneName      = type constraint on the domain of valid answers
    //   FundamentalName = contextual anchor — what other things are relative TO and BETWEEN
    // =========================================================================
    public abstract class PlaneOfReality
    {
        public abstract string Interrogative    { get; } // The question (Who/What/Where/Why/How/Cause/Effect)
        public abstract string PlaneName        { get; } // The reality domain type
        public abstract string FundamentalName  { get; } // The contextual anchor for relational meaning
        public abstract string AxisDescription  { get; } // Will and Direction / Faith and Probability / etc.
    }

    // Q1 — Who
    public class MetaPhysical : PlaneOfReality
    {
        public override string Interrogative   => "Who";
        public override string PlaneName       => "MetaPhysical";
        public override string FundamentalName => "Identity";
        public override string AxisDescription => "Will and Direction";
    }

    // Q2 — What
    public class Possible : PlaneOfReality
    {
        public override string Interrogative   => "What";
        public override string PlaneName       => "Possible";
        public override string FundamentalName => "Possible";
        public override string AxisDescription => "Faith and Probability";
    }

    // Q3 — Where
    public class Physical : PlaneOfReality
    {
        public override string Interrogative   => "Where";
        public override string PlaneName       => "Physical";
        public override string FundamentalName => "Location";
        public override string AxisDescription => "Matter and Distance";
    }

    // Q4 — Why
    public class Lyrical : PlaneOfReality
    {
        public override string Interrogative   => "Why";
        public override string PlaneName       => "Lyrical";
        public override string FundamentalName => "Meaning";
        public override string AxisDescription => "Meaning and Resonance";
    }

    // Q5 — How
    public class Logical : PlaneOfReality
    {
        public override string Interrogative   => "How";
        public override string PlaneName       => "Logical";
        public override string FundamentalName => "Mechanical";
        public override string AxisDescription => "Count and Consistency";
    }

    // Q6 — Cause
    public class Historical : PlaneOfReality
    {
        public override string Interrogative   => "Cause";
        public override string PlaneName       => "Historical";
        public override string FundamentalName => "Historical";
        public override string AxisDescription => "Sequence and Causality";
    }

    // Q7 — Effect
    public class Emotive : PlaneOfReality
    {
        public override string Interrogative   => "Effect";
        public override string PlaneName       => "Emotive";
        public override string FundamentalName => "Emotive";
        public override string AxisDescription => "Passion and Consequence";
    }

    // =========================================================================
    // ORCHARD COMPILER: Generative C# class emitter.
    // Reads from MeaningMetaRegistry and synthesizes Plant classes on disk
    // inside the Q-plane Garden namespace they belong to.
    // =========================================================================
    public static class OrchardCompiler
    {
        private static string GardensPath => Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "Gardens");

        public static void EmitPlantClass(string gardenName, string plantName, Plane targetPlane)
        {
            string dir = Path.Combine(GardensPath, gardenName);
            if (!Directory.Exists(dir))
                Directory.CreateDirectory(dir);

            string filePath = Path.Combine(dir, $"{plantName}Plant.cs");
            if (File.Exists(filePath)) return;

            string classCode = $@"using System;
using System.Collections.Generic;
using TautonicLanguageEngine;
using TautonicLanguageEngine.SAEL;
using RealityClassification;

namespace RealityClassification.Gardens.{gardenName}
{{
    // Plant growing in {gardenName} Garden (Q-Plane: {targetPlane})
    // Each Belief<T> slot is typed to a PlaneOfReality, encoding:
    //   - The interrogative question that must be answered to fill the slot
    //   - The plane type constraining what kind of answer is valid
    //   - The fundamental name anchoring cross-plane relational meaning
    public class {plantName}Plant
    {{
        // Q1 interrogative: Who?  | Plane: MetaPhysical | Anchor: Identity
        public Belief<MetaPhysical> Identity    {{ get; set; }}
        // Q2 interrogative: What? | Plane: Possible     | Anchor: Possible
        public Belief<Possible>     Possibility {{ get; set; }}
        // Q3 interrogative: Where?| Plane: Physical     | Anchor: Location
        public Belief<Physical>     Location    {{ get; set; }}
        // Q4 interrogative: Why?  | Plane: Lyrical      | Anchor: Meaning
        public Belief<Lyrical>      Meaning     {{ get; set; }}
        // Q5 interrogative: How?  | Plane: Logical      | Anchor: Mechanical
        public Belief<Logical>      Mechanical  {{ get; set; }}
        // Q6 interrogative: Cause?| Plane: Historical   | Anchor: Historical
        public Belief<Historical>   Sequence    {{ get; set; }}
        // Q7 interrogative: Effect?| Plane: Emotive     | Anchor: Emotive
        public Belief<Emotive>      Passion     {{ get; set; }}

        public Plane BasePlane => Plane.{targetPlane};

        public Idea YieldFruit(ModalPosition position, List<Meaning> accretions)
        {{
            // Fruit executes logic over accretions and returns the 7-plane Idea Seed
            return new Idea(
                Identity?.Answer,
                Location?.Answer,
                Possibility?.Answer,
                Meaning?.Answer,
                Mechanical?.Answer,
                Sequence?.Answer,
                Passion?.Answer
            );
        }}
    }}
}}";
            File.WriteAllText(filePath, classCode);
            Console.WriteLine($"[Orchard] Synthesized: {gardenName}.{plantName} (BasePlane={targetPlane})");
        }
    }
}
