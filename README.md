# AUTOMATED-REPORT-GENERATION

COMPANY : CODTECH IT SOLUTIONS

NAME : LIKHITHA N

INTERN ID : CT06DL625

DOMAIN : PYTHON PROGRAMMING

DURATION : 6 WEEKS

MENTOR : NEELA SANTOSH


# 📊 Enhanced Report Dashboard – Streamlit App

## 📝 Project Description

The **Enhanced Report Dashboard** is a powerful and interactive Python-based application built with Streamlit, designed to automate the process of generating PDF reports from CSV files. In a few clicks, users can upload a dataset, view data insights, generate a branded PDF report, and email it directly from the app. This project aims to simplify reporting tasks across industries, offering an intuitive and secure interface that requires no advanced technical knowledge from end users.

Beyond basic functionality, the app includes features like chart generation, secure login, email delivery, optional logo embedding, and admin-level log tracking. With a focus on automation, this project demonstrates practical application of data science tools, PDF formatting, database integration, and modern Python web development techniques.

---

## 🛠 Tools & Technologies Used

### 🧰 Core Technologies

* **Python**: The main programming language used to develop all application logic and backend functionality.

### 🖥️ Platform / Editor

* **Visual Studio Code (VS Code)**: Used for writing, testing, and debugging Python code, offering integrated terminal support and extensions for Streamlit and database management.

### 📚 Key Python Libraries

* **Streamlit**: For creating the interactive, browser-based dashboard with widgets, layout control, and file upload capability.
* **Pandas**: For reading, analyzing, and manipulating the CSV data files.
* **Matplotlib**: Automatically generates charts based on numeric columns in the uploaded dataset.
* **Pillow (PIL)**: To process the uploaded logo image for branding in the PDF report.
* **ReportLab**: Used to dynamically create styled and structured PDF reports.
* **smtplib & email.message**: For securely sending the generated PDF reports as email attachments.
* **sqlite3**: Used to store report generation history and logins in lightweight `.db` files.
* **dotenv**: To load sensitive variables like email credentials from `.env` securely.

---

## 📁 File Structure (As per your project)

Here's a breakdown of your project files as seen in the screenshot:

```
report_generating/
├── __pycache__/                # Python cache files
├── data.csv                    # Sample CSV data used for testing
├── exa.env                     # Environment file storing credentials (e.g., email/password)
├── logo.png                    # Optional logo image to brand the report
├── new.py                      # Likely a utility or test script (custom code)
├── report_app.py               # Main Streamlit application file
├── report_app.db               # SQLite database for logging admin actions
├── report_data.db              # SQLite database for storing user report history
├── requirements.txt            # List of dependencies for the project
```

Each of these files plays an important role in making the app fully functional.

---

## 💡 Key Features

### 🔐 Login Authentication

* Username/password login system using a Python dictionary or SQLite backend.
* Prevents unauthorized access and keeps user sessions tracked.
* Admin users can view all log activities.

### 📁 CSV Upload

* Users can upload `.csv` files via the sidebar.
* Displays a clean, interactive preview using `st.dataframe()`.

### 🖼️ Logo Upload (Branding)

* Optional branding support: users can upload a logo image (PNG/JPG).
* Logo appears at the top of the PDF report.

### 📄 PDF Report Generation

* With one click, generate a structured PDF containing:

  * Logo (if uploaded)
  * Timestamp
  * Title
  * Data table rendered from CSV
* Generated with the `ReportLab` library.

### 📊 Auto Charting

* Uses Matplotlib to analyze and generate a chart from the CSV.
* Automatically selects the first numeric column for plotting, along with a categorical column.

### 📧 Email Delivery

* Built-in form for entering sender and recipient emails.
* Sends the generated PDF as an attachment via Gmail SMTP (`smtp.gmail.com`).
* Uses environment variables to protect credentials.

### 🗂️ Report History

