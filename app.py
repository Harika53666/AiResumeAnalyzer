import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.markdown("### ATS Compatibility & Job Match Evaluation System")

# 🔐 API KEY
api_key = st.text_input("Enter your Groq API Key", type="password")

if api_key:

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    # 📄 Resume Upload
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    # 📝 Job Description Input
    job_description = st.text_area("Paste Full Job Description Here")

    if uploaded_file and job_description:

        # Resume Parsing
        reader = PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        resume_text = resume_text[:6000]  # Prevent token overflow

        st.success("✅ Resume Uploaded & Job Description Added")

        if st.button("Analyze Resume"):

            with st.spinner("Running ATS Evaluation..."):

                prompt = f"""
You are an advanced ATS (Applicant Tracking System) and HR recruiter.

Evaluate the resume against the given job description.

Provide a structured output in the following format:

1️⃣ ATS Compatibility Score (0-100)
- Explain how ATS systems evaluate this resume.
- Mention keyword density, formatting, and structure.

2️⃣ Job Match Percentage (0-100)
- Based on skills, experience, and job alignment.

3️⃣ Matching Keywords
- List important keywords found in resume that match job description.

4️⃣ Missing Keywords
- List important job description keywords missing in resume.

5️⃣ Skill Gap Analysis
- Mention missing technical and soft skills.

6️⃣ Formatting & ATS Issues
- Mention if formatting might affect ATS readability.

7️⃣ Explainable Reasoning
- Clearly explain why this score was given.

8️⃣ Actionable Recommendations
- Give clear improvement suggestions.

9️⃣ Professional Candidate Summary
- 4-5 line recruiter-style summary.

Resume:
{resume_text}

Job Description:
{job_description}
"""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )

                result = response.choices[0].message.content

                st.subheader("📊 ATS Evaluation Report")
                st.markdown(result)

                # 🎯 Simple Score Extraction (Optional Enhancement)
                st.markdown("---")
                st.info("✅ Analysis Completed Successfully!")

    elif uploaded_file and not job_description:
        st.warning("⚠ Please paste the Job Description.")

    elif job_description and not uploaded_file:
        st.warning("⚠ Please upload your Resume.")

else:
    st.warning("⚠ Please enter your Groq API key to continue.")
