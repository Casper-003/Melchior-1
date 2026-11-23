$ffDir = "C:\Users\Casper\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin"
$env:PATH = "$ffDir;$env:PATH"

$p1Dir = "c:\Users\Casper\Documents\Proj\manim_inverter\media_ql_p1\videos\p1_hbridge_scenes\480p15"
$p2Dir = "c:\Users\Casper\Documents\Proj\manim_inverter\media_ql_p2\videos\p2_spwm_motor_scenes\480p15"
$outDir = "c:\Users\Casper\Documents\Proj\manim_inverter\qa_frames"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
Remove-Item "$outDir\*.png" -Force -ErrorAction SilentlyContinue

$videos = @(
    @{ name = "P1A"; path = "$p1Dir\P1A_CanvasAndHBridge.mp4" },
    @{ name = "P1B"; path = "$p1Dir\P1B_SquareWaveAndDerivation.mp4" },
    @{ name = "P1C"; path = "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" },
    @{ name = "P2A"; path = "$p2Dir\P2A_BipolarAvgToDottedSine.mp4" },
    @{ name = "P2B"; path = "$p2Dir\P2B_SPWMCurrentAndParams.mp4" },
    @{ name = "P2C"; path = "$p2Dir\P2C_ThreePhaseMotor.mp4" }
)

foreach ($v in $videos) {
    $dur = ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $v.path
    Write-Host ("{0}: {1:N2}s -> {2}" -f $v.name, [double]$dur, $v.path)
}

function Grab($vidPath, $sec, $outName) {
    ffmpeg -y -loglevel error -ss $sec -i $vidPath -frames:v 1 "$outDir\$outName.png"
}

# P1A: full-bleed canvas, RL drawn from start, Red full-loop arrows, Blue full-loop arrows
Grab "$p1Dir\P1A_CanvasAndHBridge.mp4" 9.0 "01_p1a_rl_drawn"
Grab "$p1Dir\P1A_CanvasAndHBridge.mp4" 16.5 "02_p1a_red_full_loop"
Grab "$p1Dir\P1A_CanvasAndHBridge.mp4" 21.0 "03_p1a_blue_full_loop"

# P1B: Red half-cycle AND Blue half-cycle (zero red residue!), TNR derivation, u(t)+i(t)
Grab "$p1Dir\P1B_SquareWaveAndDerivation.mp4" 2.2 "04_p1b_red_ut"
Grab "$p1Dir\P1B_SquareWaveAndDerivation.mp4" 4.0 "05_p1b_blue_ut"
Grab "$p1Dir\P1B_SquareWaveAndDerivation.mp4" 22.0 "06_p1b_tnr_deriv"
Grab "$p1Dir\P1B_SquareWaveAndDerivation.mp4" 36.0 "07_p1b_ut_it_done"

# P1C: D2/D3 freewheeling, centered short + centered boom, Shot 11 S1/DT/S3 sync, end seam
Grab "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" 4.5 "08_p1c_fw_d2d3"
Grab "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" 28.0 "09_p1c_centered_short"
Grab "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" 30.2 "10_p1c_centered_boom"
Grab "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" 37.6 "11a_p1c_dt_s1"
Grab "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" 38.9 "11b_p1c_dt_both_off"
Grab "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" 40.0 "11c_p1c_dt_s3"
ffmpeg -y -loglevel error -sseof -0.15 -i "$p1Dir\P1C_FreewheelingAndDeadtime.mp4" -frames:v 1 "$outDir\11d_p1c_end.png"

# P2A & P2B: seam check, single avg, dotted sine, 3-tier scope (no border!)
Grab "$p2Dir\P2A_BipolarAvgToDottedSine.mp4" 0.0 "12a_p2a_start"
Grab "$p2Dir\P2A_BipolarAvgToDottedSine.mp4" 38.5 "12b_p2a_dotted_sine"
Grab "$p2Dir\P2B_SPWMCurrentAndParams.mp4" 20.0 "13_p2b_three_tier"

# P2C: Stage 1 full-size centered straight leads, Stage 2 upper shrunk + full-width lower 3-phase
Grab "$p2Dir\P2C_ThreePhaseMotor.mp4" 7.4 "14_p2c_stage1_straight"
Grab "$p2Dir\P2C_ThreePhaseMotor.mp4" 14.0 "15_p2c_stage2_split"

Write-Host "Extracted all QA verification frames to $outDir"
