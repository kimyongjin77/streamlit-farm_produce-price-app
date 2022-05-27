import streamlit as st

import pandas as pd  
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

import platform
from matplotlib import font_manager, rc

from app_ml import run_ml

#print('This System=' + platform.system())
#print('This System=' + platform.platform())

plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Linux':
    #matplotlib의 폰트를 Nanum 폰트로 지정합니다.
    path = '/usr/share/fonts/nanum/NanumGothic.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('This System=' + platform.system() + ' Unknown system... sorry~~~~')

def run_eda():
    #pass
    st.header('한국농수산식품유통공사_친환경농산물 소매가격정보')
    st.text('친환경 농산물 가격정보에 대한 데이터 출처 공공데이터포털')
    link='[공공데이터포털](https://www.data.go.kr/data/15071816/fileData.do?recommendDataYn=Y)'
    st.markdown(link, unsafe_allow_html=True)

    st.subheader('친환경(유기농, 무농약) 농산물(21년 기준) 소매가격 정보')
    df = pd.read_csv('data/price_20210916.csv', index_col=0)
    st.dataframe(df)

    st.subheader('EDA')
    st.subheader('품목(' + str(df['품목명'].nunique()) + ')별 데이터수')
    col1, col2 = st.columns([1,3])
    with col1:
        #st.text('품목별 데이터수')
        df_temp=df['품목명'].value_counts().reset_index()
        df_temp.columns=['품목명', '데이터건수']
        st.dataframe(df_temp)

    with col2:
        my_order=df['품목명'].value_counts().sort_values(ascending=False).index
        fig1=plt.figure(figsize=(10,4))
        sns.countplot(data=df,x='품목명',order=my_order)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    st.subheader('가격등록일자별로 평균가격이 어떻게 변하는지 간단하게 확인')
    item_list=sorted(df['품목명'].unique())

    col1, _, _ = st.columns(3)
    with col1:
        choice_item=st.selectbox('품목 선택', item_list)
    
    col1, col2 = st.columns(2)
    with col1:
        st.text(choice_item + ' 평균가격 변동')
        fig1=plt.figure(figsize=(10,6))
        (df.loc[df['품목명']==choice_item,].groupby('가격등록일자')['평균가격'].mean()).plot()
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    with col2:
        st.text(choice_item + ' 가격등록년도별 데이터 건수')
        my_order=df.loc[df['품목명']==choice_item, '가격등록년도'].value_counts().sort_index().index
        fig1=plt.figure(figsize=(10,6))
        sns.countplot(data=df,x=df.loc[df['품목명']==choice_item, '가격등록년도'],order=my_order)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    run_ml()