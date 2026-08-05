import { useState, useRef, useCallback, useEffect, useMemo } from "react";

export default function DensityPlot() {
  const svgRef = useRef(null);
  const frame = { left: 75, right: 295, top: 100, bottom: 320, midY: 210 };
  const cx = 185, cy = 210, rx = 155, ry = 155;
  const [point, setPoint] = useState({ x: 185, y: 210 });
  const [dragging, setDragging] = useState(false);

  const clientToSvg = useCallback((clientX, clientY) => {
    const svg = svgRef.current;
    const pt = svg.createSVGPoint();
    pt.x = clientX;
    pt.y = clientY;
    const ctm = svg.getScreenCTM().inverse();
    return pt.matrixTransform(ctm);
  }, []);

  const updateFromEvent = useCallback(
    (clientX, clientY) => {
      const { x, y } = clientToSvg(clientX, clientY);
      setPoint({
        x: Math.max(frame.left, Math.min(frame.right, x)),
        y: Math.max(frame.top, Math.min(frame.bottom, y)),
      });
    },
    [clientToSvg]
  );

  useEffect(() => {
    if (!dragging) return;
    const onMove = (e) => {
      const touchPt = e.touches ? e.touches[0] : e;
      updateFromEvent(touchPt.clientX, touchPt.clientY);
    };
    const onUp = () => setDragging(false);
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
    window.addEventListener("touchmove", onMove, { passive: false });
    window.addEventListener("touchend", onUp);
    return () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("touchmove", onMove);
      window.removeEventListener("touchend", onUp);
    };
  }, [dragging, updateFromEvent]);

  const apex = { x: frame.right, y: frame.midY };

  const tickVals = [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100];

  // circle as a radial/angular axis: degree marks every 45°, plus a radial
  // systemic scale (1x, 2x) running outward from center along the X direction
  const degMarks = [0, 45, 90, 135, 180, 225, 270, 315];
  const degPoint = (deg) => {
    const rad = (deg * Math.PI) / 180;
    return { x: cx + rx * Math.cos(rad), y: cy + ry * Math.sin(rad) };
  };

  // all 8 arms: x1,y1 is the 0% apex end, x2,y2 is the 100% corner end
  // stated: density of claimed/asserted resource. verified: density of cross-source corroborated resource.
  // both 0-100, drawn as ribbon half-width. Productive and Regressive carry the real
  // Iran-war analysis; the rest are flat placeholders pending actual claims for those corners.
  const arms = [
    { x1: apex.x, y1: apex.y, x2: frame.left, y2: frame.top, color: "#7a1f1f", dash: false, label: "Productive", group: "Potential", stated: 69, verified: 33 },
    { x1: apex.x, y1: apex.y, x2: frame.left, y2: frame.bottom, color: "#1f4a7a", dash: false, label: "Constructive", group: "Potential", stated: 69, verified: 33 },
    { x1: frame.left, y1: frame.midY, x2: frame.right, y2: frame.top, color: "#7a1f1f", dash: true, label: "Reductive", group: "Anti-potential", stated: 63, verified: 85 },
    { x1: frame.left, y1: frame.midY, x2: frame.right, y2: frame.bottom, color: "#1f4a7a", dash: true, label: "Regressive", group: "Anti-potential", stated: 80, verified: 80 },
    { x1: 185, y1: frame.top, x2: frame.left, y2: frame.bottom, color: "#b36b00", dash: false, label: "Constructive", group: "Suppressive", stated: 0, verified: 0 },
    { x1: 185, y1: frame.top, x2: frame.right, y2: frame.bottom, color: "#0a7a6a", dash: false, label: "Regressive", group: "Suppressive", stated: 0, verified: 0 },
    { x1: 185, y1: frame.bottom, x2: frame.left, y2: frame.top, color: "#b36b00", dash: true, label: "Productive", group: "Active", stated: 0, verified: 0 },
    { x1: 185, y1: frame.bottom, x2: frame.right, y2: frame.top, color: "#0a7a6a", dash: true, label: "Reductive", group: "Active", stated: 0, verified: 0 },
  ];

  // for each arm, project the point's distance to that arm's corner (x2,y2),
  // normalized against the arm's own full length (x1,y1 to x2,y2), so every
  // arm reports how far the point sits from its vertex on that arm's own 0-100 scale
  // closest point on each axis LINE to the dragged point.
  // dir = projected position on the axis's own 0-100 scale (can exceed 0-100 if the
  //       point projects past an end, which is real information, not an error)
  // mag = closeness, normalized against the frame diagonal so every axis uses the
  //       SAME scale and magnitudes are comparable between axes. 100 = on the axis.
  const closestOn = (ax) => {
    const dx = ax.x2 - ax.x1, dy = ax.y2 - ax.y1;
    const len = Math.hypot(dx, dy);
    const ux = dx / len, uy = dy / len;
    const alongRaw = (point.x - ax.x1) * ux + (point.y - ax.y1) * uy;
    const nx = ax.x1 + ux * alongRaw, ny = ax.y1 + uy * alongRaw;
    const dist = Math.hypot(point.x - nx, point.y - ny);
    const alongClamped = Math.max(0, Math.min(len, alongRaw));
    return {
      dir: (alongRaw / len) * 100,
      mag: Math.max(0, 100 * (1 - dist / len)),
      nx: ax.x1 + ux * alongClamped,
      ny: ax.y1 + uy * alongClamped,
    };
  };

  // every reading is a vector [dir, mag]: dir = position along that edge (0-100 from
  // its first corner), mag = closeness to that edge, inverted so on-edge = 100
  const edgeAxes = [
    { x1: frame.left, y1: frame.bottom, x2: frame.left, y2: frame.top, name: "Good", from: "Constructive", to: "Productive", color: "#0a7a3a" },
    { x1: frame.right, y1: frame.top, x2: frame.right, y2: frame.bottom, name: "Bad", from: "Reductive", to: "Regressive", color: "#7a1f1f" },
    { x1: frame.right, y1: frame.top, x2: frame.left, y2: frame.top, name: "Top", from: "Reductive", to: "Productive", color: "#0a7a3a" },
    { x1: frame.right, y1: frame.bottom, x2: frame.left, y2: frame.bottom, name: "Bottom", from: "Regressive", to: "Constructive", color: "#7a1f1f" },
  ];

  // Simple, direct: text moves out of other text's way.
  // DOT: fixed point, not a physics body, nothing collides with it.
  // RESULT: sprung hard onto its own dot.
  // LABEL: sprung to hug its own result from whichever side it already sits
  //        on (no left/right/any preference - the direction it hugs from is
  //        just wherever it currently is). Everything is an axis-aligned box
  //        that pushes other boxes out of the way. No rotation, no orbits.
  const labelSim = useMemo(() => {
    const allAxes = [...arms, ...edgeAxes];
    const CANVAS_W = 370, CANVAS_H = 470, MARGIN = 4, PAD = 1;

    const dots = allAxes.map((ax) => {
      const v = closestOn(ax);
      return { x: v.nx, y: v.ny };
    });

    const results = allAxes.map((ax, i) => {
      const v = closestOn(ax);
      const text = `[${v.dir.toFixed(0)},${v.mag.toFixed(0)}]`; // locked in, physics never alters this
      return { kind: "result", idx: i, text, color: ax.color,
        x: dots[i].x, y: dots[i].y, w: text.length * 4.0 + 2, h: 8 };
    });
    const labels = allAxes.map((ax, i) => {
      const name = ax.group ? `${ax.group}\u2192${ax.label}` : `${ax.from}\u2194${ax.to}`;
      // preferred side: result on the right half of the plot -> label sits
      // to its LEFT; result on the left half -> label sits to its RIGHT.
      // (so labels lean inward, away from the nearest canvas edge)
      const side = dots[i].x > CANVAS_W / 2 ? -1 : 1;
      const w = name.length * 3.8 + 2;
      return { kind: "label", idx: i, text: name, color: ax.color, side,
        x: dots[i].x + side * 20, y: dots[i].y,
        w, h: 8 };
    });
    const bodies = [...results, ...labels];

    // one collision+clamp sweep, factored out so the settling phase below
    // can run it without the springs
    const collideAndClamp = () => {
      // everything pushes everything else out of the way, EXCEPT a label
      // and its own result - that pair is glued edge-to-edge by the spring
      // above, so letting the collision resolver see them as overlapping
      // would just fight the glue and open a gap.
      for (let i = 0; i < bodies.length; i++) {
        for (let j = i + 1; j < bodies.length; j++) {
          const a = bodies[i], b = bodies[j];
          if (a.idx === b.idx && a.kind !== b.kind) continue; // own result/label pair
          const dx = b.x - a.x, dy = b.y - a.y;
          const ox = (a.w + b.w) / 2 + PAD - Math.abs(dx);
          const oy = (a.h + b.h) / 2 + PAD - Math.abs(dy);
          if (ox > 0 && oy > 0) {
            const wa = a.kind === "result" ? 0.15 : 0.85;
            const wb = b.kind === "result" ? 0.15 : 0.85;
            const tot = wa + wb;
            if (ox < oy) {
              const s = dx === 0 ? (i < j ? -1 : 1) : Math.sign(dx);
              a.x -= s * ox * (wa / tot);
              b.x += s * ox * (wb / tot);
            } else {
              const s = dy === 0 ? (i < j ? -1 : 1) : Math.sign(dy);
              a.y -= s * oy * (wa / tot);
              b.y += s * oy * (wb / tot);
            }
          }
        }
      }
      // stay on canvas
      for (const b of bodies) {
        b.x = Math.max(b.w / 2 + MARGIN, Math.min(CANVAS_W - b.w / 2 - MARGIN, b.x));
        b.y = Math.max(b.h / 2 + MARGIN, Math.min(CANVAS_H - b.h / 2 - MARGIN, b.y));
      }
    };

    for (let iter = 0; iter < 200; iter++) {
      // RESULT hugs its dot
      for (const r of results) {
        r.x += (dots[r.idx].x - r.x) * 0.35;
        r.y += (dots[r.idx].y - r.y) * 0.35;
      }
      // LABEL is sprung flush against its result on its preferred side -
      // target gap is exactly zero, so their box edges touch (glued).
      for (const l of labels) {
        const r = results[l.idx];
        const targetX = r.x + l.side * ((r.w + l.w) / 2);
        l.x += (targetX - l.x) * 0.4;
        l.y += (r.y - l.y) * 0.3;
      }
      collideAndClamp();
    }

    // SETTLING PHASE: collision only, no springs. Without this the spring
    // gets the last word on the final iteration and can pull a label back
    // on top of a neighbouring result, which is exactly the leftover
    // overlap that kept showing up. Glue is unaffected - a label and its
    // own result are excluded from collision, so they stay locked together
    // while everything else finishes separating.
    for (let iter = 0; iter < 60; iter++) collideAndClamp();

    return { results, labels, dots };
  }, [point.x, point.y]);

  const evidenceLog = {
    Productive: {
      stated: [
        { s: 1.5, text: "Islamabad direct talks, Apr 11-12, highest-level US-Iran engagement since 1979", url: "https://www.britannica.com/event/2026-Iran-war" },
        { s: 2.0, text: "Memorandum of Understanding signed mid-June", url: "https://www.cnn.com/2026/07/09/world/live-news/iran-war-trump" },
        { s: 1.0, text: "Ongoing technical talks under the MoU framework", url: "https://www.cnn.com/2026/06/30/world/live-news/iran-war-trump" },
        { s: 1.0, text: "Oman's regional push, calls with Iran, Saudi Arabia, Qatar, Kuwait, Egypt", url: "https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html" },
      ],
      verified: [
        { s: 0.5, text: "Ceasefire crumbling by July 9, fresh strikes resumed", url: "https://www.cnn.com/2026/07/09/world/live-news/iran-war-trump" },
        { s: 0.5, text: "Iran: 'no current negotiations' as of July 27", url: "https://www.cnn.com/2026/07/27/world/live-news/iran-war-trump" },
        { s: 1.0, text: "Oman's push still unresolved late July", url: "https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html" },
      ],
    },
    Constructive: {
      stated: [
        { s: 1.5, text: "Two-week pause agreed Apr 8 via Pakistan mediation", url: "https://commonslibrary.parliament.uk/research-briefings/cbp-10637/" },
        { s: 1.5, text: "Trump halted lethal strikes to give talks 'space'", url: "https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html" },
        { s: 1.0, text: "Iran reciprocated restraint during the pause", url: "https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html" },
        { s: 1.5, text: "Ceasefire stipulated safe passage for Hormuz shipping", url: "https://www.cnn.com/2026/06/30/world/live-news/iran-war-trump" },
      ],
      verified: [
        { s: 0.5, text: "Same crumbling evidence, restraint didn't hold", url: "https://www.cnn.com/2026/07/09/world/live-news/iran-war-trump" },
        { s: 0.5, text: "13 days of intensifying strikes before the July pause", url: "https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html" },
        { s: 1.0, text: "Restraint held only temporarily, not durably", url: "https://www.cnbc.com/2026/07/27/us-iran-war-trump-hormuz.html" },
      ],
    },
    Reductive: {
      stated: [
        { s: 1.5, text: "Self-defense/UN charter justification", url: "https://commonslibrary.parliament.uk/research-briefings/cbp-10521/" },
        { s: 1.0, text: "Stated goal: destroy ballistic missile capability", url: "https://www.britannica.com/event/2026-Iran-war" },
        { s: 1.0, text: "Stated goal: eliminate Iran's navy", url: "https://www.britannica.com/event/2026-Iran-war" },
        { s: 1.5, text: "Stated goal: prevent nuclear weapon acquisition", url: "https://www.britannica.com/event/2026-Iran-war" },
        { s: 1.0, text: "Stated goal: sever proxy support", url: "https://www.britannica.com/event/2026-Iran-war" },
        { s: 1.5, text: "Stated goal: regime change via Iranian uprising", url: "https://www.cfr.org/global-conflict-tracker/conflict/confrontation-between-united-states-and-iran" },
      ],
      verified: [
        { s: 1.5, text: "IAEA inspectors withdrawn, effect unclear", url: "https://www.congress.gov/crs-product/IF12106" },
        { s: 2.0, text: "Uranium stockpile unconfirmed moved, program delayed not eliminated", url: "https://israel-alma.org/iran-situation-assessment-february-2026-the-race-to-rebuild-the-nuclear-and-missile-array-casual-terror-and-the-crink/" },
        { s: 1.5, text: "Missile infrastructure being rebuilt post-war", url: "https://israel-alma.org/iran-situation-assessment-february-2026-the-race-to-rebuild-the-nuclear-and-missile-array-casual-terror-and-the-crink/" },
        { s: 2.0, text: "Officials' own 'obliterated vs still imminent' contradiction", url: "https://carnegieendowment.org/emissary/2026/05/iran-nuclear-program-progress-deal" },
        { s: 1.5, text: "War resumption driven by conventional/domestic factors, not new nuclear findings", url: "https://carnegieendowment.org/emissary/2026/05/iran-nuclear-program-progress-deal" },
      ],
    },
    Regressive: {
      stated: [
        { s: 2.0, text: "Minab school strike, ~170 killed, plus leadership deaths", url: "https://www.cfr.org/global-conflict-tracker/conflict/confrontation-between-united-states-and-iran" },
        { s: 1.5, text: "Iranian Red Crescent count: 201 killed, 150+ civilians", url: "https://en.wikipedia.org/wiki/2026_Israeli%E2%80%93United_States_strikes_on_Iran" },
        { s: 1.5, text: "HRANA independent count: 133 killed, 200+ injured", url: "https://en.wikipedia.org/wiki/2026_Israeli%E2%80%93United_States_strikes_on_Iran" },
        { s: 1.5, text: "Beit Shemesh strike, 9 Israeli civilians killed", url: "https://en.wikipedia.org/wiki/2026_Iranian_strikes_on_Israel" },
        { s: 1.5, text: "UAE strikes, 3 foreign workers killed, 58 injured", url: "https://en.wikipedia.org/wiki/Iranian_strikes_on_the_United_Arab_Emirates" },
      ],
      verified: [],
    },
  };

  return (
    <div className="w-full bg-white flex flex-col items-center p-6 font-sans select-none">
      <div className="text-sm text-neutral-600 text-center mb-2">
        drag the red handle along υ to read (υ, ψ) at that point
      </div>

      <div className="w-full flex justify-center">
      <svg
        ref={svgRef}
        width="370"
        height="470"
        viewBox="0 0 370 470"
        style={{ width: "100%", height: "auto", maxWidth: "780px", cursor: dragging ? "grabbing" : "crosshair" }}
        className="touch-none"
        onPointerDown={(e) => {
          setDragging(true);
          updateFromEvent(e.clientX, e.clientY);
        }}
      >
        <defs>
          <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="2.5" orient="auto">
            <path d="M0,0 L6,2.5 L0,5 Z" fill="#222" />
          </marker>
          <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="2.5" orient="auto">
            <path d="M0,0 L6,2.5 L0,5 Z" fill="#0a7a3a" />
          </marker>
        </defs>

        <circle
          cx={point.x}
          cy={point.y}
          r="9"
          fill={dragging ? "#c0392b" : "#333"}
          stroke="#fff"
          strokeWidth="2"
          onPointerDown={(e) => {
            e.target.setPointerCapture?.(e.pointerId);
            setDragging(true);
          }}
          onTouchStart={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
        />

        {/* CIRCLE AS AXIS: boundary plus degree ticks plus radial scale */}
        <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke="#999" strokeWidth="1.5" strokeDasharray="4,3" />
        {degMarks.map((deg) => {
          const p = degPoint(deg);
          const inner = {
            x: cx + (rx - 8) * Math.cos((deg * Math.PI) / 180),
            y: cy + (ry - 8) * Math.sin((deg * Math.PI) / 180),
          };
          const labelPos = {
            x: cx + (rx + 14) * Math.cos((deg * Math.PI) / 180),
            y: cy + (ry + 14) * Math.sin((deg * Math.PI) / 180),
          };
          return (
            <g key={deg}>
              <line x1={inner.x} y1={inner.y} x2={p.x} y2={p.y} stroke="#999" strokeWidth="1.5" />
              <text x={labelPos.x} y={labelPos.y + 3} fontSize="7" fill="#999" textAnchor="middle">{deg}°</text>
            </g>
          );
        })}
        {/* radial scale, 1x at frame edge, 2x at circle edge, running along the X crosshair direction */}
        <line x1={frame.right} y1={frame.midY} x2={cx + rx} y2={frame.midY} stroke="#0a7a3a" strokeWidth="1" strokeDasharray="1,2" />
        <text x={frame.right + 4} y={frame.midY - 6} fontSize="7" fill="#0a7a3a">1x</text>
        <text x={cx + rx - 14} y={frame.midY - 6} fontSize="7" fill="#0a7a3a">2x</text>
        <text x={185} y="26" fontSize="8" textAnchor="middle" fill="#888">±2 systemic horizon (radial axis)</text>

        {/* top edge: one full-length 0-100 scale, Productive=0/Reductive=0 respectively */}
        <line x1={frame.left} y1={frame.top} x2={frame.right} y2={frame.top} stroke="#0a7a3a" strokeWidth="2" />
        {[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map((pct) => {
          const x = frame.left + (pct / 100) * (frame.right - frame.left);
          return (
            <g key={"top" + pct} fontSize="6">
              <line x1={x} y1={frame.top - 4} x2={x} y2={frame.top + 4} stroke="#0a7a3a" strokeWidth="1" />
              <text x={x} y={frame.top - 16} textAnchor="middle" fill="#0a7a3a">{pct}</text>
              <text x={x} y={frame.top - 9} textAnchor="middle" fill="#5ab87a">{100 - pct}</text>
            </g>
          );
        })}

        {/* bottom edge: one full-length 0-100 scale, Constructive=0/Regressive=0 respectively */}
        <line x1={frame.left} y1={frame.bottom} x2={frame.right} y2={frame.bottom} stroke="#7a1f1f" strokeWidth="2" />
        {[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map((pct) => {
          const x = frame.left + (pct / 100) * (frame.right - frame.left);
          return (
            <g key={"bottom" + pct} fontSize="6">
              <line x1={x} y1={frame.bottom - 4} x2={x} y2={frame.bottom + 4} stroke="#7a1f1f" strokeWidth="1" />
              <text x={x} y={frame.bottom + 14} textAnchor="middle" fill="#7a1f1f">{pct}</text>
              <text x={x} y={frame.bottom + 21} textAnchor="middle" fill="#c07070">{100 - pct}</text>
            </g>
          );
        })}

        {/* Good edge: one full-length 0-100 scale, readable from either end, Productive=0/Constructive=0 respectively */}
        <line x1={frame.left} y1={frame.top} x2={frame.left} y2={frame.bottom} stroke="#0a7a3a" strokeWidth="2" />
        {[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map((pct) => {
          const y = frame.top + (pct / 100) * (frame.bottom - frame.top);
          return (
            <g key={"good" + pct} fontSize="6">
              <line x1={frame.left - 4} y1={y} x2={frame.left + 4} y2={y} stroke="#0a7a3a" strokeWidth="1" />
              <text x={frame.left - 22} y={y + 2} textAnchor="end" fill="#0a7a3a">{pct}</text>
              <text x={frame.left - 9} y={y + 2} textAnchor="end" fill="#5ab87a">{100 - pct}</text>
            </g>
          );
        })}

        {/* Bad edge: one full-length 0-100 scale, readable from either end, Reductive=0/Regressive=0 respectively */}
        <line x1={frame.right} y1={frame.top} x2={frame.right} y2={frame.bottom} stroke="#7a1f1f" strokeWidth="2" />
        {[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map((pct) => {
          const y = frame.top + (pct / 100) * (frame.bottom - frame.top);
          return (
            <g key={"bad" + pct} fontSize="6">
              <line x1={frame.right - 4} y1={y} x2={frame.right + 4} y2={y} stroke="#7a1f1f" strokeWidth="1" />
              <text x={frame.right + 9} y={y + 2} textAnchor="start" fill="#7a1f1f">{pct}</text>
              <text x={frame.right + 22} y={y + 2} textAnchor="start" fill="#c07070">{100 - pct}</text>
            </g>
          );
        })}


        {tickVals.map((v) => {
          const y = frame.midY - (v / 100) * (frame.midY - frame.top);
          return (
            <g key={"y" + v} fontSize="7" fill="#666">
              <line x1={frame.left} y1={y} x2={frame.right} y2={y} stroke="#f0f0f0" strokeWidth="1" />
              <line x1={185 - 4} y1={y} x2={185 + 4} y2={y} stroke="#222" strokeWidth="1.2" />
              <text x={175} y={y + 3} textAnchor="end">{v}</text>
            </g>
          );
        })}
        {tickVals.map((v) => {
          const x = 185 - (v / 100) * (frame.right - frame.left) / 2;
          return (
            <g key={"x" + v} fontSize="7" fill="#666">
              <line x1={x} y1={frame.top} x2={x} y2={frame.bottom} stroke="#f0f0f0" strokeWidth="1" />
              <line x1={x} y1={frame.midY - 4} x2={x} y2={frame.midY + 4} stroke="#222" strokeWidth="1.2" />
              <text x={x} y={frame.midY - 8} textAnchor="middle">{v}</text>
            </g>
          );
        })}

        {/* the four triangle outlines: potential, anti-potential, ascent, descent */}
        <polygon points={`${frame.left},${frame.top} ${frame.left},${frame.bottom} ${apex.x},${apex.y}`} fill="none" stroke="#222" strokeWidth="2" />
        <polygon points={`${frame.right},${frame.top} ${frame.right},${frame.bottom} ${frame.left},${frame.midY}`} fill="none" stroke="#222" strokeWidth="2" strokeDasharray="5,3" />
        <polygon points={`${frame.left},${frame.bottom} ${frame.right},${frame.bottom} ${185},${frame.top}`} fill="none" stroke="#222" strokeWidth="2" />
        <polygon points={`${frame.left},${frame.top} ${frame.right},${frame.top} ${185},${frame.bottom}`} fill="none" stroke="#222" strokeWidth="2" strokeDasharray="5,3" />

        {/* apex and corner-anchor dots */}
        <circle cx={apex.x} cy={apex.y} r="3" fill="#222" />
        <circle cx={frame.left} cy={frame.midY} r="3" fill="#222" />
        <circle cx={185} cy={frame.top} r="3" fill="#222" />
        <circle cx={185} cy={frame.bottom} r="3" fill="#222" />

        {/* the 8 arms, each a 0-100% scale with tick marks every 10 */}
        {arms.map((arm, i) => {
          const dx = arm.x2 - arm.x1, dy = arm.y2 - arm.y1;
          const len = Math.sqrt(dx * dx + dy * dy);
          const ux = dx / len, uy = dy / len;
          const px = -uy, py = ux;
          const ticks = [];
          for (let pct = 0; pct <= 100; pct += 10) {
            const f = pct / 100;
            const tx = arm.x1 + dx * f, ty = arm.y1 + dy * f;
            ticks.push(
              <g key={i + "-" + pct}>
                <line x1={tx - px * 3} y1={ty - py * 3} x2={tx + px * 3} y2={ty + py * 3} stroke={arm.color} strokeWidth="1" />
                <text x={tx + px * 9} y={ty + py * 9 + 2} fontSize="5.5" fill={arm.color} textAnchor="middle">{pct}</text>
              </g>
            );
          }
          const ribbonHalfWidth = 6;
          const statedT = arm.stated / 100, verifiedT = arm.verified / 100;
          const statedEnd = { x: arm.x1 + dx * statedT, y: arm.y1 + dy * statedT };
          const verifiedEnd = { x: arm.x1 + dx * verifiedT, y: arm.y1 + dy * verifiedT };
          const ribbon = (endPt) =>
            `${arm.x1 - px * ribbonHalfWidth},${arm.y1 - py * ribbonHalfWidth} ${endPt.x - px * ribbonHalfWidth},${endPt.y - py * ribbonHalfWidth} ${endPt.x + px * ribbonHalfWidth},${endPt.y + py * ribbonHalfWidth} ${arm.x1 + px * ribbonHalfWidth},${arm.y1 + py * ribbonHalfWidth}`;
          return (
            <g key={"arm" + i}>
              <polygon points={ribbon(statedEnd)} fill={arm.color} opacity="0.2" />
              <polygon points={ribbon(verifiedEnd)} fill={arm.color} opacity="0.45" />
              <circle cx={statedEnd.x} cy={statedEnd.y} r="2.5" fill={arm.color} opacity="0.5" />
              <circle cx={verifiedEnd.x} cy={verifiedEnd.y} r="2.5" fill={arm.color} />
              <line x1={arm.x1} y1={arm.y1} x2={arm.x2} y2={arm.y2} stroke={arm.color} strokeWidth="2" strokeDasharray={arm.dash ? "5,3" : undefined} />
              {ticks}
            </g>
          );
        })}

        {/* second pass: every arm's name label, drawn AFTER all arm lines/ribbons above,
            so no line from any arm can ever paint over any label. Fully
            static - fixed position, fixed rotation, not part of labelSim,
            exactly as originally built. */}
        {arms.map((arm, i) => {
          const dx = arm.x2 - arm.x1, dy = arm.y2 - arm.y1;
          const sameCornerArms = arms.filter((a) => a.label === arm.label);
          const pairIndex = sameCornerArms.indexOf(arm);
          const t = pairIndex === 0 ? 0.22 : 0.82;
          const labelPos = arm.x1 + dx * t;
          const labelPosY = arm.y1 + dy * t;
          let angleDeg = (Math.atan2(dy, dx) * 180) / Math.PI;
          if (angleDeg > 90 || angleDeg < -90) angleDeg += 180;
          return (
            <text
              key={"armlabel" + i}
              x={labelPos} y={labelPosY - 8}
              fontSize="6.5" fontWeight="bold" fill={arm.color} textAnchor="middle" opacity="0.45"
              transform={`rotate(${angleDeg} ${labelPos} ${labelPosY - 8})`}
              style={{ paintOrder: "stroke", stroke: "#fff", strokeWidth: 2.5 }}
            >
              {arm.group} → {arm.label}
            </text>
          );
        })}
        <text x={frame.left} y="44" fontSize="7" fill="#999" textAnchor="middle">band length = how far built, not width. light = stated, dark = verified reach</text>

        <text x={frame.left - 8} y={frame.midY + 3} fontSize="8" fill="#0a7a3a" fontWeight="bold" textAnchor="middle" opacity="0.45" transform={`rotate(-90 ${frame.left - 8} ${frame.midY + 3})`}>Constr↔Product</text>
        <text x={185} y={frame.midY - 26} fontSize="9" fill="#666" fontWeight="bold" textAnchor="middle" opacity="0.45">Mix</text>
        <text x={frame.right + 8} y={frame.midY + 3} fontSize="8" fill="#7a1f1f" fontWeight="bold" textAnchor="middle" opacity="0.45" transform={`rotate(-90 ${frame.right + 8} ${frame.midY + 3})`}>Reduct↔Regress</text>
        <text x={185} y={frame.top - 24} fontSize="8" fill="#0a7a3a" fontWeight="bold" textAnchor="middle" opacity="0.45">Reduct↔Product</text>
        <text x={185} y={frame.bottom + 32} fontSize="8" fill="#7a1f1f" fontWeight="bold" textAnchor="middle" opacity="0.45">Regress↔Constr</text>

        {/* one label per corner, not per arm, since two arms land on each corner */}
        <text x={frame.left - 10} y={frame.top - 12} fontSize="11" fontWeight="bold" fill="#333" textAnchor="middle">Productive</text>
        <text x={frame.right + 10} y={frame.top - 12} fontSize="11" fontWeight="bold" fill="#333" textAnchor="middle">Reductive</text>
        <text x={frame.left - 10} y={frame.bottom + 20} fontSize="11" fontWeight="bold" fill="#333" textAnchor="middle">Constructive</text>
        <text x={frame.right + 10} y={frame.bottom + 20} fontSize="11" fontWeight="bold" fill="#333" textAnchor="middle">Regressive</text>

        {/* the real axis: X (υ) and Y (ψ), both through the origin at center */}
        <line x1={frame.right + 15} y1={frame.midY} x2={frame.left - 15} y2={frame.midY} stroke="#222" strokeWidth="2" markerEnd="url(#arrow)" />
        <text x={frame.left - 22} y={frame.midY + 4} fontSize="11" fill="#222" fontWeight="bold" fontStyle="italic" textAnchor="end">υ</text>
        <line x1={185} y1={frame.bottom + 15} x2={185} y2={frame.top - 15} stroke="#222" strokeWidth="2" markerEnd="url(#arrow)" />
        <text x={191} y={frame.top - 18} fontSize="11" fill="#222" fontWeight="bold" fontStyle="italic">ψ</text>
        <circle cx={185} cy={frame.midY} r="2.5" fill="#222" />
        <text x={191} y={frame.midY + 16} fontSize="8" fill="#666">0,0</text>

        {/* two passes: all dots/rays first (bottom layer), then all result
            and axis-label text after (top layer), so a dot from one axis
            can never paint over another axis's text regardless of order */}
        <g pointerEvents="none">
        {labelSim.dots.map((dot, i) => (
          <g key={"dot" + i}>
            <line x1={point.x} y1={point.y} x2={dot.x} y2={dot.y} stroke={labelSim.results[i].color} strokeWidth="0.8" strokeDasharray="2,2" opacity="0.45" />
            <circle cx={dot.x} cy={dot.y} r="2.5" fill={labelSim.results[i].color} opacity="0.8" />
          </g>
        ))}
        {labelSim.results.map((result, i) => {
          const label = labelSim.labels[i];
          const dot = labelSim.dots[i];
          return (
            <g key={"text" + i}>
              <line x1={dot.x} y1={dot.y} x2={result.x} y2={result.y} stroke={result.color} strokeWidth="0.4" opacity="0.4" strokeDasharray="1,2" />
              <text x={result.x} y={result.y + 2} fontSize="6" fontWeight="bold" fill={result.color} textAnchor="middle" style={{ paintOrder: "stroke", stroke: "#fff", strokeWidth: 2.5 }}>
                {result.text}
              </text>
              <line x1={result.x} y1={result.y} x2={label.x} y2={label.y} stroke={label.color} strokeWidth="0.4" opacity="0.4" />
              <text
                x={label.x} y={label.y + 2} fontSize="6" fill={label.color} textAnchor="middle"
                style={{ paintOrder: "stroke", stroke: "#fff", strokeWidth: 2.5 }}
              >
                {label.text}
              </text>
            </g>
          );
        })}
        </g>
      </svg>
      </div>

      <div className="flex flex-row items-start justify-center gap-8 w-full flex-wrap mt-4">
      <div className="flex flex-col gap-2 text-xs min-w-[160px] max-w-[220px]">
        <div className="font-bold text-neutral-700">Legend</div>
        {["Potential", "Anti-potential", "Active", "Suppressive"].map((group) => (
          <div key={group} className="flex flex-col gap-1">
            <div className="text-xs font-semibold text-neutral-500">{group}{arms.find(a => a.group === group)?.dash ? " (dashed)" : " (solid)"}</div>
            {arms.filter(a => a.group === group).map((a, i) => (
              <div key={group + i} className="flex items-center gap-2">
                <span
                  className="inline-block w-6 h-0"
                  style={{
                    borderTop: `2px ${a.dash ? "dashed" : "solid"} ${a.color}`,
                  }}
                />
                <span style={{ color: a.color }}>{a.label}</span>
              </div>
            ))}
          </div>
        ))}
        <div className="flex flex-col gap-1 pt-2 border-t border-neutral-100">
          <div className="text-xs font-semibold text-neutral-500">Edges (full-length 0-100, both ends)</div>
          <div className="flex items-center gap-2"><span className="inline-block w-6 h-0 shrink-0" style={{ borderTop: "2px solid #0a7a3a" }} /><span style={{ color: "#0a7a3a" }}>Good edge</span></div>
          <div className="flex items-center gap-2"><span className="inline-block w-6 h-0 shrink-0" style={{ borderTop: "2px solid #7a1f1f" }} /><span style={{ color: "#7a1f1f" }}>Bad edge</span></div>
          <div className="flex items-center gap-2"><span className="inline-block w-6 h-0 shrink-0" style={{ borderTop: "2px solid #666" }} /><span className="text-neutral-500">Mix (center)</span></div>
        </div>
      </div>

      <div className="flex flex-col gap-0.5 text-[11px] text-neutral-700 min-w-[190px] leading-tight">
        <div className="font-bold text-neutral-700 text-sm mb-1">Readout</div>
        <div className="flex justify-between font-mono border-b border-neutral-100 pb-1 mb-1">
          <span>υ {(((185 - point.x) / ((frame.right - frame.left) / 2)) * 100).toFixed(0)}</span>
          <span>ψ {(((frame.midY - point.y) / (frame.midY - frame.top)) * 100).toFixed(0)}</span>
        </div>
        <div className="font-semibold text-neutral-500">Arms [dir, mag]</div>
        {arms.map((a, i) => {
          const v = closestOn(a);
          return (
            <div key={i} className="flex justify-between" style={{ color: a.color }}>
              <span>{a.group.slice(0, 9)}→{a.label.slice(0, 6)}</span>
              <span className="font-mono">[{v.dir.toFixed(0)},{v.mag.toFixed(0)}]</span>
            </div>
          );
        })}
        <div className="font-semibold text-neutral-500 mt-1">Edges [dir, mag]</div>
        {edgeAxes.map((e, i) => {
          const v = closestOn(e);
          return (
            <div key={i} className="flex justify-between" style={{ color: e.color }}>
              <span>{e.from.slice(0,6)}↔{e.to.slice(0,6)}</span>
              <span className="font-mono">[{v.dir.toFixed(0)},{v.mag.toFixed(0)}]</span>
            </div>
          );
        })}
      </div>
      </div>

      <div className="w-full max-w-3xl mt-6 border-t border-neutral-200 pt-4">
        <div className="font-bold text-neutral-700 mb-2">Evidence Log</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(evidenceLog).map(([corner, sets]) => (
            <div key={corner} className="text-xs border border-neutral-200 rounded p-2">
              <div className="font-semibold text-neutral-700 mb-1">{corner}</div>
              {["stated", "verified"].map((kind) =>
                sets[kind].length > 0 ? (
                  <div key={kind} className="mb-2">
                    <div className="text-neutral-500 font-semibold capitalize">{kind}</div>
                    {sets[kind].map((item, idx) => (
                      <div key={idx} className="flex gap-1 py-0.5">
                        <span className="font-mono text-neutral-400">S={item.s.toFixed(1)}</span>
                        <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-blue-700 underline hover:text-blue-900">
                          {item.text}
                        </a>
                      </div>
                    ))}
                  </div>
                ) : null
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
