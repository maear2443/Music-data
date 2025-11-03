@echo off
REM Windows용 단계별 라이브러리 설치 스크립트

echo ==========================================
echo 라이브러리 설치 시작...
echo ==========================================
echo.

REM pip 업그레이드
echo [1/10] pip 업그레이드 중...
python -m pip install --upgrade pip
if errorlevel 1 goto error

REM 기본 패키지
echo [2/10] setuptools, wheel 설치 중...
pip install setuptools wheel
if errorlevel 1 goto error

REM 환경 변수 관리
echo [3/10] python-dotenv 설치 중...
pip install python-dotenv
if errorlevel 1 goto error

REM 과학 계산 라이브러리 (미리 컴파일된 버전)
echo [4/10] numpy 설치 중...
pip install numpy --only-binary :all:
if errorlevel 1 goto error

echo [5/10] scipy 설치 중...
pip install scipy --only-binary :all:
if errorlevel 1 goto error

REM 데이터 처리
echo [6/10] pandas, openpyxl 설치 중...
pip install pandas openpyxl
if errorlevel 1 goto error

REM 오디오 처리
echo [7/10] 오디오 라이브러리 설치 중...
pip install soundfile audioread pydub
if errorlevel 1 goto error

REM 음악 분석
echo [8/10] librosa 설치 중...
pip install librosa
if errorlevel 1 goto error

REM UI
echo [9/10] streamlit 설치 중...
pip install streamlit
if errorlevel 1 goto error

REM API 라이브러리 (선택사항)
echo [10/10] API 라이브러리 설치 중 (선택)...
pip install google-generativeai pyacoustid pylast
if errorlevel 1 (
    echo ⚠ API 라이브러리 설치 실패 - 선택사항이므로 계속 진행
)

echo.
echo ==========================================
echo ✓ 모든 라이브러리 설치 완료!
echo ==========================================
echo.
echo 이제 run.bat을 실행하여 앱을 시작할 수 있습니다.
echo.
pause
exit /b 0

:error
echo.
echo ==========================================
echo ✗ 설치 중 오류가 발생했습니다.
echo ==========================================
echo.
echo 아래 명령어로 수동 설치를 시도해보세요:
echo   pip install python-dotenv
echo   pip install numpy scipy --only-binary :all:
echo   pip install pandas openpyxl soundfile audioread pydub librosa streamlit
echo   pip install google-generativeai pyacoustid pylast
echo.
pause
exit /b 1
