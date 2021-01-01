$package = Split-Path -leaf -path (Get-Location)
$process = "c:\Program Files\7-Zip\7z.exe"

Write-Host "=== Github Release Packager ==="
$version = Read-Host "Enter Release version "
$destinationFile = $package + "." + $version + ".zip" 

if (Test-Path -Path $destinationFile) {
    $existsCheck = Read-Host $destinationFile "already exists. Delete and recreate, Add files, or eXit now (d/a/x)? "
    switch -Regex ( $existsCheck ) {
        [dD] { 
            Write-Host "Deleting anb recreating" 
            Remove-Item $destinationFile
        }
        [aA] { Write-Host "Append" }
        [xX] { 
            Write-Host "Exiting." 
            Exit
        }
        default { 
            Write-Host "Invalid choice, Exiting." 
            Exit
        }
    }
}

Write-Host "Adding files to" $destinationFile
Start-Process $process -ArgumentList "a $destinationFile @listfile.txt"   
Write-Host "Done." 


