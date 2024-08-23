@echo off
color 0A
title PM2 應用程式管理工具

echo.
echo ======================================
echo        應用程式設置完成！
echo ======================================

:menu
cls
echo ======================================
echo        PM2 應用程式管理工具
echo ======================================
echo.
echo 選擇一個操作：
echo 1. 啟動應用程式
echo 2. 停止應用程式
echo 3. 重啟應用程式
echo 4. 檢視應用狀態
echo.
set /p choice=請選擇 [1-4]:

if "%choice%"=="1" goto start_app
if "%choice%"=="2" goto stop_app
if "%choice%"=="3" goto restart_app
if "%choice%"=="4" goto status_app

:start_app
cls
echo ======================================
echo        啟動應用程式
echo ======================================
echo.
echo 正在啟動應用程式...
pm2 start ecosystem.config.js
pause

:stop_app
cls
echo ======================================
echo        停止應用程式
echo ======================================
echo.
echo 正在停止應用程式...
pm2 stop all
pause

:restart_app
cls
echo ======================================
echo        重啟應用程式
echo ======================================
echo.
echo 正在重啟應用程式...
pm2 restart all
pause

:status_app
cls
echo ======================================
echo        應用狀態
echo ======================================
echo.
pm2 list
pause
