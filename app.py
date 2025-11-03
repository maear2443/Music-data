"""
음악 메타데이터 관리 시스템 - 메인 애플리케이션
Streamlit 기반 웹 UI
"""

import streamlit as st
import os
import shutil
import tempfile
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

# 로컬 모듈 임포트
import config
from database import get_database
from audio_analyzer import get_analyzer
from excel_exporter import get_exporter
from batch_processor import get_batch_processor
from mood_playlist_generator import get_mood_generator


# 페이지 설정
st.set_page_config(**config.STREAMLIT_CONFIG)

# 데이터베이스 및 분석기 초기화
db = get_database()
analyzer = get_analyzer()
exporter = get_exporter()
batch_processor = get_batch_processor()
mood_generator = get_mood_generator()


def main():
    """메인 함수"""
    # 헤더
    st.title(config.APP_NAME)
    st.markdown(f"*버전 {config.APP_VERSION}* | Suno AI 음악 메타데이터 관리")

    # 사이드바
    show_sidebar()

    # 메인 탭
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎵 음악 추가",
        "📁 배치 업로드",
        "📋 음악 목록",
        "📊 통계",
        "🤖 AI 플레이리스트",
        "📥 내보내기"
    ])

    with tab1:
        show_add_music_tab()

    with tab2:
        show_batch_upload_tab()

    with tab3:
        show_music_list_tab()

    with tab4:
        show_statistics_tab()

    with tab5:
        show_ai_playlist_tab()

    with tab6:
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

        # 파일 임시 저장 (Windows 호환)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
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
                try:
                    # 음악 데이터 준비
                    analysis_result = st.session_state['analysis_result']

                    music_data = {
                        'filename': uploaded_file.name,
                        'file_path': temp_path,
                        'created_date': datetime.now().strftime(config.DATE_FORMAT),
                        'suno_style': suno_style if suno_style else None,
                        'suno_prompt': suno_prompt if suno_prompt else None,
                        'lyrics': lyrics if lyrics else None,
                        'user_rating': user_rating,
                        'user_memo': user_memo if user_memo else None,
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
                    st.info(f"📁 파일 위치: {temp_path}")

                    # 세션 상태 초기화
                    if 'analysis_result' in st.session_state:
                        del st.session_state['analysis_result']

                    st.balloons()

                except Exception as e:
                    st.error(f"❌ 저장 실패: {str(e)}")
                    st.error("데이터베이스 연결 또는 저장 중 오류가 발생했습니다.")


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


def show_batch_upload_tab():
    """배치 업로드 탭 - 여러 곡 한번에 추가"""
    st.header("📁 여러 곡 한번에 추가")

    st.markdown("""
    **배치 업로드 기능:**
    - 여러 음악 파일 동시 업로드 (최대 100개)
    - 폴더 전체 업로드
    - 개별 곡마다 프롬프트/가사 입력 가능
    - 자동 중복 감지
    - 실시간 진행률 표시
    """)

    # 업로드 방식 선택
    upload_mode = st.radio(
        "업로드 방식 선택",
        ["📎 파일 선택 (다중)", "📂 폴더 경로 입력"],
        horizontal=True
    )

    files_to_process = []

    if upload_mode == "📎 파일 선택 (다중)":
        # 파일 업로더 (다중 선택)
        uploaded_files = st.file_uploader(
            "음악 파일 선택 (여러 개 가능)",
            type=['mp3', 'wav', 'm4a', 'flac'],
            accept_multiple_files=True,
            help="Ctrl/Cmd + 클릭으로 여러 파일 선택 가능"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)}개 파일 선택됨")

            # 임시 파일로 저장
            temp_dir = tempfile.gettempdir()
            for uploaded_file in uploaded_files:
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # 중복 경로 방지
                if temp_path not in files_to_process:
                    files_to_process.append(temp_path)

    else:
        # 폴더 경로 입력
        folder_path = st.text_input(
            "📂 폴더 경로 입력",
            placeholder="예: C:\\Music\\Suno_Songs 또는 /home/user/music",
            help="폴더 안의 모든 음악 파일을 찾습니다"
        )

        recursive = st.checkbox("하위 폴더도 검색", value=True)

        if folder_path and st.button("🔍 폴더 스캔"):
            if os.path.exists(folder_path):
                files_to_process = batch_processor.find_music_files_in_folder(
                    folder_path,
                    recursive=recursive
                )
                if files_to_process:
                    st.success(f"✅ {len(files_to_process)}개 음악 파일 발견!")
                else:
                    st.warning("음악 파일을 찾을 수 없습니다.")
            else:
                st.error("폴더가 존재하지 않습니다.")

    # 파일 목록 표시
    if files_to_process:
        st.divider()
        st.subheader("📋 업로드할 파일 목록")

        # 파일 목록 데이터프레임
        file_df = pd.DataFrame({
            '번호': range(1, len(files_to_process) + 1),
            '파일명': [os.path.basename(f) for f in files_to_process],
            '상태': ['대기 중'] * len(files_to_process)
        })
        st.dataframe(file_df, use_container_width=True, hide_index=True)

        st.divider()

        # 공통 정보 입력
        st.subheader("📝 공통 정보 (모든 곡에 적용)")

        col1, col2 = st.columns(2)

        with col1:
            common_style = st.text_input("공통 스타일", placeholder="예: K-pop, Electronic")
            common_rating = st.select_slider("공통 평가", options=config.RATING_OPTIONS, value=3)

        with col2:
            common_tags_input = st.text_input(
                "공통 태그",
                placeholder="태그1, 태그2, 태그3",
                help="쉼표로 구분"
            )
            common_memo = st.text_area("공통 메모", placeholder="선택사항")

        common_tags = [t.strip() for t in common_tags_input.split(',')] if common_tags_input else []

        # 개별 정보 입력 옵션
        st.divider()
        use_individual = st.checkbox(
            "📝 각 곡마다 프롬프트/가사 입력하기",
            help="체크하면 각 곡마다 다른 정보를 입력할 수 있습니다"
        )

        individual_data_list = []

        if use_individual:
            st.info("각 곡의 프롬프트와 가사를 입력하세요. 비워두면 공통 정보만 사용됩니다.")

            if len(files_to_process) > 20:
                st.warning(f"⚠️ {len(files_to_process)}개 파일이 있습니다. 페이지가 길어질 수 있으니 확장 패널을 접어서 사용하세요.")

            with st.expander("📝 개별 정보 입력", expanded=False):
                for idx, file_path in enumerate(files_to_process):  # 모든 파일 표시
                    filename = os.path.basename(file_path)
                    st.markdown(f"**{idx+1}. {filename}**")

                    col1, col2 = st.columns(2)

                    with col1:
                        prompt = st.text_area(
                            f"프롬프트 #{idx+1}",
                            key=f"prompt_{idx}",
                            placeholder="Suno 프롬프트",
                            height=100
                        )

                    with col2:
                        lyrics = st.text_area(
                            f"가사 #{idx+1}",
                            key=f"lyrics_{idx}",
                            placeholder="가사 (선택사항)",
                            height=100
                        )

                    individual_data_list.append({
                        'prompt': prompt if prompt else None,
                        'lyrics': lyrics if lyrics else None
                    })

                    st.divider()

        # 처리 시작 버튼
        st.divider()

        if st.button("🚀 모두 분석 및 저장", type="primary", use_container_width=True):
            # 공통 데이터 준비
            common_data = {
                'style': common_style if common_style else None,
                'rating': common_rating,
                'tags': common_tags,
                'memo': common_memo if common_memo else None
            }

            # 프로그레스 바
            progress_bar = st.progress(0)
            status_text = st.empty()
            result_container = st.empty()

            # 진행률 콜백
            def update_progress(progress, current, total, filename, status):
                progress_bar.progress(progress)
                status_text.text(f"처리 중: {filename} ({current}/{total}) - {status}")

            # 배치 처리 실행
            results = batch_processor.process_batch(
                file_paths=files_to_process,
                common_data=common_data,
                individual_data_list=individual_data_list if use_individual else None,
                progress_callback=update_progress
            )

            # 완료 메시지
            progress_bar.empty()
            status_text.empty()

            st.success(f"""
            ✅ 배치 업로드 완료!

            - 성공: {results['success']}개
            - 실패: {results['failed']}개
            - 중복: {results['duplicates']}개
            - 총: {results['total']}개
            """)

            # 실패한 파일 표시
            if results['failed'] > 0:
                with st.expander("❌ 실패한 파일 목록"):
                    for fail in results['details']['failed']:
                        st.error(f"- {fail['filename']}: {fail['error']}")

            # 중복 파일 표시
            if results['duplicates'] > 0:
                with st.expander("⚠️ 중복된 파일 (건너뜀)"):
                    for dup in results['details']['duplicates']:
                        st.warning(f"- {dup}")

            # 오류 로그 다운로드
            if results['failed'] > 0:
                st.divider()
                if st.button("📥 오류 로그 다운로드"):
                    log_content = batch_processor.get_error_log()
                    st.download_button(
                        label="💾 로그 다운로드",
                        data=log_content,
                        file_name=f"batch_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                        mime="text/plain"
                    )

            st.balloons()


