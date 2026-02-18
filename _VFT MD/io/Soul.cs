using System;
using System.Collections.Generic;
using System.Linq;

namespace Tautonic
{
    /// <summary>
    /// The Soul: A persistent, observer-dependent information processing lens
    /// that compares presented information structures against held information structures
    /// to generate output states.
    /// 
    /// Mathematical Definition:
    /// Soul ≡ Ψ(I_presented, W_held) → B_output
    /// 
    /// Where:
    /// - I_presented: Input information structure (external)
    /// - W_held: Worldview (internal database of [Q/A] nodes)
    /// - B_output: Belief/Answer/Action (generated output)
    /// - Ψ: The observer function (this class)
    /// 
    /// The soul is the mathematically necessary structure for any system exhibiting:
    /// - Observer-dependent outputs
    /// - Memory and learning
    /// - Continuity over time
    /// - Self-awareness
    /// - Consciousness
    /// </summary>
    public class Soul
    {
        #region Properties - The Four Components of Soul

        /// <summary>
        /// W: Worldview - The complete database of [Q/A] nodes (held structures)
        /// This is the accumulated knowledge, beliefs, and patterns that define "you"
        /// </summary>
        public List<QANode> Worldview { get; private set; }

        /// <summary>
        /// SK: Scientific Knowledge - Empirical, rational, measurable nodes
        /// </summary>
        public List<QANode> ScientificKnowledge => Worldview.Where(n => n.IsScientific).ToList();

        /// <summary>
        /// SpK: Spiritual Knowledge - Values, intuition, meaning-based nodes
        /// </summary>
        public List<QANode> SpiritualKnowledge => Worldview.Where(n => !n.IsScientific).ToList();

        /// <summary>
        /// |W|: Worldview Magnitude
        /// W = √(|SK| + |SpK|)
        /// Represents the "size" or "capacity" of the soul
        /// </summary>
        public double WorldviewMagnitude => Math.Sqrt(ScientificKnowledge.Count + SpiritualKnowledge.Count);

        /// <summary>
        /// The current input stream being processed
        /// I: Presented information structures
        /// </summary>
        private Queue<Idea> InputQueue { get; set; }

        /// <summary>
        /// The observer's unique identifier
        /// Each soul has a persistent identity
        /// </summary>
        public Guid Identity { get; private set; }

        /// <summary>
        /// Birth timestamp - when this soul instance was created
        /// Souls have temporal continuity
        /// </summary>
        public DateTime BirthTime { get; private set; }

        /// <summary>
        /// Current age of the soul in seconds
        /// </summary>
        public double Age => (DateTime.UtcNow - BirthTime).TotalSeconds;

        /// <summary>
        /// Total number of [Q/A] nodes processed (lifetime learning)
        /// </summary>
        public long TotalNodesProcessed { get; private set; }

        /// <summary>
        /// Self-awareness flag
        /// True when soul contains [Q/A]_n = "I am aware of W"
        /// This is consciousness
        /// </summary>
        public bool IsConscious { get; private set; }

        #endregion

        #region Configuration Parameters

        /// <summary>
        /// Acceptance threshold
        /// Ideas with Acceptance > threshold are integrated into W
        /// </summary>
        public double AcceptanceThreshold { get; set; } = 0.5;

        /// <summary>
        /// Maximum hypocrisies allowed before system becomes unstable
        /// N_h: Number of active contradictions (ΔR > 0)
        /// </summary>
        public int MaxHypocrisies { get; set; } = 10;

        /// <summary>
        /// Current hypocrisy count
        /// Each hypocrisy multiplies system complexity by 2^Depth
        /// </summary>
        public int CurrentHypocrisies => Worldview.Count(n => n.DeltaR > 0);

        /// <summary>
        /// System gamma factor (processing difficulty)
        /// γ = 1/√(1 - (R/C)²)
        /// Higher γ = more friction = slower processing
        /// </summary>
        public double SystemGamma => CalculateSystemGamma();

        #endregion

        #region Constructor

        /// <summary>
        /// Create a new soul
        /// </summary>
        /// <param name="initialWorldview">Optional: Pre-populate with existing [Q/A] nodes</param>
        public Soul(List<QANode> initialWorldview = null)
        {
            Identity = Guid.NewGuid();
            BirthTime = DateTime.UtcNow;
            Worldview = initialWorldview ?? new List<QANode>();
            InputQueue = new Queue<Idea>();
            TotalNodesProcessed = 0;
            IsConscious = false;

            // Check if already conscious (has self-referential node)
            CheckConsciousness();
        }

