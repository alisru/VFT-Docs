# SAMPLE CHART DATA STRUCTURE

This file provides the JSON schema for storing calculated natal chart data.

---

## COMPLETE NATAL CHART DATA (natal_chart.json)

```json
{
  "metadata": {
    "subject_name": "Alisru",
    "birth_date": "1993-07-28",
    "birth_time": "09:30:00",
    "birth_timezone": "Australia/Sydney",
    "birth_location": {
      "city": "Gosford",
      "state": "New South Wales",
      "country": "Australia",
      "latitude": -33.4250,
      "longitude": 151.3417
    },
    "birth_time_source": "birth_certificate",
    "calculation_date": "2026-02-11",
    "current_age": 32.5,
    "house_system": "Placidus"
  },
  
  "planetary_positions": {
    "sun": {
      "sign": "Leo",
      "degree": 5.23,
      "minutes": 14,
      "house": 9,
      "retrograde": false,
      "longitude": 125.23,
      "dignity": {
        "type": "domicile",
        "score": 5,
        "description": "Sun rules Leo - maximum strength"
      },
      "element": "fire",
      "modality": "fixed"
    },
    "moon": {
      "sign": "Scorpio",
      "degree": 8.47,
      "minutes": 28,
      "house": 1,
      "retrograde": false,
      "longitude": 218.47,
      "dignity": {
        "type": "fall",
        "score": -3,
        "description": "Moon uncomfortable in Scorpio"
      },
      "element": "water",
      "modality": "fixed"
    },
    "mercury": {
      "sign": "Cancer",
      "degree": 14.32,
      "minutes": 19,
      "house": 9,
      "retrograde": false,
      "longitude": 104.32,
      "dignity": {
        "type": "neutral",
        "score": 0,
        "description": "No essential dignity in Cancer"
      },
      "element": "water",
      "modality": "cardinal"
    },
    "venus": {
      "sign": "Gemini",
      "degree": 22.15,
      "minutes": 9,
      "house": 8,
      "retrograde": false,
      "longitude": 82.15,
      "dignity": {
        "type": "neutral",
        "score": 0,
        "description": "No essential dignity"
      },
      "element": "air",
      "modality": "mutable"
    },
    "mars": {
      "sign": "Virgo",
      "degree": 11.58,
      "minutes": 35,
      "house": 11,
      "retrograde": false,
      "longitude": 161.58,
      "dignity": {
        "type": "neutral",
        "score": 0,
        "description": "No essential dignity in Virgo"
      },
      "element": "earth",
      "modality": "mutable"
    },
    "jupiter": {
      "sign": "Libra",
      "degree": 18.42,
      "minutes": 51,
      "house": 11,
      "retrograde": false,
      "longitude": 198.42,
      "dignity": {
        "type": "neutral",
        "score": 0,
        "description": "No essential dignity in Libra"
      },
      "element": "air",
      "modality": "cardinal"
    },
    "saturn": {
      "sign": "Aquarius",
      "degree": 27.14,
      "minutes": 8,
      "house": 4,
      "retrograde": true,
      "longitude": 327.14,
      "dignity": {
        "type": "domicile",
        "score": 3,
        "description": "Saturn traditional ruler of Aquarius (shares with Uranus)"
      },
      "element": "air",
      "modality": "fixed"
    }
  },
  
  "angles": {
    "ascendant": {
      "sign": "Scorpio",
      "degree": 2.30,
      "longitude": 212.30
    },
    "midheaven": {
      "sign": "Leo",
      "degree": 18.45,
      "longitude": 138.45
    },
    "descendant": {
      "sign": "Taurus",
      "degree": 2.30,
      "longitude": 32.30
    },
    "ic": {
      "sign": "Aquarius",
      "degree": 18.45,
      "longitude": 318.45
    }
  },
  
  "house_cusps": [
    {"house": 1, "sign": "Scorpio", "degree": 2.30},
    {"house": 2, "sign": "Sagittarius", "degree": 8.15},
    {"house": 3, "sign": "Capricorn", "degree": 12.42},
    {"house": 4, "sign": "Aquarius", "degree": 18.45},
    {"house": 5, "sign": "Pisces", "degree": 24.18},
    {"house": 6, "sign": "Aries", "degree": 28.33},
    {"house": 7, "sign": "Taurus", "degree": 2.30},
    {"house": 8, "sign": "Gemini", "degree": 8.15},
    {"house": 9, "sign": "Cancer", "degree": 12.42},
    {"house": 10, "sign": "Leo", "degree": 18.45},
    {"house": 11, "sign": "Virgo", "degree": 24.18},
    {"house": 12, "sign": "Libra", "degree": 28.33}
  ],
  
  "major_aspects": [
    {
      "type": "square",
      "planet1": "sun",
      "planet2": "moon",
      "angle": 93.24,
      "orb": 3.24,
      "applying": false,
      "exact_date": "1993-07-27",
      "interpretation": "Identity (Q1) in friction with emotion (Q7)",
      "priority": 1,
      "i_layer": "i3"
    },
    {
      "type": "trine",
      "planet1": "mercury",
      "planet2": "moon",
      "angle": 114.15,
      "orb": 5.85,
      "applying": true,
      "exact_date": null,
      "interpretation": "Emotional logic flows with intense feeling",
      "priority": 2,
      "i_layer": "i2"
    },
    {
      "type": "trine",
      "planet1": "venus",
      "planet2": "jupiter",
      "angle": 116.27,
      "orb": 3.73,
      "applying": true,
      "exact_date": null,
      "interpretation": "Values expand through harmonic relationships",
      "priority": 3,
      "i_layer": "i2"
    }
  ],
  
  "q_structure": {
    "Q1": {
      "plane": "Meta-Physical",
      "interrogative": "WHO",
      "planet": "sun",
      "position": "Leo 5°",
      "house": 9,
      "dignity_score": 5,
      "filter": "q1",
      "coordinate": "Q1.q1",
      "interpretation": "Maximum identity strength, sovereign type"
    },
    "Q2": {
      "plane": "Physical",
      "interrogative": "WHERE",
      "planet": "saturn",
      "position": "Aquarius 27° Rx",
      "house": 4,
      "dignity_score": 3,
      "filter": "q2",
      "coordinate": "Q2.q2",
      "interpretation": "Intellectual boundaries, internal structures"
    },
    "Q3": {
      "plane": "Possible",
      "interrogative": "WHAT",
      "planet": "jupiter",
      "position": "Libra 18°",
      "house": 11,
      "dignity_score": 0,
      "filter": "q3",
      "coordinate": "Q3.q3",
      "interpretation": "Expansion through relationships, justice-oriented"
    },
    "Q4": {
      "plane": "Lyrical",
      "interrogative": "WHY",
      "planet": "venus",
      "position": "Gemini 22°",
      "house": 8,
      "dignity_score": 0,
      "filter": "q4",
      "coordinate": "Q4.q4",
      "interpretation": "Values variety, intellectual connection"
    },
    "Q5": {
      "plane": "Logical",
      "interrogative": "HOW",
      "planet": "mercury",
      "position": "Cancer 14°",
      "house": 9,
      "dignity_score": 0,
      "filter": "q5",
      "coordinate": "Q5.q5",
      "interpretation": "Emotional logic, gut-based processing"
    },
    "Q6": {
      "plane": "Historical",
      "interrogative": "CAUSE",
      "planet": "mars",
      "position": "Virgo 11°",
      "house": 11,
      "dignity_score": 0,
      "filter": "q6",
      "coordinate": "Q6.q6",
      "interpretation": "Precise action, service-oriented force"
    },
    "Q7": {
      "plane": "Emotive",
      "interrogative": "EFFECT",
      "planet": "moon",
      "position": "Scorpio 8°",
      "house": 1,
      "dignity_score": -3,
      "filter": "q7",
      "coordinate": "Q7.q7",
      "interpretation": "Intense emotion, transformative feeling"
    }
  }
}
```

