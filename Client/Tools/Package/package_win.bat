@echo off
REM 切换到Client目录
cd /d %~dp0..\..

echo 当前目录为：
cd

REM 设置当前目录为变量
set "CLIENT_DIR=%CD%"

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 一键打包MGAME项目为Windows可执行文件
REM 需先安装pyinstaller: pip install pyinstaller

REM 检查并安装pyinstaller
pip list | findstr pyinstaller > nul
if errorlevel 1 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

REM 删除旧的spec文件（如果存在）
if exist "Tools\Package\MGAME.spec" del "Tools\Package\MGAME.spec"

REM 打包命令
pyinstaller -F -w ^
    --clean ^
    --distpath Tools\Package\dist ^
    --workpath Tools\Package\build ^
    --specpath Tools\Package ^
    --add-data "%CLIENT_DIR%\config;config" ^
    --add-data "%CLIENT_DIR%\UI;UI" ^
    --add-data "%CLIENT_DIR%\backpack;backpack" ^
    --add-data "%CLIENT_DIR%\Tools\Package\language\SIMHEI.TTF;." ^
    --hidden-import pygame ^
    --hidden-import pygame.display ^
    --hidden-import pygame.font ^
    --hidden-import pygame.time ^
    --hidden-import pygame.draw ^
    --hidden-import pygame.event ^
    --hidden-import pygame.surface ^
    --hidden-import pygame.rect ^
    --name MGAME ^
    main.py

REM 打包完成后，exe在Tools\Package\dist目录下
echo 打包完成！可执行文件位于 Tools\Package\dist\MGAME.exe

REM 退出虚拟环境
deactivate

pause