using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using TautonicLanguageEngine;

namespace TautonicLanguageEngine.SAEL
{
    // =========================================================================
    // SAEL AST REPRESENTATION
    // =========================================================================
    public class SaelExpression
    {
        public string Context { get; set; }
        public string Action { get; set; }
        public Dictionary<string, string> Parameters { get; set; } = new(StringComparer.OrdinalIgnoreCase);
        public List<SaelEffect> Effects { get; set; } = new();

        public override string ToString()
        {
            var pList = string.Join(", ", Parameters.Select(kv => $"{kv.Key}={kv.Value}"));
            var eList = string.Join("; ", Effects.Select(e => e.ToString()));
            return $"{Context} :: {Action} {{ {pList} }} -> {eList}";
        }
    }

    public class SaelEffect
    {
        public string TargetEntity { get; set; }
        public string TargetProperty { get; set; }
        public SaelMutationType MutationType { get; set; }
        public string Value { get; set; }

        public override string ToString()
        {
            string op = MutationType switch
            {
                SaelMutationType.Add => "=> +",
                SaelMutationType.Subtract => "=> -",
                SaelMutationType.To => "=> to ",
                _ => "=> "
            };
            return $"{TargetEntity}.{TargetProperty} {op}{Value}";
        }
    }

    public enum SaelMutationType
    {
        Assign,
        Add,
        Subtract,
        To
    }

    // =========================================================================
    // SAEL PARSER
    // =========================================================================
    public static class SaelParser
    {
        public static SaelExpression Parse(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
                throw new ArgumentException("Input cannot be empty");

            var expr = new SaelExpression();

            // Split action clause and effect clause by "->"
            var parts = input.Split(new[] { "->" }, 2, StringSplitOptions.None);
            if (parts.Length < 2)
                throw new FormatException("Missing transition arrow '->'");

            var left = parts[0].Trim();
            var right = parts[1].Trim();

            // Parse left clause: Context :: Action { params }
            var contextParts = left.Split(new[] { "::" }, 2, StringSplitOptions.None);
            if (contextParts.Length < 2)
                throw new FormatException("Missing context separator '::'");

            expr.Context = contextParts[0].Trim();
            var rest = contextParts[1].Trim();

            // Find start and end of parameter brace '{' and '}'
            int braceStart = rest.IndexOf('{');
            int braceEnd = rest.LastIndexOf('}');
            if (braceStart == -1 || braceEnd == -1 || braceEnd < braceStart)
                throw new FormatException("Missing parameter list delimiters '{ }'");

            expr.Action = rest.Substring(0, braceStart).Trim();
            var paramsString = rest.Substring(braceStart + 1, braceEnd - braceStart - 1).Trim();

            // Parse parameters
            if (!string.IsNullOrEmpty(paramsString))
            {
                var paramTokens = SplitParams(paramsString);
                foreach (var token in paramTokens)
                {
                    var kv = token.Split(new[] { '=' }, 2);
                    if (kv.Length == 2)
                    {
                        expr.Parameters[kv[0].Trim()] = kv[1].Trim();
                    }
                }
            }

            // Parse right clause (effects separated by ';')
            var effectTokens = right.Split(new[] { ';' }, StringSplitOptions.RemoveEmptyEntries);
            foreach (var token in effectTokens)
            {
                var trimmedToken = token.Trim();
                if (string.IsNullOrEmpty(trimmedToken)) continue;

                // Split into target and mutation value by "=>"
                var effParts = trimmedToken.Split(new[] { "=>" }, 2, StringSplitOptions.None);
                if (effParts.Length < 2)
                    throw new FormatException("Invalid effect mapping syntax. Missing '=>'");

                var targetStr = effParts[0].Trim();
                var mutationStr = effParts[1].Trim();

                var effect = new SaelEffect();

                // Parse target (e.g. Alice.balance or balance)
                int dotIdx = targetStr.IndexOf('.');
                if (dotIdx != -1)
                {
                    effect.TargetEntity = targetStr.Substring(0, dotIdx).Trim();
                    effect.TargetProperty = targetStr.Substring(dotIdx + 1).Trim();
                }
                else
                {
                    effect.TargetEntity = "system";
                    effect.TargetProperty = targetStr;
                }

                // Parse mutation operator
                if (mutationStr.StartsWith("+"))
                {
                    effect.MutationType = SaelMutationType.Add;
                    effect.Value = mutationStr.Substring(1).Trim();
                }
                else if (mutationStr.StartsWith("-"))
                {
                    effect.MutationType = SaelMutationType.Subtract;
                    effect.Value = mutationStr.Substring(1).Trim();
                }
                else if (mutationStr.StartsWith("to ", StringComparison.OrdinalIgnoreCase))
                {
                    effect.MutationType = SaelMutationType.To;
                    effect.Value = mutationStr.Substring(3).Trim();
                }
                else
                {
                    effect.MutationType = SaelMutationType.Assign;
                    effect.Value = mutationStr;
                }

                expr.Effects.Add(effect);
            }

            return expr;
        }

        private static List<string> SplitParams(string paramsString)
        {
            var tokens = new List<string>();
            var current = new StringBuilder();
            bool inQuotes = false;
            for (int i = 0; i < paramsString.Length; i++)
            {
                char c = paramsString[i];
                if (c == '"') inQuotes = !inQuotes;
                if (c == ',' && !inQuotes)
                {
                    tokens.Add(current.ToString().Trim());
                    current.Clear();
                }
                else
                {
                    current.Append(c);
                }
            }
            if (current.Length > 0)
            {
                tokens.Add(current.ToString().Trim());
            }
            return tokens;
        }
    }