---

## PROGRESSIONS DATA (progressions.json)

```json
{
  "metadata": {
    "subject_name": "Alisru",
    "natal_date": "1993-07-28",
    "current_age": 32.5,
    "progressed_date": "1993-08-29",
    "calculation_date": "2026-02-11"
  },
  
  "progressed_positions": {
    "sun": {
      "sign": "Virgo",
      "degree": 27.18,
      "house": 11,
      "natal_sign": "Leo",
      "progressed_into_current_sign": "1996-08-15",
      "will_progress_into_next_sign": "2026-08-20",
      "years_in_current_sign": 30,
      "interpretation": "Identity refined through service/perfection"
    },
    "moon": {
      "sign": "Aries",
      "degree": 10.32,
      "house": 5,
      "natal_sign": "Scorpio",
      "progressed_into_current_sign": "2025-09-12",
      "will_progress_into_next_sign": "2028-02-15",
      "months_in_current_sign": 5,
      "interpretation": "New emotional cycle, assertive feelings"
    },
    "ascendant": {
      "sign": "Sagittarius",
      "degree": 14.22,
      "natal_sign": "Scorpio",
      "progressed_into_current_sign": "2018-03-10",
      "interpretation": "Public persona expanding, more optimistic"
    }
  },
  
  "progressed_aspects": [
    {
      "type": "conjunction",
      "planet1": "progressed_sun",
      "planet2": "natal_saturn",
      "angle": 0.04,
      "orb": 0.04,
      "exact_date": "2020-08-15",
      "interpretation": "Identity meeting structure - maturity milestone"
    },
    {
      "type": "trine",
      "planet1": "progressed_moon",
      "planet2": "natal_sun",
      "angle": 119.91,
      "orb": 0.09,
      "exact_date": "2026-01-20",
      "interpretation": "Emotional state harmonizing with identity (recent)"
    }
  ],
  
  "major_progressed_events": {
    "past": [
      {
        "age": 3,
        "date": "1996-07-28",
        "event": "Progressed Sun entered Virgo",
        "significance": "Shift from pure sovereignty to refinement focus"
      },
      {
        "age": 29.5,
        "date": "2023-01-15",
        "event": "Progressed Moon returned to Scorpio",
        "significance": "Emotional death/rebirth cycle began"
      }
    ],
    "future": [
      {
        "age": 33,
        "date": "2026-08-20",
        "event": "Progressed Sun enters Libra",
        "significance": "Major identity shift toward relationships"
      },
      {
        "age": 39.5,
        "date": "2033-01-15",
        "event": "Progressed Moon returns to Scorpio again",
        "significance": "Second emotional transformation cycle"
      }
    ]
  },
  
  "moon_cycle_timeline": [
    {"age_range": "0-2.5", "sign": "Scorpio", "theme": "Intense infancy"},
    {"age_range": "2.5-5", "sign": "Sagittarius", "theme": "Adventurous toddler"},
    {"age_range": "5-7.5", "sign": "Capricorn", "theme": "Serious child"},
    {"age_range": "7.5-10", "sign": "Aquarius", "theme": "Unique pre-teen"},
    {"age_range": "10-12", "sign": "Pisces", "theme": "Dreamy early teen"},
    {"age_range": "12-14.5", "sign": "Aries", "theme": "Rebellious teen"},
    {"age_range": "14.5-17", "sign": "Taurus", "theme": "Stable late teen"},
    {"age_range": "17-19.5", "sign": "Gemini", "theme": "Social young adult"},
    {"age_range": "19.5-22", "sign": "Cancer", "theme": "Emotional maturation"},
    {"age_range": "22-24.5", "sign": "Leo", "theme": "Confident 20s"},
    {"age_range": "24.5-27", "sign": "Virgo", "theme": "Anxious late 20s"},
    {"age_range": "27-29.5", "sign": "Libra", "theme": "Relationship focus"},
    {"age_range": "29.5-32", "sign": "Scorpio", "theme": "Return - transformation"},
    {"age_range": "32-34.5", "sign": "Aries", "theme": "New emotional cycle"}
  ]
}
```

