using System;
using TautonicLanguageEngine;

namespace RealityClassificationProject
{
    /// <summary>
    /// Represents a point in the 6D Possibility Space.
    /// Coordinates map to the 3-axis Cartesian structure:
    /// X-axis (Lateral): What (+x) / Where (-x)
    /// Y-axis (Longitudinal): Why (+y) / How (-y)  
    /// Z-axis (Vertical): Cause (+z) / Effect (-z)
    /// </summary>
    public class StateVector
    {
        // === The 6 Coordinates ===
        public float Where { get; set; }  // -x: Physical constraints (variance σ²)
        public float What { get; set; }   // +x: Possibility space (trial domain)
        public float Why { get; set; }    // +y: Meaning/Purpose (Bayesian update)
        public float How { get; set; }    // -y: Method/Process (convergence rate λ)
        public float Cause { get; set; }  // +z: Historical data (trial count N)
        public float Effect { get; set; } // -z: Projected outcome (risk tolerance)

        // === The Observer Parameter (WHO - Q1) ===
        public float Who { get; set; }    // Prior probability / Intent bias

        public StateVector(float who, float where, float what, float why, float how, float cause, float effect)
        {
            Who = who;
            Where = where;
            What = what;
            Why = why;
            How = how;
            Cause = cause;
            Effect = effect;
        }

        /// <summary>
        /// Constructs a StateVector from an Idea's Belief scores.
        /// </summary>
        public static StateVector FromIdea(Idea idea)
        {
            return new StateVector(
                idea.Who.Score,
                idea.Where.Score,
                idea.What.Score,
                idea.Why.Score,
                idea.How.Score,
                idea.Cause.Score,
                idea.Effect.Score
            );
        }

        /// <summary>
        /// Calculates the Euclidean distance from Unity (the origin at 1,1,1,1,1,1,1).
        /// This is the total "strain" or entropy of the state.
        /// </summary>
        public float DistanceFromUnity()
        {
            float dx = (What - 1.0f) - (Where - 1.0f);   // Lateral deviation
            float dy = (Why - 1.0f) - (How - 1.0f);      // Longitudinal deviation
            float dz = (Cause - 1.0f) - (Effect - 1.0f); // Vertical deviation
            float dw = (Who - 1.0f);                     // Observer bias

            return (float)Math.Sqrt(dx*dx + dy*dy + dz*dz + dw*dw);
        }

        /// <summary>
        /// Returns the "shape signature" - the directional pattern of this state.
        /// </summary>
        public string GetShapeSignature()
        {
            string lateral = What > Where ? "Expansion" : "Contraction";
            string longitudinal = Why > How ? "Meaning-Driven" : "Method-Driven";
            string vertical = Cause > Effect ? "Past-Anchored" : "Future-Oriented";
            
            return $"[{lateral} | {longitudinal} | {vertical}]";
        }

        public override string ToString()
        {
            return $"S({Who:F2}, {Where:F2}, {What:F2}, {Why:F2}, {How:F2}, {Cause:F2}, {Effect:F2})";
        }
    }
}