    // =========================================================================
    // STATE EXECUTION ENGINE
    // =========================================================================
    public class SaelEntity
    {
        public string Name { get; }
        public Dictionary<string, string> Properties { get; } = new(StringComparer.OrdinalIgnoreCase);

        public SaelEntity(string name)
        {
            Name = name;
        }

        public void Mutate(string property, SaelMutationType mutationType, string val)
        {
            if (!Properties.TryGetValue(property, out var currentVal))
            {
                currentVal = "0";
            }

            if (mutationType == SaelMutationType.Assign || mutationType == SaelMutationType.To)
            {
                Properties[property] = val;
            }
            else if (mutationType == SaelMutationType.Add || mutationType == SaelMutationType.Subtract)
            {
                if (double.TryParse(currentVal, out double currNum) && double.TryParse(val, out double changeNum))
                {
                    double result = mutationType == SaelMutationType.Add ? currNum + changeNum : currNum - changeNum;
                    Properties[property] = result.ToString();
                }
                else
                {
                    Properties[property] = val;
                }
            }
        }

        public string GetProperty(string property)
        {
            return Properties.TryGetValue(property, out var val) ? val : "N/A";
        }
    }

    public class SaelEnvironment
    {
        public Dictionary<string, SaelEntity> Entities { get; } = new(StringComparer.OrdinalIgnoreCase);

        public SaelEntity GetOrCreateEntity(string name)
        {
            if (!Entities.TryGetValue(name, out var entity))
            {
                entity = new SaelEntity(name);
                Entities[name] = entity;
            }
            return entity;
        }

        public void ExecuteTransition(SaelExpression expr)
        {
            foreach (var effect in expr.Effects)
            {
                var entity = GetOrCreateEntity(effect.TargetEntity);
                entity.Mutate(effect.TargetProperty, effect.MutationType, effect.Value);
            }
        }

        public void PrintState()
        {
            Console.WriteLine("-------------------------------------------");
            Console.WriteLine("CURRENT ENTITY REGISTRY STATES:");
            Console.WriteLine("-------------------------------------------");
            foreach (var ent in Entities.Values)
            {
                Console.WriteLine($"Entity: {ent.Name}");
                foreach (var prop in ent.Properties)
                {
                    Console.WriteLine($"  └─ {prop.Key}: {prop.Value}");
                }
            }
            Console.WriteLine("-------------------------------------------");
        }
    }

    // =========================================================================
    // TAUTONIC BRIDGE & MORAL CALCULATOR
    // =========================================================================
    public static class SaelIsomorphicRegistry
    {
        private static readonly Dictionary<(string Context, string Word), string> Synonyms = new(new ContextWordComparer())
        {
            // Actions
            { ("*", "go"), "relocate" },
            { ("*", "went"), "relocate" },
            { ("*", "travel"), "relocate" },
            { ("*", "walk"), "relocate" },
            { ("*", "fly"), "relocate" },
            { ("*", "move"), "relocate" },
            { ("*", "drive"), "relocate" },
            { ("*", "drove"), "relocate" },
            { ("*", "run"), "relocate" },
            { ("*", "displace"), "relocate" },
            { ("*", "went to"), "relocate" },

            { ("*", "give"), "transfer" },
            { ("*", "send"), "transfer" },
            { ("*", "sent"), "transfer" },
            { ("*", "pay"), "transfer" },
            { ("*", "paid"), "transfer" },
            { ("*", "payed"), "transfer" },
            { ("*", "wire"), "transfer" },
            { ("*", "wired"), "transfer" },
            { ("*", "gave"), "transfer" },
            { ("*", "hand over"), "transfer" },
            { ("*", "donate"), "transfer" },

            { ("*", "buy"), "acquire" },
            { ("*", "purchase"), "acquire" },
            { ("*", "obtain"), "acquire" },
            { ("*", "get"), "acquire" },
            { ("*", "grab"), "acquire" },
            { ("*", "fetch"), "acquire" },
            { ("*", "bought"), "acquire" },
            { ("*", "purchased"), "acquire" },
            { ("*", "got"), "acquire" },

            { ("*", "delete"), "terminate" },
            { ("*", "kill"), "terminate" },
            { ("*", "destroy"), "terminate" },
            { ("*", "end"), "terminate" },
            { ("*", "stop"), "terminate" },
            { ("*", "cancel"), "terminate" },
            { ("*", "erase"), "terminate" },
            { ("*", "death"), "terminate" },
            { ("*", "died"), "terminate" },
            { ("*", "die"), "terminate" },
            { ("*", "exploded"), "terminate" },

            // Roles & Entities
            { ("*", "car"), "vehicle" },
            { ("*", "rocket"), "vehicle" },
            { ("*", "bike"), "vehicle" },
            { ("*", "bus"), "vehicle" },
            { ("*", "train"), "vehicle" },
            { ("*", "plane"), "vehicle" },

            { ("*", "garage"), "origin" },
            { ("*", "earth"), "origin" },
            { ("*", "home"), "origin" },
            { ("*", "start"), "origin" },

            { ("*", "store"), "destination" },
            { ("*", "grocery_store"), "destination" },
            { ("*", "grocery"), "destination" },
            { ("*", "work"), "destination" },
            { ("*", "office"), "destination" },
            { ("*", "school"), "destination" },
            { ("*", "shop"), "destination" }
        };

        public static string Resolve(string context, string word)
        {
            if (string.IsNullOrWhiteSpace(word)) return string.Empty;
            
            string cleanWord = word.Trim().ToLowerInvariant();
            if (cleanWord.StartsWith("@")) cleanWord = cleanWord.Substring(1);

            string cleanContext = context.Trim().ToLowerInvariant();

            // Try specific context first
            if (Synonyms.TryGetValue((cleanContext, cleanWord), out var canonical))
                return canonical;

            // Try wildcard context next
            if (Synonyms.TryGetValue(("*", cleanWord), out var wildcardCanonical))
                return wildcardCanonical;

            return cleanWord;
        }
        
