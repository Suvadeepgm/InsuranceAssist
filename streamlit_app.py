import streamlit as st
import anthropic
#pipfrom redlines import Redlines
#import pyperclip


def setup_anthropic():
    anthropic.api_key = st.secrets['InsuranceAssist_Key']
    client = anthropic.Client(api_key=anthropic.api_key)
    return client


def get_response(prompt, model="claude-3-haiku-20240307"):
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.content[0].text


@st.experimental_fragment
#def add_copy(text):
    #copy_button = st.button("Copy to clipboard")
    #if copy_button:
        #pyperclip.copy(text)
        #st.toast("Copied to clipboard")


def setup_sideBar():
    st.sidebar.header('About')
    st.sidebar.markdown("""
        App is created using [OpenAI](https://openai.com) GPT api and 🎈[Streamlit](https://streamlit.io/).
        """)
    st.sidebar.markdown("""
        Developed by [Suvadeep Datta](https://www.linkedin.com/in/rifatmonzur/)
        """)

    st.sidebar.header("Resources")
    st.sidebar.markdown(
        """
        - [Source Code](https://github.com/rifat1234/Prompt-To-Do-Common-Tasks)
        """)

def create_ui():


    # The code below is to control the layout width of the app.
    if "widen" not in st.session_state:
        layout = "centered"
    else:
        layout = "wide" if st.session_state.widen else "centered"

    #######################################################
    title = 'Insurance Assist'
    st.set_page_config(layout=layout, page_title=title, page_icon="🤗")
    st.title(title)

    setup_sideBar()
    task_summarise = 'Summarise'
    task_proofread = 'Proofread'
    #option = st.selectbox(
        #'Choose Task',
        #(task_proofread, task_summarise))
    name = st.text_area(f'Write your name', height=150,
                       value="", max_chars=10000)

    age = st.text_area(f'Write your age', height=150,
                       value="", max_chars=10000)

    gender = st.text_area(f'Write your gender', height=150,
                       value="", max_chars=10000)
    occupation = st.text_area(f'What is your employment status??', height=150,
                       value="", max_chars=10000)
    smoking_history = st.text_area(f'Do you smoke?', height=150,
                       value="", max_chars=10000)

    submitted = st.button('Submit')

    if submitted:
        if len(name.strip()) == 0:
            st.warning('Input needs to have at least one character.')
            return

            prompt = f"Based on the provided name {name} , age {age} and Gender {gender}, smoking history {smoking_history} , Occupation {occupation} generate a brief profile summarizing key details that would be relevant for selecting a life insurance policy."
            response = get_response(prompt)
            st.text_area('Initial Profile', height=150, value=response, disabled=True)
            #add_copy(response)

client = setup_anthropic()
create_ui()
