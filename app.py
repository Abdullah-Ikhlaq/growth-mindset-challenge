import streamlit as st
import pandas as pd 
import os  
from io import BytesIO 

# Setup the App
st.set_page_config(page_icon="💿",page_title="Data Sweeper", layout='wide') 

st.markdown(
    "<h1 style='text-align: center; "
    "color: white;'>Growth Mindset Chanllenge 🚀</h1>", unsafe_allow_html=True)
st.markdown("---")

st.markdown(
    "<h1 style='text-align: center; "
    "color: white;'>💿 Data Sweeper</h1>", unsafe_allow_html=True)

# Not used
# st.title("Data Sweeper")
# st.write("Transform your files between CSV or Excel formats with built-in data cleaning and visualization!")


st.markdown('<div style="text-align: center;">Transform your files between CSV or Excel formats with built-in data cleaning and visualization!</div>', unsafe_allow_html=True)

st.write("####")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel): ", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()  


        if file_ext == ".csv":
           df = pd.read_csv(file)
        
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        
        else: 
            st.error(f"Unsupported file format {file_ext}")
            continue
        

        # Display info about file
        st.write(f"📄**File Name:** {file.name}")
        st.write(f"📃**File Size:** {round(file.size/1024, 2)} KB")

        # Show 5 rows of data frame df
        st.write(f"**Preview the head of the Dataframe**")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean Data of {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates form {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔ Duplicates Remved Successfully!")

            with col2:
                if st.button(f"Fill Missing Values of {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✔ Missing Values have been filled Successfuly!") 

        # Choose specific columns to keep or convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(   
            f"Choose Columns for {file.name}", 
            df.columns, 
            default=list(df.columns),
            key=f"cols_{file.name}",
        )
        df = df[columns]


        # Create Some Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        # Convet the File --> CSV or Excel
        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(
            f"Convert {file.name} to:", ["CSV","Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                st.success("All Files Processed!")

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                st.success("All Files Processed!")
            buffer.seek(0)

       
            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name=file_name,
                mime=mime_type,
            )

                
                
                

            
