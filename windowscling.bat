@echo off
:: =========================================
:: Premium Cleanup & Reset Tool
:: =========================================

:: Set title, color, and window size
title 🚀 Premium PC Cleanup & Reset Tool
color 0A
mode 100,25

:: Fancy loading animation
echo.
echo Initializing Premium Tool...
ping localhost -n 2 >nul
echo █▒▒▒▒▒▒▒▒ 10%%
ping localhost -n 2 >nul
echo ███▒▒▒▒▒▒ 30%%
ping localhost -n 2 >nul
echo █████▒▒▒▒ 50%%
ping localhost -n 2 >nul
echo ███████▒▒ 70%%
ping localhost -n 2 >nul
echo ██████████ 100%%
ping localhost -n 2 >nul
echo Initialization Complete!
echo.

:: =========================================
:: Step 1: Reset Windows Firewall
echo Resetting Windows Firewall to default...
netsh advfirewall reset
echo Firewall reset complete.
echo.

:: =========================================
:: Step 2: Reset Network Settings
echo Resetting network settings...
netsh int ip reset >nul
netsh winsock reset >nul
ipconfig /release >nul
ipconfig /renew >nul
ipconfig /flushdns >nul
echo Network reset complete.
echo.

:: =========================================
:: Step 3: Clean Temp Files
echo Cleaning temporary files...
echo Deleting Windows TEMP folder...
rd /s /q C:\Windows\Temp
md C:\Windows\Temp
echo Deleting User TEMP folder...
rd /s /q "%TEMP%"
md "%TEMP%"
echo Temporary files cleaned.
echo.

:: =========================================
:: Finished
echo =========================================
echo ✅ All tasks completed successfully!

:: Show a message box
powershell -Command "[System.Windows.Forms.MessageBox]::Show('🎉 All cleanup and resets completed successfully!','Premium Tool','OK')"

:: Exit
exit
