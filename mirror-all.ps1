$baseUrl = "https://oxygendx.com"
$pages = @("index.html", "diagnostic.html", "homecare.html", "login.html", "tpa.html", "contact.html")
$allAssets = @()

foreach ($page in $pages) {
    $url = if ($page -eq "index.html") { "$baseUrl/" } else { "$baseUrl/$page" }
    try {
        $html = (Invoke-WebRequest -Uri $url -UseBasicParsing).Content
        $html | Out-File $page -Encoding utf8
        $pattern = '(?i)(?:src|href)=["'']([^"'' >\s]+\.(webp|jpg|jpeg|png|gif|svg|js|css|ico|woff2|woff|ttf))(\?v=\d+)?["'']'
        $assets = [regex]::Matches($html, $pattern) | ForEach-Object { $_.Groups[1].Value }
        $allAssets += $assets
    } catch {
        Write-Host "Failed to fetch $page"
    }
}

$uniqueAssets = $allAssets | Sort-Object -Unique
$uniqueAssets | Out-File "all_assets.txt" -Encoding utf8

function Download-Asset {
    param([string]$BaseUrl, [string]$AssetPath, [string]$OutDir)
    
    $filename = Split-Path $AssetPath -Leaf
    $outFile = Join-Path $OutDir $filename
    
    if (Test-Path $outFile) {
        Write-Host "SKIP (exists): $filename"
        return
    }
    
    $url = if ($AssetPath -match '^https?://') { $AssetPath } else { "$BaseUrl/$($AssetPath.TrimStart('/'))" }
    
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13
        $wc = New-Object System.Net.WebClient
        $wc.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        $wc.Headers.Add("Referer", $BaseUrl)
        $wc.DownloadFile($url, $outFile)
        $size = (Get-Item $outFile).Length
        Write-Host "OK ($size bytes): $filename"
    } catch {
        Write-Host "FAIL: $filename - $_"
    }
}

$outDir = "C:\Users\LENOVO\.gemini\antigravity-ide\scratch\oxygendx"
foreach ($asset in $uniqueAssets) {
    if ($asset -notmatch '^https?://') {
        Download-Asset $baseUrl $asset $outDir
    }
}
