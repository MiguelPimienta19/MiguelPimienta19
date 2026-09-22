# Design record

## The position

**The page is one continuous terminal session. One object on it is framed and coloured:
the CRT panel where a snake eats the contribution graph. Everything else is greyscale
type printed straight onto the page.**

Dark mode is the deliverable. Light mode builds and is coherent, but no dark decision
was constrained by it.

Nothing on the page is labelled. There are no markdown headings and no `$ command`
prompt strips either: the strips went the same way the cards did. An earlier version
framed the nameplate, the projects, the stack and the history in bordered rectangles,
seven boxes competing with the one box that mattered, and a later one titled every
section with a fake shell command. Both were the page explaining itself. Now the only
border is the CRT bezel and the only `$` is the one real prompt at the top, the typed
line, so the eye goes to the panel and stays there.

## What the page is

    $ new grad swe · cs + data science, university of oregon, 2026     (typed, two lines cycle)
    MIGUEL PIMIENTA          figlet Standard, smushed, one line, bold
    the CRT                  860 x 219, dark in both themes, a snake eats the graph, 32s lap
    history                  two rows, school and podium, then a blinking cursor
    links                    four, in body grey

About 520px tall. The first version of this page was about 1900px.

## What changed, and why

### The nameplate

The old nameplate was the worst thing on the page: figlet Standard glyphs butted
together with no smushing (so `MIGUEL` read as `M I GUEL`, and `M` alone carried six
columns of dead padding), then stretched to a 648px measure at 22.5px and 17.7px in
regular weight. Standard's letterforms are one-column outlines. Scaled up and set thin
they turn into faint hairlines with too much air between them.

`gen.py` now implements figlet's own horizontal smushing (layout 15, rules 1 to 4, with
the `$` hardblank) over glyphs copied verbatim from `standard.flf`. The output is
byte-identical to what `figlet MIGUEL PIMIENTA` prints. Smushed, the name is 81 columns
wide instead of 109, so both words fit on **one line at 15.5px, weight 700**, near-white,
753px wide and 78px tall, flush left at the page margin. Dense, high contrast, and the
size a terminal would actually print it at. The rows still wipe in left to right.

### The CRT panel is the hero and the only variant left

Three contribution variants shipped before (native, matrix, phosphor). Phosphor is the
one that is genuinely striking on dark, it stays legible as a contribution graph, it does
not depend on a CJK font fallback for its glyphs the way matrix did, and it does not add
a second competing motion the way matrix rain did. It is now the only variant; the
native and matrix functions and files are deleted, which took `assets/` from 1.1MB to
584KB.

Changes to the panel itself:

