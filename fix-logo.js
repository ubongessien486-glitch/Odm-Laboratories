const fs = require('fs');

const svgLogo = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 60" fill="none">
  <circle cx="30" cy="30" r="26" fill="#00A3B5" opacity="0.15"/>
  <circle cx="30" cy="30" r="18" fill="#00A3B5" opacity="0.3"/>
  <circle cx="30" cy="30" r="10" fill="#00A3B5"/>
  <path d="M30 14 L30 46 M14 30 L46 30" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="65" y="12" width="150" height="36" rx="0" fill="none"/>
  <text x="65" y="33" font-family="Inter,Arial,sans-serif" font-size="18" font-weight="800" fill="#003A70" letter-spacing="-0.5">OXYGEN</text>
  <text x="65" y="50" font-family="Inter,Arial,sans-serif" font-size="10" font-weight="500" fill="#00A3B5" letter-spacing="2">GROUP</text>
</svg>`;

fs.writeFileSync('logo.svg', svgLogo);

const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
files.forEach(f => {
  let content = fs.readFileSync(f, 'utf8');
  content = content.replace(/logo\.png/g, 'logo.svg');
  // Also check for the base64 inline svg and replace that too if present
  content = content.replace(/data:image\/svg\+xml;base64,[A-Za-z0-9+/=]+/g, 'logo.svg');
  fs.writeFileSync(f, content);
});
console.log('Fixed logo in HTML files');
