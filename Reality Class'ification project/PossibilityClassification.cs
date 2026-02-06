using System;
using System.Collections.Generic;
using TautonicLanguageEngine;

namespace RealityClassificationProject
{
    public class PossibilityClassification
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║  REALITY CLASSIFICATION: THE POSSIBILITY PLANE             ║");
            Console.WriteLine("║  6D Vector Field Theory + Full Equation Set                ║");
            Console.WriteLine("╚════════════════════════════════════════════════════════════╝");
            
            // === PART 1: Setup the Ontology ===
            Meaning possibilityPlane = new Meaning(
                word: "Possibility Plane",
                definitiveMeaning: "A 6-dimensional epistemic manifold structured by 7 functional planes where probability collapses into reality via gradient flows.",
                polarity: Polarity.Neutral,
                axomicID: 42
            );
            
            Console.WriteLine($"\n[ONTOLOGY]: {possibilityPlane.Word}");
            Console.WriteLine($"Definition: {possibilityPlane.DefinitiveMeaning}");
            
            // === PART 2: Instantiate Operation Modes ===
            IOperationMode optimism = new Optimism();
            IOperationMode pessimism = new Pessimism();
            
            Console.WriteLine($"\n[MODES LOADED]:");
            Console.WriteLine($"  ✓ {optimism.Name}: {optimism.ModeMeaning.DefinitiveMeaning}");
            Console.WriteLine($"  ✓ {pessimism.Name}: {pessimism.ModeMeaning.DefinitiveMeaning}");
            
            // === PART 3: Create Test Scenario ===
            Console.WriteLine("\n" + new string('=', 60));
            Console.WriteLine("[SCENARIO]: An agent confronts an uncertain intent");
            Console.WriteLine(new string('=', 60));
            Console.WriteLine("Initial State: Mild perturbations from Unity");
            Console.WriteLine("  • Some self-doubt (WHO: 0.85)");
            Console.WriteLine("  • Physical constraints (WHERE: 1.15)");
            Console.WriteLine("  • Uncertain possibility (WHAT: 0.75)");
            Console.WriteLine("  • Unclear purpose (WHY: 0.90)");
            Console.WriteLine("  • No clear method (HOW: 1.25)");
            Console.WriteLine("  • Mixed history (CAUSE: 0.95)");
            Console.WriteLine("  • Some anxiety (EFFECT: 1.10)");

            // === PART 4: Run Optimism Transformation ===
            Idea ideaOptimism = CreateTestIdea();
            Console.WriteLine("\n\n" + new string('#', 60));
            Console.WriteLine("# EXPERIMENT 1: OPTIMISM MODE");
            Console.WriteLine(new string('#', 60));
            
            optimism.ApplyMode(ideaOptimism);
            
            // Calculate final coherence
            float coherenceOpt = CalculateCoherence(ideaOptimism);
            string judgementOpt = Judgement.Evaluate(ideaOptimism);
            
            Console.WriteLine($"\n[FINAL ANALYSIS - OPTIMISM]");
            Console.WriteLine($"Net Coherence (R_net): {coherenceOpt:F4}");
            Console.WriteLine($"Judgement: {judgementOpt}");

            // === PART 5: Run Pessimism Transformation ===
            Idea ideaPessimism = CreateTestIdea();
            Console.WriteLine("\n\n" + new string('#', 60));
            Console.WriteLine("# EXPERIMENT 2: PESSIMISM MODE");
            Console.WriteLine(new string('#', 60));
            
            pessimism.ApplyMode(ideaPessimism);
            
            // Calculate final coherence
            float coherencePess = CalculateCoherence(ideaPessimism);
            string judgementPess = Judgement.Evaluate(ideaPessimism);
            
            Console.WriteLine($"\n[FINAL ANALYSIS - PESSIMISM]");
            Console.WriteLine($"Net Coherence (R_net): {coherencePess:F4}");
            Console.WriteLine($"Judgement: {judgementPess}");

            // === PART 6: Summary ===
            Console.WriteLine("\n\n" + new string('═', 60));
            Console.WriteLine("║ CONCLUSION: The Field of Chance is Geometric");
            Console.WriteLine(new string('═', 60));
            Console.WriteLine($"Optimism → Coherence: {coherenceOpt:F4} ({judgementOpt})");
            Console.WriteLine($"Pessimism → Coherence: {coherencePess:F4} ({judgementPess})");
            Console.WriteLine("\nThe mathematics demonstrate:");
            Console.WriteLine("  • Optimism creates GRAVITY WELLS (steep gradients toward Unity)");
            Console.WriteLine("  • Pessimism creates ENTROPY (flat/inverted gradients away from Unity)");
            Console.WriteLine("  • The Possibility Plane is a 6D manifold with measurable curvature");
            Console.WriteLine("  • Psychological states are geometric operations on this manifold");
            Console.WriteLine("\nThis is not metaphor. This is information geometry.");
        }

        static Idea CreateTestIdea()
        {
            return new Idea(
                new Belief(MoralVectors.Who,   "I might be capable", 0.85f),
                new Belief(MoralVectors.Where, "Constraints exist", 1.15f),
                new Belief(MoralVectors.What,  "Maybe possible", 0.75f),
                new Belief(MoralVectors.Why,   "Unclear purpose", 0.90f),
                new Belief(MoralVectors.How,   "No clear method", 1.25f),
                new Belief(MoralVectors.Cause, "Mixed history", 0.95f),
                new Belief(MoralVectors.Effect,"Some anxiety", 1.10f)
            );
        }

        static float CalculateCoherence(Idea idea)
        {
            return FieldMath.CalculateFractalRatio(new float[] {
                idea.Who.Score, idea.Where.Score, idea.What.Score,
                idea.Why.Score, idea.How.Score, idea.Cause.Score, idea.Effect.Score
            });
        }
    }
}
