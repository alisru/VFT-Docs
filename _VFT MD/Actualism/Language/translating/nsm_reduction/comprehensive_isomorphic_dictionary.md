# Comprehensive Isomorphic Scaling Dictionary

This document maps the broader English vocabulary to the 31 core base semantic anchors using polarity scaling modifiers (`+` and `-`).

---

## Mappings by Axis Category

### 1. Motion & Locomotion (Bases: `run`, `walk`, `fly`, `go`, `do`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **sprint** | `run+++` | Maximum scale running speed |
| **dash / bolt / race** | `run+++` | Maximum scale running speed |
| **jog / trot / canter** | `run-` | Slower than typical running speed |
| **scurry / scramble** | `run` | Typical running speed in a confined space |
| **walk** | `walk` | Default walking speed |
| **stroll / amble / wander** | `walk-` | Slower/relaxed walking speed |
| **saunter / crawl (traffic)** | `walk--` | Extremely slow walking speed |
| **march / stride / pace** | `walk+` | Faster/assertive walking speed |
| **crawl / creep / slither** | `go---` | Absolute minimum movement speed (on belly/ground) |
| **swim / float** | `go` | Movement through fluid medium |
| **dive / plunge / sink** | `go---` | Vertical downward movement |
| **climb / ascend / scale** | `go+` | Vertical upward movement |
| **soar / glide** | `fly+` | High-efficiency flying |
| **hover / flutter** | `fly-` | Minimal flying height or stationary flying |

### 2. Vocal Volume & Expression (Bases: `say`, `laugh`, `cry`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **scream / shout / shriek** | `say+++` | Maximum vocal volume/intensity |
| **yell / bellow / roar** | `say+++` | Maximum vocal volume/intensity |
| **whisper / mutter / murmur** | `say---` | Minimum vocal volume/intensity |
| **mumble** | `say--` | Low vocal volume/clarity |
| **converse / talk / discuss** | `say` | Default vocal volume/intensity |
| **sing / chant** | `say+` | Tuned/rhythmic vocal expression |
| **giggle / chuckle / snicker** | `laugh-` | Low-intensity laughter |
| **guffaw / cackle / roar** | `laugh+++` | Maximum-intensity laughter |
| **weep / sob / wail** | `cry+++` | Maximum-intensity crying |
| **whimper / sniffle / sigh** | `cry-` | Low-intensity crying/distress |

### 3. Quality & Value Evaluation (Bases: `good`, `bad`, `true`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **excellent / perfect / superb** | `good+++` | Maximum positive value/quality |
| **wonderful / magnificent** | `good+++` | Maximum positive value/quality |
| **satisfactory / decent / fine** | `good+` | Minor positive value/quality |
| **terrible / horrific / awful** | `bad+++` | Maximum negative value/quality |
| **evil / vile / disastrous** | `bad+++` | Maximum negative value/quality |
| **poor / mediocre / subpar** | `bad+` | Minor negative value/quality |
| **correct / factual / valid** | `true` | Standard match to reality |
| **flawless / absolute truth** | `true+++` | Maximum match to reality |
| **false / fake / incorrect** | `true---` | Absolute mismatch to reality (lie) |

### 4. Size & Dimension (Bases: `big`, `small`, `long`, `short`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **huge / gigantic / colossal** | `big+++` | Maximum size scale |
| **massive / immense / vast** | `big+++` | Maximum size scale |
| **tiny / microscopic / minute** | `small+++` | Minimum size scale |
| **short / brief** | `short` | Default small duration/length |
| **momentary / fleeting** | `short+++` | Minimum duration scale |
| **extended / stretched** | `long+` | Length greater than typical |
| **infinite / endless** | `long+++` | Maximum length/duration scale |

### 5. Mind, Sensation & Affinity (Bases: `know`, `think`, `want`, `feel`, `see`, `hear`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **prove / verify** | `know+++` | Maximum factual certainty |
| **suspect / guess / assume** | `think-` | Low-certainty cognition |
| **doubt / question** | `think--` | Moderate uncertainty cognition |
| **disbelieve / deny** | `know---` | Maximum negation of certainty |
| **crave / yearn / covet** | `want+++` | Maximum intensity of desire |
| **wish / prefer / hope** | `want-` | Low intensity of desire |
| **love / adore / cherish** | `feel+++` | Maximum positive affinity |
| **like / appreciate** | `feel+` | Moderate positive affinity |
| **dislike / resent** | `feel-` | Moderate negative affinity |
| **hate / despise / detest / loathe**| `feel---` | Maximum negative affinity |
| **gaze / stare / watch** | `see+` | High-duration active sight |
| **glance / glimpse / peek** | `see-` | Low-duration passive sight |
| **listen / attend** | `hear+` | Active auditory attention |
| **eavesdrop / overhear** | `hear++` | High-focus covert auditory attention |

### 6. Temperature (Bases: `hot`, `cold`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **boiling / scalding / scorching** | `hot+++` | Maximum thermal energy |
| **warm / tepid / mild** | `hot-` | Moderate thermal energy |
| **freezing / icy / frigid** | `cold+++` | Maximum coldness |
| **cool / chilly / brisk** | `cold-` | Moderate coldness |

### 7. Space & Proximity (Bases: `place`, `near`, `far`, `above`, `below`, `side`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **adjacent / touching / close** | `near+++` | Minimum spatial distance |
| **distant / remote / isolated** | `far+++` | Maximum spatial distance |
| **over / overhead** | `above` | Standard higher vertical coordinate |
| **zenith / apex** | `above+++` | Maximum vertical coordinate |
| **under / underneath** | `below` | Standard lower vertical coordinate |
| **abyss / bottom** | `below+++` | Minimum vertical coordinate |
| **lateral / beside** | `side` | Side coordinate |

### 8. Time & Frequency (Bases: `time`, `now`, `before`, `after`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **always / eternal / perpetual** | `time+++` | Continuous temporal existence |
| **never** | `time---` | Zero temporal existence |
| **often / frequently / constantly** | `time+` | High temporal frequency |
| **rarely / seldom / occasionally** | `time-` | Low temporal frequency |
| **instantly / immediately** | `now+++` | Zero temporal delay |
| **past / yesterday** | `before` | Prior temporal state |
| **future / tomorrow** | `after` | Subsequent temporal state |

### 9. Quantities & Totality (Bases: `one`, `two`, `some`, `many`)

| English Word | Scaled Equivalent | Axis & Degree Description |
| :--- | :--- | :--- |
| **all / every / whole** | `many+++` | Maximum quantity / totality |
| **none / zero / void** | `many---` | Zero quantity |
| **few / sparse / scarce** | `some-` | Less than some quantity |
| **crowd / assembly / mass** | `many+` | High quantity collective |
| **pile / heap / stack** | `many+` | High quantity object stack |
