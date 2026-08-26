# final_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import smtplib
from email.message import EmailMessage
from io import BytesIO
from PIL import Image

# --- Initialize DB ---
conn = sqlite3.connect('report_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS uploads (username TEXT, filename TEXT, timestamp TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS reports (username TEXT, report_name TEXT, timestamp TEXT)''')

# --- User login system (basic) ---
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.username = username
            st.success("Logged in as admin")
        elif username == "user" and password == "user123":
            st.session_state.username = username
            st.success("Logged in as user")
        else:
            st.error("Invalid credentials")

# --- PDF Generator ---
def generate_pdf(df, chart_img, logo_img):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    if logo_img:
        elements.append(RLImage(logo_img, width=100, height=50))
    elements.append(Paragraph("<b>Data Report</b>", styles['Title']))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)
    elements.append(table)

    if chart_img:
        elements.append(Spacer(1, 12))
        elements.append(RLImage(chart_img, width=400, height=300))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- Email Sender ---
def send_email(to_email, pdf_buffer):
    msg = EmailMessage()
    msg['Subject'] = 'Your Data Report'
    msg['From'] = 'your_email@example.com'
    msg['To'] = to_email
    msg.set_content('Please find attached the generated report.')

    msg.add_attachment(pdf_buffer.read(), maintype='application', subtype='pdf', filename='report.pdf')
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('your_email@example.com', 'your_app_password')
            smtp.send_message(msg)
            return True
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False

# --- Main App ---
def main_app():
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Dashboard", "Generate Report", "My History", "Admin"])

    st.title("📊 Smart Report Dashboard")

    if menu == "Dashboard":
        st.header("Upload CSV & Visualize")
        uploaded = st.file_uploader("Upload CSV", type=['csv'])
        logo = st.file_uploader("Upload Logo (optional)", type=['png', 'jpg'])

        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df)
            c.execute("INSERT INTO uploads VALUES (?, ?, ?)", (st.session_state.username, uploaded.name, str(datetime.now())))
            conn.commit()

            chart = px.line(df, x=df.columns[0], y=df.columns[1])
            st.plotly_chart(chart)

            # Save chart image
            chart_buffer = BytesIO()
            chart.write_image(chart_buffer, format='png')
            chart_buffer.seek(0)

            logo_path = None
            if logo:
                logo_img = Image.open(logo)
                logo_buffer = BytesIO()
                logo_img.save(logo_buffer, format='PNG')
                logo_buffer.seek(0)
                logo_path = logo_buffer

            if st.button("Generate PDF"):
                pdf_buffer = generate_pdf(df, chart_buffer, logo_path)
                report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                c.execute("INSERT INTO reports VALUES (?, ?, ?)", (st.session_state.username, report_name, str(datetime.now())))
                conn.commit()
                st.download_button("Download PDF", data=pdf_buffer, file_name=report_name)

            email_to = st.text_input("Send report to (email):")
            if st.button("Send Email"):
                pdf_buffer = generate_pdf(df, chart_buffer, logo_path)
                if send_email(email_to, pdf_buffer):
                    st.success("Email sent!")

    elif menu == "My History":
        st.subheader("My Upload & Report History")
        uploads = c.execute("SELECT * FROM uploads WHERE username=?", (st.session_state.username,)).fetchall()
        reports = c.execute("SELECT * FROM reports WHERE username=?", (st.session_state.username,)).fetchall()
        st.write("### Uploaded Files")
        st.dataframe(pd.DataFrame(uploads, columns=["Username", "Filename", "Timestamp"]))
        st.write("### Generated Reports")
        st.dataframe(pd.DataFrame(reports, columns=["Username", "Report Name", "Timestamp"]))

    elif menu == "Admin" and st.session_state.username == "admin":
        st.subheader("Admin Activity Logs")
        st.write("### Upload Logs")
        st.dataframe(pd.read_sql("SELECT * FROM uploads", conn))
        st.write("### Report Logs")
        st.dataframe(pd.read_sql("SELECT * FROM reports", conn))

# --- Main Entry ---
if st.session_state.username:
    main_app()
else:
    login()