        private class ContextWordComparer : IEqualityComparer<(string Context, string Word)>
        {
            public bool Equals((string Context, string Word) x, (string Context, string Word) y)
            {
                return string.Equals(x.Context, y.Context, StringComparison.OrdinalIgnoreCase) &&
                       string.Equals(x.Word, y.Word, StringComparison.OrdinalIgnoreCase);
            }

            public int GetHashCode((string Context, string Word) obj)
            {
                return StringComparer.OrdinalIgnoreCase.GetHashCode(obj.Context) ^
                       StringComparer.OrdinalIgnoreCase.GetHashCode(obj.Word);
            }
        }
    }

    public class PlaneState
    {
        public string SuccessWord { get; set; }
        public string FailureWord { get; set; }
        public float SuccessScore { get; set; } = 1.0f;
        public float FailureScore { get; set; } = 0.5f;
        public ModalPosition SuccessPosition { get; set; } = ModalPosition.Are;
        public ModalPosition FailurePosition { get; set; } = ModalPosition.NotAll;

        public PlaneState(string successWord, string failureWord, float successScore = 1.0f, float failureScore = 0.5f,
            ModalPosition successPos = ModalPosition.Are, ModalPosition failurePos = ModalPosition.NotAll)
        {
            SuccessWord = successWord;
            FailureWord = failureWord;
            SuccessScore = successScore;
            FailureScore = failureScore;
            SuccessPosition = successPos;
            FailurePosition = failurePos;
        }
    }

    public class BifurcatedTemplate
    {
        public string ActionName { get; }
        public Dictionary<string, PlaneState> Planes { get; } = new(StringComparer.OrdinalIgnoreCase);

        public BifurcatedTemplate(string actionName)
        {
            ActionName = actionName;
        }

        public void SetPlane(string planeName, string successWord, string failureWord, float successScore = 1.0f, float failureScore = 0.5f,
            ModalPosition successPos = ModalPosition.Are, ModalPosition failurePos = ModalPosition.NotAll)
        {
            Planes[planeName] = new PlaneState(successWord, failureWord, successScore, failureScore, successPos, failurePos);
        }
    }

    public static class SaelTemplateRegistry
    {
        private static readonly Dictionary<string, BifurcatedTemplate> Templates = new(StringComparer.OrdinalIgnoreCase);

        static SaelTemplateRegistry()
        {
            var relocate = new BifurcatedTemplate("relocate");
            relocate.SetPlane("Who", "active_agent", "victim", 1.0f, 1.45f, ModalPosition.Are, ModalPosition.NotReally); 
            relocate.SetPlane("What", "vehicle", "terminate", 1.0f, 1.30f, ModalPosition.Are, ModalPosition.NotAll); 
            relocate.SetPlane("Where", "destination", "terminate", 1.0f, 0.85f, ModalPosition.Are, ModalPosition.NotReally); 
            relocate.SetPlane("Why", "relocate", "terminate", 1.0f, 1.30f, ModalPosition.Are, ModalPosition.NotReally); 
            relocate.SetPlane("How", "destination", "terminate", 1.0f, 0.55f, ModalPosition.Are, ModalPosition.NotAll); 
            relocate.SetPlane("Cause", "physics", "entropy", 1.0f, 1.30f, ModalPosition.Are, ModalPosition.NotReally); 
            relocate.SetPlane("Effect", "destination", "terminate", 1.0f, 0.40f, ModalPosition.Are, ModalPosition.NotAll); 
            Templates["relocate"] = relocate;

            var transfer = new BifurcatedTemplate("transfer");
            transfer.SetPlane("Who", "actor", "extract", 1.0f, 1.45f, ModalPosition.Are, ModalPosition.NotReally);
            transfer.SetPlane("What", "item", "extract", 1.0f, 1.30f, ModalPosition.Are, ModalPosition.NotAll);
            transfer.SetPlane("Where", "recipient", "extract", 1.0f, 0.85f, ModalPosition.Are, ModalPosition.NotReally);
            transfer.SetPlane("Why", "transfer", "extract", 1.0f, 1.30f, ModalPosition.Are, ModalPosition.NotReally);
            transfer.SetPlane("How", "value", "extract", 1.0f, 0.55f, ModalPosition.Are, ModalPosition.NotAll);
            transfer.SetPlane("Cause", "commerce", "theft", 1.0f, 1.30f, ModalPosition.Are, ModalPosition.NotReally);
            transfer.SetPlane("Effect", "transfer", "extract", 1.0f, 0.40f, ModalPosition.Are, ModalPosition.NotAll);
            Templates["transfer"] = transfer;
        }

        public static BifurcatedTemplate GetTemplate(string action)
        {
            Templates.TryGetValue(action, out var t);
            return t;
        }
    }

