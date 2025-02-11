import streamlit as st
import json
from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    groq_api_key="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"
)

# Streamlit UI
st.image("https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif", use_column_width=True)
st.title("Python Code Reviewer 🐍")
st.write("Enter your Python code below to check for errors and improvements.")

# User input for Python code
python_code = st.text_area("Paste your Python code here:", height=200)

if python_code.strip():  # Automatically review when code is entered
    # Structured prompt for JSON output
    code_review_prompt = f"""
    You are a professional Python code reviewer. 
    Analyze the following function and provide a structured review.

    Return the response in strict JSON format with three keys:
    {{
        "errors": [],  # List of syntax or logical errors
        "suggestions": [],  # List of improvements
        "optimized_code": ""  # Corrected and optimized function
    }}

    Function to review:
    {python_code}
    """

    # Invoke the LLM
    response = llm.invoke(code_review_prompt)

    # Handle JSON output
    try:
        review_result = json.loads(response.content.strip())

        st.subheader("Review Results:")
        
        # Display Errors
        if review_result.get("errors"):
            st.error("⚠️ Errors Found:")
            for error in review_result["errors"]:
                st.write(f"- {error}")
        else:
            st.success("✅ No syntax errors detected.")

        # Display Suggestions
        if review_result.get("suggestions"):
            st.info("💡 Suggestions for Improvement:")
            for suggestion in review_result["suggestions"]:
                st.write(f"- {suggestion}")

        # Display Optimized Code
        if review_result.get("optimized_code"):
            st.subheader("✨ Optimized Code:")
            st.code(review_result["optimized_code"], language="python")

    except json.JSONDecodeError:
        st.error("Error: The response was not valid JSON.")