---

## TRANSITS DATA (transits.json)

```json
{
  "metadata": {
    "subject_name": "Alisru",
    "analysis_date": "2026-02-11",
    "current_age": 32.5
  },
  
  "current_transits": {
    "sun": {
      "position": "Aquarius 22.30°",
      "aspects_to_natal": [
        {
          "natal_planet": "saturn",
          "aspect": "conjunction",
          "orb": 4.84,
          "interpretation": "Illuminating structures and limits"
        },
        {
          "natal_planet": "sun",
          "aspect": "opposition",
          "orb": 7.07,
          "interpretation": "Opposition point - 6 months from birthday"
        }
      ]
    },
    "moon": {
      "position": "Scorpio 15.20°",
      "aspects_to_natal": [
        {
          "natal_planet": "moon",
          "aspect": "conjunction",
          "orb": 6.73,
          "interpretation": "Monthly lunar return - emotional activation"
        }
      ]
    },
    "jupiter": {
      "position": "Cancer 8.15°",
      "house": 9,
      "aspects_to_natal": [
        {
          "natal_planet": "mercury",
          "aspect": "conjunction",
          "orb": 6.17,
          "interpretation": "Expanding mental processes and communication"
        },
        {
          "natal_planet": "jupiter",
          "aspect": "square",
          "orb": 10.27,
          "interpretation": "Jupiter waxing square - growth challenge"
        }
      ]
    },
    "saturn": {
      "position": "Pisces 15.42°",
      "house": 5,
      "aspects_to_natal": [
        {
          "natal_planet": "saturn",
          "aspect": "sextile",
          "orb": 11.72,
          "interpretation": "Post-return stabilization phase"
        }
      ]
    }
  },
  
  "major_upcoming_transits": [
    {
      "date_range": "2026-06-15 to 2026-08-20",
      "transit": "Jupiter conjunct natal Sun",
      "description": "Major expansion of identity and creative power",
      "priority": "CRITICAL",
      "preparation": "Set intentions for growth, be ready for opportunities"
    },
    {
      "date_range": "2026-08-20 to 2027-02-15",
      "transit": "Jupiter in Leo (Sun's sign)",
      "description": "Extended period of confidence and visibility",
      "priority": "HIGH",
      "preparation": "Leverage increased optimism for major projects"
    },
    {
      "date_range": "2027-05-10 to 2027-07-20",
      "transit": "Saturn enters Aries",
      "description": "New structural cycle begins",
      "priority": "MEDIUM",
      "preparation": "Review structures built since Saturn return"
    },
    {
      "date_range": "2028-10-15 to 2029-06-30",
      "transit": "Jupiter return to Libra",
      "description": "Third Jupiter return - expansion cycle completes",
      "priority": "HIGH",
      "preparation": "Major relationship or partnership milestone likely"
    }
  ],
  
  "major_return_cycles": {
    "completed": [
      {
        "cycle": "Saturn Return (1st)",
        "date_range": "2021-12-15 to 2023-03-20",
        "age": "28-30",
        "status": "COMPLETED",
        "theme": "Reality check, structural maturity"
      },
      {
        "cycle": "Jupiter Return (2nd)",
        "date": "2016-09-15",
        "age": 23,
        "status": "COMPLETED",
        "theme": "Expansion phase 2"
      }
    ],
    "upcoming": [
      {
        "cycle": "Jupiter Return (3rd)",
        "date": "2028-11-20",
        "age": 35,
        "status": "FUTURE",
        "theme": "Relationship-based expansion"
      },
      {
        "cycle": "Saturn Return (2nd)",
        "date_range": "2052-01-10 to 2053-06-15",
        "age": "58-60",
        "status": "FUTURE",
        "theme": "Life's work manifestation"
      }
    ]
  }
}
```

