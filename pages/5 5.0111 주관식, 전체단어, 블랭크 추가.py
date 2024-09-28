import streamlit as st
import random

# 단어와 이모지 목록
word_emojis = {
    'busy': '😰', 'clean': '🧼', 'dish': '🍽️', 'doll': '🧸', 'homework': '📚', 
    'house': '🏠', 'kitchen': '🍳', 'sleep': '😴', 'sure': '👍', 'wash': '🧼',
    'glove': '🧤', 'hair band': '👸', 'hundred': '💯', 'much': '🔢', 
    'pencil case': '✏️', 'really': '❗', 'scientist': '🔬'
}

def generate_question():
    word, emoji = random.choice(list(word_emojis.items()))
    word_chars = list(word)
    word_length = len(word_chars)
    
    if word_length <= 3:
        num_blanks = 1
    elif 4 <= word_length <= 5:
        num_blanks = 2
    elif 6 <= word_length <= 7:
        num_blanks = 3
    else:
        num_blanks = 4
    
    # 빈칸의 위치를 랜덤하게 선택
    blank_indices = random.sample(range(word_length), num_blanks)
    
    # 빈칸을 정확히 표시
    for i in blank_indices:
        word_chars[i] = '_'
    
    # 모든 문자와 빈칸 사이에 공백 추가
    blanked_word = ' '.join(word_chars)
    
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

if st.button("새 문제 만들기"):
    blanked_word, emoji, correct_word = generate_question()
    
    st.session_state.blanked_word = blanked_word
    st.session_state.emoji = emoji
    st.session_state.correct_word = correct_word
    st.session_state.question_generated = True
    
    # 페이지 새로고침
    st.rerun()

if st.session_state.question_generated:
    st.markdown("### 문제")
    st.write(f"빈칸을 채워 전체 단어를 입력하세요: {st.session_state.blanked_word} {st.session_state.emoji}")
    st.write(f"(힌트: 이 단어는 {len(st.session_state.correct_word.replace(' ', ''))}개의 글자로 이루어져 있습니다.)")
      
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
