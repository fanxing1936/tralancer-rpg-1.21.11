@echo off
chcp 65001 >nul
setlocal EnableExtensions

rem ============================================================
rem  破碎大陆 · Paper 1.21.11 服务端启动脚本
rem  只需要改下面「需要你填」的几行，其余不用动。
rem ============================================================

rem ---- 需要你填 ----------------------------------------------
rem 服务端所在文件夹（放 Paper jar 的地方）。留空 = 本脚本所在的文件夹
set "SERVER_DIR=D:\PAPER1.21.11\paper-1.21.11-132.jar"
rem Paper 服务端 jar 的文件名（1.21.11 版，例如 paper-1.21.11-132.jar）
set "SERVER_JAR=paper-1.21.11-132.jar"
rem Java 21 的 java.exe（1.21.11 最低要求 Java 21）。找不到时会改用系统 PATH 里的 java
set "JAVA_EXE=C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot\bin\java.exe"
rem 内存：8G / 8G（建议两者相同，例如 4G 4G）
set "MIN_RAM=4G"
set "MAX_RAM=4G"
rem 服务器关闭或崩溃后是否自动重启：1 = 自动重启，0 = 不重启
set "AUTO_RESTART=0"
rem -----------------------------------------------------------

title 破碎大陆 - Paper 1.21.11

if "%SERVER_DIR%"=="" set "SERVER_DIR=%~dp0"
if not exist "%SERVER_DIR%\" (
  echo [错误] 找不到服务端文件夹：
  echo        %SERVER_DIR%
  echo        请在 run.bat 里改 SERVER_DIR。
  goto :fail
)
cd /d "%SERVER_DIR%"

if not exist "%SERVER_JAR%" (
  echo [错误] 在 %CD% 里找不到服务端：%SERVER_JAR%
  echo        请把 Paper 1.21.11 的 jar 放进来，或在 run.bat 里改 SERVER_JAR。
  goto :fail
)

if not exist "%JAVA_EXE%" (
  where java >nul 2>nul
  if errorlevel 1 (
    echo [错误] 找不到 Java。请安装 Java 21，或在 run.bat 里改 JAVA_EXE。
    goto :fail
  )
  echo [提示] JAVA_EXE 指向的路径不存在，改用系统 PATH 里的 java：
  set "JAVA_EXE=java"
)
"%JAVA_EXE%" -version 2>&1 | findstr /r /c:"version \"2[1-9]" /c:"version \"[3-9][0-9]" >nul
if errorlevel 1 (
  echo [警告] 这个 Java 版本可能低于 21，1.21.11 需要 Java 21 或更高：
  "%JAVA_EXE%" -version
  echo.
)

if not exist "eula.txt" (
  echo [提示] 第一次启动会生成 eula.txt 后自动退出。
  echo        阅读 https://aka.ms/MinecraftEULA ，同意后把 eula.txt 里的 eula=false 改成 eula=true，再重新运行本脚本。
  echo.
)

rem Paper 官方推荐的 JVM 参数（Aikar's flags，适用于 12G 以下内存）
set "JVM_FLAGS=-XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled -XX:+PerfDisableSharedMem -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1HeapWastePercent=5 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1NewSizePercent=30 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 -XX:MaxGCPauseMillis=200 -XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -Dfile.encoding=UTF-8"

:start
echo 正在启动 %SERVER_JAR% （内存 %MIN_RAM% ~ %MAX_RAM%）...
echo.
"%JAVA_EXE%" -Xms%MIN_RAM% -Xmx%MAX_RAM% %JVM_FLAGS% -jar "%SERVER_JAR%" --nogui
echo.
if "%AUTO_RESTART%"=="1" (
  echo 服务器已停止，10 秒后自动重启。按 Ctrl+C 取消。
  timeout /t 10 >nul
  goto :start
)
echo 服务器已停止。
pause
exit /b 0

:fail
echo.
pause
exit /b 1
