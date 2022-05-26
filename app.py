import streamlit as st

from app_eda import run_eda

def main():
    #pass
    st.header('친환경농산물 소매가격 예측 (Facebook Prophet 라이브러리)')
    run_eda()

if __name__=='__main__':
    main()