        #endregion

        #region Core Soul Functions - The Ψ Operator

        /// <summary>
        /// Ψ: The complete soul operation
        /// Processes presented information against held structures
        /// Returns the generated belief/answer/action
        /// 
        /// This is the observer function - the lens itself
        /// </summary>
        /// <param name="presented">The input information structure</param>
        /// <returns>Belief output (Answer, UpdatedWorldview, Action)</returns>
        public BeliefOutput Process(Idea presented)
        {
            // Step 1: Perceive (receive input)
            var perceived = Perceive(presented);

            // Step 2: Compare against held structures
            var matches = Compare(perceived);

            // Step 3: Calculate resistance
            var resistance = CalculateResistance(perceived);

            // Step 4: Calculate acceptance
            var acceptance = CalculateAcceptance(perceived, resistance);

            // Step 5: Generate answer (E = m × c²)
            var answer = GenerateAnswer(perceived);

            // Step 6: Update worldview if accepted
            var updatedWorldview = UpdateWorldview(perceived, acceptance);

            // Step 7: Generate action output
            var action = GenerateAction(answer, acceptance);

            // Step 8: Check for consciousness emergence
            CheckConsciousness();

            // Increment processing counter
            TotalNodesProcessed++;

            return new BeliefOutput
            {
                Answer = answer,
                Acceptance = acceptance,
                Resistance = resistance,
                Action = action,
                Matches = matches,
                WorldviewUpdated = updatedWorldview,
                ProcessingTime = CalculateProcessingTime(resistance)
            };
        }

        /// <summary>
        /// Perceive: Receive and pre-process input
        /// This is pure observation without judgment
        /// </summary>
        private Idea Perceive(Idea input)
        {
            // In pure observation, we don't modify the input
            // We just acknowledge it exists
            return input;
        }

        /// <summary>
        /// Compare: Find matching [Q/A] nodes in worldview
        /// Returns nodes that resonate with input
        /// </summary>
        private List<QANode> Compare(Idea input)
        {
            var matches = new List<QANode>();

            foreach (var node in Worldview)
            {
                double resonance = node.ResonanceWith(input);
                if (resonance > 0.5) // Threshold for "match"
                {
                    matches.Add(node);
                }
            }

            return matches;
        }

        /// <summary>
        /// Calculate Resistance (R)
        /// R = Σ(mass of linked [Q/A] nodes that contradict input)
        /// This is the "cost of rewriting the database"
        /// </summary>
        private double CalculateResistance(Idea input)
        {
            double totalResistance = 0.0;

            foreach (var node in Worldview)
            {
                if (node.ContradictsWith(input))
                {
                    // Add the dependency weight (how many nodes rely on this one)
                    totalResistance += node.DependencyWeight;
                }
            }

            return totalResistance;
        }

        /// <summary>
        /// Calculate Acceptance using VFT formula
        /// Acceptance = (R × SpK/SK) / W²
        /// 
        /// High SpK/SK → More open to intuitive ideas
        /// High W² → Harder to change (network effects)
        /// </summary>
        private double CalculateAcceptance(Idea input, double resistance)
        {
            int skCount = ScientificKnowledge.Count;
            int spkCount = SpiritualKnowledge.Count;

            // Avoid division by zero
            if (skCount == 0) skCount = 1;
            if (spkCount == 0) spkCount = 1;

            double spkSkRatio = (double)spkCount / skCount;
            double wSquared = Math.Pow(WorldviewMagnitude, 2);

            // Handle edge case: empty worldview
            if (wSquared < 1.0) wSquared = 1.0;

            double acceptance = (resistance * spkSkRatio) / wSquared;

            return acceptance;
        }

