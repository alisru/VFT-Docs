# The Reduced Dictionary: Isomorphic Prime & Word Scaling

This dictionary combines the scaling modifier system applied to:
1.  **NSM Prime Reduction:** Scaling the 65 Natural Semantic Metalanguage (NSM) primes along their distinct spectrum axes, removing redundant intensifiers, quantifiers, and temporal durations.
2.  **Lexicon-Wide Spectral Mapping:** Mapping complex, specific English words to these base words decorated with scaling modifiers (`+` and `-`) along continuous spectrums.

---

## 1. Grammar & Modifier Specification

Every semantic axis has a default state and scales in positive or negative directions:

### The Spectrum Template: `---word+++`

*   **`word`** = The typical, default intensity or speed of the concept on its axis.
*   **`word+`** = One degree greater than typical (e.g., faster, larger, louder).
*   **`word++`** = Very high intensity.
*   **`word+++`** = Absolute maximum capability, limit, or degree.
*   **`word-`** = One degree less than typical (e.g., slower, smaller, quieter).
*   **`word--`** = Very low intensity.
*   **`word---`** = Absolute minimum capability, limit, or degree.

---

## Part I: Reduction of the 65 NSM Primes to the Core Bases

By using the modifier scaling stack (`+` and `-`), we can eliminate redundant primes representing intensity, quantity, or duration. 

Categorical, non-spectral concepts (like substantives, logical operators, and physical interactions) are preserved as **distinct base anchors** and are not collapsed. Modifiers are only applied to scale their intensity when applicable:

### 1. Intensification (2 Primes $\rightarrow$ Replaced by Modifiers)
*   **`VERY`** $\rightarrow$ Replaced by `+` (e.g., `good+` for very good)
*   **`MORE`** $\rightarrow$ Replaced by `++` (e.g., `big++` for much bigger)

### 2. Time & Durations (8 Primes $\rightarrow$ 5 Bases)
We keep `time`, `now`, `before`, and `after` as distinct anchors. We remove durations:
*   **`TIME` / `WHEN`** $\rightarrow$ `time`
*   **`NOW`** $\rightarrow$ `now`
*   **`BEFORE` / `PAST`** $\rightarrow$ `before`
*   **`AFTER` / `FUTURE`** $\rightarrow$ `after`
*   **`A LONG TIME`** $\rightarrow$ `time+++` (Maximum duration)
*   **`A SHORT TIME`** $\rightarrow$ `time-` (Minimum duration)
*   **`MOMENT`** $\rightarrow$ `time---` (Instantaneous point)
*   **`FOR SOME TIME`** $\rightarrow$ `time+` (Moderate duration)

### 3. Quantifiers (6 Primes $\rightarrow$ 4 Bases)
We keep `one`, `two`, `some`, and `many` as distinct anchors. We remove `all` and `few`:
*   **`ONE`** $\rightarrow$ `one`
*   **`TWO`** $\rightarrow$ `two`
*   **`SOME`** $\rightarrow$ `some`
*   **`MANY`** $\rightarrow$ `many`
*   **`ALL`** $\rightarrow$ `many+++` (Maximum limit of quantity)
*   **`FEW / LITTLE`** $\rightarrow$ `some-` (Less than some)

### 4. Evaluators & Descriptors (4 Primes $\rightarrow$ preserved as distinct anchors)
*   **`GOOD`** $\rightarrow$ `good` (`good+++` = excellent / perfect)
*   **`BAD`** $\rightarrow$ `bad` (`bad+++` = terrible / horrific)
*   **`BIG`** $\rightarrow$ `big` (`big+++` = gigantic / colossal)
*   **`SMALL`** $\rightarrow$ `small` (`small+++` = tiny / microscopic)

### 5. Cognition & Perception (6 Primes $\rightarrow$ preserved as distinct anchors)
*   **`KNOW`** $\rightarrow$ `know` (`know+++` = proven with absolute certainty)
*   **`THINK`** $\rightarrow$ `think` (`think-` = guess / suspect)
*   **`WANT`** $\rightarrow$ `want` (`want+++` = crave)
*   **`FEEL`** $\rightarrow$ `feel` (`feel+++` = love)
*   **`SEE`** $\rightarrow$ `see` (`see+` = stare)
*   **`HEAR`** $\rightarrow$ `hear` (`hear+` = listen)

### 6. Substantives (6 Primes $\rightarrow$ preserved as distinct anchors)
*   **`I`** $\rightarrow$ `I`
*   **`YOU`** $\rightarrow$ `you`
*   **`SOMEONE`** $\rightarrow$ `someone`
*   **`PEOPLE`** $\rightarrow$ `people`
*   **`SOMETHING / THING`** $\rightarrow$ `thing`
*   **`BODY`** $\rightarrow$ `body`

