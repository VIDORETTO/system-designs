/*
 * Authorized-browser element picker.
 * Paste into the console, click one element, and copy the returned JSON.
 * It prevents the first click from activating the page action.
 */
(() => {
  const evidenceId = "E-element-picker-" + Date.now();
  const selectorPart = (node) => {
    if (!(node instanceof Element)) return "";
    const tag = node.tagName.toLowerCase();
    const id = node.id ? "#" + CSS.escape(node.id) : "";
    const classes = [...node.classList].slice(0, 3).map((name) => "." + CSS.escape(name)).join("");
    return tag + id + classes;
  };
  const ancestry = (node) => {
    const parts = [];
    let current = node;
    while (current && current instanceof Element && parts.length < 6) {
      parts.unshift(selectorPart(current));
      current = current.parentElement;
    }
    return parts.join(" > ");
  };
  const pick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    const node = event.target;
    const style = getComputedStyle(node);
    const rect = node.getBoundingClientRect();
    const media = node.matches("img,video,audio,canvas,svg,iframe") ? {
      kind: node.tagName.toLowerCase(),
      source: node.currentSrc || node.src || node.getAttribute("src") || node.getAttribute("poster") || null,
      poster: node.poster || null,
      autoplay: "autoplay" in node ? Boolean(node.autoplay) : null,
      muted: "muted" in node ? Boolean(node.muted) : null,
      loop: "loop" in node ? Boolean(node.loop) : null,
      playsinline: "playsInline" in node ? Boolean(node.playsInline) : null,
    } : null;
    const result = {
      meta: {
        schema_version: 2,
        tool: "runtime_element_picker",
        generated_at: new Date().toISOString(),
        url: location.href,
        viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio },
      },
      source: {
        id: evidenceId,
        source_type: "live",
        locator: location.href,
        captured_at: new Date().toISOString(),
        context: { state: "element-picked", viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio } },
        limitations: ["one selected state; pseudo-elements and hidden states require separate captures"],
      },
      element: {
        selector: ancestry(node),
        tag: node.tagName.toLowerCase(),
        role: node.getAttribute("role") || null,
        text: (node.innerText || "").trim().slice(0, 240),
        rect: { x: Math.round(rect.x), y: Math.round(rect.y), width: Math.round(rect.width), height: Math.round(rect.height) },
        typography: {
          family: style.fontFamily,
          size: style.fontSize,
          weight: style.fontWeight,
          line_height: style.lineHeight,
          letter_spacing: style.letterSpacing,
          color: style.color,
        },
        surface: {
          background: style.background,
          border: style.border,
          radius: style.borderRadius,
          shadow: style.boxShadow,
          opacity: style.opacity,
          filter: style.filter,
          transform: style.transform,
        },
        custom_properties: Object.fromEntries([...document.styleSheets].flatMap((sheet) => {
          try {
            return [...sheet.cssRules].flatMap((rule) => rule.style ? [...rule.style].filter((name) => name.startsWith("--")).map((name) => [name, getComputedStyle(node).getPropertyValue(name).trim()]) : []);
          } catch (_) { return []; }
        })),
        media,
        basis: "observed",
        confidence: "high",
        evidence_ids: [evidenceId],
      },
    };
    window.removeEventListener("click", pick, true);
    window.removeEventListener("keydown", escape, true);
    console.log(JSON.stringify(result, null, 2));
    return result;
  };
  const escape = (event) => {
    if (event.key === "Escape") {
      window.removeEventListener("click", pick, true);
      window.removeEventListener("keydown", escape, true);
      console.info("Element picker cancelled.");
    }
  };
  window.addEventListener("click", pick, true);
  window.addEventListener("keydown", escape, true);
  console.info("Element picker armed. Click one element or press Escape.");
  return { armed: true, evidence_id: evidenceId };
})()
