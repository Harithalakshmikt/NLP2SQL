import streamlit as st
import requests

st.set_page_config(page_title="NLP to SQL", page_icon="🧠", layout="centered")

st.title("🧠 NLP to SQL Demo")
st.write("Ask questions about the clinic database")

# Input
question = st.text_input("Enter your question:")

# Button
if st.button("Run Query"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Generating SQL and fetching results..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"question": question}
                )

                # 🔍 Debug info (helps if something breaks)
                if response.status_code != 200:
                    st.error(f"API Error: {response.status_code}")
                    st.text(response.text)
                else:
                    data = response.json()

                    # Handle error from backend
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success("Query executed successfully!")

                        # SQL
                        st.subheader("Generated SQL")
                        st.code(data["sql"], language="sql")

                        # Result
                        st.subheader("Result")

                        if isinstance(data["result"], list):
                            if len(data["result"]) > 0:
                                st.dataframe(data["result"])
                            else:
                                st.info("No data found")
                        else:
                            st.write(data["result"])

            except Exception as e:
                st.error(f"Connection Error: {e}")