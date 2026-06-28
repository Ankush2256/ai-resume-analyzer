import streamlit as st
import os

from utils.pdf_reader import extract_text_from_pdf
from services.gemini_service import (
    test_connection,
    analyze_resume
)

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Upload Folder ---------------- #

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- Sidebar ---------------- #

st.sidebar.title("🤖 AI Resume Analyzer Pro")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

st.sidebar.markdown("---")

if st.sidebar.button("🔌 Test Gemini Connection"):

    with st.spinner("Connecting..."):

        result = test_connection()

    st.sidebar.success(result)

# ---------------- Main UI ---------------- #

st.title("🤖 AI Resume Analyzer Pro")

st.write(
    "Upload your resume and get an AI-powered ATS analysis."
)

# ---------------- Resume Upload ---------------- #

if uploaded_file is not None:

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume Uploaded Successfully")

    resume_text = extract_text_from_pdf(file_path)

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=250
    )

    st.divider()

    if st.button("🤖 Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            result = analyze_resume(resume_text)

        # ---------- Error ---------- #

        if "error" in result:

            st.error(result["error"])

        else:

            st.success("✅ Analysis Completed")

            st.divider()

            # ---------------- ATS Score ---------------- #

            st.subheader("🎯 ATS Score")

            st.metric(
                "ATS Score",
                f"{result['ats_score']} / 100"
            )

            st.divider()

            # ---------------- Summary ---------------- #

            st.subheader("📝 Summary")

            st.write(result["summary"])

            st.divider()

            # ---------------- Strengths ---------------- #

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("🟢 Strengths")

                for item in result["strengths"]:
                    st.success(item)

            with col2:

                st.subheader("🔴 Weaknesses")

                for item in result["weaknesses"]:
                    st.error(item)

            st.divider()

            # ---------------- Missing Skills ---------------- #

            st.subheader("📚 Missing Skills")

            for skill in result["missing_skills"]:

                st.warning(skill)

            st.divider()

            # ---------------- Recommended Jobs ---------------- #

            st.subheader("💼 Recommended Job Roles")

            for job in result["recommended_jobs"]:

                st.info(job)

            st.divider()

            # ---------------- Suggestions ---------------- #

            st.subheader("💡 Suggestions")

            for suggestion in result["suggestions"]:

                st.write("✅", suggestion)