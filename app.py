import streamlit as st
import pandas as pd
import re
from thefuzz import fuzz, process
import difflib


st.set_page_config(page_title="藥品適應症查詢", page_icon="💊", layout="wide")
df = pd.read_csv('./data.csv')
st.title('同類及同成份藥物查詢')
st.markdown("""
<style>
[data-testid="stTextInput"] label p{
    font-size: 22px !important;
}
[data-testid="stTextInput"] input {
    font-size: 20px !important;
}
</style>
""", unsafe_allow_html=True)
col = ["藥品代碼", "商品名稱", '藥品學名', '藥品中文名', 'DC藥預設替代藥', '衛署適應症']
tab1, tab2, tab3 = st.tabs(["商品名稱檢索", "藥品代碼檢索", "疾病中文名檢索"])
with tab1:
    st.subheader("商品名稱檢索")
    trade = set()
    for i in df['商品名稱'].unique():
        j = i.split(' ')[0].upper()
        trade.add(j)

    drug = st.text_input("請輸入檢索藥名：", value='asp', max_chars=25).upper()
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
        st.write(trade_ing[col])
        trade_class = df[df['ATC_CODE1'].str.startswith(class_trade)]
        st.subheader('同類藥物：')
        st.write(trade_class[col])
    except:
        st.write('無符合條件藥物')

with tab2:
    try:
        st.subheader("藥品代碼檢索")
        drug_code = st.text_input("請輸入藥品代碼：", value='flu11i', max_chars=6).upper()
        choice_ = df.query('藥品代碼 == @drug_code')
        class_= choice_['ATC_CODE1'].str[:5].iloc[0]
        ingredient_ = choice_['ATC_CODE1'].iloc[0]
        st.subheader('同成份藥物：')
        code_ing = df[df['ATC_CODE1'].str.startswith(ingredient_)]
        st.write(code_ing[col])
        
        st.subheader('同類藥物：')
        code_class = df[df['ATC_CODE1'].str.startswith(class_)]
        st.write(code_class[col])
    except:
        st.write('無符合條件藥物')

with tab3:
    try:
        st.subheader("疾病中文名檢索")
        disease = st.text_input("請輸入中文疾病名稱：", value='使用*表示不確定性詞語，如：甲狀腺*', max_chars=10)
        df["衛署適應症"] = df["衛署適應症"].fillna("").astype(str)# 先做直接關鍵字搜尋
        direct_match = df["衛署適應症"].str.contains(disease, na=False, regex=False)
        result = df[direct_match]
        st.markdown('# 全吻合：<span style="color:red; font-size:22px">確認適應症或禁忌</span>', unsafe_allow_html=True)
        st.write(result[col])
        # 若直接搜尋沒有結果，再做模糊比對
        if result.empty:
            df["相似度分數"] = df["衛署適應症"].apply(lambda x: fuzz.partial_ratio(disease, x))
            result = df[df["相似度分數"] >= 70]
            resultQ = result.sort_values("相似度分數", ascending=False)
            st.markdown('# 相似度排序：<span style="color:red; font-size:22px">確認內容為適應症或禁忌</span>', unsafe_allow_html=True)
            st.write(resultQ[col])
        # else:
        #     resultQ = "無匹配適應症"
        #     st.write(resultQ)
    except:
        st.write('無符合條件疾病')