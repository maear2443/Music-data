@echo off
REM Windows용 단계별 라이브러리 설치 스크립트

echo ==========================================
echo 라이브러리 설치 시작...
echo ==========================================
echo.

REM pip 업그레이드
echo [1/8] pip 업그레이드 중...
python -m pip install --upgrade pip
if errorlevel 1 goto error

REM 기본 패키지
echo [2/8] setuptools, wheel 설치 중...
pip install setuptools wheel
if errorlevel 1 goto error

REM 과학 계산 라이브러리 (미리 컴파일된 버전)
echo [3/8] numpy 설치 중...
pip install numpy --only-binary :all:
if errorlevel 1 goto error

echo [4/8] scipy 설치 중...
pip install scipy --only-binary :all:
if errorlevel 1 goto error

REM 데이터 처리
echo [5/8] pandas, openpyxl 설치 중...
pip install pandas openpyxl
if errorlevel 1 goto error

REM 오디오 처리
echo [6/8] 오디오 라이브러리 설치 중...
pip install soundfile audioread pydub
if errorlevel 1 goto error

REM 음악 분석
echo [7/8] librosa 설치 중...
pip install librosa
if errorlevel 1 goto error

REM UI
echo [8/8] streamlit 설치 중...
pip install streamlit
if errorlevel 1 goto error

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
echo   pip install numpy scipy --only-binary :all:
echo   pip install pandas openpyxl soundfile audioread pydub librosa streamlit
echo.
pause
exit /b 1
