@echo off
echo.
echo  ================================================
echo   NexBank - Lab de Pentest OWASP Top 10
echo   Instalando dependencias...
echo  ================================================
echo.
pip install flask --quiet
echo.
echo  Iniciando servidor em http://127.0.0.1:5000
echo  Pressione Ctrl+C para parar.
echo  ================================================
echo.
python app.py
pause
