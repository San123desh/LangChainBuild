import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper


os.environ['OPENAI_API_KEY'] = apikey

#App framework
st.title("🦜️🔗 Language Modeling YouTube GPT Creator")
prompt = st.text_input("Please enter your prompt here")

#Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'write me a youtube video title about {topic}'
)


script_template = PromptTemplate(
    input_variables = ['title','wikipedia_research'],
    template = 'write me a youtube video script based on this title Title: {title} while leveraging this wikipedia research:{wikipedi_research}'
)


#Memory
title_memory = ConversationBufferMemory(input_key = 'topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key = 'title', memory_key='chat_history')


#llms
#temprature -> position keyword argument(how creative is our llm)
llm = OpenAI(temperature = 0.9)
title_chain = LLMChain(llm = llm, prompt = title_template, verbose = True, output_key = 'title', memory=title_memory)
script_chain = LLMChain(llm = llm, prompt = script_template, verbose = True, output_key = 'script', memory=script_memory)

sequential_chain = SequentialChain(chain = [title_chain, script_chain],verbose = True, input_variables = ['topic'], output_variables=['title','script'])

#shows content to the screen is there's a prompt
if prompt:
    response = sequential_chain.run(prompt)
    st.write(response['title'])
    st.write(response['script'])

#render back to screen
    with st.expander('Message History'):
        st.info(memory.buffer)










