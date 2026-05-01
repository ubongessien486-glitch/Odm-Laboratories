const fs = require('fs');
const files = fs.readdirSync('.').filter(f => f.endsWith('.html') && f !== 'index.html' && f !== 'homecare.html');
files.forEach(f => {
  let content = fs.readFileSync(f, 'utf8');
  content = content.replace(/href="index\.html"/g, 'href="diagnostic.html"');
  content = content.replace(/window\.location\.href='index\.html'/g, "window.location.href='diagnostic.html'");
  fs.writeFileSync(f, content);
});
console.log('Updated links in ' + files.length + ' files');
