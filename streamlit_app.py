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
        max_tokens=500,
        temperature=0
    )
    return response.content[0].text


#st.experimental_fragment
#def add_copy(text):
    #copy_button = st.button("Copy to clipboard")
    #if copy_button:
        #pyperclip.copy(text)
        #st.toast("Copied to clipboard")


def setup_sideBar():
    st.sidebar.header('About')
    st.sidebar.markdown("""
        App is created using [Anthropic](https://www.anthropic.com/) Claude - Haiku api and 🎈[Streamlit](https://streamlit.io/).
        """)
    st.sidebar.markdown("""
        Developed by [Suvadeep Datta](https://www.linkedin.com/in/connectsuvadeep/)
        """)

    st.sidebar.header("Resources")
    st.sidebar.markdown(
        """
        - [Source Code](https://github.com/Suvadeepgm/InsuranceAssist)
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
    name = st.text_area(f'Write your name', height=50,
                       value="", max_chars=100)

    age = st.number_input(f'Write your age', format="%i" ,
                       value="", max_chars=100)

    gender = st.text_area(f'Write your gender', height=50,
                       value=None, max_chars=100)
    occupation = st.text_area(f'What is your employment status?', height=50,
                       value="", max_chars=1000)
    smoking_history = st.selectbox(
...                    'Are you a smoker or a non-smoker?',
...                     ('Smoker', 'Non - Smoker'))

    submitted = st.button('Submit')

    if submitted:
        if len(name.strip()) == 0:
            st.warning('Input needs to have at least one character.')
            return
        
        prompt = f"Based on the provided name {name} , age {age} and Gender {gender}, smoking history {smoking_history} , Occupation {occupation} generate a brief profile summarizing key details that would be relevant for selecting a life insurance policy."
        initial_profile = get_response(prompt)
        st.text_area('Initial Profile', height=550, value=initial_profile, disabled=True)
        #add_copy(response)

        insurance_type = st.selectbox(
...                    'Select the type of insurance you would like to enquire about:',
...                     ('Life', 'Health', 'Automobile', 'Home'))

        submitted = st.button('Submit')
        if submitted:
            prompt = f"Given the profile: {initial_profile} and the requested insurance type {insurance_type}, suggest 2-3 specific policy options of John Hancock that could be a good fit, along with a brief explanation for each recommendation. Give the names of the plans as well."
            policy_recommendation = get_response(prompt)
            st.text_area('Policy Recommendation', height=550, value=policy_recommendation, disabled=True)

            quote_yes_no = st.selectbox(
...                    'Do you want to see the approximate quotes for the above policies?',
...                     ('Yes', 'No'))
            if quote_yes_no='Yes':
                prompt = f"Given the profile: {initial_profile} and the Policy Recommendation {policy_recommendation} , suggest a Quote for the recommended policies."
                quote_recommendation = get_response(prompt)
                st.text_area('Apptoximate Quotes', height=550, value=quote_recommendation, disabled=True)

            



client = setup_anthropic()
create_ui()
