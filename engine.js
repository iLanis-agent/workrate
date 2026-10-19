// Work Rate Math engine - how long jobs take when workers (or pipes) combine.
// Mirrored by oracle.py; keep the op order identical.
// Times are typed in hours with up to 2 decimals, from 0.01 to 10000. Arithmetic is exact (big integer fractions).
// Each worker does a steady share of one job per hour, which is 1 divided by the time they need alone.

var TIME_ERR = "each time must be a positive number of hours with at most 2 decimals, from 0.01 to 10000";

// A typed time as hundredths of an hour.
function _t(text) {
  var t = typeof text === "string" ? text.trim() : "";
  var m = /^([0-9]+)(?:\.([0-9]{1,2}))?$/.exec(t);
  if (!m) throw new Error(TIME_ERR);
  var h = BigInt(m[1]) * 100n + BigInt((m[2] || "") + "00".slice((m[2] || "").length));
  if (h < 1n || h > 1000000n) throw new Error(TIME_ERR);
  return { text: t, h: h };
}

// A time n/d hours as text: the figure rounded to 2 decimals (half up) and the nearest minute.
function _time(n, d) {
  var s = (2n * n * 100n + d) / (2n * d);
  var fig;
  if (s === 0n) fig = "under 0.01";
  else {
    var frac = String(s % 100n);
    while (frac.length < 2) frac = "0" + frac;
    while (frac.length > 0 && frac.charAt(frac.length - 1) === "0") frac = frac.slice(0, -1);
    fig = ((n * 100n) % d === 0n ? "exactly " : "about ") + (s / 100n) + (frac ? "." + frac : "");
  }
  var m = (2n * n * 60n + d) / (2n * d);
  return fig + " h, or " + (m / 60n) + " h " + (m % 60n) + " min to the nearest minute";
}

function _list(items) {
  var parts = items.map(function (x) { return x.text + " h"; });
  if (parts.length === 1) return parts[0];
  return parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1];
}

// The together truth: several workers on one job.
function togetherTruth(times) {
  var tokens = (typeof times === "string" ? times : "").split(/[\s,]+/).filter(function (x) { return x !== ""; });
  if (tokens.length < 2 || tokens.length > 6) throw new Error("enter 2 to 6 times, " + TIME_ERR);
  var ts = tokens.map(_t);
  // rate per hour = 100/h each; sum as a fraction num/den
  var num = 0n, den = 1n;
  ts.forEach(function (x) { num = num * x.h + 100n * den; den = den * x.h; });
  // time = 1 / (num/den) = den/num hours
  return "Working together, " + _list(ts) + " finish one job in " + _time(den, num) + ".";
}

// The other truth: one worker's time and the together time give the other worker's time.
function otherTruth(alone, together) {
  var a = _t(alone), t = _t(together);
  if (a.h <= t.h) throw new Error("the one worker's time must be longer than the together time, because working together is always faster than working alone");
  // 1/x = 1/t - 1/a  ->  x = t*a / (a - t)
  return "If one worker alone takes " + a.text + " h and both together take " + t.text + " h, the other worker alone takes " +
    _time(t.h * a.h, (a.h - t.h) * 100n) + ".";
}

// The pipe truth: an inlet that fills a tank and an outlet that drains it, both open.
function pipeTruth(fill, drain) {
  var f = _t(fill), d = _t(drain);
  var head = "An inlet that fills the tank in " + f.text + " h and an outlet that drains it in " + d.text + " h, both open, ";
  if (f.h === d.h) return head + "cancel out: the level never changes.";
  if (f.h < d.h) return head + "fill an empty tank in " + _time(f.h * d.h, (d.h - f.h) * 100n) + ".";
  return head + "empty a full tank in " + _time(f.h * d.h, (f.h - d.h) * 100n) + ".";
}
