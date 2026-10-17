# Deploy outputs/_site to contentfellow.com via the cPanel API. Run on YOUR Windows computer (PowerShell):
#   irm https://raw.githubusercontent.com/glameonline/AISA/claude/seo-geo-content-agents/tools/deploy_cpanel.ps1 | iex
# It asks for a cPanel API token (cPanel > Security > Manage API Tokens). The token is never stored.
$ErrorActionPreference = "Stop"
$CpUser = "contwfah"; $HostUrl = "https://server247.web-hosting.com:2083"; $Doc = "/home/$CpUser/public_html"
$Br = "claude/seo-geo-content-agents"; $Raw = "https://raw.githubusercontent.com/glameonline/AISA/$Br"; $Zip = "contentfellow-site-2026-10-16.zip"
$sec = Read-Host "cPanel API token" -AsSecureString
$Token = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
$H = @{ Authorization = "cpanel ${CpUser}:$Token" }
$Bk = Join-Path $HOME ("contentfellow-backup-" + (Get-Date -Format "yyyyMMdd-HHmm")); New-Item -ItemType Directory -Force $Bk | Out-Null; Set-Location $Bk
function Qs($q) { ($q.GetEnumerator() | ForEach-Object { $_.Key + "=" + [uri]::EscapeDataString([string]$_.Value) }) -join "&" }
function Uapi($mod, $fn, $q) { $u = $HostUrl + "/execute/" + $mod + "/" + $fn + "?" + (Qs $q); Invoke-RestMethod -Headers $H -Uri $u }
function Api2($q) { $q.cpanel_jsonapi_user=$CpUser; $q.cpanel_jsonapi_apiversion="2"; $q.cpanel_jsonapi_module="Fileman"; $q.cpanel_jsonapi_func="fileop"
  $u = $HostUrl + "/json-api/cpanel?" + (Qs $q); Invoke-RestMethod -Headers $H -Uri $u }

Write-Host "1/6 Checking login..."
$l = Uapi "Fileman" "list_files" @{ dir = $Doc }; if ($l.status -ne 1) { throw "Login failed: $($l.errors)" }

Write-Host "2/6 Backing up index.html and .htaccess to $Bk ..."
$old = @{}
foreach ($f in "index.html", ".htaccess") {
  $r = Uapi "Fileman" "get_file_content" @{ dir = $Doc; file = $f }
  if ($r.status -ne 1) { throw "Backup of $f failed, stopping (nothing changed): $($r.errors)" }
  $old[$f] = $r.data.content; Set-Content -Path "backup-$f" -Value $r.data.content -NoNewline -Encoding UTF8
}

Write-Host "3/6 Downloading the site package from GitHub..."
Invoke-WebRequest "https://github.com/glameonline/AISA/raw/$Br/outputs/_deploy/$Zip" -OutFile $Zip
$add = (Invoke-WebRequest "$Raw/outputs/_site-fixes/htaccess-add-at-top.txt" -UseBasicParsing).Content

Write-Host "4/6 Uploading and extracting into public_html..."
$up = curl.exe -fsS -H "Authorization: cpanel ${CpUser}:$Token" -F "dir=$Doc" -F "overwrite=1" -F "file-1=@$Zip" "$HostUrl/execute/Fileman/upload_files" | ConvertFrom-Json
if ($up.status -ne 1) { throw "Upload failed: $($up.errors)" }
$ex = Api2 @{ op = "extract"; sourcefiles = "$Doc/$Zip"; destfiles = $Doc }
if ($ex.cpanelresult.data[0].result -ne 1) { Write-Host "Extract failed. In cPanel File Manager: right-click $Zip > Extract." }
try { Api2 @{ op = "unlink"; sourcefiles = "$Doc/$Zip" } | Out-Null } catch {}

Write-Host "5/6 Adding SEO rules to the top of .htaccess..."
if ($old[".htaccess"] -notmatch "ContentFellow SEO fixes") {
  [IO.File]::WriteAllText((Join-Path $Bk "htaccess-new.txt"), ($add + "`n" + $old[".htaccess"]), (New-Object Text.UTF8Encoding $false))
  $ht = curl.exe -fsS -H "Authorization: cpanel ${CpUser}:$Token" -F "dir=$Doc" -F "file=.htaccess" -F "content=<htaccess-new.txt" "$HostUrl/execute/Fileman/save_file_content" | ConvertFrom-Json
  if ($ht.status -eq 1) { Write-Host "   .htaccess updated." } else { Write-Host "   .htaccess not updated; paste the rules manually." }
} else { Write-Host "   rules already present." }

Write-Host "6/6 Checking pages..."
foreach ($p in "", "blog/", "services/", "services/development/", "services/management/", "services/search-fellow/", "get-started/", "burnley/", "about/", "faq/", "privacy/", "sitemap.xml", "llms.txt", "llms-full.txt") {
  $code = curl.exe -s -o NUL -w "%{http_code}" "https://contentfellow.com/$p"; Write-Host ("  /{0,-28} {1}" -f $p, $code)
}
Write-Host ("  www -> non-www: " + (curl.exe -s -o NUL -w "%{http_code} %{redirect_url}" "https://www.contentfellow.com/"))
Write-Host "Done. Backup kept in $Bk. Tell Claude: 'script chal gayi' and paste this output."
