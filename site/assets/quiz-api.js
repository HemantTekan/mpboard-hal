/* educationdew quiz API client. Any quiz page:
 *   <div id="board"></div> <script src="/assets/quiz-api.js" defer></script>
 *   EDQuiz.submit({quiz:"hi/class-09/maths/chapter-03", name, score, total, wrong:[0-based q numbers], seconds})
 *     .then(() => EDQuiz.board("hi/class-09/maths/chapter-03", document.getElementById("board"), name));
 * Fails silently: the quiz always works even if the API is down. */
(function () {
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  function submit(a) {
    try {
      return fetch("/api/quiz/attempts", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(a), keepalive: true })
        .then(function (r) { return r.ok; }).catch(function () { return false; });
    } catch (e) { return Promise.resolve(false); }
  }
  function board(quiz, el, me) {
    if (!el) return Promise.resolve();
    return fetch("/api/quiz/leaderboard?quiz=" + encodeURIComponent(quiz) + "&days=30&limit=10&t=" + Date.now())
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || !d.rows || !d.rows.length) { el.hidden = true; return; }
        var medal = ["🥇", "🥈", "🥉"];
        el.innerHTML = '<p class="ed-board__title">🏆 इस क्विज़ के टॉपर (पिछले 30 दिन)</p><ol class="ed-board__list">' +
          d.rows.map(function (r, i) {
            var mine = me && r.name === me;
            return '<li' + (mine ? ' class="is-me"' : "") + '><span class="ed-board__rank">' + (medal[i] || i + 1) + '</span><span class="ed-board__name">' +
              esc(r.name) + (mine ? " (आप)" : "") + '</span><span class="ed-board__score">' + r.score + "/" + r.total + "</span></li>";
          }).join("") + "</ol>";
        el.hidden = false;
      }).catch(function () { el.hidden = true; });
  }
  window.EDQuiz = { submit: submit, board: board };
})();
