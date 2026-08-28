$conns = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -ge 8500 -and $_.LocalPort -le 8600 }
foreach ($c in $conns) {
    if ($c.LocalPort -ne 8590 -and $c.LocalPort -ne 8595 -and $c.LocalPort -ne 8598) {
        Write-Host "Stopping process $($c.OwningProcess) on port $($c.LocalPort)"
        Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}
