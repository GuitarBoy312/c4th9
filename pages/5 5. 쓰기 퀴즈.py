import streamlit as st
import random
import string

# 단어와 이모지 목록
word_emojis = {
    'busy': '😰', 'clean': '🧼', 'dish': '🍽️', 'doll': '🧸', 'homework': '📚', 
    'house': '🏠', 'kitchen': '🍳', 'sleep': '😴', 'sure': '👍', 'wash': '🧼',
    'glove': '🧤', 'hair band': '👸', 'hundred': '💯', 'much': '🔢', 
    'pencil case': '✏️', 'really': '❗', 'scientist': '🔬'
}

def generate_question():
    word, emoji = random.choice(list(word_emojis.items()))
    blank_index = random.randint(0, len(word) - 1)
    correct_letter = word[blank_index]
    
    blanked_word = word[:blank_index] + '_' + word[blank_index+1:]
    
    options = [correct_letter]
    while len(options) < 4:
        random_letter = random.choice(string.ascii_lowercase)
        if random_letter not in options:
            options.append(random_letter)
    
    random.shuffle(options)
    
    return blanked_word, emoji, options, correct_letter

# Streamlit UI
st.header("✨인공지능 영어단어 퀴즈 선생님 퀴즐링🕵️‍♀️")
st.subheader("빈칸에 들어갈 알파벳을 고르세요🔤")
st.divider()

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ [새 문제 만들기] 버튼을 눌러 문제 만들기.<br>
    2️⃣ 빈칸에 들어갈 알파벳을 고르세요.<br> 
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

if st.button("새 문제 만들기"):
    # 세션 상태 초기화
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    blanked_word, emoji, options, correct_letter = generate_question()
    
    st.session_state.blanked_word = blanked_word
    st.session_state.emoji = emoji
    st.session_state.options = options
    st.session_state.correct_letter = correct_letter
    st.session_state.question_generated = True
    
    # 페이지 새로고침
    st.rerun()

if 'question_generated' in st.session_state and st.session_state.question_generated:
    st.markdown("### 문제")
    st.write(f"빈칸에 들어갈 알파벳을 고르세요: {st.session_state.blanked_word} {st.session_state.emoji}")
      
    with st.form(key='answer_form'):
        selected_option = st.radio("정답을 선택하세요:", st.session_state.options, index=None)
        submit_button = st.form_submit_button(label='정답 확인')

        if submit_button:
            if selected_option:
                st.info(f"선택한 답: {selected_option}")
                if selected_option == st.session_state.correct_letter:  
                    st.success("정답입니다!")
                    st.write(f"정답 단어: {st.session_state.blanked_word.replace('_', st.session_state.correct_letter)} {st.session_state.emoji}")
                else:
                    st.error(f"틀렸습니다. 정답은 {st.session_state.correct_letter}입니다.")
                    st.write(f"정답 단어: {st.session_state.blanked_word.replace('_', st.session_state.correct_letter)} {st.session_state.emoji}")
            else:
                st.warning("답을 선택해주세요.")
