# Work Rate Math

Combined work rate arithmetic. A 6-hour worker and a 3-hour worker finish one job in 2 hours, not 4.5.

## What it computes

- **The together truth** - how long 2 to 6 workers take on one job, from each worker's time alone.
- **The other truth** - one worker's time alone plus the time together gives the other worker's time alone.
- **The pipe truth** - an inlet that fills a tank and an outlet that drains it, both open: time to fill an empty tank, time to empty a full one, or "cancel out" when they match.

Times are in hours, up to 2 decimals, from 0.01 to 10000. Each worker or pipe is assumed to keep one steady rate (1 divided by the time alone). Arithmetic is exact with fractions. Figures are rounded to 2 decimals, half up, and marked "exactly" or "about"; the nearest minute is given too.

## Boundary

Arithmetic only. It does not know about slowdowns, handoffs, setup time or whether the numbers you typed are right. Check those where they apply.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (48 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/workrate/
Repo: https://github.com/iLanis-agent/workrate
