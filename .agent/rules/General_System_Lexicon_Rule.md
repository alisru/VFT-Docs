# Rule: General System Lexicon Collation

## Purpose
This rule defines the procedure for collating specific meaning interpretations into a unified System Lexicon. The lexicon is MANDATED to be structured around the 7x7x7 process (Q.q.c Tensor), using the C# `Meaning` and `Word` class structures from the `Reality Class'ification project` as the formal representation.

## Core Mandate
Whenever a new interpretation or "non-standard" definition is identified (e.g., from personal notes, philosophical cross-references, or VFT derivations), it must be translated into a `Meaning` object and registered in the `MeaningMetaRegistry`.

## Formal Structure (Scale Assumptions)
The dictionary uses a 6-deep nested structure where each level represents a functional **Scale of Assumption**, analogous to the Oldsoul format. These scales define the "geometric scope" of the meaning.

| Layer | Name | Scale of Assumption | Conflict Tier Counterpart |
| :--- | :--- | :--- | :--- |
| **6** | `RegistryLayer` | **Universal/System** | Tier 6/7: Abstract/Truth Warfare |
| **5** | `TemporalLayer` | **Historical/Sequential** | Tier 5: Existential (The Nuke) |
| **4** | `LanguageLayer` | **Cultural/Strategic** | Tier 4: Global (The Missile) |
| **3** | `PhraseLayer` | **Relational/Social** | Tier 3: Regional (The Bomb) |
| **2** | `WordLayer` | **Definition/Lexical** | Tier 2: Group (The Artillery) |
| **1** | `CharLayer` | **Atomic/Action** | Tier 1: Personal (The Gun) |

### Meaning Object Template
```csharp
new Meaning(
    word: "[TERM]",
    definitiveMeaning: "[SYSTEM_DEFINITION]",
    polarity: Polarity.[Neutral|Positive|Negative|Mixed],
    axomicID: [UID],
    wordLayer: [Q], // Plane of Reality (1-7)
    phraseLayer: [q], // Functional Sub-domain (1-7)
    languageLayer: [c], // Atomic Impulse (1-7)
    temporalLayer: [DAY_OF_YEAR],
    registryLayer: [SPECIFIC_DOMAIN_INDEX]
);
```

### Word Registration Template
```csharp
new Word("[TERM]", [MEANING_OBJECT]);
```

## 7x7x7 Structural Mapping
The dictionary does not store words alphabetically; it stores them by **Geometric Location** within the 7x7x7 tensor:
1.  **Q (Plane)**: Maps to `wordLayer`.
2.  **q (Sub-plane)**: Maps to `phraseLayer`.
3.  **c (Atomic)**: Maps to `languageLayer`.


## Collation Procedure
1.  **Extraction**: Identify "words of significance" from the source text (e.g., Q-planes, specific analogies like "The Gun", or "360 degree meaning").
2.  **Mapping**: Determine the `Q.q.c` coordinate using the `7x7x7-meaning.md` interrogative logic.
3.  **Synthesis**: Create a `definitiveMeaning` that reflects the "VFT System Definition" while preserving the original intent.
4.  **Formatting**: Output the C# instantiation code into the target `.cs` dictionary file.

## Domain Registry Layers
- **Layer 0**: General Language.
- **Layer 1**: Physical/Field Math.
- **Layer 7**: Conflict/Warfare Tiers.
- **Layer 9**: Biblical/Metaphysical.
