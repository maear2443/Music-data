# 🎵 음악 메타데이터 관리 시스템

Suno AI로 생성한 음악들의 메타데이터를 체계적으로 관리하고 분석하는 **개인용 프로그램**입니다.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)

---

## 🌟 주요 기능

### 🎵 음악 관리
- **단일 곡 추가**: 상세한 메타데이터 입력
- **📁 배치 업로드**: 여러 곡 한번에 추가 (최대 100개)
- **폴더 업로드**: 폴더 전체를 한번에 스캔 및 추가
- **중복 감지**: 같은 파일 자동 필터링

### 🤖 AI 기능
- **AI 플레이리스트**: 기분/상황 입력 시 자동으로 플레이리스트 생성
- **자동 태그 생성**: 프롬프트/가사 분석으로 태그 자동 추출
- **음악 자동 분석**: BPM, 장르, 분위기, 에너지 레벨 감지

### 📊 분석 & 관리
- **검색 & 필터**: 스타일, 분위기, BPM 범위로 검색
- **통계 대시보드**: 스타일/분위기/태그별 분포 차트
- **엑셀 내보내기**: 3개 시트로 구성된 상세 리포트

### 🏷️ 메타데이터
- Suno 정보 (스타일, 프롬프트, 가사)
- 자동 태그 + 커스텀 태그
- 평가 및 개인 메모
- BPM, 장르, 분위기, 에너지, 밝기

---

## 🚀 빠른 시작 (Windows)

### 📥 1단계: 프로젝트 다운로드

```cmd
# Git으로 클론
git clone https://github.com/maear2443/Music-data.git
cd Music-data
```

