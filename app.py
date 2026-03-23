import streamlit as st
import pandas as pd
import re
from thefuzz import fuzz, process
import difflib


df = pd.read_csv('./data.csv')
st.title('同類及同成份藥物查詢')
tab1, tab2 = st.tabs(["商品名稱檢索", "藥品代碼檢索"])
with tab1:
    st.subheader("商品名稱檢索")
    trade = set()
    for i in df['商品名稱'].unique():
        j = i.split(' ')[0].upper()
        trade.add(j)

    drug = st.text_input("請輸入檢索藥名：", max_chars=25).upper()
    try:
        # best_match = process.extractOne(drug, trade)[0]
        # st.write(best_match)
        # matches = difflib.get_close_matches(drug, trade, n=1, cutoff=0.65)
        # st.write(matches)
        filtered = [c for c in trade if c.lower().startswith(drug.lower()[:3])]
        best_match = process.extractOne(drug, filtered)[0]
        st.write(f'比對的藥品： {best_match}')
        choice_trade = df.query('商品名 == @best_match').iloc[0]
        class_trade = choice_trade['ATC_CODE1'][:5]
        ingredient_trade = choice_trade['ATC_CODE1']
        trade_ing = df[df['ATC_CODE1'].str.startswith(ingredient_trade)]
        st.subheader('同成份藥物：')
        st.write(trade_ing.iloc[:,:-1])
        trade_class = df[df['ATC_CODE1'].str.startswith(class_trade)]
        st.subheader('同類藥物：')
        st.write(trade_class.iloc[:,:-1])
    except:
        st.write('無符合條件藥物')

with tab2:
    try:
        st.subheader("藥品代碼檢索")
        drug_code = st.text_input("請輸入藥品代碼：", max_chars=6).upper()
        choice_ = df.query('藥品代碼 == @drug_code')
        class_= choice_['ATC_CODE1'].str[:5].iloc[0]
        ingredient_ = choice_['ATC_CODE1'].iloc[0]
        st.subheader('同成份藥物：')
        code_ing = df[df['ATC_CODE1'].str.startswith(ingredient_)]
        st.write(code_ing.iloc[:,:-1])
        
        st.subheader('同類藥物：')
        code_class = df[df['ATC_CODE1'].str.startswith(class_)]
        st.write(code_class.iloc[:,:-1])
    except:
        st.write('無符合條件藥物')