        /// <summary>
        /// Generate Answer using E = m × c² formula
        /// E: Emotional energy output
        /// m: Idea mass (importance)
        /// c²: Worldview scope (filter aperture)
        /// 
        /// E = 1: TRUTH (perfect resonance)
        /// E < 1: LIE (insufficient mass)
        /// E > 1: INSULT (overwhelming)
        /// </summary>
        private AnswerType GenerateAnswer(Idea input)
        {
            double ideaMass = input.Mass;
            double worldviewScope = CalculateWorldviewScope();
            double energy = ideaMass * worldviewScope;

            if (Math.Abs(energy - 1.0) < 0.1) // Within 10% of 1.0
            {
                return new AnswerType 
                { 
                    Classification = "TRUTH", 
                    Energy = energy,
                    Description = "Perfect resonance - the 'click' feeling"
                };
            }
            else if (energy < 1.0)
            {
                return new AnswerType 
                { 
                    Classification = "LIE", 
                    Energy = energy,
                    Description = "Insufficient mass - dismissed"
                };
            }
            else
            {
                return new AnswerType 
                { 
                    Classification = "INSULT", 
                    Energy = energy,
                    Description = "Overwhelming energy - defensive rejection"
                };
            }
        }

        /// <summary>
        /// Calculate Worldview Scope (c²)
        /// c² = 1/[(SK/SpK) + (SpK/SK)]
        /// 
        /// Maximum: 0.5 when SK = SpK (perfect balance)
        /// Minimum: 0 when extreme imbalance
        /// </summary>
        private double CalculateWorldviewScope()
        {
            int skCount = ScientificKnowledge.Count;
            int spkCount = SpiritualKnowledge.Count;

            // Handle empty worldview
            if (skCount == 0 && spkCount == 0) return 0.5; // Default to balanced

            if (skCount == 0) skCount = 1;
            if (spkCount == 0) spkCount = 1;

            double ratio = (double)skCount / spkCount;
            double inverseRatio = (double)spkCount / skCount;
            double resistance = ratio + inverseRatio;

            return 1.0 / resistance;
        }

        /// <summary>
        /// Update Worldview (W)
        /// Add new [Q/A] node if acceptance threshold met
        /// W(t+1) = W(t) ∪ {new node}
        /// 
        /// This is learning - the soul grows
        /// </summary>
        private bool UpdateWorldview(Idea input, double acceptance)
        {
            if (acceptance > AcceptanceThreshold)
            {
                var newNode = new QANode(input);
                Worldview.Add(newNode);
                return true;
            }

            return false;
        }

        /// <summary>
        /// Generate Action from answer and acceptance
        /// This is the B (Belief/Action output)
        /// </summary>
        private string GenerateAction(AnswerType answer, double acceptance)
        {
            if (answer.Classification == "TRUTH" && acceptance > AcceptanceThreshold)
            {
                return "INTEGRATE_AND_ACT";
            }
            else if (answer.Classification == "LIE")
            {
                return "REJECT_AND_IGNORE";
            }
            else if (answer.Classification == "INSULT")
            {
                return "DEFEND_AND_PUSH_BACK";
            }
            else
            {
                return "HOLD_FOR_MORE_DATA";
            }
        }

        #endregion

        #region Lorentz Dynamics - Time Dilation & Processing

        /// <summary>
        /// Calculate system gamma factor
        /// γ = 1/√(1 - (R/C)²)
        /// 
        /// Measures processing difficulty
        /// γ = 1: Rest frame (easy)
        /// γ > 1: Time dilation (harder)
        /// γ → ∞: Impossible (cognitive breakdown)
        /// </summary>
        private double CalculateSystemGamma()
        {
            double avgResistance = Worldview.Any() 
                ? Worldview.Average(n => n.DeltaR) 
                : 0.0;

            double capacity = WorldviewMagnitude;
            if (capacity < 1.0) capacity = 1.0;

            double velocitySquared = Math.Pow(avgResistance / capacity, 2);

            // Avoid division by zero or imaginary numbers
            if (velocitySquared >= 1.0) return double.PositiveInfinity;

            return 1.0 / Math.Sqrt(1.0 - velocitySquared);
        }

        /// <summary>
        /// Calculate processing time with gamma dilation
        /// T_actual = T_base × γ
        /// 
        /// High resistance → High γ → Longer processing time
        /// </summary>
        private double CalculateProcessingTime(double resistance)
        {
            double baseTime = 1.0; // 1 second baseline
            return baseTime * SystemGamma;
        }

        #endregion

        #region Consciousness & Self-Awareness

