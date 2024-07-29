import streamlit as st
import requests
from htmlTemplates import css,bot_template,user_template

def upload_files(files):
    url = "http://localhost:8000/upload"
    files_to_send = [("files", (file.name, file.read(), file.type)) for file in files]
    response = requests.post(url, files=files_to_send)
    return response.json()

def ask_question(question):
    url = "http://localhost:8000/ask"
    response = requests.post(url, data={"question": question})
    return response.json()

def main():
    st.set_page_config(page_title="PDFs Information Retrieval", page_icon=":books:")
    st.write(css,unsafe_allow_html=True)
    st.title("PDFs Information Retrieval :books:")

    with st.sidebar:
        st.subheader("Upload Documents")
        uploaded_files = st.sidebar.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

        if st.sidebar.button("Process Documents"):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    result = upload_files(uploaded_files)
                    st.sidebar.success(result.get("message", "Documents processed successfully."))
            else:
                st.sidebar.error("Please upload PDF files to process.")

    st.header("Ask Questions")
    user_question = st.text_input("Enter your question:")
    if st.button("Submit Question"):
        if user_question.strip():
            response = ask_question(user_question)
            if "error" in response:
                st.error(response["error"])
            else:
                for conversation in response.get("responses", []):
                    # st.markdown(f"**User:** {conversation['user']}")
                    # st.markdown(f"**Bot:** {conversation['bot']}")
                    st.write(user_template.replace("{{MSG}}",conversation['user']), unsafe_allow_html=True)
                    st.write(bot_template.replace("{{MSG}}",conversation['bot']), unsafe_allow_html=True)

    if user_question == "":
        st.error("Please ask a question to PDF.")



if __name__ == '__main__':
    main()
