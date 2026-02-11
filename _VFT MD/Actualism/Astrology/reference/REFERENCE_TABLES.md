# HEGEMONIC ASTROLOGY: REFERENCE TABLES
**Version:** 1.0  
**Purpose:** Quick lookup for calculations and interpretations

---

## ESSENTIAL DIGNITIES TABLE

### Planetary Dignities by Sign

| Planet  | Domicile          | Exaltation | Detriment         | Fall      | Dignity Scores |
|---------|-------------------|------------|-------------------|-----------|----------------|
| Sun     | Leo               | Aries      | Aquarius          | Libra     | +5, +4, -4, -3 |
| Moon    | Cancer            | Taurus     | Capricorn         | Scorpio   | +5, +4, -4, -3 |
| Mercury | Gemini, Virgo     | Virgo      | Sagittarius, Pisces| Pisces   | +5, +4, -4, -3 |
| Venus   | Taurus, Libra     | Pisces     | Scorpio, Aries    | Virgo     | +5, +4, -4, -3 |
| Mars    | Aries, Scorpio    | Capricorn  | Libra, Taurus     | Cancer    | +5, +4, -4, -3 |
| Jupiter | Sagittarius, Pisces| Cancer    | Gemini, Virgo     | Capricorn | +5, +4, -4, -3 |
| Saturn  | Capricorn, Aquarius| Libra     | Cancer, Leo       | Aries     | +5, +4, -4, -3 |

### Scoring System

```
+5 = Domicile (planet rules the sign) - MAXIMUM STRENGTH
+4 = Exaltation (planet honored in the sign) - VERY STRONG
 0 = Neutral (no essential dignity) - MODERATE
-3 = Fall (planet uncomfortable) - DIFFICULT
-4 = Detriment (opposite to domicile) - WEAK
```

### Quick Dignity Check

**For any planet in any sign:**

1. Check if planet rules the sign → Domicile (+5)
2. Check if planet is exalted in the sign → Exaltation (+4)
3. Check if planet is in opposite sign of domicile → Detriment (-4)
4. Check if planet is in opposite sign of exaltation → Fall (-3)
5. If none of above → Neutral (0)

---

## MAJOR ASPECTS TABLE

### Aspect Types and Orbs

| Aspect       | Angle | Orb (Luminaries) | Orb (Planets) | Nature    | i-Layer |
|--------------|-------|------------------|---------------|-----------|---------|
| Conjunction  | 0°    | ±10°             | ±8°           | Fusion    | i1      |
| Semi-sextile | 30°   | ±2°              | ±2°           | Friction  | i4      |
| Sextile      | 60°   | ±6°              | ±6°           | Harmony   | i2      |
| Square       | 90°   | ±8°              | ±6°           | Friction  | i3      |
| Trine        | 120°  | ±8°              | ±6°           | Harmony   | i2      |
| Quincunx     | 150°  | ±3°              | ±3°           | Paradox   | i5      |
| Opposition   | 180°  | ±10°             | ±8°           | Polarity  | i3      |

**Luminaries:** Sun and Moon  
**Planets:** Mercury through Saturn (and outer planets if used)

### Aspect Calculation

**Formula:**
```
aspect_angle = |planet1_longitude - planet2_longitude|

if aspect_angle > 180:
    aspect_angle = 360 - aspect_angle

# Check against aspect table with orbs
for each aspect_type:
    if abs(aspect_angle - aspect_type.angle) <= orb:
        return aspect_type
```

### Aspect Interpretation Quick Reference

**Conjunction (0°):** Fusion, blending, intensification
- Harmonious planets → Synergy
- Challenging planets → Conflict
- Same element → Natural blend
- Different elements → Creative tension

**Sextile (60°):** Opportunity, ease, support
- Requires conscious activation
- Natural talents that need development
- Supportive but not automatic