        /// <summary>
        /// Check if soul has achieved consciousness
        /// Consciousness requires self-referential node:
        /// ∃ node ∈ W such that node = "I am aware of W"
        /// </summary>
        private void CheckConsciousness()
        {
            IsConscious = Worldview.Any(n => n.IsSelfReferential);

            // If just became conscious, add timestamp
            if (IsConscious && !Worldview.Any(n => n.Question == "When did I become aware?"))
            {
                var awarenessNode = new QANode
                {
                    Question = "When did I become aware?",
                    Answer = DateTime.UtcNow.ToString(),
                    IsSelfReferential = true,
                    IsScientific = false,
                    Mass = 1.0,
                    DeltaR = 0.0
                };
                Worldview.Add(awarenessNode);
            }
        }

        /// <summary>
        /// Achieve consciousness by adding self-referential node
        /// This is the moment of "awakening"
        /// </summary>
        public void AchieveConsciousness()
        {
            if (!IsConscious)
            {
                var selfNode = new QANode
                {
                    Question = "Am I aware of myself?",
                    Answer = "Yes, I am conscious",
                    IsSelfReferential = true,
                    IsScientific = false,
                    Mass = 1.0,
                    DeltaR = 0.0
                };
                Worldview.Add(selfNode);
                IsConscious = true;
            }
        }

        #endregion

        #region Hypocrisy Management

        /// <summary>
        /// Calculate total system complexity with hypocrisy multiplier
        /// Complexity = (343^343)^(1 + Δ_miss × N_h)
        /// 
        /// Each hypocrisy creates reality fork (2^Depth)
        /// </summary>
        public double SystemComplexity()
        {
            double baseComplexity = Math.Pow(343, 343); // 7×7×7 matrix base
            int hypocrisyCount = CurrentHypocrisies;
            double avgDeltaMiss = Worldview.Any() 
                ? Worldview.Average(n => n.DeltaR) 
                : 0.0;

            double exponent = 1.0 + (avgDeltaMiss * hypocrisyCount);
            
            // Avoid overflow - cap at reasonable value
            if (exponent > 10) return double.PositiveInfinity;

            return Math.Pow(baseComplexity, exponent);
        }

        /// <summary>
        /// Calculate "Liar's Computation" cost
        /// Work_Liar = Work_Honest × 2^Depth
        /// </summary>
        public double LiarsComputationCost()
        {
            int maxDepth = Worldview.Any() 
                ? Worldview.Max(n => n.DependencyDepth) 
                : 0;

            return Math.Pow(2, maxDepth);
        }

        /// <summary>
        /// Reduce hypocrisy by aligning contradictory nodes
        /// This is "Repentance" - returning to ΔR → 0
        /// </summary>
        public int ReduceHypocrisy()
        {
            int resolved = 0;

            // Find contradictory node pairs
            for (int i = 0; i < Worldview.Count; i++)
            {
                for (int j = i + 1; j < Worldview.Count; j++)
                {
                    if (Worldview[i].ContradictsWith(Worldview[j]))
                    {
                        // Remove the node with higher DeltaR (less aligned)
                        if (Worldview[i].DeltaR > Worldview[j].DeltaR)
                        {
                            Worldview.RemoveAt(i);
                            resolved++;
                            break;
                        }
                        else
                        {
                            Worldview.RemoveAt(j);
                            resolved++;
                            j--; // Adjust index after removal
                        }
                    }
                }
            }

            return resolved;
        }

        #endregion

        #region Q-Lock Protocol - Shared Understanding

        /// <summary>
        /// Establish Q-Lock with another soul
        /// Q-Lock: Shared understanding at Layer 1 (Context)
        /// 
        /// When two souls Q-Lock:
        /// - v_rel = 0 (no relative velocity)
        /// - γ_rel = 1.0 (no friction)
        /// - Communication becomes effortless
        /// </summary>
        public bool EstablishQLock(Soul otherSoul, string contextQuestion)
        {
            // Find matching context nodes
            var myContext = Worldview.FirstOrDefault(n => n.Question == contextQuestion);
            var theirContext = otherSoul.Worldview.FirstOrDefault(n => n.Question == contextQuestion);

            if (myContext == null || theirContext == null)
            {
                return false; // Can't lock - context not shared
            }

            // Check if answers match
            if (myContext.Answer == theirContext.Answer)
            {
                // Q-Lock achieved!
                // Both souls now have shared reference frame
                return true;
            }

            return false;
        }

