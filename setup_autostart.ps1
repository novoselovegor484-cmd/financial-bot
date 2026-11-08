$startup = [Environment]::GetFolderPath('Startup')
$desktop = [Environment]::GetFolderPath('Desktop')
$ws = New-Object -ComObject WScript.Shell

$startupLnk = Join-Path $startup "FinancialOffersBot.lnk"
$s1 = $ws.CreateShortcut($startupLnk)
$s1.TargetPath = "wscript.exe"
$s1.Arguments = "`"C:\Users\Администратор\Desktop\financial_offers_bot\start_hidden.vbs`""
$s1.WorkingDirectory = "C:\Users\Администратор\Desktop\financial_offers_bot"
$s1.Save()

$desktopLnk1 = Join-Path $desktop "Start_Bot_Hidden.lnk"
$s2 = $ws.CreateShortcut($desktopLnk1)
$s2.TargetPath = "wscript.exe"
$s2.Arguments = "`"C:\Users\Администратор\Desktop\financial_offers_bot\start_hidden.vbs`""
$s2.WorkingDirectory = "C:\Users\Администратор\Desktop\financial_offers_bot"
$s2.Save()

$desktopLnk2 = Join-Path $desktop "Stop_Bot.lnk"
$s3 = $ws.CreateShortcut($desktopLnk2)
$s3.TargetPath = "C:\Users\Администратор\Desktop\financial_offers_bot\stop_bot.bat"
$s3.WorkingDirectory = "C:\Users\Администратор\Desktop\financial_offers_bot"
$s3.Save()

Write-Output "Autostart and shortcuts configured successfully."
