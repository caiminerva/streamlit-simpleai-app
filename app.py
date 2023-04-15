#Import required packages
import openai
import requests
import os
from PIL import Image
from io import BytesIO
import streamlit as st
from streamlit_option_menu import option_menu

# OpenAI API Key
openai.api_key = st.secrets["api_key"]

# Define Streamlit app
def app():
    st.set_page_config(page_title="SimpleAI", page_icon=":robot_face:")
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Python Code Generator", "Topic Explanator", "AI Image Generator", "Language Translator"],
            icons=["house", "laptop", "book", "brush", "translate"],
            menu_icon='cast',
            default_index=0
        )

    if selected == "Home":
        st.title("Welcome to SimpleAI!")
        st.subheader("By: John Cairo Minerva BSCS 3A-AI")
        st.write("""The SimpleAI is an app that allows users to generate 
            Python code, explain topics at different educational levels, and generate 
            images based on a topic using OpenAI's text and image generation models. 
            Users can input instructions for the code they want to create, input a topic 
            and select an educational level to generate a written explanation of the 
            topic at the selected level, and input a topic to generate an image related 
            to that topic. The app uses artificial intelligence to generate the code, 
            explanations, and images and displays them for the user to see.
        """)

    elif selected == "Python Code Generator":
        st.title("Python Guru")
        st.write(""" Python Guru is a tool that helps you generate 
            Python code. You input instructions for the code you want to 
            create using the text box. When you're finished, you click 
            the "Done" button to generate the code. Python Guru uses AI
            (Artificial Intelligence) with OpenAI to generate the code 
            based on your instructions. 
            """)

        # Get user input
        instructions = []
        instr = st.text_input("Enter instruction:")
        button1 = st.button("Done")
        if button1:
            instructions.append(instr)
        elif not instr:
            st.warning("Please enter a topic.")

        # Generate code
        def generate_code(str_inst):
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=input_string + "\n",
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                temperature=0.0,
                stop=None,
            )
            answer = response.choices[0].text.strip()
            return answer

        str_inst = ''
        count = 0
        for i in instructions:
            str_inst = str_inst + i
            if count < len(instructions) - 1:
                str_inst = str_inst + ', \n'
            count += 1

        input_string = "Generate python code as follows: " + str_inst
        if len(instructions) > 0:
            output = generate_code(input_string)
            # Show output
            st.subheader("Generated Code:")
            st.code(output, language='python')

    elif selected == "Topic Explanator":
        st.title("6 Leveled Virtuoso")
        st.write(""" Have you watched the "5 Levels" playlist of WIRED in 
            YouTube? This tool is similar to that in which it allows users 
            to generate explanations of various topics at different educational 
            levels / complexity using OpenAI's text generation model. Try to input
            a topic and select an educational level, and let the AI generate a 
            written explanation of the topic at the selected level. The output 
            is then displayed below.
            """)

        # Get user input
        levels = ["Kinder", "Elementary", "High School", "Senior High", "College", "Graduate Student"]
        topic = st.text_input("Enter the topic you want to explain: ")
        level = st.selectbox(f"Enter the level you want to explain '{topic}' to", levels)

        # Explain topic
        output_container = st.empty()  # create empty container for output

        # Explain topic
        if not topic:
            output_container.warning("Please enter a topic.")
        else:
            # Function to explain topic
            def explain_topic(topic, level):
                prompt = f"Explain '{topic}' to a {level} student."
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                return response.choices[0].text.strip()

            explanation = explain_topic(topic, level.lower())
            output_container.write(explanation)

    elif selected == "AI Image Generator":
        st.title("Imagination Visualizer")
        st.write(""" The Imagination Visualizer is tool that lets you 
        create an image based on a topic that you input. You simply type 
        in a topic you want to visualize, click the button, and the tool 
        generates an image related to that topic. The tool uses artificial 
        intelligence to create the image, and displays it for you to see. 
        The caption for the displayed image tells you what topic the image 
        represents.
        """)

        # Get user input
        topic = st.text_input("Which topic do you want to visualize?")

        # Generate image
        if st.button("Generate"):
            response = openai.Image.create(
                prompt=f"visualize {topic}",
                n=1,
                size="512x512",
                model="image-alpha-001",
            )
            image_url = response.data[0]["url"]
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=f"Visualization of '{topic}'")
    
    elif selected == "Language Translator":
       # Define a function to translate text using GPT-3
       def translate_text(prompt, target_language):
           response = openai.Completion.create(
               engine="text-davinci-002",
               prompt=f"Translate the following text from {target_language} to English:\n{prompt}",
               max_tokens=2048,
               n=1,
               stop=None,
               temperature=0.5,
           )
           return response.choices[0].text.strip()
        
       st.title('Penta Lingo')
       st.write(""" Penta Lingo lets you translate text from five different languages 
       such as Japanese, Spanish, Korean, French, and Filipino to English. You can 
       enter some text to translate in the text input field and select the language 
       you want to translate from using the dropdown menu. When you're ready to
       translate, click the "Submit" button and the app will show you the translation 
       in English.
       """)
       text = st.text_input('Enter some text to translate:')
       target_languages = ['Japanese', 'Spanish', 'Korean', 'French', 'Filipino']
       target_language = st.selectbox('Select a target language:', target_languages)
       submit_button = st.button('Submit')

       if submit_button and text:
           translation = translate_text(text, target_language)
           st.write(f'Translation from {target_language} to English:')
           st.write(translation)

# Run Streamlit app
if __name__ == "__main__":
    app()

