import streamlit as st
from openai import OpenAI
import random
import re

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 세션 상태 초기화
if 'current_question_type' not in st.session_state:
    st.session_state.current_question_type = None
if 'question_data' not in st.session_state:
    st.session_state.question_data = None
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

def generate_essay_question():
    name = random.choice(["You","Eric","Mia","Paul","Sara","Someone"])
    answer = random.choice([
        "I'm singing.",
        "I'm dancing.",
        "I'm cooking.",
        "I'm sleeping.",
        "I'm making a doll.",
        "I'm cleaning the house.",
        "I'm watching TV.",
        "I'm washing dishes."
    ])
    prompt = f"""
    다음 대화를 이용하여 CEFR A1 수준의 영어 지문을 1문장으로 작성해주세요:
    A: What are you doing?
    B: {answer}
    
    그 다음, 지문에 관한 간단한 질문을 한국어로 만들어주세요. 
    질문을 만들 때, 지문에 맞는 화자를 포함해서 질문해 주세요.
    마지막으로, 질문에 대한 4개의 선택지를 한국어로 제공해주세요. 
    정답은 선택지 중 하나여야 합니다.
    
    출력 형식:
    질문: (한국어 질문)
    지문: (영어 지문)
    선택지:
    1. (선택지 1)
    2. (선택지 2)
    3. (선택지 3)
    4. (선택지 4)
    정답: (정답 번호)
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_conversation_question():
    answer = random.choice([
        "I'm singing in the shower.",
        "I'm dancing to my favorite song.",
        "I'm cooking dinner for my family.",
        "I'm sleeping in my comfortable bed.",
        "I'm making a doll for my little sister.",
        "I'm cleaning the house before my parents come home.",
        "I'm watching TV in the living room.",
        "I'm washing dishes after lunch."
    ])
    prompt = f"""
    다음 대화를 바탕으로 CEFR A1 수준의 간단한 영어 대화를 생성해주세요:
    A: What are you doing?
    B: {answer}
    
    영어 대화를 생성할 때, 마지막 대화 내용은 알려주지 말고 대화 내용에 관한 객관식 질문으로 만들어야 합니다. 
    그 후 대화 내용에 관한 객관식 질문을 한국어로 만들어주세요.  
    조건: 문제의 정답은 1개입니다. 
    A와 B가 대화할 때 상대방의 이름을 부르면서 대화를 합니다. 
    영어 대화는 A와 B가 각각 1번 말하고 끝납니다.
    
    형식:
    [영어 대화]
    A: ...
    B: ...

    [한국어 질문]
    질문: (한국어로 된 질문)
    A. (선택지)
    B. (선택지)
    C. (선택지)
    D. (선택지)
    정답: (정답 선택지)
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_question():
    if st.session_state.current_question_type == 'essay' or st.session_state.current_question_type is None:
        question_type = 'conversation'
    else:
        question_type = 'essay'
    
    st.session_state.current_question_type = question_type
    
    if question_type == 'essay':
        return generate_essay_question(), "essay"
    else:
        return generate_conversation_question(), "conversation"

def parse_question_data(data, question_type):
    lines = data.split('\n')
    if question_type == "essay":
        passage = ""
        question = ""
        options = []
        correct_answer = None

        for line in lines:
            if line.startswith("지문:"):
                passage = line.replace("지문:", "").strip()
            elif line.startswith("질문:"):
                question = line.replace("질문:", "").strip()
            elif re.match(r'^\d+\.', line):
                options.append(line.strip())
            elif line.startswith("정답:"):
                correct_answer = line.replace("정답:", "").strip()

        if correct_answer:
            correct_answer = int(re.search(r'\d+', correct_answer).group())

        return passage, question, options, correct_answer
    else:
        dialogue = ""
        question = ""
        options = []
        correct_answer = None

        dialogue_section = True
        for line in lines:
            if line.strip() == "[한국어 질문]":
                dialogue_section = False
                continue
            if dialogue_section:
                dialogue += line + "\n"
            else:
                if line.startswith("질문:"):
                    question = line.replace("질문:", "").strip()
                elif line.startswith(("A.", "B.", "C.", "D.")):
                    options.append(line.strip())
                elif line.startswith("정답:"):
                    correct_answer = line.replace("정답:", "").strip()

        return dialogue.strip(), question, options, correct_answer

def main():
    st.header("✨인공지능 영어 퀴즈 선생님 퀴즐링🕵️‍♀️")
    st.subheader("지금 하고 있는 일에 대한 영어읽기 퀴즈🕺")
    st.divider()

    if st.button("새로운 문제 생성"):
        st.session_state.question_data, st.session_state.question_type = generate_question()
        st.session_state.selected_option = None
        st.session_state.show_answer = False

    if st.session_state.question_data:
        if st.session_state.question_type == "essay":
            passage, question, options, correct_answer = parse_question_data(st.session_state.question_data, "essay")
            
            st.subheader("질문")
            st.write(question)

            st.divider()
            st.write(passage)
            st.divider()

            st.subheader("다음 중 알맞은 답을 골라보세요.")
            for i, option in enumerate(options, 1):
                if st.checkbox(option, key=f"option_{i}", value=st.session_state.selected_option == i):
                    st.session_state.selected_option = i

        else:
            dialogue, question, options, correct_answer = parse_question_data(st.session_state.question_data, "conversation")
            
            st.markdown("### 질문")
            st.write(question)
            
            st.markdown("### 대화")
            st.text(dialogue)
              
            st.subheader("다음 중 알맞은 답을 골라보세요.")
            for i, option in enumerate(options):
                if st.checkbox(option, key=f"option_{i}", value=st.session_state.selected_option == option):
                    st.session_state.selected_option = option

        if st.button("정답 확인"):
            st.session_state.show_answer = True

        if st.session_state.show_answer:
            if st.session_state.selected_option is not None:
                if (st.session_state.question_type == "essay" and st.session_state.selected_option == correct_answer) or \
                   (st.session_state.question_type == "conversation" and st.session_state.selected_option == correct_answer):
                    st.success("정답입니다!")
                else:
                    st.error(f"틀렸습니다. 정답은 {correct_answer}입니다.")
            else:
                st.warning("선택지를 선택해주세요.")

if __name__ == "__main__":
    main()
