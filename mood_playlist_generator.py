"""
음악 메타데이터 관리 시스템 - Gemini AI 기분 기반 플레이리스트 생성기
"""

import json
import re
from typing import Dict, List, Optional
import config


class MoodPlaylistGenerator:
    """Gemini AI를 사용한 기분 기반 플레이리스트 생성기"""

    def __init__(self):
        """초기화"""
        self.api_key = config.GEMINI_API_KEY
        self.is_available = config.is_api_available('gemini')

    def generate_playlist_from_mood(self, mood_text: str, num_songs: int = 10) -> Dict:
        """
        사용자의 기분/상황 텍스트로부터 플레이리스트 조건 생성

        Args:
            mood_text: 사용자가 입력한 기분/상황 (예: "오늘 비 와서 우울해")
            num_songs: 플레이리스트에 포함할 곡 수

        Returns:
            {
                'title': '플레이리스트 제목',
                'description': '설명',
                'conditions': {조건들},
                'num_songs': 곡 수
            }
        """

        if not self.is_available:
            # Gemini API 없을 때 기본 룰 기반 분석
            return self._fallback_analysis(mood_text, num_songs)

        try:
            # Gemini API 호출
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')

            # 프롬프트 작성
            prompt = self._create_analysis_prompt(mood_text, num_songs)

            # AI 분석 요청
            response = model.generate_content(prompt)
            result_text = response.text

            # JSON 파싱
            result = self._parse_ai_response(result_text)

            if result:
                return result
            else:
                return self._fallback_analysis(mood_text, num_songs)

        except Exception as e:
            print(f"Gemini API 오류: {e}")
            return self._fallback_analysis(mood_text, num_songs)

    def _create_analysis_prompt(self, mood_text: str, num_songs: int) -> str:
        """Gemini AI에게 전달할 프롬프트 생성"""

        prompt = f"""
당신은 음악 큐레이터입니다. 사용자의 기분/상황을 분석하여 플레이리스트를 만들어주세요.

사용자 입력: "{mood_text}"

다음 JSON 형식으로 정확히 응답해주세요:

{{
    "title": "감성적인 플레이리스트 제목 (이모지 포함)",
    "description": "이 플레이리스트에 대한 짧은 설명",
    "moods": ["분위기1", "분위기2"],
    "bpm_min": 최소BPM(숫자),
    "bpm_max": 최대BPM(숫자),
    "energy_min": 최소에너지(0-100),
    "energy_max": 최대에너지(0-100),
    "brightness_min": 최소밝기(0-100),
    "brightness_max": 최대밝기(0-100),
    "has_vocal": true/false/null (null이면 상관없음),
    "rating_min": 최소평가(1-5),
    "tags": ["태그1", "태그2"],
    "num_songs": {num_songs}
}}

분위기 옵션: {', '.join(config.MOOD_CATEGORIES)}

규칙:
- 사용자의 감정을 정확히 파악하세요
- 플레이리스트 제목은 창의적이고 감성적으로
- BPM은 분위기에 맞게 (슬픔: 60-90, 행복: 110-140, 운동: 130-160)
- 에너지는 상황에 맞게 (차분: 0-40, 중간: 40-70, 활동적: 70-100)
- 반드시 유효한 JSON만 응답하세요
"""

        return prompt

    def _parse_ai_response(self, response_text: str) -> Optional[Dict]:
        """AI 응답에서 JSON 추출 및 파싱"""

        try:
            # JSON 블록 찾기
            json_match = re.search(r'\{[\s\S]*\}', response_text)

            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)

                # 조건 객체 생성
                conditions = {}

                if result.get('bpm_min'):
                    conditions['bpm_min'] = result['bpm_min']
                if result.get('bpm_max'):
                    conditions['bpm_max'] = result['bpm_max']

                if result.get('energy_min') is not None:
                    conditions['energy_min'] = result['energy_min']
                if result.get('energy_max') is not None:
                    conditions['energy_max'] = result['energy_max']

                if result.get('brightness_min') is not None:
                    conditions['brightness_min'] = result['brightness_min']
                if result.get('brightness_max') is not None:
                    conditions['brightness_max'] = result['brightness_max']

                if result.get('moods'):
                    conditions['moods'] = result['moods']

                if result.get('has_vocal') is not None:
                    conditions['has_vocal'] = 1 if result['has_vocal'] else 0

                if result.get('rating_min'):
                    conditions['rating_min'] = result['rating_min']

                if result.get('tags'):
                    conditions['tags'] = result['tags']

                return {
                    'title': result.get('title', '나만의 플레이리스트'),
                    'description': result.get('description', ''),
                    'conditions': conditions,
                    'num_songs': result.get('num_songs', 10)
                }

        except Exception as e:
            print(f"JSON 파싱 오류: {e}")
            return None

        return None

    def _fallback_analysis(self, mood_text: str, num_songs: int) -> Dict:
        """
        Gemini API 없을 때 기본 키워드 기반 분석
        """

        mood_text_lower = mood_text.lower()

        # 기본값
        conditions = {}
        title = "나만의 플레이리스트"
        description = mood_text

        # 키워드 매핑
        sad_keywords = ['슬프', 'sad', '우울', '힘들', '이별', '외로', '그리워']
        happy_keywords = ['행복', 'happy', '기쁘', '즐거', '신나', '좋아']
        calm_keywords = ['차분', 'calm', '조용', '평화', '편안', '집중', '공부', '작업']
        energetic_keywords = ['운동', 'workout', '에너지', '활동', '춤', '파티']
        romantic_keywords = ['사랑', 'love', '로맨틱', '데이트']

        # 감정 분석
        if any(kw in mood_text_lower for kw in sad_keywords):
            title = "🌧️ 슬픈 날의 위로"
            conditions['moods'] = ['melancholic', 'calm']
            conditions['bpm_min'] = 60
            conditions['bpm_max'] = 90
            conditions['energy_max'] = 40
            conditions['brightness_max'] = 40

        elif any(kw in mood_text_lower for kw in happy_keywords):
            title = "☀️ 기분 좋은 하루"
            conditions['moods'] = ['upbeat', 'cheerful']
            conditions['bpm_min'] = 110
            conditions['bpm_max'] = 140
            conditions['energy_min'] = 60
            conditions['brightness_min'] = 60

        elif any(kw in mood_text_lower for kw in calm_keywords):
            title = "🎧 집중과 평온"
            conditions['moods'] = ['calm', 'relaxing']
            conditions['bpm_min'] = 70
            conditions['bpm_max'] = 110
            conditions['energy_max'] = 50
            conditions['has_vocal'] = 0  # instrumental

        elif any(kw in mood_text_lower for kw in energetic_keywords):
            title = "💪 에너제틱 부스터"
            conditions['moods'] = ['energetic', 'aggressive']
            conditions['bpm_min'] = 130
            conditions['bpm_max'] = 180
            conditions['energy_min'] = 70

        elif any(kw in mood_text_lower for kw in romantic_keywords):
            title = "💕 로맨틱한 순간"
            conditions['moods'] = ['romantic', 'dreamy']
            conditions['bpm_min'] = 80
            conditions['bpm_max'] = 120
            conditions['energy_min'] = 40
            conditions['energy_max'] = 70

        else:
            # 기본: 전체
            title = "🎵 " + mood_text[:20]
            conditions['rating_min'] = 3

        return {
            'title': title,
            'description': description,
            'conditions': conditions,
            'num_songs': num_songs
        }

    def explain_conditions(self, conditions: Dict) -> str:
        """조건을 사람이 읽기 쉽게 설명"""

        explanations = []

        if 'bpm_min' in conditions or 'bpm_max' in conditions:
            bpm_min = conditions.get('bpm_min', 0)
            bpm_max = conditions.get('bpm_max', 300)
            explanations.append(f"🎵 BPM: {bpm_min}-{bpm_max}")

        if 'energy_min' in conditions or 'energy_max' in conditions:
            energy_min = conditions.get('energy_min', 0)
            energy_max = conditions.get('energy_max', 100)
            explanations.append(f"⚡ 에너지: {energy_min}-{energy_max}")

        if 'brightness_min' in conditions or 'brightness_max' in conditions:
            bright_min = conditions.get('brightness_min', 0)
            bright_max = conditions.get('brightness_max', 100)
            explanations.append(f"💡 밝기: {bright_min}-{bright_max}")

        if 'moods' in conditions:
            moods = ', '.join(conditions['moods'])
            explanations.append(f"🎭 분위기: {moods}")

        if 'has_vocal' in conditions:
            vocal = "보컬 있음" if conditions['has_vocal'] == 1 else "인스트루멘탈"
            explanations.append(f"🎤 {vocal}")

        if 'rating_min' in conditions:
            explanations.append(f"⭐ 최소 평가: {conditions['rating_min']}점")

        if 'tags' in conditions:
            tags = ', '.join(conditions['tags'])
            explanations.append(f"🏷️ 태그: {tags}")

        return '\n'.join(explanations) if explanations else "조건 없음"


# 싱글톤 인스턴스
_generator_instance = None

def get_mood_generator() -> MoodPlaylistGenerator:
    """기분 기반 플레이리스트 생성기 인스턴스 가져오기"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = MoodPlaylistGenerator()
    return _generator_instance
