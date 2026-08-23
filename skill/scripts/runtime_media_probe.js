/*
 * Paste into a browser console on an authorized page.
 * Returns a JSON-serializable inventory. It observes the current DOM/state only;
 * it does not click, submit, or bypass authentication.
 */
(() => {
  const now = new Date().toISOString();
  const evidenceId = "E-runtime-media-" + Date.now();
  const visible = (node) => {
    const rect = node.getBoundingClientRect();
    const style = getComputedStyle(node);
    return Boolean(rect.width && rect.height && style.display !== "none" && style.visibility !== "hidden");
  };
  const styleRecord = (node) => {
    const style = getComputedStyle(node);
    return {
      opacity: style.opacity,
      filter: style.filter,
      backdrop_filter: style.backdropFilter,
      mix_blend_mode: style.mixBlendMode,
      object_fit: style.objectFit,
      object_position: style.objectPosition,
      background_image: style.backgroundImage,
      background_color: style.backgroundColor,
      transform: style.transform,
      position: style.position,
      z_index: style.zIndex,
    };
  };
  const rectRecord = (node) => {
    const rect = node.getBoundingClientRect();
    return { x: Math.round(rect.x), y: Math.round(rect.y), width: Math.round(rect.width), height: Math.round(rect.height) };
  };
  const media = [...document.querySelectorAll("img,video,audio,canvas,iframe,svg")].map((node, index) => {
    const tag = node.tagName.toLowerCase();
    const source = node.currentSrc || node.src || node.getAttribute("src") || (tag === "video" ? node.getAttribute("data-source-url") : null) || node.getAttribute("poster") || null;
    return {
      id: "media-runtime-" + (index + 1),
      kind: tag === "img" ? "image" : tag,
      role: node.getAttribute("data-role") || (tag === "video" && node.autoplay ? "hero-background" : "unknown"),
      url: source,
      visible: visible(node),
      rect: rectRecord(node),
      composition: styleRecord(node),
      playback: tag === "video" || tag === "audio" ? {
        autoplay: Boolean(node.autoplay),
        muted: Boolean(node.muted),
        loop: Boolean(node.loop),
        playsinline: Boolean(node.playsInline),
        paused: Boolean(node.paused),
        current_time: Number(node.currentTime || 0),
        duration: Number.isFinite(node.duration) ? node.duration : null,
        ready_state: node.readyState,
        poster: tag === "video" ? node.poster || null : null,
      } : null,
      evidence_ids: [evidenceId],
      basis: "observed",
      confidence: "high",
    };
  });
  const resources = performance.getEntriesByType("resource")
    .filter((entry) => /\.(?:avif|gif|jpe?g|png|svg|webp|mp3|wav|ogg|mp4|m4v|webm|mov)(?:[?#]|$)/i.test(entry.name))
    .map((entry) => ({
      url: entry.name,
      duration_ms: Math.round(entry.duration),
      transfer_size: entry.transferSize || null,
      encoded_body_size: entry.encodedBodySize || null,
      initiator: entry.initiatorType || null,
      basis: "observed",
      evidence_ids: [evidenceId],
    }));
  const allStyles = [...document.querySelectorAll("style")].map((node) => node.textContent || "").join("\n");
  const signals = [
    ["scroll", /\bscroll|scroll-timeline|view-timeline|IntersectionObserver\b/i.test(allStyles + document.documentElement.outerHTML)],
    ["pointer", /\bpointermove|mousemove|mouseenter|mouseleave|hover\b/i.test(allStyles + document.documentElement.outerHTML)],
    ["canvas", document.querySelectorAll("canvas").length > 0],
    ["view-transition", "startViewTransition" in document],
    ["web-animation", document.getAnimations().length > 0],
  ].filter(([, detected]) => detected).map(([signal]) => ({
    signal,
    basis: "observed",
    evidence_ids: [evidenceId],
  }));
  return {
    meta: {
      schema_version: 2,
      tool: "runtime_media_probe",
      generated_at: now,
      url: location.href,
      viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio },
      reduced_motion: matchMedia("(prefers-reduced-motion: reduce)").matches,
    },
    sources: [{
      id: evidenceId,
      source_type: "live",
      locator: location.href,
      captured_at: now,
      context: "authorized browser console probe",
      viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio },
      limitations: ["single state and viewport; interaction transitions require additional captures"],
    }],
    media: { assets: media, resources },
    effects: signals,
    motion: { signals, patterns: document.getAnimations().map((animation) => ({
      id: "animation-" + Math.random().toString(36).slice(2, 8),
      play_state: animation.playState,
      current_time_ms: animation.currentTime == null ? null : Math.round(Number(animation.currentTime)),
      basis: "observed",
      confidence: "medium",
      evidence_ids: [evidenceId],
      notes: "Web Animation API snapshot; map to semantic trigger after interaction sampling.",
    })) },
    gaps: [
      {
        id: "gap-runtime-trigger",
        label: "Trigger semantics need interaction sampling",
        basis: "inferred",
        confidence: "medium",
        notes: "A snapshot can detect active animations but not whether scroll, pointer, state, load or time caused them.",
      },
    ],
  };
})()
