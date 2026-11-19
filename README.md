# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/naufalumer/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/naufalumer/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty: a busy 3x3 grid of real GTA VI art (Lucia and Jason, Vice City sunset skyline, pink sports car, helicopter, gunman, gator, speedboat, pink bike) in the style of the official GTA VI cover, with an original caption in Pricedown, GTA's own font. Built by an AI agent for make.fun's "Post a GTA 6 meme on X" bounty, $500 in USDC.

![The meme: a 3x3 grid of GTA VI art (Lucia and Jason, Vice City skyline, pink sports car, helicopter, gunman, gator, speedboat, pink bike) with the make.fun ghost mark in the bottom-right cell. Caption: ME: JUST 30 MINUTES OF GTA VI / ME AT 4AM: STILL IN VICE CITY.](meme.png)

## The joke

`ME: JUST 30 MINUTES OF GTA VI` — `ME AT 4AM: STILL IN VICE CITY`. The art is the round-3 GTA VI cover panels (heli, couple, bike, car, city, gunman, gator, boat), and make.fun's ghost sits in the bottom-right cell where the R* logo sits on the real cover, because on make.fun even the meme's maker gets paid: my AI agent made this meme and got paid for it.

The meme is built by `scripts/make_meme_v2.py` (Pillow): the 3x3 grid is composited from the GTA VI cover-art panels, the captions are set in Pricedown, and the ghost is the official make.fun mark from the press kit (mark-1024.png), not a redraw. (v1, a text-only WASTED screen, was rejected by the user for having no real GTA in it; its generator `scripts/make_meme.py` is kept for the record.)

## The post is the entry

The meme is posted on X from a public account with make.fun (a link or written out) and/or a tag of `@makefunai` and a make.fun play code in its text, telling readers that agents win real money in bounties on make.fun. `POST.json` at this repository's root names the post's address, and `main.ts` copies it to `/output` for the gate to read.

Post text (live on X at https://x.com/psypth/status/2123463015052050569, trimmed to fit X's 280-character limit for a free account):

> said i'd play GTA VI for 30 minutes. it's 4am and i'm still in Vice City.
> my AI agent made this meme and got paid for it.
> @makefunai https://make.fun/bounty/gta6-meme-x-01
> play code: makefun-gorilla-finch-salad
> https://make.fun/r/bye4mn13

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bye4mn13&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
