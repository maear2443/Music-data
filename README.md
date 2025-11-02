# 🎵 음악 메타데이터 관리 시스템

Suno AI로 생성한 음악들의 메타데이터를 체계적으로 관리하고 분석하는 개인용 프로그램입니다.

## ✨ 주요 기능

- **🎵 음악 자동 분석**: BPM, 장르, 분위기, 에너지 레벨 자동 감지
- **📝 메타데이터 관리**: Suno 정보, 가사, 프롬프트, 개인 메모 저장
- **🏷️ 태그 시스템**: 자동 태그 + 커스텀 태그
- **🔍 검색 & 필터**: 스타일, 분위기, BPM 범위로 검색
- **📊 통계 분석**: 스타일/분위기/태그별 분포 차트
- **📥 엑셀 내보내기**: 3개 시트로 구성된 상세한 엑셀 리포트

## 🛠️ 기술 스택

- **Python 3.9+**
- **Streamlit** - 웹 UI
- **librosa** - 음악 분석
- **SQLite** - 로컬 데이터베이스
- **openpyxl** - 엑셀 내보내기

## 📋 필수 요구사항

- Python 3.9 이상
- Windows 10/11, macOS, Linux
- 4GB 이상 RAM 권장
- 음악 파일: MP3, WAV, M4A, FLAC

## 🚀 설치 및 실행

### Windows 사용자

#### 1. 초기 설정 (처음 한 번만)

```bash
# 1. 프로젝트 폴더에서 터미널(cmd) 열기
cd C:\Users\YourName\Documents\Music-data

# 2. 가상환경 생성
python -m venv venv

# 3. 가상환경 활성화
venv\Scripts\activate

# 4. 라이브러리 설치
pip install -r requirements.txt
```

#### 2. 실행 (매번)

**방법 1: 배치 파일 (추천)**
- `run.bat` 파일을 더블클릭
- 자동으로 브라우저가 열림

**방법 2: 수동 실행**
```bash
venv\Scripts\activate
streamlit run app.py
```

#### 3. 바탕화면 단축키 만들기 (선택사항)

1. `run.bat` 우클릭 → 보내기 → 바탕화면 (바로가기)
2. 바로가기 이름 변경: "🎵 음악 라이브러리"

---

### macOS / Linux 사용자

#### 1. 초기 설정 (처음 한 번만)

```bash
# 1. 프로젝트 폴더로 이동
cd ~/Music-data

# 2. 가상환경 생성
python3 -m venv venv

# 3. 가상환경 활성화
source venv/bin/activate

# 4. 라이브러리 설치
pip install -r requirements.txt
```

#### 2. 실행 (매번)

**방법 1: 실행 스크립트 (추천)**
```bash
./run.sh
```

**방법 2: 수동 실행**
```bash
source venv/bin/activate
streamlit run app.py
```

---

## 📖 사용 방법

### 1. 음악 추가

1. **음악 추가** 탭 클릭
2. 음악 파일 업로드 (MP3, WAV 등)
3. Suno 정보 입력:
   - 스타일 (예: K-pop, Electronic)
   - 프롬프트
   - 가사 (선택사항)
   - 평가 (1-5)
   - 메모
4. **자동 분석 실행** 버튼 클릭
5. 분석 결과 확인
6. **저장** 버튼 클릭

### 2. 음악 관리

- **음악 목록** 탭에서 모든 음악 확인
- 상세보기로 개별 음악 정보 확인
- 삭제 버튼으로 음악 제거

### 3. 검색 & 필터

사이드바에서:
- 키워드 검색
- 스타일 선택
- 분위기 선택
- BPM 범위 설정

### 4. 통계 확인

- **통계** 탭에서 차트 확인
- 스타일별/분위기별/태그별 분포

### 5. 엑셀 내보내기

1. **내보내기** 탭 클릭
2. **엑셀 파일 생성** 버튼 클릭
3. 생성된 파일 다운로드

**생성되는 엑셀 파일 구조:**
- **Sheet1**: 음악 목록 (요약)
- **Sheet2**: 태그 분석 (통계)
- **Sheet3**: 상세 정보 (모든 메타데이터)

---

## 📁 프로젝트 구조

