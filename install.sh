#!/bin/bash
# Linux/Mac용 단계별 라이브러리 설치 스크립트

echo "=========================================="
echo "라이브러리 설치 시작..."
echo "=========================================="
echo ""

# pip 업그레이드
echo "[1/8] pip 업그레이드 중..."
python -m pip install --upgrade pip || { echo "pip 업그레이드 실패"; exit 1; }

# 기본 패키지
echo "[2/8] setuptools, wheel 설치 중..."
pip install setuptools wheel || { echo "설치 실패"; exit 1; }

# 과학 계산 라이브러리
echo "[3/8] numpy 설치 중..."
pip install numpy || { echo "numpy 설치 실패"; exit 1; }

echo "[4/8] scipy 설치 중..."
pip install scipy || { echo "scipy 설치 실패"; exit 1; }

# 데이터 처리
echo "[5/8] pandas, openpyxl 설치 중..."
pip install pandas openpyxl || { echo "설치 실패"; exit 1; }

# 오디오 처리
echo "[6/8] 오디오 라이브러리 설치 중..."
pip install soundfile audioread pydub || { echo "설치 실패"; exit 1; }

# 음악 분석
echo "[7/8] librosa 설치 중..."
pip install librosa || { echo "librosa 설치 실패"; exit 1; }

# UI
echo "[8/8] streamlit 설치 중..."
pip install streamlit || { echo "streamlit 설치 실패"; exit 1; }

echo ""
echo "=========================================="
echo "✓ 모든 라이브러리 설치 완료!"
echo "=========================================="
echo ""
echo "이제 ./run.sh를 실행하여 앱을 시작할 수 있습니다."
echo ""
