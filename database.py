"""
음악 메타데이터 관리 시스템 - 데이터베이스 관리
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import config


class MusicDatabase:
    """음악 메타데이터를 관리하는 SQLite 데이터베이스 클래스"""

    def __init__(self, db_path: str = config.DB_PATH):
        """데이터베이스 초기화"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """데이터베이스 연결"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Dict 형태로 결과 반환
        self.cursor = self.conn.cursor()

    def _create_tables(self):
        """테이블 생성"""
        # 음악 메타데이터 테이블
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS music (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                created_date TEXT NOT NULL,

                -- Suno 정보 (사용자 입력)
                suno_style TEXT,
                suno_prompt TEXT,
                lyrics TEXT,
                user_rating INTEGER,
                user_memo TEXT,

                -- 자동 분석
                bpm REAL,
                duration REAL,
                genre TEXT,
                mood TEXT,
                energy_level INTEGER,
                brightness INTEGER,
                has_vocal INTEGER,

                -- 태그 (JSON 배열로 저장)
                auto_tags TEXT,
                custom_tags TEXT,

                -- 메타데이터
                updated_date TEXT
            )
        ''')

        # 태그 통계 테이블 (선택적)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT UNIQUE NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        ''')

        self.conn.commit()

    def add_music(self, music_data: Dict) -> int:
        """음악 추가"""
        now = datetime.now().strftime(config.DATE_FORMAT)

        # 리스트를 JSON 문자열로 변환
        auto_tags = json.dumps(music_data.get('auto_tags', []))
        custom_tags = json.dumps(music_data.get('custom_tags', []))

        self.cursor.execute('''
            INSERT INTO music (
                filename, file_path, created_date,
                suno_style, suno_prompt, lyrics, user_rating, user_memo,
                bpm, duration, genre, mood, energy_level, brightness, has_vocal,
                auto_tags, custom_tags, updated_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            music_data.get('filename'),
            music_data.get('file_path'),
            music_data.get('created_date', now),
            music_data.get('suno_style'),
            music_data.get('suno_prompt'),
            music_data.get('lyrics'),
            music_data.get('user_rating'),
            music_data.get('user_memo'),
            music_data.get('bpm'),
            music_data.get('duration'),
            music_data.get('genre'),
            music_data.get('mood'),
            music_data.get('energy_level'),
            music_data.get('brightness'),
            music_data.get('has_vocal', 0),
            auto_tags,
            custom_tags,
            now
        ))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_music(self) -> List[Dict]:
        """모든 음악 조회"""
        self.cursor.execute('SELECT * FROM music ORDER BY created_date DESC')
        rows = self.cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_music_by_id(self, music_id: int) -> Optional[Dict]:
        """ID로 음악 조회"""
        self.cursor.execute('SELECT * FROM music WHERE id = ?', (music_id,))
        row = self.cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def update_music(self, music_id: int, music_data: Dict) -> bool:
        """음악 정보 업데이트"""
        now = datetime.now().strftime(config.DATE_FORMAT)

        # 리스트를 JSON 문자열로 변환
        if 'auto_tags' in music_data:
            music_data['auto_tags'] = json.dumps(music_data['auto_tags'])
        if 'custom_tags' in music_data:
            music_data['custom_tags'] = json.dumps(music_data['custom_tags'])

        # 동적으로 UPDATE 쿼리 생성
        fields = []
        values = []
        for key, value in music_data.items():
            if key != 'id':
                fields.append(f"{key} = ?")
                values.append(value)

        fields.append("updated_date = ?")
        values.append(now)
        values.append(music_id)

        query = f"UPDATE music SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

        return self.cursor.rowcount > 0

    def delete_music(self, music_id: int) -> bool:
        """음악 삭제"""
        self.cursor.execute('DELETE FROM music WHERE id = ?', (music_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def search_music(self,
                     keyword: Optional[str] = None,
                     style: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     min_bpm: Optional[float] = None,
                     max_bpm: Optional[float] = None,
                     mood: Optional[str] = None) -> List[Dict]:
        """음악 검색"""
        query = "SELECT * FROM music WHERE 1=1"
        params = []

        if keyword:
            query += " AND (filename LIKE ? OR suno_style LIKE ? OR user_memo LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])

        if style:
            query += " AND suno_style LIKE ?"
            params.append(f"%{style}%")

        if tags:
            for tag in tags:
                query += " AND (auto_tags LIKE ? OR custom_tags LIKE ?)"
                params.extend([f"%{tag}%", f"%{tag}%"])

        if min_bpm is not None:
            query += " AND bpm >= ?"
            params.append(min_bpm)

        if max_bpm is not None:
            query += " AND bpm <= ?"
            params.append(max_bpm)

        if mood:
            query += " AND mood = ?"
            params.append(mood)

        query += " ORDER BY created_date DESC"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_statistics(self) -> Dict:
        """통계 데이터 조회"""
        stats = {}

        # 총 음악 수
        self.cursor.execute('SELECT COUNT(*) as count FROM music')
        stats['total_count'] = self.cursor.fetchone()['count']

        # 평균 BPM
        self.cursor.execute('SELECT AVG(bpm) as avg_bpm FROM music WHERE bpm IS NOT NULL')
        stats['avg_bpm'] = self.cursor.fetchone()['avg_bpm']

        # 스타일별 분포
        self.cursor.execute('''
            SELECT suno_style, COUNT(*) as count
            FROM music
            WHERE suno_style IS NOT NULL
            GROUP BY suno_style
            ORDER BY count DESC
        ''')
        stats['style_distribution'] = [dict(row) for row in self.cursor.fetchall()]

        # 분위기별 분포
        self.cursor.execute('''
            SELECT mood, COUNT(*) as count
            FROM music
            WHERE mood IS NOT NULL
            GROUP BY mood
            ORDER BY count DESC
        ''')
        stats['mood_distribution'] = [dict(row) for row in self.cursor.fetchall()]

        # 태그 통계
        all_tags = {}
        self.cursor.execute('SELECT auto_tags, custom_tags FROM music')
        for row in self.cursor.fetchall():
            for tag_field in ['auto_tags', 'custom_tags']:
                tags_json = row[tag_field]
                if tags_json:
                    tags = json.loads(tags_json)
                    for tag in tags:
                        all_tags[tag] = all_tags.get(tag, 0) + 1

        stats['tag_distribution'] = sorted(
            [{'tag': k, 'count': v} for k, v in all_tags.items()],
            key=lambda x: x['count'],
            reverse=True
        )

        return stats

    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Row 객체를 Dict로 변환"""
        if row is None:
            return None

        data = dict(row)

        # JSON 문자열을 리스트로 변환
        if data.get('auto_tags'):
            try:
                data['auto_tags'] = json.loads(data['auto_tags'])
            except:
                data['auto_tags'] = []
        else:
            data['auto_tags'] = []

        if data.get('custom_tags'):
            try:
                data['custom_tags'] = json.loads(data['custom_tags'])
            except:
                data['custom_tags'] = []
        else:
            data['custom_tags'] = []

        return data

    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """소멸자"""
        self.close()


# 싱글톤 인스턴스 (Streamlit에서 사용)
_db_instance = None

def get_database() -> MusicDatabase:
    """데이터베이스 인스턴스 가져오기"""
    global _db_instance
    if _db_instance is None:
        _db_instance = MusicDatabase()
    return _db_instance
