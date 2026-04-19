import streamlit as st
import google.generativeai as genai

# 見た目の設定
st.set_page_config(page_title="ドイツ語動詞チェッカー", page_icon="🇩🇪")
st.title("🇩🇪 ドイツ語動詞チェッカー")
st.write("文章を貼ると、動詞を抜き出して不定詞（元の形）と意味をリストにします。")

# APIキーの設定（後でStreamlitのサイト側で設定します）
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key, transport='rest')
model = genai.GenerativeModel('gemini-1.5-flash')

# 入力欄
user_input = st.text_area("ドイツ語の文章を入力してください：", placeholder="例: Ich war gestern in Berlin.")

if st.button("動詞を解析する"):
    if user_input:
        with st.spinner('解析中...'):
            prompt = f"""
            以下のドイツ語の文章から動詞（助動詞を含む）をすべて抜き出し、以下の形式でリストアップしてください。
            文章に動詞がない場合は「動詞が見つかりませんでした」と答えてください。

            【形式】
            - 文中の形 ➔ 不定詞（元の形）: 日本語の意味

            文章：
            {user_input}
            """
            response = model.generate_content(prompt)
            st.success("解析完了！")
            st.markdown(response.text)
    else:
        st.warning("文章を入力してください。")
