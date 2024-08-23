@echo off
title NPM 可視化啟動介面
color 0A

:menu
cls
echo  ==========================================
echo  ||          NPM 啟動管理工具           ||
echo  ==========================================
echo  ||  1. 啟動前後端服務 (npm start)     ||
echo  ||  2. 單獨啟動前端 (npm run dev)     ||
echo  ||  3. 單獨啟動後端 (npm run server)  ||
echo  ||  4. 停止所有服務                   ||
echo  ||  5. 退出                           ||
echo  ==========================================
echo.
set /p choice=請選擇 [1-5]:

if "%choice%"=="1" goto start_all
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_backend
if "%choice%"=="4" goto stop_all
if "%choice%"=="5" goto exit

:start_all
cls
echo  ==========================================
echo  ||       正在啟動前後端服務...         ||
echo  ==========================================
npm start
pause
goto menu

:start_frontend
cls
echo  ==========================================
echo  ||        正在啟動前端服務...          ||
echo  ==========================================
npm run dev
pause
goto menu

:start_backend
cls
echo  ==========================================
echo  ||        正在啟動後端服務...          ||
echo  ==========================================
npm run server
pause
goto menu

:stop_all
cls
echo  ==========================================
echo  ||      停止所有服務 (Ctrl+C)          ||
echo  ==========================================
pause
goto menu

:exit
cls
echo  ==========================================
echo  ||         感謝使用，再見！            ||
echo  ==========================================
pause
exit
