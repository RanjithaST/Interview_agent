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

        .main-title {
            text-align: center !important;
            color: #0073e6 !important;
            font-size: 40px !important;
            font-weight: 700 !important;
            margin-bottom: 20px;
        }

        .stSubheader {
            text-align: center !important;
            color: #0073e6 !important;
            font-weight: 700 !important;
        }
        .stTextInput label {
            color: #0073e6 !important;
            font-weight: 600;
        }

        .stTextInput > div > div > input {
            border: 2px solid #0066cc !important;
            background-color: #f0f8ff !important;
            color: #000000 !important;
            border-radius: 6px !important;
            padding: 8px !important;
        }

        .stTextArea textarea {
            background-color: #f0f0f0 !important;
            border-radius: 6px !important;
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
            background-color: #f0f8ff;
            padding: 12px;
            border-radius: 6px;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'> AI Interview Agent</h1>", unsafe_allow_html=True)

if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "score" not in st.session_state:
    st.session_state.score = None

left_col, center_col, right_col = st.columns([1.2, 2.0, 1.2])

with left_col:
    st.subheader("User Details")
    name = st.text_input("Name", placeholder="Enter your name")
    role = st.text_input("Job Role", placeholder="Enter job role")

    if st.button("Get Interview Question", use_container_width=True):
        if role.strip() == "":
            st.error("Please enter a job role before generating a question.")
        else:
            with st.spinner("Generating question..."):
                st.session_state.question = generate_question(role)
                st.session_state.feedback = ""
                st.session_state.score = None
                st.session_state.answer = ""  # Clear answer box

with center_col:
    st.subheader("Interview Question")

    if st.session_state.question:
        st.markdown(f"<div class='info-box'>{st.session_state.question}</div>", unsafe_allow_html=True)

        # Keep the answer updated
        st.session_state.answer = st.text_area(
            "Your Answer",
            value=st.session_state.answer,
            height=200
        )

        if st.button("Evaluate Answer", use_container_width=True):
            if st.session_state.answer.strip() == "":
                st.error("Please write your answer before evaluating.")
            else:
                with st.spinner("Evaluating answer..."):
                    try:
                        feedback = evaluate_answer(
                            st.session_state.question,
                            st.session_state.answer
                        )
                        st.session_state.feedback = feedback

                        # Score extraction
                        score = 0
                        match = re.search(r"Score:\s*(\d+)\s*/\s*(\d+)", feedback)
                        if match:
                            obtained = int(match.group(1))
                            total = int(match.group(2))
                            score = round((obtained / total) * 100)
                        elif "Correct" in feedback:
                            score = 100
                        elif "Partially" in feedback:
                            score = 50
                        st.session_state.score = score

                        st.success("Evaluation complete! Click 'Get Interview Question' to continue.")

                    except Exception as e:
                        st.error("Evaluation error.")
                        st.exception(e)
    else:
        st.info("Click 'Get Interview Question' to begin.")

with right_col:
    st.subheader("Evaluation Result")

    if st.session_state.feedback:
      
        st.markdown(
            f"""
            <div style="
                background-color:#f0f8ff;
                color:#000000;
                padding:12px;
                border-radius:6px;
                height:200px;
                overflow-y:auto;
                white-space: pre-wrap;
                font-size:15px;
            ">
                {st.session_state.feedback}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h3 style='text-align:center; color:#0073e6;'>Score: {st.session_state.score}%</h3>",
            unsafe_allow_html=True
        )

        st.warning("Click 'Get Interview Question' to continue.")

        # if st.button("Save Result", use_container_width=True):
        #     if name.strip() == "" or role.strip() == "":
        #         st.error("Name and Job Role required!")
        #     else:
        #         with st.spinner("Saving result..."):
        #             try:
        #                 save_to_sheets(
        #                     name,
        #                     role,
        #                     st.session_state.question,
        #                     st.session_state.answer,
        #                     st.session_state.feedback,
        #                     st.session_state.score
        #                 )
        #                 st.success("Result saved successfully!")
        #             except Exception as e:
        #                 st.error("Failed to save.")
        #                 st.exception(e)
    else:
        st.info("Your evaluation will appear here.")
