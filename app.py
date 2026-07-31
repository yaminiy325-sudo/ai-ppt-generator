#step 1: load modules
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st

# ================step 2: streamlit front-end================
#to show web - app :complete page layout
st.set_page_config(layout="wide")

st.title("AI PPT GENERATOR")
st.divider()
st.sidebar.title("enter api-keys")
#==============step 3: load api keys==================
GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API", type = "password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API", type = "password")
#==============api validation===============
ALL_API = [GOOOGLE_API_KEY, TAVILY-API-KEY]

if not all(ALL_API):
st.sidebar.error("must pass all API_KEYS")

elif all(ALL_API):
  st.sidebar.success("API_KEYS loaded successfully")
#model load
model = ChatGoogleGenerativeAI(
  google_api_key - GOOGLE_API_KEY,
  model = st.sidebar.selectbox("Gemini-Model-Name",
                            options = ["gemini-2.5-flash",
                                       "gemini2.5-flash-lite",
                                       "gemini-3.5-flash",
                                       "gemini-3.5-flash-lite"])
)
else:
  st.sidenar.info("CHECK-API-KEYS")
  
#============STEP5:BACKEND CODE============
  #search_latest_info using tavily
def search_latest_info(query):
  """this fucntion helps to give
  latest search using tavily
  based on given user query related research or
  contents"""

  client = TavilyClient(api_key=TAVILY_API_KEY)
  response = client.search(query)
  return response

  
#=============== STEP6: USER INPUT============  
st.header("write a prompt to generate ppt or image or fetch latest news")
user_input = st.text_area("write here")

#tool 2 generate image using free api

def generate_image(img_prompt,slide_no = 1):
  """this is function helps user to generate
  image using free api,with given
  img_prompt"""

  url = f"https://image.pollinations.ai/{img_prompt}"

  import requests as r
  content = r.get(url).content
  with open(f"ai_image_{slide_no}.jpeg",'wb') as f:
    f.write(content)

  from PIL import Image
  img = Image.open(f"ai_image_{slide_no}.jpeg")
  return img

def agent_prompt(query):
  """This help to promptify the given user query
  suppose user needs PPT based on given query by user, it give detailed Professional prompt to return the output"""

  prompt = f"""Give detailed highly professional prompt for below given prompt.

  you are a professional ppt designer,
  based on user given query, your task is to professional HTML output prompt with no markdowns.
  user query: {query}"""

  response = model.invoke(prompt)
  final_prompt = response.content[-1]['text']

  with open("PPT_PROMPT.txt", 'w') as f:
    f.write(final_prompt)

  return final_prompt

def run_agent(leader_agent, query):
  prompt = f"""Based on Below given Query,
  your task is to call specific tool,
  first to promptify user prompt,
  than call image tool, or latest search if required.
  give slide dynamic, ui ux, with creative design,
  genrate image using
  keep help of function to generate image and embed or use direct url based on given topic,
  Generate image as no of slides and using file handling embed this in output html,
  use java script function to generate image using a sync func and threading and give output in html
  User Query given below:

  """

  prompt = agent_prompt(prompt+ query)

  response = leader_agent.invoke({'messages':[{'role': 'user',
  'content': prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code



#================step 7:agent call===============
# leader_agent creation
if all(ALL_API):
leader_agent = create_agent(
    model = model,
    tools = [search_latest_info,
            #generate_image
             ])
#=================step8: navbar streamlit===============
tab1,tab2,tab3 = st.tab(["Generate image"
                         "fetch latest news",
                         "generate ppt"])
else:
  st.info("pass-all-app-keys and return")
if(user_input) and (agent):
  #tab 1 code
  with tab1:
    if st,button("generate image",key= "gen-image"):
     with st.spinner("running agent"):
       try:
         generate_image(user_input)
       except:
         url = f"https://image.pollinations.ai/{img_prompt}"
         time.sleep(4)
         st.input(url)
  # tab 2code:
  with tab 2:
    if st.button("fetch news",key = "fetch news"):
      with st.spinner("running agent"):
        try:
          prompt ="give multiple news in html card formatfor topic" + user_input
          response = leader_agent.invoke({"messages":[{'rolr':'user',
                                                       'content':prompt}]}]
                                         code = response['messages'][-1].content[-1]['text']
          st.html(code,width="stretch",
                  unsafe_allow_javascript=True)
  #TAB 3 Code:
  with tab3:
  if st.button("Generate PPT", keys = "Gen-PPT"):
    with st.spinner ("Running Agent"): 
     try:
      code = run_agent(leader_agent, user_input)
      st.html(code, width="stretch",
              unsafe_allow_javascript=True)

     #file save
    with open("ppt.html","w")as f:
      f.write(code)

    st.download_button(label = "download ppt",
                  data = code,
                  file_name = 'ppt.html',
                  mime = 'text/html')
        except exception as err:
          st.error(err)
  






  
                               
