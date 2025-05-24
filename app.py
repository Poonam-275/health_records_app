import streamlit as st
import datetime

# Initialize session state for users, records, and appointments
if 'users' not in st.session_state:
    st.session_state['users'] = {}  # username: {role, records, appointments}
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

def login():
    st.title("Health Records Management System")
    st.subheader("Login")
    username = st.text_input("Username")
    role = st.selectbox("Role", ["Patient", "Doctor"])
    if st.button("Login"):
        if username:
            # Initialize user if new
            if username not in st.session_state['users']:
                st.session_state['users'][username] = {
                    'role': role,
                    'records': [],  # list of dicts: {type, date, filename}
                    'appointments': []  # list of dicts: {doctor/patient, date, status}
                }
            st.session_state['current_user'] = username
            st.success(f"Logged in as {username} ({role})")
        else:
            st.error("Enter a username.")

def logout():
    st.session_state['current_user'] = None

def user_dashboard():
    user = st.session_state['current_user']
    role = st.session_state['users'][user]['role']
    st.sidebar.write(f"Logged in as {user} ({role})")
    if st.sidebar.button("Logout"):
        logout()
        return

    # Show role-specific options
    if role == "Patient":
        patient_menu()
    elif role == "Doctor":
        doctor_menu()

def patient_menu():
    user = st.session_state['current_user']
    user_data = st.session_state['users'][user]

    st.header("Patient Dashboard")
    st.subheader("Upload Health Record")
    with st.form("record_form"):
        file = st.file_uploader("Upload file (PDF, JPG, PNG, TXT)", type=["pdf", "jpg", "png", "txt"])
        record_type = st.text_input("Record Type (e.g., Lab Report)")
        date_str = st.text_input("Date (YYYY-MM-DD)", value=str(datetime.date.today()))
        submitted = st.form_submit_button("Upload")
        if submitted:
            if file and record_type:
                # Save metadata
                record = {
                    'type': record_type,
                    'date': date_str,
                    'filename': file.name,
                    'content': file.read()
                }
                user_data['records'].append(record)
                st.success(f"Record '{file.name}' uploaded.")
            else:
                st.error("Please provide file and record type.")

    st.subheader("My Records")
    if user_data['records']:
        for idx, rec in enumerate(user_data['records']):
            st.write(f"**{rec['type']}** on {rec['date']} - {rec['filename']}")
    else:
        st.info("No records uploaded yet.")

    st.subheader("Schedule Appointment")
    appointment_date = st.date_input("Select appointment date", min_value=datetime.date.today())
    doctor_name = st.text_input("Doctor's Name")
    if st.button("Book Appointment"):
        if doctor_name:
            appointment = {
                'doctor': doctor_name,
                'date': str(appointment_date),
                'status': 'Pending'
            }
            user_data['appointments'].append(appointment)
            st.success(f"Appointment with Dr. {doctor_name} on {appointment_date} booked.")
        else:
            st.error("Enter doctor's name.")

    st.subheader("My Appointments")
    for appt in user_data['appointments']:
        st.write(f"With Dr. {appt['doctor']} on {appt['date']} - Status: {appt['status']}")

def doctor_menu():
    user = st.session_state['current_user']
    doctor_name = user

    st.header("Doctor Dashboard")
    st.subheader("Search Patients")
    patient_name = st.text_input("Enter Patient Username to Search")
    if st.button("Search"):
        if patient_name in st.session_state['users']:
            patient_data = st.session_state['users'][patient_name]
            st.write(f"**Patient:** {patient_name}")
            st.write("**Records:**")
            if patient_data['records']:
                for rec in patient_data['records']:
                    st.write(f"- {rec['type']} on {rec['date']} ({rec['filename']})")
            else:
                st.write("No records.")
            st.write("**Appointments:**")
            for appt in patient_data['appointments']:
                st.write(f"- {appt['doctor']} on {appt['date']} - Status: {appt['status']}")
            # Optionally, add appointment approval or notes
        else:
            st.write("Patient not found.")

    st.subheader("View All My Appointments")
    # For simplicity, list all appointments where doctor is current user
    for username, data in st.session_state['users'].items():
        for appt in data['appointments']:
            if appt['doctor'] == doctor_name:
                st.write(f"Patient: {username} on {appt['date']} - Status: {appt['status']}")

# Main app logic
if 'current_user' not in st.session_state or st.session_state['current_user'] is None:
    login()
else:
    user_dashboard()
