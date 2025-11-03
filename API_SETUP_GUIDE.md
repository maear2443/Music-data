# 🔑 API 설정 가이드

음악 메타데이터 관리 시스템의 고급 기능을 위한 API 키 설정 방법입니다.

## ⚠️ 중요

**모든 API는 선택사항입니다!**
- API 키 없이도 기본 기능은 모두 작동합니다
- 원하는 API만 선택적으로 설정 가능
- 언제든지 추가/제거 가능

---

## 📋 API 목록 및 용도

| API | 용도 | 필수 여부 | 무료 여부 |
|-----|------|----------|----------|
| **Gemini AI** | 기분 기반 플레이리스트 AI 생성 | 선택 | ✅ 무료 (월 60회) |
| **AcoustID** | 음악 지문 인식, 메타데이터 자동 가져오기 | 권장 | ✅ 완전 무료 |
| **Last.fm** | 장르/태그 정보, 유사 곡 추천 | 권장 | ✅ 완전 무료 |
| **Spotify** | Spotify 음악 분석 (Suno 곡 불필요) | 선택 | ✅ 무료 |

---

## 🎨 1. Gemini AI (기분 기반 플레이리스트)

### 🎯 기능

**"오늘 비 와서 우울해..."** → AI가 자동으로:
- 플레이리스트 제목 생성: "🌧️ 빗소리와 함께하는 고요"
- 조건 자동 설정: 느린 BPM, 낮은 에너지, 차분한 분위기
- 몇 곡 추천할지 결정
- 완벽한 플레이리스트 자동 생성!

### 📝 발급 방법

1. **Google AI Studio 접속**
   ```
   https://makersuite.google.com/app/apikey
   또는
   https://aistudio.google.com/app/apikey
   ```

2. **Google 계정 로그인**

3. **"Get API Key" 또는 "Create API Key" 클릭**

4. **새 프로젝트 만들기 또는 기존 프로젝트 선택**
   - Name: "Music Metadata Manager" (아무거나)

5. **API Key 복사**
   - 형식: `AIzaSyA1b2C3d4E5f6G7h8I9j0K1L2M3N4O5P6Q`
   - ⚠️ 한 번만 표시되므로 바로 복사!

6. **무료 사용량**
   - ✅ 월 60회 API 호출 무료
   - 하루 2-3번 사용하면 충분
   - 신용카드 불필요

### 💾 .env 파일에 추가

```bash
GEMINI_API_KEY=여기에_복사한_키_붙여넣기
```

---

## 🎵 2. AcoustID (음악 지문 인식)

### 🎯 기능

- 음악 파일 "지문" 생성
- 자동으로 제목, 아티스트, 장르 인식
- MusicBrainz DB에서 메타데이터 가져오기

### 📝 발급 방법

1. **AcoustID 웹사이트 접속**
   ```
   https://acoustid.org/
   ```

2. **회원가입** (우측 상단 "Sign up")
   - Email만 필요

3. **로그인 후 "New Application" 페이지**
   ```
   https://acoustid.org/new-application
   ```

4. **정보 입력**
   - Name: "Music Metadata Manager"
   - Version: "1.0"
   - Email: (당신의 이메일)

5. **"Create" 클릭 → API Key 복사**
   - 형식: `8XaBELgH` (짧은 문자열)

6. **무료 사용량**
   - ✅ 완전 무료
   - 무제한 요청
   - 영구 사용 가능

### 💾 .env 파일에 추가

```bash
ACOUSTID_API_KEY=여기에_복사한_키_붙여넣기
```

---

## 🎧 3. Last.fm (태그, 장르 정보)

### 🎯 기능

- 풍부한 장르/태그 정보
- 유사 곡 추천
- 인기도 정보
- 커뮤니티 태그

### 📝 발급 방법

1. **Last.fm 웹사이트 접속**
   ```
   https://www.last.fm/
   ```

2. **회원가입** (우측 상단 "Sign up")

3. **API 계정 생성**
   ```
   https://www.last.fm/api/account/create
   ```

4. **정보 입력**
   - Application name: "Music Metadata Manager"
   - Application description: "Personal music management system"
   - Application homepage: (비워도 됨)
   - Callback URL: (비워도 됨)

5. **"Submit" 클릭**

6. **API Key와 Shared Secret 복사**
   - API Key: 긴 문자열 (예: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)
   - Shared Secret: 짧은 문자열 (예: `9m8n7o6p5q4r3s2t`)

7. **무료 사용량**
   - ✅ 완전 무료
   - 초당 5회 요청 제한 (충분함)

### 💾 .env 파일에 추가

