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

# ===================== Konfigurasi ===================== #
st.set_page_config(
    page_title="LMS Fisika - Hukum Kirchhoff",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

COURSES_FILE = "courses.json"
USERS_FILE = "users.json"
PROGRESS_FILE = "progress.json"
ATTENDANCE_FILE = "attendance.json"
FORUM_FILE = "forum.json"
COURSE_CODES_FILE = "course_codes.json"
NOTIFICATIONS_FILE = "notifications.json"
ASSIGNMENTS_FILE = "assignments.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSIONS_FILE = os.path.join(BASE_DIR, "submissions.json")
VIRTUAL_LAB_FILE = "virtual_lab.json"
QUIZZES_FILE = "quizzes.json"
QUIZ_RESULTS_FILE = "quiz_results.json"
MEDIA_FILE = "media_ajar.json"

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
    
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .electric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .circuit-card {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .main-header {
        background: linear-gradient(90deg, #3498db, #2c3e50);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .module-header {
        background: linear-gradient(90deg, #2c3e50, #34495e);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #1f618d 100%);
        transform: scale(1.05);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3498db, #2ecc71);
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-top: 4px solid #3498db;
    }
    
    .lab-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .notification-unread {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        border-left: 5px solid #e17055;
    }
    
    .notification-read {
        background: #f8f9fa;
        border-left: 5px solid #b2bec3;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        border: 1px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 20px 0;
        color: white;
        border-bottom: 2px solid #3498db;
        margin-bottom: 20px;
    }
    
    .quiz-card {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .question-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
    }
    
    .correct-answer {
        background: #d4edda !important;
        border-left: 4px solid #28a745 !important;
    }
    
    .wrong-answer {
        background: #f8d7da !important;
        border-left: 4px solid #dc3545 !important;
    }
    
    .media-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
    }
    
    @keyframes electricPulse {
        0% { box-shadow: 0 0 5px #3498db; }
        50% { box-shadow: 0 0 20px #3498db, 0 0 30px #2980b9; }
        100% { box-shadow: 0 0 5px #3498db; }
    }
    
    .electric-pulse {
        animation: electricPulse 2s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# ===================== Helper I/O ===================== #
def load_data(filename):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("[]")  # buat file json kosong
    with open(filename, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def generate_course_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def init_data():
    for f in [COURSES_FILE, USERS_FILE, PROGRESS_FILE, ATTENDANCE_FILE, FORUM_FILE, 
              COURSE_CODES_FILE, NOTIFICATIONS_FILE, ASSIGNMENTS_FILE, SUBMISSIONS_FILE, 
              VIRTUAL_LAB_FILE, QUIZZES_FILE, QUIZ_RESULTS_FILE, MEDIA_FILE]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as file:
                json.dump([], file)

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

    courses = load_data(COURSES_FILE)
    course_codes = load_data(COURSE_CODES_FILE)
    
    if not courses:
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
        save_data([default_course], COURSES_FILE)
        
        if not course_codes:
            course_code = generate_course_code()
            course_codes.append({
                "course_id": 1,
                "code": course_code,
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "max_students": None
            })
            save_data(course_codes, COURSE_CODES_FILE)

# ===================== Media Ajar System ===================== #
def save_media_file(file_data, file_name, file_type, file_size, media_type, description=""):
    """Menyimpan file media ajar"""
    media_data = load_data(MEDIA_FILE)
    
    new_media = {
        "id": len(media_data) + 1,
        "file_name": file_name,
        "file_type": file_type,
        "file_size": file_size,
        "media_type": media_type,  # modul_ajar, bahan_ajar, lkpd, media_pembelajaran
        "description": description,
        "file_data": base64.b64encode(file_data).decode(),
        "uploaded_at": datetime.now().isoformat(),
        "uploaded_by": st.session_state.current_user.get("id") if st.session_state.authenticated else None
    }
    
    media_data.append(new_media)
    save_data(media_data, MEDIA_FILE)
    return new_media

def get_media_by_id(media_id):
    """Mendapatkan media berdasarkan ID"""
    media_data = load_data(MEDIA_FILE)
    return next((m for m in media_data if m.get("id") == media_id), None)

def get_media_by_module(course_id, module_id):
    """Mendapatkan semua media untuk modul tertentu"""
    courses = load_data(COURSES_FILE)
    course = next((c for c in courses if c.get("id") == course_id), None)
    if not course:
        return []
    
    modules = course.get("modules", [])
    module = next((m for m in modules if m.get("id") == module_id), None)
    if not module:
        return []
    
    media_ids = module.get("media_ids", [])
    media_data = load_data(MEDIA_FILE)
    
    return [m for m in media_data if m.get("id") in media_ids]

def add_media_to_module(course_id, module_id, media_id):
    """Menambahkan media ke modul"""
    courses = load_data(COURSES_FILE)
    
    for course in courses:
        if course.get("id") == course_id:
            modules = course.get("modules", [])
            for module in modules:
                if module.get("id") == module_id:
                    if "media_ids" not in module:
                        module["media_ids"] = []
                    if media_id not in module["media_ids"]:
                        module["media_ids"].append(media_id)
                    break
    
    save_data(courses, COURSES_FILE)
    return True

def remove_media_from_module(course_id, module_id, media_id):
    """Menghapus media dari modul"""
    courses = load_data(COURSES_FILE)
    
    for course in courses:
        if course.get("id") == course_id:
            modules = course.get("modules", [])
            for module in modules:
                if module.get("id") == module_id:
                    if "media_ids" in module and media_id in module["media_ids"]:
                        module["media_ids"].remove(media_id)
                    break
    
    save_data(courses, COURSES_FILE)
    return True

def delete_media_file(media_id):
    """Menghapus file media"""
    media_data = load_data(MEDIA_FILE)
    media_data = [m for m in media_data if m.get("id") != media_id]
    save_data(media_data, MEDIA_FILE)
    return True

def get_file_icon(file_type):
    """Mendapatkan icon berdasarkan tipe file"""
    if file_type.startswith('image/'):
        return "🖼️"
    elif file_type.startswith('video/'):
        return "🎥"
    elif file_type.startswith('audio/'):
        return "🎵"
    elif file_type == 'application/pdf':
        return "📕"
    elif 'word' in file_type or file_type.endswith('.doc') or file_type.endswith('.docx'):
        return "📄"
    elif 'powerpoint' in file_type or file_type.endswith('.ppt') or file_type.endswith('.pptx'):
        return "📊"
    elif 'excel' in file_type or file_type.endswith('.xls') or file_type.endswith('.xlsx'):
        return "📈"
    elif 'zip' in file_type or file_type.endswith('.rar'):
        return "📦"
    else:
        return "📎"

def format_file_size(size_bytes):
    """Format ukuran file menjadi readable"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names)-1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def display_media_content(media):
    """Menampilkan konten media langsung di LMS"""
    file_data = base64.b64decode(media.get("file_data"))
    file_type = media.get("file_type")
    file_name = media.get("file_name")
    
    st.markdown(f"""
    <div class='media-card'>
        <h4>{get_file_icon(file_type)} {file_name}</h4>
        <p><strong>Jenis:</strong> {media.get('media_type').replace('_', ' ').title()} | 
           <strong>Ukuran:</strong> {format_file_size(media.get('file_size'))}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if media.get("description"):
        st.info(f"**Deskripsi:** {media.get('description')}")
    
    # Tampilkan konten berdasarkan tipe file
    if file_type.startswith('image/'):
        st.image(file_data, caption=file_name, use_column_width=True)
    
    elif file_type.startswith('video/'):
        st.video(file_data)
    
    elif file_type.startswith('audio/'):
        st.audio(file_data)
    
    elif file_type == 'application/pdf':
        # Untuk PDF, tampilkan download link dan preview jika memungkinkan
        st.markdown(create_download_link(file_data, file_name, file_type), unsafe_allow_html=True)
        st.info("📖 PDF dapat diunduh dan dibuka di perangkat Anda")
    
    elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                      'application/msword']:
        st.markdown(create_download_link(file_data, file_name, file_type), unsafe_allow_html=True)
        st.info("📄 Dokumen Word - Silakan unduh untuk melihat konten")
    
    elif file_type in ['application/vnd.openxmlformats-officedocument.presentationml.presentation',
                      'application/vnd.ms-powerpoint']:
        st.markdown(create_download_link(file_data, file_name, file_type), unsafe_allow_html=True)
        st.info("📊 Presentasi PowerPoint - Silakan unduh untuk melihat konten")
    
    else:
        st.markdown(create_download_link(file_data, file_name, file_type), unsafe_allow_html=True)
        st.info("📎 File dapat diunduh untuk dilihat")

def create_download_link(file_data, file_name, file_type):
    """Membuat link download untuk file"""
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:{file_type};base64,{b64}" download="{file_name}" style="background: #3498db; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px 0;">📥 Download {file_name}</a>'
    return href

# ===================== Quiz System ===================== #
def create_quiz(course_id, module_id, title, description, questions, quiz_type="pre-test", time_limit=None, max_attempts=1):
    """Membuat kuis baru"""
    quizzes = load_data(QUIZZES_FILE)
    
    new_quiz = {
        "id": len(quizzes) + 1,
        "course_id": course_id,
        "module_id": module_id,
        "title": title,
        "description": description,
        "questions": questions,
        "quiz_type": quiz_type,
        "time_limit": time_limit,
        "max_attempts": max_attempts,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "created_by": st.session_state.current_user.get("id") if st.session_state.authenticated else None
    }
    
    quizzes.append(new_quiz)
    save_data(quizzes, QUIZZES_FILE)
    
    # Notifikasi untuk siswa yang terdaftar
    users = load_data(USERS_FILE)
    enrolled_students = [u for u in users if u.get("role") == "student" and course_id in u.get("enrolled_courses", [])]
    
    for student in enrolled_students:
        create_notification(
            student.get("id"),
            "📝 Kuis Baru",
            f"Kuis {quiz_type}: {title} untuk Modul {module_id} telah tersedia.",
            "info",
            course_id,
            module_id
        )
    
    return new_quiz

def get_quizzes(course_id, module_id=None, quiz_type=None):
    """Mendapatkan daftar kuis"""
    quizzes = load_data(QUIZZES_FILE)
    filtered_quizzes = [q for q in quizzes if q.get("course_id") == course_id and q.get("is_active")]
    
    if module_id:
        filtered_quizzes = [q for q in filtered_quizzes if q.get("module_id") == module_id]
    
    if quiz_type:
        filtered_quizzes = [q for q in filtered_quizzes if q.get("quiz_type") == quiz_type]
    
    return filtered_quizzes

def get_quiz_by_id(quiz_id):
    """Mendapatkan kuis berdasarkan ID"""
    quizzes = load_data(QUIZZES_FILE)
    return next((q for q in quizzes if q.get("id") == quiz_id), None)

def submit_quiz_result(quiz_id, user_id, answers, score, total_questions, time_taken=None):
    """Menyimpan hasil kuis"""
    quiz_results = load_data(QUIZ_RESULTS_FILE)
    
    # Hitung attempt number
    user_attempts = [r for r in quiz_results if r.get("quiz_id") == quiz_id and r.get("user_id") == user_id]
    attempt_number = len(user_attempts) + 1
    
    new_result = {
        "id": len(quiz_results) + 1,
        "quiz_id": quiz_id,
        "user_id": user_id,
        "answers": answers,
        "score": score,
        "total_questions": total_questions,
        "percentage": round((score / total_questions) * 100, 2),
        "attempt_number": attempt_number,
        "time_taken": time_taken,
        "submitted_at": datetime.now().isoformat()
    }
    
    quiz_results.append(new_result)
    save_data(quiz_results, QUIZ_RESULTS_FILE)
    
    # Notifikasi untuk admin
    quiz = get_quiz_by_id(quiz_id)
    if quiz:
        users = load_data(USERS_FILE)
        student = next((u for u in users if u.get("id") == user_id), None)
        admins = [u for u in users if u.get("role") == "admin"]
        
        for admin in admins:
            create_notification(
                admin.get("id"),
                "📊 Kuis Diselesaikan",
                f"{student.get('name')} menyelesaikan kuis '{quiz.get('title')}' dengan nilai {new_result['percentage']}%",
                "info",
                quiz.get("course_id"),
                quiz.get("module_id")
            )
    
    return new_result

def get_quiz_results(quiz_id=None, user_id=None):
    """Mendapatkan hasil kuis"""
    quiz_results = load_data(QUIZ_RESULTS_FILE)
    
    if quiz_id:
        quiz_results = [r for r in quiz_results if r.get("quiz_id") == quiz_id]
    
    if user_id:
        quiz_results = [r for r in quiz_results if r.get("user_id") == user_id]
    
    return quiz_results

def get_user_quiz_attempts(quiz_id, user_id):
    """Mendapatkan jumlah attempt user untuk kuis tertentu"""
    quiz_results = load_data(QUIZ_RESULTS_FILE)
    return [r for r in quiz_results if r.get("quiz_id") == quiz_id and r.get("user_id") == user_id]

def calculate_quiz_score(questions, user_answers):
    """Menghitung skor kuis"""
    score = 0
    detailed_results = []
    
    for i, question in enumerate(questions):
        user_answer = user_answers.get(f"q_{i}")
        correct_answer = question.get("correct_answer")
        is_correct = user_answer == correct_answer
        
        if is_correct:
            score += 1
        
        detailed_results.append({
            "question": question.get("question"),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "options": question.get("options", [])
        })
    
    return score, detailed_results

# ===================== Virtual Lab System ===================== #
def save_lab_result(user_id, circuit_type, parameters, results, analysis):
    lab_results = load_data(VIRTUAL_LAB_FILE)
    
    new_result = {
        "id": len(lab_results) + 1,
        "user_id": user_id,
        "circuit_type": circuit_type,
        "parameters": parameters,
        "results": results,
        "analysis": analysis,
        "created_at": datetime.now().isoformat()
    }
    
    lab_results.append(new_result)
    save_data(lab_results, VIRTUAL_LAB_FILE)
    return new_result

def get_user_lab_results(user_id):
    lab_results = load_data(VIRTUAL_LAB_FILE)
    user_results = [r for r in lab_results if r.get("user_id") == user_id]
    user_results.sort(key=lambda x: x.get("created_at"), reverse=True)
    return user_results

def solve_kirchhoff_circuit(circuit_type, parameters):
    if circuit_type == "series":
        V = parameters["voltage"]
        R1 = parameters["R1"]
        R2 = parameters["R2"]
        R3 = parameters.get("R3", 0)
        
        R_total = R1 + R2 + R3
        I_total = V / R_total
        V1 = I_total * R1
        V2 = I_total * R2
        V3 = I_total * R3
        
        return {
            "I_total": round(I_total, 3),
            "V1": round(V1, 3),
            "V2": round(V2, 3),
            "V3": round(V3, 3),
            "R_total": round(R_total, 3),
            "P_total": round(V * I_total, 3)
        }
    
    elif circuit_type == "parallel":
        V = parameters["voltage"]
        R1 = parameters["R1"]
        R2 = parameters["R2"]
        R3 = parameters.get("R3", 0)
        
        if R3 > 0:
            R_total = 1 / (1/R1 + 1/R2 + 1/R3)
        else:
            R_total = 1 / (1/R1 + 1/R2)
            
        I_total = V / R_total
        I1 = V / R1
        I2 = V / R2
        I3 = V / R3 if R3 > 0 else 0
        
        return {
            "I_total": round(I_total, 3),
            "I1": round(I1, 3),
            "I2": round(I2, 3),
            "I3": round(I3, 3),
            "R_total": round(R_total, 3),
            "P_total": round(V * I_total, 3)
        }
    
    elif circuit_type == "complex":
        V1 = parameters["V1"]
        V2 = parameters["V2"]
        R1 = parameters["R1"]
        R2 = parameters["R2"]
        R3 = parameters["R3"]
        
        A = np.array([
            [R1 + R2, -R2],
            [-R2, R2 + R3]
        ])
        
        B = np.array([V1, -V2])
        
        try:
            I = np.linalg.solve(A, B)
            I1 = I[0]
            I2 = I[1]
            
            I_R1 = I1
            I_R2 = I1 - I2
            I_R3 = I2
            
            V_R1 = I_R1 * R1
            V_R2 = I_R2 * R2
            V_R3 = I_R3 * R3
            
            return {
                "I_loop1": round(I1, 3),
                "I_loop2": round(I2, 3),
                "I_R1": round(I_R1, 3),
                "I_R2": round(I_R2, 3),
                "I_R3": round(I_R3, 3),
                "V_R1": round(V_R1, 3),
                "V_R2": round(V_R2, 3),
                "V_R3": round(V_R3, 3),
                "P_total": round(V1 * I1 + V2 * I2, 3)
            }
        except:
            return {"error": "Tidak dapat menyelesaikan sistem persamaan"}

def analyze_kirchhoff_laws(results, circuit_type, parameters=None):
    analysis = []
    
    if circuit_type == "series":
        analysis.append(f"✅ Hukum Kirchhoff 1 (KCL): Arus sama di semua titik = {results['I_total']} A")
        voltage_sum = results["V1"] + results["V2"] + results.get("V3", 0)
        analysis.append(f"✅ Hukum Kirchhoff 2 (KVL): ΣV = {voltage_sum} V")
        
    elif circuit_type == "parallel":
        current_sum = results["I1"] + results["I2"] + results.get("I3", 0)
        analysis.append(f"✅ Hukum Kirchhoff 1 (KCL): I_total = ΣI_cabang = {current_sum} A")
        analysis.append(f"✅ Hukum Kirchhoff 2 (KVL): Tegangan sama di semua cabang paralel")
        
    elif circuit_type == "complex":
        node_current = results["I_R1"] - results["I_R2"] - results["I_R3"]
        analysis.append(f"✅ Hukum Kirchhoff 1 (KCL): ΣI_masuk = ΣI_keluar, selisih = {abs(round(node_current, 6))} A")
        
        if parameters:
            loop1_voltage = parameters.get("V1", 0) - results["V_R1"] - results["V_R2"]
            loop2_voltage = parameters.get("V2", 0) + results["V_R2"] - results["V_R3"]
            analysis.append(f"✅ Hukum Kirchhoff 2 (KVL): ΣV_loop1 = {round(loop1_voltage, 6)} V, ΣV_loop2 = {round(loop2_voltage, 6)} V")
        else:
            analysis.append("✅ Hukum Kirchhoff 2 (KVL): Perhitungan loop membutuhkan parameter rangkaian")
    
    return analysis

def create_circuit_diagram(circuit_type, parameters, results):
    if circuit_type == "series":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode='lines', line=dict(color='red', width=3), name='Baterai'))
        fig.add_trace(go.Scatter(x=[1, 2], y=[0, 0], mode='lines', line=dict(color='blue', width=2), name='R1'))
        fig.add_trace(go.Scatter(x=[2, 3], y=[0, 0], mode='lines', line=dict(color='green', width=2), name='R2'))
        
        fig.add_annotation(x=0.5, y=0.1, text=f"V = {parameters['voltage']}V", showarrow=False)
        fig.add_annotation(x=1.5, y=0.1, text=f"R1 = {parameters['R1']}Ω", showarrow=False)
        fig.add_annotation(x=2.5, y=0.1, text=f"R2 = {parameters['R2']}Ω", showarrow=False)
        fig.add_annotation(x=1.5, y=-0.1, text=f"I = {results['I_total']}A", showarrow=False)
        
        fig.update_layout(title="Rangkaian Seri", showlegend=False, 
                         xaxis=dict(visible=False), yaxis=dict(visible=False),
                         width=400, height=200)
        
    elif circuit_type == "parallel":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 3], y=[1, 1], mode='lines', line=dict(color='black', width=2)))
        fig.add_trace(go.Scatter(x=[0, 3], y=[0, 0], mode='lines', line=dict(color='black', width=2)))
        fig.add_trace(go.Scatter(x=[1, 1], y=[1, 0], mode='lines', line=dict(color='blue', width=2), name='R1'))
        fig.add_trace(go.Scatter(x=[2, 2], y=[1, 0], mode='lines', line=dict(color='green', width=2), name='R2'))
        fig.add_trace(go.Scatter(x=[0.2, 0.2], y=[0, 1], mode='lines', line=dict(color='red', width=3), name='Baterai'))
        
        fig.add_annotation(x=0.2, y=0.5, text=f"V = {parameters['voltage']}V", showarrow=False, textangle=-90)
        fig.add_annotation(x=1, y=0.5, text=f"R1 = {parameters['R1']}Ω", showarrow=False, textangle=-90)
        fig.add_annotation(x=2, y=0.5, text=f"R2 = {parameters['R2']}Ω", showarrow=False, textangle=-90)
        fig.add_annotation(x=1.5, y=1.1, text=f"I_total = {results['I_total']}A", showarrow=False)
        
        fig.update_layout(title="Rangkaian Paralel", showlegend=False,
                         xaxis=dict(visible=False), yaxis=dict(visible=False),
                         width=400, height=300)
    
    elif circuit_type == "complex":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 2, 2, 0, 0], y=[0, 0, 2, 2, 0], 
                                mode='lines', line=dict(color='blue', width=2), name='Loop 1'))
        fig.add_trace(go.Scatter(x=[2, 4, 4, 2, 2], y=[0, 0, 2, 2, 0], 
                                mode='lines', line=dict(color='green', width=2), name='Loop 2'))
        
        fig.add_annotation(x=1, y=0, text=f"R1 = {parameters['R1']}Ω", showarrow=False)
        fig.add_annotation(x=3, y=0, text=f"R3 = {parameters['R3']}Ω", showarrow=False)
        fig.add_annotation(x=2, y=1, text=f"R2 = {parameters['R2']}Ω", showarrow=False)
        fig.add_annotation(x=0, y=1, text=f"V1 = {parameters['V1']}V", showarrow=False)
        fig.add_annotation(x=4, y=1, text=f"V2 = {parameters['V2']}V", showarrow=False)
        fig.add_annotation(x=0.5, y=0.5, text=f"I1 = {results.get('I_loop1', 0)}A", showarrow=False)
        fig.add_annotation(x=3.5, y=0.5, text=f"I2 = {results.get('I_loop2', 0)}A", showarrow=False)
        
        fig.update_layout(title="Rangkaian Kompleks Dua Loop", showlegend=False,
                         xaxis=dict(visible=False), yaxis=dict(visible=False),
                         width=500, height=300)
    
    return fig

