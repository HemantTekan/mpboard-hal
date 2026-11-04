-- Quiz attempts: one row per finished quiz. Nickname only (no phone/email) for student privacy.
-- quiz_id is the quiz's site path, e.g. 'hi/class-09/maths/chapter-03'.
-- wrong is a JSON array of original question numbers (0-based) the student missed.
CREATE TABLE IF NOT EXISTS quiz_attempts (
  id         INTEGER PRIMARY KEY,
  quiz_id    TEXT    NOT NULL,
  nickname   TEXT,
  score      INTEGER NOT NULL CHECK (score >= 0),
  total      INTEGER NOT NULL CHECK (total > 0 AND score <= total),
  wrong      TEXT    NOT NULL DEFAULT '[]',
  seconds    INTEGER,
  created_at INTEGER NOT NULL DEFAULT (unixepoch())
);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_board ON quiz_attempts (quiz_id, created_at);