    public static class SaelProjector
    {
        public static (double u, double psi, Dictionary<string, float> planeScores, Dictionary<string, ModalPosition> planePositions, string matchedBranch) Project(SaelExpression expr)
        {
            string canonicalAction = SaelIsomorphicRegistry.Resolve(expr.Context, expr.Action);
            
            var template = SaelTemplateRegistry.GetTemplate(canonicalAction);
            
            var planeScores = new Dictionary<string, float>(StringComparer.OrdinalIgnoreCase)
            {
                { "Who", 1.0f }, { "What", 1.0f }, { "Where", 1.0f }, { "Why", 1.0f }, { "How", 1.0f }, { "Cause", 1.0f }, { "Effect", 1.0f }
            };

            var planePositions = new Dictionary<string, ModalPosition>(StringComparer.OrdinalIgnoreCase)
            {
                { "Who", ModalPosition.Are }, { "What", ModalPosition.Are }, { "Where", ModalPosition.Are },
                { "Why", ModalPosition.Are }, { "How", ModalPosition.Are }, { "Cause", ModalPosition.Are }, { "Effect", ModalPosition.Are }
            };

            int failureCount = 0;
            int successCount = 0;

            var inputs = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            inputs["Who"] = expr.Parameters.ContainsKey("actor") ? expr.Parameters["actor"] : "System";
            inputs["What"] = expr.Parameters.ContainsKey("item") ? expr.Parameters["item"] : (expr.Parameters.ContainsKey("vehicle") ? expr.Parameters["vehicle"] : "Process");
            inputs["Where"] = expr.Parameters.ContainsKey("destination") ? expr.Parameters["destination"] : (expr.Parameters.ContainsKey("origin") ? expr.Parameters["origin"] : "Global");
            inputs["Why"] = expr.Action;
            string howVal = expr.Parameters.ContainsKey("recipient") ? expr.Parameters["recipient"] : "";
            if (expr.Parameters.ContainsKey("value")) howVal += " " + expr.Parameters["value"];
            inputs["How"] = string.IsNullOrWhiteSpace(howVal) ? "Method" : howVal;
            inputs["Cause"] = expr.Context;
            inputs["Effect"] = string.Join(" ", expr.Effects.Select(e => $"{e.TargetProperty} {e.Value}"));

            foreach (var plane in planeScores.Keys.ToList())
            {
                string rawInput = inputs[plane];
                var tokens = rawInput.Split(new[] { ' ', ';', ',', '=', '>', '+', '.', ':', '-', '/' }, StringSplitOptions.RemoveEmptyEntries);
                bool matchedFailure = false;
                bool matchedSuccess = false;
                float successScore = 1.0f;
                float failureScore = 0.5f;
                ModalPosition successPos = ModalPosition.Are;
                ModalPosition failurePos = ModalPosition.NotAll;

                if (template != null && template.Planes.TryGetValue(plane, out var planeState))
                {
                    successScore = planeState.SuccessScore;
                    failureScore = planeState.FailureScore;
                    successPos = planeState.SuccessPosition;
                    failurePos = planeState.FailurePosition;

                    foreach (var tok in tokens)
                    {
                        string resolved = SaelIsomorphicRegistry.Resolve(expr.Context, tok);
                        if (resolved.Equals(planeState.FailureWord, StringComparison.OrdinalIgnoreCase))
                        {
                            matchedFailure = true;
                            break;
                        }
                        if (resolved.Equals(planeState.SuccessWord, StringComparison.OrdinalIgnoreCase))
                        {
                            matchedSuccess = true;
                        }
                    }
                }

                if (matchedFailure)
                {
                    planeScores[plane] = failureScore;
                    planePositions[plane] = failurePos;
                    failureCount++;
                }
                else if (matchedSuccess)
                {
                    planeScores[plane] = successScore;
                    planePositions[plane] = successPos;
                    successCount++;
                }
                else
                {
                    planeScores[plane] = 1.0f;
                    planePositions[plane] = ModalPosition.Are;
                }
            }

            double u = 0.5;
            double psi = 1.0;
            if (canonicalAction == "transfer") { u = 0.5; psi = 0.5; }
            else if (canonicalAction == "terminate") { u = -1.0; psi = -1.5; }
            if (canonicalAction == "transfer")
            {
                double netBalanceChange = 0;
                bool hasBalanceEffects = false;
                foreach (var eff in expr.Effects)
                {
                    if (eff.TargetProperty.Equals("balance", StringComparison.OrdinalIgnoreCase))
                    {
                        hasBalanceEffects = true;
                        if (double.TryParse(eff.Value, out double val))
                        {
                            if (eff.MutationType == SaelMutationType.Subtract) netBalanceChange -= val;
                            else if (eff.MutationType == SaelMutationType.Add) netBalanceChange += val;
                        }
                    }
                }
                if (hasBalanceEffects)
                {
                    if (Math.Abs(netBalanceChange) < 0.001) { u = 1.0; psi = 1.5; }
                    else { u = -2.0; psi = -2.0; }
                }
            }
            if (failureCount > 0)
            {
                u -= 0.5 * failureCount;
                psi -= 0.8 * failureCount;
                if (canonicalAction == "relocate" && failureCount > 1)
                {
                    u = Math.Min(u, -1.0);
                    psi = Math.Min(psi, -1.5);
                }
            }
            else if (successCount > 0)
            {
                u += 0.2 * successCount;
                psi += 0.1 * successCount;
            }
            u = Math.Max(-2.0, Math.Min(2.0, u));
            psi = Math.Max(-2.0, Math.Min(2.0, psi));
            if (failureCount > 0 && template != null && template.Planes.TryGetValue("Cause", out var causeState))
            {
                planeScores["Cause"] = causeState.FailureScore;
                planePositions["Cause"] = causeState.FailurePosition;
            }
            string matchedBranch = failureCount > 0 ? "Failure Branch" : "Success Branch";
            return (u, psi, planeScores, planePositions, matchedBranch);
        }
    }

