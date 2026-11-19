// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: a GTA 6 meme made by an AI agent, posted
// from a public X account with make.fun (a link or written out) and/or a tag
// of @makefunai and a make.fun play code in its text. This program only hands
// the post's address to the gate: it copies POST.json from the repository
// root to the output directory, where the house reads it and fetches the post
// from X. Nothing this program writes is judged.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// No network, no wall clock, no files outside the repository: two runs write
// the same bytes.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });

// Fail loudly on a POST.json that is not a JSON object naming a post URL,
// instead of copying garbage the gate would refuse anyway.
let post;
try {
  post = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf8'));
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof post !== 'object' || post === null || typeof post.url !== 'string'
    || !post.url.startsWith('http')) {
  console.error('POST.json must be a JSON object with a url string');
  process.exit(1);
}

try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`could not copy POST.json from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
