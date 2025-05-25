import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import base64
import smtplib
import sqlite3
import datetime
from email.message import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Enhanced Report Dashboard", layout="wide")
USER_CREDENTIALS = {"admin": "admin", "demo": "demo"}

from dotenv import load_dotenv
import os

# ----------------- DATABASE INIT -----------------
def init_db():
    conn = sqlite3.connect("report_app.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS report_history (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    filename TEXT,
                    timestamp TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_logs (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    action TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

def log_action(username, action):
    conn = sqlite3.connect("report_app.db")
    c = conn.cursor()
    c.execute("INSERT INTO admin_logs (username, action, timestamp) VALUES (?, ?, ?)",
              (username, action, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def save_report_history(username, filename):
    conn = sqlite3.connect("report_app.db")
    c = conn.cursor()
    c.execute("INSERT INTO report_history (username, filename, timestamp) VALUES (?, ?, ?)",
              (username, filename, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def fetch_report_history(username):
    conn = sqlite3.connect("report_app.db")
    df = pd.read_sql_query("SELECT * FROM report_history WHERE username=?", conn, params=(username,))
    conn.close()
    return df

def fetch_logs():
    conn = sqlite3.connect("report_app.db")
    df = pd.read_sql_query("SELECT * FROM admin_logs", conn)
    conn.close()
    return df

# ----------------- PDF GENERATOR -----------------
def generate_pdf(data, logo_img):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    if logo_img:
        logo_path = BytesIO()
        logo_img.save(logo_path, format='PNG')
        logo_path.seek(0)
        rl_img = RLImage(logo_path, width=100, height=40)
        elements.append(rl_img)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("📄 Auto-Generated Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    table_data = [list(data.columns)] + data.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ----------------- CHART GENERATOR -----------------
import matplotlib.pyplot as plt

def generate_chart(data):
    # Select only numeric columns
    numeric_cols = data.select_dtypes(include=['number']).columns

    # Need at least one numeric column to plot
    if len(numeric_cols) < 1:
        st.warning("⚠️ No numeric data available to generate a chart.")
        return None

    # Use the first non-numeric column (if exists) as x-axis
    non_numeric_cols = data.select_dtypes(exclude=['number']).columns
    x_col = non_numeric_cols[0] if len(non_numeric_cols) > 0 else numeric_cols[0]
    y_col = numeric_cols[0]

    fig, ax = plt.subplots()
    data.plot(kind='bar', x=x_col, y=y_col, ax=ax)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


# ----------------- EMAIL REPORT -----------------
def send_email(sender_email, sender_password, receiver_email, pdf_buffer):
    msg = EmailMessage()
    msg['Subject'] = 'Automated Report'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('Please find the attached report.')
    msg.add_attachment(pdf_buffer.read(), maintype='application', subtype='pdf', filename='report.pdf')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        load_dotenv()
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        #smtp.login(sender_email, sender_password)
        #smtp.send_message(msg)
        recipient_email = st.text_input("Enter recipient email")


# ----------------- APP START -----------------
init_db()
st.title("📊 Enhanced Report Dashboard")

# --- LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader("🔐 Login")
    col1, col2 = st.columns([1, 2])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if USER_CREDENTIALS.get(username) == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                log_action(username, "Logged in")
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    st.stop()

# --- LOGGED IN ---
st.sidebar.success(f"👤 Logged in as: {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.experimental_rerun()

# --- File Upload ---
csv_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
logo_file = st.sidebar.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])

if csv_file:
    df = pd.read_csv(csv_file)
    st.subheader("📄 Data Preview")
    st.dataframe(df)

    logo_img = Image.open(logo_file) if logo_file else None

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Generate PDF"):
            pdf_buffer = generate_pdf(df, logo_img)
            filename = f"{st.session_state.username}_report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            save_report_history(st.session_state.username, filename)
            log_action(st.session_state.username, "Generated PDF report")

            b64 = base64.b64encode(pdf_buffer.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

    with col2:
        with st.form("email_form"):
            sender = st.text_input("Sender Email")
            sender_pass = st.text_input("Sender Password", type="password")
            recipient = st.text_input("Recipient Email")
            submit = st.form_submit_button("📤 Send Email")
            if submit:
                pdf_buffer = generate_pdf(df, logo_img)
                send_email(sender, sender_pass, recipient, pdf_buffer)
                log_action(st.session_state.username, f"Emailed report to {recipient}")
                st.success("📧 Email sent!")

    with col3:
        st.download_button("⬇ Export CSV", data=df.to_csv(index=False), file_name="report.csv")

    st.subheader("📊 Chart")
    chart_buffer = generate_chart(df)
    if chart_buffer:
        st.image(chart_buffer, use_column_width=True)


# --- Report History ---
st.subheader("📁 Report History")
history_df = fetch_report_history(st.session_state.username)
st.dataframe(history_df)

# --- Admin Logs ---
if st.session_state.username == "admin":
    st.subheader("🛠️ Admin Logs")
    log_df = fetch_logs()
    st.dataframe(log_df)
