import streamlit as st
import pandas as pd
import numpy as np

# 페이지 타이틀 설정
st.title('Challenge Health Diary')

# 사용자 이름 및 주차 입력
name = st.sidebar.text_input('이름')
week = st.sidebar.number_input('주차', min_value=1)

# 파일 업로드 기능
uploaded_file = st.sidebar.file_uploader("사진 업로드", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Meal Photo', use_column_width=True)

# 요일별 식사 기록 섹션
st.header(f'{week}주차 식사 일지')
days_of_week = ['월', '화', '수', '목', '금', '토', '일']
columns = st.columns(7)

meal_data = {}
water_intake_data = {}
sleep_data = {}
stress_data = {}

for i, day in enumerate(days_of_week):
    with columns[i]:
        st.subheader(day)
        meal_data[day] = st.text_area('식사 기록', key=f'meal_{day}')
        water_intake_data[day] = st.number_input('물 섭취량(L)', min_value=0.0, max_value=10.0, step=0.1, key=f'water_{day}')
        sleep_data[day] = st.number_input('수면 시간(시간)', min_value=0, max_value=24, key=f'sleep_{day}')
        stress_data[day] = st.slider(f'{day} 스트레스 지수', 0, 10, 1, key=f'stress_{day}')

# 스트레스 지수 데이터 시각화
st.header('주간 스트레스 지수 변화')

# DataFrame을 생성하고 요일 순으로 정렬합니다.
days_order = ['월', '화', '수', '목', '금', '토', '일']
stress_df = pd.DataFrame(list(stress_data.items()), columns=['Day', 'Stress Level'])
stress_df['Day'] = pd.Categorical(stress_df['Day'], categories=days_order, ordered=True)
stress_df = stress_df.sort_values('Day')

# 인덱스를 다시 설정합니다.
stress_df.set_index('Day', inplace=True)

# Streamlit으로 라인 차트를 생성합니다.
st.line_chart(stress_df)

# 나의 건강소감 및 목표 섹션
st.header('나의 건강소감 및 목표')
health_notes = st.text_area('건강소감', key='health_notes')
goals = st.text_area('이번 주 목표', key='goals')

# 데이터 분석 및 시각화 섹션
st.header('몸 상태 분석')

# 데이터를 데이터프레임으로 변환
df_sleep = pd.DataFrame.from_dict(sleep_data, orient='index', columns=['수면 시간'])
df_stress = pd.DataFrame.from_dict(stress_data, orient='index', columns=['스트레스 지수'])

# 분석 로직: 충분한 수면을 취하지 않았고 스트레스 지수가 높은 날을 탐색
poor_condition_days = df_stress[(df_sleep['수면 시간'] < 7) & (df_stress['스트레스 지수'] > 5)].index.tolist()

# 분석 결과 시각화
st.write(f"수면 부족 및 스트레스가 높은 날: {', '.join(poor_condition_days) if poor_condition_days else '없음'}")


# 데이터를 CSV로 다운로드
if st.button('데이터 저장'):
    df_meals = pd.DataFrame.from_dict(meal_data, orient='index').transpose()
    df_water = pd.DataFrame.from_dict(water_intake_data, orient='index').transpose()
    
    df = pd.concat([df_meals, df_water, df_sleep, df_stress], axis=1)
    df['건강소감'] = health_notes
    df['목표'] = goals
    
    st.download_button(label='Download data as CSV',
                       data=df.to_csv(index=False).encode('utf-8'),
                       file_name=f'{name}_week_{week}_health_diary.csv',
                       mime='text/csv')

# Streamlit 앱을 실행하려면 이 스크립트를 저장하고, 터미널에서 `streamlit run your_script.py` 명