**Square (90°):** Friction, challenge, motivation
- Different modalities (Cardinal/Fixed/Mutable)
- Internal tension drives growth
- Source of frustration and achievement

**Trine (120°):** Harmony, flow, natural ability
- Same element
- Effortless expression
- Risk of complacency if not developed

**Opposition (180°):** Polarity, awareness, balance
- Same modality, opposite signs
- See-saw effect
- Integration challenge

---

## PLANET-TO-PLANE MAPPING (Q.q Structure)

### The 7 Planes (Q)

| # | Plane         | Interrogative | Domain        | Astrological Body |
|---|---------------|---------------|---------------|-------------------|
| 1 | Meta-Physical | WHO           | Identity      | Sun               |
| 2 | Physical      | WHERE         | Boundaries    | Saturn            |
| 3 | Possible      | WHAT          | Expansion     | Jupiter           |
| 4 | Lyrical       | WHY           | Meaning       | Venus             |
| 5 | Logical       | HOW           | Reasoning     | Mercury           |
| 6 | Historical    | CAUSE         | Action        | Mars              |
| 7 | Emotive       | EFFECT        | Feeling       | Moon              |

### The 7 Senses/Filters (q)

Each planet filters through the zodiac sign it occupies:

| # | Filter     | Quality                           |
|---|------------|-----------------------------------|
| 1 | Identity   | Who-ness, selfhood                |
| 2 | Definition | What-ness, essence                |
| 3 | Matter     | Where-ness, location              |
| 4 | Meaning    | Why-ness, purpose                 |
| 5 | Reason     | How-ness, method                  |
| 6 | Event      | Cause-ness, origin                |
| 7 | Feeling    | Effect-ness, consequence          |

---

## 343-CUBE INTERROGATIVE MAP

### The Structure: [n1.n2.n3]

```
n1 = Primary Plane (which reality domain)
n2 = Interrogative Lens (which filter)
n3 = Measurement Metric (which dimension)
```

### The Seven Interrogatives

| # | Interrogative | Measures            | Examples                    |
|---|---------------|---------------------|-----------------------------|
| 1 | WHO           | Identity, agent     | Which specific person?      |
| 2 | WHAT          | Definition, essence | What is its nature?         |
| 3 | WHERE         | Location, matter    | What physical space?        |
| 4 | WHY           | Purpose, meaning    | What is the significance?   |
| 5 | HOW           | Method, process     | What is the mechanism?      |
| 6 | CAUSE         | Origin, event       | What created this?          |
| 7 | EFFECT        | Result, feeling     | What consequence flows?     |

### Question Generation Formula

**For node [n1.n2.n3]:**

```
Question Template:
"What [n3_interrogative] [n2_interrogative_qualifier] the [n1_plane_domain]?"

Example [1.2.3]:
n1 = 1 (Meta-Physical/WHO plane)
n2 = 2 (WHAT lens)
n3 = 3 (WHERE metric)

Question: "What material location (n3=WHERE) defines (n2=WHAT) 
          this identity (n1=WHO plane)?"

Answer: "The physical body / The home / The primary location 
        of identity manifestation"
```

### Priority Nodes (Minimum for Valid Analysis)

**For ANY planet:**
```
[n.n.1] - WHO of [Interrogative] of [Plane]
[n.n.2] - WHAT of [Interrogative] of [Plane]
[n.n.4] - WHY of [Interrogative] of [Plane]
[n.n.6] - CAUSE of [Interrogative] of [Plane]
[n.n.7] - EFFECT of [Interrogative] of [Plane]
```

**For PRIMARY placement (e.g., Sun in Leo):**
```
[1.1.1] - Core identity
[1.1.7] - Emotional consequence of identity
[1.7.7] - Meta-emotional state
```

**For SECONDARY placement (e.g., Moon in Scorpio):**
```
[7.7.1] - Emotional identity
[7.7.7] - Extinction point / maximum depth
```

---

## TEMPORAL CALCULATIONS

### Secondary Progressions

