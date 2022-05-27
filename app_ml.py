from matplotlib import container
import streamlit as st
import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

def run_ml():
    #pass
    st.header('Facebook Prophet을 이용한 평균가격 예측')

    st.text_area('예측율을 높이는 조건',disabled=True
                ,value='1.정확한 데이터가 많아야 한다.\n' +
                        '2.일자(년도)별 데이터수가 균일해야 한다.\n' +
                        '예) 상추가 데이터가 제일 많으며, 2008년~2019년도 사이의 데이터건수가 비슷하다.')

    df = pd.read_csv('data/price_20210916.csv', index_col=0)

    #st.dataframe(df)
    col1, col2, col3 = st.columns(3)
    with col1:
        item_list=sorted(df['품목명'].unique())
        choice_item=st.selectbox('예측 품목 선택', item_list)
        year_list=sorted(df.loc[ (df['품목명']==choice_item),'가격등록년도'].unique())
    with col2:
        choice_from_year=st.selectbox('From가격등록년도 선택', year_list)
    with col3:
        choice_to_year=st.selectbox('To가격등록년도 선택', year_list)
    
    n_years = st.slider('예측 년수 선택',1,4,1)
    n_days_period = n_years * 365

    submitted = st.button(label='실행')

    if submitted:
        if choice_to_year >= choice_from_year: 
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            #prophet_df = df.loc[ (df['품목명']==choice_item) & (df['가격등록년도'].isin(choice_year)), ['가격등록일자', '평균가격']]
            prophet_df = df.loc[ (df['품목명']==choice_item) & (df['가격등록년도']>=choice_from_year) & (df['가격등록년도']<=choice_to_year)
                                ,['가격등록일자', '평균가격']]
            #st.dataframe(prophet_df)
            prophet_df.columns = ['ds', 'y']
            #txt_info.info('학습데이터 추출 완료.')
            prophet=Prophet()
            txt_info.info('학습 중입니다. 잠시 기다려 주세요...')
            prophet.fit(prophet_df)
            txt_info.info('학습 완료하여 예측 중입니다. 잠시 기다려 주세요...')
            future=prophet.make_future_dataframe(periods=n_days_period, freq='D')
            forecast=prophet.predict(future)
            txt_info.info('예측 완료.')

            st.subheader(choice_item + ' ' + str(choice_from_year) + '~' + str(choice_to_year) + '년도 데이터로 예측 ' + str(n_years) + '년 그래프')
            fig1 = plot_plotly(prophet, forecast)
            st.plotly_chart(fig1)
            
            st.subheader(f'예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)

        else:
            st.error('From가격등록년도가 To가격등록년도 보다 클 수 없습니다.')