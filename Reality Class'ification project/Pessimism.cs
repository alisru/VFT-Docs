using System;
using TautonicLanguageEngine;

namespace RealityClassificationProject
{
    public class Pessimism : IOperationMode
    {
        public string Name => "Pessimism";
        public Meaning ModeMeaning { get; private set; }
        private Random _rng;

        public Pessimism()
        {
            ModeMeaning = new Meaning(
                word: "Pessimism",
                definitiveMeaning: "Perceptual Inversion: The generation of entropy. Distorts the planes creating infinite strain (Divergence).",
                polarity: Polarity.Negative
            );
            _rng = new Random();
        }

        public void ApplyMode(Idea idea)
        {
            Console.WriteLine($"\n{'=',60}");
            Console.WriteLine($"[APPLYING PESSIMISM] Generating Entropy Field...");
            Console.WriteLine($"{'=',60}");

            // Convert Idea to StateVector for geometric operations
            StateVector initialState = StateVector.FromIdea(idea);
            
            // Display initial geometry
            GeometryVisualizer.PlotState(initialState, "Initial State (Before Pessimism)");
            GeometryVisualizer.Plot3DAxes(initialState);

            Console.WriteLine($"\n[PERCEPTUAL INVERSION] Creating Mountains and Deficits...");

            // Pessimism Strategy: Invert the landscape
            // Instead of pulling toward Unity, push AWAY from Unity
            // Create "Mountains" (excess difficulty) and "Valleys" (deficits)

            StateVector distortedState = new StateVector(
                FieldMath.InvertCoordinate(initialState.Who, _rng),
                FieldMath.InvertCoordinate(initialState.Where, _rng),
                FieldMath.InvertCoordinate(initialState.What, _rng),
                FieldMath.InvertCoordinate(initialState.Why, _rng),
                FieldMath.InvertCoordinate(initialState.How, _rng),
                FieldMath.InvertCoordinate(initialState.Cause, _rng),
                FieldMath.InvertCoordinate(initialState.Effect, _rng)
            );

            // Additional variance jamming: Add noise to physical and logical planes
            // These are the "It's too hard" and "It's too far" distortions
            distortedState.Where += 1.0f + (float)_rng.NextDouble(); // "Constraints are impossible"
            distortedState.How += 1.0f + (float)_rng.NextDouble();   // "Method is too complex"
            
            // Reduce possibility and meaning (Deficits)
            distortedState.What *= 0.5f;  // "Unlikely to succeed"
            distortedState.Why *= 0.5f;   // "Pointless anyway"

            // Update the Idea's beliefs with the distorted coordinates
            idea.Who.Score = distortedState.Who;
            idea.Where.Score = distortedState.Where;
            idea.What.Score = distortedState.What;
            idea.Why.Score = distortedState.Why;
            idea.How.Score = distortedState.How;
            idea.Cause.Score = distortedState.Cause;
            idea.Effect.Score = distortedState.Effect;

            // Display final geometry
            GeometryVisualizer.PlotState(distortedState, "Final State (After Pessimism)");
            GeometryVisualizer.Plot3DAxes(distortedState);
            
            // Show transformation analysis
            GeometryVisualizer.ComparStates(initialState, distortedState, "PESSIMISM (Entropy)");

            // Display the physics interpretation
            Console.WriteLine($"\n[PHYSICS INTERPRETATION]");
            Console.WriteLine($"• Perceptual Inversion created 'Mountains' (high Φ barriers)");
            Console.WriteLine($"• Gradient flattened: ∇Φ ≈ 0 (no clear direction)");
            Console.WriteLine($"• System entropy increased: {FieldMath.CalculateSystemEntropy(initialState):F4} → {FieldMath.CalculateSystemEntropy(distortedState):F4}");
            Console.WriteLine($"• Variance jamming on Q2 (WHERE) and Q5 (HOW) created perceived impossibility");
            Console.WriteLine($"• Result: High strain (σ), zero movement (dS ≈ 0) → Stagnation");
        }

        public float GetGradientProfile(float currentProb)
        {
            // Pessimism creates a flat or inverted gradient
            return 0.0f; // No pull, or negative (repelling)
        }
    }
}
