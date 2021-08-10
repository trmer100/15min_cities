import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd


df= pd.read_excel('C:/Users/jklue/OneDrive/Desktop/output_data3.xlsx')
print(df)
print(df[df.amenity.isin(["hospital"])])
#st.write(df)
#st.map(df[df.amenity.isin(["hospital"])])
#st.write(df[df.amenity.isin(["hospital"])])

if st.checkbox("hospital"):
    st.map(df[df.amenity.isin(["hospital"])])


if st.checkbox("fuel"):
    st.map(df[df.amenity.isin(["fuel"])])