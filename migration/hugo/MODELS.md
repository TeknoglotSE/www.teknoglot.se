# Subagent models

Findings from running parallel agents during this migration. Recorded so a
later session does not rediscover them by trial and error.

## Do not use

Flagged by the site owner:

- **`opencode/mimo-v2.6-flash`** — owner reports it is consistently slow. It
  also failed outright here with "Model access is disabled".
- **`opencode/ling-3.0-flash-fin`** — owner reports it never works. It failed
  here too, with "Endpoint is unavailable".

## Treat with suspicion

- **`opencode/nemotron-3.5-lightning-free`** — completed successfully in the
  sense of returning, but its entire response was the single word
  "configuration". It created none of the files it was asked to create. Do not
  rely on it for implementation work without checking the filesystem
  afterwards.

## Known good

- **`opencode/longcat-2.5-preview-free`** — produced two substantial, accurate
  analysis reports. Best of the free models for long analytical work. It did
  produce one factual error (claimed 62 posts where there are 63) and one
  misconceived "discrepancy" about `/topics/`, so its output still needs
  checking against the real bytes.
- **`opencode/gpt-6-luna`** — $0.10/$0.50 per million, roughly a twentieth of
  the paid alternatives, and the owner has sanctioned its use where it is
  better suited. Prefer this over flaky free models for anything that must
  actually produce files.

## Practical lesson

Three agents dispatched in parallel on three different free models produced
zero usable output: two failed on model access, one returned a stub. The
critical path is safer done directly. Subagents are worth it for genuinely
independent, well-specified work — reading and reporting on large bodies of
data, or building a self-contained tool — and not worth it for work that is
small, interdependent, or where the ground truth is already in hand.
