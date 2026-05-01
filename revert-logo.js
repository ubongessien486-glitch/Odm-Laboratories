const fs = require('fs');

const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
let count = 0;
files.forEach(f => {
  let content = fs.readFileSync(f, 'utf8');
  // Match the entire data URI SVG we inserted earlier
  content = content.replace(/data:image\/svg\+xml;base64,[A-Za-z0-9+/=]+/g, 'logo.png');
  fs.writeFileSync(f, content);
  count++;
  console.log('Updated: ' + f);
});
console.log(`Done. Reverted logo in ${count} files.`);
