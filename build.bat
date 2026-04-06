@echo off
chcp 65001 >nul
echo ========================================
echo    今天吃什么 - 打包脚本
echo ========================================
echo.

REM 检查 PyInstaller 是否安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败！
        pause
        exit /b 1
    )
)

echo [1/3] 清理旧的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "今天吃什么.spec" del /q "今天吃什么.spec"

echo [2/3] 开始打包...
pyinstaller --onefile --windowed --name "今天吃什么" main.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo [3/3] 清理临时文件...
if exist "build" rmdir /s /q "build"
if exist "今天吃什么.spec" del /q "今天吃什么.spec"

echo.
echo ========================================
echo    打包完成！
echo    输出文件: dist\今天吃什么.exe
echo ========================================
echo.
pause
