// The Daily Globe - 20 November 2026 (v6 entrypoint).
// Node 22, stdlib only. Copies the rendered front page (entry.png)
// into the directory make.fun expects for this bounty.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outputDir, "entry.png"));

// v6: full winners' formula -- 35 numbered stories, Friday-first lead
// (Kyiv bridges, not the Thursday-first ICJ verdict), numbers strip,
// region bar, 3 illustrated leads + 10 illustrated secondaries,
// dotted world map with numbered pins, ALSO ON FRIDAY list, date-check
// box, per-story sources. Rendered by render.py; two runs write
// byte-identical entry.png. Verify with: python3 render.py twice and
// compare sha256sums before committing.