### 7. Other Non-Spectral Primes (Preserved as distinct anchors)
These categorical concepts do not represent spectrums and are not collapsed:
*   **`KIND`** $\rightarrow$ `kind`
*   **`PART`** $\rightarrow$ `part`
*   **`THIS`** $\rightarrow$ `this`
*   **`OTHER / ELSE`** $\rightarrow$ `other`
*   **`THE SAME`** $\rightarrow$ `same`
*   **`SAY`** $\rightarrow$ `say`
*   **`WORDS`** $\rightarrow$ `words`
*   **`TRUE`** $\rightarrow$ `true`
*   **`DO`** $\rightarrow$ `do`
*   **`HAPPEN`** $\rightarrow$ `happen`
*   **`MOVE`** $\rightarrow$ `move`
*   **`TOUCH`** $\rightarrow$ `touch`
*   **`BE (SOMEWHERE)`** $\rightarrow$ `be`
*   **`THERE IS`** $\rightarrow$ `there is`
*   **`HAVE`** $\rightarrow$ `have`
*   **`BE (SOMEONE/THING)`** $\rightarrow$ `be`
*   **`LIVE`** $\rightarrow$ `live`
*   **`DIE`** $\rightarrow$ `die`
*   **`PLACE`** $\rightarrow$ `place`
*   **`HERE`** $\rightarrow$ `here`
*   **`ABOVE`** $\rightarrow$ `above`
*   **`BELOW`** $\rightarrow$ `below`
*   **`SIDE`** $\rightarrow$ `side`
*   **`INSIDE`** $\rightarrow$ `inside`
*   **`NEAR`** $\rightarrow$ `near`
*   **`FAR`** $\rightarrow$ `far`
*   **`CAN`** $\rightarrow$ `can`
*   **`MAYBE`** $\rightarrow$ `maybe`
*   **`BECAUSE`** $\rightarrow$ `because`
*   **`IF`** $\rightarrow$ `if`
*   **`NOT`** $\rightarrow$ `-` (Negation overlay)
*   **`LIKE / WAY`** $\rightarrow$ `like`

---

## Part II: Lexicon-Wide Spectral Mapping (Complex English Examples)

For words that naturally exist along a continuous spectrum, we redirect the specific English word to a scaled base-word container:

### 1. Motion & Speed (Base: `run`, `walk`, `fly`, `go`)

| Specialized Word | Isomorphic Scaled Equivalent | Description / Axis Context |
| :--- | :--- | :--- |
| **sprint / dash / bolt / race** | `run+++` | Maximum capability running |
| **jog / trot** | `run-` | Running slower than typical |
| **crawl / creep / slither** | `go---` | Minimum possible movement speed |
| **stroll / amble / wander** | `walk-` | Walking slower than typical |
| **march / stride** | `walk+` | Walking faster/more intently than typical |
| **soar / glide** | `fly+` | Flying with high capability |
| **hover / flutter** | `fly-` | Minimal flying speed/height |

### 2. Volume & Communication (Base: `say`, `laugh`, `cry`)

| Specialized Word | Isomorphic Scaled Equivalent | Description / Axis Context |
| :--- | :--- | :--- |
| **scream / shout / yell / bellow** | `say+++` | Vocalizing at maximum volume |
| **whisper / mutter / mumble** | `say---` | Vocalizing at minimum volume |
| **giggle / chuckle / snicker** | `laugh-` | Laughing at low intensity/volume |
| **guffaw / howl / roar** | `laugh+++` | Laughing at maximum intensity/volume |
| **weep / sob / wail** | `cry+++` | Crying at maximum intensity |
| **whimper / sniffle** | `cry-` | Crying at low intensity |

### 3. Temperature & Climate (Base: `hot`, `cold`)

| Specialized Word | Isomorphic Scaled Equivalent | Description / Axis Context |
| :--- | :--- | :--- |
| **boiling / scalding / scorching** | `hot+++` | Maximum thermal energy |
| **warm / tepid / mild** | `hot-` | Moderate thermal energy |
| **freezing / icy / frigid** | `cold+++` | Maximum coldness |
| **cool / chilly** | `cold-` | Moderate coldness |

### 4. Sensation, Emotion & Affinity (Base: `feel`, `want`)

| Specialized Word | Isomorphic Scaled Equivalent | Description / Axis Context |
| :--- | :--- | :--- |
| **love / adore / cherish** | `feel+++` | Maximum positive affinity |
| **like / appreciate** | `feel+` | Moderate positive affinity |
| **dislike / resent** | `feel-` | Moderate negative affinity |
| **hate / despise / detest / loathe**| `feel---` | Maximum negative affinity |
| **crave / yearn / covet** | `want+++` | Maximum intensity of desire |
| **wish / prefer** | `want-` | Low intensity of desire |

### 5. Proximity & Space (Base: `near`, `far`)

| Specialized Word | Isomorphic Scaled Equivalent | Description / Axis Context |
| :--- | :--- | :--- |
| **distant / remote** | `far+++` | Maximum spatial distance |
| **adjacent / close / touching** | `near+++` | Minimum spatial distance |

### 6. Frequency & Time (Base: `time`)

| Specialized Word | Isomorphic Scaled Equivalent | Description / Axis Context |
| :--- | :--- | :--- |
| **always / eternal / perpetual** | `time+++` | Continuous frequency |
| **never** | `time---` | Zero frequency |
| **often / frequently** | `time+` | High frequency |
| **rarely / seldom** | `time-` | Low frequency |
