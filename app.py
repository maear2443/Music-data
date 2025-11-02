"""
음악 메타데이터 관리 시스템 - 메인 애플리케이션
Streamlit 기반 웹 UI
"""

import streamlit as st
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

# 로컬 모듈 임포트
import config
from database import get_database
from audio_analyzer import get_analyzer
from excel_exporter import get_exporter


# 페이지 설정
st.set_page_config(**config.STREAMLIT_CONFIG)

# 데이터베이스 및 분석기 초기화
db = get_database()
analyzer = get_analyzer()
exporter = get_exporter()


def main():
    """메인 함수"""
    # 헤더
    st.title(config.APP_NAME)
    st.markdown(f"*버전 {config.APP_VERSION}* | Suno AI 음악 메타데이터 관리")

    # 사이드바
    show_sidebar()

    # 메인 탭
    tab1, tab2, tab3, tab4 = st.tabs(["🎵 음악 추가", "📋 음악 목록", "📊 통계", "📥 내보내기"])

    with tab1:
        show_add_music_tab()

    with tab2:
        show_music_list_tab()

    with tab3:
        show_statistics_tab()

    with tab4:
        show_export_tab()


def show_sidebar():
    """사이드바 표시"""
    with st.sidebar:
        st.header("🔍 검색 & 필터")

        # 검색어
        search_keyword = st.text_input("키워드 검색", placeholder="제목, 스타일, 메모 등...")

        # 스타일 필터
        all_music = db.get_all_music()
        styles = list(set([m.get('suno_style', '') for m in all_music if m.get('suno_style')]))
        selected_style = st.selectbox("스타일", ["전체"] + styles)

        # 분위기 필터
        selected_mood = st.selectbox("분위기", ["전체"] + config.MOOD_CATEGORIES)

        # BPM 범위
        st.subheader("BPM 범위")
        col1, col2 = st.columns(2)
        with col1:
            min_bpm = st.number_input("최소", min_value=0, max_value=300, value=0)
        with col2:
            max_bpm = st.number_input("최대", min_value=0, max_value=300, value=300)

        # 검색 버튼
        if st.button("🔍 검색", use_container_width=True):
            st.session_state['search_params'] = {
                'keyword': search_keyword if search_keyword else None,
                'style': selected_style if selected_style != "전체" else None,
                'mood': selected_mood if selected_mood != "전체" else None,
                'min_bpm': min_bpm if min_bpm > 0 else None,
                'max_bpm': max_bpm if max_bpm < 300 else None
            }
            st.rerun()

        # 초기화 버튼
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state['search_params'] = {}
            st.rerun()

        # 통계 요약
        st.divider()
        st.subheader("📈 라이브러리 요약")
        stats = db.get_statistics()
        st.metric("총 음악 수", stats.get('total_count', 0))
        if stats.get('avg_bpm'):
            st.metric("평균 BPM", f"{stats['avg_bpm']:.1f}")


