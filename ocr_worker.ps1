param(
    [string]$ImageDir,
    [string]$OutputFile
)

Add-Type -AssemblyName System.Runtime.WindowsRuntime

function AwaitTask($asyncOp, $type) {
    $asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { 
        $_.Name -eq 'AsTask' -and 
        $_.GetParameters().Count -eq 1 -and 
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' 
    })[0]
    $netTask = $asTask.MakeGenericMethod($type).Invoke($null, @($asyncOp))
    $netTask.Wait()
    return $netTask.Result
}

[Windows.Globalization.Language, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.SoftwareBitmap, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null

$lang = [Windows.Globalization.Language]::new("ko")
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)

if ($engine -eq $null) {
    Write-Error "Korean OCR Engine not available!"
    exit 1
}

$pngFiles = Get-ChildItem -Path $ImageDir -Filter "*.png" | Sort-Object Name
$allText = @()

foreach ($img in $pngFiles) {
    $pageNum = [System.IO.Path]::GetFileNameWithoutExtension($img.Name)
    try {
        $fileOp = [Windows.Storage.StorageFile]::GetFileFromPathAsync($img.FullName)
        $file = AwaitTask $fileOp ([Windows.Storage.StorageFile])

        $streamOp = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
        $stream = AwaitTask $streamOp ([Windows.Storage.Streams.IRandomAccessStream])

        $decoderOp = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
        $decoder = AwaitTask $decoderOp ([Windows.Graphics.Imaging.BitmapDecoder])

        $bitmapOp = $decoder.GetSoftwareBitmapAsync()
        $bitmap = AwaitTask $bitmapOp ([Windows.Graphics.Imaging.SoftwareBitmap])

        $ocrOp = $engine.RecognizeAsync($bitmap)
        $ocrResult = AwaitTask $ocrOp ([Windows.Media.Ocr.OcrResult])

        $allText += "---"
        $allText += "## [$pageNum]"
        $allText += ""
        $allText += $ocrResult.Text
        $allText += ""
    } catch {
        $allText += "---"
        $allText += "## [$pageNum] (OCR Error: $_)"
        $allText += ""
    }
}

$allText | Out-File -FilePath $OutputFile -Encoding utf8
Write-Host "Processed $($pngFiles.Count) pages -> $OutputFile"
