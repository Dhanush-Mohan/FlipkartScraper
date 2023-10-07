import streamlit as st
import pandas as pd
import base64
from io import BytesIO
# Import your scraping functions
from flipkart_scraper import scrape_flipkart

# Set the app's background color and text color


col1, col2, col3 = st.columns([1, 2, 1])

st.title("Flipkart Web Scraper")



product_name = st.text_input("Enter Product Name")

if st.button("Fetch Data"):
    if not product_name:
        st.warning("Please enter a product name.")
    
    else:
        data = scrape_flipkart(product_name)
        if data:
            # Convert the scraped data to a DataFrame
            data_df = pd.DataFrame(data)

            # Display the scraped data as a table
            st.subheader("📊 Scraped Data 📊")
            st.write(data_df)
             # Allow users to download the data as an Excel file
            st.subheader("Download Data")
            excel_file = BytesIO()
            with pd.ExcelWriter(excel_file, engine='xlsxwriter', mode='xlsx', datetime_format='yyyy-mm-dd') as writer:
                data_df.to_excel(writer, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="scraped_data.xlsx">Download as Excel</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        else:
            st.error("An error occurred while fetching data. Please try again later.")

# Run the Streamlit app with 'streamlit run app.py'
