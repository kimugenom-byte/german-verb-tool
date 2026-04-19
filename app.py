import streamlit as st
import google.generativeai as genai

# 見た目の設定
st.set_page_config(page_title="ドイツ語構造解析ツール", page_icon="🇩🇪")
st.title("🇩🇪 ドイツ語 構造解析ツール")
st.write("文章を入力すると、動詞と名詞の「格」を詳しく解析します。")

# APIキーの設定
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # 接続の安定性を高める設定
    genai.configure(api_key=api_key, transport='rest') 
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"設定エラー: {e}")

# 入力欄
user_input = st.text_area("ドイツ語の文章を入力してください：", placeholder="例: Kannst du mir ihre Handynummer geben?", height=150)

if st.button("文章を解析する"):
    if user_input:
        with st.spinner('AIが文構造を解析中...'):
            try:
                # 指示（プロンプト）をより詳細に改良
                prompt = f"""
                以下のドイツ語の文章を解析し、2つのセクションで出力してください。

                1. 【動詞リスト】
                   - 文中の形 → 不定詞（元の形）：日本語の意味
                2. 【名詞・代名詞の格判定】
                   - 単語（またはフレーズ）: 何格か（1〜4格）：文中での役割（主語、〜に、〜を等）

                文章：
                {user_input}
                """
                
                response = model.generate_content(prompt)
                st.write("### 解析結果")
                st.info(response.text)
                
            except Exception as e:
                st.error("現在、AIとの接続を待機中です。")
                st.info(f"エラー詳細: {e}")
    else:
        st.warning("文章を入力してください。")