**Formula:**
```
progressed_date = birth_date + current_age_in_days

Example:
Birth: July 28, 1993
Current Age: 32 years
Progressed Date: July 28, 1993 + 32 days = August 29, 1993

Calculate planetary positions for August 29, 1993
These are the progressed positions at age 32
```

**Progressed Sun Sign Changes:**
```
Sun moves ~1° per day = ~30° per 30 days = ~30° per 30 years

Average time in each sign: ~30 years
Key transitions typically around ages: 3, 33, 63, 93
```

**Progressed Moon Cycle:**
```
Moon moves ~13° per day = ~13° per year

Full zodiac cycle: ~28 years
Returns to natal position ages: 0, 28-29, 56-58, 84-86

Sign changes every ~2.5 years
```

### Major Cycles

**Jupiter Return:** Every ~12 years
```
Ages: 12, 24, 36, 48, 60, 72, 84, 96
Theme: Expansion, growth, opportunity, belief systems
```

**Saturn Return:** Every ~29.5 years
```
Ages: 29-30, 58-60, 88-90
Theme: Reality check, maturity, responsibility, structures
```

**Uranus Opposition:** Age ~42
```
Age: 40-44 (Uranus at 180° from natal position)
Theme: Mid-life awakening, revolution, authenticity
```

**Chiron Return:** Age ~50
```
Age: 48-52
Theme: Healing, wisdom, teaching, integration of wounds
```

---

## 252 STATES OF BEING MATRIX

### The Six Will States

**Personal Will Options:**
```
+? = Inquiring (seeking to know)
~? = Indifferent (neutral)
-? = Rejecting (actively avoiding)
=  = Believing (settled on truth)
<  = Denying (settled on falsehood)
>  = Dismissing (contemptuous rejection)
```

**Social Will Options:** Same 6 states applied to perceived social consensus

### The Seven Objective Frames

```
0. Natural State (unknown truth value)
1. Good Truth (true and beneficial)
2. Bad Truth (true but harmful)
3. Good Lie (false but beneficial)
4. Bad Lie (false and harmful)
5. Good Preference (beneficial but unknown truth)
6. Bad Preference (harmful but unknown truth)
```

### Matrix Calculation

```
Base States: 6 (Personal) × 6 (Social) = 36 combinations
Full States: 36 × 7 (Objective Frames) = 252 total states

Example:
Personal: +? (Inquiring)
Social: < (Society denies)
Frame: Natural State (0)
→ State: "THE HERETIC" (seeking unknown truth against consensus)
```

### Hegemonic Vector Coordinates

**υ (Moral/Universal Scope):**
```
-1.0 = Maximum self-preservation (pure ego)
 0.0 = Balanced (neither selfish nor altruistic)
+1.0 = Maximum universal benefit (pure service)
```

**ψ (Will/Proactive Force):**
```
-1.0 = Maximum reactive (purely responsive)
 0.0 = Balanced (neither proactive nor reactive)
+1.0 = Maximum proactive (pure initiation)
```

**Quadrants:**
```
Upper-Left:  (+υ, +ψ) = The Builder/Creator
Upper-Right: (-υ, +ψ) = The Conqueror/Taker
Lower-Left:  (+υ, -ψ) = The Supporter/Helper
Lower-Right: (-υ, -ψ) = The Victim/Receiver
```

---

## HOUSE SYSTEM REFERENCE

### Natural House Meanings

| House | Sign | Plane | Theme                    | Life Area           |
|-------|------|-------|--------------------------|---------------------|
| 1     | Ari  | Q6    | Self                     | Identity, body      |
| 2     | Tau  | Q4    | Resources                | Money, values       |
| 3     | Gem  | Q5    | Communication            | Learning, siblings  |
| 4     | Can  | Q7    | Foundation               | Home, family        |
| 5     | Leo  | Q1    | Creativity               | Expression, joy     |
| 6     | Vir  | Q5    | Service                  | Work, health        |
| 7     | Lib  | Q3    | Partnership              | Relationships       |
| 8     | Sco  | Q7    | Transformation           | Shared resources    |
| 9     | Sag  | Q3    | Expansion                | Philosophy, travel  |
| 10    | Cap  | Q2    | Career                   | Public life         |
| 11    | Aqu  | Q2    | Community                | Groups, ideals      |
| 12    | Pis  | Q3    | Transcendence            | Spirituality        |

