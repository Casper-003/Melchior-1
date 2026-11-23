$ErrorActionPreference = "Stop"
$ffDir = "C:\Users\Casper\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin"
$env:PATH = "$ffDir;$env:PATH"

$root = "c:\Users\Casper\Documents\Proj\manim_inverter"
$outDir = "c:\Users\Casper\Documents\Proj\manim_videos"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$p1a = "$root\media_qh\P1A\videos\p1_hbridge_scenes\1080p60\P1A_CanvasAndHBridge.mp4"
$p1b = "$root\media_qh\P1B\videos\p1_hbridge_scenes\1080p60\P1B_SquareWaveAndDerivation.mp4"
$p1c = "$root\media_qh\P1C\videos\p1_hbridge_scenes\1080p60\P1C_FreewheelingAndDeadtime.mp4"
$p2a = "$root\media_qh\P2A\videos\p2_spwm_motor_scenes\1080p60\P2A_BipolarAvgToDottedSine.mp4"
$p2b = "$root\media_qh\P2B\videos\p2_spwm_motor_scenes\1080p60\P2B_SPWMCurrentAndParams.mp4"
$p2c = "$root\media_qh\P2C\videos\p2_spwm_motor_scenes\1080p60\P2C_ThreePhaseMotor.mp4"

foreach ($f in @($p1a, $p1b, $p1c, $p2a, $p2b, $p2c)) {
    if (-not (Test-Path $f)) {
        throw "Missing rendered clip: $f"
    }
}

$tmpDir = "$root\media_qh\_concat_lists"
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null

function Stitch($listName, $clips, $destMp4) {
    $listPath = "$tmpDir\$listName"
    $lines = $clips | ForEach-Object { "file '$($_.Replace('\', '/'))'" }
    [System.IO.File]::WriteAllLines($listPath, $lines, (New-Object System.Text.UTF8Encoding($false)))
    ffmpeg -y -loglevel error -f concat -safe 0 -i $listPath `
        -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -r 60 -movflags +faststart `
        $destMp4
}

$outP1 = "$outDir\第3页_单相H桥与续流死区_1080p60.mp4"
$outP2 = "$outDir\第4页_SPWM调制与三相电机_1080p60.mp4"
$outAll = "$outDir\主驱逆变器_科普动画完整版_1080p60.mp4"

Stitch "p1.txt" @($p1a, $p1b, $p1c) $outP1
Stitch "p2.txt" @($p2a, $p2b, $p2c) $outP2
Stitch "all.txt" @($p1a, $p1b, $p1c, $p2a, $p2b, $p2c) $outAll

Write-Host "`n=== Final Output Verification (ffprobe) ==="
foreach ($out in @($outP1, $outP2, $outAll)) {
    $info = ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name,pix_fmt -show_entries format=duration -of csv=p=0 $out
    $mb = [math]::Round((Get-Item $out).Length / 1MB, 2)
    Write-Host "$out | $mb MB | $info"
}
