import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
from datetime import datetime

class AuditoriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Papeles de trabajo Auditoría en sistemas Chalen, Luo y Palau")
        self.root.geometry("800x600")
        self.users = {}
        self.attempts = {}
        self.current_user = None
        self.files = {"nomina": None, "asistencia": None, "productividad": None}
        self.main_interface()

    def main_interface(self):
        """Crea la interfaz principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Pantalla de login
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=100)

        tk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.login_frame, text="Crear Usuario", command=self.create_user_interface).grid(row=3, column=0, columnspan=2, pady=5)

    def create_user_interface(self):
        """Interfaz para crear un nuevo usuario."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_user_frame = tk.Frame(self.root)
        self.create_user_frame.pack(pady=100)

        tk.Label(self.create_user_frame, text="Nuevo Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.new_username_entry = tk.Entry(self.create_user_frame)
        self.new_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.create_user_frame, text="Nueva Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.new_password_entry = tk.Entry(self.create_user_frame, show='*')
        self.new_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.create_user_frame, text="Crear Usuario", command=self.create_user).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.create_user_frame, text="Retornar", command=self.main_interface).grid(row=3, column=0, columnspan=2, pady=5)

    def create_user(self):
        """Crea un nuevo usuario."""
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña no pueden estar vacíos.")
            return

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas y números.")
            return

        self.users[username] = password
        self.attempts[username] = 0
        messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
        self.main_interface()

    def login(self):
        """Verifica el usuario y la contraseña."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            self.load_main_app(username)
        else:
            self.attempts[username] = self.attempts.get(username, 0) + 1
            if self.attempts[username] >= 3:
                messagebox.showerror("Error", "Usuario bloqueado. Demasiados intentos fallidos.")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def load_main_app(self, username):
        """Carga la interfaz principal de la aplicación después de iniciar sesión."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Bienvenido a Papeles de trabajo Auditoría en sistemas Chalen, Luo y Palau, {username}",
                 font=("Arial", 14)).pack(pady=20)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.tab_carga_archivos = tk.Frame(self.notebook)
        self.notebook.add(self.tab_carga_archivos, text="Carga de archivos")

        self.tab_generacion_analisis = tk.Frame(self.notebook)
        self.notebook.add(self.tab_generacion_analisis, text="Generación de análisis")

        self.tab_papel_trabajo = tk.Frame(self.notebook)
        self.notebook.add(self.tab_papel_trabajo, text="Papel de Trabajo")

        self.setup_carga_archivos_tab()
        self.setup_generacion_analisis_tab()
        self.setup_papel_trabajo_tab()

        tk.Button(self.root, text="Cerrar Sesión", command=self.main_interface).pack(pady=10)

    def setup_carga_archivos_tab(self):
        """Configura la pestaña de carga de archivos."""
        tk.Button(self.tab_carga_archivos, text="Carga archivo de nómina", command=self.load_nomina_file).pack(pady=10)
        tk.Button(self.tab_carga_archivos, text="Carga archivo de asistencia", command=self.load_asistencia_file).pack(pady=10)
        tk.Button(self.tab_carga_archivos, text="Carga archivo de productividad", command=self.load_productividad_file).pack(pady=10)

    def load_nomina_file(self):
        """Carga el archivo de nómina."""
        self.files['nomina'] = filedialog.askopenfilename(title="Selecciona el archivo de nómina", filetypes=[("Excel files", "*.xlsx")])
        if self.files['nomina']:
            messagebox.showinfo("Éxito", "Archivo de nómina cargado correctamente.")

    def load_asistencia_file(self):
        """Carga el archivo de asistencia."""
        self.files['asistencia'] = filedialog.askopenfilename(title="Selecciona el archivo de asistencia", filetypes=[("Excel files", "*.xlsx")])
        if self.files['asistencia']:
            messagebox.showinfo("Éxito", "Archivo de asistencia cargado correctamente.")

    def load_productividad_file(self):
        """Carga el archivo de productividad."""
        self.files['productividad'] = filedialog.askopenfilename(title="Selecciona el archivo de productividad", filetypes=[("Excel files", "*.xlsx")])
        if self.files['productividad']:
            messagebox.showinfo("Éxito", "Archivo de productividad cargado correctamente.")

    def setup_generacion_analisis_tab(self):
        """Configura la pestaña de generación de análisis."""
        tk.Button(self.tab_generacion_analisis, text="Análisis de nómina", command=self.analyze_nomina).pack(pady=10)
        tk.Button(self.tab_generacion_analisis, text="Análisis de asistencia", command=self.analyze_asistencia).pack(pady=10)
        tk.Button(self.tab_generacion_analisis, text="Análisis de productividad", command=self.analyze_productividad).pack(pady=10)

    def analyze_nomina(self):
        """Genera el análisis de nómina para detectar duplicados."""
        if not self.files['nomina']:
            messagebox.showerror("Error", "No se ha cargado ningún archivo de nómina.")
            return

        df_nomina = pd.read_excel(self.files['nomina'])
        duplicados_nombre = df_nomina[df_nomina.duplicated(subset='Nombre', keep=False)]
        duplicados_cuenta = df_nomina[df_nomina.duplicated(subset='Cuenta Bancaria', keep=False)]

        total_rows = len(df_nomina)
        anomalías = len(duplicados_nombre) + len(duplicados_cuenta)
        porcentaje_anomalías = (anomalías / total_rows) * 100 if total_rows > 0 else 0

        report = f"Anomalías identificadas:\n\nNúmero de Empleados duplicados: {len(duplicados_nombre)}\nNúmero de cuenta bancaria Empleados duplicadas: {len(duplicados_cuenta)}"
        messagebox.showinfo("Reporte de Nómina", report)

        # Guardar los datos para usarlos en el papel de trabajo
        self.nomina_data = {
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
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Título del reporte
        title = Paragraph("Análisis de Nómina - Anomalías Identificadas", styles['Title'])
        elements.append(title)

        # Auditor/es
        auditor_paragraph = Paragraph(f"Auditor/es: {self.current_user}", styles['Normal'])
        elements.append(auditor_paragraph)

        # Resumen de las anomalías
        summary = Paragraph(f"<br/>Número de Empleados duplicados: {len(self.nomina_data['duplicados_nombre'])}<br/>"
                            f"Número de cuentas bancarias duplicadas: {len(self.nomina_data['duplicados_cuenta'])}<br/><br/>", styles['Normal'])
        elements.append(summary)

        # Sección 1: Listado de empleados duplicados por nombre
        elements.append(Paragraph("Listado de Empleados Duplicados:", styles['Heading2']))

        # Filtrado y ordenación alfabética para el primer listado
        filtered_data_1 = self.nomina_data['duplicados_nombre'][['ID de Empleado', 'Nombre']].sort_values(by='Nombre')
        data_table_1 = [filtered_data_1.columns.tolist()] + filtered_data_1.values.tolist()

        # Ajuste para que las columnas de la tabla se adapten al ancho disponible
        table_1 = Table(data_table_1, colWidths=[doc.width / len(data_table_1[0])] * len(data_table_1[0]), repeatRows=1)
        
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

        # Sección 2: Listado de cuentas bancarias duplicadas
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Listado de Cuentas Bancarias Duplicadas:", styles['Heading2']))

        # Filtrado y ordenación alfabética para el segundo listado
        filtered_data_2 = self.nomina_data['duplicados_cuenta'][['ID de Empleado', 'Nombre', 'Cuenta Bancaria']].sort_values(by='Nombre')
        data_table_2 = [filtered_data_2.columns.tolist()] + filtered_data_2.values.tolist()

        # Ajuste para que las columnas de la tabla se adapten al ancho disponible
        table_2 = Table(data_table_2, colWidths=[doc.width / len(data_table_2[0])] * len(data_table_2[0]), repeatRows=1)
        
        table_2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_2)

        # Diagramas de pastel
        elements.append(Spacer(1, 12))
        self.create_pie_chart(len(self.nomina_data['duplicados_nombre']), self.nomina_data['total_rows'], "nombres_duplicados.png", "Porcentaje de Nombres Duplicados")
        self.create_pie_chart(len(self.nomina_data['duplicados_cuenta']), self.nomina_data['total_rows'], "cuentas_duplicadas.png", "Porcentaje de Cuentas Bancarias Duplicadas")

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Nombres Duplicados:", styles['Heading2']))
        elements.append(Image("nombres_duplicados.png", 4 * inch, 4 * inch))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Cuentas Bancarias Duplicadas:", styles['Heading2']))
        elements.append(Image("cuentas_duplicadas.png", 4 * inch, 4 * inch))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Reporte PDF generado exitosamente en {pdf_path}.")




    def create_pie_chart(self, count, total, filename, title):
        """Crea un gráfico de pastel y lo guarda como imagen."""
        if total == 0:
            return
        labels = ['Duplicados', 'Únicos']
        sizes = [count, total - count]
        colors = ['#ff9999','#66b3ff']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.axis('equal')  # Para que el gráfico sea circular
        plt.title(title)
        plt.savefig(filename)
        plt.close()

    def analyze_asistencia(self):
        """Genera el análisis de asistencia."""
        if not self.files['asistencia']:
            messagebox.showerror("Error", "No se ha cargado ningún archivo de asistencia.")
            return

        try:
            df_asistencia = pd.read_excel(self.files['asistencia'])
            meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            anomalías_mensuales = {}
            all_anomalías = pd.DataFrame()

            for mes in meses:
                columna = f'Días Trabajados en {mes}'
                if columna in df_asistencia.columns:
                    anomalías_mensuales[mes] = df_asistencia[df_asistencia[columna] <= 20]
                    all_anomalías = pd.concat([all_anomalías, anomalías_mensuales[mes]])
                else:
                    messagebox.showerror("Error", f"No se encuentra la columna para {mes} en el archivo.")
                    return

            all_anomalías = all_anomalías.drop_duplicates()
            total_anomalías = df_asistencia[df_asistencia['Total Días Trabajados'] < 120]
            all_anomalías = pd.concat([all_anomalías, total_anomalías]).drop_duplicates()

            report = f"Análisis de Asistencia:\n\nNúmero de empleados con anomalías en días trabajados por mes: {len(all_anomalías)}\n"
            messagebox.showinfo("Reporte de Asistencia", report)

            self.asistencia_data = {
                'df_asistencia': df_asistencia,
                'anomalías_mensuales': anomalías_mensuales,
                'total_anomalías': total_anomalías,
                'all_anomalías': all_anomalías
            }

            self.create_asistencia_pdf_report()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error durante el análisis de asistencia: {str(e)}")



    def create_asistencia_pdf_report(self):
        """Genera un reporte PDF con los resultados del análisis de asistencia."""
        try:
            pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not pdf_path:
                return  # Si el usuario cancela el diálogo de guardado, no continúa.

            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Título del reporte
            title = Paragraph("Análisis de Asistencia - Anomalías Identificadas", styles['Title'])
            elements.append(title)

            # Auditor/es
            auditor_paragraph = Paragraph(f"Auditor/es: {self.current_user}", styles['Normal'])
            elements.append(auditor_paragraph)

            # Resumen de las anomalías
            summary = Paragraph(f"<br/>Número de empleados con menos de 20 días trabajados en al menos un mes: {len(self.asistencia_data['all_anomalías'])}<br/>"
                                f"Empleados con menos de 120 días trabajados en total: {len(self.asistencia_data['total_anomalías'])}<br/><br/>", styles['Normal'])
            elements.append(summary)

            # Tabla con los datos del Excel
            elements.append(Paragraph("Datos de Asistencia:", styles['Heading2']))
            data_table = [self.asistencia_data['df_asistencia'].columns.tolist()] + self.asistencia_data['df_asistencia'].values.tolist()
            
            # Ajuste para que las columnas de la tabla se adapten al ancho disponible
            table = Table(data_table, colWidths=[doc.width / len(data_table[0])] * len(data_table[0]), repeatRows=1)
            
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

            # Diagramas de pastel
            elements.append(Spacer(1, 12))
            self.create_pie_chart(len(self.asistencia_data['all_anomalías']), len(self.asistencia_data['df_asistencia']), "dias_trabajados.png", "Porcentaje de Anomalías en Días Trabajados")

            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Gráfico de Días Trabajados:", styles['Heading2']))
            elements.append(Image("dias_trabajados.png", 4 * inch, 4 * inch))

            # Construir el documento PDF
            doc.build(elements)
            messagebox.showinfo("Éxito", f"Reporte PDF generado exitosamente en {pdf_path}.")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al generar el reporte PDF: {str(e)}")


    def create_pie_chart(self, count, total, filename, title):
        """Crea un gráfico de pastel y lo guarda como imagen."""
        if total == 0:
            return
        labels = ['Con Anomalías', 'Sin Anomalías']
        sizes = [count, total - count]
        colors = ['#ff9999','#66b3ff']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.axis('equal')  # Para que el gráfico sea circular
        plt.title(title)
        plt.savefig(filename)
        plt.close()


    def analyze_productividad(self):
        """Genera el análisis de productividad."""
        if not self.files['productividad']:
            messagebox.showerror("Error", "No se ha cargado ningún archivo de productividad.")
            return

        df_productividad = pd.read_excel(self.files['productividad'])
        anomalías_mensuales = {}
        anomalías_totales = []

        for mes in ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']:
            anomalías_mensuales[mes] = df_productividad[df_productividad[f'Tareas Realizadas en {mes}'] < 17]

        total_anomalías = df_productividad[df_productividad['Productividad (Tareas - 6 meses)'] < 102]

        for mes in anomalías_mensuales:
            anomalías_totales.append(anomalías_mensuales[mes])

        anomalías_totales.append(total_anomalías)
        all_anomalías = pd.concat(anomalías_totales).drop_duplicates()

        report = f"Análisis de Productividad:\n\nNúmero de empleados con anomalías en tareas realizadas por mes: {len(all_anomalías)}\n"
        messagebox.showinfo("Reporte de Productividad", report)

        self.productividad_data = {
            'df_productividad': df_productividad,
            'anomalías_mensuales': anomalías_mensuales,
            'total_anomalías': total_anomalías,
            'all_anomalías': all_anomalías
        }

        self.create_productividad_pdf_report()

    def create_productividad_pdf_report(self):
        """Genera un reporte PDF con los resultados del análisis de productividad."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        title = Paragraph("Análisis de Productividad - Anomalías Identificadas", styles['Title'])
        elements.append(title)

        auditor_paragraph = Paragraph(f"Auditor/es: {self.current_user}", styles['Normal'])
        elements.append(auditor_paragraph)

        summary = Paragraph(f"<br/>Número de empleados con menos de 17 tareas realizadas en al menos un mes: {len(self.productividad_data['all_anomalías'])}<br/>"
                            f"Empleados con menos de 102 tareas realizadas en total: {len(self.productividad_data['total_anomalías'])}<br/><br/>", styles['Normal'])
        elements.append(summary)

        elements.append(Paragraph("Datos de Productividad:", styles['Heading2']))
        data_table = [self.productividad_data['df_productividad'].columns.tolist()] + self.productividad_data['df_productividad'].values.tolist()
        
        # Ajuste para que las columnas de la tabla se adapten al ancho disponible
        table = Table(data_table, colWidths=[doc.width / len(data_table[0])] * len(data_table[0]), repeatRows=1)
        
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
        self.create_pie_chart(len(self.productividad_data['all_anomalías']), len(self.productividad_data['df_productividad']), "tareas_realizadas.png", "Porcentaje de Anomalías en Tareas Realizadas")

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Tareas Realizadas:", styles['Heading2']))
        elements.append(Image("tareas_realizadas.png", 4 * inch, 4 * inch))

        doc.build(elements)
        messagebox.showinfo("Éxito", f"Reporte PDF generado exitosamente en {pdf_path}.")


    def setup_papel_trabajo_tab(self):
        """Configura la pestaña de Papel de Trabajo."""
        tk.Button(self.tab_papel_trabajo, text="Generar Papel de Trabajo de Nómina", command=self.generate_papel_trabajo_nomina).pack(pady=10)
        tk.Button(self.tab_papel_trabajo, text="Generar Papel de Trabajo de Asistencia", command=self.generate_papel_trabajo_asistencia).pack(pady=10)
        tk.Button(self.tab_papel_trabajo, text="Generar Papel de Trabajo de Productividad", command=self.generate_papel_trabajo_productividad).pack(pady=10)

    def generate_papel_trabajo_nomina(self):
        """Genera el papel de trabajo de nómina basado en el análisis realizado."""
        if not hasattr(self, 'nomina_data'):
            messagebox.showerror("Error", "No se ha realizado ningún análisis de nómina.")
            return

        porcentaje_anomalías = self.nomina_data['porcentaje_anomalías']
        if porcentaje_anomalías == 0:
            self.create_papel_trabajo_nomina_escenario1()
        elif 0 < porcentaje_anomalías <= 15:
            self.create_papel_trabajo_nomina_escenario2()
        else:
            self.create_papel_trabajo_nomina_escenario3()

    def create_papel_trabajo_nomina_escenario1(self):
        """Genera el papel de trabajo de nómina para el escenario 1."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['nomina']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Nómina", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        
        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de nómina para asegurar que todos los pagos 
        correspondan a empleados reales y estén correctamente registrados.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de nómina y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se sospecha que podría haber empleados fantasmas en la nómina de Verde Campo. 
        La auditoría busca confirmar o descartar esta posibilidad.
        Alcance de la auditoría: Revisión de los registros de nómina y pagos bancarios correspondientes a los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron registros de nómina, contratos de trabajo, y extractos bancarios.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de nómina con la documentación de los empleados.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de nómina.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Todos los registros revisados coinciden correctamente; no se encontraron discrepancias. 
        Insertar porcentaje de anomalías encontradas: {self.nomina_data['porcentaje_anomalías']}%.
        Análisis de evidencias: Los registros de nómina corresponden con las cuentas bancarias verificadas y no se 
        detectaron empleados fantasmas.
        Cronología de eventos: No aplicable, ya que no se encontraron incidentes relevantes.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: No se identificaron impactos negativos en la organización relacionados con la nómina.
        Implicaciones legales y de cumplimiento: No se detectaron infracciones legales o normativas.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: No se requieren acciones correctivas.
        Mejoras en seguridad: Se recomienda continuar con los procedimientos actuales de validación de nómina.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: No se encontraron anomalías en los registros de nómina. La empresa mantiene un control adecuado sobre sus procesos de pago.
        Reflexión sobre controles: Los controles actuales son efectivos y no requieren modificaciones.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados duplicados en orden alfabético, la lista de 
        cuentas bancarias duplicadas ordenadas de menor a mayor, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con los gráficos de pastel que representan el porcentaje de nombres duplicados y de cuentas bancarias duplicadas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados duplicados por nombre
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados Duplicados por Nombre:", styles['Heading2']))
        empleados_duplicados_nombre = [self.nomina_data['duplicados_nombre'].columns.tolist()] + self.nomina_data['duplicados_nombre'].values.tolist()
        table_nombre = Table(empleados_duplicados_nombre, repeatRows=1)
        table_nombre.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_nombre)

        # Empleados duplicados por cuenta bancaria
        elements.append(Paragraph("Empleados Duplicados por Cuenta Bancaria:", styles['Heading2']))
        empleados_duplicados_cuenta = [self.nomina_data['duplicados_cuenta'].columns.tolist()] + self.nomina_data['duplicados_cuenta'].values.tolist()
        table_cuenta = Table(empleados_duplicados_cuenta, repeatRows=1)
        table_cuenta.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_cuenta)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Nombres Duplicados:", styles['Heading2']))
        elements.append(Image("nombres_duplicados.png", 4 * inch, 4 * inch))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Cuentas Bancarias Duplicadas:", styles['Heading2']))
        elements.append(Image("cuentas_duplicadas.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def create_papel_trabajo_nomina_escenario2(self):
        """Genera el papel de trabajo de nómina para el escenario 2."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['nomina']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Nómina", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de nómina para asegurar que todos los pagos 
        correspondan a empleados reales y estén correctamente registrados.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de nómina y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se sospecha que podría haber empleados fantasmas en la nómina. Esta auditoría busca verificar la validez de los registros de nómina.
        Alcance de la auditoría: Revisión de los registros de nómina y pagos bancarios correspondientes a los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron registros de nómina, contratos de trabajo, y extractos bancarios.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de nómina con la documentación de los empleados.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de nómina.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Se encontraron pequeñas discrepancias en los montos pagados a algunos empleados. 
        Insertar porcentaje de anomalías encontradas: {self.nomina_data['porcentaje_anomalías']}%.
        Análisis de evidencias: Aunque se detectaron diferencias en los pagos, estas no son significativas en términos de impacto financiero.
        Cronología de eventos: Las discrepancias se observaron esporádicamente a lo largo del periodo revisado.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: Las discrepancias no afectan de manera significativa la situación financiera de la empresa.
        Implicaciones legales y de cumplimiento: Las anomalías detectadas no constituyen una infracción legal o normativa grave.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: Revisar y ajustar los procesos de cálculo de nómina para corregir las discrepancias menores encontradas.
        Mejoras en seguridad: Implementar una revisión mensual de los registros de nómina para detectar y corregir errores menores de manera oportuna.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: Se encontraron anomalías menores en los registros de nómina que no son significativas. Se recomienda hacer ajustes menores.
        Reflexión sobre controles: Los controles son adecuados, pero pueden beneficiarse de una revisión adicional.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados duplicados en orden alfabético, la lista de 
        cuentas bancarias duplicadas ordenadas de menor a mayor, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con los gráficos de pastel que representan el porcentaje de nombres duplicados y de cuentas bancarias duplicadas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados duplicados por nombre
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados Duplicados por Nombre:", styles['Heading2']))
        empleados_duplicados_nombre = [self.nomina_data['duplicados_nombre'].columns.tolist()] + self.nomina_data['duplicados_nombre'].values.tolist()
        table_nombre = Table(empleados_duplicados_nombre, repeatRows=1)
        table_nombre.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_nombre)

        # Empleados duplicados por cuenta bancaria
        elements.append(Paragraph("Empleados Duplicados por Cuenta Bancaria:", styles['Heading2']))
        empleados_duplicados_cuenta = [self.nomina_data['duplicados_cuenta'].columns.tolist()] + self.nomina_data['duplicados_cuenta'].values.tolist()
        table_cuenta = Table(empleados_duplicados_cuenta, repeatRows=1)
        table_cuenta.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_cuenta)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Nombres Duplicados:", styles['Heading2']))
        elements.append(Image("nombres_duplicados.png", 4 * inch, 4 * inch))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Cuentas Bancarias Duplicadas:", styles['Heading2']))
        elements.append(Image("cuentas_duplicadas.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def create_papel_trabajo_nomina_escenario3(self):
        """Genera el papel de trabajo de nómina para el escenario 3."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['nomina']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Nómina", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de nómina para asegurar que todos los pagos 
        correspondan a empleados reales y estén correctamente registrados.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de nómina y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se sospecha la existencia de empleados fantasmas en la nómina. La auditoría forense busca identificar y evaluar la magnitud de cualquier fraude.
        Alcance de la auditoría: Revisión de los registros de nómina y pagos bancarios correspondientes a los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron registros de nómina, contratos de trabajo, y extractos bancarios.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de nómina con la documentación de los empleados.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de nómina.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Se detectaron trabajadores y cuentas duplicadas y cuentas bancarias que no corresponden a empleados reales, así como empleados fantasmas en la nómina. 
        Insertar porcentaje de anomalías encontradas: {self.nomina_data['porcentaje_anomalías']}%.
        Análisis de evidencias: Las discrepancias identificadas son materiales y sugieren la presencia de fraude o errores graves en el sistema de nómina.
        Cronología de eventos: Las anomalías materiales se observaron consistentemente durante el periodo revisado.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: Las anomalías detectadas tienen un impacto financiero significativo y pueden haber comprometido la integridad financiera de la empresa.
        Implicaciones legales y de cumplimiento: Las irregularidades detectadas podrían implicar infracciones legales graves y potenciales sanciones.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: Iniciar una revisión completa del sistema de nómina, incluyendo una auditoría externa, y tomar medidas disciplinarias contra los responsables.
        Mejoras en seguridad: Implementar controles más estrictos y auditorías internas regulares para prevenir futuros incidentes.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: Se encontraron anomalías materiales en los registros de nómina que requieren una acción inmediata y significativa.
        Reflexión sobre controles: Los controles actuales son inadecuados y necesitan una revisión urgente.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados duplicados en orden alfabético, la lista de 
        cuentas bancarias duplicadas ordenadas de menor a mayor, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con los gráficos de pastel que representan el porcentaje de nombres duplicados y de cuentas bancarias duplicadas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados duplicados por nombre
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados Duplicados por Nombre:", styles['Heading2']))
        empleados_duplicados_nombre = [self.nomina_data['duplicados_nombre'].columns.tolist()] + self.nomina_data['duplicados_nombre'].values.tolist()
        table_nombre = Table(empleados_duplicados_nombre, repeatRows=1)
        table_nombre.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_nombre)

        # Empleados duplicados por cuenta bancaria
        elements.append(Paragraph("Empleados Duplicados por Cuenta Bancaria:", styles['Heading2']))
        empleados_duplicados_cuenta = [self.nomina_data['duplicados_cuenta'].columns.tolist()] + self.nomina_data['duplicados_cuenta'].values.tolist()
        table_cuenta = Table(empleados_duplicados_cuenta, repeatRows=1)
        table_cuenta.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_cuenta)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Nombres Duplicados:", styles['Heading2']))
        elements.append(Image("nombres_duplicados.png", 4 * inch, 4 * inch))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Cuentas Bancarias Duplicadas:", styles['Heading2']))
        elements.append(Image("cuentas_duplicadas.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def generate_papel_trabajo_asistencia(self):
        """Genera el papel de trabajo de asistencia basado en el análisis realizado."""
        try:
            if not hasattr(self, 'asistencia_data'):
                messagebox.showerror("Error", "No se ha realizado ningún análisis de asistencia.")
                return

            # Calcular el porcentaje de anomalías
            total_empleados = len(self.asistencia_data['df_asistencia'])
            total_anomalías = len(self.asistencia_data['all_anomalías'])
            porcentaje_anomalías = (total_anomalías / total_empleados) * 100 if total_empleados > 0 else 0

            if porcentaje_anomalías == 0:
                self.create_papel_trabajo_asistencia_escenario1(porcentaje_anomalías)
            elif 0 < porcentaje_anomalías <= 15:
                self.create_papel_trabajo_asistencia_escenario2(porcentaje_anomalías)
            else:
                self.create_papel_trabajo_asistencia_escenario3(porcentaje_anomalías)

            messagebox.showinfo("Éxito", "Papel de trabajo de asistencia generado y guardado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al generar el papel de trabajo de asistencia: {str(e)}")




    def create_papel_trabajo_asistencia_escenario1(self, porcentaje_anomalías):
        """Genera el papel de trabajo de asistencia para el escenario 1."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['asistencia']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Asistencia", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de asistencia para asegurar que todos los 
        empleados cumplan con las políticas de la empresa.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de asistencia y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se realizó una auditoría para verificar la exactitud de los registros de asistencia. 
        No se encontraron anomalías significativas.
        Alcance de la auditoría: Revisión de los registros de asistencia de los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron los registros de asistencia proporcionados por el cliente.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de asistencia con las políticas de la empresa.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de asistencia.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: No se encontraron discrepancias significativas en los registros de asistencia. 
        Porcentaje de anomalías encontradas: {porcentaje_anomalías}%.
        Análisis de evidencias: Los registros de asistencia son coherentes con las políticas de la empresa.
        Cronología de eventos: No aplicable, ya que no se encontraron incidentes relevantes.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: No se identificaron impactos negativos en la organización relacionados con la asistencia.
        Implicaciones legales y de cumplimiento: No se detectaron infracciones legales o normativas.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: No se requieren acciones correctivas.
        Mejoras en seguridad: Se recomienda continuar con los procedimientos actuales de validación de asistencia.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: No se encontraron anomalías en los registros de asistencia. La empresa mantiene un control adecuado sobre sus procesos de asistencia.
        Reflexión sobre controles: Los controles actuales son efectivos y no requieren modificaciones.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados con menos de 20 días trabajados en orden alfabético, 
        la lista de empleados con menos de 120 días trabajados, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con el gráfico de pastel que representa el porcentaje de anomalías encontradas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados con menos de 20 días trabajados en algún mes
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados con Menos de 20 Días Trabajados en algún mes:", styles['Heading2']))
        empleados_menos_20_dias = [self.asistencia_data['all_anomalías'].columns.tolist()] + self.asistencia_data['all_anomalías'].values.tolist()
        table_menos_20_dias = Table(empleados_menos_20_dias, repeatRows=1)
        table_menos_20_dias.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_20_dias)

        # Empleados con menos de 120 días trabajados en total
        elements.append(Paragraph("Empleados con Menos de 120 Días Trabajados en total:", styles['Heading2']))
        empleados_menos_120_dias = [self.asistencia_data['total_anomalías'].columns.tolist()] + self.asistencia_data['total_anomalías'].values.tolist()
        table_menos_120_dias = Table(empleados_menos_120_dias, repeatRows=1)
        table_menos_120_dias.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_120_dias)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Anomalías en Días Trabajados:", styles['Heading2']))
        elements.append(Image("dias_trabajados.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def create_papel_trabajo_asistencia_escenario2(self, porcentaje_anomalías):
        """Genera el papel de trabajo de asistencia para el escenario 2."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['asistencia']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Asistencia", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de asistencia para asegurar que todos los 
        empleados cumplan con las políticas de la empresa.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de asistencia y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se realizó una auditoría para verificar la exactitud de los registros de asistencia. 
        Se encontraron algunas discrepancias menores.
        Alcance de la auditoría: Revisión de los registros de asistencia de los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron los registros de asistencia proporcionados por el cliente.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de asistencia con las políticas de la empresa.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de asistencia.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Se encontraron algunas discrepancias menores en los registros de asistencia. 
        Porcentaje de anomalías encontradas: {porcentaje_anomalías}%.
        Análisis de evidencias: Aunque se detectaron algunas diferencias, estas no son significativas en términos de cumplimiento.
        Cronología de eventos: Las discrepancias se observaron esporádicamente a lo largo del periodo revisado.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: Las discrepancias no afectan de manera significativa la situación de la empresa.
        Implicaciones legales y de cumplimiento: Las anomalías detectadas no constituyen una infracción legal o normativa grave.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: Revisar y ajustar los procesos de control de asistencia para corregir las discrepancias menores encontradas.
        Mejoras en seguridad: Implementar una revisión mensual de los registros de asistencia para detectar y corregir errores menores de manera oportuna.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: Se encontraron anomalías menores en los registros de asistencia que no son significativas. Se recomienda hacer ajustes menores.
        Reflexión sobre controles: Los controles son adecuados, pero pueden beneficiarse de una revisión adicional.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados con menos de 20 días trabajados en orden alfabético, 
        la lista de empleados con menos de 120 días trabajados, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con el gráfico de pastel que representa el porcentaje de anomalías encontradas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados con menos de 20 días trabajados en algún mes
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados con Menos de 20 Días Trabajados en algún mes:", styles['Heading2']))
        empleados_menos_20_dias = [self.asistencia_data['all_anomalías'].columns.tolist()] + self.asistencia_data['all_anomalías'].values.tolist()
        table_menos_20_dias = Table(empleados_menos_20_dias, repeatRows=1)
        table_menos_20_dias.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_20_dias)

        # Empleados con menos de 120 días trabajados en total
        elements.append(Paragraph("Empleados con Menos de 120 Días Trabajados en total:", styles['Heading2']))
        empleados_menos_120_dias = [self.asistencia_data['total_anomalías'].columns.tolist()] + self.asistencia_data['total_anomalías'].values.tolist()
        table_menos_120_dias = Table(empleados_menos_120_dias, repeatRows=1)
        table_menos_120_dias.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_120_dias)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Anomalías en Días Trabajados:", styles['Heading2']))
        elements.append(Image("dias_trabajados.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def create_papel_trabajo_asistencia_escenario3(self, porcentaje_anomalías):
        """Genera el papel de trabajo de asistencia para el escenario 3."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['asistencia']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Asistencia", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de asistencia para asegurar que todos los 
        empleados cumplan con las políticas de la empresa.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de asistencia y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se realizó una auditoría para verificar la exactitud de los registros de asistencia. 
        Se encontraron anomalías significativas que requieren atención inmediata.
        Alcance de la auditoría: Revisión de los registros de asistencia de los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron los registros de asistencia proporcionados por el cliente.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de asistencia con las políticas de la empresa.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de asistencia.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Se detectaron discrepancias significativas en los registros de asistencia. 
        Porcentaje de anomalías encontradas: {porcentaje_anomalías}%.
        Análisis de evidencias: Las discrepancias identificadas sugieren la necesidad de una revisión urgente del sistema de control de asistencia.
        Cronología de eventos: Las anomalías se observaron consistentemente durante el periodo revisado.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: Las anomalías detectadas tienen un impacto significativo en la organización.
        Implicaciones legales y de cumplimiento: Las irregularidades detectadas podrían implicar infracciones legales graves.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: Iniciar una revisión completa del sistema de control de asistencia.
        Mejoras en seguridad: Implementar controles más estrictos y auditorías internas regulares para prevenir futuros incidentes.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: Se encontraron anomalías significativas en los registros de asistencia que requieren acción inmediata.
        Reflexión sobre controles: Los controles actuales son inadecuados y necesitan una revisión urgente.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados con menos de 20 días trabajados en orden alfabético, 
        la lista de empleados con menos de 120 días trabajados, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con el gráfico de pastel que representa el porcentaje de anomalías encontradas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados con menos de 20 días trabajados en algún mes
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados con Menos de 20 Días Trabajados en algún mes:", styles['Heading2']))
        empleados_menos_20_dias = [self.asistencia_data['all_anomalías'].columns.tolist()] + self.asistencia_data['all_anomalías'].values.tolist()
        table_menos_20_dias = Table(empleados_menos_20_dias, repeatRows=1)
        table_menos_20_dias.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_20_dias)

        # Empleados con menos de 120 días trabajados en total
        elements.append(Paragraph("Empleados con Menos de 120 Días Trabajados en total:", styles['Heading2']))
        empleados_menos_120_dias = [self.asistencia_data['total_anomalías'].columns.tolist()] + self.asistencia_data['total_anomalías'].values.tolist()
        table_menos_120_dias = Table(empleados_menos_120_dias, repeatRows=1)
        table_menos_120_dias.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_120_dias)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Anomalías en Días Trabajados:", styles['Heading2']))
        elements.append(Image("dias_trabajados.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def generate_papel_trabajo_productividad(self):
        """Genera el papel de trabajo de productividad basado en el análisis realizado."""
        if not hasattr(self, 'productividad_data'):
            messagebox.showerror("Error", "No se ha realizado ningún análisis de productividad.")
            return

        porcentaje_anomalías = (len(self.productividad_data['all_anomalías']) / len(self.productividad_data['df_productividad'])) * 100
        if porcentaje_anomalías == 0:
            self.create_papel_trabajo_productividad_escenario1(porcentaje_anomalías)
        elif 0 < porcentaje_anomalías <= 15:
            self.create_papel_trabajo_productividad_escenario2(porcentaje_anomalías)
        else:
            self.create_papel_trabajo_productividad_escenario3(porcentaje_anomalías)

    def create_papel_trabajo_productividad_escenario1(self, porcentaje_anomalías):
        """Genera el papel de trabajo de productividad para el escenario 1."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['productividad']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Productividad", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """

        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de productividad para asegurar que todos los 
        empleados cumplan con las políticas de la empresa.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de productividad y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se realizó una auditoría para verificar la exactitud de los registros de productividad. 
        No se encontraron anomalías significativas.
        Alcance de la auditoría: Revisión de los registros de productividad de los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron los registros de productividad proporcionados por el cliente.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de productividad con las políticas de la empresa.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de productividad.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: No se encontraron discrepancias significativas en los registros de productividad. 
        Porcentaje de anomalías encontradas: {porcentaje_anomalías}%.
        Análisis de evidencias: Los registros de productividad son coherentes con las políticas de la empresa.
        Cronología de eventos: No aplicable, ya que no se encontraron incidentes relevantes.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: No se identificaron impactos negativos en la organización relacionados con la productividad.
        Implicaciones legales y de cumplimiento: No se detectaron infracciones legales o normativas.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: No se requieren acciones correctivas.
        Mejoras en seguridad: Se recomienda continuar con los procedimientos actuales de validación de productividad.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: No se encontraron anomalías en los registros de productividad. La empresa mantiene un control adecuado sobre sus procesos de productividad.
        Reflexión sobre controles: Los controles actuales son efectivos y no requieren modificaciones.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados con menos de 17 tareas realizadas en orden alfabético, 
        la lista de empleados con menos de 102 tareas realizadas, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con el gráfico de pastel que representa el porcentaje de anomalías encontradas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados con menos de 17 tareas realizadas en algún mes
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados con Menos de 17 Tareas Realizadas en algún mes:", styles['Heading2']))
        empleados_menos_17_tareas = [self.productividad_data['all_anomalías'].columns.tolist()] + self.productividad_data['all_anomalías'].values.tolist()
        table_menos_17_tareas = Table(empleados_menos_17_tareas, repeatRows=1)
        table_menos_17_tareas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_17_tareas)

        # Empleados con menos de 102 tareas realizadas en total
        elements.append(Paragraph("Empleados con Menos de 102 Tareas Realizadas en total:", styles['Heading2']))
        empleados_menos_102_tareas = [self.productividad_data['total_anomalías'].columns.tolist()] + self.productividad_data['total_anomalías'].values.tolist()
        table_menos_102_tareas = Table(empleados_menos_102_tareas, repeatRows=1)
        table_menos_102_tareas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_102_tareas)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Anomalías en Tareas Realizadas:", styles['Heading2']))
        elements.append(Image("tareas_realizadas.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def create_papel_trabajo_productividad_escenario2(self, porcentaje_anomalías):
        """Genera el papel de trabajo de productividad para el escenario 2."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['productividad']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Productividad", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de productividad para asegurar que todos los 
        empleados cumplan con las políticas de la empresa.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de productividad y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se realizó una auditoría para verificar la exactitud de los registros de productividad. 
        Se encontraron algunas discrepancias menores.
        Alcance de la auditoría: Revisión de los registros de productividad de los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron los registros de productividad proporcionados por el cliente.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de productividad con las políticas de la empresa.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de productividad.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Se encontraron algunas discrepancias menores en los registros de productividad. 
        Porcentaje de anomalías encontradas: {porcentaje_anomalías}%.
        Análisis de evidencias: Aunque se detectaron algunas diferencias, estas no son significativas en términos de cumplimiento.
        Cronología de eventos: Las discrepancias se observaron esporádicamente a lo largo del periodo revisado.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: Las discrepancias no afectan de manera significativa la situación de la empresa.
        Implicaciones legales y de cumplimiento: Las anomalías detectadas no constituyen una infracción legal o normativa grave.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: Revisar y ajustar los procesos de control de productividad para corregir las discrepancias menores encontradas.
        Mejoras en seguridad: Implementar una revisión mensual de los registros de productividad para detectar y corregir errores menores de manera oportuna.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: Se encontraron anomalías menores en los registros de productividad que no son significativas. Se recomienda hacer ajustes menores.
        Reflexión sobre controles: Los controles son adecuados, pero pueden beneficiarse de una revisión adicional.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados con menos de 17 tareas realizadas en orden alfabético, 
        la lista de empleados con menos de 102 tareas realizadas, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con el gráfico de pastel que representa el porcentaje de anomalías encontradas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados con menos de 17 tareas realizadas en algún mes
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados con Menos de 17 Tareas Realizadas en algún mes:", styles['Heading2']))
        empleados_menos_17_tareas = [self.productividad_data['all_anomalías'].columns.tolist()] + self.productividad_data['all_anomalías'].values.tolist()
        table_menos_17_tareas = Table(empleados_menos_17_tareas, repeatRows=1)
        table_menos_17_tareas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_17_tareas)

        # Empleados con menos de 102 tareas realizadas en total
        elements.append(Paragraph("Empleados con Menos de 102 Tareas Realizadas en total:", styles['Heading2']))
        empleados_menos_102_tareas = [self.productividad_data['total_anomalías'].columns.tolist()] + self.productividad_data['total_anomalías'].values.tolist()
        table_menos_102_tareas = Table(empleados_menos_102_tareas, repeatRows=1)
        table_menos_102_tareas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_102_tareas)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Anomalías en Tareas Realizadas:", styles['Heading2']))
        elements.append(Image("tareas_realizadas.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

    def create_papel_trabajo_productividad_escenario3(self, porcentaje_anomalías):
        """Genera el papel de trabajo de productividad para el escenario 3."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        fecha = datetime.now().strftime("%Y-%m-%d")
        auditor = self.current_user
        nombre_archivo = self.files['productividad']

        # Portada
        elements.append(Paragraph(f"Papel de Trabajo de Auditoría en Sistemas en soporte a la Auditoría Forense - Productividad", styles['Title']))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
        elements.append(Paragraph(f"Auditor/es: {auditor}", styles['Normal']))
        elements.append(Paragraph(f"Cliente/Organización: {nombre_archivo}", styles['Normal']))
        elements.append(PageBreak())

        # Índice
        indice_text = """
        1. Portada<br/>
        2. Índice<br/>
        3. Objetivo del Papel de Trabajo<br/>
        4. Antecedentes del Caso<br/>
        5. Metodología<br/>
        6. Hallazgos<br/>
        7. Evaluación de Impacto<br/>
        8. Recomendaciones<br/>
        9. Conclusión<br/>
        10. Anexos<br/>
        11. Firma del Auditor
        """
        elements.append(Paragraph("Índice", styles['Title']))
        elements.append(Paragraph(indice_text, styles['Normal']))
        elements.append(PageBreak())

        # Objetivo del Papel de Trabajo
        objetivo_text = """
        Propósito: Verificar la exactitud y legitimidad de los registros de productividad para asegurar que todos los 
        empleados cumplan con las políticas de la empresa.
        Uso del documento: Este documento servirá como referencia durante la auditoría forense para documentar 
        el proceso de revisión de productividad y los hallazgos correspondientes.
        """
        elements.append(Paragraph("Objetivo del Papel de Trabajo", styles['Title']))
        elements.append(Paragraph(objetivo_text, styles['Normal']))
        elements.append(PageBreak())

        # Antecedentes del Caso
        antecedentes_text = """
        Descripción del incidente: Se realizó una auditoría para verificar la exactitud de los registros de productividad. 
        Se encontraron anomalías significativas que requieren atención inmediata.
        Alcance de la auditoría: Revisión de los registros de productividad de los últimos 6 meses.
        """
        elements.append(Paragraph("Antecedentes del Caso", styles['Title']))
        elements.append(Paragraph(antecedentes_text, styles['Normal']))
        elements.append(PageBreak())

        # Metodología
        metodologia_text = """
        Procedimientos de recopilación de evidencia: Se revisaron los registros de productividad proporcionados por el cliente.
        Cadena de custodia: Los documentos fueron resguardados en un repositorio digital seguro con acceso limitado al equipo auditor.
        Análisis forense: Comparación detallada de los registros de productividad con las políticas de la empresa.
        Documentación de los procedimientos: Se documentaron todos los pasos seguidos en la revisión de los registros de productividad.
        """
        elements.append(Paragraph("Metodología", styles['Title']))
        elements.append(Paragraph(metodologia_text, styles['Normal']))
        elements.append(PageBreak())

        # Hallazgos
        hallazgos_text = f"""
        Evidencias clave: Se detectaron discrepancias significativas en los registros de productividad. 
        Porcentaje de anomalías encontradas: {porcentaje_anomalías}%.
        Análisis de evidencias: Las discrepancias identificadas sugieren la necesidad de una revisión urgente del sistema de control de productividad.
        Cronología de eventos: Las anomalías se observaron consistentemente durante el periodo revisado.
        """
        elements.append(Paragraph("Hallazgos", styles['Title']))
        elements.append(Paragraph(hallazgos_text, styles['Normal']))
        elements.append(PageBreak())

        # Evaluación de Impacto
        impacto_text = """
        Impacto en la organización: Las anomalías detectadas tienen un impacto significativo en la organización.
        Implicaciones legales y de cumplimiento: Las irregularidades detectadas podrían implicar infracciones legales graves.
        """
        elements.append(Paragraph("Evaluación de Impacto", styles['Title']))
        elements.append(Paragraph(impacto_text, styles['Normal']))
        elements.append(PageBreak())

        # Recomendaciones
        recomendaciones_text = """
        Acciones correctivas: Iniciar una revisión completa del sistema de control de productividad.
        Mejoras en seguridad: Implementar controles más estrictos y auditorías internas regulares para prevenir futuros incidentes.
        """
        elements.append(Paragraph("Recomendaciones", styles['Title']))
        elements.append(Paragraph(recomendaciones_text, styles['Normal']))
        elements.append(PageBreak())

        # Conclusión
        conclusion_text = """
        Resumen: Se encontraron anomalías significativas en los registros de productividad que requieren acción inmediata.
        Reflexión sobre controles: Los controles actuales son inadecuados y necesitan una revisión urgente.
        """
        elements.append(Paragraph("Conclusión", styles['Title']))
        elements.append(Paragraph(conclusion_text, styles['Normal']))
        elements.append(PageBreak())

        # Anexos
        anexos_text = """
        Se incluyen las listas de empleados con menos de 17 tareas realizadas en orden alfabético, 
        la lista de empleados con menos de 102 tareas realizadas, al lado del ID del empleado que se encuentra en la 
        columna “ID de Empleado”, junto con el gráfico de pastel que representa el porcentaje de anomalías encontradas.
        """
        elements.append(Paragraph("Anexos", styles['Title']))
        elements.append(Paragraph(anexos_text, styles['Normal']))

        # Anexar las tablas y gráficos
        # Empleados con menos de 17 tareas realizadas en algún mes
        elements.append(PageBreak())
        elements.append(Paragraph("Empleados con Menos de 17 Tareas Realizadas en algún mes:", styles['Heading2']))
        empleados_menos_17_tareas = [self.productividad_data['all_anomalías'].columns.tolist()] + self.productividad_data['all_anomalías'].values.tolist()
        table_menos_17_tareas = Table(empleados_menos_17_tareas, repeatRows=1)
        table_menos_17_tareas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_17_tareas)

        # Empleados con menos de 102 tareas realizadas en total
        elements.append(Paragraph("Empleados con Menos de 102 Tareas Realizadas en total:", styles['Heading2']))
        empleados_menos_102_tareas = [self.productividad_data['total_anomalías'].columns.tolist()] + self.productividad_data['total_anomalías'].values.tolist()
        table_menos_102_tareas = Table(empleados_menos_102_tareas, repeatRows=1)
        table_menos_102_tareas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table_menos_102_tareas)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Gráfico de Anomalías en Tareas Realizadas:", styles['Heading2']))
        elements.append(Image("tareas_realizadas.png", 4 * inch, 4 * inch))

        # Firma del Auditor
        elements.append(PageBreak())
        elements.append(Paragraph("Firma del Auditor", styles['Title']))
        firma_text = f"""
        Firma: {auditor}
        """
        elements.append(Paragraph(firma_text, styles['Normal']))

        # Construir el documento PDF
        doc.build(elements)
        messagebox.showinfo("Éxito", f"Papel de trabajo PDF generado exitosamente en {pdf_path}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AuditoriaApp(root)
    root.mainloop()