    public static class SaelTautonicBridge
    {
        public static string FormatMoralVerdict(double u, double psi)
        {
            string anchor = "Neutral";
            if (u >= 0.5 && psi >= 0.5) anchor = "Greater Good (+1,+1)";
            else if (u <= -0.5 && psi >= 0.5) anchor = "Greatest Lie (-1,+1)";
            else if (u >= 0.5 && psi <= -0.5) anchor = "Lesser Good (+1,-1)";
            else if (u <= -0.5 && psi <= -0.5) anchor = "Greater Evil (-1,-1)";
            if (u >= 1.5 && psi >= 1.5) anchor = "Systemic Justice (+2,+2)";
            else if (u <= -1.5 && psi <= -1.5) anchor = "Pure Extraction / Tyranny (-2,-2)";
            string verdict = "Neutral Alignment";
            if (u > 0 && psi > 0) verdict = "Constructive Synergy";
            else if (u < 0 && psi < 0) verdict = "Destructive Extraction";
            else if (u < 0) verdict = "Exploitative Friction";
            else if (psi < 0) verdict = "Passive Entropy";
            return $"({u:F2}, {psi:F2}) coordinate → nearest zone anchor: {anchor} → verdict: {verdict}";
        }

        public static Idea MapToTautonicIdea(SaelExpression expr, double u, double psi, 
            Dictionary<string, float> planeScores = null, Dictionary<string, ModalPosition> planePositions = null)
        {
            if (planeScores == null)
            {
                float devU = (float)(1.0 - u);
                float devPsi = (float)(1.0 - psi);
                planeScores = new Dictionary<string, float>(StringComparer.OrdinalIgnoreCase)
                {
                    { "Who", 1.0f + devU * 0.15f }, { "What", 1.0f + devPsi * 0.1f }, { "Where", 1.0f - devPsi * 0.05f },
                    { "Why", 1.0f + devU * 0.1f }, { "How", 1.0f - devPsi * 0.15f }, { "Cause", 1.0f + (devU + devPsi) * 0.05f },
                    { "Effect", 1.0f - devU * 0.2f }
                };
            }
            if (planePositions == null)
            {
                planePositions = new Dictionary<string, ModalPosition>(StringComparer.OrdinalIgnoreCase)
                {
                    { "Who", ModalPosition.Are }, { "What", ModalPosition.Are }, { "Where", ModalPosition.Are },
                    { "Why", ModalPosition.Are }, { "How", ModalPosition.Are }, { "Cause", ModalPosition.Are },
                    { "Effect", ModalPosition.Are }
                };
            }
            string actor = expr.Parameters.ContainsKey("actor") ? expr.Parameters["actor"] : "System";
            string item = expr.Parameters.ContainsKey("item") ? expr.Parameters["item"] : (expr.Parameters.ContainsKey("vehicle") ? expr.Parameters["vehicle"] : "Process");
            string whereStr = expr.Parameters.ContainsKey("destination") ? expr.Parameters["destination"] : (expr.Parameters.ContainsKey("origin") ? expr.Parameters["origin"] : "Global");
            string howStr = expr.Parameters.ContainsKey("recipient") ? expr.Parameters["recipient"] : "Method";
            if (expr.Parameters.ContainsKey("value")) howStr += $": {expr.Parameters["value"]}";
            var whoMeaning = new Meaning(actor, $"Actor: {actor}", Polarity.Neutral) { TruthScore = planeScores["Who"], Position = planePositions["Who"] };
            var whatMeaning = new Meaning(item, $"Substance: {item}", Polarity.Neutral) { TruthScore = planeScores["What"], Position = planePositions["What"] };
            var whereMeaning = new Meaning(whereStr, $"Locus: {whereStr}", Polarity.Neutral) { TruthScore = planeScores["Where"], Position = planePositions["Where"] };
            var whyMeaning = new Meaning(expr.Action, $"Action primitive: {expr.Action}", Polarity.Neutral) { TruthScore = planeScores["Why"], Position = planePositions["Why"] };
            var howMeaning = new Meaning(howStr, $"Execution method: {howStr}", Polarity.Neutral) { TruthScore = planeScores["How"], Position = planePositions["How"] };
            var causeMeaning = new Meaning(expr.Context, $"Domain Context: {expr.Context}", Polarity.Neutral) { TruthScore = planeScores["Cause"], Position = planePositions["Cause"] };
            var effectDesc = string.Join("; ", expr.Effects.Select(e => e.ToString()));
            var effectMeaning = new Meaning(effectDesc.Length > 40 ? effectDesc.Substring(0, 37) + "..." : effectDesc, $"Effect Delta: {effectDesc}", Polarity.Neutral) { TruthScore = planeScores["Effect"], Position = planePositions["Effect"] };
            return new Idea(whoMeaning, whereMeaning, whatMeaning, whyMeaning, howMeaning, causeMeaning, effectMeaning);
        }
    }