def show_ai_playlist_tab():
    """AI 플레이리스트 탭 - Gemini AI 기반 기분 플레이리스트"""
    st.header("🤖 AI 기분 플레이리스트")

    # API 키 확인
    if not config.is_api_available('gemini'):
        st.warning("""
        ⚠️ Gemini API 키가 설정되지 않았습니다.

        **기본 키워드 기반 분석을 사용합니다.**

        더 정확한 AI 분석을 원하시면:
        1. https://aistudio.google.com/app/apikey 에서 API 키 발급
        2. .env 파일에 `GEMINI_API_KEY=...` 추가
        3. 앱 재시작

        📖 자세한 설명: API_SETUP_GUIDE.md 참고
        """)
    else:
        st.success("✅ Gemini AI가 활성화되었습니다!")

    st.markdown("""
    **AI가 당신의 기분을 분석하여 완벽한 플레이리스트를 만들어드립니다!**

    예시:
    - "오늘 비가 와서 우울해... 혼자 조용히 있고 싶어"
    - "헬스장 가는데 진짜 빡세게 운동하고 싶어!"
    - "보고서 써야 하는데 집중이 안 돼..."
    """)

    st.divider()

    # 기분 입력
    mood_text = st.text_area(
        "😊 지금 기분이나 상황을 자유롭게 적어주세요",
        placeholder="예: 오늘 날씨가 좋아서 기분이 너무 좋아! 신나는 음악 듣고 싶어",
        height=150,
        help="자세히 적을수록 AI가 더 정확한 플레이리스트를 만들어줍니다"
    )

    # 곡 수 선택
    num_songs = st.slider(
        "플레이리스트 곡 수",
        min_value=5,
        max_value=50,
        value=15,
        step=5
    )

    # 생성 버튼
    if st.button("✨ AI 플레이리스트 생성", type="primary", use_container_width=True):
        if not mood_text:
            st.error("기분이나 상황을 입력해주세요!")
        else:
            with st.spinner("AI가 당신의 기분을 분석하고 있습니다..."):
                # AI 분석
                playlist_data = mood_generator.generate_playlist_from_mood(
                    mood_text=mood_text,
                    num_songs=num_songs
                )

                # 결과 표시
                st.success("✅ AI 분석 완료!")

                st.divider()

                # 플레이리스트 정보
                st.subheader(f"🎵 {playlist_data['title']}")
                st.write(f"*{playlist_data['description']}*")

                st.divider()

                # 조건 설명
                st.subheader("📋 플레이리스트 조건")
                conditions_text = mood_generator.explain_conditions(playlist_data['conditions'])
                st.code(conditions_text)

                st.divider()

                # 조건에 맞는 곡 검색
                st.subheader("🔍 조건에 맞는 곡 찾기")

                matching_songs = db.search_music(**playlist_data['conditions'])

                if matching_songs:
                    # 요청한 곡 수만큼만
                    selected_songs = matching_songs[:playlist_data['num_songs']]

                    st.success(f"✅ {len(selected_songs)}개 곡 발견!")

                    # 곡 목록 표시
                    playlist_df = pd.DataFrame([{
                        'ID': s['id'],
                        '제목': s['filename'],
                        'BPM': f"{s['bpm']:.0f}" if s.get('bpm') else '',
                        '에너지': s.get('energy_level', ''),
                        '분위기': s.get('mood', ''),
                        '평가': '⭐' * s['user_rating'] if s.get('user_rating') else ''
                    } for s in selected_songs])

                    st.dataframe(playlist_df, use_container_width=True, hide_index=True)

                    # 플레이리스트 저장 (TODO: 나중에 구현)
                    st.info("💡 향후 업데이트: 플레이리스트 저장 기능 추가 예정")

                else:
                    st.warning("""
                    😢 조건에 맞는 곡을 찾을 수 없습니다.

                    **제안:**
                    - 더 많은 음악을 추가해보세요
                    - 조건을 조금 완화해보세요
                    """)

    st.divider()

    # 사용 예시
    with st.expander("💡 사용 팁"):
        st.markdown("""
        **효과적인 기분 표현 방법:**

        1. **구체적으로**
           - ❌ "슬퍼"
           - ✅ "이별 후 혼자 있는데 너무 외로워"

        2. **상황 설명**
           - ❌ "운동"
           - ✅ "헬스장에서 데드리프트 하는데 힘이 필요해"

        3. **감정 + 활동**
           - ✅ "비 오는 날 창가에서 책 읽고 싶어"
           - ✅ "친구들이랑 드라이브 가는데 신나는 음악 필요해"

        **AI가 분석하는 것들:**
        - 감정 (슬픔, 행복, 분노, 평온 등)
        - 에너지 레벨 (저, 중, 고)
        - 속도 (느림, 보통, 빠름)
        - 보컬 선호도
        - 분위기 (밝음, 어두움)
        """)


if __name__ == "__main__":
    main()
