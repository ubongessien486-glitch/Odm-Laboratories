$html = (Invoke-WebRequest -Uri "https://oxygendx.com" -UseBasicParsing).Content
$pattern = '(?i)(?:src|href)=["'']([^"'' >\s]+\.(webp|jpg|jpeg|png|gif|svg|js|css|ico|woff2|woff|ttf))["'']'
$assets = [regex]::Matches($html, $pattern) | ForEach-Object { $_.Groups[1].Value }
$assets | Sort-Object -Unique | Out-File "assets.txt" -Encoding utf8
$html | Out-File "index.html" -Encoding utf8
