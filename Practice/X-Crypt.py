import streamlit as st
import pickle
import os
from datetime import datetime

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FEEDBACK_DIR = os.path.join(BASE_DIR, "feedback")
CONFIG_PATH = os.path.join(BASE_DIR, "config.pkl")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# ================= DEFAULT CONFIG =================
DEFAULT_CONFIG = {
    "APP_TITLE": "🔐 XCRYPT",
    "ADMIN_PASSWORD": "Xcrypt@ADMIN",
    "ADMIN_ENABLED": True,
    "MASTER_PASSWORD": "Master@XCRYPT"   # 🔥 super admin
}

# ================= LOAD / INIT CONFIG =================
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "wb") as f:
        pickle.dump(DEFAULT_CONFIG, f)

try:
    with open(CONFIG_PATH, "rb") as f:
        CONFIG = pickle.load(f)
except Exception:
    # fallback if config is corrupted or unreadable
    CONFIG = {
        "APP_TITLE": "🔐 XCRYPT",
        "ADMIN_PASSWORD": "xcryptadmin",
        "ADMIN_ENABLED": True,
        "MASTER_PASSWORD": "xcryptmaster"
    }
    with open(CONFIG_PATH, "wb") as f:
        pickle.dump(CONFIG, f)


# ================= PAGE CONFIG =================
st.set_page_config(page_title=CONFIG["APP_TITLE"], layout="centered")
st.title(CONFIG["APP_TITLE"])

# ================= MODE SELECTION =================
modes = ["Encrypt", "Decrypt", "Submit Feedback"]

if CONFIG["ADMIN_ENABLED"]:
    modes.append("Admin: View Feedback")

modes.append("Master Admin")

mode = st.radio("Select Mode", modes)

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

            st.success("Data encrypted and saved!")

# ================= DECRYPT =================
elif mode == "Decrypt":
    st.subheader("Decrypt Data")
    filename = st.text_input("Enter filename")

    if st.button("Decrypt"):
        path = os.path.join(DATA_DIR, filename + ".dat")
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = pickle.load(f)
            for k, v in data.items():
                st.write(f"**{k}:** {v}")
        else:
            st.error("File not found")

# ================= FEEDBACK =================
elif mode == "Submit Feedback":
    st.subheader("💬 Feedback")

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

            st.success("Feedback saved ❤️")

# ================= ADMIN VIEW =================
elif mode == "Admin: View Feedback":
    st.subheader("🔐 Admin Login")
    pwd = st.text_input("Admin Password", type="password")

    if pwd == CONFIG["ADMIN_PASSWORD"]:
        st.success("Access Granted")
        entries = []

        for file in os.listdir(FEEDBACK_DIR):
            if not file.endswith(".dat"):
                continue

            name = file.replace(".dat", "")
            path = os.path.join(FEEDBACK_DIR, file)

            with open(path, "rb") as f:
                while True:
                    try:
                        d = pickle.load(f)
                        time_ = d.get("time", "N/A")
                        text = d.get("feedback", str(d))
                        entries.append((name, time_, text))
                    except EOFError:
                        break

        for n, t, fb in entries:
            st.markdown(f"**{n}**  \n🕒 {t}  \n💬 {fb}")
            st.markdown("---")

    elif pwd:
        st.error("Wrong password")

# ================= MASTER ADMIN =================
elif mode == "Master Admin":
    st.subheader("🧠 Master Control Panel")

    mpwd = st.text_input("Master Password", type="password")

    if mpwd == CONFIG["MASTER_PASSWORD"]:
        st.success("Master Access Granted")

        new_title = st.text_input("App Title", CONFIG["APP_TITLE"])
        new_admin_pwd = st.text_input("Admin Password", CONFIG["ADMIN_PASSWORD"])
        admin_toggle = st.checkbox("Enable Admin Mode", CONFIG["ADMIN_ENABLED"])

        if st.button("Save Settings"):
            CONFIG["APP_TITLE"] = new_title
            CONFIG["ADMIN_PASSWORD"] = new_admin_pwd
            CONFIG["ADMIN_ENABLED"] = admin_toggle

            with open(CONFIG_PATH, "wb") as f:
                pickle.dump(CONFIG, f)

            st.success("Settings saved! Refresh app 🔄")

    elif mpwd:
        st.error("Wrong master password")



