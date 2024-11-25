Get-FileHash -Path dir HW.txt | format-list

$hash1=Get-FileHash -Path HW.txt
$hash2=Get-FileHash -Path HW.txt

$hash1.Hash -eq $hash2.Hash

#script to run this commands every 45 sec
#while(1) { sleep -sec 2; .\get-filehash.ps1 }
