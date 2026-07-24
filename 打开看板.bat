@echo off
chcp 65001 >nul
echo 正在构建看板...
cd /d E:\TODO
python build.py
echo.
echo 正在打开看板...
start dist\index.html
echo 完成！
