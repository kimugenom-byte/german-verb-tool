import streamlit as st
import google.generativeai as genai

# 見た目の設定
st.set_page_config(page_title="ドイツ語動詞チェッカー", page_icon="🇩🇪")
st.title("🇩🇪 ドイツ語動詞チェッカー")
st.write("文章を貼ると、動詞を抜き出して不定詞（元の形）と意味をリストにします。")

# APIキーの設定（Secretsから取得）
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # モデルの指定方法をより確実なものに変更
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"設定エラー: {e}")

# 入力欄
user_input = st.text_area("ドイツ語の文章を入力してください：", placeholder="例: Ich war gestern in Berlin.")

if st.button("動詞を解析する"):
    if user_input:
        with st.spinner('解析中...'):
            try:
                prompt = f"""
                以下のドイツ語の文章から動詞（助動詞を含む）をすべて抜き出し、以下の形式でリストアップしてください。
                文章に動詞がない場合は「動詞が見つかりませんでした」と答えてください。

                【形式】
                - 文中の形 → 不定詞（元の形）：日本語の意味

                文章：
                {user_input}
                """
                # 生成実行
                response = model.generate_content(prompt)
                st.write("### 解析結果")
                st.write(response.text)
            except Exception as e:
                st.error(f"解析中にエラーが発生しました。APIキーが正しく設定されていない可能性があります。")
                st.info("エラー詳細: " + str(e))
    else:
        st.warning("文章を入力してください。")
