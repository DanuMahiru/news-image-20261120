// The Daily Globe - 20 November 2026 (v4 entrypoint).
// Node 22, stdlib only. Copies the rendered front page (entry.png)
// into the directory make.fun expects.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outputDir, "entry.png"));

// Verified: two runs write byte-identical output, identical to entry.png.