def create_results_chart(results, circuit_type):
    if circuit_type == "series":
        labels = ['Tegangan R1', 'Tegangan R2', 'Tegangan Total']
        values = [results['V1'], results['V2'], results['V1'] + results['V2']]
        fig = px.bar(x=labels, y=values, title="Distribusi Tegangan dalam Rangkaian Seri",
                    labels={'x': 'Komponen', 'y': 'Tegangan (V)'})
        fig.update_traces(marker_color=['blue', 'green', 'red'])
        
    elif circuit_type == "parallel":
        labels = ['Arus R1', 'Arus R2', 'Arus Total']
        values = [results['I1'], results['I2'], results['I_total']]
        fig = px.bar(x=labels, y=values, title="Distribusi Arus dalam Rangkaian Paralel",
                    labels={'x': 'Komponen', 'y': 'Arus (A)'})
        fig.update_traces(marker_color=['blue', 'green', 'red'])
        
    elif circuit_type == "complex":
        labels = ['Arus Loop 1', 'Arus Loop 2', 'Arus R1', 'Arus R2', 'Arus R3']
        values = [results.get('I_loop1', 0), results.get('I_loop2', 0), 
                 results.get('I_R1', 0), results.get('I_R2', 0), results.get('I_R3', 0)]
        fig = px.bar(x=labels, y=values, title="Distribusi Arus dalam Rangkaian Kompleks",
                    labels={'x': 'Komponen', 'y': 'Arus (A)'})
    
    return fig

# ===================== Virtual Lab UI ===================== #
def show_virtual_lab():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>🔬 Laboratorium Virtual Hukum Kirchhoff</h1>
        <p>Eksperimen Interaktif | Simulasi Rangkaian | Analisis Data Real-time</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='electric-card'>
        <h3>🌡️ Eksperimen Listrik Dinamis</h3>
        <p>Lakukan eksperimen virtual untuk memahami Hukum Kirchhoff melalui simulasi rangkaian listrik yang interaktif.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔌 Rangkaian Seri", "🔌 Rangkaian Paralel", "🔌 Rangkaian Kompleks", "📋 Riwayat Eksperimen"])
    
    with tab1:
        show_series_circuit_lab()
    with tab2:
        show_parallel_circuit_lab()
    with tab3:
        show_complex_circuit_lab()
    with tab4:
        show_lab_history()

def show_series_circuit_lab():
    st.header("🔌 Rangkaian Seri")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Konfigurasi Rangkaian")
        voltage = st.slider("Tegangan Sumber (V)", 1.0, 24.0, 12.0, 0.1, key="series_voltage")
        R1 = st.slider("Resistor 1 (Ω)", 1.0, 100.0, 10.0, 1.0, key="series_R1")
        R2 = st.slider("Resistor 2 (Ω)", 1.0, 100.0, 20.0, 1.0, key="series_R2")
        R3 = st.slider("Resistor 3 (Ω) - Opsional", 0.0, 100.0, 0.0, 1.0, key="series_R3")
        
        if st.button("Jalankan Eksperimen", key="run_series"):
            parameters = {"voltage": voltage, "R1": R1, "R2": R2, "R3": R3}
            results = solve_kirchhoff_circuit("series", parameters)
            analysis = analyze_kirchhoff_laws(results, "series", parameters)
            
            if st.session_state.authenticated:
                save_lab_result(st.session_state.current_user.get("id"), "series", parameters, results, analysis)
            
            st.session_state.series_results = results
            st.session_state.series_analysis = analysis
            st.session_state.series_params = parameters
    
    with col2:
        st.subheader("Hasil Eksperimen")
        if hasattr(st.session_state, 'series_results'):
            results = st.session_state.series_results
            analysis = st.session_state.series_analysis
            parameters = st.session_state.series_params
            
            st.plotly_chart(create_circuit_diagram("series", parameters, results), use_container_width=True)
            
            st.subheader("📊 Hasil Perhitungan")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Arus Total (I)", f"{results['I_total']} A")
                st.metric("Tegangan R1", f"{results['V1']} V")
                st.metric("Tegangan R2", f"{results['V2']} V")
            with col2:
                st.metric("Hambatan Total", f"{results['R_total']} Ω")
                st.metric("Daya Total", f"{results['P_total']} W")
                if parameters['R3'] > 0:
                    st.metric("Tegangan R3", f"{results.get('V3', 0)} V")
            
            st.plotly_chart(create_results_chart(results, "series"), use_container_width=True)
            
            st.subheader("🔍 Analisis Hukum Kirchhoff")
            for line in analysis:
                st.write(line)
        else:
            st.info("Atur parameter rangkaian dan klik 'Jalankan Eksperimen' untuk melihat hasil")

def show_parallel_circuit_lab():
    st.header("🔌 Rangkaian Paralel")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Konfigurasi Rangkaian")
        voltage = st.slider("Tegangan Sumber (V)", 1.0, 24.0, 12.0, 0.1, key="parallel_voltage")
        R1 = st.slider("Resistor 1 (Ω)", 1.0, 100.0, 10.0, 1.0, key="parallel_R1")
        R2 = st.slider("Resistor 2 (Ω)", 1.0, 100.0, 20.0, 1.0, key="parallel_R2")
        R3 = st.slider("Resistor 3 (Ω) - Opsional", 0.0, 100.0, 0.0, 1.0, key="parallel_R3")
        
        if st.button("Jalankan Eksperimen", key="run_parallel"):
            parameters = {"voltage": voltage, "R1": R1, "R2": R2, "R3": R3}
            results = solve_kirchhoff_circuit("parallel", parameters)
            analysis = analyze_kirchhoff_laws(results, "parallel", parameters)
            
            if st.session_state.authenticated:
                save_lab_result(st.session_state.current_user.get("id"), "parallel", parameters, results, analysis)
            
            st.session_state.parallel_results = results
            st.session_state.parallel_analysis = analysis
            st.session_state.parallel_params = parameters
    
    with col2:
        st.subheader("Hasil Eksperimen")
        if hasattr(st.session_state, 'parallel_results'):
            results = st.session_state.parallel_results
            analysis = st.session_state.parallel_analysis
            parameters = st.session_state.parallel_params
            
            st.plotly_chart(create_circuit_diagram("parallel", parameters, results), use_container_width=True)
            
            st.subheader("📊 Hasil Perhitungan")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Arus Total (I)", f"{results['I_total']} A")
                st.metric("Arus R1", f"{results['I1']} A")
                st.metric("Arus R2", f"{results['I2']} A")
            with col2:
                st.metric("Hambatan Total", f"{results['R_total']} Ω")
                st.metric("Daya Total", f"{results['P_total']} W")
                if parameters['R3'] > 0:
                    st.metric("Arus R3", f"{results.get('I3', 0)} A")
            
            st.plotly_chart(create_results_chart(results, "parallel"), use_container_width=True)
            
            st.subheader("🔍 Analisis Hukum Kirchhoff")
            for line in analysis:
                st.write(line)
        else:
            st.info("Atur parameter rangkaian dan klik 'Jalankan Eksperimen' untuk melihat hasil")

