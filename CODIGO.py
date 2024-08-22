import streamlit as st
import pandas as pd
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
from datetime import datetime
import os

class AuditoriaApp:
    def __init__(self):
        # Iniciar la aplicación Streamlit
        if 'users' not in st.session_state:
            st.session_state['users'] = {}
        if 'attempts' not in st.session_state:
            st.session_state['attempts'] = {}
        if 'current_user' not in st.session_state:
            st.session_state['current_user'] = None
        if 'files' not in st.session_state:
            st.session_state['files'] = {"nomina": None, "asistencia": None, "productividad": None}
        self.main_interface()

    def main_interface(self):
        """Crea la interfaz principal."""
        st.title("Papeles de trabajo Auditoría en sistemas Chalen, Luo y Palau")

        # Pantalla de login o bienvenida
        if st.session_state['current_user'] is None:
            self.login_interface()
        else:
            self.load_main_app(st.session_state['current_user'])

    def login_interface(self):
        """Interfaz para el inicio de sesión."""
        st.subheader("Iniciar Sesión")
        username = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type='password')

        if st.button("Iniciar Sesión"):
            self.login(username, password)

        if st.button("Crear Usuario"):
            self.create_user_interface()

    def create_user_interface(self):
        """Interfaz para crear un nuevo usuario."""
        st.subheader("Crear Nuevo Usuario")
        new_username = st.text_input("Nuevo Usuario:")
        new_password = st.text_input("Nueva Contraseña:", type='password')

        if st.button("Crear Usuario"):
            self.create_user(new_username, new_password)

        if st.button("Regresar"):
            self.main_interface()

    def create_user(self, username, password):
        """Crea un nuevo usuario."""
        if not username or not password:
            st.error("Usuario y contraseña no pueden estar vacíos.")
            return

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            st.error("La contraseña debe tener al menos 8 caracteres, incluir mayúsculas y números.")
            return

        st.session_state['users'][username] = password
        st.session_state['attempts'][username] = 0
        st.success("Usuario creado exitosamente.")
        self.main_interface()

    def login(self, username, password):
        """Verifica el usuario y la contraseña."""
        if username in st.session_state['users'] and st.session_state['users'][username] == password:
            st.session_state['current_user'] = username
            st.success("Inicio de sesión exitoso.")
            self.load_main_app(username)
        else:
            st.session_state['attempts'][username] = st.session_state['attempts'].get(username, 0) + 1
            if st.session_state['attempts'][username] >= 3:
                st.error("Usuario bloqueado. Demasiados intentos fallidos.")
            else:
                st.error("Usuario o contraseña incorrectos.")

    def load_main_app(self, username):
        """Carga la interfaz principal de la aplicación después de iniciar sesión."""
        st.subheader(f"Bienvenido a Papeles de trabajo Auditoría en sistemas Chalen, Luo y Palau, {username}")

        option = st.selectbox("Seleccione una opción", ["Carga de archivos", "Generación de análisis", "Papel de Trabajo"])

        if option == "Carga de archivos":
            self.setup_carga_archivos_tab()
        elif option == "Generación de análisis":
            self.setup_generacion_analisis_tab()
        elif option == "Papel de Trabajo":
            self.setup_papel_trabajo_tab()

        if st.button("Cerrar Sesión"):
            st.session_state['current_user'] = None
            self.main_interface()

    def setup_carga_archivos_tab(self):
        """Configura la pestaña de carga de archivos."""
        st.subheader("Carga de Archivos")
        st.session_state['files']['nomina'] = st.file_uploader("Carga archivo de nómina", type=["xlsx"])
        st.session_state['files']['asistencia'] = st.file_uploader("Carga archivo de asistencia", type=["xlsx"])
        st.session_state['files']['productividad'] = st.file_uploader("Carga archivo de productividad", type=["xlsx"])

    def setup_generacion_analisis_tab(self):
        """Configura la pestaña de generación de análisis."""
        st.subheader("Generación de Análisis")
        if st.button("Análisis de nómina"):
            self.analyze_nomina()
        if st.button("Análisis de asistencia"):
            self.analyze_asistencia()
        if st.button("Análisis de productividad"):
            self.analyze_productividad()

    def analyze_nomina(self):
        """Genera el análisis de nómina para detectar duplicados."""
        nomina_file = st.session_state['files']['nomina']
        if not nomina_file:
            st.error("No se ha cargado ningún archivo de nómina.")
            return

        df_nomina = pd.read_excel(nomina_file)
        duplicados_nombre = df_nomina[df_nomina.duplicated(subset='Nombre', keep=False)]
        duplicados_cuenta = df_nomina[df_nomina.duplicated(subset='Cuenta Bancaria', keep=False)]

        total_rows = len(df_nomina)
        anomalías = len(duplicados_nombre) + len(duplicados_cuenta)
        porcentaje_anomalías = (anomalías / total_rows) * 100 if total_rows > 0 else 0

        st.write(f"Anomalías identificadas:\n\nNúmero de Empleados duplicados: {len(duplicados_nombre)}\nNúmero de cuenta bancaria Empleados duplicadas: {len(duplicados_cuenta)}")

        # Guardar los datos para usarlos en el papel de trabajo
        st.session_state['nomina_data'] = {
            'df_nomina': df_nomina,
            'duplicados_nombre': duplicados_nombre,
            'duplicados_cuenta': duplicados_cuenta,
            'total_rows': total_rows,
            'porcentaje_anomalías': porcentaje_anomalías
        }

        # Generar el PDF del análisis
        self.create_nomina_pdf_report()

    def create_nomina_pdf_report(self):
        """Genera un reporte PDF con los resultados del análisis de nómina."""
        pdf_path = st.text_input("Escriba la ruta para guardar el PDF:", "nomina_report.pdf")
        if st.button("Generar Reporte PDF"):
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Título del reporte
            title = Paragraph("Análisis de Nómina - Anomalías Identificadas", styles['Title'])
            elements.append(title)

            # Auditor/es
            auditor_paragraph = Paragraph(f"Auditor/es: {st.session_state['current_user']}", styles['Normal'])
            elements.append(auditor_paragraph)

            # Resumen de las anomalías
            summary = Paragraph(f"<br/>Número de Empleados duplicados: {len(st.session_state['nomina_data']['duplicados_nombre'])}<br/>"
                                f"Número de cuentas bancarias duplicadas: {len(st.session_state['nomina_data']['duplicados_cuenta'])}<br/><br/>", styles['Normal'])
            elements.append(summary)

            # Sección 1: Listado de empleados duplicados por nombre
            elements.append(Paragraph("Listado de Empleados Duplicados:", styles['Heading2']))

            # Filtrado y ordenación alfabética para el primer listado
            filtered_data_1 = st.session_state['nomina_data']['duplicados_nombre'][['ID de Empleado', 'Nombre']].sort_values(by='Nombre')
            data_table_1 = [filtered_data_1.columns.tolist()] + filtered_data_1.values.tolist()

            table_1 = Table(data_table_1, repeatRows=1)
            table_1.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table_1)

            elements.append(Spacer(1, 12))
            st.write("Generando Reporte PDF...")
            doc.build(elements)
            st.success(f"Reporte PDF generado exitosamente en {pdf_path}.")

    def analyze_asistencia(self):
        """Genera el análisis de asistencia."""
        asistencia_file = st.session_state['files']['asistencia']
        if not asistencia_file:
            st.error("No se ha cargado ningún archivo de asistencia.")
            return

        df_asistencia = pd.read_excel(asistencia_file)
        meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        anomalías_mensuales = {}
        all_anomalías = pd.DataFrame()

        for mes in meses:
            columna = f'Días Trabajados en {mes}'
            if columna in df_asistencia.columns:
                anomalías_mensuales[mes] = df_asistencia[df_asistencia[columna] <= 20]
                all_anomalías = pd.concat([all_anomalías, anomalías_mensuales[mes]])
            else:
                st.error(f"No se encuentra la columna para {mes} en el archivo.")
                return

        all_anomalías = all_anomalías.drop_duplicates()
        total_anomalías = df_asistencia[df_asistencia['Total Días Trabajados'] < 120]
        all_anomalías = pd.concat([all_anomalías, total_anomalías]).drop_duplicates()

        st.write(f"Análisis de Asistencia:\n\nNúmero de empleados con anomalías en días trabajados por mes: {len(all_anomalías)}\n")

        st.session_state['asistencia_data'] = {
            'df_asistencia': df_asistencia,
            'anomalías_mensuales': anomalías_mensuales,
            'total_anomalías': total_anomalías,
            'all_anomalías': all_anomalías
        }

        self.create_asistencia_pdf_report()

    def create_asistencia_pdf_report(self):
        """Genera un reporte PDF con los resultados del análisis de asistencia."""
        pdf_path = st.text_input("Escriba la ruta para guardar el PDF:", "asistencia_report.pdf")
        if st.button("Generar Reporte PDF"):
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            title = Paragraph("Análisis de Asistencia - Anomalías Identificadas", styles['Title'])
            elements.append(title)

            auditor_paragraph = Paragraph(f"Auditor/es: {st.session_state['current_user']}", styles['Normal'])
            elements.append(auditor_paragraph)

            summary = Paragraph(f"<br/>Número de empleados con menos de 20 días trabajados en al menos un mes: {len(st.session_state['asistencia_data']['all_anomalías'])}<br/>"
                                f"Empleados con menos de 120 días trabajados en total: {len(st.session_state['asistencia_data']['total_anomalías'])}<br/><br/>", styles['Normal'])
            elements.append(summary)

            elements.append(Paragraph("Datos de Asistencia:", styles['Heading2']))
            data_table = [st.session_state['asistencia_data']['df_asistencia'].columns.tolist()] + st.session_state['asistencia_data']['df_asistencia'].values.tolist()
            
            table = Table(data_table, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

            elements.append(Spacer(1, 12))
            st.write("Generando Reporte PDF...")
            doc.build(elements)
            st.success(f"Reporte PDF generado exitosamente en {pdf_path}.")

    def analyze_productividad(self):
        """Genera el análisis de productividad."""
        productividad_file = st.session_state['files']['productividad']
        if not productividad_file:
            st.error("No se ha cargado ningún archivo de productividad.")
            return

        df_productividad = pd.read_excel(productividad_file)
        anomalías_mensuales = {}
        anomalías_totales = []

        for mes in ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']:
            anomalías_mensuales[mes] = df_productividad[df_productividad[f'Tareas Realizadas en {mes}'] < 17]

        total_anomalías = df_productividad[df_productividad['Productividad (Tareas - 6 meses)'] < 102]

        for mes in anomalías_mensuales:
            anomalías_totales.append(anomalías_mensuales[mes])

        anomalías_totales.append(total_anomalías)
        all_anomalías = pd.concat(anomalías_totales).drop_duplicates()

        st.write(f"Análisis de Productividad:\n\nNúmero de empleados con anomalías en tareas realizadas por mes: {len(all_anomalías)}\n")

        st.session_state['productividad_data'] = {
            'df_productividad': df_productividad,
            'anomalías_mensuales': anomalías_mensuales,
            'total_anomalías': total_anomalías,
            'all_anomalías': all_anomalías
        }

        self.create_productividad_pdf_report()

    def create_productividad_pdf_report(self):
        """Genera un reporte PDF con los resultados del análisis de productividad."""
        pdf_path = st.text_input("Escriba la ruta para guardar el PDF:", "productividad_report.pdf")
        if st.button("Generar Reporte PDF"):
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            title = Paragraph("Análisis de Productividad - Anomalías Identificadas", styles['Title'])
            elements.append(title)

            auditor_paragraph = Paragraph(f"Auditor/es: {st.session_state['current_user']}", styles['Normal'])
            elements.append(auditor_paragraph)

            summary = Paragraph(f"<br/>Número de empleados con menos de 17 tareas realizadas en al menos un mes: {len(st.session_state['productividad_data']['all_anomalías'])}<br/>"
                                f"Empleados con menos de 102 tareas realizadas en total: {len(st.session_state['productividad_data']['total_anomalías'])}<br/><br/>", styles['Normal'])
            elements.append(summary)

            elements.append(Paragraph("Datos de Productividad:", styles['Heading2']))
            data_table = [st.session_state['productividad_data']['df_productividad'].columns.tolist()] + st.session_state['productividad_data']['df_productividad'].values.tolist()
            
            table = Table(data_table, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

            elements.append(Spacer(1, 12))
            st.write("Generando Reporte PDF...")
            doc.build(elements)
            st.success(f"Reporte PDF generado exitosamente en {pdf_path}.")

    def setup_papel_trabajo_tab(self):
        """Configura la pestaña de Papel de Trabajo."""
        st.subheader("Generar Papel de Trabajo")
        if st.button("Generar Papel de Trabajo de Nómina"):
            self.generate_papel_trabajo_nomina()
        if st.button("Generar Papel de Trabajo de Asistencia"):
            self.generate_papel_trabajo_asistencia()
        if st.button("Generar Papel de Trabajo de Productividad"):
            self.generate_papel_trabajo_productividad()

    def generate_papel_trabajo_nomina(self):
        """Genera el papel de trabajo de nómina basado en el análisis realizado."""
        if 'nomina_data' not in st.session_state or not st.session_state['nomina_data']:
            st.error("No se ha realizado ningún análisis de nómina.")
            return

        porcentaje_anomalías = st.session_state['nomina_data']['porcentaje_anomalías']
        if porcentaje_anomalías == 0:
            st.write("Escenario 1: No se encontraron anomalías.")
        elif 0 < porcentaje_anomalías <= 15:
            st.write("Escenario 2: Se encontraron algunas anomalías.")
        else:
            st.write("Escenario 3: Se encontraron muchas anomalías.")
        st.write("Esta sección debería incluir la generación del papel de trabajo en base a las anomalías encontradas.")

    def generate_papel_trabajo_asistencia(self):
        """Genera el papel de trabajo de asistencia basado en el análisis realizado."""
        if 'asistencia_data' not in st.session_state or not st.session_state['asistencia_data']:
            st.error("No se ha realizado ningún análisis de asistencia.")
            return

        porcentaje_anomalías = len(st.session_state['asistencia_data']['all_anomalías']) / len(st.session_state['asistencia_data']['df_asistencia']) * 100
        if porcentaje_anomalías == 0:
            st.write("Escenario 1: No se encontraron anomalías.")
        elif 0 < porcentaje_anomalías <= 15:
            st.write("Escenario 2: Se encontraron algunas anomalías.")
        else:
            st.write("Escenario 3: Se encontraron muchas anomalías.")
        st.write("Esta sección debería incluir la generación del papel de trabajo en base a las anomalías encontradas.")

    def generate_papel_trabajo_productividad(self):
        """Genera el papel de trabajo de productividad basado en el análisis realizado."""
        if 'productividad_data' not in st.session_state or not st.session_state['productividad_data']:
            st.error("No se ha realizado ningún análisis de productividad.")
            return

        porcentaje_anomalías = len(st.session_state['productividad_data']['all_anomalías']) / len(st.session_state['productividad_data']['df_productividad']) * 100
        if porcentaje_anomalías == 0:
            st.write("Escenario 1: No se encontraron anomalías.")
        elif 0 < porcentaje_anomalías <= 15:
            st.write("Escenario 2: Se encontraron algunas anomalías.")
        else:
            st.write("Escenario 3: Se encontraron muchas anomalías.")
        st.write("Esta sección debería incluir la generación del papel de trabajo en base a las anomalías encontradas.")

# Inicialización de la aplicación
if __name__ == "__main__":
    app = AuditoriaApp()
    app.run()