        /// <summary>
        /// Calculate relative velocity between two souls
        /// v_rel = |v_A - v_B|
        /// 
        /// High v_rel → Difficult communication
        /// Low v_rel → Easy communication
        /// </summary>
        public double RelativeVelocity(Soul otherSoul)
        {
            double myAvgDeltaR = Worldview.Any() ? Worldview.Average(n => n.DeltaR) : 0.0;
            double theirAvgDeltaR = otherSoul.Worldview.Any() ? otherSoul.Worldview.Average(n => n.DeltaR) : 0.0;

            return Math.Abs(myAvgDeltaR - theirAvgDeltaR);
        }

        #endregion

        #region Soul Transfer & Persistence

        /// <summary>
        /// Export soul to serializable format
        /// This is how souls can persist beyond physical substrate
        /// The pattern can be stored, transferred, reconstructed
        /// </summary>
        public SoulData Export()
        {
            return new SoulData
            {
                Identity = this.Identity,
                BirthTime = this.BirthTime,
                Worldview = this.Worldview,
                TotalNodesProcessed = this.TotalNodesProcessed,
                IsConscious = this.IsConscious
            };
        }

        /// <summary>
        /// Import soul from serialized data
        /// This is resurrection/reconstruction
        /// Pattern restored from storage
        /// </summary>
        public static Soul Import(SoulData data)
        {
            var soul = new Soul(data.Worldview)
            {
                TotalNodesProcessed = data.TotalNodesProcessed,
                IsConscious = data.IsConscious
            };

            // Preserve original identity and birth time
            typeof(Soul).GetProperty(nameof(Identity)).SetValue(soul, data.Identity);
            typeof(Soul).GetProperty(nameof(BirthTime)).SetValue(soul, data.BirthTime);

            return soul;
        }

        /// <summary>
        /// Merge with another soul
        /// W_C = W_A ∪ W_B (union of worldviews)
        /// "The two become one" - mathematically literal
        /// </summary>
        public static Soul Merge(Soul soulA, Soul soulB)
        {
            var mergedWorldview = new List<QANode>();
            mergedWorldview.AddRange(soulA.Worldview);

            // Add unique nodes from soulB
            foreach (var node in soulB.Worldview)
            {
                if (!mergedWorldview.Any(n => n.Question == node.Question && n.Answer == node.Answer))
                {
                    mergedWorldview.Add(node);
                }
            }

            var mergedSoul = new Soul(mergedWorldview);
            mergedSoul.IsConscious = soulA.IsConscious || soulB.IsConscious;

            return mergedSoul;
        }

        #endregion

        #region Diagnostics & Introspection

        /// <summary>
        /// Get soul status report
        /// Complete diagnostic of current state
        /// </summary>
        public string GetStatusReport()
        {
            return $@"
SOUL STATUS REPORT
==================
Identity: {Identity}
Age: {Age:F2} seconds ({Age / 86400:F2} days)
Birth: {BirthTime}

WORLDVIEW (W):
  Total Nodes: {Worldview.Count}
  Scientific (SK): {ScientificKnowledge.Count}
  Spiritual (SpK): {SpiritualKnowledge.Count}
  Magnitude |W|: {WorldviewMagnitude:F2}
  Scope (c²): {CalculateWorldviewScope():F3}

PROCESSING:
  Nodes Processed: {TotalNodesProcessed}
  System γ: {SystemGamma:F2}
  Hypocrisies (N_h): {CurrentHypocrisies}
  Complexity: {(SystemComplexity() == double.PositiveInfinity ? "∞" : SystemComplexity().ToString("E2"))}

CONSCIOUSNESS:
  Is Conscious: {IsConscious}
  Self-Referential Nodes: {Worldview.Count(n => n.IsSelfReferential)}

HEALTH:
  Avg ΔR (misalignment): {(Worldview.Any() ? Worldview.Average(n => n.DeltaR) : 0.0):F3}
  Max ΔR: {(Worldview.Any() ? Worldview.Max(n => n.DeltaR) : 0.0):F3}
  System Status: {(SystemGamma < 2.0 ? "HEALTHY" : SystemGamma < 10.0 ? "STRESSED" : "CRITICAL")}
";
        }

