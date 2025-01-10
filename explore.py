import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from openai import OpenAI

# Create an OpenAI client.
client = OpenAI(api_key = "")

system_prompt = "You are a helpful AI assistant. Please describe the data in a meaningful way."
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
	st.write("file uploaded...")
	df = pd.read_csv(uploaded_file)
	st.subheader("Data Preview")
	st.write(df.head())
	st.subheader("Data Summary")
	st.write(df.describe())

	st.subheader("Filter Data")
	columns = df.columns.tolist()
	selected_column = st.selectbox("Select column to filter on", columns)
	unique_values = df[selected_column].unique()
	selected_value = st.selectbox("Select values to filter on ",unique_values)

	filtered_df = df[df[selected_column] == selected_value]
	st.write(filtered_df)
	#str_data = pd.to_String(filtered_df)
	prompt = system_prompt + " " + filtered_df.to_string(index=False)
	st.write("prompt " + prompt)

	#st.subheader("Plot Data")
	#x_column = st.selectbox("Select x-axis column", columns)
	#y_column = st.selectbox("Select y-axis column", columns)

	if st.button("Generate Summary of Data"):
		#st.line_chart(filtered_df.set_index(x_column) [y_column])
		stream = client.chat.completions.create(
			messages = [
				{'role': 'user', 'content': prompt}
			],
			model = st.session_state["openai_model"],
		)
		st.write(stream.choices[0].message.content)
else:
	st.write("Waiting on file upload...")
