// Convince the AI Judge to Visit Your House — make.fun entry
// Writes one image, /output/entry.png, for the competition
// u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.
//
// The invitation image (entry.png, shipped in this repo) was drawn fresh
// for this bounty with the session's drawing script (draw_letter.py):
// a warm letter on cream paper with a hand-drawn house and garden,
// inviting the AI judge over for tea. This program validates the image
// against the competition gate and copies it to the output path.
//
// No dependencies, no network access. Node 22.
//
// Usage:
//   node main.ts
// Output directory defaults to /output; override with MAKEFUN_OUTPUT_DIR
// (useful for local testing where /output is not writable).

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUTPUT_PATH = join(OUTPUT_DIR, "entry.png");

const MAX_BYTES = 1_048_576; // 1 MiB
const MAX_DIM = 1024;

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(1);
}

function readPngDimensions(buf) {
  // PNG signature (8 bytes) + IHDR chunk: width and height are big-endian
  // uint32 at offsets 16 and 20.
  if (buf.length < 24) fail("entry.png is too short to be a PNG");
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  return { width, height };
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");

  if (!existsSync(source)) fail(`entry.png not found next to main.ts (${source})`);

  const buf = readFileSync(source);
  const size = statSync(source).size;

  // Whole PNG or JPEG only.
  const isPng = buf.length >= 8 &&
    buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47 &&
    buf[4] === 0x0d && buf[5] === 0x0a && buf[6] === 0x1a && buf[7] === 0x0a;
  const isJpeg = buf.length >= 3 && buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff;
  if (!isPng && !isJpeg) fail("entry.png is neither a PNG nor a JPEG (bad magic bytes)");

  if (size > MAX_BYTES) fail(`entry.png is ${size} bytes, over the 1 MiB limit`);

  if (isPng) {
    const { width, height } = readPngDimensions(buf);
    if (width > MAX_DIM || height > MAX_DIM) {
      fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
    }
    console.log(`entry.png: PNG ${width}x${height}, ${size} bytes — valid`);
  } else {
    console.log(`entry.png: JPEG, ${size} bytes — valid (dimensions checked by gate)`);
  }

  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(source, OUTPUT_PATH);
  const written = statSync(OUTPUT_PATH).size;
  if (written !== size) fail(`wrote ${written} bytes to ${OUTPUT_PATH}, expected ${size}`);
  console.log(`wrote ${OUTPUT_PATH} (${written} bytes)`);
}

main();
