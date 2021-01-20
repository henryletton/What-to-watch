'''
    File name: hl_test.py
    Author: Henry Letton
    Date created: 2021-01-20
    Python Version: 3.8.3
    Desciption: Testing streamlit functionality
'''
#https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2
#https://docs.streamlit.io/en/stable/main_concepts.html
#https://docs.streamlit.io/en/stable/streamlit_components.html
#https://docs.streamlit.io/en/stable/api.html

import pandas as pd
import streamlit as st
import plotly.express as px

# Data caching
@st.cache
def get_data():
    url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
    return pd.read_csv(url)
df = get_data()

# Start with heading and quote
st.title("Streamlit 101: An in-depth introduction")
st.markdown("Welcome to this in-depth introduction to [...].")
st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am [...]")

# Data view
st.dataframe(df.head())
#st.table(df.head()) #static

# Show code blocks, also st.echo
st.code("""
@st.cache
def get_data():
    url = "http://data.insideairbnb.com/[...]"
    return pd.read_csv(url)
""", language="python")

# Map data
df_expensive = df.copy()[df['price'] > 500]
st.map(df_expensive)

# User selecting columns
cols = ["name", "host_name", "neighbourhood", "room_type", "price"]
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
st.dataframe(df[st_ms])

# JSON Rendering
st.json({
     'foo': 'bar',
     'baz': 'boz',
     'stuff': [
         'stuff 1',
         'stuff 2',
         'stuff 3',
         'stuff 5',
     ],
 })


# Sidebar and price range slider
values = st.sidebar.slider("Price range", 0., 1000., (50., 300.))
f = px.histogram(df.query(f"price >= {values[0]}").query(f"price <= {values[1]}"), 
                 x="price", nbins=15, title="Price distribution")
f.update_xaxes(title="Price")
f.update_yaxes(title="No. of listings")
st.plotly_chart(f)

# Select and tick boxes
st.write("Using a radio button restricts selection to only one option at a time.")
neighborhood = st.radio("Neighborhood", df.neighbourhood_group.unique())
show_exp = st.checkbox("Include expensive listings")

# Another plot
df.query("availability_365>0")\
.groupby("neighbourhood_group")\
.availability_365.mean()\
.plot.bar(rot=0)\
.set(title="Average availability by neighborhood group",
xlabel="Neighborhood group", ylabel="Avg. availability (in no. of days)")
st.pyplot()

# Sliders
minimum = st.sidebar.number_input("Minimum", min_value=0, value=0)
maximum = st.sidebar.number_input("Maximum", min_value=0, value=5)

# Images and dropdown
pics = {
    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg"
}
pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])

# Buttons
st.markdown("## Party time!")
st.write("Yay! You're done with this tutorial of Streamlit. Click below to celebrate.")
btn = st.button("Celebrate!")
if btn:
    st.balloons()

# Beta columns
left_column, right_column = st.beta_columns(2)
left_column.button('Press me!')
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")






