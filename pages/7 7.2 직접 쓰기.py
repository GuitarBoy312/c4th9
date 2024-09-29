import streamlit as st
import random

# 문장과 이모지 목록
sentences = [
    ("What are you doing?", "❓"),
    ("I'm singing.", "🎤"),
    ("I'm dancing.", "💃"),
    ("I'm cooking.", "👨‍🍳"),
    ("I'm sleeping.", "😴"),
    ("I'm making a doll.", "🧸"),
    ("I'm cleaning the house.", "🧹"),
    ("I'm watching TV.", "📺"),
    ("I'm washing dishes.", "🍽️")
]

def generate_question():
    sentence, emoji = random.choice(sentences)
    words = sentence.split()
    blank_index = random.randint(0, len(words) - 1)
    correct_word = words[blank_index]
    
    blanked_sentence = ' '.join(words[:blank_index] + ['_____'] + words[blank_index+1:])
    
    return blanked_sentence, emoji, correct_word

# Streamlit UI
st.header("✨인공지능 영어문장 퀴즈 선생님 퀴즐링🕵️‍♀️")
st.subheader("빈칸에 들어갈 단어를 고르세요🔤")
st.divider()

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ [새 문제 만들기] 버튼을 눌러 문제 만들기.<br>
    2️⃣ 빈칸에 들어갈 단어를 고르세요.<br> 
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
    st.session_state.blanked_sentence = ""
    st.session_state.emoji = ""
    st.session_state.correct_word = ""

if st.session_state.question_generated:
    st.markdown("### 문제")
    st.write("빈칸에 들어갈 단어를 입력하세요:")
    st.markdown(f'<p style="font-size: 24px; margin-top: 10px;">{st.session_state.blanked_sentence} {st.session_state.emoji}</p>', unsafe_allow_html=True)
      
    with st.form(key='answer_form'):
        user_input = st.text_input("정답을 입력하세요:", key="user_answer")
        submit_button = st.form_submit_button(label='정답 확인')

        if submit_button:
            if user_input:
                st.info(f"입력한 답: {user_input}")
                if user_input.lower() == st.session_state.correct_word.lower():  
                    st.success("정답입니다!")
                    st.markdown(f'<p style="font-size: 24px;">정답 문장: {st.session_state.blanked_sentence.replace("_____", st.session_state.correct_word)} {st.session_state.emoji}</p>', unsafe_allow_html=True)
                else:
                    st.error(f"틀렸습니다. 정답은 {st.session_state.correct_word}입니다.")
                    st.markdown(f'<p style="font-size: 24px;">정답 문장: {st.session_state.blanked_sentence.replace("_____", st.session_state.correct_word)} {st.session_state.emoji}</p>', unsafe_allow_html=True)
            else:
                st.warning("답을 입력해주세요.")

# 새 문제 만들기 버튼을 페이지 맨 아래로 이동
if st.button("새 문제 만들기"):
    blanked_sentence, emoji, correct_word = generate_question()
    
    st.session_state.blanked_sentence = blanked_sentence
    st.session_state.emoji = emoji
    st.session_state.correct_word = correct_word
    st.session_state.question_generated = True
    
    # 페이지 새로고침
    st.rerun()
