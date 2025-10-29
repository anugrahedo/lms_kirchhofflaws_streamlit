
import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import secrets
import string
import base64
from io import BytesIO
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- Firebase ---
import firebase_admin
from firebase_admin import credentials, db

# ===================== Konfigurasi ===================== #
st.set_page_config(
    page_title="LMS Fisika - Hukum Kirchhoff",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Local filenames (used only for on-prem migration fallback)
COURSES_FILE = "courses.json"
USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"
ATTENDANCE_FILE = "attendance.json"
FORUM_FILE = "forum.json"
COURSE_CODES_FILE = "course_codes.json"
NOTIFICATIONS_FILE = "notifications.json"
ASSIGNMENTS_FILE = "assignments.json"
SUBMISSIONS_FILE = "submissions.json"
VIRTUAL_LAB_FILE = "virtual_lab.json"

# ===================== CSS Custom ===================== #
def inject_custom_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
    }
    .electric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
    }
    .main-header {
        background: linear-gradient(90deg, #3498db, #2c3e50);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ===================== FIREBASE SETUP & HELPERS ===================== #
def init_firebase():
    if not firebase_admin._apps:
        # Expecting st.secrets["firebase"] to contain the service account JSON object
        # and st.secrets["databaseURL"] to contain the realtime DB URL.
        try:
            cred_dict = st.secrets["firebase"]
            databaseURL = st.secrets["databaseURL"]
        except Exception as e:
            st.error("Firebase credentials not found in Streamlit secrets. Please add service account JSON as 'firebase' and databaseURL.")
            st.stop()
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {'databaseURL': databaseURL})

def firebase_ref(path):
    """Return db reference for a path. Path may be 'courses' or 'courses/1/modules/2'"""
    return db.reference(path)

def fb_get(path):
    ref = firebase_ref(path)
    data = ref.get()
    return data

def fb_set(path, value):
    ref = firebase_ref(path)
    ref.set(value)

def fb_push(path, value):
    ref = firebase_ref(path)
    new_ref = ref.push(value)
    return new_ref.key

def fb_update(path, value):
    ref = firebase_ref(path)
    ref.update(value)

# Migration: if local JSON files exist (on your laptop), push them to Firebase once.
def migrate_local_to_firebase():
    # Only run migration when running locally (detect by presence of local files)
    files = {
        "courses": COURSES_FILE,
        "users": USERS_FILE,
        "progress": PROGRESS_FILE,
        "attendance": ATTENDANCE_FILE,
        "forum": FORUM_FILE,
        "course_codes": COURSE_CODES_FILE,
        "notifications": NOTIFICATIONS_FILE,
        "assignments": ASSIGNMENTS_FILE,
        "submissions": SUBMISSIONS_FILE,
        "virtual_lab": VIRTUAL_LAB_FILE
    }
    migrated = False
    for key, fname in files.items():
        if os.path.exists(fname):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Only migrate if firebase path empty
                if fb_get(key) is None:
                    fb_set(key, data)
                    migrated = True
            except Exception:
                pass
    if migrated:
        st.info("Migrasi data lokal ke Firebase selesai.")

# Wrapper functions used by the app (replace old load_data/save_data)
def load_data(path):
    """
    For compatibility, this function returns a Python list or dict.
    If the Firebase path is None, returns an empty list.
    """
    data = fb_get(path)
    if data is None:
        return []
    # Firebase may return dict keyed by push-keys; try to normalize to list where appropriate
    if isinstance(data, dict):
        # Heuristic: if values contain 'id' keys or are ordered numeric keys, return list
        values = list(data.values())
        # if dict is a mapping from numeric string ids to objects, convert
        try:
            # check if keys numeric (like "1","2") -> convert to list ordered by key
            if all(k.isdigit() for k in data.keys()):
                items = []
                for k in sorted(data.keys(), key=lambda x: int(x)):
                    items.append(data[k])
                return items
        except Exception:
            pass
        # If values are dicts with 'id' fields, return a list of those dicts
        if all(isinstance(v, dict) for v in values):
            return values
        # else return as-is (dict)
        return data
    return data

def save_data(path, data):
    """
    Save a list or dict to firebase path. Overwrites the path.
    """
    fb_set(path, data)

# Utility to get next numeric id for list stored as list
def next_id_from_list(lst):
    if not lst:
        return 1
    try:
        ids = [int(item.get("id", 0)) for item in lst if isinstance(item, dict) and "id" in item]
        return max(ids) + 1 if ids else len(lst) + 1
    except Exception:
        return len(lst) + 1

# Initialize Firebase and migrate if needed
init_firebase()
# Run migration only when local files exist (so it won't overwrite cloud)
migrate_local_to_firebase()

# ===================== App Logic (adapted) ===================== #
# Note: The remainder is adapted from your original app but uses load_data/save_data wrappers above.

def generate_course_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def init_data():
    # Create default data in Firebase if not present
    if not load_data("users"):
        admin = {
            "id": 1,
            "username": "edoanugrah",
            "password": "fisika123",
            "email": "anugrahedo50@gmail.com",
            "name": "Edo Anugrah",
            "role": "admin",
            "registered_at": datetime.now().isoformat()
        }
        save_data("users", [admin])
    if not load_data("courses"):
        default_course = {
            "id": 1,
            "title": "Hukum Kirchhoff - Dasar Teori dan Aplikasi",
            "description": "Kursus ini membahas konsep Hukum Kirchhoff tentang tegangan dan arus dalam rangkaian listrik sesuai Kurikulum Merdeka.",
            "instructor": "Edo Anugrah",
            "category": "Fisika - Kelistrikan",
            "level": "SMA Kelas 12",
            "created_at": datetime.now().isoformat(),
            "modules": []
        }
        save_data("courses", [default_course])
    if not load_data("course_codes"):
        code = generate_course_code()
        save_data("course_codes", [{"course_id": 1, "code": code, "is_active": True, "created_at": datetime.now().isoformat()}])

# ---------- Notification helpers ----------
def create_notification(user_id, title, message, notification_type="info", course_id=None, module_id=None):
    notifications = load_data("notifications") or []
    nid = next_id_from_list(notifications)
    new_notification = {
        "id": nid,
        "user_id": user_id,
        "title": title,
        "message": message,
        "type": notification_type,
        "course_id": course_id,
        "module_id": module_id,
        "is_read": False,
        "created_at": datetime.now().isoformat()
    }
    notifications.append(new_notification)
    save_data("notifications", notifications)
    return new_notification

def get_user_notifications(user_id, unread_only=False):
    notifications = load_data("notifications") or []
    res = [n for n in notifications if n.get("user_id")==user_id]
    if unread_only:
        res = [n for n in res if not n.get("is_read")]
    res.sort(key=lambda x: x.get("created_at"), reverse=True)
    return res

def mark_notification_as_read(notification_id):
    notifications = load_data("notifications") or []
    for n in notifications:
        if n.get("id") == notification_id:
            n["is_read"] = True
            n["read_at"] = datetime.now().isoformat()
            break
    save_data("notifications", notifications)

# ---------- Auth & Users ----------
def authenticate(username, password):
    users = load_data("users") or []
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None

def register_student(name, username, password, email):
    users = load_data("users") or []
    if any(u.get("username")==username for u in users):
        return False
    new_user = {
        "id": next_id_from_list(users),
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "role": "student",
        "registered_at": datetime.now().isoformat(),
        "enrolled_courses": []
    }
    users.append(new_user)
    save_data("users", users)
    return True

# ---------- Course & Modules ----------
def get_course_by_id(course_id):
    courses = load_data("courses") or []
    return next((c for c in courses if c.get("id")==course_id), None)

def save_course(course):
    courses = load_data("courses") or []
    updated = False
    for i,c in enumerate(courses):
        if c.get("id") == course.get("id"):
            courses[i] = course
            updated = True
            break
    if not updated:
        courses.append(course)
    save_data("courses", courses)

def get_module_by_id(modules, module_id):
    if not modules:
        return None
    return next((m for m in modules if m.get("id")==module_id), None)

# ---------- Progress ----------
def ensure_progress_for_user(user_id, course_id):
    progress = load_data("progress") or []
    existing = next((p for p in progress if p.get("user_id")==user_id and p.get("course_id")==course_id), None)
    if not existing:
        new_prog = {
            "user_id": user_id,
            "course_id": course_id,
            "progress": 0,
            "completed_modules": [],
            "enrolled_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        progress.append(new_prog)
        save_data("progress", progress)
        return new_prog
    return existing

# ---------- Attendance ----------
def mark_attendance(user_id, course_id, status="Hadir"):
    attendance = load_data("attendance") or []
    today = date.today().isoformat()
    for a in attendance:
        if a.get("user_id")==user_id and a.get("course_id")==course_id and a.get("date")==today:
            a["status"]=status
            a["updated_at"]=datetime.now().isoformat()
            save_data("attendance", attendance)
            return True
    attendance.append({"user_id": user_id, "course_id": course_id, "date": today, "status": status, "marked_at": datetime.now().isoformat()})
    save_data("attendance", attendance)
    return True

# ---------- Forum ----------
def post_forum_message(course_id, module_id, user_id, user_name, content, parent_id=None):
    forum = load_data("forum") or []
    msg_id = next_id_from_list(forum)
    msg = {"id": msg_id, "course_id": course_id, "module_id": module_id, "user_id": user_id, "user_name": user_name, "content": content, "parent_id": parent_id, "timestamp": datetime.now().isoformat()}
    forum.append(msg)
    save_data("forum", forum)
    return msg

# ---------- Assignments ----------
def create_assignment(course_id, module_id, title, description, due_date, max_points=100, file_types=None):
    assignments = load_data("assignments") or []
    new_assignment = {
        "id": next_id_from_list(assignments),
        "course_id": course_id,
        "module_id": module_id,
        "title": title,
        "description": description,
        "due_date": due_date.isoformat() if isinstance(due_date, date) else due_date,
        "max_points": max_points,
        "file_types": file_types or [".pdf", ".doc", ".docx", ".jpg", ".png"],
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    assignments.append(new_assignment)
    save_data("assignments", assignments)
    # notify students
    users = load_data("users") or []
    students = [u for u in users if u.get("role")=="student" and course_id in u.get("enrolled_courses",[])]
    for s in students:
        create_notification(s.get("id"), "📝 Tugas Baru", f"Tugas baru: {title} untuk Modul {module_id}", "info", course_id, module_id)
    return new_assignment

def submit_assignment(assignment_id, user_id, file_data, file_name, file_type, notes=""):
    submissions = load_data("submissions") or []
    existing = next((s for s in submissions if s.get("assignment_id")==assignment_id and s.get("user_id")==user_id), None)
    if existing:
        existing.update({"file_data": file_data, "file_name": file_name, "file_type": file_type, "notes": notes, "submitted_at": datetime.now().isoformat(), "status":"submitted"})
    else:
        new_sub = {
            "id": next_id_from_list(submissions),
            "assignment_id": assignment_id,
            "user_id": user_id,
            "file_data": file_data,
            "file_name": file_name,
            "file_type": file_type,
            "notes": notes,
            "submitted_at": datetime.now().isoformat(),
            "status": "submitted",
            "score": None,
            "feedback": None
        }
        submissions.append(new_sub)
    save_data("submissions", submissions)
    return True

# ---------- Virtual Lab ----------
def save_lab_result(user_id, circuit_type, parameters, results, analysis):
    v = load_data("virtual_lab") or []
    new_result = {"id": next_id_from_list(v), "user_id": user_id, "circuit_type": circuit_type, "parameters": parameters, "results": results, "analysis": analysis, "created_at": datetime.now().isoformat()}
    v.append(new_result)
    save_data("virtual_lab", v)
    return new_result

# ===================== UI / Routing ===================== #
def show_dashboard():
    inject_custom_css()
    st.markdown("<div class='main-header'><h1>Dashboard</h1><p>Selamat datang di LMS Fisika</p></div>", unsafe_allow_html=True)
    u = st.session_state.current_user
    st.write(f"Selamat belajar, {u.get('name')}!")
    # simple stats
    courses = load_data("courses") or []
    users = load_data("users") or []
    st.metric("Kursus", len(courses))
    st.metric("Pengguna", len(users))

def show_my_courses():
    inject_custom_css()
    courses = load_data("courses") or []
    if not courses:
        st.info("Belum ada kursus.")
        return
    course = courses[0]
    st.markdown(f"## {course.get('title')}\n{course.get('description')}")
    modules = course.get("modules", [])
    for m in modules:
        with st.expander(f"{m.get('id')}. {m.get('title')}"):
            st.write(m.get("content"))

def show_manage_modules():
    inject_custom_css()
    courses = load_data("courses") or []
    if not courses:
        st.warning("Belum ada kursus.")
        return
    course = courses[0]
    st.markdown(f"## Kelola Modul - {course.get('title')}")
    modules = course.get("modules", [])
    for mid in range(1, 12):
        m = get_module_by_id(modules, mid)
        title = st.text_input(f"Judul Modul {mid}", value=m.get("title") if m else f"Modul {mid}", key=f"title_{mid}")
        content = st.text_area(f"Konten Modul {mid}", value=m.get("content") if m else "", height=200, key=f"content_{mid}")
        if st.button(f"Simpan Modul {mid}", key=f"save_{mid}"):
            new_module = {"id": mid, "title": title, "content": content}
            found = False
            for i,mod in enumerate(modules):
                if mod.get("id")==mid:
                    modules[i] = new_module
                    found = True
                    break
            if not found:
                modules.append(new_module)
            course["modules"] = modules
            save_course(course)
            st.success(f"Modul {mid} tersimpan.")
            st.experimental_rerun()

def main():
    init_data()
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.current_user = None

    inject_custom_css()
    st.sidebar.title("LMS Fisika - Menu")
    menu = ["Login", "Dashboard", "Materi Pembelajaran", "Kelola Modul", "Profil"]
    choice = st.sidebar.selectbox("Pilih menu", menu)

    if choice == "Login":
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            uname = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.button("Login"):
                user = authenticate(uname, pwd)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user = user
                    st.success("Login berhasil")
                    st.experimental_rerun()
                else:
                    st.error("Login gagal")
        with tab2:
            name = st.text_input("Nama")
            uname = st.text_input("Username baru", key="reg_uname")
            pwd = st.text_input("Password baru", type="password", key="reg_pwd")
            email = st.text_input("Email", key="reg_email")
            if st.button("Daftar"):
                if name and uname and pwd and email:
                    ok = register_student(name, uname, pwd, email)
                    if ok:
                        st.success("Registrasi berhasil")
                    else:
                        st.error("Username sudah ada")

    else:
        if not st.session_state.authenticated:
            st.info("Silakan login dulu.")
            return
        # routing
        if choice == "Dashboard":
            show_dashboard()
        elif choice == "Materi Pembelajaran":
            show_my_courses()
        elif choice == "Kelola Modul":
            if st.session_state.current_user.get("role") == "admin":
                show_manage_modules()
            else:
                st.error("Hanya admin yang dapat mengakses.")
        elif choice == "Profil":
            u = st.session_state.current_user
            st.write(u)

if __name__ == "__main__":
    main()
