#!/usr/bin/env node
/*
 * Capture authorized routes with Playwright.
 *
 * The runner records screenshots and a runtime_media_probe snapshot for each
 * viewport/reduced-motion combination. It never logs in, clicks destructive
 * controls, or bypasses access controls.
 */

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

function parseArgs(argv) {
  const args = { config: null, output: "artifacts/browser-capture", headed: false, help: false };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--config") args.config = argv[++index];
    else if (value === "--output") args.output = argv[++index];
    else if (value === "--headed") args.headed = true;
    else if (value === "--help" || value === "-h") args.help = true;
    else throw new Error("Unknown argument: " + value);
  }
  return args;
}

function printHelp() {
  console.log([
    "Usage: node skill/scripts/capture_browser.mjs --config CONFIG [--output DIR] [--headed]",
    "",
    "CONFIG contains targets, viewports, reduced_motion, wait_ms and full_page.",
    "Each target URL may be HTTP(S), file://, or a repository-relative path.",
  ].join("\n"));
}

function safeName(value) {
  return String(value || "capture")
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 96);
}

function resolveUrl(value) {
  const raw = String(value || "");
  if (/^(https?:|file:)/i.test(raw)) return raw;
  return pathToFileURL(path.resolve(raw)).href;
}

function viewportValue(viewport) {
  return {
    width: Number(viewport.width),
    height: Number(viewport.height),
    deviceScaleFactor: Number(viewport.device_scale_factor || viewport.dpr || 1),
  };
}

async function loadPlaywright() {
  try {
    const require = createRequire(path.resolve(process.cwd(), "package.json"));
    return require("playwright");
  } catch (error) {
    console.error("Playwright is required for browser capture.");
    console.error("Install the pinned dependency with: npm install");
    console.error(String(error));
    process.exitCode = 3;
    return null;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }
  if (!args.config) throw new Error("--config is required");

  const config = JSON.parse(await readFile(args.config, "utf8"));
  const targets = Array.isArray(config.targets) ? config.targets : [];
  const viewports = Array.isArray(config.viewports) ? config.viewports : [];
  const reducedStates = Array.isArray(config.reduced_motion) ? config.reduced_motion : [false, true];
  if (!targets.length) throw new Error("config.targets must contain at least one target");
  if (!viewports.length) throw new Error("config.viewports must contain at least one viewport");

  const playwright = await loadPlaywright();
  if (!playwright) return;
  const { chromium } = playwright;
  const outputDir = path.resolve(args.output);
  await mkdir(outputDir, { recursive: true });
  const probeSource = await readFile(new URL("./runtime_media_probe.js", import.meta.url), "utf8");
  const executablePath = process.env.BROWSER_EXECUTABLE_PATH || chromium.executablePath();
  const browser = await chromium.launch({ headless: !args.headed, executablePath });
  const captures = [];
  const errors = [];
  const waitMs = Number(config.wait_ms || 350);
  const networkIdleTimeout = Number(config.network_idle_timeout_ms || 12000);

  try {
    for (const target of targets) {
      const targetName = safeName(target.name || target.url);
      const targetUrl = resolveUrl(target.url || target.path);
      for (const viewport of viewports) {
        const viewportInfo = viewportValue(viewport);
        for (const reducedMotion of reducedStates) {
          const viewportName = safeName(viewport.name || (viewportInfo.width + "x" + viewportInfo.height));
          const stateName = reducedMotion ? "reduced-motion" : "normal-motion";
          const captureName = targetName + "--" + viewportName + "--" + stateName;
          const screenshotName = captureName + ".png";
          const screenshotPath = path.join(outputDir, screenshotName);
          const context = await browser.newContext({
            viewport: { width: viewportInfo.width, height: viewportInfo.height },
            deviceScaleFactor: viewportInfo.deviceScaleFactor,
            reducedMotion: reducedMotion ? "reduce" : "no-preference",
            colorScheme: target.color_scheme || config.color_scheme || "dark",
          });
          const page = await context.newPage();
          const pageErrors = [];
          const requestFailures = [];
          page.on("pageerror", (error) => pageErrors.push(String(error)));
          page.on("requestfailed", (request) => requestFailures.push({
            url: request.url(),
            error: request.failure()?.errorText || "request failed",
          }));
          const startedAt = new Date().toISOString();

          try {
            const response = await page.goto(targetUrl, {
              waitUntil: "domcontentloaded",
              timeout: Number(config.navigation_timeout_ms || 30000),
            });
            await page.waitForLoadState("networkidle", { timeout: networkIdleTimeout }).catch(() => {});
            await page.waitForTimeout(waitMs);
            const probe = await page.evaluate((source) => {
              const factory = new Function("return (" + source + ");");
              return factory();
            }, probeSource);
            const pageInfo = await page.evaluate(() => ({
              title: document.title,
              lang: document.documentElement.lang || null,
              headings: [...document.querySelectorAll("h1,h2,h3")].slice(0, 40).map((node) => node.textContent.trim()),
              interactive_count: document.querySelectorAll("a,button,input,select,textarea,[tabindex]").length,
              media_count: document.querySelectorAll("img,video,audio,canvas,svg,iframe").length,
              focused: document.activeElement?.tagName || null,
            }));
            await page.screenshot({
              path: screenshotPath,
              fullPage: config.full_page !== false,
              animations: "allow",
            });
            captures.push({
              id: captureName,
              target: targetName,
              url: targetUrl,
              viewport: {
                name: viewport.name || viewportName,
                width: viewportInfo.width,
                height: viewportInfo.height,
                dpr: viewportInfo.deviceScaleFactor,
              },
              reduced_motion: reducedMotion,
              state: stateName,
              started_at: startedAt,
              finished_at: new Date().toISOString(),
              response_status: response?.status() || null,
              screenshot: screenshotName,
              page: pageInfo,
              page_errors: pageErrors,
              request_failures: requestFailures,
              probe,
            });
          } catch (error) {
            const failure = {
              id: captureName,
              target: targetName,
              url: targetUrl,
              viewport: viewportInfo,
              reduced_motion: reducedMotion,
              state: stateName,
              error: String(error),
              page_errors: pageErrors,
              request_failures: requestFailures,
            };
            captures.push(failure);
            errors.push(failure);
          } finally {
            await context.close();
          }
        }
      }
    }
  } finally {
    await browser.close();
  }

  const manifest = {
    schema_version: 2,
    tool: "capture_browser",
    generated_at: new Date().toISOString(),
    config,
    output_dir: outputDir,
    captures,
    summary: {
      total: captures.length,
      succeeded: captures.filter((item) => !item.error).length,
      failed: errors.length,
      page_errors: captures.reduce((total, item) => total + (item.page_errors || []).length, 0),
      request_failures: captures.reduce((total, item) => total + (item.request_failures || []).length, 0),
    },
  };
  await writeFile(path.join(outputDir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n", "utf8");
  console.log(JSON.stringify(manifest.summary, null, 2));
  if (errors.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exitCode = 1;
});
