import pandas as pd
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc

df = pd.DataFrame({'A' : []})
df_item_list = pd.DataFrame({'A' : []})

def DataLoad():
    global df
    global df_item_list
    df = pd.read_csv('data/price_20210916.csv', index_col=0)
    df_item_list=sorted(df['품목명'].unique())

def fontLoad():
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