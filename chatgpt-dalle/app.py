import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]

st.title("KJH_GPT&DALL-E")  
st.markdown("##### 이 애플리케이션은 당신의 텍스트 입력을 기반으로 GPT-3와 DALL-E를 사용하여 이미지를 생성합니다.")

with st.form("form"):
    user_input = st.text_input("Prompt")
    size = st.selectbox("Size", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("Submit")

if submit and user_input:
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appearance of the input. Response it shortly around 20 words"
    }]

    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("ChatGPT가 응답을 준비하는 중입니다..."):
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt
        )

    prompt = gpt_response["choices"][0]["message"]["content"]
    st.write(f"GPT-3에 의해 생성된 프롬프트: **{prompt}**")

    with st.spinner("DALL-E가 이미지를 생성하는 중입니다..."):
        dalle_response = openai.Image.create(
            prompt=prompt,
            size=size
        )

    st.image(dalle_response["data"][0]["url"], caption=f"{prompt}에 대한 DALL-E의 시각화")


    st.image(dalle_response["data"][0]["url"])
