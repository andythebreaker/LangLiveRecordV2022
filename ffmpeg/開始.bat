@echo off
TITLE "����:�K�W���}����UENTER�۰��^��"
set CD="%~dp0"
set /p URLName=    ��J���}�G
TITLE "��Q�䰱���^��"
%~dp0\bin\ffmpeg -i "%URLName%" -c copy %~dp0youtube.ts
echo �^�������w�g�b�ؿ��U�ͦ�youtube.ts�Ьd�ݡA�Ы����N������...&pause>nul

