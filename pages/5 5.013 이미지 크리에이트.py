import streamlit as st
from openai import OpenAI
import random
import requests
from io import BytesIO

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 단어와 이모지 목록
word_emojis = {
    'busy': '😰', 'clean': '🧼', 'dish': '🍽️', 'doll': '🧸', 'homework': '📚', 
    'house': '🏠', 'kitchen': '🍳', 'sleep': '😴', 'sure': '👍', 'wash': '🧼',
    'glove': '🧤', 'hair band': '👸', 'hundred': '💯', 'much': '🔢', 
    'pencil case': '✏️', 'really': '❗', 'scientist': '🔬'
}

def generate_image(word):
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=f"anime illustration of {word} that if ordinary elementary school student see the picture can guess {word}",
            size="256x256",
            n=1,
        )
        image_url = response.data[0].url
        return image_url 
    except Exception as e:
        st.error(f"이미지 생성 중 오류 발생: {str(e)}")
        return None

def generate_question(num_blanks):
    word, emoji = random.choice(list(word_emojis.items()))
    word_length = len(word)
    num_blanks = min(num_blanks, word_length)  # 단어 길이보다 빈칸이 많지 않도록 함
    
    blank_indices = random.sample(range(word_length), num_blanks)
    blanked_word = list(word)
    for index in blank_indices:
        blanked_word[index] = '_'
    blanked_word = ''.join(blanked_word)
    
    return blanked_word, emoji, word

# Streamlit UI
st.header("✨인공지능 영어단어 퀴즈 선생님 퀴즐링🕵️‍♀️")
st.subheader("빈칸에 들어갈 단어를 입력하세요🔤")
st.divider()

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ [새 문제 만들기] 버튼을 눌러 문제 만들기.<br>
    2️⃣ 빈칸에 들어갈 단어를 입력하세요.<br> 
    3️⃣ [정답 확인] 버튼 누르기.<br>
    4️⃣ 정답 확인하기.<br>
    <br>
    🙏 퀴즐링은 완벽하지 않을 수 있어요.<br> 
    🙏 그럴 때에는 [새 문제 만들기] 버튼을 눌러주세요.
    """
    , unsafe_allow_html=True)

# 세션 상태 초기화
if 'question_generated' not in st.session_state:
    st.session_state.question_generated = False
    st.session_state.blanked_word = ""
    st.session_state.emoji = ""
    st.session_state.correct_word = ""
    st.session_state.num_blanks = 1

# 슬라이더를 사이드바에서 메인 영역으로 이동
st.session_state.num_blanks = st.slider("빈칸 개수", min_value=1, max_value=3, value=1)

if st.button("새 문제 만들기"):
    blanked_word, emoji, correct_word = generate_question(st.session_state.num_blanks)
    
    st.session_state.blanked_word = blanked_word
    st.session_state.emoji = emoji
    st.session_state.correct_word = correct_word
    st.session_state.question_generated = True
    
    # 이미지 생성
    with st.spinner('이미지를 생성 중입니다...'):
        image_url = generate_image(correct_word)
        if image_url:
            st.session_state.image_url = image_url
        else:
            st.session_state.image_url = None
            st.warning("이미지 생성에 실패했습니다.")
    
    # 페이지 새로고침
    st.rerun()

if st.session_state.question_generated:
    st.markdown("### 문제")
    st.write(f"빈칸을 채워 전체 단어를 입력하세요: {st.session_state.blanked_word} {st.session_state.emoji}")
    
    if st.session_state.image_url:
        st.image(st.session_state.image_url, caption="단어 관련 이미지", width=200)  # 너비를 200으로 줄임
    
    with st.form(key='answer_form'):
        user_answer = st.text_input("정답을 입력하세요:")
        submit_button = st.form_submit_button(label='정답 확인')

        if submit_button:
            if user_answer:
                st.info(f"입력한 답: {user_answer}")
                if user_answer.lower() == st.session_state.correct_word.lower():  
                    st.success("정답입니다!")
                else:
                    st.error(f"틀렸습니다. 정답은 {st.session_state.correct_word}입니다.")
                st.write(f"정답 단어: {st.session_state.correct_word} {st.session_state.emoji}")
            else:
                st.warning("답을 입력해주세요.")
