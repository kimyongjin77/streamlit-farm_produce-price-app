import streamlit as st

from app_eda import run_eda
import common as cm

st.set_page_config(
   page_title='친환경농산물 소매가격 예측',
   page_icon='data/icon.png',
   layout='centered',
   initial_sidebar_state='expanded'
)

def main():
    #pass
    st.title('친환경농산물 소매가격 예측 (Facebook Prophet 라이브러리)')

    cm.fontLoad()

    cm.DataLoad()

    run_eda()

if __name__=='__main__':
    main()