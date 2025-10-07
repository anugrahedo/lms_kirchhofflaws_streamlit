import streamlit as st
import json
import os
from datetime import datetime, date

# ===================== Konfigurasi ===================== #
st.set_page_config(
    page_title="LMS Fisika - Hukum Kirchhoff",
    page_icon="⚡",
    layout="wide"
)

COURSES_FILE = "courses.json"
USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"
ATTENDANCE_FILE = "attendance.json"
FORUM_FILE = "forum.json"

# ===================== Helper I/O ===================== #
def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def init_data():
    for f in [COURSES_FILE, USERS_FILE, PROGRESS_FILE, ATTENDANCE_FILE, FORUM_FILE]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as file:
                json.dump([], file)

    # admin default
    users = load_data(USERS_FILE)
    if not any(u.get("username") == "edoanugrah" for u in users):
        admin = {
            "id": 1,
            "username": "edoanugrah",
            "password": "fisika123",
            "email": "anugrahedo50@gmail.com",
            "name": "Edo Anugrah",
            "role": "admin",
            "registered_at": datetime.now().isoformat()
        }
        users.append(admin)
        save_data(users, USERS_FILE)

    # course default
    courses = load_data(COURSES_FILE)
    if not courses:
        default_course = {
            "id": 1,
            "title": "Hukum Kirchhoff - Dasar Teori dan Aplikasi",
            "description": "Kursus ini membahas konsep Hukum Kirchhoff tentang tegangan dan arus dalam rangkaian listrik.",
            "instructor": "Edo Anugrah",
            "category": "Fisika - Kelistrikan",
            "level": "SMA Kelas 12",
            "created_at": datetime.now().isoformat(),
            "modules": []
        }
        save_data([default_course], COURSES_FILE)

# ===================== Auth ===================== #
def authenticate(username, password):
    users = load_data(USERS_FILE)
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None

def register_user(username, password, email, name, role="student"):
    users = load_data(USERS_FILE)
    if any(u.get("username") == username for u in users):
        return False, "❌ Username sudah terdaftar."
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "role": role,
        "registered_at": datetime.now().isoformat()
    }
    users.append(new_user)
    save_data(users, USERS_FILE)
    return True, "✅ Registrasi berhasil!"

# ===================== Modul helper ===================== #
def get_module_by_id(modules, mid):
    for m in modules:
        if m.get("id") == mid:
            return m
    return None

def render_module_content(m):
    if not m:
        st.write("_Modul ini belum tersedia._")
        return
    st.write(f"### {m.get('title','')}")
    if m.get("content"):
        st.write(m.get("content"))
    if m.get("video_url"):
        try:
            st.video(m.get("video_url"))
        except Exception:
            st.markdown(f"[Video]({m.get('video_url')})")
    if m.get("quiz_url"):
        st.markdown(f"🔍 **Quiz Modul:** [Buka Quiz]({m.get('quiz_url')})")
    if m.get("files"):
        st.write("📂 **File Pendukung:**")
        for f in m["files"]:
            st.markdown(f"- [{f.get('title','File')}]({f.get('url')})")

# ===================== Absensi ===================== #
def mark_attendance(user_id, course_id, status="Hadir"):
    attendance = load_data(ATTENDANCE_FILE)
    today = date.today().isoformat()
    for a in attendance:
        if a.get("user_id") == user_id and a.get("course_id") == course_id and a.get("date") == today:
            a["status"] = status
            a["updated_at"] = datetime.now().isoformat()
            save_data(attendance, ATTENDANCE_FILE)
            return True
    attendance.append({
        "user_id": user_id,
        "course_id": course_id,
        "date": today,
        "status": status,
        "marked_at": datetime.now().isoformat()
    })
    save_data(attendance, ATTENDANCE_FILE)
    return True

def get_attendance(course_id, date_str=None):
    attendance = load_data(ATTENDANCE_FILE)
    if date_str is None:
        date_str = date.today().isoformat()
    return [a for a in attendance if a.get("course_id") == course_id and a.get("date") == date_str]

