// stdin: JSON array of TeX strings -> stdout: JSON array of HTML
const katex = require(__dirname + '/vendor/katex.min.js');
let d = ''; process.stdin.on('data', c => d += c).on('end', () => {
  const a = JSON.parse(d);
  process.stdout.write(JSON.stringify(a.map(t => katex.renderToString(t, {throwOnError: true, output: 'html'}))));
});
