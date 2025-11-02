"""
음악 메타데이터 관리 시스템 - 음악 분석 엔진
librosa를 사용한 자동 음악 분석
"""

import librosa
import numpy as np
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

import config


class AudioAnalyzer:
    """음악 파일을 분석하는 클래스"""

    def __init__(self):
        """분석기 초기화"""
        self.sample_rate = config.ANALYSIS_SETTINGS['sample_rate']
        self.n_mfcc = config.ANALYSIS_SETTINGS['n_mfcc']
        self.hop_length = config.ANALYSIS_SETTINGS['hop_length']

    def analyze(self, audio_path: str) -> Dict:
        """
        음악 파일 전체 분석

        Args:
            audio_path: 음악 파일 경로

        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 오디오 로드
            y, sr = librosa.load(audio_path, sr=self.sample_rate)

            # 각종 분석 수행
            analysis_result = {
                'bpm': self._analyze_bpm(y, sr),
                'duration': self._analyze_duration(y, sr),
                'genre': self._analyze_genre(y, sr),
                'mood': self._analyze_mood(y, sr),
                'energy_level': self._analyze_energy(y, sr),
                'brightness': self._analyze_brightness(y, sr),
                'has_vocal': self._detect_vocal(y, sr),
                'auto_tags': []
            }

            # 자동 태그 생성
            analysis_result['auto_tags'] = self._generate_auto_tags(analysis_result)

            return analysis_result

        except Exception as e:
            print(f"음악 분석 중 오류 발생: {e}")
            return self._get_default_result()

    def _analyze_bpm(self, y: np.ndarray, sr: int) -> float:
        """BPM 분석"""
        try:
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            return round(float(tempo), 1)
        except:
            return 120.0  # 기본값

    def _analyze_duration(self, y: np.ndarray, sr: int) -> float:
        """곡 길이 분석 (초 단위)"""
        return round(float(len(y) / sr), 2)

    def _analyze_genre(self, y: np.ndarray, sr: int) -> str:
        """
        장르 추정 (간단한 휴리스틱 기반)
        실제로는 머신러닝 모델을 사용할 수 있지만, 여기서는 간단한 규칙 기반
        """
        try:
            # MFCC 특성 추출
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
            mfcc_mean = np.mean(mfcc, axis=1)

            # 스펙트럴 센트로이드
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_centroid_mean = np.mean(spectral_centroids)

            # 제로 크로싱 레이트
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            zcr_mean = np.mean(zcr)

            # 템포
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

            # 간단한 규칙 기반 장르 분류
            if tempo > 140 and zcr_mean > 0.1:
                return "Electronic"
            elif tempo < 90 and spectral_centroid_mean < 2000:
                return "Jazz"
            elif tempo > 120 and spectral_centroid_mean > 3000:
                return "Rock"
            elif 90 <= tempo <= 120:
                return "Pop"
            else:
                return "Other"

        except:
            return "Other"

    def _analyze_mood(self, y: np.ndarray, sr: int) -> str:
        """
        분위기 분석
        에너지와 발랜스(밝기)를 기반으로 분위기 결정
        """
        try:
            energy = self._analyze_energy(y, sr)
            brightness = self._analyze_brightness(y, sr)

            # 2D 그리드로 분위기 결정
            if energy > 60:
                if brightness > 60:
                    return "upbeat"
                elif brightness < 40:
                    return "aggressive"
                else:
                    return "energetic"
            elif energy < 40:
                if brightness > 60:
                    return "cheerful"
                elif brightness < 40:
                    return "melancholic"
                else:
                    return "calm"
            else:
                if brightness > 60:
                    return "dreamy"
                elif brightness < 40:
                    return "dark"
                else:
                    return "relaxing"

        except:
            return "calm"

    def _analyze_energy(self, y: np.ndarray, sr: int) -> int:
        """
        에너지 레벨 분석 (0-100)
        RMS 에너지 기반
        """
        try:
            rms = librosa.feature.rms(y=y)[0]
            rms_mean = np.mean(rms)

            # 정규화 (0-100 범위로)
            # 일반적인 RMS 값 범위를 고려하여 스케일링
            energy = min(100, int(rms_mean * 1000))
            return max(0, energy)

        except:
            return 50  # 기본값

    def _analyze_brightness(self, y: np.ndarray, sr: int) -> int:
        """
        밝기 분석 (0-100)
        스펙트럴 센트로이드 기반
        """
        try:
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            centroid_mean = np.mean(spectral_centroids)

            # 정규화 (0-100 범위로)
            # 일반적인 센트로이드 값 범위 (0-8000Hz)를 고려
            brightness = int((centroid_mean / 8000) * 100)
            return min(100, max(0, brightness))

        except:
            return 50  # 기본값

    def _detect_vocal(self, y: np.ndarray, sr: int) -> int:
        """
        보컬 감지 (0: 없음, 1: 있음)
        하모닉/퍼커시브 분리를 사용한 간단한 휴리스틱
        """
        try:
            # 하모닉/퍼커시브 분리
            y_harmonic, y_percussive = librosa.effects.hpss(y)

            # 하모닉 성분의 강도
            harmonic_strength = np.mean(librosa.feature.rms(y=y_harmonic)[0])
            percussive_strength = np.mean(librosa.feature.rms(y=y_percussive)[0])

            # 하모닉 성분이 강하면 보컬이 있을 가능성이 높음
            if harmonic_strength > percussive_strength * 0.7:
                return 1
            else:
                return 0

        except:
            return 0  # 기본값: 없음

    def _generate_auto_tags(self, analysis_result: Dict) -> List[str]:
        """분석 결과를 바탕으로 자동 태그 생성"""
        tags = []

        # BPM 기반 태그
        bpm = analysis_result['bpm']
        for (min_bpm, max_bpm), tag in config.BPM_TAG_MAPPING.items():
            if min_bpm <= bpm < max_bpm:
                tags.append(tag)
                break

        # 에너지 기반 태그
        energy = analysis_result['energy_level']
        for (min_energy, max_energy), tag in config.ENERGY_TAG_MAPPING.items():
            if min_energy <= energy < max_energy:
                tags.append(tag)
                break

        # 장르 태그
        if analysis_result['genre']:
            tags.append(analysis_result['genre'].lower())

        # 분위기 태그
        if analysis_result['mood']:
            tags.append(analysis_result['mood'])

        # 보컬 태그
        if analysis_result['has_vocal']:
            tags.append("vocal")
        else:
            tags.append("instrumental")

        # 밝기 태그
        brightness = analysis_result['brightness']
        if brightness > 70:
            tags.append("bright")
        elif brightness < 30:
            tags.append("dark")

        return tags

    def _get_default_result(self) -> Dict:
        """분석 실패 시 기본값 반환"""
        return {
            'bpm': 120.0,
            'duration': 0.0,
            'genre': "Other",
            'mood': "calm",
            'energy_level': 50,
            'brightness': 50,
            'has_vocal': 0,
            'auto_tags': ["unknown"]
        }

    def get_audio_info(self, audio_path: str) -> str:
        """음악 파일의 기본 정보를 문자열로 반환"""
        try:
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            duration = len(y) / sr

            info = f"샘플레이트: {sr}Hz\n"
            info += f"길이: {duration:.2f}초\n"
            info += f"샘플 수: {len(y)}\n"

            return info

        except Exception as e:
            return f"정보 로드 실패: {e}"


# 싱글톤 인스턴스
_analyzer_instance = None

def get_analyzer() -> AudioAnalyzer:
    """분석기 인스턴스 가져오기"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = AudioAnalyzer()
    return _analyzer_instance
