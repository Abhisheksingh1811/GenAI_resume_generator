import streamlit as st
import google.generativeai as genai

api_key = API
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Function to generate resume using Google Generative AI API
def generate_resume(name, job_title):
    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
        generation_config=generation_config,
    )

    context = f'name:{name}\njob_titl1e:{job_title}\nwrite a resume on above data.'

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [context],
            },
        ]
    )

    response = chat_session.send_message(context)
    
    text = response.candidates[0].content if isinstance(response.candidates[0].content, str) \
           else response.candidates[0].content.parts[0].text
    
    return text

# Function to clean the generated resume text
def clean_resume_text(text):
    cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
    cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
    cleaned_text = cleaned_text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    cleaned_text = cleaned_text.replace("[University Name]", "[Your University Name]")
    cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
    return cleaned_text

# --- Streamlit UI ---
st.title("Resume Generator")

name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")

# Submit button
if st.button("Generate Resume"):
    if name and job_title:
        resume = generate_resume(name, job_title)
        cleaned = clean_resume_text(resume)
        st.markdown("### Generated Resume")
        st.markdown(cleaned)
    else:
        st.warning("Please enter both your name and job title.")


# Local URL: http://localhost:8501
# Network URL: http://192.168.0.6:8501