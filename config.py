"""
음악 메타데이터 관리 시스템 - 설정 파일
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 애플리케이션 설정
APP_NAME = "🎵 내 음악 라이브러리"
APP_VERSION = "1.0.0"

# 데이터베이스 설정
DB_NAME = "music_data.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

# 지원하는 음악 파일 포맷
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".flac"]

# 분위기 (mood) 카테고리
MOOD_CATEGORIES = [
    "upbeat",
    "calm",
    "melancholic",
    "energetic",
    "relaxing",
    "dark",
    "cheerful",
    "dreamy",
    "aggressive",
    "romantic"
]

# 장르 카테고리
GENRE_CATEGORIES = [
    "Pop",
    "Rock",
    "Electronic",
    "Hip-Hop",
    "Jazz",
    "Classical",
    "Folk",
    "R&B",
    "Metal",
    "Indie",
    "Ambient",
    "Dance",
    "Blues",
    "Country",
    "Reggae",
    "Other"
]

# 자동 태그 키워드 매핑 (BPM 기반)
BPM_TAG_MAPPING = {
    (0, 80): "slow",
    (80, 120): "moderate",
    (120, 140): "fast",
    (140, 200): "very_fast"
}

# 에너지 레벨 기반 태그
ENERGY_TAG_MAPPING = {
    (0, 30): "low_energy",
    (30, 60): "medium_energy",
    (60, 100): "high_energy"
}

# 엑셀 내보내기 설정
EXCEL_EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
EXCEL_COLUMNS = [
    "ID",
    "제목",
    "생성날짜",
    "스타일",
    "BPM",
    "길이(초)",
    "분위기",
    "에너지",
    "보컬",
    "평가",
    "자동태그",
    "커스텀태그",
    "메모"
]

# Streamlit 설정
STREAMLIT_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🎵",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 음악 분석 설정
ANALYSIS_SETTINGS = {
    "sample_rate": 22050,  # librosa 기본 샘플레이트
    "n_mfcc": 13,          # MFCC 계수 개수
    "hop_length": 512,     # FFT 윈도우 간격
}

# 사용자 평가 옵션
RATING_OPTIONS = [1, 2, 3, 4, 5]

# 날짜 형식
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_DISPLAY_FORMAT = "%Y년 %m월 %d일"

# ========================================
# API Keys (선택적)
# ========================================

# AcoustID - 음악 지문 인식
ACOUSTID_API_KEY = os.getenv('ACOUSTID_API_KEY', '')

# Last.fm - 태그, 장르 정보
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY', '')
LASTFM_API_SECRET = os.getenv('LASTFM_API_SECRET', '')

# Gemini AI - 기분 기반 플레이리스트 (선택)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Spotify - Spotify 음악 분석 (선택)
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')

# API 사용 가능 여부 확인
def is_api_available(api_name):
    """API 키가 설정되어 있는지 확인"""
    api_keys = {
        'acoustid': ACOUSTID_API_KEY,
        'lastfm': LASTFM_API_KEY and LASTFM_API_SECRET,
        'gemini': GEMINI_API_KEY,
        'spotify': SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
    }
    return bool(api_keys.get(api_name.lower(), False))