또는 [ZIP 다운로드](https://github.com/maear2443/Music-data/archive/refs/heads/main.zip) 후 압축 해제

---

### ⚙️ 2단계: 설치 (처음 한 번만)

#### 방법 A: 자동 설치 스크립트 (추천!) ⭐

1. `install.bat` 파일을 **더블클릭**
2. 자동으로 모든 라이브러리 설치 (약 2-3분)
3. 완료!

#### 방법 B: 수동 설치

```cmd
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
venv\Scripts\activate

# 3. 라이브러리 설치
pip install -r requirements.txt
```

---

### 🎵 3단계: 실행

#### 방법 A: 원클릭 실행 (추천!) ⭐

`run.bat` 파일을 **더블클릭**
→ 브라우저가 자동으로 열림!

#### 방법 B: 수동 실행

```cmd
venv\Scripts\activate
streamlit run app.py
```

---

### 🔗 4단계: 바탕화면 바로가기 (선택)

1. `run.bat` 우클릭
2. **보내기** → **바탕화면 (바로가기)**
3. 바로가기 이름 변경: `🎵 음악 라이브러리`

이제 바탕화면에서 **더블클릭**으로 바로 실행! 🎉

---

## 📖 사용 방법

### 🎵 음악 추가 (단일)

1. **🎵 음악 추가** 탭 클릭
2. 음악 파일 업로드 (MP3, WAV, M4A, FLAC)
3. Suno 정보 입력:
   - 스타일 (예: K-pop, Electronic)
   - 프롬프트
   - 가사 (선택)
   - 평가 (1-5)
4. **🔍 자동 분석 실행** 클릭
5. 분석 결과 확인 후 **💾 저장**

---

### 📁 배치 업로드 (여러 곡 한번에) ⭐ 신기능!

1. **📁 배치 업로드** 탭 클릭
2. 업로드 방식 선택:
   - **파일 선택**: Ctrl 누르고 여러 파일 선택
   - **폴더 경로**: `C:\Music\Suno_Songs` 입력
3. **공통 정보** 입력 (모든 곡에 적용)
   - 스타일, 평가, 태그, 메모
4. (선택) **각 곡마다 프롬프트/가사 입력** 체크
   - 각 곡의 프롬프트와 가사 개별 입력
5. **🚀 모두 분석 및 저장** 클릭
6. 진행률 확인 및 완료!

**예시:**
```
폴더: C:\Music\Suno_2024
→ 50개 음악 파일 발견
→ 공통 스타일: "K-pop"
→ 공통 태그: "2024, new"
→ 개별 프롬프트: 각 곡마다 다르게 입력
→ 한 번에 모두 저장!
```

---

### 🤖 AI 플레이리스트 ⭐ 신기능!

1. **🤖 AI 플레이리스트** 탭 클릭
2. 기분/상황 입력창에 자유롭게 작성:
   ```
   예시:
   - "오늘 비가 와서 우울해... 혼자 조용히 있고 싶어"
   - "헬스장 가는데 진짜 빡세게 운동하고 싶어!"
   - "보고서 써야 하는데 집중이 안 돼..."
   ```
3. 플레이리스트 곡 수 선택 (5-50곡)
4. **✨ AI 플레이리스트 생성** 클릭
5. AI가 자동으로:
   - 플레이리스트 제목 생성
   - 최적 조건 설정 (BPM, 에너지, 분위기)
   - 라이브러리에서 자동으로 곡 검색

**결과 예시:**
```
입력: "비 와서 우울해..."
→ 제목: 🌧️ 빗소리와 함께하는 고요
→ 조건: BPM 60-90, 에너지 낮음, 차분한 분위기
→ 15곡 자동 선택
```

---

### 📊 통계 & 검색

#### 사이드바 (검색 & 필터)
- 키워드 검색
- 스타일 선택
- 분위기 선택
- BPM 범위 설정

#### 📊 통계 탭
- 총 음악 수, 평균 BPM
- 스타일별/분위기별 분포 차트
- 자주 사용되는 태그 Top 15

#### 📥 내보내기 탭
- 엑셀 파일 생성 (3개 시트)
- 다운로드 및 백업

---

## 🔑 API 설정 (선택사항)

**API 키 없이도 모든 기능 사용 가능!**
하지만 더 정확한 분석을 원하면 API 키를 설정하세요.

### 추천 API

| API | 용도 | 무료 |
|-----|------|------|
| **Gemini AI** | AI 플레이리스트 (더 정확) | ✅ 월 60회 |
| **AcoustID** | 음악 인식, 메타데이터 | ✅ 무제한 |
| **Last.fm** | 장르/태그 정보 | ✅ 무제한 |

### 설정 방법

1. **API 키 발급**
   - Gemini: https://aistudio.google.com/app/apikey
   - AcoustID: https://acoustid.org/new-application
   - Last.fm: https://www.last.fm/api/account/create

2. **.env 파일 생성**
   ```cmd
   # 프로젝트 폴더에 .env 파일 생성
   copy .env.example .env
   ```

3. **API 키 입력**
   ```bash
   # .env 파일 열기
   notepad .env

   # 내용 입력
   GEMINI_API_KEY=여기에_발급받은_키_붙여넣기
   ACOUSTID_API_KEY=여기에_발급받은_키_붙여넣기
   LASTFM_API_KEY=여기에_발급받은_키_붙여넣기
   LASTFM_API_SECRET=여기에_발급받은_시크릿_붙여넣기
   ```

4. **앱 재시작**
   ```cmd
   run.bat
   ```

📖 **자세한 설명**: [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) 참고

---

## 🛠️ 기술 스택

- **Python 3.9+** - 기본 언어
- **Streamlit** - 웹 UI 프레임워크
- **librosa** - 음악 분석 엔진
- **SQLite** - 로컬 데이터베이스
- **openpyxl** - 엑셀 내보내기
- **Gemini AI** - AI 플레이리스트 (선택)
- **python-dotenv** - 환경 변수 관리

---

## 📋 시스템 요구사항

### 필수
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.9 이상
- **RAM**: 4GB 이상 권장
- **저장공간**: 500MB 이상

### 지원 음악 파일
- MP3
- WAV
- M4A
- FLAC

---

## 📁 프로젝트 구조

```
Music-data/
├── app.py                      # 메인 애플리케이션
├── config.py                   # 설정 파일
├── database.py                 # 데이터베이스 관리
├── audio_analyzer.py           # 음악 분석 엔진
├── excel_exporter.py           # 엑셀 내보내기
├── batch_processor.py          # 배치 처리 시스템
├── mood_playlist_generator.py  # AI 플레이리스트
├── requirements.txt            # 라이브러리 목록
├── run.bat                     # Windows 실행 스크립트
├── install.bat                 # 자동 설치 스크립트
├── .env.example                # API 키 템플릿
├── API_SETUP_GUIDE.md          # API 설정 가이드
├── music_data.db               # 데이터베이스 (자동 생성)
└── exports/                    # 엑셀 파일 (자동 생성)
```

---

## 🔧 문제 해결

### "python을 찾을 수 없습니다"

**해결:**
1. [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.9+ 다운로드
2. 설치 시 **"Add Python to PATH"** 체크박스 필수!
3. 재설치 후 `python --version` 확인

---

### "ModuleNotFoundError: No module named 'XXX'"

**해결:**
```cmd
# 가상환경 활성화
venv\Scripts\activate

# 해당 모듈 설치
pip install XXX

# 또는 전체 재설치
pip install -r requirements.txt
```

---

### 포트 8501 이미 사용 중

**해결:**
```cmd
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

또는 실행 중인 앱 종료 후 재시작

---

### 음악 분석이 느림

**정상입니다!**
- 첫 실행 시 librosa 모델 다운로드 (1-2분)
- 긴 음악(5분+)은 분석에 1-2분 소요
- 배치 업로드 시 여러 곡은 더 오래 걸림

---

### 가상환경 오류

**해결:**
```cmd
# 가상환경 삭제
rmdir /s venv

# 다시 생성
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 💡 팁 & 트릭

### 효율적인 작업 흐름

1. **첫 사용**: 배치 업로드로 많은 곡 추가
2. **일상 사용**: 단일 곡 추가로 새 음악 관리
3. **플레이리스트**: AI로 기분 맞춤 재생 목록
4. **분석**: 통계 탭으로 라이브러리 인사이트
5. **백업**: 엑셀 내보내기로 정기 백업

### 태그 활용법

**자동 태그**: 음악 분석으로 자동 생성
- 예: `fast`, `high_energy`, `vocal`, `bright`

**커스텀 태그**: 용도별 분류
- 예: `workout`, `study`, `commercial`, `favorite`

**프롬프트/가사 태그**: 텍스트 분석으로 추출
- 프롬프트: "upbeat summer vibes" → `upbeat`, `summer`
- 가사: "사랑, 이별" → `romantic`, `sad`

### 검색 활용

**복합 검색**: 여러 조건 조합
```
예시:
- 스타일: "K-pop"
- BPM: 120-140
- 분위기: "upbeat"
- 평가: 4점 이상
→ 정확한 곡 찾기!
```

---

## 📊 데이터 구조

각 음악 레코드에 저장되는 정보:

```python
{
    # 기본 정보
    'filename': '곡_제목.mp3',
    'created_date': '2024-11-03 15:30:00',

    # Suno 정보 (사용자 입력)
    'suno_style': 'K-pop',
    'suno_prompt': '밝고 경쾌한 여름 노래',
    'lyrics': '가사 내용...',
    'user_rating': 5,
    'user_memo': '개인 메모',

    # 자동 분석
    'bpm': 128.5,
    'duration': 180.2,
    'genre': 'Pop',
    'mood': 'upbeat',
    'energy_level': 75,
    'brightness': 68,
    'has_vocal': True,

    # 태그
    'auto_tags': ['fast', 'high_energy', 'vocal', 'bright'],
    'custom_tags': ['favorite', 'summer', '2024']
}
```

---

## 🎯 향후 개발 계획

- [ ] Essentia AI 통합 (더 정확한 분석)
- [ ] 플레이리스트 저장 기능
- [ ] 내장 음악 플레이어
- [ ] 유사 곡 추천 시스템
- [ ] 자동 백업 스케줄
- [ ] 다크 모드

---

## ❓ FAQ

**Q: 음악 파일 자체도 저장되나요?**
A: 아니요. 파일 경로만 저장하므로 원본 파일을 이동하지 마세요.

**Q: API 키 없이 사용 가능한가요?**
A: 네! 모든 기본 기능은 API 없이 작동합니다. API는 더 정확한 분석을 위한 선택사항입니다.

**Q: 여러 컴퓨터에서 사용할 수 있나요?**
A: `music_data.db` 파일을 복사하면 다른 컴퓨터에서도 사용 가능합니다.

**Q: Suno 외 다른 음악도 분석 가능한가요?**
A: 네! 모든 음악 파일(MP3, WAV 등)을 분석할 수 있습니다.

**Q: 데이터가 외부로 전송되나요?**
A: 아니요. 모든 데이터는 로컬에만 저장됩니다. (API 사용 시 해당 API로만 요청)

---

## 📞 지원 & 기여

### 버그 리포트
GitHub Issues에서 버그를 리포트해주세요.

### 기능 제안
새로운 기능 아이디어가 있으면 Issues에 제안해주세요!

---

## 📄 라이선스

개인 사용 목적의 프로젝트입니다.

---

## 🎉 즐거운 음악 관리 되세요!

**제작**: Claude & maear2443
**버전**: 1.0.0
**최종 업데이트**: 2024-11-03

---

### 🌟 Star를 눌러주세요!

이 프로젝트가 도움이 되셨다면 ⭐ Star를 눌러주세요!