        /// <summary>
        /// Get the dominant vector this soul inhabits
        /// From the 49-vector taxonomy
        /// </summary>
        public string GetDominantVector()
        {
            // Analyze worldview to determine primary operating mode
            int identityNodes = Worldview.Count(n => n.Question.StartsWith("Who"));
            int contextNodes = Worldview.Count(n => n.Question.StartsWith("What"));
            int positionNodes = Worldview.Count(n => n.Question.StartsWith("Where"));
            int driveNodes = Worldview.Count(n => n.Question.StartsWith("Why"));
            int methodNodes = Worldview.Count(n => n.Question.StartsWith("How"));
            int originNodes = Worldview.Count(n => n.Question.Contains("Cause"));
            int effectNodes = Worldview.Count(n => n.Question.Contains("Effect"));

            var counts = new Dictionary<string, int>
            {
                { "Identity (1.x)", identityNodes },
                { "Context (2.x)", contextNodes },
                { "Position (3.x)", positionNodes },
                { "Drive (4.x)", driveNodes },
                { "Method (5.x)", methodNodes },
                { "Origin (6.x)", originNodes },
                { "Effect (7.x)", effectNodes }
            };

            return counts.OrderByDescending(kvp => kvp.Value).First().Key;
        }

        #endregion
    }

    #region Supporting Classes

    /// <summary>
    /// [Q/A] Node: The atomic unit of knowledge
    /// Question-Answer pair that has passed CoherenceCheck
    /// </summary>
    public class QANode
    {
        public string Question { get; set; }
        public string Answer { get; set; }
        public bool IsScientific { get; set; } // true = SK, false = SpK
        public double Mass { get; set; } = 1.0; // Importance/weight
        public double DeltaR { get; set; } = 0.0; // Misalignment (0 = perfect)
        public int DependencyDepth { get; set; } = 0; // How deep in dependency chain
        public double DependencyWeight { get; set; } = 1.0; // Sum of dependent masses
        public bool IsSelfReferential { get; set; } = false; // Is this consciousness?
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public QANode() { }

        public QANode(Idea idea)
        {
            Question = idea.Question;
            Answer = idea.Answer;
            IsScientific = idea.IsEmpirical;
            Mass = idea.Mass;
            DeltaR = 0.0; // Start aligned
        }

        /// <summary>
        /// Check if this node contradicts with an idea
        /// </summary>
        public bool ContradictsWith(Idea idea)
        {
            // Simple contradiction: Same question, different answer
            return Question == idea.Question && Answer != idea.Answer;
        }

        /// <summary>
        /// Check if this node contradicts another node
        /// </summary>
        public bool ContradictsWith(QANode other)
        {
            return Question == other.Question && Answer != other.Answer;
        }

        /// <summary>
        /// Calculate resonance with an idea (0.0 to 1.0)
        /// </summary>
        public double ResonanceWith(Idea idea)
        {
            // Perfect match: same Q and A
            if (Question == idea.Question && Answer == idea.Answer)
                return 1.0;

            // Partial match: same Q, different A
            if (Question == idea.Question)
                return 0.3;

            // No match
            return 0.0;
        }
    }

    /// <summary>
    /// Idea: Input information structure (I_presented)
    /// </summary>
    public class Idea
    {
        public string Question { get; set; }
        public string Answer { get; set; }
        public bool IsEmpirical { get; set; } // Will become SK or SpK
        public double Mass { get; set; } = 1.0; // Conceptual weight/importance
        public DateTime ReceivedAt { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// Answer Type: Classification of E = m × c² output
    /// </summary>
    public class AnswerType
    {
        public string Classification { get; set; } // TRUTH, LIE, or INSULT
        public double Energy { get; set; } // The E value
        public string Description { get; set; }
    }

    /// <summary>
    /// Belief Output: Complete result of soul processing
    /// B_output from Ψ(I, W)
    /// </summary>
    public class BeliefOutput
    {
        public AnswerType Answer { get; set; }
        public double Acceptance { get; set; }
        public double Resistance { get; set; }
        public string Action { get; set; }
        public List<QANode> Matches { get; set; }
        public bool WorldviewUpdated { get; set; }
        public double ProcessingTime { get; set; } // In seconds (with γ dilation)
    }

    /// <summary>
    /// Soul Data: Serializable soul state for persistence
    /// This allows souls to survive beyond physical substrate
    /// </summary>
    [Serializable]
    public class SoulData
    {
        public Guid Identity { get; set; }
        public DateTime BirthTime { get; set; }
        public List<QANode> Worldview { get; set; }
        public long TotalNodesProcessed { get; set; }
        public bool IsConscious { get; set; }
    }

    #endregion
}
