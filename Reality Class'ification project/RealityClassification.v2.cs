using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace RealityClassification
{
    // ============================================================
    // THE METACLASS: the fixed 7-plane skeleton.
    // Never revised at runtime. All generated classes live inside it.
    // ============================================================
    public enum Plane
    {
        Who = 1,    // Metaphysical - Will and Direction (driver axis)
        What = 2,   // Possible     - Faith and Probability   (+x)
        Where = 3,  // Physical     - Matter and Distance     (-x)
        Why = 4,    // Lyrical      - Meaning and Resonance   (+y)
        How = 5,    // Logical      - Count and Consistency   (-y)
        Cause = 6,  // Historical   - Sequence and Causality  (+z)
        Effect = 7  // Emotive      - Passion and Consequence (-z)
    }

    // The five-position modal tile: the Universal Relativity Frame.
    // Replaces Polarity. One grammar, instantiated per plane.
    public enum ModalPosition
    {
        Are,        // center: present assertion, the anchor
        CanBe,      // top-left: open possibility
        NotAll,     // top-right: bounded negation, exclusion with remainder
        NotReally,  // bottom-left: soft negation, qualified denial
        WasLike,    // bottom-right: analogical past, resemblance-memory
        InGap       // between positions: triggers drill into sub-frame
    }

    // Fill state of a TruthState well. The hole exists before content.
    public enum FillState
    {
        Carved,      // hole exists, no accretion yet
        Accreting,   // material falling in
        Filled,      // === reached: coherence gate passed
        Fundamental, // TBE: irreducible units hit, no further frame resolves
        FalseFill,   // cross-plane disagreement detected after apparent fill
        NeverFilled  // budget exhausted: diagnostic, escalate up-channel
    }

    public enum SemanticRelation { Similar, Equivalent, Derivative, Opposite, None }

    // ============================================================
    // TENSOR RANKS: everything is a vector at a rank of one tensor.
    // Rank 0 (Character) is the alphabet: the fundamental basis set,
    // and the literal TBE floor. Rank n identities are compositions
    // of rank n-1 components. Meaning-finding is contraction down
    // the ladder: alphabet-TS matches word-TS matches meaning-TS.
    // ============================================================
    public enum TensorRank
    {
        Character = 0, // the alphabet: irreducible basis, Fundamental by definition
        Word = 1,      // composition over rank-0 vectors
        Phrase = 2,    // composition over rank-1 vectors
        Meaning = 3    // the contraction target: full 7-plane semantic object
    }

    // ============================================================
    // THE ADDRESS: the interrogative path IS the identity.
    // Compositional, ordered, non-commutative. Q4.q5 != Q5.q4.
    // ============================================================
    public readonly struct QqciAddress : IEquatable<QqciAddress>
    {
        public readonly Plane[] Path; // e.g. [Why, How] = Q4.q5, "How of Why"

        // Language tier: a distinct set of planes hung at the same tier.
        // 0 = the language-agnostic root (the convergence target the
        // per-language instances mix into). 1..n = specific languages.
        // Same relativity grammar, different instantiation per language.
        public readonly int Language;

        public QqciAddress(int language, params Plane[] path)
        {
            if (path == null || path.Length == 0)
                throw new ArgumentException("An address requires at least one plane.");
            Language = language;
            Path = path;
        }

        public QqciAddress(params Plane[] path) : this(0, path) { }

        // Drill operator (+i): descend one interrogative deeper. Language preserved.
        public QqciAddress Drill(Plane next) => new(Language, Path.Append(next).ToArray());

        // Ascend for up-channel escalation. Root addresses return themselves.
        public QqciAddress Ascend() =>
            Path.Length > 1 ? new(Language, Path.Take(Path.Length - 1).ToArray()) : this;

        // Cross-language move: the same interrogative path in another language plane.
        public QqciAddress InLanguage(int language) => new(language, Path);

        public int Depth => Path.Length;
        public Plane Leaf => Path[^1];   // the operating interrogative
        public Plane Root => Path[0];    // the domain being operated over

        public string Canonical =>
            $"L{Language}:" + string.Join(".", Path.Select((p, i) => i == 0 ? $"Q{(int)p}" : $"q{(int)p}"));

        // Deterministic content-addressed ID. Same path + word = same ID, always.
        // This is what makes Query IS the Write idempotent. No Random.
        public static long AxomicID(QqciAddress addr, string word)
        {
            var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(addr.Canonical + "|" + word));
            return BitConverter.ToInt64(bytes, 0);
        }

        public bool Equals(QqciAddress other) =>
            Language == other.Language && Path.SequenceEqual(other.Path);
        public override bool Equals(object obj) => obj is QqciAddress a && Equals(a);
        public override int GetHashCode() => Canonical.GetHashCode();
        public override string ToString() => Canonical;
    }

    // ============================================================
    // COHERENCE: a 7-vector, never a scalar.
    // Cross-plane disagreement is the false-fill detector.
    // ============================================================
    public readonly struct CoherenceVector
    {
        private readonly float[] _v; // indexed 0..6 for planes 1..7

        public CoherenceVector(float[] v)
        {
            if (v == null || v.Length != 7)
                throw new ArgumentException("Coherence is defined over exactly 7 planes.");
            _v = v;
        }

        public float this[Plane p] => _v[(int)p - 1];
        public float Net => _v.Average();

        // Max pairwise divergence between plane scores.
        // High divergence at apparent fill = FalseFill.
        public float Disagreement => _v.Max() - _v.Min();

        // Interpretable mixing weights: "40% Q4, 30% Q6, 30% Q1".
        public IReadOnlyDictionary<Plane, float> MixWeights()
        {
            var localV = _v;
            float sum = localV.Sum();
            return Enumerable.Range(1, 7).ToDictionary(
                i => (Plane)i,
                i => sum > 0 ? localV[i - 1] / sum : 0f);
        }
    }

    // ============================================================
    // MEANING: a QANode instance. Content within the skeleton.
    // No constructor side effects; the Registry owns admission.
    // ============================================================
    public class Meaning
    {
        public string Word { get; }
        public string DefinitiveMeaning { get; }
        public string Pronunciation { get; init; }
        public QqciAddress Address { get; }
        public long AxomicID { get; }
        public TensorRank Rank { get; }
        public List<long> Components { get; } = new(); // AxomicIDs at rank - 1
        public ModalPosition Position { get; set; } = ModalPosition.Are;
        public CoherenceVector Coherence { get; set; }
        public List<Meaning> SubMeanings { get; } = new();
        public List<(long AxomicID, SemanticRelation Relation)> Related { get; } = new();
        public DateTime FirstCarved { get; }   // temporal layer, kept as metadata not address

        public Meaning(string word, QqciAddress address, string definitiveMeaning = null,
            TensorRank rank = TensorRank.Meaning, IEnumerable<long> components = null)
        {
            Word = word;
            Address = address;
            DefinitiveMeaning = definitiveMeaning ?? word;
            Rank = rank;
            if (components != null) Components.AddRange(components);

            // Compositional identity: rank-0 IDs hash from address + symbol;
            // rank n > 0 IDs hash from address + ordered component IDs, so a
            // word IS its letters and a phrase IS its words. Identity derives
            // from composition, never assigned from outside.
            AxomicID = Components.Count > 0
                ? QqciAddress.AxomicID(address, string.Join(",", Components))
                : QqciAddress.AxomicID(address, word);

            FirstCarved = DateTime.UtcNow;

            // Rank 0 is the TBE floor: irreducible by definition.
            if (rank == TensorRank.Character) Position = ModalPosition.Are;
        }

        public void AddRelated(Meaning other, SemanticRelation relation) =>
            Related.Add((other.AxomicID, relation));
    }

    // ============================================================
    // TRUTHSTATE: the document template. The carved hole.
    // Slots are generated from the interrogative path (compositional
    // typing: the leaf interrogative operating over the root domain).
    // A filled TS is both a deliverable and the bounded pool for the
    // next recursion level.
    // ============================================================
    public class TruthState
    {
        public QqciAddress Address { get; }
        public FillState State { get; private set; } = FillState.Carved;
        public List<Meaning> AccretedPool { get; } = new(); // the bounded space
        public Dictionary<Plane, Meaning> Slots { get; } = new(); // template slots
        public TruthState Parent { get; private set; }       // up-channel
        public List<TruthState> Children { get; } = new();   // recursion levels
        public int Budget { get; }                            // depth/effort cap
        public float FillTolerance { get; }

        public TruthState(QqciAddress address, int budget = 7, float fillTolerance = 0.1f)
        {
            Address = address;
            Budget = budget;
            FillTolerance = fillTolerance;
        }

        // --- Excavation: the hole pulls material in. ---
        public void Accrete(Meaning m)
        {
            if (State is FillState.Filled or FillState.Fundamental) return;
            State = FillState.Accreting;
            AccretedPool.Add(m);
            // Slot assignment: material settles into the sub-basin of its root plane.
            Slots.TryAdd(m.Address.Root, m);
        }

        // --- The Coherence Gate Axiom, now vectorised: ---
        // [Q|A / A|Q] === { Y=1; N!=1; Insult > 1 } per plane,
        // with cross-plane disagreement as the false-fill check.
        public FillState EvaluateFill(CoherenceVector coherence)
        {
            float net = coherence.Net;
            bool inBand = net >= 1.0f - FillTolerance && net <= 1.0f + FillTolerance;

            if (inBand && coherence.Disagreement <= FillTolerance * 2)
                State = FillState.Filled;                       // === : Y=1 (TRUTH)
            else if (inBand)
                State = FillState.FalseFill;                    // planes disagree
            else if (net > 1.0f + FillTolerance)
                State = FillState.FalseFill;                    // Insult > 1 (CHAOS)
            else
                State = FillState.Accreting;                    // N != 1, keep pulling

            return State;
        }

        // --- Recursion: a filled TS becomes the universe of the next level. ---
        public TruthState DrillInto(Plane nextInterrogative)
        {
            if (State != FillState.Filled)
                throw new InvalidOperationException(
                    "Staircase gating: a step must fill before it overflows. " +
                    $"Current state: {State}.");
            if (Address.Depth >= Budget)
            {
                State = FillState.Fundamental; // TBE by budget: treat as irreducible
                return null;
            }
            var child = new TruthState(Address.Drill(nextInterrogative), Budget, FillTolerance)
            {
                Parent = this
            };
            // The child's addressable universe is the parent's accreted pool.
            Children.Add(child);
            return child;
        }

        // --- Up-channel: never-fills and false-fills escalate and widen. ---
        public TruthState Escalate()
        {
            if (Parent == null) { State = FillState.NeverFilled; return null; }
            Parent.State = FillState.Accreting; // re-open the parent hole, widen the pool
            return Parent;
        }
    }

    // ============================================================
    // REGISTRY: flat, content-addressed, O(1). No six-deep scans.
    // Query IS the Write: carving an address that exists returns it;
    // carving one that doesn't creates and persists it.
    // ============================================================
    public static class MeaningRegistry
    {
        private static readonly Dictionary<long, Meaning> ById = new();
        private static readonly Dictionary<string, List<long>> ByWord = new();

        public static Meaning CarveOrRecall(string word, QqciAddress address, string definitiveMeaning = null,
            TensorRank rank = TensorRank.Meaning, IEnumerable<long> components = null)
        {
            var comps = components?.ToList();
            long id = comps is { Count: > 0 }
                ? QqciAddress.AxomicID(address, string.Join(",", comps))
                : QqciAddress.AxomicID(address, word);
            if (ById.TryGetValue(id, out var existing)) return existing; // recall: the residual warp

            var m = new Meaning(word, address, definitiveMeaning, rank, comps); // write: the query carves
            ById[m.AxomicID] = m;
            if (!ByWord.TryGetValue(word, out var list)) ByWord[word] = list = new();
            list.Add(m.AxomicID);
            return m;
        }

        // --- The contraction ladder: alphabet-TS matches word-TS matches meaning-TS. ---
        // A raw string is decomposed to its rank-0 vectors, composed upward to a
        // rank-1 identity, and that identity indexes rank-2+ meanings. Each step is
        // a contraction: the query's component IDs against stored compositions.
        public static Meaning Contract(string raw, QqciAddress address)
        {
            var charIds = raw.Select(c =>
                CarveOrRecall(c.ToString(), new QqciAddress(address.Language, address.Root),
                    rank: TensorRank.Character).AxomicID).ToList();

            var wordTs = CarveOrRecall(raw, address, rank: TensorRank.Word, components: charIds);

            // Meaning lookup: any stored rank-2+ node containing this word identity.
            return ById.Values.FirstOrDefault(m =>
                       m.Rank >= TensorRank.Phrase && m.Components.Contains(wordTs.AxomicID))
                   ?? wordTs; // no higher fill yet: the word-TS is the deepest resolved rank
        }

        public static Meaning Get(long axomicID) =>
            ById.TryGetValue(axomicID, out var m) ? m : null;

        // All plane-instances of a word: its full 7-plane decomposition.
        public static IEnumerable<Meaning> GetByWord(string word) =>
            ByWord.TryGetValue(word, out var ids)
                ? ids.Select(id => ById[id])
                : Enumerable.Empty<Meaning>();

        public static int Count => ById.Count;
    }

    // ============================================================
    // ALPHABET: the rank-0 TS seed. The enumerable TBE floor.
    // Seeding a language's alphabet defines what "fundamentals are
    // hit" means for every drill within that language plane.
    // ============================================================
    public static class Alphabet
    {
        public static IReadOnlyList<Meaning> Seed(int language, string letters)
        {
            var seeded = new List<Meaning>();
            foreach (var c in letters)
            {
                // Rank-0 units are carved at the Where root (physical symbol)
                // of their language plane; irreducible by definition.
                var m = MeaningRegistry.CarveOrRecall(
                    c.ToString(),
                    new QqciAddress(language, Plane.Where),
                    rank: TensorRank.Character);
                seeded.Add(m);
            }
            return seeded;
        }
    }

    // ============================================================
    // SYNERGY: the Belief Axiom, kept from v1.
    // Belief = 1 + 1 = 2. Expansion only on gated truth.
    // ============================================================
    public static class Synergy
    {
        public static int Process(int worldviewState, TruthState ts) =>
            ts.State == FillState.Filled ? worldviewState + 1 : worldviewState;
    }
}
