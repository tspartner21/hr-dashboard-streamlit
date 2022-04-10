# Import libraries
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st
#import warnings

# workaround to suppress warnings from plotly and pandas
# FIXME: fix the issues and remove this workaround
#warnings.filterwarnings("ignore")

pio.templates.default = "simple_white"
st.set_page_config(page_title="HR Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state='expanded')


# ---- READ FILE ----
@st.cache
def read_file(file_name):
    return pd.read_csv(file_name)

df = read_file('data/hr_data.csv')

# ---- SIDEBAR ----
st.sidebar.write("Hi and welcome to my HR Dashboard project. Feel free to use the filter below "
                 "and the dashboard will be dynamically updated. Enjoy! 😀")

st.sidebar.header("Please Filter Here:")
dept_selection = st.sidebar.multiselect(
    "Select the Department:",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)
country_selection = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)
df_dc_selection = df.query('Department == @dept_selection & Country == @country_selection')
df_c_selection = df.query('Country == @country_selection')
df_d_selection = df.query('Department == @dept_selection')

# ---- MAINPAGE ----
st.title(":bar_chart: HR Dashboard")
st.write("Created by Alfie Danish")

# TOP KPI's
total_employees = len(df_dc_selection)
full_time = len(df_dc_selection[df_dc_selection['Time Type'] == "Full time"])
part_time = len(df_dc_selection[df_dc_selection['Time Type'] == "Part time"])

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Employees:")
    st.subheader(f":busts_in_silhouette: {total_employees}")
with middle_column:
    st.subheader("Full-Time:")
    st.subheader(f":bust_in_silhouette: {full_time}")
with right_column:
    st.subheader("Part-Time:")
    st.subheader(f":bust_in_silhouette: {part_time}")

st.markdown("---")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    # Employee distribution by gender
    gender = df_dc_selection["Gender"].value_counts()
    donut_1 = px.pie(labels=gender.index,
                     values=gender.values,
                     title="Percentage of Gender Distribution",
                     names=gender.index,
                     hole=0.6
                     )
    donut_1.update_traces(textposition='outside',
                          textfont_size=15,
                          textinfo='percent')
    st.plotly_chart(donut_1, use_container_width=True)

with middle_column:
    # Employee distribution by country
    country = df_d_selection["Country"].value_counts().sort_values(ascending=True)
    hist_1 = px.histogram(x=country.values,
                          y=country.index,
                          color=country.values,
                          log_x=True
                          )
    hist_1.update_layout(showlegend=False,
                         title="Total Employee by Country",
                         yaxis_title=None,
                         yaxis_showticklabels=True,
                         xaxis_title="Total Employee",
                         plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_showticklabels=False
                         )
    st.plotly_chart(hist_1, use_container_width=True)

with right_column:
    # Employee distribution by department
    dept = df_c_selection["Department"].value_counts()
    donut_2 = px.pie(labels=dept.index,
                     values=dept.values,
                     title="Employee Distribution by Department",
                     names=dept.index
                     )
    donut_2.update_traces(textposition='inside',
                          textfont_size=15,
                          textinfo='percent+label',
                          pull=[0.05, 0.05, 0.05, 0.05, 0.05])
    donut_2.update_layout(showlegend=False)
    st.plotly_chart(donut_2, use_container_width=True)

left_column, right_column = st.columns(2)
with left_column:
    # Total Employee per year
    #df_dc_selection["Hire Year"] = df_dc_selection["Hire Date"].dt.year
    df_dc_selection["Hire Year"] = pd.DatetimeIndex(df_dc_selection["Hire Date"], dayfirst=True).year
    running_hire = df_dc_selection.groupby("Hire Year", as_index=False).count()
    running_hire['Total per Year'] = np.nan
    for i in range(len(running_hire)):
        running_hire["Total per Year"].iloc[i] = running_hire["EmployeeID"].iloc[0:i + 1].sum()
    bar_1 = px.bar(running_hire,
                   x="Hire Year",
                   y="Total per Year",
                   color="Hire Year",
                   title="Total Employee per Year",
                   )
    bar_1.update_layout(xaxis_type="category",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)'
                        )
    bar_1.update_coloraxes(showscale=False)
    st.plotly_chart(bar_1)

with right_column:
    # Compensation Distribution by Department
    bar_2 = px.histogram(df_c_selection,
                         x="Salary",
                         y="Department",
                         color="Department",
                         title="Compensation Distribution by Department",
                         )
    bar_2.update_layout(showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis_title=None)
    st.plotly_chart(bar_2)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
