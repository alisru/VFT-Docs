using System;
using TautonicLanguageEngine;

namespace RealityClassificationProject
{
    public class Optimism : IOperationMode
    {
        public string Name => "Optimism";
        public Meaning ModeMeaning { get; private set; }

        public Optimism()
        {
            ModeMeaning = new Meaning(
                word: "Optimism",
                definitiveMeaning: "Possigravity: The generation of mass/certainty. Bends the 7 planes toward the intended outcome (Convergence).",
                polarity: Polarity.Positive
            );
        }

        public void ApplyMode(Idea idea)
        {
            Console.WriteLine($"\n{'=',60}");
            Console.WriteLine($"[APPLYING OPTIMISM] Generating Possigravity Field...");
            Console.WriteLine($"{'=',60}");

            // Convert Idea to StateVector for geometric operations
            StateVector initialState = StateVector.FromIdea(idea);
            
            // Display initial geometry
            GeometryVisualizer.PlotState(initialState, "Initial State (Before Optimism)");
            GeometryVisualizer.Plot3DAxes(initialState);

            // Define Unity as the target attractor
            StateVector unity = new StateVector(1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f);

            // Calculate Possigravity gradient (force toward Unity)
            StateVector gradient = FieldMath.CalculateGradientVector(initialState, unity);
            
            Console.WriteLine($"\n[POSSIGRAVITY GRADIENT]");
            Console.WriteLine($"Force Vector: {gradient}");
            
            // Apply gradient flow with high learning rate (strong Optimism = high efficiency)
            float optimismIntensity = 0.8f; // 80% pull per iteration
            StateVector finalState = FieldMath.ApplyGradientFlow(initialState, gradient, optimismIntensity);

            // Update the Idea's beliefs with the new coordinates
            idea.Who.Score = finalState.Who;
            idea.Where.Score = finalState.Where;
            idea.What.Score = finalState.What;
            idea.Why.Score = finalState.Why;
            idea.How.Score = finalState.How;
            idea.Cause.Score = finalState.Cause;
            idea.Effect.Score = finalState.Effect;

            // Display final geometry
            GeometryVisualizer.PlotState(finalState, "Final State (After Optimism)");
            GeometryVisualizer.Plot3DAxes(finalState);
            
            // Show transformation analysis
            GeometryVisualizer.ComparStates(initialState, finalState, "OPTIMISM (Possigravity)");

            // Display the physics interpretation
            Console.WriteLine($"\n[PHYSICS INTERPRETATION]");
            Console.WriteLine($"• Possigravity created a 'Gravity Well' at Unity (1,1,1,1,1,1,1)");
            Console.WriteLine($"• All 7 planes bent toward the attractor basin");
            Console.WriteLine($"• System entropy decreased: {FieldMath.CalculateSystemEntropy(initialState):F4} → {FieldMath.CalculateSystemEntropy(finalState):F4}");
            Console.WriteLine($"• Convergence achieved through gradient descent on probability manifold");
        }

        public float GetGradientProfile(float currentProb)
        {
            // Optimism creates a steep gradient (Deep Well)
            return FieldMath.CalculatePossigravity(currentProb, 1.0f);
        }
    }
}
