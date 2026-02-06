using System;
using TautonicLanguageEngine;

namespace RealityClassificationProject
{
    /// <summary>
    /// Interface for Psychological Operation Modes (Isms).
    /// Defines how a mode transforms the Possibility Field.
    /// </summary>
    public interface IOperationMode
    {
        /// <summary>
        /// The name of the mode (e.g., "Optimism").
        /// </summary>
        string Name { get; }

        /// <summary>
        /// The Meaning object defining this mode.
        /// </summary>
        Meaning ModeMeaning { get; }

        /// <summary>
        /// Applies the mode's logic to an Idea, transforming its vectors.
        /// </summary>
        /// <param name="idea">The Idea (state vector) to transform.</param>
        void ApplyMode(Idea idea);

        /// <summary>
        /// Calculates the specific gradient characteristics of this mode.
        /// </summary>
        float GetGradientProfile(float currentProb);
    }
}