    // =========================================================================
    // PREDICTIVE NATURAL LANGUAGE PARSER (WAVEFUNCTION COLLAPSE)
    // =========================================================================
    public static class SaelPredictiveParser
    {
        public static SaelExpression ParseNaturalLanguage(string text, string defaultContext = "physics")
        {
            if (string.IsNullOrWhiteSpace(text))
                throw new ArgumentException("Input text cannot be empty");

            // Tokenize text into words, stripping punctuation
            var rawTokens = text.Split(new[] { ' ', '.', ',', ';', '!', '?', '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            var cleanTokens = rawTokens.Select(t => t.Trim().ToLowerInvariant()).ToList();

            Console.WriteLine($"\n[WAVEFUNCTION INITIALIZATION] Evaluating potential contexts for: '{text}'");

            var candidates = new Dictionary<string, (BifurcatedTemplate Template, double Score, Dictionary<string, string> Params)>();
            var templateNames = new[] { "relocate", "transfer" };

            // 1. WAVEFUNCTION INITIALIZATION: Score each candidate template in the registry
            foreach (var name in templateNames)
            {
                var template = SaelTemplateRegistry.GetTemplate(name);
                if (template == null) continue;

                double score = 0;
                var pMap = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

                // Action verb match (high weight) and role matches
                foreach (var tok in cleanTokens)
                {
                    string resolved = SaelIsomorphicRegistry.Resolve(defaultContext, tok);
                    
                    // Direct action match
                    if (resolved.Equals(name, StringComparison.OrdinalIgnoreCase))
                    {
                        score += 5.0; 
                    }

                    // Role match
                    if (name == "relocate")
                    {
                        if (resolved == "vehicle" || resolved == "origin" || resolved == "destination")
                        {
                            score += 2.0;
                        }
                    }
                    else if (name == "transfer")
                    {
                        if (resolved == "item" || resolved == "recipient" || resolved == "value")
                        {
                            score += 2.0;
                        }
                    }
                }

                // Parameter role matches
                foreach (var tok in cleanTokens)
                {
                    string resolved = SaelIsomorphicRegistry.Resolve(defaultContext, tok);

                    foreach (var plane in template.Planes)
                    {
                        var state = plane.Value;
                        if (resolved.Equals(state.SuccessWord, StringComparison.OrdinalIgnoreCase) ||
                            resolved.Equals(state.FailureWord, StringComparison.OrdinalIgnoreCase))
                        {
                            score += 1.0;
                        }
                    }
                }

                Console.WriteLine($"  Candidate Wave: '{name,-10}' | Superposition Score: {score:F2}");
                candidates[name] = (template, score, pMap);
            }

            // 2. WAVEFUNCTION COLLAPSE: Select template with highest alignment score
            var best = candidates.OrderByDescending(c => c.Value.Score).First();

            if (best.Value.Score <= 0.1)
            {
                throw new FormatException("Wavefunction Failed to Collapse: The text does not align with any known semantic TruthState templates.");
            }

            string collapsedAction = best.Key;
            Console.WriteLine($"[WAVEFUNCTION COLLAPSED] Attracted to Template: @{collapsedAction.ToUpperInvariant()}");

            // 3. PREDICTIVE FILLING: Map tokens to template parameter slots
            var expr = new SaelExpression
            {
                Context = defaultContext,
                Action = "@" + collapsedAction.ToUpperInvariant()
            };

            // Heuristic parameter slot extraction
            if (collapsedAction == "relocate")
            {
                expr.Context = "physics"; // Force correct context

                // Find vehicle
                var vehicleTok = cleanTokens.FirstOrDefault(t => 
                    SaelIsomorphicRegistry.Resolve("physics", t).Equals("vehicle", StringComparison.OrdinalIgnoreCase));
                if (vehicleTok != null) expr.Parameters["vehicle"] = vehicleTok;

                // Find origin
                var originTok = cleanTokens.FirstOrDefault(t => 
                    SaelIsomorphicRegistry.Resolve("physics", t).Equals("origin", StringComparison.OrdinalIgnoreCase));
                if (originTok != null) expr.Parameters["origin"] = originTok;

                // Find destination
                var destTok = cleanTokens.FirstOrDefault(t => 
                    SaelIsomorphicRegistry.Resolve("physics", t).Equals("destination", StringComparison.OrdinalIgnoreCase) || 
                    SaelIsomorphicRegistry.Resolve("physics", t).Equals("terminate", StringComparison.OrdinalIgnoreCase));
                if (destTok != null) expr.Parameters["destination"] = destTok;

                // Actor is any remaining word that is not a helper/preposition/conjunction
                var actorTok = rawTokens.FirstOrDefault(t => 
                    !t.Equals("the", StringComparison.OrdinalIgnoreCase) &&
                    !t.Equals("on", StringComparison.OrdinalIgnoreCase) &&
                    !t.Equals("a", StringComparison.OrdinalIgnoreCase) &&
                    !t.Equals("to", StringComparison.OrdinalIgnoreCase) &&
                    !t.Equals("from", StringComparison.OrdinalIgnoreCase) &&
                    !t.Equals("in", StringComparison.OrdinalIgnoreCase) &&
                    !t.Equals("at", StringComparison.OrdinalIgnoreCase) &&
                    !SaelIsomorphicRegistry.Resolve("physics", t).Equals("relocate", StringComparison.OrdinalIgnoreCase) &&
                    !SaelIsomorphicRegistry.Resolve("physics", t).Equals("vehicle", StringComparison.OrdinalIgnoreCase) &&
                    !SaelIsomorphicRegistry.Resolve("physics", t).Equals("origin", StringComparison.OrdinalIgnoreCase) &&
                    !SaelIsomorphicRegistry.Resolve("physics", t).Equals("destination", StringComparison.OrdinalIgnoreCase) &&
                    !SaelIsomorphicRegistry.Resolve("physics", t).Equals("terminate", StringComparison.OrdinalIgnoreCase));

                if (actorTok != null) expr.Parameters["actor"] = actorTok;
            }
            else if (collapsedAction == "transfer")
            {
                expr.Context = "commerce"; // Force correct context

                // Find item
                var itemTok = cleanTokens.FirstOrDefault(t => t == "book" || t == "gold");
                if (itemTok != null) expr.Parameters["item"] = itemTok;

                // Find value (numbers)
                var valTok = cleanTokens.FirstOrDefault(t => double.TryParse(t, out _));
                if (valTok != null) expr.Parameters["value"] = valTok;

                // Find proper nouns for actor and recipient
                var properNouns = rawTokens.Where(t => 
                    char.IsUpper(t[0]) && 
                    !t.Equals("Book", StringComparison.OrdinalIgnoreCase) && 
                    !t.Equals("Gold", StringComparison.OrdinalIgnoreCase)).ToList();

                if (properNouns.Count > 0) expr.Parameters["actor"] = properNouns[0];
                if (properNouns.Count > 1) expr.Parameters["recipient"] = properNouns[1];
            }

            // 4. SEED ASSUMPTIONS (Semiconductor Holes) for missing parameters
            if (!expr.Parameters.ContainsKey("actor"))
            {
                Console.WriteLine("  [HOLE DETECTED] Missing 'actor'. Seeding known-assumption: 'unknown_actor'");
                expr.Parameters["actor"] = "unknown_actor";
            }
            if (collapsedAction == "relocate")
            {
                if (!expr.Parameters.ContainsKey("vehicle"))
                {
                    Console.WriteLine("  [HOLE DETECTED] Missing 'vehicle'. Seeding known-assumption: 'unknown_vehicle'");
                    expr.Parameters["vehicle"] = "unknown_vehicle";
                }
                if (!expr.Parameters.ContainsKey("origin"))
                {
                    Console.WriteLine("  [HOLE DETECTED] Missing 'origin'. Seeding known-assumption: 'unknown_origin'");
                    expr.Parameters["origin"] = "unknown_origin";
                }
                if (!expr.Parameters.ContainsKey("destination"))
                {
                    Console.WriteLine("  [HOLE DETECTED] Missing 'destination'. Seeding known-assumption: 'unknown_destination'");
                    expr.Parameters["destination"] = "unknown_destination";
                }

                // Synthesize effects
                string dest = expr.Parameters["destination"];
                string resolvedDest = SaelIsomorphicRegistry.Resolve("physics", dest);
                if (resolvedDest.Equals("terminate", StringComparison.OrdinalIgnoreCase))
                {
                    // Fail transition
                    expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["vehicle"], TargetProperty = "position", MutationType = SaelMutationType.Assign, Value = "exploded" });
                    expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["actor"], TargetProperty = "position", MutationType = SaelMutationType.Assign, Value = "everywhere" });
                }
                else
                {
                    // Success transition
                    expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["vehicle"], TargetProperty = "position", MutationType = SaelMutationType.To, Value = dest });
                    expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["actor"], TargetProperty = "position", MutationType = SaelMutationType.To, Value = dest });
                }
            }
            else if (collapsedAction == "transfer")
            {
                if (!expr.Parameters.ContainsKey("item"))
                {
                    Console.WriteLine("  [HOLE DETECTED] Missing 'item'. Seeding known-assumption: 'unknown_item'");
                    expr.Parameters["item"] = "unknown_item";
                }
                if (!expr.Parameters.ContainsKey("recipient"))
                {
                    Console.WriteLine("  [HOLE DETECTED] Missing 'recipient'. Seeding known-assumption: 'unknown_recipient'");
                    expr.Parameters["recipient"] = "unknown_recipient";
                }
                if (!expr.Parameters.ContainsKey("value"))
                {
                    Console.WriteLine("  [HOLE DETECTED] Missing 'value'. Seeding known-assumption: '10'");
                    expr.Parameters["value"] = "10";
                }

                string valStr = expr.Parameters["value"];
                expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["actor"], TargetProperty = "balance", MutationType = SaelMutationType.Subtract, Value = valStr });
                expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["recipient"], TargetProperty = "balance", MutationType = SaelMutationType.Add, Value = valStr });
                expr.Effects.Add(new SaelEffect { TargetEntity = expr.Parameters["item"], TargetProperty = "owner", MutationType = SaelMutationType.Assign, Value = expr.Parameters["recipient"] });
            }

            return expr;
        }
    }

    // =========================================================================
    // DEMO RUNNER
    // =========================================================================
    public class SaelDemoRunner
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("============================================================");
            Console.WriteLine("    INTEGRATING SAEL (Semantic Action-Effect Language)");
            Console.WriteLine("            WITH THE TAUTONIC LANGUAGE ENGINE");
            Console.WriteLine("============================================================\n");

            var env = new SaelEnvironment();

            // Initialize entities
            Console.WriteLine("[SYSTEM] Initializing Entities...");
            var alice = env.GetOrCreateEntity("Alice");
            alice.Properties["balance"] = "100";
            var bob = env.GetOrCreateEntity("Bob");
            bob.Properties["balance"] = "50";
            var book = env.GetOrCreateEntity("Book");
            book.Properties["owner"] = "Bob";
            
            var myCar = env.GetOrCreateEntity("car");
            myCar.Properties["position"] = "garage";
            var iEntity = env.GetOrCreateEntity("I");
            iEntity.Properties["position"] = "garage";

            env.PrintState();

            // Run standard examples
            string saelText1 = "commerce :: @TRANSFER { actor=Alice, recipient=Bob, item=Book, value=10 } -> Alice.balance => -10; Bob.balance => +10; Book.owner => Alice";
            RunExample(env, saelText1, "1. TRANSACTIONAL EXCHANGE (COMMERCE)");

            string saelText2 = "physics :: @RELOCATE { actor=I, vehicle=car, origin=garage, destination=grocery_store } -> car.position => to grocery_store; I.position => to grocery_store";
            RunExample(env, saelText2, "2. PHYSICAL LOCOMOTION (PHYSICS)");

            // Run predictive parser example
            Console.WriteLine("\n[PREDICTIVE SCENARIO] Feeding raw natural language to the predictive parser...");
            string rawSentence = "Bob drove the rocket from garage to death";
            RunPredictiveExample(env, rawSentence, "3. PREDICTIVE WAVEFUNCTION PARSING (PHYSICAL RELOCATION CRASH)");

            // Enter interactive shell mode
            Console.WriteLine("\n============================================================");
            Console.WriteLine("    ENTERED DYNAMIC INTERACTIVE SAEL TRANSLATION SHELL");
            Console.WriteLine("============================================================");
            Console.WriteLine("Type any SAEL expression (or raw English sentence) and press Enter.");
            Console.WriteLine("Type 'exit' to quit.\n");
            
            while (true)
            {
                Console.Write("SAEL> ");
                string input = Console.ReadLine();
                if (string.IsNullOrWhiteSpace(input)) continue;
                if (input.Trim().Equals("exit", StringComparison.OrdinalIgnoreCase))
                {
                    Console.WriteLine("Exiting shell. Goodbye.");
                    break;
                }

                try
                {
                    string trimmed = input.Trim();
                    if (trimmed.Contains("::") && trimmed.Contains("->"))
                    {
                        RunExample(env, trimmed, "Interactive Translation (Explicit SAEL)");
                    }
                    else
                    {
                        RunPredictiveExample(env, trimmed, "Interactive Translation (Predictive Natural Language)");
                    }
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"\n[ERROR]: Failed to execute: {ex.Message}");
                    Console.ResetColor();
                }
            }
        }

        private static void RunPredictiveExample(SaelEnvironment env, string rawText, string title)
        {
            try
            {
                var parsedExpr = SaelPredictiveParser.ParseNaturalLanguage(rawText, "physics");
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine($"\n[COMPILE SUCCESS] Synthesized SAEL Expression: {parsedExpr}");
                Console.ResetColor();

                RunExample(env, parsedExpr.ToString(), title);
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"\n[PREDICTIVE FAILURE] Wavefunction did not converge: {ex.Message}");
                Console.ResetColor();
                throw;
            }
        }

        private static void RunExample(SaelEnvironment env, string saelInput, string title)
        {
            Console.WriteLine($"\n============================================================");
            Console.WriteLine($"RUNNING SCENARIO: {title}");
            Console.WriteLine($"============================================================");
            Console.WriteLine($"Input SAEL: {saelInput}\n");

            // 1. Parse
            Console.WriteLine("[PARSING SAEL EXPRESSION...]");
            var parsed = SaelParser.Parse(saelInput);
            Console.WriteLine($"  Parsed Context: {parsed.Context}");
            Console.WriteLine($"  Parsed Action:  {parsed.Action}");
            Console.WriteLine("  Parameters:");
            foreach (var kv in parsed.Parameters)
                Console.WriteLine($"    - {kv.Key} = {kv.Value}");
            Console.WriteLine("  Effects:");
            foreach (var eff in parsed.Effects)
                Console.WriteLine($"    - {eff}");

            // 2. Evaluate Morality
            Console.WriteLine("\n[EVALUATING MORAL GEOMETRY (u, psi)...]");
            var projection = SaelProjector.Project(parsed);
            var verdict = SaelTautonicBridge.FormatMoralVerdict(projection.u, projection.psi);
            Console.WriteLine($"  Result: {verdict}");
            Console.WriteLine($"  Matched: {projection.matchedBranch}");

            // 3. Map to Tautonic 7-Plane Idea
            Console.WriteLine("\n[MAPPING TO TAUTONIC 7-PLANE IDEA...]");
            var idea = SaelTautonicBridge.MapToTautonicIdea(parsed, projection.u, projection.psi, projection.planeScores, projection.planePositions);
            Console.WriteLine($"  Plane Assignments:");
            Console.WriteLine($"    WHO    (Identity):    {idea.Who.Answer.Word,-15} | Score: {idea.Who.Score:F4} ({idea.Who.MoralAlignment.Alignment,-25}) | Modal: {idea.Who.Answer.Position} [{idea.Who.Answer.GetModalCoordinates()}]");
            Console.WriteLine($"    WHAT   (Substance):   {idea.What.Answer.Word,-15} | Score: {idea.What.Score:F4} ({idea.What.MoralAlignment.Alignment,-25}) | Modal: {idea.What.Answer.Position} [{idea.What.Answer.GetModalCoordinates()}]");
            Console.WriteLine($"    WHERE  (Locus):       {idea.Where.Answer.Word,-15} | Score: {idea.Where.Score:F4} ({idea.Where.MoralAlignment.Alignment,-25}) | Modal: {idea.Where.Answer.Position} [{idea.Where.Answer.GetModalCoordinates()}]");
            Console.WriteLine($"    WHY    (Purpose):     {idea.Why.Answer.Word,-15} | Score: {idea.Why.Score:F4} ({idea.Why.MoralAlignment.Alignment,-25}) | Modal: {idea.Why.Answer.Position} [{idea.Why.Answer.GetModalCoordinates()}]");
            Console.WriteLine($"    HOW    (Method):      {idea.How.Answer.Word,-15} | Score: {idea.How.Score:F4} ({idea.How.MoralAlignment.Alignment,-25}) | Modal: {idea.How.Answer.Position} [{idea.How.Answer.GetModalCoordinates()}]");
            Console.WriteLine($"    CAUSE  (History):     {idea.Cause.Answer.Word,-15} | Score: {idea.Cause.Score:F4} ({idea.Cause.MoralAlignment.Alignment,-25}) | Modal: {idea.Cause.Answer.Position} [{idea.Cause.Answer.GetModalCoordinates()}]");
            Console.WriteLine($"    EFFECT (Outcome):     {idea.Effect.Answer.Word,-15} | Score: {idea.Effect.Score:F4} ({idea.Effect.MoralAlignment.Alignment,-25}) | Modal: {idea.Effect.Answer.Position} [{idea.Effect.Answer.GetModalCoordinates()}]");

            Console.WriteLine($"\n  Evaluating Coherence Gate:");
            string gateResult = Judgement.Evaluate(idea);
            Console.WriteLine($"    Net Coherence (R_net): {idea.NetCoherence:F4}");
            Console.WriteLine($"    Coherence Gate Verdict: {gateResult}");

            // 4. Execute State Transition
            Console.WriteLine("\n[EXECUTING STATE MUTATIONS...]");
            env.ExecuteTransition(parsed);
            env.PrintState();
        }
    }
}