def show_add_music_tab():
    """음악 추가 탭"""
    st.header("🎵 새 음악 추가")

    # 파일 업로드
    uploaded_file = st.file_uploader(
        "음악 파일 선택",
        type=['mp3', 'wav', 'm4a', 'flac'],
        help="MP3, WAV, M4A, FLAC 파일을 지원합니다."
    )

    if uploaded_file is not None:
        st.success(f"파일 선택됨: {uploaded_file.name}")

        # 파일 임시 저장
        temp_path = os.path.join("/tmp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Suno 정보 입력
        st.subheader("📝 Suno 정보")

        col1, col2 = st.columns(2)

        with col1:
            suno_style = st.text_input("스타일", placeholder="예: K-pop, Electronic, Jazz")
            user_rating = st.select_slider("평가", options=config.RATING_OPTIONS)

        with col2:
            suno_prompt = st.text_area("프롬프트", placeholder="Suno에 입력한 프롬프트를 입력하세요")

        lyrics = st.text_area("가사", placeholder="가사를 입력하세요 (선택사항)")
        user_memo = st.text_area("메모", placeholder="개인 메모를 입력하세요")

        # 커스텀 태그
        custom_tags_input = st.text_input(
            "커스텀 태그",
            placeholder="태그를 쉼표로 구분하여 입력 (예: favorite, workout, chill)"
        )
        custom_tags = [tag.strip() for tag in custom_tags_input.split(',')] if custom_tags_input else []

        # 자동 분석 버튼
        if st.button("🔍 자동 분석 실행", use_container_width=True):
            with st.spinner("음악 분석 중... (최대 1분 소요될 수 있습니다)"):
                analysis_result = analyzer.analyze(temp_path)
                st.session_state['analysis_result'] = analysis_result
                st.success("분석 완료!")

        # 분석 결과 표시
        if 'analysis_result' in st.session_state:
            st.subheader("🎯 자동 분석 결과")
            result = st.session_state['analysis_result']

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("BPM", f"{result['bpm']:.1f}")
                st.metric("에너지", f"{result['energy_level']}/100")

            with col2:
                st.metric("길이", f"{result['duration']:.2f}초")
                st.metric("밝기", f"{result['brightness']}/100")

            with col3:
                st.metric("장르", result['genre'])
                st.metric("보컬", "있음" if result['has_vocal'] else "없음")

            with col4:
                st.metric("분위기", result['mood'])

            # 자동 태그
            st.write("**자동 생성 태그:**", ", ".join(result['auto_tags']))

        # 저장 버튼
        if st.button("💾 저장", type="primary", use_container_width=True):
            if 'analysis_result' not in st.session_state:
                st.error("먼저 '자동 분석 실행'을 클릭하세요!")
            else:
                # 음악 데이터 준비
                analysis_result = st.session_state['analysis_result']

                music_data = {
                    'filename': uploaded_file.name,
                    'file_path': temp_path,
                    'created_date': datetime.now().strftime(config.DATE_FORMAT),
                    'suno_style': suno_style,
                    'suno_prompt': suno_prompt,
                    'lyrics': lyrics,
                    'user_rating': user_rating,
                    'user_memo': user_memo,
                    'bpm': analysis_result['bpm'],
                    'duration': analysis_result['duration'],
                    'genre': analysis_result['genre'],
                    'mood': analysis_result['mood'],
                    'energy_level': analysis_result['energy_level'],
                    'brightness': analysis_result['brightness'],
                    'has_vocal': analysis_result['has_vocal'],
                    'auto_tags': analysis_result['auto_tags'],
                    'custom_tags': custom_tags
                }

                # 데이터베이스에 저장
                music_id = db.add_music(music_data)

                st.success(f"✅ 음악이 저장되었습니다! (ID: {music_id})")

                # 세션 상태 초기화
                if 'analysis_result' in st.session_state:
                    del st.session_state['analysis_result']

                st.balloons()


def show_music_list_tab():
    """음악 목록 탭"""
    st.header("📋 음악 목록")

    # 검색 파라미터 가져오기
    search_params = st.session_state.get('search_params', {})

    # 음악 조회
    if search_params:
        music_list = db.search_music(**search_params)
        st.info(f"검색 결과: {len(music_list)}개")
    else:
        music_list = db.get_all_music()

    if not music_list:
        st.info("등록된 음악이 없습니다. '음악 추가' 탭에서 음악을 추가하세요.")
        return

    # 테이블 데이터 준비
    table_data = []
    for music in music_list:
        table_data.append({
            "ID": music['id'],
            "제목": music['filename'],
            "생성날짜": music['created_date'][:10] if music['created_date'] else "",
            "스타일": music.get('suno_style', ''),
            "BPM": f"{music['bpm']:.1f}" if music.get('bpm') else "",
            "분위기": music.get('mood', ''),
            "평가": "⭐" * music['user_rating'] if music.get('user_rating') else "",
            "태그": ", ".join(music.get('auto_tags', [])[:3])  # 처음 3개만
        })

    # DataFrame으로 표시
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 상세보기
    st.subheader("🔍 상세보기")
    selected_id = st.selectbox(
        "음악 선택",
        options=[m['id'] for m in music_list],
        format_func=lambda x: f"ID {x}: {next((m['filename'] for m in music_list if m['id'] == x), '')}"
    )

    if selected_id:
        music = db.get_music_by_id(selected_id)

        if music:
            col1, col2 = st.columns(2)

            with col1:
                st.write("**기본 정보**")
                st.write(f"- 파일명: {music['filename']}")
                st.write(f"- 생성일: {music.get('created_date', '')}")
                st.write(f"- 스타일: {music.get('suno_style', '')}")
                st.write(f"- 평가: {'⭐' * music['user_rating'] if music.get('user_rating') else '없음'}")

                st.write("**분석 결과**")
                st.write(f"- BPM: {music.get('bpm', 'N/A')}")
                st.write(f"- 길이: {music.get('duration', 'N/A')}초")
                st.write(f"- 장르: {music.get('genre', 'N/A')}")
                st.write(f"- 분위기: {music.get('mood', 'N/A')}")
                st.write(f"- 에너지: {music.get('energy_level', 'N/A')}/100")
                st.write(f"- 밝기: {music.get('brightness', 'N/A')}/100")
                st.write(f"- 보컬: {'있음' if music.get('has_vocal') else '없음'}")

            with col2:
                st.write("**Suno 정보**")
                st.write(f"- 프롬프트: {music.get('suno_prompt', '')}")

                if music.get('lyrics'):
                    st.write("**가사**")
                    st.text_area("", music['lyrics'], height=150, disabled=True, label_visibility="collapsed")

                if music.get('user_memo'):
                    st.write("**메모**")
                    st.text_area("", music['user_memo'], height=100, disabled=True, label_visibility="collapsed")

            # 태그
            st.write("**태그**")
            all_tags = music.get('auto_tags', []) + music.get('custom_tags', [])
            if all_tags:
                st.write(" • ".join([f"`{tag}`" for tag in all_tags]))
            else:
                st.write("태그 없음")

            # 삭제 버튼
            if st.button("🗑️ 이 음악 삭제", type="secondary"):
                if db.delete_music(selected_id):
                    st.success("음악이 삭제되었습니다.")
                    st.rerun()
                else:
                    st.error("삭제 실패")


def show_statistics_tab():
    """통계 탭"""
    st.header("📊 통계")

    stats = db.get_statistics()

    # 기본 통계
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("총 음악 수", stats.get('total_count', 0))

    with col2:
        avg_bpm = stats.get('avg_bpm', 0)
        st.metric("평균 BPM", f"{avg_bpm:.1f}" if avg_bpm else "N/A")

    with col3:
        # 가장 많이 사용된 스타일
        style_dist = stats.get('style_distribution', [])
        top_style = style_dist[0]['suno_style'] if style_dist else "없음"
        st.metric("인기 스타일", top_style)

    st.divider()

    # 스타일 분포
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("스타일별 곡 수")
        style_dist = stats.get('style_distribution', [])
        if style_dist:
            style_df = pd.DataFrame(style_dist)
            st.bar_chart(style_df.set_index('suno_style')['count'])
        else:
            st.info("데이터 없음")

    with col2:
        st.subheader("분위기별 곡 수")
        mood_dist = stats.get('mood_distribution', [])
        if mood_dist:
            mood_df = pd.DataFrame(mood_dist)
            st.bar_chart(mood_df.set_index('mood')['count'])
        else:
            st.info("데이터 없음")

    # 태그 분포
    st.subheader("자주 사용되는 태그 (상위 15개)")
    tag_dist = stats.get('tag_distribution', [])[:15]
    if tag_dist:
        tag_df = pd.DataFrame(tag_dist)
        st.bar_chart(tag_df.set_index('tag')['count'])
    else:
        st.info("데이터 없음")


def show_export_tab():
    """내보내기 탭"""
    st.header("📥 엑셀 내보내기")

    st.write("""
    음악 라이브러리를 엑셀 파일로 내보냅니다.

    **포함 내용:**
    - Sheet1: 음악 목록 (요약)
    - Sheet2: 태그 분석 (통계)
    - Sheet3: 상세 정보 (모든 메타데이터)
    """)

    # 내보내기 옵션
    music_list = db.get_all_music()
    stats = db.get_statistics()

    st.metric("내보낼 음악 수", len(music_list))

    if st.button("📥 엑셀 파일 생성", type="primary", use_container_width=True):
        if not music_list:
            st.error("내보낼 음악이 없습니다.")
        else:
            with st.spinner("엑셀 파일 생성 중..."):
                try:
                    filepath = exporter.export(music_list, stats)
                    st.success(f"✅ 엑셀 파일이 생성되었습니다!")
                    st.info(f"저장 위치: {filepath}")

                    # 파일 다운로드 버튼
                    with open(filepath, "rb") as file:
                        st.download_button(
                            label="📥 다운로드",
                            data=file,
                            file_name=os.path.basename(filepath),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"엑셀 생성 실패: {e}")

    # 내보내기 미리보기
    if music_list:
        st.subheader("📋 내보내기 미리보기 (처음 10개)")
        preview_data = []
        for music in music_list[:10]:
            preview_data.append({
                "ID": music['id'],
                "제목": music['filename'],
                "스타일": music.get('suno_style', ''),
                "BPM": music.get('bpm', ''),
                "분위기": music.get('mood', ''),
                "평가": music.get('user_rating', '')
            })

        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
