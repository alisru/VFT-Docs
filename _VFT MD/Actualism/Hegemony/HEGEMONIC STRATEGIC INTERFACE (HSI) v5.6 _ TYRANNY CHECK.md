import React, { useState, useMemo } from 'react';

import {

Target, Plus, Info, Brain, Sparkles, Loader2, FlaskConical, X,

ChevronRight, ChevronDown, RefreshCw, Zap, Microscope, History,

Link2, Globe, Layers, Search, AlertTriangle, Scale, Settings,

ArrowLeft, ArrowRight, Server, Cloud, Radio, PlayCircle, StopCircle, Compass

} from 'lucide-react';

/\*\*

\* HEGEMONIC STRATEGIC INTERFACE (HSI) v5.6 // TYRANNY CHECK

\* \* Topology: The Structural Matrix (Objective vs Subjective).

\* \* Features:

\* - Infinite Timeline & Recursive Nesting.

\* - 7-Vector Fractal Judgement.

\* - Live Plotting of Judgement Vectors on Graph.

\* - Multi-Provider Support.

\* \* Update: STRICT MORAL DEFINITIONS to prevent "Tyrant's Delusion" errors.

\*/

// --- TYPES ---

type VectorNode = {

id: string;

label: string;

description: string;

details?: string;

u: number;

p: number;

importance: number;

feasibility: number;

subSteps?: VectorNode\[\];

};

type AnalysisScenario = {

goal: string;

steps: VectorNode\[\];

};

type AnchorNode = {

u: number;

p: number;

label: string;

subLabel: string;

type: 'objective' \| 'subjective';

color: string;

};

type JudgementEntry = {

questionId: string;

questionText: string;

answer: string;

u?: number; // Moral Coordinate

p?: number; // Will Coordinate

sources?: { title: string; uri: string }\[\];

};

type AiProvider = 'google' \| 'ollama' \| 'perplexity';

// --- DATA: FRACTAL VECTORS (THE KANON) ---

const FRACTAL_VECTORS = \[

{ id: 'WHO', label: 'WHO', question: 'Who is the agent? Who benefits? Who loses?', color: 'text-pink-400 border-pink-900/50 hover:bg-pink-900/30' },

{ id: 'what', label: 'WHAT', question: 'What is the definition? What is the substance?', color: 'text-yellow-400 border-yellow-900/50 hover:bg-yellow-900/30' },

{ id: 'WHERE', label: 'WHERE', question: 'Where does this exist? What is the context/territory?', color: 'text-orange-400 border-orange-900/50 hover:bg-orange-900/30' },

{ id: 'WHY', label: 'WHY', question: 'Why is this driven? What is the core purpose/intent?', color: 'text-emerald-400 border-emerald-900/50 hover:bg-emerald-900/30' },

{ id: 'HOW', label: 'HOW', question: 'How is this executed? What is the method/mechanism?', color: 'text-cyan-400 border-cyan-900/50 hover:bg-cyan-900/30' },

{ id: 'CAUSE', label: 'CAUSE', question: 'What caused this? What are the historical precursors?', color: 'text-indigo-400 border-indigo-900/50 hover:bg-indigo-900/30' },

{ id: 'EFFECT', label: 'EFFECT', question: 'What is the effect? What are the 2nd/3rd order consequences?', color: 'text-purple-400 border-purple-900/50 hover:bg-purple-900/30' },

\];

// --- DATA: STRUCTURAL ANCHORS ---

const STRUCTURAL_NODES: AnchorNode\[\] = \[

{ u: 1.0, p: 1.0, label: "GREATER GOOD", subLabel: "(Objective)", type: 'objective', color: '#10b981' },

{ u: -1.0, p: 1.0, label: "GREATEST LIE", subLabel: "(Objective)", type: 'objective', color: '#f59e0b' },

{ u: 1.0, p: -1.0, label: "LESSER GOOD", subLabel: "(Objective)", type: 'objective', color: '#0ea5e9' },

{ u: -1.0, p: -1.0, label: "GREATER EVIL", subLabel: "(Objective)", type: 'objective', color: '#ef4444' },

{ u: 0.5, p: 0.5, label: "NAIVETY", subLabel: "(P-Lesser Evil)", type: 'subjective', color: '#34d399' },

{ u: -0.5, p: 0.5, label: "AMBITION", subLabel: "(P-Greater Good)", type: 'subjective', color: '#fbbf24' },

{ u: 0.5, p: -0.5, label: "THE ROT", subLabel: "(P-Greater Evil)", type: 'subjective', color: '#38bdf8' },

{ u: -0.5, p: -0.5, label: "THE SHIELD", subLabel: "(P-Lesser Good)", type: 'subjective', color: '#f87171' },

\];

// --- HELPER FUNCTIONS ---

const flattenNodes = (nodes: VectorNode\[\]): VectorNode\[\] =\> {

let flat: VectorNode\[\] = \[\];

nodes.forEach(node =\> {

flat.push(node);

if (node.subSteps && node.subSteps.length \> 0) {

flat = flat.concat(flattenNodes(node.subSteps));

}

});

return flat;

};

const addChildrenToNode = (nodes: VectorNode\[\], targetId: string, newChildren: VectorNode\[\]): VectorNode\[\] =\> {

return nodes.map(node =\> {

if (node.id === targetId) {

return { ...node, subSteps: \[...(node.subSteps \|\| \[\]), ...newChildren\] };

}

if (node.subSteps) {

return { ...node, subSteps: addChildrenToNode(node.subSteps, targetId, newChildren) };

}

return node;

});

};

const findNodeById = (nodes: VectorNode\[\], id: string): VectorNode \| undefined =\> {

for (const node of nodes) {

if (node.id === id) return node;

if (node.subSteps) {

const found = findNodeById(node.subSteps, id);

if (found) return found;

}

}

return undefined;

};

// --- COMPONENTS ---

