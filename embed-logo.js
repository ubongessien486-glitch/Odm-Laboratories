const fs = require('fs');

// SVG logo: Oxygen Group mark — works on both dark & light backgrounds
const svgLogo = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 60" fill="none">
  <circle cx="30" cy="30" r="26" fill="#00A3B5" opacity="0.15"/>
  <circle cx="30" cy="30" r="18" fill="#00A3B5" opacity="0.3"/>
  <circle cx="30" cy="30" r="10" fill="#00A3B5"/>
  <path d="M30 14 L30 46 M14 30 L46 30" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="65" y="12" width="150" height="36" rx="0" fill="none"/>
  <text x="65" y="33" font-family="Inter,Arial,sans-serif" font-size="18" font-weight="800" fill="#003A70" letter-spacing="-0.5">OXYGEN</text>
  <text x="65" y="50" font-family="Inter,Arial,sans-serif" font-size="10" font-weight="500" fill="#00A3B5" letter-spacing="2">GROUP</text>
</svg>`;

// Convert to base64 data URL
const b64 = Buffer.from(svgLogo).toString('base64');
const dataUrl = `data:image/svg+xml;base64,${b64}`;

// Replace all logo.png references with the data URL in every HTML file
const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
let count = 0;
files.forEach(f => {
  let content = fs.readFileSync(f, 'utf8');
  if (content.includes('logo.png')) {
    content = content.replace(/logo\.png/g, dataUrl);
    fs.writeFileSync(f, content);
    count++;
    console.log('Updated: ' + f);
  }
});
console.log(`Done. Updated ${count} files.`);
