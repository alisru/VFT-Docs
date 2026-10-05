---
title: "Modal Vector Matrix"
chat_id: "gemini-d08d1f25bc6c4079"
chat_title: "Mapping Modal Verbs Geometrically - Google Gemini"
chat_url: "https://gemini.google.com/app/bef2c048f6f0120d?utm_source=app_launcher&utm_medium=owned&utm_campaign=base_all"
type: "code"
updated: "2026-10-05T11:33:18.118534+00:00"
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Modal Auxiliary Linear Map</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus
  +Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      user-select: none;
    }
    .mono {
      font-family: 'JetBrains Mono', monospace;
    }
    .node-pt {
      cursor: pointer;
    }
    .node-pt circle.dot {
      transition: r 0.18s cubic-bezier(0.34, 1.56, 0.64, 1), stroke-width 0.18s ease;
    }
    .node-pt:hover circle.dot {
      r: 9;
      stroke-width: 3.5;
    }
    .active-dot circle.dot {
      r: 9.5;
      stroke-width: 3.5;
      filter: drop-shadow(0 0 10px rgba(251, 191, 36, 0.95));
    }
    .axis-track {
      transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
  </style>
</head>
<body class="bg-[#090d16] text-slate-100 min-h-screen flex flex-col items-center p-3 sm:p-6 antialiased">

  <header class="w-full max-w-4xl flex flex-wrap items-center justify-between gap-3 pb-4 mb-3 border-b
