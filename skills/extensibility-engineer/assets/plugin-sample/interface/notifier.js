// Exported extension interface sample. NOTE: no stability tier annotation —
// intentionally left unlabeled so the surface checker reports a gap.
export function notify(title, body) {
  return { title, body };
}
