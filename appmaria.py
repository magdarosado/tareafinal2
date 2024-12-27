import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Título de la aplicación
st.title("Carga de Dataset")

# Carga del archivo CSV
uploaded_file = st.file_uploader("Sube tu dataset", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())
    st.write("Columnas disponibles:", df.columns.tolist())  # Muestra las columnas disponibles

    # Mostrar estadísticas descriptivas
    if st.button("Mostrar estadísticas descriptivas"):
        stats = df.describe()
        st.write(stats)

    # Selector para histograma
    column_to_plot = st.selectbox("Selecciona la columna para el histograma:", df.columns.tolist())

    # Visualizar gráfica (histograma)
    if st.button("Visualizar histograma"):
        try:
            fig, ax = plt.subplots()
            sns.histplot(df[column_to_plot], kde=True, ax=ax)
            st.pyplot(fig)
            # Guardar la figura del histograma
            hist_file_path = "histograma.png"
            plt.savefig(hist_file_path)
            plt.close(fig)  # Cerrar la figura para liberar memoria
        except Exception as e:
            st.error(f"Ocurrió un error al generar el histograma: {e}")

    # Selector para gráfico de dispersión
    x_column = st.selectbox("Selecciona la columna para el eje X del gráfico de dispersión:", df.columns.tolist())
    y_column = st.selectbox("Selecciona la columna para el eje Y del gráfico de dispersión:", df.columns.tolist())

    # Visualizar gráfica (dispersión)
    if st.button("Visualizar gráfico de dispersión"):
        try:
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x_column, y=y_column, ax=ax)
            st.pyplot(fig)
            # Guardar la figura del gráfico de dispersión
            scatter_file_path = "grafico_dispersion.png"
            plt.savefig(scatter_file_path)
            plt.close(fig)  # Cerrar la figura para liberar memoria
        except Exception as e:
            st.error(f"Ocurrió un error al generar el gráfico de dispersión: {e}")

    # Generar Informe PDF
    if st.button("Generar Informe"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título del informe
        pdf.cell(200, 10, txt="Informe de Análisis", ln=True)

        # Resumen del dataset
        pdf.cell(200, 10, txt="Resumen del dataset:", ln=True)
        summary = df.describe().to_string()
        pdf.multi_cell(0, 10, summary)

        # Incluir histogramas en el informe si existe el archivo
        if os.path.exists("histograma.png"):
            pdf.cell(200, 10, txt="Histograma generado:", ln=True)
            pdf.image("histograma.png", x=10, y=None, w=180)  # Ajusta el tamaño según sea necesario

        # Incluir gráfico de dispersión en el informe si existe el archivo
        if os.path.exists("grafico_dispersion.png"):
            pdf.cell(200, 10, txt="Gráfico de dispersión generado:", ln=True)
            pdf.image("grafico_dispersion.png", x=10, y=None, w=180)  # Ajusta el tamaño según sea necesario

        # Guardar el PDF en un archivo temporal
        pdf_file_path = "informe.pdf"
        pdf.output(pdf_file_path)

        # Proporcionar enlace para descargar el PDF
        with open(pdf_file_path, "rb") as f:
            btn = st.download_button(
                label="Descargar Informe PDF",
                data=f,
                file_name=pdf_file_path,
                mime="application/pdf"
            )
        
        # Mensaje de éxito
        if btn:
            st.success("Informe generado con éxito. Puedes descargarlo.")