---

## PULSE PROTOCOL DATA (pulse_state.json)

```json
{
  "metadata": {
    "subject_name": "Alisru",
    "analysis_date": "2026-02-11"
  },
  
  "A0": {
    "personal_will": "+?",
    "social_will": "<",
    "objective_frame": "natural_state",
    "belief_state": "THE_HERETIC",
    "hegemonic_vector": {
      "upsilon": 0.3,
      "psi": 0.6
    },
    "archetype": "Seeking truth that society rejects",
    "quadrant": "upper_left"
  },
  
  "A1": {
    "logic_status": "CLEAN",
    "independence": true,
    "non_circular": true,
    "falsifiable": true
  },
  
  "A2": {
    "personal_will": "=",
    "social_will": "<",
    "objective_frame": "bad_truth",
    "belief_state": "THE_CASSANDRA",
    "hegemonic_vector": {
      "upsilon": 0.5,
      "psi": 0.7
    },
    "delta": "LARGE",
    "primary_discovery": "Sun square Moon - internal war",
    "secondary_discoveries": [
      "Mercury in Cancer - emotional logic",
      "Jupiter in Libra - relationship-dependent expansion",
      "Moon in Scorpio - life-or-death intensity"
    ]
  },
  
  "A_final": {
    "personal_will": "=",
    "social_will": "<",
    "objective_frame": "good_truth",
    "belief_state": "THE_PROPHET",
    "hegemonic_vector": {
      "upsilon": 0.7,
      "psi": 0.9
    },
    "archetype": "Teaching verified truth against consensus",
    "quadrant": "upper_left"
  },
  
  "transformation_metrics": {
    "certainty_gain": 45,
    "upsilon_change": 0.4,
    "upsilon_percent_change": 133,
    "psi_change": 0.3,
    "psi_percent_change": 50,
    "reality_frame_shift": "natural_state_to_good_truth",
    "archetype_evolution": "heretic_to_prophet"
  }
}
```

---

## USAGE NOTES

**These JSON files can be used to:**

1. Store calculated data for programmatic access
2. Generate charts from templates automatically
3. Track changes over time (version each reading)
4. Build databases of charts for research
5. Create web applications that visualize the data
6. Export/import between different analysis tools

**File Organization:**
```
/charts/
  /subject_name/
    /2026-02-11/  (analysis date)
      natal_chart.json
      progressions.json
      transits.json
      pulse_state.json
      [generated markdown documents]
```

---

*End Sample Data Structures*
