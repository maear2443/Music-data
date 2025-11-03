"""
음악 메타데이터 관리 시스템 - 배치 업로드 프로세서
여러 곡을 한번에 처리하는 시스템
"""

import os
import tempfile
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import logging

import config
from audio_analyzer import get_analyzer
from database import get_database

# 로거 설정
logging.basicConfig(
    filename='batch_upload.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class BatchProcessor:
    """배치 음악 처리 프로세서"""

    def __init__(self):
        """초기화"""
        self.db = get_database()
        self.analyzer = get_analyzer()
        self.logger = logging.getLogger(__name__)

        # 처리 상태
        self.total_files = 0
        self.processed_files = 0
        self.success_count = 0
        self.failed_count = 0

        # 결과 저장
        self.results = {
            'success': [],
            'failed': [],
            'duplicates': []
        }

    def find_music_files_in_folder(self, folder_path: str, recursive: bool = True) -> List[str]:
        """
        폴더에서 음악 파일 찾기

        Args:
            folder_path: 폴더 경로
            recursive: 하위 폴더도 검색할지 여부

        Returns:
            음악 파일 경로 리스트
        """
        music_files = []

        if not os.path.exists(folder_path):
            self.logger.error(f"폴더가 존재하지 않음: {folder_path}")
            return music_files

        if recursive:
            # 하위 폴더까지 재귀 검색
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in config.SUPPORTED_AUDIO_FORMATS):
                        full_path = os.path.join(root, file)
                        music_files.append(full_path)
        else:
            # 현재 폴더만
            for file in os.listdir(folder_path):
                full_path = os.path.join(folder_path, file)
                if os.path.isfile(full_path):
                    if any(file.lower().endswith(ext) for ext in config.SUPPORTED_AUDIO_FORMATS):
                        music_files.append(full_path)

        self.logger.info(f"폴더에서 {len(music_files)}개 음악 파일 발견")
        return music_files

    def check_duplicate(self, filename: str) -> bool:
        """
        중복 파일 확인 (파일명 기반)

        Args:
            filename: 파일명

        Returns:
            중복 여부
        """
        all_music = self.db.get_all_music()
        for music in all_music:
            if music['filename'] == filename:
                return True
        return False

    def analyze_text_for_tags(self, text: str) -> List[str]:
        """
        텍스트(프롬프트/가사)에서 태그 추출

        Args:
            text: 분석할 텍스트

        Returns:
            추출된 태그 리스트
        """
        if not text:
            return []

        text_lower = text.lower()
        tags = []

        # 분위기 키워드
        mood_keywords = {
            'upbeat': ['upbeat', 'cheerful', 'happy', 'bright', '밝은', '경쾌'],
            'sad': ['sad', 'melancholic', 'lonely', '슬픈', '우울', '쓸쓸'],
            'romantic': ['love', 'romantic', '사랑', '로맨틱'],
            'dark': ['dark', 'mysterious', 'haunting', '어두운', '미스터리'],
            'chill': ['chill', 'relax', 'calm', '차분', '평온', '여유'],
            'energetic': ['energetic', 'powerful', 'intense', '에너지', '강렬'],
            'dreamy': ['dreamy', 'ethereal', 'ambient', '몽환', '환상']
        }

        # 장르 키워드
        genre_keywords = {
            'kpop': ['k-pop', 'kpop', '케이팝'],
            'electronic': ['electronic', 'edm', 'synth', 'techno', '일렉'],
            'rock': ['rock', 'guitar', 'punk', '록'],
            'jazz': ['jazz', 'blues', 'swing', '재즈'],
            'hiphop': ['hip-hop', 'hiphop', 'rap', '힙합', '랩'],
            'ballad': ['ballad', '발라드']
        }

        # 템포 키워드
        tempo_keywords = {
            'fast': ['fast', 'quick', 'rapid', '빠른', '신속'],
            'slow': ['slow', 'gentle', '느린', '천천히']
        }

        # 악기 키워드
        instrument_keywords = {
            'piano': ['piano', 'keys', '피아노'],
            'guitar': ['guitar', '기타'],
            'drums': ['drums', 'percussion', '드럼'],
            'synth': ['synth', 'synthesizer', '신디사이저']
        }

        # 키워드 매칭
        for tag, keywords in {**mood_keywords, **genre_keywords, **tempo_keywords, **instrument_keywords}.items():
            for keyword in keywords:
                if keyword in text_lower:
                    tags.append(tag)
                    break

        return list(set(tags))  # 중복 제거

    def process_single_file(
        self,
        file_path: str,
        common_data: Dict,
        individual_data: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        단일 파일 처리

        Args:
            file_path: 파일 경로
            common_data: 공통 정보 (스타일, 평가 등)
            individual_data: 개별 정보 (프롬프트, 가사)

        Returns:
            (성공 여부, 메시지)
        """
        filename = os.path.basename(file_path)

        try:
            # 1. 중복 확인
            if self.check_duplicate(filename):
                self.logger.warning(f"중복 파일 건너뜀: {filename}")
                self.results['duplicates'].append(filename)
                return False, "중복"

            # 2. 음악 분석
            self.logger.info(f"분석 시작: {filename}")
            analysis_result = self.analyzer.analyze(file_path)

            # 3. 개별 데이터 처리
            if individual_data is None:
                individual_data = {}

            # 프롬프트/가사에서 태그 추출
            text_tags = []
            if individual_data.get('prompt'):
                text_tags.extend(self.analyze_text_for_tags(individual_data['prompt']))
            if individual_data.get('lyrics'):
                text_tags.extend(self.analyze_text_for_tags(individual_data['lyrics']))

            # 4. 데이터 병합
            music_data = {
                'filename': filename,
                'file_path': file_path,
                'created_date': datetime.now().strftime(config.DATE_FORMAT),

                # 공통 정보
                'suno_style': common_data.get('style'),
                'user_rating': common_data.get('rating', 3),
                'user_memo': common_data.get('memo'),

                # 개별 정보
                'suno_prompt': individual_data.get('prompt'),
                'lyrics': individual_data.get('lyrics'),

                # 분석 결과
                'bpm': analysis_result['bpm'],
                'duration': analysis_result['duration'],
                'genre': analysis_result['genre'],
                'mood': analysis_result['mood'],
                'energy_level': analysis_result['energy_level'],
                'brightness': analysis_result['brightness'],
                'has_vocal': analysis_result['has_vocal'],

                # 태그
                'auto_tags': analysis_result['auto_tags'],
                'custom_tags': list(set(
                    common_data.get('tags', []) +
                    text_tags +
                    individual_data.get('tags', [])
                ))
            }

            # 5. 데이터베이스 저장
            music_id = self.db.add_music(music_data)
            self.logger.info(f"저장 완료: {filename} (ID: {music_id})")

            self.results['success'].append({
                'filename': filename,
                'id': music_id
            })

            return True, f"성공 (ID: {music_id})"

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"처리 실패: {filename} - {error_msg}")

            self.results['failed'].append({
                'filename': filename,
                'error': error_msg
            })

            return False, error_msg

    def process_batch(
        self,
        file_paths: List[str],
        common_data: Dict,
        individual_data_list: Optional[List[Dict]] = None,
        progress_callback=None
    ) -> Dict:
        """
        배치 처리 메인 함수

        Args:
            file_paths: 파일 경로 리스트
            common_data: 공통 정보
            individual_data_list: 개별 정보 리스트 (파일별)
            progress_callback: 진행률 콜백 함수

        Returns:
            처리 결과 딕셔너리
        """
        self.total_files = len(file_paths)
        self.processed_files = 0
        self.success_count = 0
        self.failed_count = 0

        # 결과 초기화
        self.results = {
            'success': [],
            'failed': [],
            'duplicates': []
        }

        self.logger.info(f"배치 처리 시작: {self.total_files}개 파일")

        for idx, file_path in enumerate(file_paths):
            # 개별 데이터 가져오기
            individual_data = None
            if individual_data_list and idx < len(individual_data_list):
                individual_data = individual_data_list[idx]

            # 파일 처리
            success, message = self.process_single_file(
                file_path,
                common_data,
                individual_data
            )

            # 카운터 업데이트
            self.processed_files += 1
            if success:
                self.success_count += 1
            else:
                self.failed_count += 1

            # 진행률 콜백
            if progress_callback:
                progress = self.processed_files / self.total_files
                progress_callback(
                    progress=progress,
                    current=self.processed_files,
                    total=self.total_files,
                    filename=os.path.basename(file_path),
                    status=message
                )

        self.logger.info(
            f"배치 처리 완료: "
            f"성공 {self.success_count}, "
            f"실패 {self.failed_count}, "
            f"중복 {len(self.results['duplicates'])}"
        )

        return {
            'total': self.total_files,
            'success': self.success_count,
            'failed': self.failed_count,
            'duplicates': len(self.results['duplicates']),
            'details': self.results
        }

    def get_error_log(self) -> str:
        """오류 로그 가져오기"""
        try:
            with open('batch_upload.log', 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "로그 파일 없음"

    def clear_log(self):
        """로그 파일 초기화"""
        try:
            with open('batch_upload.log', 'w', encoding='utf-8') as f:
                f.write('')
            self.logger.info("로그 초기화")
        except:
            pass


# 싱글톤 인스턴스
_processor_instance = None

def get_batch_processor() -> BatchProcessor:
    """배치 프로세서 인스턴스 가져오기"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = BatchProcessor()
    return _processor_instance
