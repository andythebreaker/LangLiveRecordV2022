@echo off
TITLE "提示:貼上網址後按下ENTER自動擷取"
set CD="%~dp0"
set /p URLName=    輸入網址：
TITLE "按Q鍵停止擷取"
%~dp0\bin\ffmpeg -i "%URLName%" -c copy %~dp0youtube.ts
echo 擷取結束已經在目錄下生成youtube.ts請查看，請按任意鍵關閉...&pause>nul