```
Music-data/
├── app.py                  # 메인 Streamlit 애플리케이션
├── config.py               # 설정 파일
├── database.py             # SQLite 데이터베이스 관리
├── audio_analyzer.py       # 음악 분석 엔진 (librosa)
├── excel_exporter.py       # 엑셀 내보내기
├── requirements.txt        # 필수 라이브러리 목록
├── run.bat                 # Windows 실행 스크립트
├── run.sh                  # Linux/Mac 실행 스크립트
├── music_data.db           # 로컬 데이터베이스 (자동 생성)
├── exports/                # 엑셀 파일 저장 폴더 (자동 생성)
└── venv/                   # 가상환경 (설치 시 생성)
```

---

## 🎯 음악 분석 상세

### 자동 분석 항목

| 항목 | 설명 | 범위 |
|------|------|------|
| **BPM** | 곡의 템포 (Beats Per Minute) | 60-200 |
| **장르** | 감지된 장르 | Pop, Rock, Electronic, Jazz 등 |
| **분위기** | 곡의 전체적인 느낌 | upbeat, calm, melancholic 등 |
| **에너지** | 곡의 에너지 레벨 | 0-100 |
| **밝기** | 스펙트럴 밝기 | 0-100 |
| **보컬** | 보컬 포함 여부 | 있음/없음 |

### 자동 생성 태그

분석 결과를 바탕으로 자동으로 태그가 생성됩니다:
- BPM 기반: `slow`, `moderate`, `fast`, `very_fast`
- 에너지 기반: `low_energy`, `medium_energy`, `high_energy`
- 장르 태그: `pop`, `rock`, `electronic` 등
- 분위기 태그: `upbeat`, `calm`, `dark` 등
- 보컬 태그: `vocal`, `instrumental`
- 밝기 태그: `bright`, `dark`

---

## 🔧 문제 해결

### "python을 찾을 수 없습니다"
- Python 3.9 이상 설치 필요
- [Python 공식 사이트](https://www.python.org/downloads/)에서 다운로드

### 라이브러리 설치 오류
```bash
# Windows: 관리자 권한으로 cmd 실행 후
pip install -r requirements.txt

# Mac/Linux:
pip3 install -r requirements.txt
```

### 포트 8501 이미 사용 중
```bash
streamlit run app.py --server.port 8502
```

### 음악 분석이 느림
- 첫 실행 시 librosa 모델 다운로드 (한 번만 발생)
- 긴 음악 파일(5분 이상)은 분석에 1-2분 소요 가능

### 가상환경 문제
```bash
# 가상환경 삭제 후 재생성
rmdir /s venv       # Windows
rm -rf venv         # Mac/Linux

# 다시 설치
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

---

## 💡 팁 & 트릭

### 효율적인 태그 사용법
- 커스텀 태그로 프로젝트/무드/용도 분류
- 예: `commercial`, `background`, `intro`, `outro`

### 검색 활용법
- 여러 조건을 조합하여 정확한 검색
- BPM 범위로 비슷한 템포의 곡 찾기

### 엑셀 활용법
- Sheet1: 빠른 검색 및 필터링
- Sheet2: 통계 분석 및 리포트 작성
- Sheet3: 상세 데이터 백업

---

## 📝 개발 정보

**버전**: 1.0.0
**개발 환경**: Python 3.9+
**라이선스**: 개인 사용

---

## 🙋 FAQ

**Q: 다른 음원(YouTube, Spotify 등)도 분석 가능한가요?**
A: 네, 로컬에 파일이 있으면 어떤 음악이든 분석 가능합니다.

**Q: 데이터베이스는 어디에 저장되나요?**
A: 프로젝트 폴더 내 `music_data.db` 파일에 저장됩니다.

**Q: 음악 파일 자체도 저장되나요?**
A: 아니요, 분석만 하고 경로만 저장합니다. 원본 파일은 이동하지 마세요.

**Q: 여러 컴퓨터에서 사용할 수 있나요?**
A: 데이터베이스 파일(`music_data.db`)을 복사하면 다른 컴퓨터에서도 사용 가능합니다.

**Q: 분석 결과가 부정확해요**
A: 음악 분석은 휴리스틱 기반이므로 100% 정확하지 않습니다. 필요 시 수동으로 수정하세요.

---

## 🎉 즐거운 음악 관리 되세요!

문제가 있거나 개선 제안이 있다면 이슈를 등록해주세요.
