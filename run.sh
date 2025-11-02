#!/bin/bash
# 음악 메타데이터 관리 시스템 - 실행 스크립트 (Linux/Mac)
# 이 스크립트를 실행하면 자동으로 애플리케이션이 실행됩니다.

# 현재 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

echo "=========================================="
echo "🎵 음악 라이브러리 시작 중..."
echo "=========================================="
echo ""

# 가상환경 확인 및 활성화
if [ -d "venv" ]; then
    echo "✓ 가상환경 발견"
    source venv/bin/activate
else
    echo "⚠ 가상환경이 없습니다."
    echo ""
    echo "처음 실행하는 경우, 아래 명령어를 실행하세요:"
    echo ""
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    echo "설치 후 이 스크립트를 다시 실행하세요."
    echo ""
    exit 1
fi

# Python 확인
if ! command -v python &> /dev/null; then
    echo "✗ Python이 설치되어 있지 않습니다."
    echo "Python 3.9 이상을 설치하세요."
    echo ""
    exit 1
fi

echo "✓ Python 발견"
echo ""

# Streamlit 실행
echo "🚀 애플리케이션 시작..."
echo ""
echo "브라우저가 자동으로 열립니다."
echo "열리지 않으면 다음 주소를 방문하세요: http://localhost:8501"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo "=========================================="
echo ""

# Streamlit 실행 (로그 레벨: error, 브라우저 자동 열기)
python -m streamlit run app.py --server.headless=false --browser.gatherUsageStats=false

echo ""
echo "=========================================="
echo "애플리케이션이 종료되었습니다."
echo "=========================================="
