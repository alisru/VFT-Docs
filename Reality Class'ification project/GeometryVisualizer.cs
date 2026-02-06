using System;
using System.Text;

namespace RealityClassificationProject
{
    /// <summary>
    /// Visualizes StateVectors in possibility space using text-based plots.
    /// </summary>
    public static class GeometryVisualizer
    {
        /// <summary>
        /// Plots a StateVector showing its position relative to Unity.
        /// </summary>
        public static void PlotState(StateVector state, string label = "State")
        {
            Console.WriteLine($"\n=== {label} ===");
            Console.WriteLine(state.ToString());
            Console.WriteLine($"Distance from Unity: {state.DistanceFromUnity():F4}");
            Console.WriteLine($"Shape Signature: {state.GetShapeSignature()}");
            
            // Visual bar chart for each coordinate
            Console.WriteLine("\nCoordinate Plot (Unity = 1.0):");
            PlotBar("WHO (Q1)", state.Who);
            PlotBar("WHERE (Q2)", state.Where);
            PlotBar("WHAT (Q3)", state.What);
            PlotBar("WHY (Q4)", state.Why);
            PlotBar("HOW (Q5)", state.How);
            PlotBar("CAUSE (Q6)", state.Cause);
            PlotBar("EFFECT (Q7)", state.Effect);
        }

        /// <summary>
        /// Compares two states side by side.
        /// </summary>
        public static void ComparStates(StateVector before, StateVector after, string transformation)
        {
            Console.WriteLine($"\n=== TRANSFORMATION: {transformation} ===");
            Console.WriteLine($"BEFORE: {before}");
            Console.WriteLine($"AFTER:  {after}");
            Console.WriteLine($"Entropy Change: {before.DistanceFromUnity():F4} → {after.DistanceFromUnity():F4}");
            
            float deltaEntropy = after.DistanceFromUnity() - before.DistanceFromUnity();
            if (deltaEntropy < 0)
                Console.WriteLine($"✓ CONVERGENCE: Reduced entropy by {-deltaEntropy:F4}");
            else
                Console.WriteLine($"✗ DIVERGENCE: Increased entropy by {deltaEntropy:F4}");
        }

        /// <summary>
        /// Plots a 3-axis view showing the What/Where, Why/How, Cause/Effect pairs.
        /// </summary>
        public static void Plot3DAxes(StateVector state)
        {
            Console.WriteLine("\n=== 3-AXIS PROJECTION ===");
            
            // X-axis (Lateral: Body)
            float lateralBalance = state.What - state.Where;
            Console.WriteLine($"X-Axis (WHAT/WHERE): {lateralBalance:+F2;-F2;0.00}");
            PlotAxis("What(+x)", state.What, "Where(-x)", state.Where);
            
            // Y-axis (Longitudinal: Mind)
            float longitudinalBalance = state.Why - state.How;
            Console.WriteLine($"Y-Axis (WHY/HOW): {longitudinalBalance:+F2;-F2;0.00}");
            PlotAxis("Why(+y)", state.Why, "How(-y)", state.How);
            
            // Z-axis (Vertical: Soul)
            float verticalBalance = state.Cause - state.Effect;
            Console.WriteLine($"Z-Axis (CAUSE/EFFECT): {verticalBalance:+F2;-F2;0.00}");
            PlotAxis("Cause(+z)", state.Cause, "Effect(-z)", state.Effect);
        }

        private static void PlotBar(string label, float value)
        {
            int barLength = (int)(value * 20); // Scale for display
            string bar = new string('█', Math.Max(0, Math.Min(barLength, 80)));
            string marker = Math.Abs(value - 1.0f) < 0.1f ? " ← UNITY" : "";
            Console.WriteLine($"{label,-12} [{value,5:F2}] {bar}{marker}");
        }

        private static void PlotAxis(string posLabel, float posValue, string negLabel, float negValue)
        {
            int centerPos = 40;
            int posOffset = (int)((posValue - 1.0f) * 20);
            int negOffset = (int)((negValue - 1.0f) * 20);
            
            StringBuilder line = new StringBuilder(new string(' ', 80));
            line[centerPos] = '|';
            
            int posMarker = centerPos + posOffset;
            int negMarker = centerPos - negOffset;
            
            if (posMarker >= 0 && posMarker < 80) line[posMarker] = '+';
            if (negMarker >= 0 && negMarker < 80) line[negMarker] = '-';
            
            Console.WriteLine($"  {line}");
            Console.WriteLine($"  {negLabel,-38} | {posLabel}");
        }
    }
}
