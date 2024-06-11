# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st

# """
# # Welcome to Streamlit!

# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).

# In the meantime, below is an example of what you can do with just a few lines of code:
# """

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })

# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))


# import streamlit as st
# from openai_App import ask_gpt 
# #import simpleCalc
# # Custom CSS to style the chat input
# custom_css = """
# <style>
# /* Example of customizing input boxes */
# .st-emotion-cache-arzcut {
#     padding-bottom : 15px;
# }
# </style>
# """

# # Inject the custom CSS into the Streamlit app
# st.markdown(custom_css, unsafe_allow_html=True)

# # message = st.chat_message("assistant")
# # message.write("Hello human")

# prompt = st.chat_input("Say something")

# messages=[
#     {"role": "system", "content": "Hi, How can I assist you?"},
# ]

# reply = ask_gpt(prompt, messages)
# messages.append({
#     "role": "assistant", "content": reply
# })
# print(reply)

import salesforce_case_App
