import streamlit as st

from app_eda import run_eda

st.set_page_config(
   page_title='친환경농산물 소매가격 예측',
   page_icon='data/icon.png',
   layout='wide',
   initial_sidebar_state='expanded',
)

def main():
    #pass
    st.title('친환경농산물 소매가격 예측 (Facebook Prophet 라이브러리)')
    run_eda()

if __name__=='__main__':
    main()