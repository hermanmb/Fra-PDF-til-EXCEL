import streamlit as st
import tabula
import pandas as pd
from io import BytesIO

def convert_pdf_to_excel(pdf_bytes):
    # Les tabeller fra PDF-filen
    tables = tabula.read_pdf(BytesIO(pdf_bytes), pages='all', multiple_tables=True)
    
    # Hvis vi har flere tabeller, kombiner dem til én DataFrame
    all_data = pd.concat(tables, ignore_index=True)
    
    # Lagre den kombinerte dataen i en Excel-fil i minnet
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        all_data.to_excel(writer, index=False)
    
    return output.getvalue()

# Streamlit UI
st.title("PDF to Excel Converter")

uploaded_file = st.file_uploader("Dra og slipp en PDF-fil", type="pdf")

if uploaded_file is not None:
    if st.button("Konverter til Excel"):
        excel_data = convert_pdf_to_excel(uploaded_file.read())
        st.download_button(label="Last ned Excel-fil",
                           data=excel_data,
                           file_name="converted.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
