# Class Definition: Corruption

**Purpose:** To formalize the identification of corruption by treating it as a structured object composed of validated sub-classes. This moves analysis from subjective opinion to objective, object-oriented pattern recognition.

Constructor: \`\`\`javascript

const currentCase = new Corruption(

new Agents(who),

new Action(what),

new Domain(where),

new Motive(why),

new Mechanism(how),

new SystemicFactor(cause),

new Outcome(effect),

new Timeline(when)

);

---
\### 1. The Sub-Classes (The Components)
\#### \*\*Class: \`Agents\` (Who)\*\*
\* \*\*Properties:\*\*
\* \`public_agent\` (String): The entity entrusted with power (e.g., "The Labor Government").
\* \`private_beneficiary\` (String): The entity receiving the extracted value (e.g., "Construction Consortiums").
\* \`relationship\` (String): The link between them (e.g., "Donor/Political Ally").
\* \*\*Method \`has_conflict()\`:\*\* Returns \`True\` if the \*public_agent\* acts in the interest of the \*private_beneficiary\* over the public.
\#### \*\*Class: \`Action\` (What)\*\*
\* \*\*Properties:\*\*
\* \`name\` (String): The specific policy or project (e.g., "Suburban Rail Loop").
\* \`scale\` (String): The magnitude of the act (e.g., "\$216 Billion").
\* \`type\` (String): The category of action (e.g., "Major Infrastructure Project").
\* \*\*Method \`is_deviation()\`:\*\* Returns \`True\` if the action deviates from standard operating procedure or expert advice.
\#### \*\*Class: \`Domain\` (Where)\*\*
\* \*\*Properties:\*\*
\* \`jurisdiction\` (String): The legal/political boundary (e.g., "Victoria, Australia").
\* \`resource_pool\` (String): The specific asset being drained (e.g., "State Budget / Transport Infrastructure").
\* \`impact_zone\` (String): The area affected (e.g., "Metropolitan Melbourne").
\#### \*\*Class: \`Motive\` (Why)\*\*
\* \*\*Properties:\*\*
\* \`currency\` (Enum): The type of value transferred \[\`Money\`, \`Power\`, \`Influence\`, \`Legacy\`\].
\* \`strategic_goal\` (String): The ultimate aim (e.g., "Secure electoral victory via 'Big Build' branding").
\* \*\*Method \`is_extractive()\`:\*\* Returns \`True\` if the motive prioritizes private/political gain over public utility.
\#### \*\*Class: \`Mechanism\` (How)\*\*
\* \*\*Properties:\*\*
\* \`tactic\` (String): The method of execution (e.g., "Secrecy", "Surprise Announcement").
\* \`bypassed_safeguards\` (List): The checks and balances ignored (e.g., \`\["Infrastructure Victoria", "Department of Transport"\]\`).
\* \*\*Method \`is_subversive()\`:\*\* Returns \`True\` if safeguards were intentionally disabled or ignored.
\#### \*\*Class: \`SystemicFactor\` (Cause)\*\*
\* \*\*Properties:\*\*
\* \`vulnerability\` (String): The flaw in the system (e.g., "Unchecked Executive Power / 'Captain's Call' culture").
\* \`incentive_structure\` (String): Why the system rewards the corruption (e.g., "Electoral reward for 'Ribbon Cutting' vs invisible maintenance").
\#### \*\*Class: \`Outcome\` (Effect)\*\*
\* \*\*Properties:\*\*
\* \`bcr\` (Float): Benefit-Cost Ratio (e.g., \`0.6\`).
\* \`public_loss\` (String): The quantifiable damage (e.g., "Net debt increase, Opportunity cost for Health").
\* \`private_gain\` (String): The quantifiable extraction (e.g., "Guaranteed construction profits").
\* \*\*Method \`destroys_value()\`:\*\* Returns \`True\` if \`bcr \< 1.0\`.
\#### \*\*Class: \`Timeline\` (When)\*\*
\* \*\*Properties:\*\*
\* \`inception_date\` (Date): When the plan was hatched (e.g., "Pre-2018 Election").
\* \`revelation_date\` (Date): When the true cost was revealed (e.g., "2022/2024").
\* \`status\` (Enum): \[\`Active\`, \`Paused\`, \`Complete\`\].
---
\### 2. The Main Class: \`Corruption\`
\*\*Logic:\*\*
The \`Corruption\` object is only valid if its constituent parts validate the extraction of public value for private/political gain.
\`\`\`javascript
class Corruption {
constructor(agents, action, domain, motive, mechanism, systemic, outcome, timeline) {
this.agents = agents;
this.action = action;
// ... assign other properties
}
function IsCorrupt() {
// 1. Is there a conflict of interest?
if (!this.agents.has_conflict()) return False;
// 2. Was the process subversive?
if (!this.mechanism.is_subversive()) return False;
// 3. Does it destroy public value?
if (!this.outcome.destroys_value()) return False;
// 4. Is the motive extractive?
if (!this.motive.is_extractive()) return False;
return True; // All gates passed. Definition met.
}
function GenerateIndictment() {
return \`This is an act of corruption.
AGENTS: \${this.agents.public_agent} acting for \${this.agents.private_beneficiary}.
MECHANISM: \${this.mechanism.tactic} used to bypass \${this.mechanism.bypassed_safeguards}.
OUTCOME: Value destruction confirmed (BCR: \${this.outcome.bcr}).
MOTIVE: Transfer of \${this.motive.currency} for \${this.motive.strategic_goal}.\`;
}
}

### 3. Instantiation: new Corruption(SRL)

**Data Injection:**

- **Agents:** Labor Govt -\> Construction Consortiums/Unions.

- **Mechanism:** "Captain's Call" bypassing Infrastructure Victoria.

- **Outcome:** BCR 0.6 (Value Destruction).

- **Motive:** Political Power & Corporate Profit.

**Result:** SRL.IsCorrupt() returns **TRUE**.