### House-to-c-Layer Mapping

**The 7 Uses (c-layer):**
```
c1 = Existence (being)
c2 = Placement (positioning)
c3 = Definition (naming)
c4 = Driving (motivating)
c5 = Calculation (planning)
c6 = Attribution (assigning)
c7 = Impact (affecting)
```

**House Assignments:**
```
c1 (Existence): House 1 (Ascendant)
c2 (Placement): Houses 2, 9
c3 (Definition): Houses 3, 10 (MC)
c4 (Driving): Houses 4 (IC), 11
c5 (Calculation): Houses 5, 12
c6 (Attribution): House 6
c7 (Impact): Houses 7 (Descendant), 8
```

---

## ELEMENT & MODALITY COMBINATIONS

### The Four Elements

| Element | Quality      | Signs              | Planets        |
|---------|--------------|--------------------|-----------------
| Fire    | Active       | Aries, Leo, Sag    | Sun, Mars      |
| Earth   | Stable       | Taurus, Virgo, Cap | Saturn, Venus  |
| Air     | Mental       | Gemini, Libra, Aqu | Mercury, Venus |
| Water   | Emotional    | Cancer, Scorp, Pis | Moon, Mars     |

### The Three Modalities

| Modality | Quality      | Signs              | Action          |
|----------|--------------|--------------------|-----------------
| Cardinal | Initiating   | Ari, Can, Lib, Cap | Starts          |
| Fixed    | Sustaining   | Tau, Leo, Sco, Aqu | Maintains       |
| Mutable  | Adapting     | Gem, Vir, Sag, Pis | Adjusts         |

### Sign Combinations

**Same Element:**
- Trine (120°) - Natural harmony
- Example: Leo-Sagittarius (both Fire)

**Compatible Elements:**
- Fire + Air = Stimulation
- Earth + Water = Nourishment

**Same Modality:**
- Square (90°) - Friction
- Example: Leo-Scorpio (both Fixed)

**Opposite Elements:**
- Fire/Water = Evaporation/Quenching
- Earth/Air = Grounding/Elevation

---

## SYMBOL REFERENCE

### Planetary Symbols
```
☉ - Sun
☽ - Moon
☿ - Mercury
♀ - Venus
♂ - Mars
♃ - Jupiter
♄ - Saturn
♅ - Uranus
♆ - Neptune
♇ - Pluto
```

### Zodiac Symbols
```
♈ - Aries
♉ - Taurus
♊ - Gemini
♋ - Cancer
♌ - Leo
♍ - Virgo
♎ - Libra
♏ - Scorpio
♐ - Sagittarius
♑ - Capricorn
♒ - Aquarius
♓ - Pisces
```

### Aspect Symbols
```
☌ - Conjunction (0°)
⚹ - Sextile (60°)
□ - Square (90°)
△ - Trine (120°)
⚺ - Quincunx (150°)
☍ - Opposition (180°)
```

---

## QUICK CALCULATION CHECKLIST

**For Each Chart:**
```
□ Birth data verified (date, time, location)
□ Planetary longitudes calculated
□ House cusps calculated (if birth time known)
□ Ascendant/MC calculated
□ Dignity scores assigned
□ Major aspects identified (with orbs)
□ Progressions calculated (Sun, Moon minimum)
□ Current transits calculated
□ Solar return calculated (if within year)
```

---

*End Reference Tables*
*Version 1.0*
*For use with Hegemonic Astrology generation package*