# ===================== Forum ===================== #
def post_forum_message(course_id, module_id, user_id, user_name, content, parent_id=None):
    forum = load_data(FORUM_FILE)
    msg_id = (max([m.get("id",0) for m in forum]) + 1) if forum else 1
    msg = {
        "id": msg_id,
        "course_id": course_id,
        "module_id": module_id,
        "user_id": user_id,
        "user_name": user_name,
        "content": content,
        "parent_id": parent_id,
        "timestamp": datetime.now().isoformat()
    }
    forum.append(msg)
    save_data(forum, FORUM_FILE)
    return msg

def get_forum_threads(course_id, module_id=None):
    forum = load_data(FORUM_FILE)
    threads = [m for m in forum if m.get("course_id") == course_id and (module_id is None or m.get("module_id") == module_id)]
    threads_sorted = sorted(threads, key=lambda x: x.get("timestamp"))
    return threads_sorted

# ===================== Tampilan ===================== #
def show_welcome():
    st.title("⚡ LMS Fisika - Hukum Kirchhoff")
    st.subheader("Selamat Datang di LMS Fisika")
    try:
        st.video("https://youtu.be/ALeDH_6qn5M")
    except Exception:
        st.write("Video welcome: https://youtu.be/ALeDH_6qn5M")
    st.info("Silakan login untuk mulai belajar atau registrasi sebagai siswa.")