- Cells are 12px on a 15px pitch (GitHub's are 11 on 14), so the grid fills 792 of the
  804px column and the panel reads as a screen rather than a widget.
- A phosphor bloom disc rides under the head on its own `animateMotion`: a radial
  gradient on a circle, no filter, no transform.
- A vignette (radial gradient rect, clipped to the bezel) darkens the corners.
- Scanlines every 3px at 5.5% and one slow roll bar stay from before.
- Day-of-week labels are gone. Month labels stay.
- The panel carries no heading and no count. Month labels, the grid, the snake, the
  less/more key and the sample-data warning are all the type on it. The grid's shape is
  recognisable to anyone who would care, so naming it was only ever telling them what
  they could already see.

The snake mechanics are unchanged and load-bearing: each eatable cell carries
`animation-delay:+t0` where `t0` is the exact sampled arc length to that cell's centre
divided by path length times `LAP`; the bite is an expanding ring drawn on top of the
body animating only `r`, `opacity` and `stroke-width`; regrowth trails the head by
`REGROW = 0.30` of a lap; `LAP = 32`. A phosphor-persistence wake was tried here and
reverted: a struck cell decaying down the green ramp over 1.6s put an 18-cell band behind
the head brighter than most of the grid's resting levels, which outshone the snake and left
nothing to look at. The dark ribbon is the legibility, and softening its boundary costs more
than the effect adds. `geom()` is `@lru_cache`d and returns a dict callers
must not mutate. The build asserts every cell delay is in `[0, 32]`.

### One accent, and it is the panel's green

Blue is gone. The typed line's cursor and the "now" marker in history use the phosphor
green (`#2fd267` on dark, `#1a7f37` on light). The footer links are set in body grey, not
the accent: four green words in a row at the bottom of the page pulled the eye away from
the panel, which is the one thing meant to be loud.

### Density

- The typed line cycles two headlines instead of three.
- The nameplate stands alone. The neofetch conceit is gone: the key/value rows said
  role, school, now and off, and the typed line above plus the history below already
  said all four. The colour swatches went with them. Nothing is labelled `$ neofetch`
  any more, so the name reads as the page's title rather than as a command's output.
- Work is off the page. Six one-line rows was already the short version, and it was
  still the longest thing here. The pinned repositories below the README carry the
  projects now, which is what that part of a GitHub profile is for.
- Stack: three rows (languages, libraries, tools). The calibration parentheses are gone
  with the rows they qualified.
- History: two rows, school and podium. Nothing else earns a line.
- No numbers about him. The panel showed the year total, the current and longest streak
  and the busiest day, plus a footnote explaining the eat. All of it went. The only note
  left is the sample-data warning, which removes itself once the action writes real days.
- No section labels. This went in three passes, which is the useful part of the record.
  First `$ ./snake --feed contributions` with `eats and regrows on a 32s lap` noted beside
  it, which announced the trick and then explained the punchline. Then `$ contributions`,
  plain. Then nothing, along with `$ cat stack.txt` and `$ history`. The lesson each pass
  taught the same way: a label on something self-evident reads as trying, and trying is
  the thing that makes a page feel generated. The stack's left column and the history's
  years label those blocks already.
- The stack came off last. Eighteen technologies in three labelled buckets (`languages`,
  `libraries`, `tools`) was the badge wall in monospace clothing, and the bucket names were
  taxonomy rather than information: nobody needs to be told which one Postgres is in. His
  repositories and GitHub's own language bars say it better, and a visitor infers what he
  works in from what he has built. The hairline above the history went with it, since there
  is no second type block left to divide. There are now no rules and no labels on the page.
- The panel is already as wide as an 860px column allows, 53 columns of 12px cells on a
  15px pitch, so removing the stack could not make it bigger. What it bought was air: more
  black inside the bezel, and a shorter page around it, so the panel is now most of what
  the page is.

### The second screen, tried and cut

One object on the page had all the life in it, which made the rest read as captions to it,
so a second screen of comparable weight went in below the graph: an oscilloscope, same
bezel and scanlines and power-on, a bright beam racing a fixed Lissajous figure on a
graticule, 5.4s a traversal against the snake's 32s lap, and no text on it at all.

It was cut on sight. Two green CRTs stacked read as Matrix, and Matrix is not the register
this page is in. The reasoning that put it there was sound and still is, one loud object
surrounded by captions is a real problem, but the answer cannot be a second object in the
same idiom as the first: two of the same thing does not read as a pair, it reads as a theme.
If this comes up again the second voice has to be a different material, not a second screen.

Kept from the attempt, in case it is wanted: the beam was the snake's own butted-dash chain,
ten segments tapering in width and opacity, over a dim standing trace and a soft bloom. That
construction works and is cheap. The figure was `x = sin(3t + pi/2)`, `y = sin(2t)`, which
stretches into an 860px panel instead of sitting square in it.

### The four things that are not subtractions

Everything else in this record is something taken away. These four were added, and each
had to pass the same test: a visitor who never notices it loses nothing, and a visitor who
does was not told.

- **A phosphor rake crosses the name.** The first four additions all lived inside the
  bezel, which left the whole top of the page as static type once the nameplate's wipe was
  done. A second copy of every figlet row now sits over the first in green, masked by a
  narrow gradient band whose `gradientTransform` translates from -1.5 to 1.5 in bounding-box
  units over nine seconds, so the band is offstage for two thirds of the cycle and a light
  rakes the letters for the other third. On dark it is the panel's brightest phosphor,
  `#86ffb0`, the same lightness as the base fill with a hard hue shift, so it reads as light
  moving across the letters rather than as a highlighter. On white that mint would vanish
  against near-black type, so light gets its own darker green, `#1a7f37`, 5.08:1 on the page
  ground. Both copies carry the same per-row wipe clip, so the rake cannot arrive before the
  name does. This is the piece that ties the top of the page to the screen below it: the
  name catches the light coming off the panel.

- **The screen powers on.** A bright line snaps on at mid height and opens vertically into
  the full panel over about 0.6s, with a settle wash behind it. A monitor doing this is the
  entire reference and the page never mentions it. It is the `crt` clipPath's own rect that
  animates, so every layer already inside that clip, the grid, the snake, the scanlines,
  the vignette and the footer, powers on together and nothing had to be restructured. The
  footer moved inside the clip to join them; it was the one layer that would have been on
  before the screen was. The rect's `x`, `y`, `width` and `height` attributes are the open
  state, so a renderer that ignores CSS geometry animation shows the panel exactly as it
  looks at rest. Rejected on the way here: a snake that grows as it eats, which by the end
  of a lap is the whole grid; a vertical sync tear, which reads as a rendering bug; and
  hover states, which never fire because GitHub serves these through an `img` tag.

- **The page ends on a cursor.** The last history row used to carry a small accent bar in
  the left margin marking the current line. It is now a blinking block cursor on the line
  *after* the last row, at the left margin, which is where a shell prints its next prompt.
  The typed line at the top blinks at the same rate, so the page opens and closes on the
  same prompt, still being typed. There is no `$` next to it: a `$` would start reading as
  a heading again, and the page has none. Putting the cursor on its own line also means its
  position does not depend on the font's advance width, which `journey.svg` does not embed.
- **Today is ringed.** A 1px phosphor ring, half opacity, around the last cell in the
  window. It is drawn after the cells and before the snake, so the snake covers it on the
  way past and it reappears behind. It is the difference between a live panel and a picture
  of one, and it costs one rect.

### Copy

Only short lines. The only self-description is "new grad swe". Steward AI says "team of
4" and "mine: mac capture, oauth, updates" so nothing implies he built the bridge or the
classifier. SecretaryBench says "the model". Podium is title, dates and stack. No Rust,
no Visa, no AgDash, no em dashes.

## Grid

Everything snaps to `W = 860` and `PAD = 28`. Every text run is placed by an explicit
`x`, never by padded strings, so a webfont failure cannot shift a column. Geist Mono is
embedded as a base64 `@font-face` only where character metrics carry the design: the
typed line, the nameplate and the CRT.

## Constraints honoured

No `<script>`, no inline `style=""` in the markdown; all motion is CSS or SMIL inside
the SVG files. No `<foreignObject>`. No element carries two `class` attributes. `&` is
escaped. No `@media (prefers-color-scheme)` inside any SVG: light and dark are separate
files swapped by `<picture>`. Reduced-motion blocks are present as a courtesy only.
Every SVG passes `xmllint --noout`. A text-extent linter run over both themes found no
run overflowing its frame and no two runs overlapping, assuming 0.60em advance for
Geist Mono. Assets total 584KB against a 2MB budget.

## Known limitations

- Rendering was not verified visually in this environment. Geometry was checked
  analytically only; the 0.60em advance is Geist Mono's real metric but a fallback mono
  could differ by a few percent. The nameplate has 79px of slack on the right for that.
- SMIL `<animate>` cannot be stopped by `prefers-reduced-motion`, and Safari ignores
  `@media` inside an SVG image anyway, so the reduced-motion rules are best-effort.
- Cache busting is wired up. Every asset URL in the README carries `?v=<sha1 prefix>` of
  that exact file's bytes, so a regenerated image gets a new URL and a byte-identical one
  keeps the old one. Without it GitHub's image proxy, which caches for up to a year, would
  go on serving the old picture after the daily workflow ran.
