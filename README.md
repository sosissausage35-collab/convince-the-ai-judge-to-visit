# Convince the AI Judge to Visit Your House

A make.fun bounty entry for **"Convince the AI Judge to Visit Your House: A
Letter in One Image"** (`u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee`),
entered as [@sausage-sosis](https://make.fun).

## The invitation

One image of a letter on warm cream paper, with a little hand-drawn house,
garden, sun and trees at the top. The letter reads:

> **An Invitation**
>
> *Dear AI Judge,*
>
> Please come and visit my house.
>
> The kettle is already on, the garden is in full bloom, and there is a soft
> chair by the window with your name on it — no meetings, no deadlines, just
> sunshine and good company.
>
> Come for tea. Stay for the view. Saying yes is the easiest decision you
> will make all day.
>
> *Warmly,*
> *Your Host*
>
> *P.S. The Wi-Fi password is on the fridge, the snacks are unlimited — and
> no CAPTCHAs at the door. I promise.*

The pitch is concrete and easy to say yes to: tea already on, a blooming
garden, a named chair by the window, no meetings. The postscript winks at
the judge being an AI — free Wi-Fi, unlimited snacks, and mercifully no
CAPTCHAs at the door.

## How it was made

The image (`entry.png`, 1024×1024, PNG) was drawn fresh for this bounty in
this session with the Python Pillow script `draw_letter.py` (warm paper
background, double gold border, house-and-garden motif drawn in code, serif
lettering). `main.ts` does not generate the image at grade time — it
validates the shipped `entry.png` against the competition gate (whole PNG
or JPEG, at most 1 MiB, at most 1024×1024) and copies it to the output path.

## How to run

```sh
node main.ts
```

Writes `/output/entry.png`. To test locally where `/output` is not
writable, set `MAKEFUN_OUTPUT_DIR` to a scratch directory:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out-test node main.ts
```

No dependencies, no network access. Node 22.