* Automatically logs each report generation (date, user, filename) into `report_data.db`.
* Users can view their full history of generated reports.

### 🛡️ Admin Logs

* If logged in as an admin, a full activity log from `report_app.db` can be viewed.
* Includes login timestamps, report generations, and emails sent.

---

## 💼 Applications & Use Cases

This tool has a wide range of potential use cases:

* **Corporate Reporting**: Generate branded sales, inventory, or HR reports and email them directly to stakeholders.
* **Academic Reporting**: Upload student marksheets, convert them into structured PDFs, and email them to faculty or students.
* **Freelance / Client Reporting**: Freelancers can easily turn raw client data into elegant, branded documents.
* **Administrative Dashboards**: Replace manual Excel work with instant report generation.

---

## 🛠 How to Run the Project

1. **Clone or copy the project folder**:

   ```
   git clone <your_repo_link>
   ```

2. **Install dependencies**:

   ```
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** (`exa.env`) with contents like:

   ```
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

4. **Run the Streamlit app**:

   ```
   streamlit run report_app.py
   ```

5. Open in your browser at: `http://localhost:8501`

---

## 🔒 Security Note

* Never share your `.env` file publicly.
* Consider hashing passwords and adding multi-user registration for production.
* You can upgrade to PostgreSQL or Firebase for more scalable database needs.

---

## 📌 Future Improvements

* Add file type validation for better input security.
* Include multi-chart support with user-selected columns.
* Enable role-based access control and full user management.
* Add scheduled email reports using `schedule` or `APScheduler`.

---

## ✅ Conclusion

The **Enhanced Report Dashboard** project is a complete, scalable reporting solution that brings together multiple powerful technologies in one accessible package. Whether for business, education, or freelance work, it automates the most common tasks involved in data reporting, offering a practical, real-world application of Python development.

![Image](https://github.com/user-attachments/assets/11fe3328-6cdf-4735-86d0-83659955f8cc)

![Image](https://github.com/user-attachments/assets/769b8b99-937e-4c28-92ad-acb861b74002)

![Image](https://github.com/user-attachments/assets/d4875fe3-16f8-4b8e-a74f-34682eba7c75)

![Image](https://github.com/user-attachments/assets/775c8ce9-04c4-481b-b7ac-d56a9b16da67)

![Image](https://github.com/user-attachments/assets/f17d8706-d52c-4a2b-90b6-da05facafbc3)

![Image](https://github.com/user-attachments/assets/9534d8c7-107d-4d0b-86c4-91a988dee0ee)

![Image](https://github.com/user-attachments/assets/8644dcc2-f874-4b64-b813-bcfd89a26c52)

![Image](https://github.com/user-attachments/assets/40da73a7-cbff-4243-b413-4775b54e8554)

![Image](https://github.com/user-attachments/assets/194ff2d0-961d-4fcf-812b-4c86b7658d92)

![Image](https://github.com/user-attachments/assets/2303a1b0-4fa7-4fdc-8f0e-a5df3ba64517)

![Image](https://github.com/user-attachments/assets/bce19759-cc25-4c19-87dd-16f5a34398df)

![Image](https://github.com/user-attachments/assets/0c466884-1988-4e30-b239-7b91df4adc06)

![Image](https://github.com/user-attachments/assets/ca2a2ca3-b1ca-474d-96b0-ff97aeaef687)

![Image](https://github.com/user-attachments/assets/9c48fbb2-e4cb-4aac-af65-349b8d880092)

![Image](https://github.com/user-attachments/assets/2739e27f-513e-41bb-8936-90d3db201bf5)

![Image](https://github.com/user-attachments/assets/7e2853e6-2593-4f23-8383-896ca4f8439a)

![Image](https://github.com/user-attachments/assets/7150bbf9-ea1b-4592-9078-8581ecba0935)

![Image](https://github.com/user-attachments/assets/beda1bbe-cdd7-41e2-8116-e48f86e06266)






