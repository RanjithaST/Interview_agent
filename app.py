import streamlit as st
from interview_engine import generate_question
from evaluator import evaluate_answer
from sheets import save_to_sheets
import re
st.set_page_config(page_title="AI Interview Agent", layout="wide")
st.markdown("""
    <style>
        body, .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .stTextInput > div > div > input, .stTextArea textarea {
            background-color: #f0f0f0;
            color: #000000;
        }
        .stButton button {
            background-color: #0073e6;
            color: white;
            border-radius: 6px;
            padding: 0.6rem;
        }
        .stButton button:hover {
            background-color: #005bb5;
        }
        .info-box {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            color: #000000;
        }
        .center-text {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;color:#0073e6;'>Interview Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555555;'>Refine your answers with AI guidance and boost your interview confidence.</p>", unsafe_allow_html=True)

if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "score" not in st.session_state:
    st.session_state.score = None
if "new_question" not in st.session_state:
    st.session_state.new_question = False
if "answer_key" not in st.session_state:
    st.session_state.answer_key = "answer_default"

left_col, center_col, right_col = st.columns([1.2, 2, 1.3])

with left_col:
    st.markdown("<h3 class='center-text'>User Details</h3>", unsafe_allow_html=True)
    name = st.text_input("Name")
    role = st.text_input("Job Role")

    if st.button("Get Interview Question", use_container_width=True):
        if role.strip() == "":
            st.error("Please enter a job role before generating a question.")
        else:
            with st.spinner("Generating question..."):
                st.session_state.question = generate_question(role)
            st.session_state.feedback = ""
            st.session_state.score = None
            st.session_state.new_question = True

with center_col:
    st.markdown("<h3 class='center-text'>AI Agent Interview</h3>", unsafe_allow_html=True)

    if st.session_state.question != "":
        st.markdown(f"<div class='info-box'>{st.session_state.question}</div>", unsafe_allow_html=True)

        if st.session_state.new_question:
            st.session_state.answer = ""
            st.session_state.answer_key = f"answer_{st.session_state.question}"
            st.session_state.new_question = False

        st.session_state.answer = st.text_area(
            "Your Answer",
            value=st.session_state.answer,
            height=200,
            key=st.session_state.answer_key
        )

        if st.button("Evaluate Answer", use_container_width=True):
            if st.session_state.answer.strip() == "":
                st.error("Please write your answer before evaluating.")
            else:
                try:
                    with st.spinner("Evaluating answer..."):
                        feedback = evaluate_answer(st.session_state.question, st.session_state.answer)
                        st.session_state.feedback = feedback

                        # Calculate score
                        match = re.search(r"(\d+)\s*/\s*(\d+)", feedback)
                        if match:
                            obtained = int(match.group(1))
                            total = int(match.group(2))
                            st.session_state.score = round((obtained / total) * 100)
                        else:
                            if "Correct" in feedback:
                                st.session_state.score = 100
                            elif "Partially" in feedback:
                                st.session_state.score = 50
                            else:
                                st.session_state.score = 0

                    st.success("Answer evaluated.")
                except Exception as e:
                    st.error("An error occurred during evaluation.")
                    st.exception(e)
    else:
        st.info("Click 'Get Interview Question' to begin.")

with right_col:
    st.markdown("<h3 class='center-text'>Evaluation</h3>", unsafe_allow_html=True)
    if st.session_state.feedback != "":
        st.text_area("Feedback", value=st.session_state.feedback, height=220, key="feedback_box")
        st.markdown(f"<h3 class='center-text' style='color:#0073e6;'>Score: {st.session_state.score}%</h3>", unsafe_allow_html=True)

        if st.button("Save Result", use_container_width=True):
            if name.strip() == "" or role.strip() == "":
                st.error("Name and Job Role are required to save.")
            else:
                try:
                    with st.spinner("Saving result..."):
                        save_to_sheets(
                            name,
                            role,
                            st.session_state.question,
                            st.session_state.answer,
                            st.session_state.feedback,
                            st.session_state.score
                        )
                    st.success("Result saved successfully.")
                except Exception as e:
                    st.error("Failed to save result.")
                    st.exception(e)
    else:
        st.info("Your evaluation will appear here.")
