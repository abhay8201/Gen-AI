import streamlit as st
from langchain_groq import ChatGroq

# Function to check grammar
def correct_grammar(text):
    llm = ChatGroq(
        model="gemma2-9b-it",
        temperature=0,
        groq_api_key="your_api_key_here"  # Replace with your actual API key
    )
    
    prompt = f"""Check the grammar of the following text. 
    If it's correct, return it as is. 
    If it has grammar mistakes, correct them without 
    changing the meaning or adding extra words. 
    Also, list the incorrect words and provide feedback 
    on what went wrong.\nText: {text}"""
    
    response = llm.invoke(prompt)  # Get AIMessage object
    corrected_text = response.content  # Extract actual text
    
    if corrected_text.strip() == text.strip():
        return text, "The sentence is already correct."
    else:
        return corrected_text, "Grammar errors were found and corrected."

# Streamlit UI
st.title("Grammar Checker with Streamlit")

user_input = st.text_area("Enter a sentence to check grammar:")
if st.button("Check Grammar"):
    if user_input:
        corrected_text, message = correct_grammar(user_input)
        st.write("### Corrected Text:")
        st.success(corrected_text)
        st.write("### Feedback:")
        st.info(message)
    else:
        st.warning("Please enter a sentence.")