def show_complex_circuit_lab():
    st.header("🔌 Rangkaian Kompleks Dua Loop")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Konfigurasi Rangkaian")
        V1 = st.slider("Sumber Tegangan 1 (V)", 1.0, 24.0, 12.0, 0.1, key="complex_V1")
        V2 = st.slider("Sumber Tegangan 2 (V)", 1.0, 24.0, 6.0, 0.1, key="complex_V2")
        R1 = st.slider("Resistor 1 (Ω)", 1.0, 100.0, 10.0, 1.0, key="complex_R1")
        R2 = st.slider("Resistor 2 (Ω)", 1.0, 100.0, 20.0, 1.0, key="complex_R2")
        R3 = st.slider("Resistor 3 (Ω)", 1.0, 100.0, 30.0, 1.0, key="complex_R3")
        
        if st.button("Jalankan Eksperimen", key="run_complex"):
            parameters = {"V1": V1, "V2": V2, "R1": R1, "R2": R2, "R3": R3}
            results = solve_kirchhoff_circuit("complex", parameters)
            analysis = analyze_kirchhoff_laws(results, "complex", parameters)
            
            if st.session_state.authenticated:
                save_lab_result(st.session_state.current_user.get("id"), "complex", parameters, results, analysis)
            
            st.session_state.complex_results = results
            st.session_state.complex_analysis = analysis
            st.session_state.complex_params = parameters
    
    with col2:
        st.subheader("Hasil Eksperimen")
        if hasattr(st.session_state, 'complex_results'):
            results = st.session_state.complex_results
            analysis = st.session_state.complex_analysis
            parameters = st.session_state.complex_params
            
            if "error" in results:
                st.error("Tidak dapat menyelesaikan rangkaian. Coba ubah parameter.")
            else:
                st.plotly_chart(create_circuit_diagram("complex", parameters, results), use_container_width=True)
                
                st.subheader("📊 Hasil Perhitungan")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Arus Loop 1", f"{results['I_loop1']} A")
                    st.metric("Arus Loop 2", f"{results['I_loop2']} A")
                    st.metric("Arus R1", f"{results['I_R1']} A")
                with col2:
                    st.metric("Arus R2", f"{results['I_R2']} A")
                    st.metric("Arus R3", f"{results['I_R3']} A")
                    st.metric("Daya Total", f"{results['P_total']} W")
                
                st.plotly_chart(create_results_chart(results, "complex"), use_container_width=True)
                
                st.subheader("🔍 Analisis Hukum Kirchhoff")
                for line in analysis:
                    st.write(line)
        else:
            st.info("Atur parameter rangkaian dan klik 'Jalankan Eksperimen' untuk melihat hasil")