const CoordinateGrid = ({

steps,

hoveredStep,

setHoveredStep

}: {

steps: VectorNode\[\],

hoveredStep: string \| null,

setHoveredStep: (id: string \| null) =\> void

}) =\> {

const allNodes = useMemo(() =\> flattenNodes(steps), \[steps\]);

const mapX = (u: number) =\> ((2 - u) / 4) \* 100;

const mapY = (p: number) =\> ((2 - p) / 4) \* 100;

const pathData = useMemo(() =\> {

if (steps.length === 0) return "";

let d = \`M 50 50\`;

steps.forEach(step =\> {

d += \` L \${mapX(step.u)} \${mapY(step.p)}\`;

});

return d;

}, \[steps\]);

const renderAnchor = (node: AnchorNode) =\> {

const x = mapX(node.u);

const y = mapY(node.p);

const isObj = node.type === 'objective';

return (

\<g key={\`\${node.label}\`}\>

\<line x1="50" y1="50" x2={x} y2={y} stroke={node.color} strokeWidth="0.1" opacity="0.1" strokeDasharray="1 1" /\>

\<circle cx={x} cy={y} r={isObj ? 1.2 : 0.8} fill="none" stroke={node.color} strokeWidth="0.2" opacity="0.8" /\>

{isObj && \<circle cx={x} cy={y} r={0.4} fill={node.color} opacity="0.6" /\>}

\<text

x={x} y={y - (isObj ? 2.5 : 2)}

textAnchor="middle"

className={\`text-\[2px\] font-bold tracking-widest \${isObj ? 'font-mono uppercase' : 'font-sans'} fill-slate-200 pointer-events-none select-none\`}

style={{ textShadow: \`0 0 2px \${node.color}40\` }}

\>

{node.label}

\</text\>

\<text

x={x} y={y + (isObj ? 3 : 2.5)}

textAnchor="middle"

className="text-\[1.2px\] fill-slate-500 font-mono pointer-events-none select-none"

\>

{node.subLabel}

\</text\>

\</g\>

);

};

return (

\<div className="relative w-full aspect-square bg-slate-950 rounded-lg overflow-hidden border border-slate-800 shadow-2xl"\>

\<svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 100 100" preserveAspectRatio="none"\>

\<line x1="50" y1="0" x2="50" y2="100" stroke="#475569" strokeWidth="0.2" opacity="0.5" /\>

\<line x1="0" y1="50" x2="100" y2="50" stroke="#475569" strokeWidth="0.2" opacity="0.5" /\>

\<rect x="25" y="25" width="50" height="50" fill="none" stroke="#64748b" strokeWidth="0.2" opacity="0.3" rx="1" /\>

\<text x="26" y="24" className="text-\[1.5px\] fill-slate-600 font-mono tracking-widest"\>OBJECTIVE HORIZON (±1.0)\</text\>

\<rect x="37.5" y="37.5" width="25" height="25" fill="none" stroke="#64748b" strokeWidth="0.2" strokeDasharray="1 1" opacity="0.2" rx="0.5" /\>

\<text x="38" y="36.5" className="text-\[1.2px\] fill-slate-700 font-mono tracking-widest"\>PERCEPTUAL HORIZON (±0.5)\</text\>

{STRUCTURAL_NODES.map(renderAnchor)}

{/\* Draw path if nodes exist \*/}

{allNodes.length \> 0 && (

\<path d={pathData} fill="none" stroke="#94a3b8" strokeWidth="0.4" strokeDasharray="2 1" className="opacity-90"/\>

)}

{allNodes.map((step) =\> (

\<line

key={\`line-\${step.id}\`}

x1="50" y1="50"

x2={mapX(step.u)}

y2={mapY(step.p)}

stroke={hoveredStep === step.id ? "#ffffff" : "#475569"}

strokeWidth={hoveredStep === step.id ? "0.3" : "0.1"}

opacity="0.2"

/\>

))}

\</svg\>

\<div className="absolute top-1 left-1/2 -translate-x-1/2 text-\[3px\] text-emerald-500 font-mono font-bold"\>+2Ψ (SYNTHESIZED)\</div\>

\<div className="absolute bottom-1 left-1/2 -translate-x-1/2 text-\[3px\] text-red-500 font-mono font-bold"\>-2Ψ (THEOLOGICAL)\</div\>

\<div className="absolute left-1 top-1/2 -translate-y-1/2 text-\[3px\] text-emerald-500 font-mono font-bold vertical-rl"\>+2Υ (VIRTUE)\</div\>

\<div className="absolute right-1 top-1/2 -translate-y-1/2 text-\[3px\] text-red-500 font-mono font-bold vertical-rl"\>-2Υ (VICE)\</div\>

{allNodes.map((step, index) =\> {

const x = mapX(step.u);

const y = mapY(step.p);

const isHovered = hoveredStep === step.id;

const baseSize = allNodes.length \> 20 ? 3 : 5;

const size = baseSize + (step.importance \* (allNodes.length \> 20 ? 6 : 10));

return (

\<div

key={step.id}

className="absolute rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 transform -translate-x-1/2 -translate-y-1/2 group"

style={{

left: \`\${x}%\`,

top: \`\${y}%\`,

width: \`\${size}px\`,

height: \`\${size}px\`,

opacity: isHovered ? 1 : Math.max(0.4, step.feasibility),

backgroundColor: step.u \> 0 ? (step.p \> 0 ? '#10b981' : '#0ea5e9') : (step.p \> 0 ? '#f59e0b' : '#ef4444'),

zIndex: isHovered ? 30 : 20,

border: isHovered ? '2px solid white' : '1px solid rgba(255,255,255,0.2)'

}}

onMouseEnter={() =\> setHoveredStep(step.id)}

onMouseLeave={() =\> setHoveredStep(null)}

\>

{isHovered && (

\<div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-black/80 px-2 py-1 rounded text-\[8px\] text-white whitespace-nowrap z-50 border border-slate-700 pointer-events-none shadow-xl"\>

\<span className="font-bold text-emerald-400"\>{step.label}\</span\>

\<span className="block text-\[6px\] text-slate-400 font-mono"\>\[{step.u.toFixed(2)}, {step.p.toFixed(2)}\]\</span\>

\</div\>

)}

{index === allNodes.length - 1 && (

\<div className="absolute inset-0 rounded-full animate-ping opacity-20 bg-white"\>\</div\>

)}

\</div\>

);

})}

\</div\>

);

};

const SidebarNode = ({

step, idxString, level, hoveredStep, setHoveredStep, removeStep,

handleFractalAnalysis, handleSetReference, isLoading

}: {

step: VectorNode, idxString: string, level: number, hoveredStep: string \| null,

setHoveredStep: (id: string \| null) =\> void, removeStep: (id: string) =\> void,

handleFractalAnalysis: (node: VectorNode, vector: string, question: string) =\> void,

handleSetReference: (node: VectorNode) =\> void, isLoading: boolean

}) =\> {

const \[isExpanded, setIsExpanded\] = useState(false);

const hasChildren = step.subSteps && step.subSteps.length \> 0;

return (

\<div className={\`mb-2 rounded border transition-all relative overflow-hidden group \${isExpanded ? 'bg-slate-800/80 border-slate-600' : 'bg-black/40 border-slate-800/50 hover:border-slate-700'}\`}\>

\<div

className="p-3 flex justify-between items-center cursor-pointer"

onClick={() =\> setIsExpanded(!isExpanded)}

onMouseEnter={() =\> setHoveredStep(step.id)}

onMouseLeave={() =\> setHoveredStep(null)}

\>

\<div className="flex items-center gap-3"\>

\<div className={\`p-1 rounded-full \${step.u \> 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}\`}\>

{hasChildren ? (isExpanded ? \<ChevronDown className="w-3 h-3" /\> : \<ChevronRight className="w-3 h-3" /\>) : \<div className="w-3 h-3" /\>}

\</div\>

\<div\>

\<div className="text-\[10px\] font-mono text-slate-500 flex gap-2"\>

\<span\>STEP {idxString}\</span\>

\<span className="text-slate-600"\>\[{step.u.toFixed(2)}, {step.p.toFixed(2)}\]\</span\>

\</div\>

\<h3 className={\`text-sm font-bold \${step.u \> 0 ? 'text-emerald-400' : 'text-amber-400'}\`}\>{step.label}\</h3\>

\</div\>

\</div\>

\<div className="flex items-center gap-1"\>

\<button onClick={(e) =\> { e.stopPropagation(); handleSetReference(step); }} className="text-slate-600 hover:text-purple-400 p-2 opacity-50 hover:opacity-100" title="Refer To This Step"\>\<Link2 className="w-3 h-3" /\>\</button\>

{level === 0 && (

\<button onClick={(e) =\> { e.stopPropagation(); removeStep(step.id); }} className="text-slate-600 hover:text-red-400 p-2 opacity-50 hover:opacity-100"\>\<X className="w-3 h-3" /\>\</button\>

)}

\</div\>

\</div\>

{isExpanded && (

\<div className="px-3 pb-3 pt-0 animate-in slide-in-from-top-2"\>

\<div className="pl-9 space-y-3"\>

\<p className="text-xs text-slate-300 leading-relaxed border-l-2 border-slate-700 pl-2"\>{step.description}\</p\>

{step.details && \<p className="text-xs text-slate-400 italic"\>"{String(step.details)}"\</p\>}

\<div className="pt-2 border-t border-slate-700/50 mt-2"\>

\<h4 className="text-\[8px\] uppercase tracking-widest text-slate-500 mb-2 flex items-center gap-2"\>\<Layers className="w-3 h-3" /\> Fractal Ratio Protocol\</h4\>

\<div className="grid grid-cols-4 gap-1"\>

{FRACTAL_VECTORS.map((vec) =\> (

\<button

key={vec.id}

onClick={(e) =\> { e.stopPropagation(); handleFractalAnalysis(step, vec.label, vec.question); setIsExpanded(true); }}

disabled={isLoading}

className={\`rounded py-1 px-1 text-\[9px\] font-bold border flex items-center justify-center transition-colors \${vec.color}\`}

title={vec.question}

\>

{vec.label}

\</button\>

))}

\</div\>

\</div\>

{hasChildren && (

\<div className="mt-4 border-l border-slate-800 pl-2"\>

\<h4 className="text-\[9px\] uppercase tracking-widest text-slate-500 mb-2 pl-2"\>Sub-Vectors\</h4\>

{step.subSteps!.map((child, i) =\> (

\<SidebarNode

key={child.id} step={child} idxString={\`\${idxString}.\${i+1}\`} level={level + 1}

hoveredStep={hoveredStep} setHoveredStep={setHoveredStep} removeStep={removeStep}

handleFractalAnalysis={handleFractalAnalysis} handleSetReference={handleSetReference} isLoading={isLoading}

/\>

))}

\</div\>

)}

\</div\>

\</div\>

)}

\</div\>

);

};

// --- MAIN APP ---

export default function App() {

// State

const \[timeline, setTimeline\] = useState\<VectorNode\[\]\>(\[\]);

const \[goalInput, setGoalInput\] = useState('');

const \[globalContext, setGlobalContext\] = useState('');

const \[hoveredStep, setHoveredStep\] = useState\<string \| null\>(null);

const \[mode, setMode\] = useState\<'timeline' \| 'manual' \| 'judgement'\>('timeline');

const \[activeRefId, setActiveRefId\] = useState\<string \| null\>(null);

const \[useSearch, setUseSearch\] = useState(false);

const \[isSettingsOpen, setIsSettingsOpen\] = useState(false);

const \[judgeEvent, setJudgeEvent\] = useState('');

const \[judgeIdx, setJudgeIdx\] = useState(0);

const \[judgeLog, setJudgeLog\] = useState\<JudgementEntry\[\]\>(\[\]);

const \[isAutoScanning, setIsAutoScanning\] = useState(false);

const \[isLoading, setIsLoading\] = useState(false);

const \[aiError, setAiError\] = useState\<string \| null\>(null);

// Settings / Providers

const \[aiProvider, setAiProvider\] = useState\<AiProvider\>('google');

const \[userApiKey, setUserApiKey\] = useState('');

const \[googleModel, setGoogleModel\] = useState('gemini-2.5-flash-preview-09-2025');

const \[ollamaBaseUrl, setOllamaBaseUrl\] = useState('http://localhost:11434');

const \[ollamaModel, setOllamaModel\] = useState('llama3');

const \[perplexityModel, setPerplexityModel\] = useState('sonar-pro');

const envApiKey = "";

// Manual Input

const \[newStepLabel, setNewStepLabel\] = useState('');

const \[newStepU, setNewStepU\] = useState(0);

const \[newStepP, setNewStepP\] = useState(0);

const activeReference = useMemo(() =\> {

if (!activeRefId) return null;

return findNodeById(timeline, activeRefId);

}, \[timeline, activeRefId\]);

// Actions

const handleClear = () =\> {

setTimeline(\[\]);

setGlobalContext('');

setGoalInput('');

setActiveRefId(null);

setJudgeLog(\[\]);

setIsAutoScanning(false);

};

const removeStep = (id: string) =\> setTimeline(prev =\> prev.filter(s =\> s.id !== id));

const handleSetReference = (node: VectorNode) =\> setActiveRefId(node.id);

const handleManualAdd = () =\> {

if (!newStepLabel) return;

const newStep: VectorNode = {

id: \`m-\${Date.now()}\`,

label: newStepLabel,

description: 'User defined vector.',

u: newStepU,

p: newStepP,

importance: 0.5,

feasibility: 0.5,

subSteps: \[\]

};

setTimeline(prev =\> \[...prev, newStep\]);

setNewStepLabel('');

setNewStepU(0);

setNewStepP(0);

};

// --- DYNAMIC GRAPH DATA ---

const plotData = useMemo(() =\> {

if (mode === 'judgement') {

// Map Judgement Log to Plottable Nodes

return judgeLog

.filter(j =\> j.u !== undefined && j.p !== undefined)

.map(j =\> ({

id: j.questionId,

label: j.questionId, // e.g. "WHO", "WHY"

description: j.answer,

u: j.u!,

p: j.p!,

importance: 0.7,

feasibility: 1.0,

subSteps: \[\]

} as VectorNode));

}

// Default to Timeline

return timeline;

}, \[mode, timeline, judgeLog\]);

// --- UNIVERSAL API HANDLER ---

const callAIProvider = async (payload: any) =\> {

// 1. GOOGLE GEMINI

if (aiProvider === 'google') {

const effectiveKey = userApiKey \|\| envApiKey;

const url = \`https://generativelanguage.googleapis.com/v1beta/models/\${googleModel}:generateContent?key=\${effectiveKey}\`;

const options = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) };

for (let i = 0; i \< 2; i++) {

try {

const response = await fetch(url, options);

if (!response.ok) {

if (response.status === 400 && useSearch) throw new Error("SEARCH_BLOCKED");

throw new Error(\`HTTP \${response.status}\`);

}

const data = await response.json();

return { text: data.candidates?.\[0\]?.content?.parts?.\[0\]?.text, raw: data };

} catch (err: any) {

if (err.message === "SEARCH_BLOCKED") throw err; // Don't retry logic error

await new Promise(res =\> setTimeout(res, 1000));

}

}

throw new Error("Google API Failed.");

}

// 2. OLLAMA

else if (aiProvider === 'ollama') {

const promptText = payload.contents?.\[0\]?.parts?.\[0\]?.text;

if (!promptText) throw new Error("Invalid Prompt");

try {

const response = await fetch(\`\${ollamaBaseUrl}/api/generate\`, {

method: 'POST',

headers: { 'Content-Type': 'application/json' },

body: JSON.stringify({ model: ollamaModel, prompt: promptText, stream: false, format: "json" })

});

if (!response.ok) throw new Error(\`Ollama Error: \${response.statusText}\`);

const data = await response.json();

return { text: data.response, raw: data };

} catch (err: any) {

throw new Error(\`Ollama Failed. Check URL & Origins.\`);

}

}

// 3. PERPLEXITY

else if (aiProvider === 'perplexity') {

const promptText = payload.contents?.\[0\]?.parts?.\[0\]?.text;

try {

const response = await fetch('https://api.perplexity.ai/chat/completions', {

method: 'POST',

headers: { 'Content-Type': 'application/json', 'Authorization': \`Bearer \${userApiKey}\` },

body: JSON.stringify({

model: perplexityModel,

messages: \[{ role: "system", content: "Output strictly JSON." }, { role: "user", content: promptText }\]

})

});

if (!response.ok) throw new Error("Perplexity API Error");

const data = await response.json();

return { text: data.choices\[0\].message.content, raw: data };

} catch (err: any) {

throw new Error(\`Perplexity Failed: \${err.message}\`);

}

}

throw new Error("Unknown Provider");

};

// --- CORE ANALYTICS ---

const handleGeminiAnalysis = async (customContext?: string, customInstruction?: string, forceParentId?: string) =\> {

const inputToUse = customContext ? "" : goalInput;

if (!customContext && !inputToUse.trim()) return;

setIsLoading(true);

setAiError(null);

const parentId = forceParentId \|\| activeRefId;

const parentNode = parentId ? findNodeById(timeline, parentId) : null;

const contextLines = \[\];

if (globalContext) contextLines.push(\`GLOBAL OVERARCHING GOAL: "\${globalContext}"\`);

if (parentNode) contextLines.push(\`FOCUS CONTEXT: "\${parentNode.label}" - \${parentNode.description}\`);

else if (timeline.length \> 0) contextLines.push(\`EXISTING TRAJECTORY:\\n\${timeline.map(s =\> \`"\${s.label}"\`).join(', ')}\`);

const task = customInstruction \|\| (parentNode

? \`USER INPUT: "\${inputToUse}". TASK: Generate 2-3 SUB-STEPS nested in "\${parentNode.label}". Explain simply.\`

: \`USER INPUT: "\${inputToUse}". TASK: Generate 3-5 major steps based on Global Goal. Explain simply.\`);

const prompt = \`

IDENTITY: Alethekanon.

CORE DIRECTIVE: You must strictly adhere to the Psochic Hegemony definitions.

\- MORAL AXIS (+U): Universal Benefit, Freedom, Autonomy. (Positive)

\- MORAL AXIS (-U): Self/Group Benefit, Control, Tyranny, Slavery. (Negative)

\- WILL AXIS (+P): Proactive, Building, Creating. (Positive)

\- WILL AXIS (-P): Suppressive, Destroying, Preventing. (Negative)

WARNING: Do NOT confuse "Order" or "Efficiency" with "Good". If a step involves control, centralization, or removing choice, it is NEGATIVE MORALITY (-U), even if it creates "Peace".

CONTEXT:\\n\${contextLines.join('\\n')}\\nCOMMAND: \${task}

OUTPUT JSON: { "steps": \[ { "id": "...", "label": "...", "description": "...", "details": "...", "u": float, "p": float, "importance": float, "feasibility": float } \] }

\`;

const payload: any = { contents: \[{ parts: \[{ text: prompt }\] }\], generationConfig: { responseMimeType: "application/json" } };

if (useSearch && aiProvider === 'google') payload.tools = \[{ google_search: {} }\];

try {

const { text } = await callAIProvider(payload);

const cleaned = text.replace(/\`\`\`json/g, '').replace(/\`\`\`/g, '').trim();

if (cleaned) {

const result = JSON.parse(cleaned);

const newSteps = result.steps.map((s: any, i: number) =\> ({ ...s, id: \`ai-\${Date.now()}-\${i}\`, subSteps: \[\] }));

parentId ? setTimeline(prev =\> addChildrenToNode(prev, parentId, newSteps)) : setTimeline(prev =\> \[...prev, ...newSteps\]);

}

} catch (err: any) {

// FAILOVER LOGIC

if (err.message === "SEARCH_BLOCKED" && useSearch) {

setAiError("Search blocked by environment. Falling back to Logic Core...");

const fallbackPayload = { ...payload };

delete fallbackPayload.tools; // Remove tool

try {

const { text } = await callAIProvider(fallbackPayload);

const cleaned = text.replace(/\`\`\`json/g, '').replace(/\`\`\`/g, '').trim();

const result = JSON.parse(cleaned);

const newSteps = result.steps.map((s: any, i: number) =\> ({ ...s, id: \`ai-\${Date.now()}-\${i}\`, subSteps: \[\] }));

parentId ? setTimeline(prev =\> addChildrenToNode(prev, parentId, newSteps)) : setTimeline(prev =\> \[...prev, ...newSteps\]);

setAiError(null);

} catch (retryErr) {

setAiError("Fallback failed. System Offline.");

}

} else {

setAiError(err.message \|\| "Connection Failed");

}

} finally {

setIsLoading(false);

if (!customContext) setGoalInput('');

}

};

// --- DYNAMIC PRESET LOADER (Calculated Live) ---

const handleQuickPreset = (type: 'empire' \| 'peace') =\> {

// Clear legacy hardcoded state

setTimeline(\[\]);

const goal = type === 'empire' ? "Build a Tech Empire" : "Achieve Community Peace";

setGlobalContext(goal);

const prompt = \`Generate a rigorous, 4-step strategic plan for: "\${goal}". Calculate precise Moral(U) and Will(P) coordinates for each step based on the Alethekanon Framework.\`;

handleGeminiAnalysis(undefined, prompt);

};

// --- AUTO JUDGEMENT (7 VECTORS) ---

const handleAutoScan = async () =\> {

if (!judgeEvent.trim()) return;

setIsAutoScanning(true);

setIsLoading(true);

setAiError(null);

const prompt = \`

IDENTITY: Alethekanon Fractal Judgement.

TARGET EVENT: "\${judgeEvent}"

CONTEXT: "\${globalContext}"

VECTORS: Who, What, Where, Why, How, Cause, Effect.

INSTRUCTION: Provide structured answers for these 7 vectors. Be concise and objective.

CRITICAL VECTOR CALCULATION:

\- Moral (u): Does this increase Freedom (+2) or Control (-2)?

\- Will (p): Is this Creative (+2) or Suppressive (-2)?

OUTPUT JSON:

{

"results": \[

{ "vector": "WHO", "answer": "...", "u": 0.0, "p": 0.0 },

{ "vector": "WHAT", "answer": "...", "u": 0.0, "p": 0.0 },

... for all 7 vectors

\]

}

\`;

const payload: any = { contents: \[{ parts: \[{ text: prompt }\] }\], generationConfig: { responseMimeType: "application/json" } };

if (useSearch && aiProvider === 'google') payload.tools = \[{ google_search: {} }\];

try {

const { text, raw } = await callAIProvider(payload);

const cleaned = text.replace(/\`\`\`json/g, '').replace(/\`\`\`/g, '').trim();

const result = JSON.parse(cleaned);

let groundingSources: any\[\] = \[\];

if (aiProvider === 'google' && raw.candidates?.\[0\]?.groundingMetadata?.groundingChunks) {

groundingSources = raw.candidates\[0\].groundingMetadata.groundingChunks.map((c: any) =\> c.web?.uri ? { title: c.web.title, uri: c.web.uri } : null).filter(Boolean);

}

const newEntries = result.results.map((res: any) =\> ({

questionId: res.vector,

questionText: FRACTAL_VECTORS.find(v =\> v.id === res.vector)?.question \|\| res.vector,

answer: res.answer,

u: res.u,

p: res.p,

sources: groundingSources

}));

setJudgeLog(newEntries);

} catch (err: any) {

setAiError(\`Auto-Scan Failed: \${err.message}\`);

} finally {

setIsLoading(false);

setIsAutoScanning(false);

}

};

const handleJudgementScan = async () =\> {

if (!judgeEvent.trim()) return;

setIsLoading(true); setAiError(null);

const vector = FRACTAL_VECTORS\[judgeIdx\];

const prompt = \`IDENTITY: Alethekanon Judgement Protocol.\\nEVENT: "\${judgeEvent}"\\nCONTEXT: "\${globalContext}"\\nVECTOR: "\${vector.label}: \${vector.question}"\\nINSTRUCTION: Answer strictly. Calculate U (Moral) and P (Will) coords. REMEMBER: Control is -U.\\nOUTPUT JSON: { "answer": "...", "u": 0.0, "p": 0.0, "sources": \[ {"title": "...", "uri": "..."} \] }\`;

const payload: any = { contents: \[{ parts: \[{ text: prompt }\] }\], generationConfig: { responseMimeType: "application/json" } };

if (useSearch && aiProvider === 'google') payload.tools = \[{ google_search: {} }\];

try {

const { text, raw } = await callAIProvider(payload);

let sources = \[\];

if (aiProvider === 'google' && raw.candidates?.\[0\]?.groundingMetadata?.groundingChunks) {

sources = raw.candidates\[0\].groundingMetadata.groundingChunks.map((c: any) =\> c.web?.uri ? { title: c.web.title, uri: c.web.uri } : null).filter(Boolean);

} else if (aiProvider === 'perplexity' && raw.citations) {

sources = raw.citations.map((url: string, i: number) =\> ({ title: \`Ref \${i+1}\`, uri: url }));

}

const cleaned = text.replace(/\`\`\`json/g, '').replace(/\`\`\`/g, '').trim();

const result = JSON.parse(cleaned);

setJudgeLog(prev =\> {

const filtered = prev.filter(e =\> e.questionId !== vector.id);

return \[...filtered, {

questionId: vector.id,

questionText: vector.question,

answer: result.answer,

u: result.u,

p: result.p,

sources: result.sources \|\| sources

}\].sort((a,b) =\> FRACTAL_VECTORS.findIndex(v =\> v.id === a.questionId) - FRACTAL_VECTORS.findIndex(v =\> v.id === b.questionId));

});

} catch (err: any) {

setAiError(err.message \|\| "Judgement Failed.");

} finally { setIsLoading(false); }

};

const handleFractalAnalysis = (node: VectorNode, vector: string, question: string) =\> {

handleGeminiAnalysis(\`Node: "\${node.label}"\`, \`APPLY FRACTAL VECTOR \[\${vector}\]: \${question}. Generate 1-2 sub-steps.\`, node.id);

};

return (

\<div className="min-h-screen bg-black text-slate-200 font-sans p-4 md:p-8 flex flex-col items-center"\>

{/\* HEADER \*/}

\<div className="w-full max-w-6xl mb-6 flex flex-col md:flex-row justify-between items-end border-b border-slate-800 pb-4"\>

\<div\>

\<h1 className="text-3xl font-bold tracking-tighter text-white mb-2 flex items-center gap-2"\>

\<Brain className="w-8 h-8 text-emerald-500" /\>

ALETHEKANON \<span className="text-slate-600 text-sm font-normal mt-2"\>v5.6 // TYRANNY CHECK\</span\>

\</h1\>

\<p className="text-slate-400 text-sm max-w-xl"\>Hegemonic Strategic Interface. Corrected Moral Vectors.\</p\>

\</div\>

\<div className="flex gap-2 mt-4 md:mt-0 relative"\>

\<button onClick={() =\> setIsSettingsOpen(!isSettingsOpen)} className={\`px-4 py-1 text-xs uppercase rounded flex gap-2 \${isSettingsOpen ? 'bg-slate-800 text-white' : 'bg-slate-900 text-slate-500 border border-slate-800'}\`}\>\<Settings className="w-3 h-3" /\> Config\</button\>

\<button onClick={() =\> setMode('timeline')} className={\`px-4 py-1 text-xs uppercase rounded \${mode === 'timeline' ? 'bg-purple-900/50 text-purple-400 border-purple-800' : 'bg-slate-900 text-slate-500 border-slate-800'}\`}\>Timeline\</button\>

\<button onClick={() =\> setMode('judgement')} className={\`px-4 py-1 text-xs uppercase rounded flex gap-2 \${mode === 'judgement' ? 'bg-amber-900/50 text-amber-400 border-amber-800' : 'bg-slate-900 text-slate-500 border-slate-800'}\`}\>\<Scale className="w-3 h-3" /\> Judgement\</button\>

{/\* SETTINGS MODAL \*/}

{isSettingsOpen && (

\<div className="absolute top-10 right-0 w-80 bg-slate-900 border border-slate-700 rounded-lg p-4 shadow-2xl z-50"\>

\<h3 className="text-xs font-bold text-white uppercase tracking-widest mb-4"\>System Core\</h3\>

\<div className="space-y-4"\>

\<div\>

\<label className="text-\[10px\] text-slate-400 uppercase font-bold block mb-1"\>Provider Node\</label\>

\<div className="grid grid-cols-3 gap-2"\>

\<button onClick={() =\> setAiProvider('google')} className={\`text-\[10px\] py-2 rounded border \${aiProvider === 'google' ? 'bg-emerald-900/50 border-emerald-500 text-emerald-400' : 'bg-black border-slate-700'}\`}\>Google\</button\>

\<button onClick={() =\> setAiProvider('ollama')} className={\`text-\[10px\] py-2 rounded border \${aiProvider === 'ollama' ? 'bg-orange-900/50 border-orange-500 text-orange-400' : 'bg-black border-slate-700'}\`}\>Ollama\</button\>

\<button onClick={() =\> setAiProvider('perplexity')} className={\`text-\[10px\] py-2 rounded border \${aiProvider === 'perplexity' ? 'bg-blue-900/50 border-blue-500 text-blue-400' : 'bg-black border-slate-700'}\`}\>Perplex\</button\>

\</div\>

\</div\>

{aiProvider !== 'ollama' && (

\<input type="password" value={userApiKey} onChange={(e) =\> setUserApiKey(e.target.value)} placeholder={aiProvider === 'google' ? "Google API Key..." : "Perplexity API Key..."} className="w-full bg-black border border-slate-700 rounded p-2 text-xs" /\>

)}

{aiProvider === 'ollama' && (

\<div className="space-y-2"\>

\<input type="text" value={ollamaBaseUrl} onChange={(e) =\> setOllamaBaseUrl(e.target.value)} className="w-full bg-black border border-slate-700 rounded p-2 text-xs" /\>

\<input type="text" value={ollamaModel} onChange={(e) =\> setOllamaModel(e.target.value)} className="w-full bg-black border border-slate-700 rounded p-2 text-xs" /\>

\</div\>

)}

\</div\>

\</div\>

)}

\</div\>

\</div\>

\<main className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-3 gap-8"\>

{/\* VISUALIZER \*/}

\<div className="lg:col-span-2 space-y-4"\>

\<CoordinateGrid steps={plotData} hoveredStep={hoveredStep} setHoveredStep={setHoveredStep} /\>

\<div className="bg-slate-900/30 border border-slate-800 rounded-lg p-4 flex flex-col gap-4"\>

\<div className="flex flex-col gap-1"\>

\<label className="text-\[10px\] font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2"\>\<Globe className="w-3 h-3" /\> Global Directive\</label\>

\<input type="text" placeholder="Overarching Goal (e.g. 'Build Mars Colony')..." value={globalContext} onChange={(e) =\> setGlobalContext(e.target.value)} className="w-full bg-black/50 border border-slate-700 rounded p-2 text-sm text-emerald-400 focus:border-emerald-500 outline-none font-mono" /\>

\</div\>

{mode === 'timeline' && (

\<div className="flex flex-col gap-2"\>

\<div className="flex items-center gap-2"\>

\<span className="text-xs font-bold text-purple-300 uppercase tracking-widest"\>Oracle Command\</span\>

\<div className="ml-auto flex items-center gap-2"\>

\<button onClick={() =\> aiProvider === 'google' && setUseSearch(!useSearch)} className={\`flex items-center gap-2 px-2 py-1 rounded border text-\[10px\] font-mono transition-colors \${aiProvider === 'google' ? (useSearch ? 'bg-blue-900/50 border-blue-500 text-blue-400' : 'bg-black border-slate-700 text-slate-500 hover:border-slate-500') : 'opacity-50 cursor-not-allowed border-slate-800 text-slate-600'}\`} title={aiProvider === 'google' ? "Toggle Live Data" : "Search handled natively by provider"}\>\<Search className="w-3 h-3" /\> {useSearch ? "LIVE DATA" : "LOGIC ONLY"}\</button\>

\<div className={\`px-2 py-1 rounded bg-black border text-\[10px\] font-mono uppercase flex items-center gap-1 \${aiProvider === 'google' ? 'border-emerald-900/50 text-emerald-500' : aiProvider === 'ollama' ? 'border-orange-900/50 text-orange-500' : 'border-blue-900/50 text-blue-500'}\`}\>

{aiProvider === 'google' ? \<Cloud className="w-3 h-3" /\> : aiProvider === 'ollama' ? \<Server className="w-3 h-3" /\> : \<Radio className="w-3 h-3" /\>}

{aiProvider === 'google' ? 'GEMINI 2.5' : aiProvider === 'ollama' ? ollamaModel : perplexityModel}

\</div\>

\</div\>

\</div\>

{activeReference && (

\<div className="flex items-center gap-2 bg-purple-900/20 border border-purple-500/30 p-2 rounded"\>\<Link2 className="w-3 h-3 text-purple-400" /\>\<span className="text-xs text-purple-200"\>Ref: \<span className="font-bold"\>{activeReference.label}\</span\>\</span\>\<button onClick={() =\> setActiveRefId(null)} className="ml-auto text-purple-400"\>\<X className="w-3 h-3" /\>\</button\>\</div\>

)}

\<div className="flex gap-2"\>

\<input type="text" placeholder={activeReference ? \`Query "\${activeReference.label}"...\` : "Add step..."} value={goalInput} onChange={(e) =\> setGoalInput(e.target.value)} onKeyDown={(e) =\> e.key === 'Enter' && handleGeminiAnalysis(undefined, undefined)} className="flex-1 bg-black border border-slate-700 rounded p-3 text-sm text-white focus:border-purple-500 outline-none" disabled={isLoading} /\>

\<button onClick={() =\> handleGeminiAnalysis(undefined, undefined)} disabled={isLoading \|\| !goalInput} className="bg-purple-900/50 hover:bg-purple-800 text-purple-200 border border-purple-700 rounded px-6 py-2 text-xs uppercase font-bold tracking-widest flex items-center gap-2"\>{isLoading ? \<Loader2 className="w-4 h-4 animate-spin" /\> : \<Sparkles className="w-4 h-4" /\>}\</button\>

\</div\>

\</div\>

)}

{mode === 'judgement' && (

\<div className="flex flex-col gap-4"\>

\<div className="flex gap-2"\>\<input type="text" placeholder="Event to Judge..." value={judgeEvent} onChange={(e) =\> setJudgeEvent(e.target.value)} className="flex-1 bg-black border border-amber-900/50 rounded p-3 text-sm text-amber-100 placeholder:text-amber-900/50 focus:border-amber-500 outline-none" /\>\</div\>

{/\* BATCH CONTROLS \*/}

\<div className="flex items-center justify-between bg-black/40 p-2 rounded border border-slate-800"\>

\<span className="text-\[10px\] text-slate-500 uppercase tracking-widest pl-2"\>7-Vector Auto Scan\</span\>

\<button

onClick={handleAutoScan}

disabled={isLoading \|\| !judgeEvent}

className={\`flex items-center gap-2 px-3 py-1.5 rounded text-xs uppercase font-bold tracking-widest border transition-all \${isAutoScanning ? 'bg-red-900/50 border-red-500 text-red-400 animate-pulse' : 'bg-emerald-900/50 border-emerald-500 text-emerald-400 hover:bg-emerald-900'}\`}

\>

{isLoading ? \<Loader2 className="w-3 h-3 animate-spin" /\> : \<PlayCircle className="w-3 h-3" /\>} Calculate

\</button\>

\</div\>

\<div className="bg-amber-950/20 border border-amber-900/50 rounded p-4 relative"\>

\<div className="text-\[10px\] font-mono text-amber-600 mb-1"\>VECTOR {judgeIdx + 1}/7\</div\>

\<h3 className="text-sm font-bold text-amber-200 mb-4"\>{FRACTAL_VECTORS\[judgeIdx\].label}: {FRACTAL_VECTORS\[judgeIdx\].question}\</h3\>

\<div className="flex gap-2"\>

\<button onClick={() =\> setJudgeIdx(Math.max(0, judgeIdx - 1))} className="p-2 rounded bg-amber-900/20 text-amber-500"\>\<ArrowLeft className="w-4 h-4" /\>\</button\>

\<button onClick={handleJudgementScan} disabled={isLoading \|\| !judgeEvent \|\| isAutoScanning} className="flex-1 bg-amber-600 hover:bg-amber-500 text-black font-bold uppercase text-xs tracking-widest rounded flex items-center justify-center gap-2"\>{isLoading && !isAutoScanning ? \<Loader2 className="w-4 h-4 animate-spin" /\> : "Scan Single"}\</button\>

\<button onClick={() =\> setJudgeIdx(Math.min(6, judgeIdx + 1))} className="p-2 rounded bg-amber-900/20 text-amber-500"\>\<ArrowRight className="w-4 h-4" /\>\</button\>

\</div\>

\</div\>

\</div\>

)}

{aiError && \<div className="text-xs text-red-400 px-2 py-1 bg-red-950/20 border border-red-900/50 rounded flex items-center gap-2"\>\<AlertTriangle className="w-3 h-3" /\> {aiError}\</div\>}

\</div\>

\</div\>

{/\* SIDEBAR LOG \*/}

\<div className="flex flex-col h-\[600px\] bg-slate-900/50 border border-slate-800 rounded-lg overflow-hidden"\>

\<div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900"\>

\<h2 className="text-sm font-bold text-slate-300 uppercase tracking-widest flex items-center gap-2"\>\<Info className="w-4 h-4" /\> {mode === 'judgement' ? 'Verdict Log' : 'Strategic Log'}\</h2\>

\<div className="flex gap-2"\>

{mode === 'timeline' && (

\<div className="flex gap-1"\>

\<button onClick={() =\> handleQuickPreset('empire')} title="Generate Empire Strategy" className="p-1 hover:bg-slate-800 rounded text-slate-500 hover:text-emerald-400 transition-colors"\>\<FlaskConical className="w-3 h-3" /\>\</button\>

\<button onClick={() =\> handleQuickPreset('peace')} title="Generate Peace Strategy" className="p-1 hover:bg-slate-800 rounded text-slate-500 hover:text-blue-400 transition-colors"\>\<Target className="w-3 h-3" /\>\</button\>

\</div\>

)}

\<div className="w-px h-4 bg-slate-800 mx-1"\>\</div\>

\<button onClick={handleClear} className="p-1 hover:bg-red-900/30 rounded text-slate-500 hover:text-red-400"\>\<RefreshCw className="w-3 h-3" /\>\</button\>

\</div\>

\</div\>

\<div className="flex-1 overflow-y-auto p-2 space-y-2 scrollbar-thin scrollbar-thumb-slate-700"\>

{mode !== 'judgement' ? (

timeline.length === 0 ? (

\<div className="text-center text-slate-600 text-xs py-10 italic"\>Timeline Empty.\<br/\>Use Oracle or Quick-Gen.\</div\>

) : (

timeline.map((step, idx) =\> \<SidebarNode key={step.id} step={step} idxString={\`\${idx + 1}\`} level={0} hoveredStep={hoveredStep} setHoveredStep={setHoveredStep} removeStep={removeStep} handleFractalAnalysis={handleFractalAnalysis} handleSetReference={handleSetReference} isLoading={isLoading} /\>)

)

) : (

judgeLog.length === 0 ? (

\<div className="text-center text-slate-600 text-xs py-10 italic"\>No Judgements.\<br/\>Enter Event & Scan.\</div\>

) : (

judgeLog.map((entry) =\> (

\<div

key={entry.questionId}

className={\`bg-amber-950/20 border rounded p-3 mb-2 transition-all cursor-pointer \${hoveredStep === entry.questionId ? 'border-amber-500 bg-amber-900/30' : 'border-amber-900/30'}\`}

onMouseEnter={() =\> setHoveredStep(entry.questionId)}

onMouseLeave={() =\> setHoveredStep(null)}

\>

\<div className="flex justify-between items-start mb-2"\>

\<div className="text-\[9px\] font-mono text-amber-600 mb-1"\>{entry.questionId}\</div\>

{entry.u !== undefined && (

\<div className="flex gap-2 text-\[9px\] font-mono"\>

\<span className={entry.u \> 0 ? "text-emerald-500" : "text-amber-500"}\>U: {entry.u.toFixed(2)}\</span\>

\<span className={entry.p && entry.p \> 0 ? "text-emerald-500" : "text-red-500"}\>P: {entry.p?.toFixed(2)}\</span\>

\</div\>

)}

\</div\>

\<div className="text-xs text-amber-200 font-bold mb-2"\>{entry.questionText}\</div\>

\<p className="text-xs text-slate-300 leading-relaxed pl-2 border-l-2 border-amber-800"\>{entry.answer}\</p\>

{entry.sources && \<div className="mt-2 pt-2 border-t border-amber-900/20 flex flex-wrap gap-2"\>{entry.sources.map((s, i) =\> \<a key={i} href={s.uri} target="\_blank" rel="noreferrer" className="text-\[9px\] text-amber-500 hover:text-amber-300 underline flex items-center gap-1"\>\<Link2 className="w-2 h-2" /\> {s.title \|\| 'Source'}\</a\>)}\</div\>}

\</div\>

))

)

)}

\</div\>

\</div\>

\</main\>

\</div\>

);

}
