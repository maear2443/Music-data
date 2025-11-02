"""
음악 메타데이터 관리 시스템 - 엑셀 내보내기
openpyxl을 사용한 고급 엑셀 내보내기 (조건부 서식, 필터 등)
"""

import os
from datetime import datetime
from typing import List, Dict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

import config


class ExcelExporter:
    """음악 데이터를 엑셀로 내보내는 클래스"""

    def __init__(self):
        """엑셀 내보내기 초기화"""
        # 내보내기 디렉토리 생성
        if not os.path.exists(config.EXCEL_EXPORT_DIR):
            os.makedirs(config.EXCEL_EXPORT_DIR)

    def export(self, music_data: List[Dict], statistics: Dict) -> str:
        """
        음악 데이터를 엑셀 파일로 내보내기

        Args:
            music_data: 음악 데이터 리스트
            statistics: 통계 데이터

        Returns:
            생성된 엑셀 파일 경로
        """
        # 워크북 생성
        wb = Workbook()

        # Sheet1: 전체 음악 목록
        self._create_music_list_sheet(wb, music_data)

        # Sheet2: 태그 분석
        self._create_tag_analysis_sheet(wb, statistics)

        # Sheet3: 상세 정보
        self._create_detail_sheet(wb, music_data)

        # 기본 시트 삭제 (생성 시 자동으로 만들어진 빈 시트)
        if 'Sheet' in wb.sheetnames:
            del wb['Sheet']

        # 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"음악_라이브러리_{timestamp}.xlsx"
        filepath = os.path.join(config.EXCEL_EXPORT_DIR, filename)

        wb.save(filepath)
        return filepath

    def _create_music_list_sheet(self, wb: Workbook, music_data: List[Dict]):
        """Sheet1: 전체 음악 목록"""
        ws = wb.active
        ws.title = "음악 목록"

        # 헤더
        headers = [
            "ID", "제목", "생성날짜", "스타일", "BPM", "길이(초)",
            "장르", "분위기", "에너지", "밝기", "보컬", "평가",
            "자동태그", "커스텀태그", "메모"
        ]

        # 헤더 스타일
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

        # 데이터 입력
        for row_num, music in enumerate(music_data, 2):
            ws.cell(row=row_num, column=1, value=music.get('id'))
            ws.cell(row=row_num, column=2, value=music.get('filename'))
            ws.cell(row=row_num, column=3, value=music.get('created_date'))
            ws.cell(row=row_num, column=4, value=music.get('suno_style'))
            ws.cell(row=row_num, column=5, value=music.get('bpm'))
            ws.cell(row=row_num, column=6, value=music.get('duration'))
            ws.cell(row=row_num, column=7, value=music.get('genre'))
            ws.cell(row=row_num, column=8, value=music.get('mood'))
            ws.cell(row=row_num, column=9, value=music.get('energy_level'))
            ws.cell(row=row_num, column=10, value=music.get('brightness'))
            ws.cell(row=row_num, column=11, value="있음" if music.get('has_vocal') else "없음")
            ws.cell(row=row_num, column=12, value=music.get('user_rating'))

            # 태그를 문자열로 변환
            auto_tags = ", ".join(music.get('auto_tags', []))
            custom_tags = ", ".join(music.get('custom_tags', []))
            ws.cell(row=row_num, column=13, value=auto_tags)
            ws.cell(row=row_num, column=14, value=custom_tags)
            ws.cell(row=row_num, column=15, value=music.get('user_memo'))

        # 열 너비 자동 조정
        self._auto_adjust_column_width(ws)

        # 필터 추가
        ws.auto_filter.ref = ws.dimensions

        # 테두리 추가
        self._add_borders(ws, len(music_data) + 1, len(headers))

        # 틀 고정 (헤더 행)
        ws.freeze_panes = "A2"

    def _create_tag_analysis_sheet(self, wb: Workbook, statistics: Dict):
        """Sheet2: 태그 분석"""
        ws = wb.create_sheet(title="태그 분석")

        # 제목
        ws['A1'] = "📊 태그 분석"
        ws['A1'].font = Font(bold=True, size=14)

        # 기본 통계
        ws['A3'] = "총 음악 수:"
        ws['B3'] = statistics.get('total_count', 0)
        ws['A4'] = "평균 BPM:"
        ws['B4'] = round(statistics.get('avg_bpm', 0), 1) if statistics.get('avg_bpm') else 0

        # 스타일 분포
        ws['A6'] = "스타일별 곡 수"
        ws['A6'].font = Font(bold=True, size=12)

        style_dist = statistics.get('style_distribution', [])
        ws['A7'] = "스타일"
        ws['B7'] = "곡 수"

        for idx, item in enumerate(style_dist, 8):
            ws[f'A{idx}'] = item.get('suno_style', 'Unknown')
            ws[f'B{idx}'] = item.get('count', 0)

        # 분위기 분포
        start_row = 8 + len(style_dist) + 2
        ws[f'A{start_row}'] = "분위기별 곡 수"
        ws[f'A{start_row}'].font = Font(bold=True, size=12)

        ws[f'A{start_row + 1}'] = "분위기"
        ws[f'B{start_row + 1}'] = "곡 수"

        mood_dist = statistics.get('mood_distribution', [])
        for idx, item in enumerate(mood_dist):
            row = start_row + 2 + idx
            ws[f'A{row}'] = item.get('mood', 'Unknown')
            ws[f'B{row}'] = item.get('count', 0)

        # 태그 분포 (상위 20개)
        tag_start_row = start_row + len(mood_dist) + 4
        ws[f'A{tag_start_row}'] = "자주 사용되는 태그 (상위 20개)"
        ws[f'A{tag_start_row}'].font = Font(bold=True, size=12)

        ws[f'A{tag_start_row + 1}'] = "태그"
        ws[f'B{tag_start_row + 1}'] = "사용 횟수"

        tag_dist = statistics.get('tag_distribution', [])[:20]
        for idx, item in enumerate(tag_dist):
            row = tag_start_row + 2 + idx
            ws[f'A{row}'] = item.get('tag', 'Unknown')
            ws[f'B{row}'] = item.get('count', 0)

        # 열 너비 조정
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 15

    def _create_detail_sheet(self, wb: Workbook, music_data: List[Dict]):
        """Sheet3: 상세 정보"""
        ws = wb.create_sheet(title="상세 정보")

        # 모든 필드를 포함한 상세 정보
        headers = [
            "ID", "파일명", "파일경로", "생성날짜", "수정날짜",
            "Suno 스타일", "Suno 프롬프트", "가사",
            "BPM", "길이(초)", "장르", "분위기",
            "에너지 레벨", "밝기", "보컬 여부",
            "사용자 평가", "사용자 메모",
            "자동 태그", "커스텀 태그"
        ]

        # 헤더 스타일
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.font = header_font
            cell.fill = header_fill

        # 데이터 입력
        for row_num, music in enumerate(music_data, 2):
            ws.cell(row=row_num, column=1, value=music.get('id'))
            ws.cell(row=row_num, column=2, value=music.get('filename'))
            ws.cell(row=row_num, column=3, value=music.get('file_path'))
            ws.cell(row=row_num, column=4, value=music.get('created_date'))
            ws.cell(row=row_num, column=5, value=music.get('updated_date'))
            ws.cell(row=row_num, column=6, value=music.get('suno_style'))
            ws.cell(row=row_num, column=7, value=music.get('suno_prompt'))
            ws.cell(row=row_num, column=8, value=music.get('lyrics'))
            ws.cell(row=row_num, column=9, value=music.get('bpm'))
            ws.cell(row=row_num, column=10, value=music.get('duration'))
            ws.cell(row=row_num, column=11, value=music.get('genre'))
            ws.cell(row=row_num, column=12, value=music.get('mood'))
            ws.cell(row=row_num, column=13, value=music.get('energy_level'))
            ws.cell(row=row_num, column=14, value=music.get('brightness'))
            ws.cell(row=row_num, column=15, value="있음" if music.get('has_vocal') else "없음")
            ws.cell(row=row_num, column=16, value=music.get('user_rating'))
            ws.cell(row=row_num, column=17, value=music.get('user_memo'))

            # 태그를 문자열로 변환
            auto_tags = ", ".join(music.get('auto_tags', []))
            custom_tags = ", ".join(music.get('custom_tags', []))
            ws.cell(row=row_num, column=18, value=auto_tags)
            ws.cell(row=row_num, column=19, value=custom_tags)

        # 열 너비 자동 조정
        self._auto_adjust_column_width(ws)

        # 필터 추가
        ws.auto_filter.ref = ws.dimensions

        # 틀 고정
        ws.freeze_panes = "A2"

    def _auto_adjust_column_width(self, ws):
        """열 너비 자동 조정"""
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted_width = min(max_length + 2, 50)  # 최대 50자
            ws.column_dimensions[column_letter].width = adjusted_width

    def _add_borders(self, ws, max_row: int, max_col: int):
        """테두리 추가"""
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        for row in range(1, max_row + 1):
            for col in range(1, max_col + 1):
                ws.cell(row=row, column=col).border = thin_border


# 싱글톤 인스턴스
_exporter_instance = None

def get_exporter() -> ExcelExporter:
    """엑셀 내보내기 인스턴스 가져오기"""
    global _exporter_instance
    if _exporter_instance is None:
        _exporter_instance = ExcelExporter()
    return _exporter_instance
