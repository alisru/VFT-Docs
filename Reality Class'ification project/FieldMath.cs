using System;

namespace RealityClassificationProject
{
    /// <summary>
    /// Implements the core mathematical equations from 'The Field of Chance'.
    /// </summary>
    public static class FieldMath
    {
        // === 1. Resolution Time & Convergence ===

        /// <summary>
        /// Calculates the Resolution Time (tau) required for convergence.
        /// Derived from: Convergence Rate proportional to N / sigma^2
        /// </summary>
        public static float CalculateResolutionTime(float currentCertainty, float targetCertainty, float variance, float efficiency)
        {
            // tau ~ (Target - Current) * Variance / Efficiency
            // If Efficiency is high, Tau is low (fast).
            // If Variance is high, Tau is high (slow).
            if (efficiency <= 0.001f) efficiency = 0.001f; // Prevent div by zero
            return Math.Abs(targetCertainty - currentCertainty) * variance / efficiency;
        }

        // === 2. Bayesian Inference ===

        /// <summary>
        /// Updates belief based on new evidence (Q4/Q6).
        /// P(S|Data) propto P(Data|S) * P(S)
        /// </summary>
        public static float CalculatePosterior(float prior, float likelihood)
        {
            // Simplified Bayesian update for scalar probabilities [0,1]
            // Post = (Likelihood * Prior) / Normalizer
            // We'll use a simplified formulation for simulation:
            // Post = Prior + (Likelihood - Prior) * LearningRate
            float learningRate = 0.1f; // Standard update step
            return prior + (likelihood - prior) * learningRate;
        }

        // === 3. Possigravity (The Potential Field) ===

        /// <summary>
        /// Calculates the Potential function Phi(S).
        /// Phi(S) = -log P(S | Data)
        /// </summary>
        public static float CalculatePotential(float probability)
        {
            if (probability <= 0) return 100f; // High potential (barrier) for 0 prob
            return -(float)Math.Log(probability);
        }

        /// <summary>
        /// Calculates Possigravity Force (Gradient of Potential).
        /// F = -Grad(Phi)
        /// Positive F pulls towards higher probability.
        /// </summary>
        public static float CalculatePossigravity(float probability, float targetProbability)
        {
            float phiCurrent = CalculatePotential(probability);
            float phiTarget = CalculatePotential(targetProbability);
            
            // Gradient is slope: -(Delta Phi / Delta S)
            // Here we treat distance as 1 unit for simplicity
            return -(phiTarget - phiCurrent); 
        }

        // === 4. Entropy & Resistance ===

        /// <summary>
        /// Calculates Entropy (Resistance/Strain).
        /// H(S) = -Sum(p log p)
        /// In VFT context: Deviation from Unity (1.0)
        /// </summary>
        public static float CalculateVFTEntropy(float vectorScore)
        {
            // VFT Definition: Truth is the ratio of 1.
            // Entropy is the distance from 1.0.
            return Math.Abs(vectorScore - 1.0f);
        }

        /// <summary>
        /// The Fractal Ratio Protocol (Re-implemented for math utility)
        /// R_net = 1 / Product(Vectors)
        /// </summary>
        public static float CalculateFractalRatio(float[] vectorScores)
        {
            float product = 1.0f;
            foreach (float s in vectorScores) product *= s;
            if (product == 0) return float.PositiveInfinity;
            return 1.0f / product;
        }

        // === 5. Vector Operations ===

        /// <summary>
        /// Calculates the gradient vector (Possigravity force field).
        /// Returns the direction and magnitude of pull toward target state.
        /// </summary>
        public static StateVector CalculateGradientVector(StateVector current, StateVector target)
        {
            return new StateVector(
                (target.Who - current.Who) * 0.5f,      // Willpower gradient
                (target.Where - current.Where) * 0.5f,  // Physical gradient
                (target.What - current.What) * 0.5f,    // Possibility gradient
                (target.Why - current.Why) * 0.5f,      // Meaning gradient
                (target.How - current.How) * 0.5f,      // Method gradient
                (target.Cause - current.Cause) * 0.5f,  // Historical gradient
                (target.Effect - current.Effect) * 0.5f // Emotional gradient
            );
        }

        /// <summary>
        /// Applies a gradient flow update: S_new = S_old + dt * (-∇Φ)
        /// </summary>
        public static StateVector ApplyGradientFlow(StateVector current, StateVector gradient, float learningRate = 0.1f)
        {
            return new StateVector(
                current.Who + gradient.Who * learningRate,
                current.Where + gradient.Where * learningRate,
                current.What + gradient.What * learningRate,
                current.Why + gradient.Why * learningRate,
                current.How + gradient.How * learningRate,
                current.Cause + gradient.Cause * learningRate,
                current.Effect + gradient.Effect * learningRate
            );
        }

        // === 6. Complete Bayesian Inference Loop ===

        /// <summary>
        /// Performs a full Bayesian update cycle on a StateVector.
        /// Incorporates: Prior (Q1), Evidence (Q6), Variance (Q2), etc.
        /// </summary>
        public static StateVector BayesianUpdate(StateVector prior, float[] evidence, float learningRate = 0.1f)
        {
            // Simplified: Each evidence point slightly shifts belief toward Unity
            // In full implementation, this would use proper likelihood functions
            StateVector posterior = prior;
            
            foreach (float e in evidence)
            {
                // Update each coordinate based on evidence
                float evidenceStrength = e; // Normalize [0,1]
                
                posterior.What = posterior.What + (evidenceStrength - posterior.What) * learningRate;
                // ... (similar for other coordinates)
            }
            
            return posterior;
        }

        // === 7. The 7-Plane Bending Mechanics ===

        /// <summary>
        /// Simulates "bending" a plane toward a target using Possigravity.
        /// Returns the bent/corrected value.
        /// </summary>
        public static float BendTowardUnity(float currentValue, float intensity = 0.8f)
        {
            // Pull toward 1.0 with given intensity
            return currentValue + (1.0f - currentValue) * intensity;
        }

        /// <summary>
        /// Inverts a coordinate (Pessimism operation).
        /// Creates "mountains" (excess > 1) or "deficits" (shortage < 1).
        /// </summary>
        public static float InvertCoordinate(float currentValue, Random rng)
        {
            // If already near Unity, push it away
            if (currentValue > 0.5f && currentValue < 1.5f)
            {
                // Push to extremes
                return rng.NextDouble() > 0.5 
                    ? currentValue * 0.5f          // Create deficit
                    : currentValue + 1.0f + (float)rng.NextDouble(); // Create mountain
            }
            return currentValue;
        }

        // === 8. Information Measures ===

        /// <summary>
        /// Calculates Shannon entropy H = -Σ p log p for a probability distribution.
        /// </summary>
        public static float CalculateShannonEntropy(float[] probabilities)
        {
            float entropy = 0;
            foreach (float p in probabilities)
            {
                if (p > 0) entropy -= p * (float)Math.Log(p);
            }
            return entropy;
        }

        /// <summary>
        /// Calculates the total system entropy as deviation from Unity across all coordinates.
        /// </summary>
        public static float CalculateSystemEntropy(StateVector state)
        {
            return state.DistanceFromUnity();
        }
    }
}
