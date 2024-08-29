# streamlit run app.py
# field to enter the job desciption
# upload pdf
# pdf to img processing using gemini pro
# prompt templates -> multiple button functions

from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import io
import base64
import os 
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response (input,pdf_content, prompt):

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
            ##convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts =[
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking system")   
input_text = st.text_area("Job Description : ", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")

submit1 = st.button("Tell me about the resume")
# submit2 = st.button("How can I improvise my skills")
submit2 = st.button("Percentage Match")

input_prompt1 = """
    Please conduct a thorough review of the provided resume against the 
    given job description for roles in data science, full stack 
    web development, big data engineering, DevOps, or data analytics. 
    Provide a detailed professional evaluation of how well the candidate's 
    profile matches the job requirements. Highlight specific strengths and 
    weaknesses of the candidate in relation to the specified role, including 
    relevant skills, experience, and qualifications. This information will 
    be used to develop an ATS (Applicant Tracking System) evaluation feature 
    that can automatically assess candidate profiles against job descriptions.
    Your insights will help us refine the ATS's criteria for evaluating 
    candidate suitability.
"""

input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with deep expertise in evaluating resumes for roles such as data science, full stack web development,
    big data engineering, DevOps, or data analytics. Your task is to evaluate the resume against the provided job description and calculate a percentage match.
    Be consistent with the percentage match upon repeated requests for the same resume against the same job description, unless one of the factors changes.
    Provide the output in the following structured manner:
    1. Percentage Match: [percentage]
    2. Keywords Missing: [list the missing keywords in points]
    3. Final Thoughts: [provide concise and crisp points on the candidate's suitability]
"""

if submit1 : 
    if uploaded_file is not None :
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is ")
        st.write(response)
    else :
        st.write("Please upload the resume")
elif submit2 :
    if uploaded_file is not None :
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is ")
        st.write(response)
    else :
        st.write("Please upload the resume")

 