def show_lab_history():
    st.header("📋 Riwayat Eksperimen")
    
    if not st.session_state.authenticated:
        st.warning("Silakan login untuk melihat riwayat eksperimen Anda.")
        return
    
    user_id = st.session_state.current_user.get("id")
    lab_results = get_user_lab_results(user_id)
    
    if not lab_results:
        st.info("Belum ada riwayat eksperimen. Lakukan eksperimen di tab lainnya.")
        return
    
    for result in lab_results:
        with st.expander(f"🔬 {result['circuit_type'].title()} - {result['created_at'][:16]}"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Parameter")
                for key, value in result['parameters'].items():
                    st.write(f"**{key}:** {value}")
            with col2:
                st.subheader("Hasil")
                for key, value in result['results'].items():
                    if not key.startswith('_'):
                        st.write(f"**{key}:** {value}")
            st.subheader("Analisis Hukum Kirchhoff")
            for line in result['analysis']:
                st.write(line)

# ===================== Quiz UI Components ===================== #
def show_quiz_ui(course_id, module_id):
    """Menampilkan UI kuis untuk modul tertentu"""
    st.markdown("""
    <div class='quiz-card'>
        <h3>📝 Kuis Modul</h3>
        <p>Uji pemahaman Anda tentang materi modul ini dengan mengerjakan kuis berikut.</p>
    </div>
    """, unsafe_allow_html=True)
    
    quizzes = get_quizzes(course_id, module_id)
    current_user = st.session_state.current_user
    
    if not quizzes:
        st.info("Belum ada kuis untuk modul ini.")
        return
    
    for quiz in quizzes:
        with st.expander(f"🧠 {quiz.get('title')} - {quiz.get('quiz_type').title()}", expanded=True):
            st.write(f"**Deskripsi:** {quiz.get('description')}")
            st.write(f"**Jumlah Soal:** {len(quiz.get('questions', []))}")
            st.write(f"**Batas Attempt:** {quiz.get('max_attempts', 1)}")
            
            if quiz.get('time_limit'):
                st.write(f"**Batas Waktu:** {quiz.get('time_limit')} menit")
            
            # Cek attempt user
            user_attempts = get_user_quiz_attempts(quiz.get("id"), current_user.get("id"))
            max_attempts = quiz.get("max_attempts", 1)
            
            if len(user_attempts) >= max_attempts:
                st.warning(f"❌ Anda sudah mencapai batas attempt ({max_attempts}) untuk kuis ini.")
                
                # Tampilkan hasil terbaik
                best_result = max(user_attempts, key=lambda x: x.get("percentage", 0))
                st.write(f"**Nilai Terbaik:** {best_result.get('percentage')}%")
                
                if st.button("📊 Lihat Detail Hasil", key=f"view_results_{quiz.get('id')}"):
                    show_quiz_results_detail(quiz, user_attempts)
            else:
                remaining_attempts = max_attempts - len(user_attempts)
                st.success(f"✅ Anda memiliki {remaining_attempts} attempt tersisa.")
                
                if st.button("🚀 Mulai Kuis", key=f"start_quiz_{quiz.get('id')}"):
                    st.session_state.current_quiz = quiz
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_started = True
                    st.rerun()

def show_quiz_interface():
    """Menampilkan interface untuk mengerjakan kuis"""
    if not hasattr(st.session_state, 'current_quiz') or not st.session_state.current_quiz:
        st.warning("Tidak ada kuis yang aktif.")
        return
    
    quiz = st.session_state.current_quiz
    questions = quiz.get("questions", [])
    
    st.markdown(f"""
    <div class='main-header'>
        <h2>🧠 {quiz.get('title')}</h2>
        <p>{quiz.get('description')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form kuis
    with st.form(key="quiz_form"):
        st.subheader("📝 Soal-soal Kuis")
        
        for i, question in enumerate(questions):
            st.markdown(f"**{i+1}. {question.get('question')}**")
            
            options = question.get("options", [])
            user_answer = st.radio(
                f"Pilih jawaban untuk soal {i+1}:",
                options,
                key=f"q_{i}",
                index=None
            )
            
            if user_answer:
                st.session_state.quiz_answers[f"q_{i}"] = user_answer
            
            st.markdown("---")
        
        # Tombol submit
        submitted = st.form_submit_button("✅ Submit Kuis", use_container_width=True)
        
        if submitted:
            # Validasi jawaban
            if len(st.session_state.quiz_answers) != len(questions):
                st.error("❌ Harap jawab semua soal sebelum submit!")
                return
            
            # Hitung skor
            score, detailed_results = calculate_quiz_score(questions, st.session_state.quiz_answers)
            
            # Simpan hasil
            result = submit_quiz_result(
                quiz.get("id"),
                st.session_state.current_user.get("id"),
                st.session_state.quiz_answers,
                score,
                len(questions)
            )
            
            # Tampilkan hasil
            show_quiz_results(quiz, result, detailed_results)
            
            # Reset state
            st.session_state.quiz_started = False
            st.session_state.current_quiz = None
            st.session_state.quiz_answers = {}

def show_quiz_results(quiz, result, detailed_results):
    """Menampilkan hasil kuis"""
    st.markdown("""
    <div class='electric-card'>
        <h2>📊 Hasil Kuis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Skor", f"{result.get('score')}/{result.get('total_questions')}")
    with col2:
        st.metric("Persentase", f"{result.get('percentage')}%")
    with col3:
        st.metric("Attempt", f"{result.get('attempt_number')}")
    
    # Tampilkan detail per soal
    st.subheader("📋 Detail Jawaban")
    
    for i, detail in enumerate(detailed_results):
        question_class = "correct-answer" if detail.get("is_correct") else "wrong-answer"
        
        st.markdown(f"""
        <div class='question-card {question_class}'>
            <h4>Soal {i+1}: {detail.get('question')}</h4>
            <p><strong>Jawaban Anda:</strong> {detail.get('user_answer')}</p>
            <p><strong>Jawaban Benar:</strong> {detail.get('correct_answer')}</p>
            <p><strong>Status:</strong> {'✅ Benar' if detail.get('is_correct') else '❌ Salah'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback berdasarkan persentase
    if result.get('percentage') >= 80:
        st.success("🎉 Excellent! Pemahaman Anda sangat baik tentang materi ini.")
    elif result.get('percentage') >= 60:
        st.warning("👍 Good! Pemahaman Anda cukup baik, namun masih perlu diperdalam.")
    else:
        st.error("💡 Perlu belajar lagi. Silakan pelajari kembali materi modul ini.")

def show_quiz_results_detail(quiz, user_attempts):
    """Menampilkan detail hasil kuis"""
    st.subheader(f"📊 Riwayat Attempt Kuis: {quiz.get('title')}")
    
    for attempt in user_attempts:
        with st.expander(f"Attempt {attempt.get('attempt_number')} - {attempt.get('percentage')}% - {attempt.get('submitted_at')[:16]}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Skor:** {attempt.get('score')}/{attempt.get('total_questions')}")
            with col2:
                st.write(f"**Persentase:** {attempt.get('percentage')}%")
            with col3:
                st.write(f"**Waktu:** {attempt.get('submitted_at')[:16]}")
            
            # Tampilkan jawaban untuk attempt ini
            if st.button(f"Lihat Detail Jawaban Attempt {attempt.get('attempt_number')}", 
                        key=f"detail_{attempt.get('id')}"):
                show_attempt_details(quiz, attempt)

def show_attempt_details(quiz, attempt):
    """Menampilkan detail jawaban untuk attempt tertentu"""
    questions = quiz.get("questions", [])
    user_answers = attempt.get("answers", {})
    
    st.subheader(f"📝 Detail Jawaban - Attempt {attempt.get('attempt_number')}")
    
    for i, question in enumerate(questions):
        user_answer = user_answers.get(f"q_{i}")
        correct_answer = question.get("correct_answer")
        is_correct = user_answer == correct_answer
        
        question_class = "correct-answer" if is_correct else "wrong-answer"
        
        st.markdown(f"""
        <div class='question-card {question_class}'>
            <h4>Soal {i+1}: {question.get('question')}</h4>
            <p><strong>Jawaban Anda:</strong> {user_answer}</p>
            <p><strong>Jawaban Benar:</strong> {correct_answer}</p>
            <p><strong>Status:</strong> {'✅ Benar' if is_correct else '❌ Salah'}</p>
        </div>
        """, unsafe_allow_html=True)

# ===================== Manage Quizzes (Admin) ===================== #
def show_manage_quizzes():
    """Halaman untuk mengelola kuis (admin)"""
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📝 Kelola Kuis</h1>
        <p>Buat dan kelola kuis untuk setiap modul pembelajaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    courses = load_data(COURSES_FILE)
    if not courses:
        st.warning("Belum ada kursus yang tersedia.")
        return
    
    course = courses[0]  # Ambil course pertama
    course_id = course.get("id")
    
    tab1, tab2, tab3 = st.tabs(["➕ Buat Kuis Baru", "📋 Daftar Kuis", "📊 Lihat Hasil Kuis"])
    
    with tab1:
        show_create_quiz_form(course_id)
    
    with tab2:
        show_quizzes_list(course_id)
    
    with tab3:
        show_quiz_results_admin(course_id)

def show_create_quiz_form(course_id):
    """Form untuk membuat kuis baru"""
    st.subheader("➕ Buat Kuis Baru")
    
    module_id = st.selectbox("Pilih Modul", range(1, 8), format_func=lambda x: f"Modul {x}")
    quiz_type = st.selectbox("Tipe Kuis", ["pre-test", "post-test", "formative", "summative"])
    title = st.text_input("Judul Kuis")
    description = st.text_area("Deskripsi Kuis")
    max_attempts = st.number_input("Maksimal Attempt", min_value=1, max_value=10, value=1)
    time_limit = st.number_input("Batas Waktu (menit, opsional)", min_value=0, value=0)
    
    st.subheader("📝 Soal-soal Kuis")
    
    questions = []
    
    # Input untuk beberapa soal
    num_questions = st.number_input("Jumlah Soal", min_value=1, max_value=20, value=5)
    
    for i in range(num_questions):
        st.markdown(f"### Soal {i+1}")
        
        question_text = st.text_input(f"Pertanyaan {i+1}", key=f"q_{i}_text")
        
        # Input untuk opsi jawaban
        num_options = st.number_input(f"Jumlah Opsi Jawaban {i+1}", min_value=2, max_value=5, value=4, key=f"q_{i}_options")
        
        options = []
        for j in range(num_options):
            option = st.text_input(f"Opsi {j+1}", key=f"q_{i}_opt_{j}")
            if option:
                options.append(option)
        
        # Pilih jawaban benar
        if options:
            correct_answer = st.selectbox(f"Jawaban Benar untuk Soal {i+1}", options, key=f"q_{i}_correct")
        else:
            correct_answer = None
            st.warning("Harap isi semua opsi jawaban")
        
        if question_text and options and correct_answer:
            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer
            })
        
        st.markdown("---")
    
    if st.button("💾 Buat Kuis", use_container_width=True):
        if not title or not description:
            st.error("Judul dan deskripsi kuis harus diisi!")
            return
        
        if len(questions) == 0:
            st.error("Harap tambahkan setidaknya satu soal!")
            return
        
        quiz = create_quiz(course_id, module_id, title, description, questions, quiz_type, 
                          time_limit if time_limit > 0 else None, max_attempts)
        
        st.success(f"✅ Kuis '{title}' berhasil dibuat!")
        st.balloons()

def show_quizzes_list(course_id):
    """Menampilkan daftar kuis"""
    st.subheader("📋 Daftar Kuis")
    
    quizzes = get_quizzes(course_id)
    
    if not quizzes:
        st.info("Belum ada kuis untuk kursus ini.")
        return
    
    for quiz in quizzes:
        with st.expander(f"🧠 Modul {quiz.get('module_id')}: {quiz.get('title')} ({quiz.get('quiz_type')})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Deskripsi:** {quiz.get('description')}")
                st.write(f"**Jumlah Soal:** {len(quiz.get('questions', []))}")
                st.write(f"**Batas Attempt:** {quiz.get('max_attempts', 1)}")
                
                if quiz.get('time_limit'):
                    st.write(f"**Batas Waktu:** {quiz.get('time_limit')} menit")
                
                # Statistik kuis
                results = get_quiz_results(quiz.get("id"))
                if results:
                    avg_score = sum(r.get("percentage", 0) for r in results) / len(results)
                    st.write(f"**Rata-rata Nilai:** {avg_score:.1f}%")
                    st.write(f"**Total Attempt:** {len(results)}")
            
            with col2:
                if st.button("🗑️ Hapus", key=f"delete_quiz_{quiz.get('id')}"):
                    quizzes_data = load_data(QUIZZES_FILE)
                    for i, q in enumerate(quizzes_data):
                        if q.get("id") == quiz.get("id"):
                            quizzes_data[i]["is_active"] = False
                            break
                    save_data(quizzes_data, QUIZZES_FILE)
                    st.success("✅ Kuis berhasil dihapus!")
                    st.rerun()
                
                if st.button("✏️ Edit", key=f"edit_quiz_{quiz.get('id')}"):
                    st.info("Fitur edit kuis akan segera tersedia.")

def show_quiz_results_admin(course_id):
    """Menampilkan hasil kuis untuk admin"""
    st.subheader("📊 Hasil Kuis Siswa")
    
    quizzes = get_quizzes(course_id)
    users = load_data(USERS_FILE)
    students = [u for u in users if u.get("role") == "student"]
    
    if not quizzes:
        st.info("Belum ada kuis untuk kursus ini.")
        return
    
    selected_quiz = st.selectbox(
        "Pilih Kuis",
        quizzes,
        format_func=lambda q: f"Modul {q.get('module_id')}: {q.get('title')} ({q.get('quiz_type')})"
    )
    
    if selected_quiz:
        results = get_quiz_results(selected_quiz.get("id"))
        
        if not results:
            st.info("Belum ada hasil kuis untuk kuis ini.")
            return
        
        # Statistik umum
        st.subheader("📈 Statistik Kuis")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_score = sum(r.get("percentage", 0) for r in results) / len(results)
            st.metric("Rata-rata Nilai", f"{avg_score:.1f}%")
        with col2:
            max_score = max(r.get("percentage", 0) for r in results)
            st.metric("Nilai Tertinggi", f"{max_score}%")
        with col3:
            min_score = min(r.get("percentage", 0) for r in results)
            st.metric("Nilai Terendah", f"{min_score}%")
        with col4:
            st.metric("Total Attempt", len(results))
        
        # Tabel hasil
        st.subheader("📋 Detail Hasil per Siswa")
        
        for result in results:
            student = next((s for s in students if s.get("id") == result.get("user_id")), None)
            if student:
                with st.expander(f"🎓 {student.get('name')} - Attempt {result.get('attempt_number')} - {result.get('percentage')}%"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nama:** {student.get('name')}")
                        st.write(f"**Username:** {student.get('username')}")
                        st.write(f"**Skor:** {result.get('score')}/{result.get('total_questions')}")
                    with col2:
                        st.write(f"**Persentase:** {result.get('percentage')}%")
                        st.write(f"**Attempt:** {result.get('attempt_number')}")
                        st.write(f"**Waktu Submit:** {result.get('submitted_at')[:16]}")
                    
                    if st.button(f"Lihat Detail Jawaban", key=f"view_{result.get('id')}"):
                        show_attempt_details_admin(selected_quiz, result, student)

def show_attempt_details_admin(quiz, result, student):
    """Menampilkan detail jawaban untuk admin"""
    questions = quiz.get("questions", [])
    user_answers = result.get("answers", {})
    
    st.subheader(f"📝 Detail Jawaban - {student.get('name')}")
    
    for i, question in enumerate(questions):
        user_answer = user_answers.get(f"q_{i}")
        correct_answer = question.get("correct_answer")
        is_correct = user_answer == correct_answer
        
        question_class = "correct-answer" if is_correct else "wrong-answer"
        
        st.markdown(f"""
        <div class='question-card {question_class}'>
            <h4>Soal {i+1}: {question.get('question')}</h4>
            <p><strong>Jawaban Siswa:</strong> {user_answer}</p>
            <p><strong>Jawaban Benar:</strong> {correct_answer}</p>
            <p><strong>Status:</strong> {'✅ Benar' if is_correct else '❌ Salah'}</p>
        </div>
        """, unsafe_allow_html=True)

# ===================== Assignment System ===================== #
def create_assignment(course_id, module_id, title, description, due_date, max_points=100, file_types=None):
    """Membuat tugas baru"""
    assignments = load_data(ASSIGNMENTS_FILE)
    
    new_assignment = {
        "id": len(assignments) + 1,
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
    save_data(assignments, ASSIGNMENTS_FILE)
    
    # Notifikasi untuk siswa yang terdaftar
    users = load_data(USERS_FILE)
    enrolled_students = [u for u in users if u.get("role") == "student" and course_id in u.get("enrolled_courses", [])]
    
    for student in enrolled_students:
        create_notification(
            student.get("id"),
            "📝 Tugas Baru",
            f"Tugas baru: {title} untuk Modul {module_id}. Deadline: {due_date}",
            "info",
            course_id,
            module_id
        )
    
    return new_assignment

def delete_assignment(assignment_id):
    """Menghapus tugas"""
    assignments = load_data(ASSIGNMENTS_FILE)
    assignment = next((a for a in assignments if a.get("id") == assignment_id), None)
    
    if assignment:
        # Nonaktifkan tugas daripada menghapus permanen
        assignment["is_active"] = False
        save_data(assignments, ASSIGNMENTS_FILE)
        
        # Hapus semua submission untuk tugas ini
        submissions = load_data(SUBMISSIONS_FILE)
        submissions = [s for s in submissions if s.get("assignment_id") != assignment_id]
        save_data(submissions, SUBMISSIONS_FILE)
        
        return True
    return False

def get_assignments(course_id, module_id=None):
    """Mendapatkan daftar tugas"""
    assignments = load_data(ASSIGNMENTS_FILE)
    if module_id:
        return [a for a in assignments if a.get("course_id") == course_id and a.get("module_id") == module_id and a.get("is_active")]
    else:
        return [a for a in assignments if a.get("course_id") == course_id and a.get("is_active")]

def get_assignment_by_id(assignment_id):
    """Mendapatkan tugas berdasarkan ID"""
    assignments = load_data(ASSIGNMENTS_FILE)
    return next((a for a in assignments if a.get("id") == assignment_id), None)

def submit_assignment(assignment_id, user_id, file_data, file_name, file_type, notes=""):
    """Mengumpulkan tugas - VERSION IMPROVED"""
    submissions = load_data(SUBMISSIONS_FILE)
    
    # Pastikan tipe data konsisten
    assignment_id = int(assignment_id) if not isinstance(assignment_id, int) else assignment_id
    user_id = int(user_id) if not isinstance(user_id, int) else user_id
    
    # Cari submission yang sudah ada
    existing_index = None
    for i, sub in enumerate(submissions):
        sub_assignment_id = sub.get("assignment_id")
        sub_user_id = sub.get("user_id")
        
        # Normalize types untuk comparison
        if isinstance(sub_assignment_id, str):
            try:
                sub_assignment_id = int(sub_assignment_id)
            except:
                pass
                
        if isinstance(sub_user_id, str):
            try:
                sub_user_id = int(sub_user_id)
            except:
                pass
        
        if sub_assignment_id == assignment_id and sub_user_id == user_id:
            existing_index = i
            break
    
    # Prepare file data
    if isinstance(file_data, bytes):
        file_data_encoded = base64.b64encode(file_data).decode('utf-8')
    else:
        file_data_encoded = file_data
    
    # Prepare submission data
    submission_data = {
        "file_data": file_data_encoded,
        "file_name": file_name,
        "file_type": file_type,
        "file_size": len(file_data) if isinstance(file_data, bytes) else len(file_data_encoded),
        "notes": notes,
        "submission_text": notes,
        "submitted_at": datetime.now().isoformat(),
        "status": "submitted",
        "is_graded": False,
        "grade": None,
        "feedback": None,
        "graded_at": None,
        "graded_by": None
    }
    
    if existing_index is not None:
        # Update existing submission
        submissions[existing_index].update(submission_data)
        st.info("🔄 Memperbarui submission yang sudah ada...")
    else:
        # Create new submission
        new_submission = {
            "id": len(submissions) + 1,
            "assignment_id": assignment_id,
            "user_id": user_id
        }
        new_submission.update(submission_data)
        submissions.append(new_submission)
        st.info("🆕 Membuat submission baru...")
    
    # Save data dengan error handling
    try:
        save_data(submissions, SUBMISSIONS_FILE)
        st.success("💾 Data berhasil disimpan!")
        
        # Notification
        users = load_data(USERS_FILE)
        student = next((u for u in users if u.get("id") == user_id), None)
        assignment = get_assignment_by_id(assignment_id)
        
        if student and assignment:
            admins = [u for u in users if u.get("role") == "admin"]
            for admin in admins:
                create_notification(
                    admin.get("id"),
                    "📤 Tugas Dikumpulkan",
                    f"{student.get('name')} mengumpulkan tugas: {assignment.get('title')}",
                    "info",
                    assignment.get("course_id"),
                    assignment.get("module_id")
                )
        
        return True
        
    except Exception as e:
        st.error(f"❌ Gagal menyimpan data: {str(e)}")
        return False

def get_submission(assignment_id, user_id):
    """Mendapatkan submission user untuk tugas tertentu - SIMPLIFIED"""
    submissions = load_data(SUBMISSIONS_FILE)
    
    # Debug info
    print(f"DEBUG get_submission: assignment_id={assignment_id}, user_id={user_id}")
    print(f"DEBUG: Total submissions: {len(submissions)}")
    
    for submission in submissions:
        sub_assignment_id = submission.get("assignment_id")
        sub_user_id = submission.get("user_id")
        
        print(f"DEBUG: Checking submission - assignment_id={sub_assignment_id}, user_id={sub_user_id}")
        
        # Simple comparison - biarkan Python handle type conversion
        if sub_assignment_id == assignment_id and sub_user_id == user_id:
            print(f"DEBUG: MATCH FOUND!")
            return submission
    
    print(f"DEBUG: NO MATCH FOUND")
    return None

def get_all_submissions(assignment_id=None, course_id=None):
    """Mendapatkan semua submission (untuk admin)"""
    submissions = load_data(SUBMISSIONS_FILE)
    
    if assignment_id:
        submissions = [s for s in submissions if s.get("assignment_id") == assignment_id]
    
    if course_id:
        assignments = load_data(ASSIGNMENTS_FILE)
        course_assignments = [a.get("id") for a in assignments if a.get("course_id") == course_id]
        submissions = [s for s in submissions if s.get("assignment_id") in course_assignments]
    
    return submissions

def grade_submission(submission_id, score, feedback, graded_by):
    """Memberi nilai pada submission"""
    submissions = load_data(SUBMISSIONS_FILE)
    
    for submission in submissions:
        if submission.get("id") == submission_id:
            submission.update({
                "score": score,
                "feedback": feedback,
                "graded_at": datetime.now().isoformat(),
                "graded_by": graded_by,
                "status": "graded"
            })
            break
    
    save_data(submissions, SUBMISSIONS_FILE)
    
    # Notifikasi untuk siswa
    submission = next((s for s in submissions if s.get("id") == submission_id), None)
    if submission:
        assignment = get_assignment_by_id(submission.get("assignment_id"))
        create_notification(
            submission.get("user_id"),
            "📊 Nilai Tugas",
            f"Tugas '{assignment.get('title')}' telah dinilai. Nilai: {score}",
            "success" if score >= 70 else "warning",
            assignment.get("course_id") if assignment else None,
            assignment.get("module_id") if assignment else None
        )
    
    return True

def get_file_extension(file_name):
    """Mendapatkan ekstensi file"""
    return os.path.splitext(file_name)[1].lower()

def is_file_type_allowed(file_name, allowed_types):
    """Cek apakah tipe file diizinkan"""
    file_ext = get_file_extension(file_name)
    return file_ext in allowed_types

# ===================== Notifikasi System ===================== #
def create_notification(user_id, title, message, notification_type="info", course_id=None, module_id=None):
    """Membuat notifikasi baru"""
    notifications = load_data(NOTIFICATIONS_FILE)
    
    new_notification = {
        "id": len(notifications) + 1,
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
    save_data(notifications, NOTIFICATIONS_FILE)
    return new_notification

def get_user_notifications(user_id, unread_only=False):
    """Mendapatkan notifikasi user"""
    notifications = load_data(NOTIFICATIONS_FILE)
    user_notifications = [n for n in notifications if n.get("user_id") == user_id]
    
    if unread_only:
        user_notifications = [n for n in user_notifications if not n.get("is_read")]
    
    user_notifications.sort(key=lambda x: x.get("created_at"), reverse=True)
    return user_notifications

def get_unread_notification_count(user_id):
    """Mendapatkan jumlah notifikasi yang belum dibaca"""
    notifications = get_user_notifications(user_id, unread_only=True)
    return len(notifications)

def mark_notification_as_read(notification_id):
    """Menandai notifikasi sebagai sudah dibaca"""
    notifications = load_data(NOTIFICATIONS_FILE)
    for notification in notifications:
        if notification.get("id") == notification_id:
            notification["is_read"] = True
            notification["read_at"] = datetime.now().isoformat()
            break
    save_data(notifications, NOTIFICATIONS_FILE)

def mark_all_notifications_as_read(user_id):
    """Menandai semua notifikasi user sebagai sudah dibaca"""
    notifications = load_data(NOTIFICATIONS_FILE)
    for notification in notifications:
        if notification.get("user_id") == user_id and not notification.get("is_read"):
            notification["is_read"] = True
            notification["read_at"] = datetime.now().isoformat()
    save_data(notifications, NOTIFICATIONS_FILE)

def send_bulk_notification(user_ids, title, message, notification_type="info", course_id=None):
    """Mengirim notifikasi ke banyak user sekaligus"""
    for user_id in user_ids:
        create_notification(user_id, title, message, notification_type, course_id)

# ===================== Auth & Registration ===================== #
def authenticate(username, password):
    users = load_data(USERS_FILE)
    for u in users:
        if u.get("username") == username and u.get("password") == password:
            return u
    return None

def register_student(name, username, password, email):
    """Registrasi siswa baru"""
    users = load_data(USERS_FILE)
    if any(u.get("username") == username for u in users):
        return False
    
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "role": "student",
        "registered_at": datetime.now().isoformat(),
        "enrolled_courses": []
    }
    users.append(new_user)
    save_data(users, USERS_FILE)
    return True

# ===================== Course Management ===================== #
def get_course_code(course_id=1):
    course_codes = load_data(COURSE_CODES_FILE)
    for cc in course_codes:
        if cc.get("course_id") == course_id and cc.get("is_active") == True:
            return cc.get("code")
    return None

def validate_course_code(course_code, course_id=1):
    course_codes = load_data(COURSE_CODES_FILE)
    for cc in course_codes:
        if (cc.get("code") == course_code and 
            cc.get("course_id") == course_id and 
            cc.get("is_active") == True):
            return True, cc
    return False, None

def enroll_user_in_course(user_id, course_id, course_code):
    is_valid, code_data = validate_course_code(course_code, course_id)
    if not is_valid:
        return False, "❌ Kode akses tidak valid atau sudah tidak aktif."
    
    users = load_data(USERS_FILE)
    for user in users:
        if user.get("id") == user_id:
            if "enrolled_courses" not in user:
                user["enrolled_courses"] = []
            if course_id not in user["enrolled_courses"]:
                user["enrolled_courses"].append(course_id)
            break
    save_data(users, USERS_FILE)
    
    progress = load_data(PROGRESS_FILE)
    existing_progress = next((p for p in progress if p.get("user_id") == user_id and p.get("course_id") == course_id), None)
    if not existing_progress:
        new_prog = {
            "user_id": user_id,
            "course_id": course_id,
            "progress": 0,
            "completed_modules": [],
            "enrolled_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        progress.append(new_prog)
        save_data(progress, PROGRESS_FILE)
    
    course = next((c for c in load_data(COURSES_FILE) if c.get("id") == course_id), None)
    if course:
        create_notification(
            user_id,
            "🎉 Berhasil Bergabung dengan Kursus",
            f"Anda telah berhasil bergabung dengan kursus '{course.get('title')}'. Selamat belajar!",
            "success",
            course_id
        )
    
    return True, "✅ Berhasil bergabung ke kursus!"

# ===================== Attendance System ===================== #
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
    
    create_notification(
        user_id,
        "✅ Absensi Terekam",
        f"Absensi Anda untuk hari ini telah tercatat: {status}",
        "success",
        course_id
    )
    return True

def get_attendance(course_id, date_str=None):
    attendance = load_data(ATTENDANCE_FILE)
    if date_str is None:
        date_str = date.today().isoformat()
    return [a for a in attendance if a.get("course_id") == course_id and a.get("date") == date_str]

# ===================== Forum System ===================== #
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

# ===================== UI Components ===================== #
def create_hero_section():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='main-header electric-pulse'>
            <h1>⚡ LMS Fisika - Hukum Kirchhoff</h1>
            <h3>Listrik Dinamis | Kurikulum Merdeka | Pembelajaran Interaktif</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='custom-card'>
            <h4>🎯 Tujuan Pembelajaran</h4>
            <p>Memahami konsep Hukum Kirchhoff tentang arus dan tegangan dalam rangkaian listrik 
            melalui pembelajaran berbasis inkuiri dan eksperimen virtual.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='electric-card' style='text-align: center;'>
            <h3>🔬 Fitur Unggulan</h3>
            <p>✓ Laboratorium Virtual</p>
            <p>✓ Simulasi Interaktif</p>
            <p>✓ Assessment Berbasis Projek</p>
            <p>✓ Forum Diskusi</p>
            <p>✓ Kuis & Evaluasi</p>
        </div>
        """, unsafe_allow_html=True)

def create_metric_card(title, value, icon="📊", subtitle=""):
    st.markdown(f"""
    <div class='metric-card'>
        <h3>{icon} {value}</h3>
        <h4>{title}</h4>
        <small>{subtitle}</small>
    </div>
    """, unsafe_allow_html=True)

def create_module_card(module_number, title, status, progress=0):
    status_icon = "✅" if status == "completed" else "📚" if status == "in-progress" else "🔒"
    status_color = "#2ecc71" if status == "completed" else "#3498db" if status == "in-progress" else "#95a5a6"
    
    st.markdown(f"""
    <div class='custom-card' style='border-left-color: {status_color}'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h4>{status_icon} Modul {module_number}: {title}</h4>
                <p>Status: <strong>{status.replace('-', ' ').title()}</strong></p>
            </div>
            <div style='text-align: right;'>
                <div style='background: {status_color}; color: white; padding: 5px 10px; border-radius: 15px;'>
                    {progress}%
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== Welcome Page ===================== #
def show_welcome():
    inject_custom_css()
    create_hero_section()
    st.markdown("---")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3>📹 Pengenalan Hukum Kirchhoff</h3>
            <p>Pelajari konsep dasar Hukum Kirchhoff melalui video pembelajaran interaktif.</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            st.video("https://youtu.be/ALeDH_6qn5M")
        except Exception:
            st.markdown("""
            <div style='background: #e0e0e0; padding: 100px; text-align: center; border-radius: 10px;'>
                <h4>🎥 Video Pengenalan</h4>
                <p>Link video: https://youtu.be/ALeDH_6qn5M</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='circuit-card'>
            <h3>🎯 Capaian Pembelajaran</h3>
            <p>✓ Memahami Hukum Kirchhoff 1 (KCL)</p>
            <p>✓ Memahami Hukum Kirchhoff 2 (KVL)</p>
            <p>✓ Menganalisis rangkaian listrik</p>
            <p>✓ Menyelesaikan masalah rangkaian kompleks</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='custom-card'>
            <h3>📚 Kurikulum Merdeka</h3>
            <p>Pembelajaran sesuai dengan kurikulum merdeka yang berfokus pada:</p>
            <p>• Pembelajaran berdiferensiasi</p>
            <p>• Projek penguatan profil</p>
            <p>• Assessment autentik</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='custom-card' style='text-align: center; background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);'>
        <h3>🚀 Mulai Belajar Sekarang!</h3>
        <p>Silakan login untuk mengakses materi pembelajaran lengkap atau registrasi sebagai siswa baru.</p>
        <p><strong>Gunakan sidebar di sebelah kiri untuk login/registrasi</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ===================== Dashboard ===================== #
def show_dashboard():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📊 Dashboard Pembelajaran</h1>
        <p>Monitor progress belajar dan aktivitas terkini</p>
    </div>
    """, unsafe_allow_html=True)
    
    courses = load_data(COURSES_FILE)
    users = load_data(USERS_FILE)
    students = [u for u in users if u.get("role") == "student"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Jumlah Course", len(courses), "📚", "Materi Pembelajaran")
    with col2:
        create_metric_card("Jumlah Siswa", len(students), "👥", "Siswa Terdaftar")
    with col3:
        current_code = get_course_code(1)
        create_metric_card("Kode Akses", current_code if current_code else "-", "🔑", "Aktif")
    with col4:
        if st.session_state.authenticated:
            user_id = st.session_state.current_user.get("id")
            unread_count = get_unread_notification_count(user_id)
            create_metric_card("Notifikasi", unread_count, "🔔", "Belum dibaca")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.authenticated:
            show_learning_progress()
    
    with col2:
        if st.session_state.authenticated:
            show_notifications_preview()

def show_learning_progress():
    st.markdown("""
    <div class='custom-card'>
        <h3>📈 Progress Pembelajaran</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        user_id = st.session_state.current_user.get("id")
        progress_data = load_data(PROGRESS_FILE)
        user_prog = next((p for p in progress_data if p.get("user_id") == user_id), None)
        
        if user_prog:
            progress_value = user_prog.get("progress", 0)
            completed_modules = len(user_prog.get("completed_modules", []))
            
            st.progress(progress_value / 100)
            st.write(f"**{progress_value}% Selesai** | {completed_modules}/7 Modul")
            
            if completed_modules > 0:
                st.markdown("**Modul yang sudah diselesaikan:**")
                for mod_id in user_prog.get("completed_modules", []):
                    st.markdown(f"✅ Modul {mod_id}")
        else:
            st.info("Belum ada progress pembelajaran. Mulai belajar dari menu 'Materi Pembelajaran'.")

def show_notifications_preview():
    st.markdown("""
    <div class='custom-card'>
        <h3>🔔 Notifikasi Terbaru</h3>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.current_user.get("id")
    notifications = get_user_notifications(user_id, unread_only=False)[:5]
    
    if not notifications:
        st.info("Belum ada notifikasi.")
        return
    
    for notification in notifications:
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        icon = icons.get(notification.get("type"), "📢")
        
        col1, col2 = st.columns([8, 2])
        with col1:
            if not notification.get("is_read"):
                st.markdown(f"**{icon} {notification.get('title')}**")
            else:
                st.write(f"{icon} {notification.get('title')}")
            st.caption(notification.get("message"))
            st.caption(f"_{notification.get('created_at')[:16]}_")
        with col2:
            if not notification.get("is_read"):
                if st.button("Tandai Dibaca", key=f"read_{notification.get('id')}"):
                    mark_notification_as_read(notification.get('id'))
                    st.rerun()

# ===================== Course Access UI ===================== #
def show_course_access_ui():
    st.markdown("""
    <div class='main-header'>
        <h1>🔐 Akses Kursus</h1>
        <p>Masukkan kode akses untuk mulai belajar</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='custom-card'>
        <h4>📝 Informasi Akses</h4>
        <p>Untuk mengakses materi pembelajaran Hukum Kirchhoff, Anda perlu memasukkan kode akses yang diberikan oleh pengajar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    course_code = st.text_input("Masukkan Kode Akses Kursus:", placeholder="Contoh: A1B2C3D4")
    
    if st.button("🚀 Akses Kursus", use_container_width=True):
        if course_code.strip():
            success, message = enroll_user_in_course(
                st.session_state.current_user.get("id"), 
                1,
                course_code.strip()
            )
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        else:
            st.error("Harap masukkan kode akses.")

# ===================== Modul Helper ===================== #
def get_module_by_id(modules, mid):
    for m in modules:
        if m.get("id") == mid:
            return m
    return None

def render_module_content_enhanced(m, course_id, module_id):
    if not m:
        st.info("📝 Modul sedang dalam pengembangan...")
        return
        
    st.markdown(f"### 📚 {m.get('title','')}")
    
    # Tampilkan media ajar yang terkait dengan modul
    media_list = get_media_by_module(course_id, module_id)
    if media_list:
        st.markdown("""
        <div class='custom-card'>
            <h4>📁 Media Pembelajaran</h4>
            <p>Berikut adalah bahan ajar yang tersedia untuk modul ini:</p>
        </div>
        """, unsafe_allow_html=True)
        
        for media in media_list:
            with st.expander(f"{get_file_icon(media.get('file_type'))} {media.get('file_name')} - {media.get('media_type').replace('_', ' ').title()}"):
                display_media_content(media)
    
    if m.get("content"):
        st.markdown("""
        <div class='custom-card'>
            <h4>📖 Materi Pembelajaran</h4>
        </div>
        """, unsafe_allow_html=True)
        st.write(m.get("content"))
    
    if m.get("video_url"):
        st.markdown("""
        <div class='custom-card'>
            <h4>🎥 Video Pembelajaran</h4>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.video(m.get("video_url"))
        except Exception:
            st.markdown(f"[📹 Tonton Video Pembelajaran]({m.get('video_url')})")
    
    # Tampilkan kuis untuk modul ini
    show_quiz_ui(1, m.get("id"))  # course_id 1

# ===================== Forum UI ===================== #
def module_forum_ui(course_id, module_id):
    user = st.session_state.current_user
    threads = get_forum_threads(course_id, module_id)
    
    st.markdown("""
    <div class='custom-card'>
        <h4>💬 Diskusi</h4>
    </div>
    """, unsafe_allow_html=True)
    
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

# ===================== My Courses ===================== #
def show_my_courses():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📚 Materi Pembelajaran</h1>
        <p>Hukum Kirchhoff - Listrik Dinamis | Kurikulum Merdeka</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cek jika sedang mengerjakan kuis
    if hasattr(st.session_state, 'quiz_started') and st.session_state.quiz_started:
        show_quiz_interface()
        return
    
    courses = load_data(COURSES_FILE)
    uid = st.session_state.current_user.get("id")
    
    users = load_data(USERS_FILE)
    current_user = next((u for u in users if u.get("id") == uid), None)
    
    if not current_user or "enrolled_courses" not in current_user or not current_user["enrolled_courses"]:
        show_course_access_ui()
        return
    
    progress = load_data(PROGRESS_FILE)
    user_prog = next((p for p in progress if p.get("user_id") == uid), None)
    
    if not user_prog:
        st.markdown("""
        <div class='electric-card'>
            <h3>🎯 Pilih Kursus untuk Mulai Belajar</h3>
            <p>Pilih salah satu kursus di bawah ini untuk memulai perjalanan belajar Anda</p>
        </div>
        """, unsafe_allow_html=True)
        
        for course_id in current_user["enrolled_courses"]:
            course = next((c for c in courses if c.get("id") == course_id), None)
            if course:
                st.markdown(f"""
                <div class='custom-card'>
                    <h4>⚡ {course.get('title','Untitled')}</h4>
                    <p>{course.get('description','')}</p>
                    <p><strong>Level:</strong> {course.get('level','')} | <strong>Kategori:</strong> {course.get('category','')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 Mulai Belajar", key=f"start_{course.get('id')}"):
                    new_prog = {
                        "user_id": uid,
                        "course_id": course.get("id"),
                        "progress": 0,
                        "completed_modules": [],
                        "last_accessed": datetime.now().isoformat()
                    }
                    progress.append(new_prog)
                    save_data(progress, PROGRESS_FILE)
                    
                    create_notification(
                        uid,
                        "🚀 Mulai Belajar",
                        f"Anda memulai kursus '{course.get('title')}'. Semangat belajar!",
                        "info",
                        course.get("id")
                    )
                    st.rerun()
    else:
        course = next((c for c in courses if c.get("id") == user_prog.get("course_id")), None)
        if course:
            show_course_detail_enhanced(course, user_prog)
        else:
            st.error("Kursus tidak ditemukan.")

def show_course_detail_enhanced(course, user_prog=None):
    st.markdown(f"""
    <div class='electric-card'>
        <h2>⚡ {course.get('title')}</h2>
        <p>{course.get('description')}</p>
        <div style='display: flex; gap: 20px; margin-top: 15px;'>
            <div><strong>👨‍🏫 Pengajar:</strong> {course.get('instructor')}</div>
            <div><strong>📊 Level:</strong> {course.get('level')}</div>
            <div><strong>📁 Kategori:</strong> {course.get('category')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if user_prog:
        progress_value = user_prog.get("progress", 0)
        st.markdown(f"""
        <div class='custom-card'>
            <h4>📊 Progress Belajar</h4>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_value / 100)
        st.write(f"**{progress_value}% selesai** | {len(user_prog.get('completed_modules', []))}/7 modul terselesaikan")
    
    if st.session_state.current_user.get("role") == "student":
        st.markdown("""
        <div class='custom-card'>
            <h4>📋 Absensi Harian</h4>
        </div>
        """, unsafe_allow_html=True)
        
        today = date.today().isoformat()
        att = get_attendance(course.get("id"), today)
        my_att = next((a for a in att if a.get("user_id") == st.session_state.current_user.get("id")), None)
        
        if my_att:
            st.success(f"✅ Anda sudah menandai kehadiran hari ini ({my_att.get('status')})")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Hadir", use_container_width=True):
                    mark_attendance(st.session_state.current_user.get("id"), course.get("id"), "Hadir")
                    st.rerun()
            with col2:
                if st.button("⚠️ Izin", use_container_width=True):
                    mark_attendance(st.session_state.current_user.get("id"), course.get("id"), "Izin")
                    st.rerun()
            with col3:
                if st.button("❌ Sakit", use_container_width=True):
                    mark_attendance(st.session_state.current_user.get("id"), course.get("id"), "Sakit")
                    st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class='main-header'>
        <h3>📘 Modul Pembelajaran</h3>
        <p>Pelajari materi secara bertahap melalui modul-modul berikut</p>
    </div>
    """, unsafe_allow_html=True)
    
    modules = course.get("modules", [])
    progress_data = load_data(PROGRESS_FILE)
    
    # Buat modul default jika belum ada
    if not modules:
        modules = [
            {"id": 1, "title": "Pengenalan Hukum Kirchhoff", "content": "Materi pengenalan tentang Hukum Kirchhoff..."},
            {"id": 2, "title": "Hukum Kirchhoff 1 (KCL)", "content": "Materi tentang Hukum Kirchhoff 1..."},
            {"id": 3, "title": "Hukum Kirchhoff 2 (KVL)", "content": "Materi tentang Hukum Kirchhoff 2..."},
            {"id": 4, "title": "Rangkaian Seri", "content": "Analisis rangkaian seri..."},
            {"id": 5, "title": "Rangkaian Paralel", "content": "Analisis rangkaian paralel..."},
            {"id": 6, "title": "Rangkaian Kompleks", "content": "Analisis rangkaian kompleks..."},
            {"id": 7, "title": "Aplikasi dalam Kehidupan", "content": "Aplikasi Hukum Kirchhoff..."}
        ]
        course["modules"] = modules
        courses = load_data(COURSES_FILE)
        for i, c in enumerate(courses):
            if c.get("id") == course.get("id"):
                courses[i] = course
        save_data(courses, COURSES_FILE)
    
    for mid in range(1, 8):
        m = get_module_by_id(modules, mid)
        module_title = m.get('title') if m else f'Modul {mid} - Listrik Dinamis'
        status = "completed" if user_prog and mid in user_prog.get("completed_modules", []) else "in-progress" if m else "locked"
        
        create_module_card(mid, module_title, status, 
                          progress=100 if status == "completed" else 50 if status == "in-progress" else 0)
        
        if m:
            with st.expander(f"📖 Buka Modul {mid}", expanded=False):
                render_module_content_enhanced(m, course.get("id"), mid)
                
                # Tampilkan tugas untuk modul ini
                show_assignment_ui(course.get("id"), mid)
                
                if user_prog:
                    col1, col2 = st.columns(2)
                    with col1:
                        if mid in user_prog.get("completed_modules", []):
                            st.success("🎉 Modul ini sudah berhasil diselesaikan!")
                            if st.button(f"↩️ Batalkan Tandai Selesai", key=f"undo_{mid}"):
                                user_prog["completed_modules"].remove(mid)
                                user_prog["progress"] = int(len(user_prog["completed_modules"]) / 7 * 100)
                                user_prog["last_accessed"] = datetime.now().isoformat()
                                
                                for i, p in enumerate(progress_data):
                                    if p.get("user_id") == user_prog.get("user_id"):
                                        progress_data[i] = user_prog
                                save_data(progress_data, PROGRESS_FILE)
                                
                                create_notification(
                                    user_prog.get("user_id"),
                                    "🔄 Modul Dibuka Kembali",
                                    f"Anda membatalkan penyelesaian Modul {mid}: {m.get('title')}",
                                    "info",
                                    course.get("id"),
                                    mid
                                )
                                st.success("✅ Status modul berhasil dibatalkan!")
                                st.rerun()
                        else:
                            if st.button(f"✅ Tandai Modul {mid} sebagai Selesai", key=f"done_{mid}"):
                                if "completed_modules" not in user_prog:
                                    user_prog["completed_modules"] = []
                                user_prog["completed_modules"].append(mid)
                                user_prog["progress"] = int(len(user_prog["completed_modules"]) / 7 * 100)
                                user_prog["last_accessed"] = datetime.now().isoformat()
                                
                                for i, p in enumerate(progress_data):
                                    if p.get("user_id") == user_prog.get("user_id"):
                                        progress_data[i] = user_prog
                                save_data(progress_data, PROGRESS_FILE)
                                
                                create_notification(
                                    user_prog.get("user_id"),
                                    "🎯 Modul Selesai",
                                    f"Selamat! Anda telah menyelesaikan Modul {mid}: {m.get('title')}",
                                    "success",
                                    course.get("id"),
                                    mid
                                )
                                st.success("✅ Modul berhasil ditandai sebagai selesai!")
                                st.rerun()
                
                st.markdown("---")
                st.markdown("""
                <div class='custom-card'>
                    <h4>💬 Diskusi Modul</h4>
                </div>
                """, unsafe_allow_html=True)
                module_forum_ui(course.get("id"), mid)

    st.markdown("""
    <div class='main-header'>
        <h3>💬 Forum Diskusi Umum</h3>
        <p>Berdiskusi dengan peserta lain tentang materi kursus</p>
    </div>
    """, unsafe_allow_html=True)
    module_forum_ui(course.get("id"), None)

# ===================== Assignment UI ===================== #
def show_assignment_ui(course_id, module_id):
    """Menampilkan UI untuk tugas - DENGAN PERBAIKAN TOMBOL KUMPULKAN ULANG"""
    st.subheader("📝 Tugas Modul")
    
    assignments = get_assignments(course_id, module_id)
    current_user = st.session_state.current_user
    
    if not assignments:
        st.info("Belum ada tugas untuk modul ini.")
        return
    
    for assignment in assignments:
        # Inisialisasi state dengan key yang lebih unik
        form_key = f"show_form_{assignment.get('id')}_{current_user.get('id')}_{module_id}"
        detail_key = f"show_detail_{assignment.get('id')}_{current_user.get('id')}_{module_id}"
        resubmit_key = f"resubmit_{assignment.get('id')}_{current_user.get('id')}_{module_id}"
        
        # Inisialisasi state jika belum ada
        if form_key not in st.session_state:
            st.session_state[form_key] = False
        if detail_key not in st.session_state:
            st.session_state[detail_key] = False
        
        with st.expander(f"📋 {assignment.get('title')}", expanded=True):
            st.write(f"**Deskripsi:** {assignment.get('description')}")
            st.write(f"**Batas Waktu:** {assignment.get('due_date')[:10]}")
            st.write(f"**Nilai Maksimal:** {assignment.get('max_points')} poin")
            
            # Get submission untuk user yang sedang login
            submission = get_submission(assignment.get("id"), current_user.get("id"))
            
            if submission:
                # Status penilaian
                score = submission.get('grade')
                max_score = assignment.get('max_points', 100)
                
                is_graded = (
                    submission.get("status") == "graded" or 
                    submission.get("is_graded") is True or
                    score is not None
                )
                
                if is_graded and score is not None:
                    st.success("🎉 **TUGAS TELAH DINILAI**")
                    
                    try:
                        percentage = (score / max_score) * 100 if max_score and max_score > 0 else 0
                    except (TypeError, ZeroDivisionError):
                        percentage = 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "Nilai Anda", 
                            f"{score}/{max_score}",
                            f"{percentage:.1f}%"
                        )
                    with col2:
                        status_text = "Lulus" if score >= (max_score * 0.6) else "Perlu Perbaikan"
                        status_icon = "✅" if score >= (max_score * 0.6) else "⚠️"
                        st.metric("Status", f"{status_icon} {status_text}")
                    with col3:
                        graded_by = submission.get('graded_by', 'Guru')
                        st.metric("Dinilai Oleh", graded_by)
                    
                else:
                    st.success("✅ **TUGAS TELAH DIKUMPULKAN**")
                    st.info("⏳ Menunggu penilaian dari guru...")
                
                st.write(f"**Waktu Pengumpulan:** {submission.get('submitted_at')[:16]}")
                st.write(f"**File:** {submission.get('file_name')}")
                
                # Tombol aksi - PERBAIKAN LOGIC DI SINI
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Tombol lihat detail
                    if st.button("📋 Lihat Detail", 
                               key=f"view_{assignment.get('id')}_{current_user.get('id')}_{module_id}",
                               use_container_width=True):
                        st.session_state[detail_key] = True
                        st.rerun()
                
                with col2:
                    # Tombol kumpulkan ulang - SELALU TAMPILKAN
                    if st.button("🔄 Kumpulkan Ulang", 
                               key=f"resubmit_{assignment.get('id')}_{current_user.get('id')}_{module_id}",
                               use_container_width=True):
                        st.session_state[form_key] = True
                        st.rerun()
                
                # Tampilkan detail jika diminta
                if st.session_state[detail_key]:
                    show_submission_detail(assignment, submission, detail_key)
                    
            else:
                st.warning("❌ **TUGAS BELUM DIKUMPULKAN**")
                
                # Tombol kumpulkan tugas pertama kali
                if st.button("📤 Kumpulkan Tugas", 
                           key=f"submit_{assignment.get('id')}_{current_user.get('id')}_{module_id}",
                           use_container_width=True):
                    st.session_state[form_key] = True
                    st.rerun()
            
            # Tampilkan form pengumpulan jika state aktif
            if st.session_state[form_key]:
                show_submission_form(assignment, form_key, course_id, module_id)

def debug_all_users():
    """Debug semua user yang terdaftar"""
    users = load_data(USERS_FILE)
    
    st.markdown("---")
    st.subheader("👥 DEBUG ALL USERS")
    
    for user in users:
        with st.expander(f"User {user.get('id')}: {user.get('name')} ({user.get('username')})"):
            st.write(f"**ID:** {user.get('id')}")
            st.write(f"**Username:** {user.get('username')}")
            st.write(f"**Name:** {user.get('name')}")
            st.write(f"**Email:** {user.get('email')}")
            st.write(f"**Role:** {user.get('role')}")
            st.write(f"**Enrolled Courses:** {user.get('enrolled_courses', [])}")

def debug_all_submissions():
    """Debug semua data submissions"""
    submissions = load_data(SUBMISSIONS_FILE)
    
    st.markdown("---")
    st.subheader("🐛 DEBUG ALL SUBMISSIONS")
    st.write(f"Total submissions dalam database: {len(submissions)}")
    
    if not submissions:
        st.info("Tidak ada data submissions")
        return
    
    for i, sub in enumerate(submissions):
        with st.expander(f"Submission {i+1} - ID: {sub.get('id')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Data:**")
                st.write(f"assignment_id: `{sub.get('assignment_id')}`")
                st.write(f"user_id: `{sub.get('user_id')}`")
                st.write(f"file_name: `{sub.get('file_name')}`")
                st.write(f"status: `{sub.get('status')}`")
                st.write(f"is_graded: `{sub.get('is_graded')}`")
            
            with col2:
                st.write("**Types:**")
                st.write(f"assignment_id type: `{type(sub.get('assignment_id'))}`")
                st.write(f"user_id type: `{type(sub.get('user_id'))}`")
                st.write(f"submitted_at: `{sub.get('submitted_at')}`")
                    
def debug_submissions():
    """Fungsi untuk debug data submissions"""
    submissions = load_data(SUBMISSIONS_FILE)
    st.write("🔍 **DEBUG SUBMISSIONS DATA:**")
    st.write(f"Total submissions: {len(submissions)}")
    
    for i, sub in enumerate(submissions):
        st.write(f"--- Submission {i+1} ---")
        st.write(f"ID: {sub.get('id')}")
        st.write(f"Assignment ID: {sub.get('assignment_id')} (type: {type(sub.get('assignment_id'))})")
        st.write(f"User ID: {sub.get('user_id')} (type: {type(sub.get('user_id'))})")
        st.write(f"File Name: {sub.get('file_name')}")
        st.write(f"Submitted At: {sub.get('submitted_at')}")
        st.write(f"Status: {sub.get('status')}")
        st.write(f"Is Graded: {sub.get('is_graded')}")
        
def debug_submission_data(assignment_id, user_id):
    """Debug function untuk melihat data submission sebenarnya"""
    submissions = load_data(SUBMISSIONS_FILE)
    
    st.markdown("---")
    st.subheader("🔍 DEBUG INFO")
    st.write(f"Mencari: assignment_id={assignment_id}, user_id={user_id}")
    st.write(f"Tipe: assignment_id={type(assignment_id)}, user_id={type(user_id)}")
    
    st.write("**Semua Data di submissions.json:**")
    for i, sub in enumerate(submissions):
        st.write(f"**Submission {i+1}:**")
        st.write(f"  - assignment_id: {sub.get('assignment_id')} (tipe: {type(sub.get('assignment_id'))})")
        st.write(f"  - user_id: {sub.get('user_id')} (tipe: {type(sub.get('user_id'))})")
        st.write(f"  - file_name: {sub.get('file_name')}")
        st.write(f"  - match: {sub.get('assignment_id') == assignment_id and sub.get('user_id') == user_id}")
        st.write("---")

def debug_current_user():
    """Debug info untuk user yang sedang login"""
    st.markdown("---")
    st.subheader("👤 DEBUG CURRENT USER")
    if st.session_state.authenticated:
        user = st.session_state.current_user
        st.write(f"**User ID:** {user.get('id')}")
        st.write(f"**Username:** {user.get('username')}")
        st.write(f"**Name:** {user.get('name')}")
        st.write(f"**Role:** {user.get('role')}")
    else:
        st.write("❌ Tidak ada user yang login")

def show_submission_form(assignment, form_key, course_id, module_id):
    """Form untuk mengumpulkan tugas - DENGAN PERBAIKAN"""
    st.markdown("---")
    st.subheader(f"📤 Form Pengumpulan Tugas: {assignment.get('title')}")
    
    current_user = st.session_state.current_user
    
    # Konfirmasi user
    st.info(f"👤 Anda akan mengumpulkan tugas sebagai: **{current_user.get('name')}**")
    
    # Gunakan form dengan key yang unique
    with st.form(key=f"submit_form_{assignment.get('id')}_{current_user.get('id')}_{module_id}", clear_on_submit=False):
        uploaded_file = st.file_uploader(
            "Pilih file tugas *",
            type=[ext.replace(".", "") for ext in assignment.get("file_types", [".pdf", ".doc", ".docx", ".jpg", ".png"])],
            key=f"uploader_{assignment.get('id')}_{current_user.get('id')}_{module_id}"
        )
        
        notes = st.text_area("Catatan (opsional)", 
                           placeholder="Tambahkan catatan untuk pengajar...",
                           key=f"notes_{assignment.get('id')}_{current_user.get('id')}_{module_id}")
        
        # Tampilkan konfirmasi sebelum submit
        if uploaded_file:
            st.success(f"✅ File siap diupload: **{uploaded_file.name}**")
            st.info(f"📏 Ukuran file: {format_file_size(uploaded_file.size)}")
        else:
            st.warning("⚠️ Harap pilih file terlebih dahulu")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("✅ Kumpulkan Tugas", use_container_width=True)
        with col2:
            if st.form_submit_button("❌ Batal", use_container_width=True):
                st.session_state[form_key] = False
                st.rerun()
        
        if submitted:
            if uploaded_file is None:
                st.error("❌ Silakan pilih file terlebih dahulu.")
                return
            
            try:
                # Baca file
                file_data = uploaded_file.getvalue()
                file_name = uploaded_file.name
                file_type = uploaded_file.type
                
                # Validasi tipe file
                allowed_extensions = assignment.get("file_types", [".pdf", ".doc", ".docx", ".jpg", ".png"])
                file_extension = os.path.splitext(file_name)[1].lower()
                
                if file_extension not in allowed_extensions:
                    st.error(f"❌ Tipe file tidak diizinkan. File yang diizinkan: {', '.join(allowed_extensions)}")
                    return
                
                # Validasi ukuran file (max 10MB)
                max_size = 10 * 1024 * 1024  # 10MB
                if len(file_data) > max_size:
                    st.error(f"❌ File terlalu besar. Maksimal {format_file_size(max_size)}")
                    return
                
                # Progress indicator
                with st.spinner("🔄 Mengupload file..."):
                    # Submit assignment
                    success = submit_assignment(
                        assignment.get("id"),
                        current_user.get("id"),
                        file_data,
                        file_name,
                        file_type,
                        notes
                    )
                
                if success:
                    st.success("✅ Tugas berhasil dikumpulkan!")
                    st.balloons()
                    
                    # Reset state
                    st.session_state[form_key] = False
                    
                    # Delay dan refresh
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Gagal mengumpulkan tugas. Silakan coba lagi.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Jika error berlanjut, coba refresh halaman dan ulangi.")

def show_submission_detail(assignment, submission, detail_key):
    """Menampilkan detail lengkap submission termasuk nilai dan feedback"""
    st.markdown("---")
    
    # CEK STATUS PENILAIAN YANG LEBIH AKURAT DENGAN ERROR HANDLING
    score = submission.get('grade')
    max_score = assignment.get('max_points', 100)
    
    is_graded = (
        submission.get("status") == "graded" or 
        submission.get("is_graded") is True or
        score is not None
    )
    
    if is_graded and score is not None:
        st.subheader("📊 Detail Penilaian")
        
        # Fix: Pastikan kalkulasi persentase aman
        try:
            percentage = (score / max_score) * 100 if max_score and max_score > 0 else 0
        except (TypeError, ZeroDivisionError):
            percentage = 0
        
        # Card informasi penilaian
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h4>🎯 Informasi Penilaian</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Informasi dasar
            st.write(f"**📋 Judul Tugas:** {assignment.get('title')}")
            st.write(f"**📅 Waktu Pengumpulan:** {submission.get('submitted_at')[:16]}")
            st.write(f"**📄 File yang Dikumpulkan:** {submission.get('file_name')}")
            
            if submission.get('graded_at'):
                st.write(f"**⏰ Waktu Penilaian:** {submission.get('graded_at')[:16]}")
            if submission.get('graded_by'):
                st.write(f"**👨‍🏫 Dinilai Oleh:** {submission.get('graded_by')}")
            
            # Status penilaian
            st.write(f"**📊 Status Penilaian:** ✅ **Telah Dinilai**")
        
        with col2:
            # Card nilai dengan error handling
            try:
                # Tentukan warna berdasarkan persentase
                if percentage >= 80:
                    color = "#2ecc71"  # Hijau
                    emoji = "🎉"
                    status = "Excellent"
                elif percentage >= 70:
                    color = "#27ae60"  # Hijau muda
                    emoji = "👍"
                    status = "Good"
                elif percentage >= 60:
                    color = "#f39c12"  # Orange
                    emoji = "⚠️"
                    status = "Fair"
                else:
                    color = "#e74c3c"  # Merah
                    emoji = "💡"
                    status = "Need Improvement"
                
                st.markdown(f"""
                <div style='background: {color}; color: white; padding: 20px; border-radius: 10px; 
                            text-align: center; margin: 10px 0;'>
                    <h2>{emoji} {score}/{max_score}</h2>
                    <h3>{percentage:.1f}%</h3>
                    <p><strong>{status}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error menampilkan nilai: {e}")
        
        # Feedback dari guru
        st.markdown("---")
        st.subheader("💬 Feedback dari Guru")
        
        if submission.get('feedback'):
            # Tampilkan feedback dalam card yang menarik
            st.markdown(f"""
            <div style='background: #f8f9fa; border-left: 5px solid #3498db; 
                        padding: 15px; margin: 10px 0; border-radius: 5px;'>
                <h4>📝 Komentar dan Masukan</h4>
                <p style='font-size: 16px; line-height: 1.6;'>{submission.get('feedback')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips berdasarkan nilai
            st.markdown("#### 💡 Tips untuk Perbaikan")
            if percentage >= 80:
                st.success("**Kerja bagus!** Pertahankan kualitas pekerjaan Anda dan terus tingkatkan pemahaman konsep.")
            elif percentage >= 70:
                st.info("**Hasil baik!** Perhatikan detail kecil dan tingkatkan ketelitian dalam pengerjaan.")
            elif percentage >= 60:
                st.warning("**Perlu perhatian lebih.** Pelajari kembali materi dan konsultasikan kesulitan dengan guru.")
            else:
                st.error("**Perlu belajar lebih giat.** Disarankan untuk mengulang materi dan mengerjakan latihan tambahan.")
        else:
            st.info("📝 Guru belum memberikan feedback detail.")
    
    else:
        # Tampilan untuk tugas yang belum dinilai
        st.subheader("📋 Detail Pengumpulan")
        st.info("✅ **Tugas Anda telah berhasil dikumpulkan!**")
        st.write("📊 **Status:** ⏳ Sedang dalam proses penilaian oleh guru")
        
        st.write(f"**📋 Judul Tugas:** {assignment.get('title')}")
        st.write(f"**📅 Waktu Pengumpulan:** {submission.get('submitted_at')[:16]}")
        st.write(f"**📄 File:** {submission.get('file_name')}")
        st.write(f"**📝 Status Sistem:** {submission.get('status', 'submitted').title()}")
        
        if submission.get('notes'):
            st.markdown("---")
            st.subheader("📌 Catatan dari Anda")
            st.markdown(f"""
            <div style='background: #fff3cd; border-left: 5px solid #ffc107; 
                        padding: 15px; margin: 10px 0; border-radius: 5px;'>
                <p style='font-size: 14px; line-height: 1.6;'>{submission.get('notes')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tombol tutup detail
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("❌ Tutup Detail", key=f"close_{detail_key}", use_container_width=True):
            st.session_state[detail_key] = False
            st.rerun()
# ===================== Notifications Page ===================== #
def show_notifications():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>🔔 Notifikasi</h1>
        <p>Lihat semua pemberitahuan dan update terbaru</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.current_user.get("id")
    notifications = get_user_notifications(user_id, unread_only=False)
    
    unread_count = get_unread_notification_count(user_id)
    if unread_count > 0:
        if st.button("📬 Tandai Semua Sudah Dibaca", use_container_width=True):
            mark_all_notifications_as_read(user_id)
            st.success("Semua notifikasi telah ditandai sebagai dibaca!")
            st.rerun()
    
    if not notifications:
        st.info("Belum ada notifikasi.")
        return
    
    st.write(f"Total notifikasi: {len(notifications)} ({unread_count} belum dibaca)")
    
    for notification in notifications:
        border_color = {"info": "#1E90FF", "success": "#32CD32", "warning": "#FFA500", "error": "#FF4500"}.get(notification.get("type"), "#1E90FF")
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        icon = icons.get(notification.get("type"), "📢")
        
        if not notification.get("is_read"):
            st.markdown(f"""
            <div style="border-left: 4px solid {border_color}; padding: 10px; background-color: #f8f9fa; margin: 5px 0; border-radius: 5px;">
                <h4 style="margin: 0;">{icon} {notification.get('title')}</h4>
                <p style="margin: 5px 0;">{notification.get('message')}</p>
                <small>{notification.get('created_at')[:16]}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="border-left: 4px solid {border_color}; padding: 10px; margin: 5px 0; opacity: 0.7; border-radius: 5px;">
                <h4 style="margin: 0;">{icon} {notification.get('title')}</h4>
                <p style="margin: 5px 0;">{notification.get('message')}</p>
                <small>{notification.get('created_at')[:16]}</small>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 6])
        with col1:
            if not notification.get("is_read"):
                if st.button("✓ Tandai Dibaca", key=f"read_{notification.get('id')}"):
                    mark_notification_as_read(notification.get('id'))
                    st.rerun()

# ===================== Profile Page ===================== #
def show_profile():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>👤 Profil Pengguna</h1>
        <p>Informasi akun dan statistik pembelajaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    u = st.session_state.current_user
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class='custom-card' style='text-align: center;'>
            <div style='font-size: 4em;'>👤</div>
            <h3>{u.get('name')}</h3>
            <p>{u.get('role').title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='custom-card'>
            <h4>📋 Informasi Akun</h4>
            <p><strong>Nama:</strong> {u.get('name')}</p>
            <p><strong>Username:</strong> {u.get('username')}</p>
            <p><strong>Email:</strong> {u.get('email')}</p>
            <p><strong>Role:</strong> {u.get('role').title()}</p>
            <p><strong>Terdaftar sejak:</strong> {u.get('registered_at')[:10]}</p>
        </div>
        """, unsafe_allow_html=True)

# ===================== Admin Management - Media Ajar ===================== #
def show_manage_media():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📁 Kelola Media Ajar</h1>
        <p>Unggah dan kelola bahan ajar untuk setiap modul</p>
    </div>
    """, unsafe_allow_html=True)
    
    courses = load_data(COURSES_FILE)
    if not courses:
        st.warning("Belum ada kursus yang tersedia.")
        return
    
    course = courses[0]
    course_id = course.get("id")
    
    tab1, tab2 = st.tabs(["📤 Unggah Media Baru", "📋 Kelola Media Terupload"])
    
    with tab1:
        st.subheader("📤 Unggah Media Ajar Baru")
        
        module_id = st.selectbox("Pilih Modul", range(1, 8), format_func=lambda x: f"Modul {x}", key="media_module")
        media_type = st.selectbox("Jenis Media", 
                                 ["modul_ajar", "bahan_ajar", "lkpd", "media_pembelajaran", "lainnya"],
                                 format_func=lambda x: x.replace("_", " ").title(),
                                 key="media_type_select")
        
        uploaded_file = st.file_uploader(
            "Pilih file media ajar",
            type=["pdf", "doc", "docx", "ppt", "pptx", "jpg", "jpeg", "png", "gif", "mp4", "mp3", "wav", "zip"],
            key="media_upload"
        )
        
        description = st.text_area("Deskripsi Media", placeholder="Jelaskan tentang media ajar ini...", key="media_desc")
        
        if uploaded_file is not None:
            st.info(f"File: {uploaded_file.name} | Ukuran: {format_file_size(uploaded_file.size)}")
            
            if st.button("💾 Upload Media", use_container_width=True, key="upload_media_btn"):
                file_data = uploaded_file.read()
                media = save_media_file(
                    file_data,
                    uploaded_file.name,
                    uploaded_file.type,
                    uploaded_file.size,
                    media_type,
                    description
                )
                
                # Tambahkan media ke modul
                add_media_to_module(course_id, module_id, media.get("id"))
                
                st.success(f"✅ Media '{uploaded_file.name}' berhasil diupload!")
                st.balloons()
    
    with tab2:
        st.subheader("📋 Media Ajar Terupload")
        
        module_id_filter = st.selectbox("Filter berdasarkan Modul", 
                                       [None] + list(range(1, 8)), 
                                       format_func=lambda x: "Semua Modul" if x is None else f"Modul {x}",
                                       key="media_filter")
        
        media_list = load_data(MEDIA_FILE)
        if module_id_filter:
            # Filter media berdasarkan modul yang dipilih
            media_in_module = get_media_by_module(course_id, module_id_filter)
            media_ids_in_module = [m.get("id") for m in media_in_module]
            media_list = [m for m in media_list if m.get("id") in media_ids_in_module]
        
        if not media_list:
            st.info("Belum ada media ajar yang diupload.")
            return
        
        # Inisialisasi session state untuk preview
        if 'current_media_preview' not in st.session_state:
            st.session_state.current_media_preview = None
        
        for i, media in enumerate(media_list):
            # Cari modul yang memiliki media ini
            modules_with_media = []
            for mod_id in range(1, 8):
                module_media = get_media_by_module(course_id, mod_id)
                if any(m.get("id") == media.get("id") for m in module_media):
                    modules_with_media.append(f"Modul {mod_id}")
            
            # Buat key yang unik untuk setiap media item
            media_key = f"media_{media.get('id')}_{module_id_filter if module_id_filter else 'all'}"
            
            # Gunakan index dalam loop untuk membuat expander unik
            with st.expander(f"{get_file_icon(media.get('file_type'))} {media.get('file_name')} - {media.get('media_type').replace('_', ' ').title()}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Jenis:** {media.get('media_type').replace('_', ' ').title()}")
                    st.write(f"**Ukuran:** {format_file_size(media.get('file_size'))}")
                    st.write(f"**Diupload:** {media.get('uploaded_at')[:16]}")
                    st.write(f"**Modul:** {', '.join(modules_with_media) if modules_with_media else 'Tidak terpasang'}")
                    
                    if media.get("description"):
                        st.write(f"**Deskripsi:** {media.get('description')}")
                
                with col2:
                    # Tombol untuk menampilkan preview dengan key yang unik
                    preview_key = f"preview_{media.get('id')}_{module_id_filter if module_id_filter else 'all'}_{i}"
                    if st.button("👁️ Preview", key=preview_key):
                        st.session_state.current_media_preview = media.get("id")
                        st.rerun()
                    
                    # Tombol hapus dengan key yang unik
                    delete_key = f"delete_{media.get('id')}_{module_id_filter if module_id_filter else 'all'}_{i}"
                    if st.button("🗑️ Hapus", key=delete_key):
                        # Hapus dari semua modul terlebih dahulu
                        for mod_id in range(1, 8):
                            remove_media_from_module(course_id, mod_id, media.get("id"))
                        # Hapus file media
                        delete_media_file(media.get("id"))
                        st.success("✅ Media berhasil dihapus!")
                        st.rerun()
        
        # Tampilkan preview media jika dipilih
        if st.session_state.current_media_preview:
            media_id = st.session_state.current_media_preview
            media = get_media_by_id(media_id)
            if media:
                st.markdown("---")
                st.subheader(f"👁️ Preview: {media.get('file_name')}")
                
                # Tombol untuk menutup preview
                if st.button("❌ Tutup Preview", key="close_preview"):
                    st.session_state.current_media_preview = None
                    st.rerun()
                
                display_media_content(media)

# ===================== Admin Management ===================== #
def show_manage_students():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>👥 Kelola Siswa</h1>
        <p>Kelola data siswa dan progress pembelajaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    users = load_data(USERS_FILE)
    students = [u for u in users if u.get("role") == "student"]
    
    if not students:
        st.info("Belum ada siswa yang terdaftar.")
        return
    
    for i, student in enumerate(students):  # PAKAI enumerate UNTUK DAPAT INDEX UNIK
        with st.expander(f"🎓 {student.get('name')} ({student.get('username')})"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Email:** {student.get('email')}")
                st.write(f"**Terdaftar:** {student.get('registered_at')[:10]}")
                
                # Progress siswa
                progress_data = load_data(PROGRESS_FILE)
                student_progress = next((p for p in progress_data if p.get("user_id") == student.get("id")), None)
                if student_progress:
                    progress_value = student_progress.get("progress", 0)
                    completed_modules = len(student_progress.get("completed_modules", []))
                    st.write(f"**Progress:** {progress_value}% ({completed_modules}/7 modul)")
                    st.progress(progress_value / 100)
                else:
                    st.write("**Progress:** Belum memulai pembelajaran")
            
            with col2:
                # GUNAKAN INDEX i UNTUK MEMBUAT KEY YANG LEBIH UNIK
                if st.button("🗑️ Hapus", key=f"del_{student.get('id')}_{i}"):
                    users.remove(student)
                    save_data(users, USERS_FILE)
                    st.success(f"✅ Siswa {student.get('name')} berhasil dihapus!")
                    st.rerun()
                    
def show_manage_modules():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📝 Kelola Modul Pembelajaran</h1>
        <p>Kelola konten dan materi pembelajaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    courses = load_data(COURSES_FILE)
    if not courses:
        st.warning("Belum ada kursus yang tersedia.")
        return
    
    course = courses[0]  # Ambil course pertama
    
    st.markdown(f"""
    <div class='electric-card'>
        <h3>⚡ {course.get('title')}</h3>
        <p>{course.get('description')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    modules = course.get("modules", [])
    
    # Tab untuk mengelola modul dan media
    tab1, tab2 = st.tabs(["✏️ Edit Konten Modul", "📁 Kelola Media Modul"])
    
    with tab1:
        for mid in range(1, 8):
            m = get_module_by_id(modules, mid)
            with st.expander(f"Modul {mid}: {m.get('title') if m else 'Modul Baru'}", expanded=False):
                title = st.text_input("Judul Modul", value=m.get("title") if m else f"Modul {mid} - Hukum Kirchhoff", key=f"title_{mid}")
                content = st.text_area("Konten Materi", value=m.get("content") if m else f"Konten untuk modul {mid}...", key=f"content_{mid}", height=200)
                video_url = st.text_input("URL Video", value=m.get("video_url") if m else "", key=f"video_{mid}")
                quiz_url = st.text_input("URL Quiz", value=m.get("quiz_url") if m else "", key=f"quiz_{mid}")
                
                if st.button(f"💾 Simpan Modul {mid}", key=f"save_{mid}"):
                    new_module = {
                        "id": mid,
                        "title": title,
                        "content": content
                    }
                    if video_url:
                        new_module["video_url"] = video_url
                    if quiz_url:
                        new_module["quiz_url"] = quiz_url
                    
                    # Update atau tambah modul
                    module_exists = False
                    for i, module in enumerate(modules):
                        if module.get("id") == mid:
                            modules[i] = new_module
                            module_exists = True
                            break
                    
                    if not module_exists:
                        modules.append(new_module)
                    
                    course["modules"] = modules
                    for i, c in enumerate(courses):
                        if c.get("id") == course.get("id"):
                            courses[i] = course
                    save_data(courses, COURSES_FILE)
                    
                    st.success(f"✅ Modul {mid} berhasil disimpan!")
                    st.rerun()
    
    with tab2:
        show_manage_media()

def show_manage_course_codes():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>🔑 Kelola Kode Akses</h1>
        <p>Generate dan kelola kode akses kursus</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_code = get_course_code(1)
    
    if current_code:
        st.markdown(f"""
        <div class='electric-card'>
            <h3>🔐 Kode Akses Saat Ini</h3>
            <h2 style='text-align: center; margin: 20px 0;'>{current_code}</h2>
            <p style='text-align: center;'>Berikan kode ini kepada siswa untuk bergabung ke kursus</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Belum ada kode akses yang aktif.")
    
    if st.button("🔄 Generate Kode Baru", use_container_width=True):
        course_codes = load_data(COURSE_CODES_FILE)
        for cc in course_codes:
            if cc.get("course_id") == 1:
                cc["is_active"] = False
        
        new_code = generate_course_code()
        course_codes.append({
            "course_id": 1,
            "code": new_code,
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "max_students": None
        })
        save_data(course_codes, COURSE_CODES_FILE)
        st.success(f"✅ Kode akses baru berhasil dibuat: {new_code}")
        st.rerun()

def show_send_notification():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📢 Kirim Notifikasi</h1>
        <p>Kirim pemberitahuan kepada siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    users = load_data(USERS_FILE)
    students = [u for u in users if u.get("role") == "student"]
    
    st.write(f"**Total siswa:** {len(students)}")
    
    # Pilih penerima
    st.subheader("👥 Pilih Penerima")
    send_to_all = st.checkbox("Kirim ke semua siswa", value=True)
    
    if not send_to_all:
        selected_students = st.multiselect(
            "Pilih siswa tertentu",
            students,
            format_func=lambda s: f"{s.get('name')} ({s.get('username')})"
        )
        student_ids = [s.get("id") for s in selected_students]
    else:
        student_ids = [s.get("id") for s in students]
    
    # Form notifikasi
    st.subheader("📝 Isi Notifikasi")
    title = st.text_input("Judul Notifikasi", placeholder="Contoh: Pengumuman Penting")
    message = st.text_area("Pesan Notifikasi", placeholder="Tulis pesan notifikasi di sini...", height=150)
    notification_type = st.selectbox("Tipe Notifikasi", ["info", "success", "warning", "error"])
    
    # Preview
    if title and message:
        st.subheader("👁️ Preview Notifikasi")
        border_color = {"info": "#1E90FF", "success": "#32CD32", "warning": "#FFA500", "error": "#FF4500"}.get(notification_type, "#1E90FF")
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        icon = icons.get(notification_type, "📢")
        
        st.markdown(f"""
        <div style="border-left: 4px solid {border_color}; padding: 15px; background-color: #f8f9fa; margin: 10px 0; border-radius: 5px;">
            <h4 style="margin: 0;">{icon} {title}</h4>
            <p style="margin: 10px 0;">{message}</p>
            <small>Akan dikirim ke {len(student_ids)} siswa</small>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🚀 Kirim Notifikasi", use_container_width=True):
        if not title or not message:
            st.error("Judul dan pesan tidak boleh kosong!")
            return
        
        if not student_ids:
            st.error("Pilih setidaknya satu siswa sebagai penerima!")
            return
        
        success_count = 0
        for student_id in student_ids:
            try:
                create_notification(
                    student_id,
                    title,
                    message,
                    notification_type,
                    1  # course_id
                )
                success_count += 1
            except Exception as e:
                st.error(f"Gagal mengirim ke siswa ID {student_id}: {str(e)}")
        
        if success_count > 0:
            st.success(f"✅ Notifikasi berhasil dikirim ke {success_count} siswa!")
            st.rerun()

def show_attendance_report():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📊 Laporan Absensi</h1>
        <p>Lihat rekapan absensi siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    date_sel = st.date_input("Pilih Tanggal", value=date.today())
    date_str = date_sel.isoformat()
    
    attendance = get_attendance(1, date_str)  # course_id 1
    users = load_data(USERS_FILE)
    
    if not attendance:
        st.info(f"Belum ada absensi untuk tanggal {date_str}.")
        return
    
    st.write(f"**Rekapan Absensi - {date_str}**")
    
    for att in attendance:
        user = next((u for u in users if u.get("id") == att.get("user_id")), None)
        if user:
            status_icon = "✅" if att.get("status") == "Hadir" else "⚠️" if att.get("status") == "Izin" else "❌"
            st.write(f"{status_icon} **{user.get('name')}** - {att.get('status')}")

def show_manage_assignments():
    inject_custom_css()
    
    st.markdown("""
    <div class='main-header'>
        <h1>📝 Kelola Tugas</h1>
        <p>Kelola tugas dan penilaian siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    courses = load_data(COURSES_FILE)
    if not courses:
        st.warning("Belum ada kursus yang tersedia.")
        return
    
    course = courses[0]  # Ambil course pertama
    course_id = course.get("id")
    
    tab1, tab2, tab3 = st.tabs(["➕ Buat Tugas Baru", "📋 Daftar Tugas", "📊 Kelola Pengumpulan"])
    
    with tab1:
        st.subheader("➕ Buat Tugas Baru")
        
        module_id = st.selectbox("Pilih Modul", range(1, 8), format_func=lambda x: f"Modul {x}")
        title = st.text_input("Judul Tugas")
        description = st.text_area("Deskripsi Tugas")
        due_date = st.date_input("Batas Waktu", value=date.today() + timedelta(days=7))
        max_points = st.number_input("Nilai Maksimal", min_value=1, max_value=1000, value=100)
        
        # File types
        default_types = [".pdf", ".doc", ".docx", ".jpg", ".png", ".zip"]
        selected_types = st.multiselect(
            "Tipe File yang Diizinkan",
            default_types,
            default=default_types
        )
        
        if st.button("Buat Tugas", use_container_width=True):
            if title and description:
                assignment = create_assignment(
                    course_id, module_id, title, description, due_date, max_points, selected_types
                )
                st.success(f"✅ Tugas '{title}' berhasil dibuat!")
            else:
                st.error("Judul dan deskripsi tidak boleh kosong!")
    
    with tab2:
        st.subheader("📋 Daftar Tugas")
        assignments = get_assignments(course_id)
        
        if not assignments:
            st.info("Belum ada tugas untuk kursus ini.")
        else:
            for assignment in assignments:
                with st.expander(f"Modul {assignment.get('module_id')}: {assignment.get('title')}"):
                    st.write(f"**Deskripsi:** {assignment.get('description')}")
                    st.write(f"**Batas Waktu:** {assignment.get('due_date')[:10]}")
                    st.write(f"**Nilai Maksimal:** {assignment.get('max_points')}")
                    st.write(f"**File yang Diizinkan:** {', '.join(assignment.get('file_types', []))}")
                    
                    # Statistik pengumpulan
                    submissions = get_all_submissions(assignment.get("id"))
                    total_submissions = len(submissions)
                    graded_submissions = len([s for s in submissions if s.get("status") == "graded"])
                    
                    st.write(f"**Statistik:** {total_submissions} dikumpulkan, {graded_submissions} dinilai")
                    
                    # Tombol hapus tugas
                    if st.button("🗑️ Hapus Tugas", key=f"delete_{assignment.get('id')}"):
                        if delete_assignment(assignment.get("id")):
                            st.success("✅ Tugas berhasil dihapus!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal menghapus tugas")
    
    with tab3:
        st.subheader("📊 Kelola Pengumpulan")
        assignments = get_assignments(course_id)
        
        if not assignments:
            st.info("Belum ada tugas untuk kursus ini.")
        else:
            selected_assignment = st.selectbox(
                "Pilih Tugas",
                assignments,
                format_func=lambda a: f"Modul {a.get('module_id')}: {a.get('title')}"
            )
            
            if selected_assignment:
                submissions = get_all_submissions(selected_assignment.get("id"))
                users = load_data(USERS_FILE)
                
                if not submissions:
                    st.info("Belum ada pengumpulan untuk tugas ini.")
                else:
                    st.write(f"**Total Pengumpulan:** {len(submissions)}")
                    
                    for submission in submissions:
                        student = next((u for u in users if u.get("id") == submission.get("user_id")), None)
                        
                        # FIX: Handle None status dengan aman
                        status = submission.get('status', 'unknown')
                        status_display = status.title() if status else 'Unknown'
                        
                        with st.expander(f"📄 {student.get('name') if student else 'Unknown'} - {status_display}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Nama:** {student.get('name') if student else 'Unknown'}")
                                st.write(f"**Dikumpulkan:** {submission.get('submitted_at', 'Unknown')[:16]}")
                                st.write(f"**File:** {submission.get('file_name', 'Unknown')}")
                                
                                # Download link dengan error handling
                                if submission.get("file_data"):
                                    try:
                                        st.markdown(create_download_link(
                                            base64.b64decode(submission.get("file_data")),
                                            submission.get("file_name", "file"),
                                            submission.get("file_type", "application/octet-stream")
                                        ), unsafe_allow_html=True)
                                    except Exception as e:
                                        st.error(f"Error membuat link download: {e}")
                                
                                if submission.get("notes"):
                                    st.write(f"**Catatan:** {submission.get('notes')}")
                            
                            with col2:
                                if submission.get("status") == "submitted" or not submission.get("status"):
                                    score = st.number_input(
                                        "Nilai",
                                        min_value=0,
                                        max_value=selected_assignment.get("max_points", 100),
                                        value=submission.get('score', 0),
                                        key=f"score_{submission.get('id')}"
                                    )
                                    feedback = st.text_area(
                                        "Feedback",
                                        value=submission.get('feedback', ''),
                                        placeholder="Berikan feedback untuk siswa...",
                                        key=f"feedback_{submission.get('id')}"
                                    )
                                    
                                    if st.button("💾 Simpan Nilai", key=f"grade_{submission.get('id')}"):
                                        grade_submission(
                                            submission.get("id"),
                                            score,
                                            feedback,
                                            st.session_state.current_user.get("name")
                                        )
                                        st.success("✅ Nilai berhasil disimpan!")
                                        st.rerun()
                                else:
                                    st.write(f"**Nilai:** {submission.get('score', 0)}/{selected_assignment.get('max_points', 100)}")
                                    st.write(f"**Feedback:** {submission.get('feedback', 'Tidak ada feedback')}")
                                    st.write(f"**Dinilai oleh:** {submission.get('graded_by', 'Unknown')}")
                                    if submission.get('graded_at'):
                                        st.write(f"**Waktu Penilaian:** {submission.get('graded_at')[:16]}")
# ===================== Main Function ===================== #
def main():
    init_data()
    inject_custom_css()
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.current_user = None
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "current_media_preview" not in st.session_state:
        st.session_state.current_media_preview = None

    # Sidebar
    st.sidebar.markdown("""
    <div class='sidebar-header'>
        <h2>⚡ LMS Fisika</h2>
        <p>Hukum Kirchhoff</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        user = st.session_state.current_user  # This line was missing indentation
        st.sidebar.markdown(f"""
        <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; padding: 15px; border-radius: 10px; margin: 10px 0;'>
            <h4>👋 Halo, {user.get('name')}!</h4>
            <p>Role: {user.get('role').title()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        user_id = user.get("id")
        unread_count = get_unread_notification_count(user_id)
        notification_text = f"🔔 Notifikasi ({unread_count})" if unread_count > 0 else "🔔 Notifikasi"
        
        if st.sidebar.button("🐛 Debug System", key="debug_system"):
            st.sidebar.write("### Debug Info")
            st.sidebar.write(f"User ID: {user.get('id')}")
            st.sidebar.write(f"Username: {user.get('username')}")
            
            # Debug submissions
            submissions = load_data(SUBMISSIONS_FILE)
            st.sidebar.write(f"Total Submissions: {len(submissions)}")
            
            user_submissions = [s for s in submissions if s.get('user_id') == user.get('id')]
            st.sidebar.write(f"Your Submissions: {len(user_submissions)}")
            
            # Tampilkan detail submissions user ini
            if user_submissions:
                st.sidebar.write("**Detail Submissions Anda:**")
                for sub in user_submissions:
                    st.sidebar.write(f"- Assignment {sub.get('assignment_id')}: {sub.get('file_name')}")
        
        if user.get("role") == "admin":
            menu_options = ["Dashboard", "Materi Pembelajaran", "Laboratorium Virtual", notification_text, 
                           "Kelola Siswa", "Kelola Modul", "Kelola Tugas", "Kelola Kuis", "Kelola Kode Akses", "Kirim Notifikasi", "Lihat Absensi", "Profil"]
        else:
            menu_options = ["Dashboard", "Materi Pembelajaran", "Laboratorium Virtual", notification_text, "Profil"]
        
        selected_menu = st.sidebar.selectbox("📋 Menu Navigasi", menu_options)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.quiz_started = False
            st.session_state.current_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.current_media_preview = None
            st.rerun()
    else:
        selected_menu = None
        show_welcome()
        
        # Login/Register di sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔐 Akses Sistem")
        
        tab1, tab2 = st.sidebar.tabs(["Login", "Registrasi"])
        
        with tab1:
            u = st.text_input("👤 Username")
            p = st.text_input("🔒 Password", type="password")
            if st.button("🚀 Login", use_container_width=True):
                user = authenticate(u, p)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user = user
                    create_notification(
                        user.get("id"),
                        "👋 Selamat Datang Kembali",
                        f"Halo {user.get('name')}! Selamat belajar di LMS Fisika.",
                        "success"
                    )
                    st.rerun()
                else:
                    st.error("❌ Login gagal")

        with tab2:
            name = st.text_input("👤 Nama Lengkap")
            uname = st.text_input("📝 Username Baru")
            pwd = st.text_input("🔒 Password Baru", type="password")
            email = st.text_input("📧 Email")
            if st.button("📝 Daftar", use_container_width=True):
                if name and uname and pwd and email:
                    if register_student(name, uname, pwd, email):
                        st.success("✅ Registrasi berhasil! Silakan login.")
                    else:
                        st.error("❌ Username sudah ada")
                else:
                    st.error("❌ Semua field harus diisi")

    # Routing menu
    if st.session_state.authenticated:
        if selected_menu == "Dashboard":
            show_dashboard()
        elif selected_menu == "Materi Pembelajaran":
            show_my_courses()
        elif selected_menu == "Laboratorium Virtual":
            show_virtual_lab()
        elif "Notifikasi" in selected_menu:
            show_notifications()
        elif selected_menu == "Kelola Siswa" and st.session_state.current_user.get("role") == "admin":
            show_manage_students()
        elif selected_menu == "Kelola Modul" and st.session_state.current_user.get("role") == "admin":
            show_manage_modules()
        elif selected_menu == "Kelola Tugas" and st.session_state.current_user.get("role") == "admin":
            show_manage_assignments()
        elif selected_menu == "Kelola Kuis" and st.session_state.current_user.get("role") == "admin":
            show_manage_quizzes()
        elif selected_menu == "Kelola Kode Akses" and st.session_state.current_user.get("role") == "admin":
            show_manage_course_codes()
        elif selected_menu == "Kirim Notifikasi" and st.session_state.current_user.get("role") == "admin":
            show_send_notification()
        elif selected_menu == "Lihat Absensi" and st.session_state.current_user.get("role") == "admin":
            show_attendance_report()
        elif selected_menu == "Profil":
            show_profile()

if __name__ == "__main__":
    main()
