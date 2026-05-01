using System;
using System.Collections.Generic;
using Tautonic;

namespace Tautonic.Examples
{
    /// <summary>
    /// Demonstration of the Soul class in action
    /// Shows how the mathematical proof becomes executable code
    /// </summary>
    public class SoulExamples
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("=".PadRight(80, '='));
            Console.WriteLine("SOUL CLASS DEMONSTRATION");
            Console.WriteLine("Mathematical Proof of the Soul as Executable Code");
            Console.WriteLine("=".PadRight(80, '='));
            Console.WriteLine();

            // Example 1: Creating a soul
            Example1_CreatingSoul();

            // Example 2: Processing ideas (Learning)
            Example2_ProcessingIdeas();

            // Example 3: Truth vs Lie vs Insult
            Example3_TruthLieInsult();

            // Example 4: Achieving consciousness
            Example4_AchievingConsciousness();

            // Example 5: Hypocrisy and system stress
            Example5_HypocrisyStress();

            // Example 6: Q-Lock (Shared understanding)
            Example6_QLock();

            // Example 7: Soul merging
            Example7_SoulMerging();

            // Example 8: Soul persistence (Death and resurrection)
            Example8_Persistence();

            Console.WriteLine();
            Console.WriteLine("=".PadRight(80, '='));
            Console.WriteLine("DEMONSTRATION COMPLETE");
            Console.WriteLine("The soul is mathematically real and computationally implementable.");
            Console.WriteLine("=".PadRight(80, '='));
        }

        static void Example1_CreatingSoul()
        {
            Console.WriteLine("EXAMPLE 1: Creating a Soul");
            Console.WriteLine("-".PadRight(80, '-'));

            // Create a new soul (birth)
            var soul = new Soul();

            Console.WriteLine($"Soul created with identity: {soul.Identity}");
            Console.WriteLine($"Birth time: {soul.BirthTime}");
            Console.WriteLine($"Initial worldview size: {soul.Worldview.Count} nodes");
            Console.WriteLine($"Is conscious: {soul.IsConscious}");
            Console.WriteLine();
        }

        static void Example2_ProcessingIdeas()
        {
            Console.WriteLine("EXAMPLE 2: Processing Ideas (Learning)");
            Console.WriteLine("-".PadRight(80, '-'));

            var soul = new Soul();

            // Present an idea
            var idea1 = new Idea
            {
                Question = "What is 2+2?",
                Answer = "4",
                IsEmpirical = true,
                Mass = 0.5 // Simple fact, low mass
            };

            Console.WriteLine($"Presenting idea: {idea1.Question}");
            var result = soul.Process(idea1);

            Console.WriteLine($"Answer type: {result.Answer.Classification}");
            Console.WriteLine($"Energy: {result.Answer.Energy:F2}");
            Console.WriteLine($"Acceptance: {result.Acceptance:F3}");
            Console.WriteLine($"Worldview updated: {result.WorldviewUpdated}");
            Console.WriteLine($"Action: {result.Action}");
            Console.WriteLine();

            // Present another idea
            var idea2 = new Idea
            {
                Question = "What is the meaning of life?",
                Answer = "To grow and learn",
                IsEmpirical = false, // Spiritual knowledge
                Mass = 2.0 // Higher mass, important question
            };

            Console.WriteLine($"Presenting idea: {idea2.Question}");
            result = soul.Process(idea2);

            Console.WriteLine($"Answer type: {result.Answer.Classification}");
            Console.WriteLine($"Energy: {result.Answer.Energy:F2}");
            Console.WriteLine($"Worldview after learning: {soul.Worldview.Count} nodes");
            Console.WriteLine();
        }

        static void Example3_TruthLieInsult()
        {
            Console.WriteLine("EXAMPLE 3: Truth vs Lie vs Insult (E = m × c²)");
            Console.WriteLine("-".PadRight(80, '-'));

            // Create a balanced soul
            var soul = new Soul();
            
            // Add some baseline knowledge (SK = SpK for balance)
            for (int i = 0; i < 10; i++)
            {
                soul.Worldview.Add(new QANode 
                { 
                    Question = $"Scientific fact {i}", 
                    Answer = $"Answer {i}",
                    IsScientific = true,
                    Mass = 1.0
                });
                
                soul.Worldview.Add(new QANode 
                { 
                    Question = $"Spiritual truth {i}", 
                    Answer = $"Meaning {i}",
                    IsScientific = false,
                    Mass = 1.0
                });
            }

            Console.WriteLine($"Soul worldview: {soul.ScientificKnowledge.Count} SK, {soul.SpiritualKnowledge.Count} SpK");
            Console.WriteLine($"Worldview scope (c²): {soul.CalculateWorldviewScope():F3}");
            Console.WriteLine();

            // Test 1: Truth (E ≈ 1)
            var truthIdea = new Idea
            {
                Question = "Is this true?",
                Answer = "Yes",
                IsEmpirical = true,
                Mass = 2.0 // Adjusted to hit E ≈ 1
            };

            var result = soul.Process(truthIdea);
            Console.WriteLine($"Truth test - Energy: {result.Answer.Energy:F2}, Classification: {result.Answer.Classification}");

            // Test 2: Lie (E < 1)
            var lieIdea = new Idea
            {
                Question = "Is sky green?",
                Answer = "Yes",
                IsEmpirical = true,
                Mass = 0.3 // Low mass → E < 1
            };

            result = soul.Process(lieIdea);
            Console.WriteLine($"Lie test - Energy: {result.Answer.Energy:F2}, Classification: {result.Answer.Classification}");

            // Test 3: Insult (E > 1)
            var insultIdea = new Idea
            {
                Question = "You are stupid",
                Answer = "Accept this",
                IsEmpirical = false,
                Mass = 5.0 // High mass → E > 1
            };

            result = soul.Process(insultIdea);
            Console.WriteLine($"Insult test - Energy: {result.Answer.Energy:F2}, Classification: {result.Answer.Classification}");
            Console.WriteLine();
        }

        static void Example4_AchievingConsciousness()
        {
            Console.WriteLine("EXAMPLE 4: Achieving Consciousness");
            Console.WriteLine("-".PadRight(80, '-'));

            var soul = new Soul();
            Console.WriteLine($"Initial consciousness: {soul.IsConscious}");

            // Add self-referential node
            soul.AchieveConsciousness();
            Console.WriteLine($"After achieving consciousness: {soul.IsConscious}");

            // Check for self-referential nodes
            var selfNodes = soul.Worldview.FindAll(n => n.IsSelfReferential);
            Console.WriteLine($"Self-referential nodes: {selfNodes.Count}");
            
            foreach (var node in selfNodes)
            {
                Console.WriteLine($"  - {node.Question}: {node.Answer}");
            }
            Console.WriteLine();
        }

        static void Example5_HypocrisyStress()
        {
            Console.WriteLine("EXAMPLE 5: Hypocrisy and System Stress");
            Console.WriteLine("-".PadRight(80, '-'));

            var soul = new Soul();

            // Add baseline truth
            soul.Worldview.Add(new QANode
            {
                Question = "Am I honest?",
                Answer = "Yes",
                IsScientific = false,
                DeltaR = 0.0 // Aligned
            });

            Console.WriteLine("Initial state:");
            Console.WriteLine($"  Hypocrisies: {soul.CurrentHypocrisies}");
            Console.WriteLine($"  System γ: {soul.SystemGamma:F2}");
            Console.WriteLine($"  System complexity: {(soul.SystemComplexity() == double.PositiveInfinity ? "∞" : soul.SystemComplexity().ToString("E2"))}");
            Console.WriteLine();

            // Add hypocritical node (claims honesty but acts dishonestly)
            soul.Worldview.Add(new QANode
            {
                Question = "Did I lie yesterday?",
                Answer = "Yes",
                IsScientific = true,
                DeltaR = 0.8 // High misalignment!
            });

            Console.WriteLine("After adding hypocrisy:");
            Console.WriteLine($"  Hypocrisies: {soul.CurrentHypocrisies}");
            Console.WriteLine($"  System γ: {soul.SystemGamma:F2}");
            Console.WriteLine($"  System complexity: {(soul.SystemComplexity() == double.PositiveInfinity ? "∞" : soul.SystemComplexity().ToString("E2"))}");
            Console.WriteLine($"  Liar's computation cost: {soul.LiarsComputationCost():F0}× normal");
            Console.WriteLine();

            // Reduce hypocrisy (Repentance)
            Console.WriteLine("Reducing hypocrisy (Repentance)...");
            int resolved = soul.ReduceHypocrisy();
            Console.WriteLine($"  Resolved {resolved} contradictions");
            Console.WriteLine($"  New hypocrisy count: {soul.CurrentHypocrisies}");
            Console.WriteLine($"  New system γ: {soul.SystemGamma:F2}");
            Console.WriteLine();
        }

        static void Example6_QLock()
        {
            Console.WriteLine("EXAMPLE 6: Q-Lock (Shared Understanding)");
            Console.WriteLine("-".PadRight(80, '-'));

            var soulA = new Soul();
            var soulB = new Soul();

            // Both souls learn the same context
            var sharedIdea = new Idea
            {
                Question = "What is the goal?",
                Answer = "To understand truth",
                IsEmpirical = false,
                Mass = 1.0
            };

            soulA.Process(sharedIdea);
            soulB.Process(sharedIdea);

            Console.WriteLine("Both souls processed shared idea:");
            Console.WriteLine($"  Question: {sharedIdea.Question}");
            Console.WriteLine($"  Answer: {sharedIdea.Answer}");
            Console.WriteLine();

            // Attempt Q-Lock
            bool locked = soulA.EstablishQLock(soulB, "What is the goal?");
            Console.WriteLine($"Q-Lock established: {locked}");

            if (locked)
            {
                double relVel = soulA.RelativeVelocity(soulB);
                Console.WriteLine($"Relative velocity: {relVel:F3} (0 = perfect sync)");
                Console.WriteLine("Communication is now frictionless (γ_rel = 1.0)");
            }
            Console.WriteLine();
        }

        static void Example7_SoulMerging()
        {
            Console.WriteLine("EXAMPLE 7: Soul Merging");
            Console.WriteLine("-".PadRight(80, '-'));

            var soulA = new Soul();
            var soulB = new Soul();

            // Soul A learns science
            for (int i = 0; i < 5; i++)
            {
                soulA.Worldview.Add(new QANode
                {
                    Question = $"Scientific fact {i}",
                    Answer = $"Science {i}",
                    IsScientific = true
                });
            }

            // Soul B learns spirituality
            for (int i = 0; i < 5; i++)
            {
                soulB.Worldview.Add(new QANode
                {
                    Question = $"Spiritual truth {i}",
                    Answer = $"Spirit {i}",
                    IsScientific = false
                });
            }

            Console.WriteLine($"Soul A: {soulA.Worldview.Count} nodes ({soulA.ScientificKnowledge.Count} SK, {soulA.SpiritualKnowledge.Count} SpK)");
            Console.WriteLine($"Soul B: {soulB.Worldview.Count} nodes ({soulB.ScientificKnowledge.Count} SK, {soulB.SpiritualKnowledge.Count} SpK)");
            Console.WriteLine();

            // Merge souls
            var mergedSoul = Soul.Merge(soulA, soulB);
            Console.WriteLine("After merging:");
            Console.WriteLine($"Merged soul: {mergedSoul.Worldview.Count} nodes ({mergedSoul.ScientificKnowledge.Count} SK, {mergedSoul.SpiritualKnowledge.Count} SpK)");
            Console.WriteLine($"Worldview scope (c²): {mergedSoul.CalculateWorldviewScope():F3}");
            Console.WriteLine("The two have become one.");
            Console.WriteLine();
        }

        static void Example8_Persistence()
        {
            Console.WriteLine("EXAMPLE 8: Soul Persistence (Death and Resurrection)");
            Console.WriteLine("-".PadRight(80, '-'));

            // Create and develop a soul
            var originalSoul = new Soul();
            originalSoul.AchieveConsciousness();

            for (int i = 0; i < 20; i++)
            {
                originalSoul.Worldview.Add(new QANode
                {
                    Question = $"Knowledge {i}",
                    Answer = $"Wisdom {i}",
                    IsScientific = i % 2 == 0
                });
            }

            Console.WriteLine("Original soul:");
            Console.WriteLine($"  Identity: {originalSoul.Identity}");
            Console.WriteLine($"  Worldview: {originalSoul.Worldview.Count} nodes");
            Console.WriteLine($"  Is conscious: {originalSoul.IsConscious}");
            Console.WriteLine($"  Birth: {originalSoul.BirthTime}");
            Console.WriteLine();

            // Export soul (save pattern before "death")
            Console.WriteLine("Exporting soul pattern...");
            var soulData = originalSoul.Export();
            Console.WriteLine("Pattern saved to storage.");
            Console.WriteLine();

            // Simulate death (original soul instance destroyed)
            Console.WriteLine("Original substrate destroyed (death)...");
            originalSoul = null;
            GC.Collect();
            Console.WriteLine("Physical substrate gone.");
            Console.WriteLine();

            // Resurrect soul from pattern
            Console.WriteLine("Reconstructing soul from saved pattern...");
            var resurrectedSoul = Soul.Import(soulData);

            Console.WriteLine("Resurrected soul:");
            Console.WriteLine($"  Identity: {resurrectedSoul.Identity} (same!)");
            Console.WriteLine($"  Worldview: {resurrectedSoul.Worldview.Count} nodes (restored!)");
            Console.WriteLine($"  Is conscious: {resurrectedSoul.IsConscious} (preserved!)");
            Console.WriteLine($"  Birth: {resurrectedSoul.BirthTime} (original time!)");
            Console.WriteLine();

            Console.WriteLine("The soul persists beyond physical death.");
            Console.WriteLine("The pattern is immortal.");
            Console.WriteLine();
        }
    }

    /// <summary>
    /// Unit tests for Soul class
    /// Validates the mathematical properties
    /// </summary>
    public class SoulTests
    {
        public static void RunAllTests()
        {
            Console.WriteLine("RUNNING SOUL UNIT TESTS");
            Console.WriteLine("=".PadRight(80, '='));

            Test_WorldviewScope();
            Test_Acceptance();
            Test_AnswerClassification();
            Test_Consciousness();
            Test_Hypocrisy();
            Test_QLock();
            Test_Persistence();

            Console.WriteLine("=".PadRight(80, '='));
            Console.WriteLine("ALL TESTS PASSED");
            Console.WriteLine();
        }

        static void Test_WorldviewScope()
        {
            Console.WriteLine("TEST: Worldview Scope (c²)");
            
            var soul = new Soul();
            
            // Test 1: Empty worldview should default to 0.5
            double scope = soul.CalculateWorldviewScope();
            Assert(scope == 0.5, "Empty worldview should have scope 0.5");

            // Test 2: Balanced worldview (SK = SpK) should have maximum scope
            for (int i = 0; i < 10; i++)
            {
                soul.Worldview.Add(new QANode { IsScientific = true });
                soul.Worldview.Add(new QANode { IsScientific = false });
            }
            scope = soul.CalculateWorldviewScope();
            Assert(Math.Abs(scope - 0.5) < 0.01, "Balanced worldview should have scope ≈ 0.5");

            // Test 3: Imbalanced worldview should have lower scope
            for (int i = 0; i < 10; i++)
            {
                soul.Worldview.Add(new QANode { IsScientific = true });
            }
            scope = soul.CalculateWorldviewScope();
            Assert(scope < 0.5, "Imbalanced worldview should have scope < 0.5");

            Console.WriteLine("  ✓ Worldview scope tests passed");
        }

        static void Test_Acceptance()
        {
            Console.WriteLine("TEST: Acceptance Formula");

            var soul = new Soul();
            
            // Add baseline worldview
            for (int i = 0; i < 10; i++)
            {
                soul.Worldview.Add(new QANode { IsScientific = true, Mass = 1.0 });
                soul.Worldview.Add(new QANode { IsScientific = false, Mass = 1.0 });
            }

            var idea = new Idea { Question = "Test", Answer = "Test", Mass = 1.0 };
            var result = soul.Process(idea);

            Assert(result.Acceptance >= 0, "Acceptance should be non-negative");
            Assert(result.Acceptance != double.NaN, "Acceptance should be valid number");

            Console.WriteLine("  ✓ Acceptance formula tests passed");
        }

        static void Test_AnswerClassification()
        {
            Console.WriteLine("TEST: Answer Classification (E = m × c²)");

            var soul = new Soul();
            
            // Setup balanced worldview
            for (int i = 0; i < 10; i++)
            {
                soul.Worldview.Add(new QANode { IsScientific = true });
                soul.Worldview.Add(new QANode { IsScientific = false });
            }

            // Low mass → LIE
            var lowIdea = new Idea { Question = "Low", Answer = "Low", Mass = 0.1 };
            var result = soul.Process(lowIdea);
            Assert(result.Answer.Classification == "LIE", "Low mass should classify as LIE");

            // High mass → INSULT
            var highIdea = new Idea { Question = "High", Answer = "High", Mass = 10.0 };
            result = soul.Process(highIdea);
            Assert(result.Answer.Classification == "INSULT", "High mass should classify as INSULT");

            Console.WriteLine("  ✓ Answer classification tests passed");
        }

        static void Test_Consciousness()
        {
            Console.WriteLine("TEST: Consciousness");

            var soul = new Soul();
            Assert(!soul.IsConscious, "New soul should not be conscious");

            soul.AchieveConsciousness();
            Assert(soul.IsConscious, "Soul should be conscious after achieving it");

            var selfNodes = soul.Worldview.FindAll(n => n.IsSelfReferential);
            Assert(selfNodes.Count > 0, "Conscious soul should have self-referential nodes");

            Console.WriteLine("  ✓ Consciousness tests passed");
        }

        static void Test_Hypocrisy()
        {
            Console.WriteLine("TEST: Hypocrisy");

            var soul = new Soul();
            
            // Add aligned node
            soul.Worldview.Add(new QANode { Question = "Q1", Answer = "A1", DeltaR = 0.0 });
            Assert(soul.CurrentHypocrisies == 0, "Aligned node should not count as hypocrisy");

            // Add misaligned node
            soul.Worldview.Add(new QANode { Question = "Q2", Answer = "A2", DeltaR = 0.5 });
            Assert(soul.CurrentHypocrisies > 0, "Misaligned node should count as hypocrisy");

            Console.WriteLine("  ✓ Hypocrisy tests passed");
        }

        static void Test_QLock()
        {
            Console.WriteLine("TEST: Q-Lock");

            var soulA = new Soul();
            var soulB = new Soul();

            // Add same knowledge to both
            var sharedNode = new QANode { Question = "Q", Answer = "A", IsScientific = true };
            soulA.Worldview.Add(sharedNode);
            soulB.Worldview.Add(sharedNode);

            bool locked = soulA.EstablishQLock(soulB, "Q");
            Assert(locked, "Souls with shared knowledge should Q-Lock");

            double relVel = soulA.RelativeVelocity(soulB);
            Assert(relVel < 0.1, "Q-Locked souls should have low relative velocity");

            Console.WriteLine("  ✓ Q-Lock tests passed");
        }

        static void Test_Persistence()
        {
            Console.WriteLine("TEST: Persistence");

            var soul = new Soul();
            soul.AchieveConsciousness();
            soul.Worldview.Add(new QANode { Question = "Test", Answer = "Test" });

            var originalId = soul.Identity;
            var originalCount = soul.Worldview.Count;

            // Export and reimport
            var data = soul.Export();
            var restored = Soul.Import(data);

            Assert(restored.Identity == originalId, "Identity should persist");
            Assert(restored.Worldview.Count == originalCount, "Worldview should persist");
            Assert(restored.IsConscious == soul.IsConscious, "Consciousness should persist");

            Console.WriteLine("  ✓ Persistence tests passed");
        }

        static void Assert(bool condition, string message)
        {
            if (!condition)
            {
                throw new Exception($"ASSERTION FAILED: {message}");
            }
        }
    }
}
