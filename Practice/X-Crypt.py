import streamlit as st
import pickle
import os
from datetime import datetime

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FEEDBACK_DIR = os.path.join(BASE_DIR, "feedback")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# ================= CONFIG =================
ADMIN_PASSWORD = "xcryptadmin"

st.set_page_config(page_title="XCRYPT", layout="centered")
st.title("🔐 XCRYPT")

# ================= MODE SELECTION =================
mode = st.radio(
    "Select Mode",
    ["Encrypt", "Decrypt", "Submit Feedback", "Admin: View Feedback"]
)

# ================= ENCRYPT =================
if mode == "Encrypt":
    st.subheader("Encrypt Data")

    name = st.text_input("Your Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")
    password = st.text_input("Email Password", type="password")
    aadhar = st.text_input("Aadhar Number")
    city = st.text_input("City")
    state = st.text_input("State")
    filename = st.text_input("File name to save")

    if st.button("Encrypt & Save"):
        if filename:
            path = os.path.join(DATA_DIR, filename + ".dat")
            data = {
                "Name": name,
                "Phone": phone,
                "Email": email,
                "Password": password,
                "Aadhar": aadhar,
                "City": city,
                "State": state
            }
            with open(path, "wb") as f:
                pickle.dump(data, f)

            st.success("Data encrypted and saved successfully!")

# ================= DECRYPT =================
elif mode == "Decrypt":
    st.subheader("Decrypt Data")

    filename = st.text_input("Enter filename to decrypt")

    if st.button("Decrypt"):
        path = os.path.join(DATA_DIR, filename + ".dat")
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = pickle.load(f)

            st.write("### Decrypted Data")
            for k, v in data.items():
                st.write(f"**{k}:** {v}")
        else:
            st.error("File not found")

# ================= FEEDBACK =================
elif mode == "Submit Feedback":
    st.subheader("💬 Submit Feedback")

    fb_name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback")

    if st.button("Submit Feedback"):
        if fb_name and feedback:
            fb_path = os.path.join(FEEDBACK_DIR, fb_name + ".dat")

            fb_data = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "feedback": feedback
            }

            with open(fb_path, "ab") as f:
                pickle.dump(fb_data, f)

            st.success("Thank you for your feedback ❤️")

# ================= ADMIN VIEW =================
elif mode == "Admin: View Feedback":
    st.subheader("🔐 Admin Login")

    admin_pass = st.text_input("Enter Admin Password", type="password")

    if admin_pass == ADMIN_PASSWORD:
        st.success("Access Granted")

        entries = []

        files = os.listdir(FEEDBACK_DIR)
        for file in files:
            if not file.endswith(".dat"):
                continue

            name = file.replace(".dat", "")
            path = os.path.join(FEEDBACK_DIR, file)

            with open(path, "rb") as f:
                while True:
                    try:
                        data = pickle.load(f)

                        # 🔥 SAFE HANDLING (OLD + NEW DATA)
                        time_ = data.get("time", "N/A")
                        feedback_text = data.get("feedback", str(data))

                        entries.append((name, time_, feedback_text))

                    except EOFError:
                        break

        if entries:
            st.subheader("📒 Feedback Log")
            st.markdown("---")

            for name, time_, feedback in entries:
                st.markdown(f"**{name}**  \n🕒 {time_}  \n💬 {feedback}")
                st.markdown("---")
        else:
            st.info("No feedback available yet")

    elif admin_pass:
        st.error("Incorrect password")