```bash
LASTFM_API_KEY=여기에_API_Key_붙여넣기
LASTFM_API_SECRET=여기에_Shared_Secret_붙여넣기
```

---

## 🎼 4. Spotify (선택, Suno 곡에는 불필요)

### 🎯 기능

- Spotify에 있는 곡의 정확한 오디오 분석
- 댄스성, 에너지, 밸런스 등

### ⚠️ 주의

**Suno 생성 곡에는 사용 불가!**
- Suno 곡은 Spotify에 없음
- 건너뛰어도 됨

### 📝 발급 방법 (원하는 경우만)

1. **Spotify for Developers 접속**
   ```
   https://developer.spotify.com/dashboard
   ```

2. **"Log in with Spotify"**

3. **"Create an App"**
   - App name: "Music Metadata Manager"
   - App description: "Personal music manager"
   - Redirect URI: `http://localhost` (아무거나)

4. **Client ID와 Client Secret 복사**

### 💾 .env 파일에 추가

```bash
SPOTIFY_CLIENT_ID=여기에_Client_ID_붙여넣기
SPOTIFY_CLIENT_SECRET=여기에_Client_Secret_붙여넣기
```

---

## 💾 .env 파일 설정

### 1. .env 파일 생성

프로젝트 폴더에 `.env` 파일 생성:

```
C:\Users\YourName\Music-data\.env
```

### 2. API 키 입력

```bash
# 🎵 음악 메타데이터 관리 시스템 - API Keys

# Gemini AI (기분 기반 플레이리스트)
GEMINI_API_KEY=AIzaSyA1b2C3d4E5f6G7h8I9j0K1L2M3N4O5P6Q

# AcoustID (음악 지문 인식)
ACOUSTID_API_KEY=8XaBELgH

# Last.fm (태그, 장르)
LASTFM_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
LASTFM_API_SECRET=9m8n7o6p5q4r3s2t

# Spotify (선택)
# SPOTIFY_CLIENT_ID=your_client_id
# SPOTIFY_CLIENT_SECRET=your_client_secret
```

### 3. 보안 주의사항

```
⚠️ .env 파일은 절대 공유하지 마세요!
⚠️ Git에 올리지 마세요! (이미 .gitignore에 추가됨)
⚠️ 스크린샷 찍을 때 주의!
```

---

## ✅ 설정 확인

### 앱 실행 후 확인

1. **앱 실행**
   ```bash
   run.bat
   ```

2. **사이드바에서 확인**
   - ✅ 표시: API 키 정상 작동
   - ❌ 표시: API 키 없음 또는 오류

3. **기능 테스트**
   - **Gemini AI**: "🤖 AI 플레이리스트" 탭에서 기분 입력
   - **AcoustID**: 음악 추가 시 자동 메타데이터 가져오기
   - **Last.fm**: 자동 태그 생성 확인

---

## 🔧 문제 해결

### Gemini API 오류

**"API key not valid"**
```
해결:
1. API 키가 올바르게 복사되었는지 확인
2. https://aistudio.google.com/app/apikey 에서 재확인
3. .env 파일에 공백 없이 입력했는지 확인
```

**"Quota exceeded"**
```
해결:
- 월 60회 무료 사용량 초과
- 다음 달까지 대기 또는
- Gemini API 없이도 기본 분석 작동
```

### AcoustID 오류

**"No results found"**
```
정상입니다!
- Suno 생성 곡은 DB에 없을 수 있음
- 기본 분석으로 자동 전환
```

### Last.fm 오류

**"Invalid API key"**
```
해결:
1. API Key와 Secret 모두 입력했는지 확인
2. https://www.last.fm/api/accounts 에서 재확인
```

---

## 💡 추천 조합

### 초보자 (최소 설정)

```bash
# API 키 없이 사용
# 기본 기능만으로도 충분!
```

### 일반 사용자 (권장)

```bash
GEMINI_API_KEY=...  # AI 플레이리스트
ACOUSTID_API_KEY=... # 자동 인식
```

### 파워 유저 (전부 설정)

```bash
GEMINI_API_KEY=...
ACOUSTID_API_KEY=...
LASTFM_API_KEY=...
LASTFM_API_SECRET=...
```

---

## 🎉 완료!

API 키 설정이 완료되었습니다!

이제 다음 기능을 사용할 수 있습니다:
- ✅ 🤖 AI 기반 기분 플레이리스트
- ✅ 🎵 자동 음악 인식
- ✅ 🏷️ 풍부한 태그 정보
- ✅ 🎯 유사 곡 추천

즐거운 음악 관리 되세요! 🎵