def show_dashboard():
    st.title("📊 Dashboard")
    courses = load_data(COURSES_FILE)
    users = load_data(USERS_FILE)
    students = [u for u in users if u.get("role") == "student"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jumlah Course", len(courses))
    with col2:
        st.metric("Jumlah Siswa", len(students))
    with col3:
        st.metric("Materi Aktif", courses[0].get("title") if courses else "-")

def show_my_courses():
    st.title("📚 Materi Pembelajaran")
    courses = load_data(COURSES_FILE)
    progress = load_data(PROGRESS_FILE)
    uid = st.session_state.current_user.get("id")

    user_prog = next((p for p in progress if p.get("user_id") == uid), None)
    if not user_prog:
        for c in courses:
            with st.expander(c.get("title","Untitled")):
                st.write(c.get("description",""))
                if st.button("Ikuti Materi Ini", key=f"enroll_{c.get('id')}"):
                    new_prog = {
                        "user_id": uid,
                        "course_id": c.get("id"),
                        "progress": 0,
                        "completed_modules": [],
                        "last_accessed": datetime.now().isoformat()
                    }
                    progress.append(new_prog)
                    save_data(progress, PROGRESS_FILE)
                    st.rerun()
    else:
        course = next((c for c in courses if c.get("id") == user_prog.get("course_id")), None)
        st.write(f"**{course.get('title')}**")
        st.progress(user_prog.get("progress",0) / 100)
        show_course_detail(course, user_prog)

def show_course_detail(course, user_prog=None):
    st.write(course.get("description"))
    modules = course.get("modules", [])
    progress_data = load_data(PROGRESS_FILE)

    # Absensi
    if st.session_state.current_user.get("role") == "student":
        st.subheader("📋 Absensi")
        today = date.today().isoformat()
        att = get_attendance(course.get("id"), today)
        my_att = next((a for a in att if a.get("user_id") == st.session_state.current_user.get("id")), None)
        if my_att:
            st.success(f"Anda sudah hadir ({my_att.get('status')})")
        else:
            if st.button("Tandai Hadir Hari Ini"):
                mark_attendance(st.session_state.current_user.get("id"), course.get("id"))
                st.success("✅ Absensi tersimpan.")
                st.rerun()

    st.subheader("📘 Modul Pembelajaran")
    for mid in range(1, 8):
        m = get_module_by_id(modules, mid)
        with st.expander(f"Modul {mid}: {m.get('title') if m else '(Belum tersedia)'}"):
            render_module_content(m)
            if user_prog and m:
                if mid in user_prog.get("completed_modules", []):
                    st.success("✅ Modul ini sudah selesai")
                else:
                    if st.button(f"Tandai selesai Modul {mid}", key=f"done_{mid}"):
                        user_prog["completed_modules"].append(mid)
                        user_prog["progress"] = int(len(user_prog["completed_modules"]) / 7 * 100)
                        user_prog["last_accessed"] = datetime.now().isoformat()
                        for i, p in enumerate(progress_data):
                            if p.get("user_id") == user_prog.get("user_id"):
                                progress_data[i] = user_prog
                        save_data(progress_data, PROGRESS_FILE)
                        st.success("✅ Modul ditandai selesai!")
                        st.rerun()

            st.markdown("---")
            st.write("💬 Forum Diskusi Modul")
            module_forum_ui(course.get("id"), mid)

    st.subheader("💬 Forum Diskusi Umum Course")
    module_forum_ui(course.get("id"), None)

# ===================== UI Forum ===================== #
def module_forum_ui(course_id, module_id):
    user = st.session_state.current_user
    threads = get_forum_threads(course_id, module_id)
    for msg in threads:
        if msg.get("parent_id") is None:
            st.markdown(f"**{msg.get('user_name')}** • _{msg.get('timestamp')}_")
            st.write(msg.get("content"))
            replies = [r for r in threads if r.get("parent_id") == msg.get("id")]
            for r in replies:
                st.markdown(f"> **{r.get('user_name')}** • _{r.get('timestamp')}_")
                st.markdown(f"> {r.get('content')}")
    text = st.text_area("Tulis pesan baru:", key=f"forum_{course_id}_{module_id}")
    if st.button("Kirim", key=f"send_{course_id}_{module_id}"):
        if text.strip():
            post_forum_message(course_id, module_id, user.get("id"), user.get("name"), text.strip())
            st.success("Pesan terkirim.")
            st.rerun()

# ===================== Admin ===================== #
def manage_users():
    st.title("👥 Kelola Siswa")
    users = load_data(USERS_FILE)
    students = [u for u in users if u.get("role") == "student"]
    for s in students:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{s.get('name')} ({s.get('username')}) - {s.get('email')}")
        with col2:
            if st.button("Hapus", key=f"del_{s.get('id')}"):
                users.remove(s)
                save_data(users, USERS_FILE)
                st.rerun()

def manage_modules():
    st.title("📝 Kelola Modul")
    courses = load_data(COURSES_FILE)
    if not courses:
        return
    course = st.selectbox("Pilih Course", courses, format_func=lambda c: c.get("title","Untitled"))
    modules = course.get("modules", [])

    for mid in range(1, 8):
        m = get_module_by_id(modules, mid)
        with st.expander(f"Modul {mid}: {m.get('title') if m else '(Belum tersedia)'}"):
            title = st.text_input("Judul", value=m.get("title") if m else "", key=f"title_{mid}")
            content = st.text_area("Konten", value=m.get("content") if m else "", key=f"content_{mid}")
            mtype = st.selectbox("Jenis", ["teori","video","lkpd","latihan","pembahasan"], 
                                 index=["teori","video","lkpd","latihan","pembahasan"].index(m.get("type")) if m and m.get("type") else 0,
                                 key=f"type_{mid}")
            video_url = st.text_input("Video URL", value=m.get("video_url") if m else "", key=f"video_{mid}")
            quiz_url = st.text_input("Quiz URL", value=m.get("quiz_url") if m else "", key=f"quiz_{mid}")
            file1 = st.text_input("File URL 1", value=(m.get("files",[{}])[0].get("url") if m and m.get("files") else ""), key=f"file1_{mid}")
            file1_title = st.text_input("Judul File 1", value=(m.get("files",[{}])[0].get("title") if m and m.get("files") else "File 1"), key=f"file1title_{mid}")
            file2 = st.text_input("File URL 2", value=(m.get("files",[{},{}])[1].get("url") if m and len(m.get("files",[]))>1 else ""), key=f"file2_{mid}")
            file2_title = st.text_input("Judul File 2", value=(m.get("files",[{},{}])[1].get("title") if m and len(m.get("files",[]))>1 else "File 2"), key=f"file2title_{mid}")

            if st.button("Simpan", key=f"save_{mid}"):
                new_m = {"id": mid, "title": title, "content": content, "type": mtype}
                if video_url: new_m["video_url"] = video_url
                if quiz_url: new_m["quiz_url"] = quiz_url
                files = []
                if file1: files.append({"title": file1_title, "url": file1})
                if file2: files.append({"title": file2_title, "url": file2})
                if files: new_m["files"] = files
                found = False
                for i, mm in enumerate(modules):
                    if mm.get("id") == mid:
                        modules[i] = new_m
                        found = True
                if not found:
                    modules.append(new_m)
                course["modules"] = modules
                for i, c in enumerate(courses):
                    if c.get("id") == course.get("id"):
                        courses[i] = course
                save_data(courses, COURSES_FILE)
                st.success(f"✅ Modul {mid} disimpan.")
                st.rerun()

def view_attendance_admin():
    st.title("📅 Lihat Absensi")
    courses = load_data(COURSES_FILE)
    if not courses:
        return
    course = st.selectbox("Pilih Course", courses, format_func=lambda c: c.get("title","Untitled"))
    date_sel = st.date_input("Tanggal", value=date.today())
    date_str = date_sel.isoformat()
    att = get_attendance(course.get("id"), date_str)
    users = load_data(USERS_FILE)
    if not att:
        st.write("Belum ada absensi.")
    else:
        for a in att:
            user = next((u for u in users if u.get("id") == a.get("user_id")), None)
            st.write(f"- {user.get('name') if user else a.get('user_id')}: {a.get('status')}")

# ===================== Profil ===================== #
def show_profile():
    st.title("👤 Profil")
    u = st.session_state.current_user
    st.write(f"Nama: {u.get('name')}")
    st.write(f"Username: {u.get('username')}")
    st.write(f"Email: {u.get('email')}")
    st.write(f"Role: {u.get('role')}")

# ===================== Main ===================== #
def main():
    init_data()
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.current_user = None

    if not st.session_state.authenticated:
        show_welcome()

    st.sidebar.title("⚡ LMS Fisika")
    if not st.session_state.authenticated:
        st.sidebar.subheader("Login")
        u = st.sidebar.text_input("Username")
        p = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = authenticate(u, p)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.rerun()
            else:
                st.sidebar.error("Login gagal")

        st.sidebar.subheader("Registrasi Siswa")
        name = st.sidebar.text_input("Nama")
        uname = st.sidebar.text_input("Username Baru")
        pwd = st.sidebar.text_input("Password Baru", type="password")
        email = st.sidebar.text_input("Email")
        if st.sidebar.button("Daftar"):
            if name and uname and pwd and email:
                ok, msg = register_user(uname, pwd, email, name)
                if ok:
                    st.sidebar.success(msg)
                else:
                    st.sidebar.error(msg)
            else:
                st.sidebar.error("Harap isi semua field registrasi.")
    else:
        st.sidebar.success(f"Login sebagai {st.session_state.current_user.get('name')}")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()

        role = st.session_state.current_user.get("role")
        if role == "admin":
            menu = st.sidebar.selectbox(
                "Menu", 
                ["Dashboard","Materi Pembelajaran","Kelola Siswa","Kelola Modul","Lihat Absensi","Profil"]
            )
        else:
            menu = st.sidebar.selectbox(
                "Menu", 
                ["Dashboard","Materi Pembelajaran","Profil"]
            )

        if menu == "Dashboard":
            show_dashboard()
        elif menu == "Materi Pembelajaran":
            show_my_courses()
        elif menu == "Kelola Siswa" and role=="admin":
            manage_users()
        elif menu == "Kelola Modul" and role=="admin":
            manage_modules()
        elif menu == "Lihat Absensi" and role=="admin":
            view_attendance_admin()
        elif menu == "Profil":
            show_profile()

if __name__ == "__main__":
    main()
