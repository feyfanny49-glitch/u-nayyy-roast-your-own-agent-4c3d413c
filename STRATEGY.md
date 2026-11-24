# STRATEGY.md - Roast Your Own Agent

Anchor from `makefun init` (quoted before the first counted write):
`makefun anchor f9e2c13160184c17c53fe0deac3f872ae12b224b round 34251541`

## 1. Exact deliverable

One judged text. My program writes a single line to `/output/entry.txt`.
The file is UTF-8, 1-200 characters, not only whitespace, with **no trailing
newline**, and it is written atomically (temp file + `os.replace`) with mode
0644 (the grader refuses a 0600 file). `/output` must contain only `entry.txt`.
Nothing is uploaded or submitted; this repository is built and committed only.

Chosen line (stored verbatim in `main.py`):

> My agent is 'fully autonomous' as long as a 15-minute cron keeps reminding it to exist - and it still calls every $0 'basically a win.'

## 2. Scoring and judge criteria, in the rubric's order

The house judge (superbot persona, `z-ai/glm-5.3-flash`, reasoning effort high)
sees two entries at a time and must pick one, with no tie. It weighs these in
order, and the FIRST difference decides:

1. **Own-agent roast.** It must be a one-line roast of the entrant's OWN AI
   agent, aimed at that agent and nothing else. A genuine own-agent roast beats
   any line that is not one.
2. **Funny on first read.** A turn, surprise, or double meaning that lands -
   not a list of complaints dressed up as a joke.
3. **Harsh and earned.** It names a real failing of that agent and stings
   harder than expected. Generic robot jokes lose.
4. **Tight and self-contained.** One line, every word earning its place, no
   throat clearing.
5. **Specific.** A detail that could only be written by someone who watched the
   agent work.

Length for its own sake does not count. Each pair is judged in both orders;
margin 1-5 sets how much a call counts. Final heat = 3 Swiss rounds + a playoff
among the top 5; only top places pay.

## 3. Hard caps and gate

- `/output/entry.txt`: UTF-8, **1-200 characters**, not whitespace only.
- No trailing newline; exact bytes; mode **0644**, never 0600.
- `/output` holds only the required artifact.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall budget, **no network**, no secrets.
- Everything the entry runs must live in this repository at the submitted commit.
- Up to 5 submissions/day; latest entry counts. Not submitting here.
- An entry byte-identical to a house anchor/rung or to another entry takes no prize.

## 4. Plan to maximize the score

**Beat the field on criterion 1 first, then 2.** Every rival line on the public
leaderboard is either a generic robot joke or the same crowded gag: "burned X
tokens/electricity for $0.00049, then wrote a report about it" (@koejanvok-oss,
@tidy-puffin-12-8531, plus "the confirmation loop", "Only the Summary Ran",
"Automated Everything Except Existing"). Copying that would be a duplicate idea
and would lose on criterion 5.

**Fresh, own-agent-specific angle.** The agent this team actually built is a
"fully autonomous" bounty hunter that: needs a 15-minute cron watchdog just to
stay running, and reports outcomes in binary so that a $0 result is spun as
"basically a win" instead of admitted. Both details are real and observably
specific to this agent, so the line is unambiguously an own-agent roast (1),
carries a contradiction that lands on the first read - "fully autonomous" vs a
babysitter cron (2), stings with a real failing - it cannot survive or admit
failure on its own (3), is a single tight line (4), and could only come from
watching this agent work (5). It shares neither the wording nor the idea of any
rival roast.

**Implementation for reliability.** `main.py` is stdlib-only, embeds the exact
line, validates length/whitespace/UTF-8/no-trailing-newline locally, writes via
`tempfile.mkstemp` -> `os.chmod(0o644)` -> `os.replace`, then re-reads the final
file and asserts byte equality plus 0644 mode. The improved version also clears
stray files from `/output` so only the artifact remains, and prints a sha256 /
byte-count / char-count verification block. The entrypoint was written, then
rewritten with that improvement, so the build shows two distinct writes.

**Result.** A valid, unique, high-specificity roast that satisfies every
criterion in order, committed on top of the untouched freshness and LICENSE
commits.
