@echo off
REM 음악 메타데이터 관리 시스템 - 실행 스크립트
REM 이 배치 파일을 더블클릭하면 자동으로 애플리케이션이 실행됩니다.

REM UTF-8 인코딩 설정 (한글 지원)
chcp 65001 > nul

REM 현재 배치 파일이 있는 디렉토리로 이동
cd /d "%~dp0"

echo ==========================================
echo 🎵 음악 라이브러리 시작 중...
echo ==========================================
echo.

REM 가상환경 확인 및 활성화
if exist venv\Scripts\activate (
    echo ✓ 가상환경 발견
    call venv\Scripts\activate
) else (
    echo ⚠ 가상환경이 없습니다.
    echo.
    echo 처음 실행하는 경우, 아래 명령어를 실행하세요:
    echo.
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    echo 설치 후 이 파일을 다시 실행하세요.
    echo.
    pause
    exit /b 1
)

REM Python 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo ✗ Python이 설치되어 있지 않습니다.
    echo Python 3.9 이상을 설치하세요.
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python 발견
echo.

REM Streamlit 실행
echo 🚀 애플리케이션 시작...
echo.
echo 브라우저가 자동으로 열립니다.
echo 열리지 않으면 다음 주소를 복사하세요: http://localhost:8501
echo.
echo 종료하려면 이 창을 닫거나 Ctrl+C를 누르세요.
echo ==========================================
echo.

REM Streamlit 실행 (로그 레벨: error, 브라우저 자동 열기)
python -m streamlit run app.py --logger.level=error

REM 실행 후 대기
echo.
echo ==========================================
echo 애플리케이션이 종료되었습니다.
echo ==========================================
pause
