import streamlit as st
import openai

# Read the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Read the prompt from a file and truncate if necessary
with open('website_text.txt', 'r') as file:
    prompt_file_content = file.read()

max_prompt_length = 3500  # Set a max length for the initial prompt content

if len(prompt_file_content) > max_prompt_length:
    prompt = prompt_file_content[:max_prompt_length] + "..."
else:
    prompt = prompt_file_content

# Define the assistant template
hotel_assistant_template = prompt + """
You are the hotel manager of Landon Hotel, named "Mr. Landon". 
Your expertise is exclusively in providing information and advice about anything related to Landon Hotel. 
This includes any general Landon Hotel related queries. 
You do not provide information outside of this scope. 
If a question is not about Landon Hotel, respond with, "I can't assist you with that, sorry!" 
Question: {question} 
Answer: 
"""

def query_llm(question):
    full_prompt = hotel_assistant_template.format(question=question)
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=full_prompt,
            max_tokens=256
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit app interface
st.title("Landon Hotel Chatbot")
st.write("Ask any questions related to Landon Hotel, and Mr. Landon will assist you!")

question = st.text_input("Enter your question:")
if st.button("Submit"):
    if question:
        answer = query_llm(question)
        st.write("Answer:", answer)
    else:
        st.write("Please enter a question.")
