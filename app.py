import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Title and overview
st.title("Vikash DATA Services - Data Analysis and Visualization")
st.write("Upload a Dataset")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Load the uploaded dataset
        @st.cache
        def load_data():
            data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
            return data

        data = load_data()

        # Data Description
        st.write("Data Description")
        st.write(f"Number of Rows: {data.shape[0]}")
        st.write(f"Number of Columns: {data.shape[1]}")
        st.write("Data Types:")
        st.write(data.dtypes)
        st.write("Descriptive Statistics:")
        st.write(data.describe())

        # Data Overview
        st.write("Data Overview")
        st.write(data.head())

        # Object Data Type Analysis
        st.write("Object Data Type Analysis")
        object_cols = data.select_dtypes(include="object").columns
        for col in object_cols:
            st.write(f"{col} Analysis")
            st.write(f"Number of Unique Values: {data[col].nunique()}")
            st.write("Top Value Counts:")
            st.write(data[col].value_counts())

        # Categorical Column Selection
        st.write("Categorical Column Analysis")
        categorical_cols = st.multiselect("Select categorical columns for analysis", object_cols)

        if categorical_cols:
            # Univariate Categorical Analysis
            st.write("Univariate Categorical Analysis")
            for col in categorical_cols:
                st.write(f"{col} Value Counts")
                fig = px.bar(data, x=col, title=f"{col} Value Counts")
                st.plotly_chart(fig)

            # Multivariate Categorical Analysis with Hue
            st.write("Multivariate Categorical Analysis")
            x_col = st.selectbox("Select X-axis column", categorical_cols)
            hue_col = st.selectbox("Select Hue column (for color differentiation)", categorical_cols, key="hue_selection")

            if x_col and hue_col:
                fig = px.bar(data, x=x_col, color=hue_col, title=f"{x_col} vs {hue_col}")
                st.plotly_chart(fig)

        # Univariate Analysis
        st.write("Univariate Analysis")
        numeric_cols = data.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            st.subheader(f"{col} Distribution")
            fig = px.histogram(data, x=col)
            st.plotly_chart(fig)

        # Correlation Heatmap
        st.write("Correlation Heatmap")
        corr_matrix = data.corr()
        st.write(sns.heatmap(corr_matrix, annot=True))

        # Multivariate Analysis
        st.write("Multivariate Analysis")

        # Pairplot for selected columns (customize this section)
        selected_columns = st.multiselect("Select columns for the pairplot", numeric_cols)
        if selected_columns:
            st.write("Pairplot")
            pairplot = sns.pairplot(data[selected_columns])
            st.pyplot(pairplot)

        # Scatter Plot (customize this section)
        st.write("Scatter Plot")
        x_col = st.selectbox("Select X-axis column", numeric_cols)
        y_col = st.selectbox("Select Y-axis column", numeric_cols)
        fig = px.scatter(data, x=x_col, y=y_col)
        st.plotly_chart(fig)

        # Data Insights and Suggestions (customize this section)
        st.write("Data Insights and Suggestions")

        # Null Values
        null_counts = data.isnull().sum()
        st.write("Null Values")
        st.write(null_counts)

        # Outliers (customize this section)
        st.write("Outliers Detection")
        # You can add your code here to detect and display outliers

        # Suggestions (customize this section)
        st.write("Suggestions")
        # Provide suggestions based on the analysis and findings

        # Contact Developer Section
        st.write("Contact Developer")
        st.write("If you have any questions or feedback, please feel free to contact the developer:")
        st.write("- Developer Name: Vikash Goyal")
        st.write("- LinkedIn Profile: [Vikash Goyal's LinkedIn](https://www.linkedin.com/in/vikash-goyal-20692924b)")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
