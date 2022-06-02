import streamlit as st
import pandas as pd  
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import common as cm

def run_ml():
    #pass
    st.header('품목별 평균가격 예측')

    st.text_area('예측율을 높이는 조건',disabled=True
                ,value='1.정확한 데이터가 많아야 한다.\n' +
                        '2.일자(년도)별 데이터수가 균일해야 한다.\n' +
                        '예) 상추가 데이터가 제일 많으며, 2008년~2019년도 사이의 데이터건수가 비슷하다.')

    col1, col2, col3 = st.columns(3)
    with col1:
        choice_item=st.selectbox('예측 품목 선택', cm.df_item_list, key='selectbox_2')
        year_list=sorted(cm.df.loc[(cm.df['품목명']==choice_item),'가격등록년도'].unique())
    with col2:
        choice_from_year=st.selectbox('From가격등록년도 선택', year_list, key='selectbox_3')
    with col3:
        choice_to_year=st.selectbox('To가격등록년도 선택', year_list, key='selectbox_4')
    
    n_years = st.slider('예측 년수 선택',1,4,4,key='slider_1')
    n_days_period = n_years * 365

    submitted = st.button(label='실행', key='button_1')
    if submitted:
        if choice_to_year >= choice_from_year: 
            txt_info=st.info('학습데이터 추출 중입니다. 잠시 기다려 주세요...')
            prophet_df = cm.df.loc[ (cm.df['품목명']==choice_item) & (cm.df['가격등록년도']>=choice_from_year) & (cm.df['가격등록년도']<=choice_to_year)
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

            st.write(f'' + choice_item + ' ' + str(choice_from_year) + '~' + str(choice_to_year) + '년도 데이터로 예측 ' + str(n_years) + '년 그래프')
            fig1 = plot_plotly(prophet, forecast, xlabel='가격등록일자', ylabel='평균가격')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.write(f'예측 components')
            fig2=prophet.plot_components(forecast)
            st.write(fig2)

        else:
            st.error('From가격등록년도가 To가격등록년도 보다 클 수 없습니다.')