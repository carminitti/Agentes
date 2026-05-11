# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import sqlite3, json, os
from datetime import datetime

SUITE_DIR = r"C:\Users\gabriel.carminitti\Documents\claude\agentes\suite6\suite_api_browser_k6_visual_axe_zap_db_20260511_132805"
OUTPUT_DIR = os.path.join(SUITE_DIR, "banco")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ok_mark(b): return "OK" if b else "FAIL"

results = []
log_lines = [f"[{ts()}] === executor-banco -- inicio ===", f"[{ts()}] Modo: sqlite::memory: (simulated)"]


def test_elearning_schema():
    tc_id = "TC-DB-S6-001"
    title = "Integridade do schema de e-learning (courses, students, enrollments)"
    logs, checks, status, error = [], [], "passed", None
    t0 = datetime.now()

    def chk(label, ok, blocking=True):
        nonlocal status, error
        c = {"check": label, "result": "passed" if ok else "failed"}
        if not ok and blocking: status = "failed"; error = error or f"Falha: {label}"
        checks.append(c); logs.append(f"[ASSERT] {label} {ok_mark(ok)}")

    try:
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                instructor_name TEXT NOT NULL,
                duration_hours INTEGER NOT NULL CHECK(duration_hours > 0),
                max_students INTEGER NOT NULL CHECK(max_students > 0)
            );
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                enrollment_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL REFERENCES courses(id),
                student_id INTEGER NOT NULL REFERENCES students(id),
                progress_percent REAL NOT NULL CHECK(progress_percent >= 0 AND progress_percent <= 100),
                completed_at TEXT
            );
        """)
        conn.commit()
        logs.append("[DB] Schema criado com sucesso")

        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        for tbl in ["courses", "students", "enrollments"]:
            chk(f"tabela '{tbl}' existe", tbl in tables)

        # CHECK duration_hours > 0
        try:
            cur.execute("INSERT INTO courses(title,instructor_name,duration_hours,max_students) VALUES('X','Y',0,10)")
            conn.commit(); chk("CHECK duration_hours > 0 rejeitou valor 0", False)
        except sqlite3.IntegrityError:
            chk("CHECK duration_hours > 0 rejeitou valor 0", True)

        # CHECK max_students > 0
        try:
            cur.execute("INSERT INTO courses(title,instructor_name,duration_hours,max_students) VALUES('X','Y',10,0)")
            conn.commit(); chk("CHECK max_students > 0 rejeitou valor 0", False)
        except sqlite3.IntegrityError:
            chk("CHECK max_students > 0 rejeitou valor 0", True)

        # Inserir curso valido
        cur.execute("INSERT INTO courses(title,instructor_name,duration_hours,max_students) VALUES('QA Fundamentals','Jane Doe',40,30)")
        conn.commit()
        course_id = cur.lastrowid
        logs.append(f"[DB] Curso inserido ID={course_id}")

        # SELECT
        row = cur.execute("SELECT title,instructor_name,duration_hours,max_students FROM courses WHERE id=?", (course_id,)).fetchone()
        ok_sel = row is not None and row[0] == "QA Fundamentals" and row[2] == 40 and row[3] == 30
        chk("curso recuperavel via SELECT com mesmos valores", ok_sel)

        # INSERT student para testes de FK
        cur.execute("INSERT INTO students(name,email,enrollment_date) VALUES('Ana','ana@test.com','2026-01-01')")
        conn.commit()
        student_id = cur.lastrowid

        # CHECK progress_percent 0-100
        try:
            cur.execute("INSERT INTO enrollments(course_id,student_id,progress_percent) VALUES(?,?,101)", (course_id, student_id))
            conn.commit(); chk("CHECK progress_percent rejeitou valor 101", False)
        except sqlite3.IntegrityError:
            chk("CHECK progress_percent rejeitou valor 101", True)

        # FK course_id invalido
        try:
            cur.execute("INSERT INTO enrollments(course_id,student_id,progress_percent) VALUES(9999,?,50)", (student_id,))
            conn.commit(); chk("FK course_id invalido rejeitado", False)
        except sqlite3.IntegrityError:
            chk("FK course_id invalido rejeitado", True)

        conn.close()

    except Exception as e:
        status = "failed"; error = str(e); logs.append(f"[ERROR] {e}")

    duration_ms = int((datetime.now() - t0).total_seconds() * 1000)
    logs.append(f"-> STATUS: {status.upper()}")
    return {
        "id": tc_id, "title": title, "status": status, "duration_ms": duration_ms, "mode": "simulated",
        "details": {"connection": "sqlite://:memory:", "validations": checks},
        "logs": logs, "error": error
    }


def test_health_schema():
    tc_id = "TC-DB-S6-002"
    title = "Integridade do schema de saude (patients, doctors, appointments)"
    logs, checks, status, error = [], [], "passed", None
    t0 = datetime.now()

    def chk(label, ok, blocking=True):
        nonlocal status, error
        c = {"check": label, "result": "passed" if ok else "failed"}
        if not ok and blocking: status = "failed"; error = error or f"Falha: {label}"
        checks.append(c); logs.append(f"[ASSERT] {label} {ok_mark(ok)}")

    try:
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                crm TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                birth_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL REFERENCES doctors(id),
                patient_id INTEGER NOT NULL REFERENCES patients(id),
                scheduled_at TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('scheduled','completed','cancelled')),
                notes TEXT
            );
        """)
        conn.commit()
        logs.append("[DB] Schema de saude criado com sucesso")

        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        for tbl in ["doctors", "patients", "appointments"]:
            chk(f"tabela '{tbl}' existe", tbl in tables)

        # Inserir medico
        cur.execute("INSERT INTO doctors(name,specialty,crm) VALUES('Dr. QA Test','Cardiologia','CRM-123456')")
        conn.commit()
        doctor_id = cur.lastrowid

        # UNIQUE crm
        try:
            cur.execute("INSERT INTO doctors(name,specialty,crm) VALUES('Dr. Dup','Ortopedia','CRM-123456')")
            conn.commit(); chk("UNIQUE crm rejeitou duplicata", False)
        except sqlite3.IntegrityError:
            chk("UNIQUE crm rejeitou duplicata", True)

        # Inserir paciente
        cur.execute("INSERT INTO patients(name,cpf,birth_date) VALUES('Joao','111.222.333-44','1990-01-01')")
        conn.commit()
        patient_id = cur.lastrowid

        # UNIQUE cpf
        try:
            cur.execute("INSERT INTO patients(name,cpf,birth_date) VALUES('Maria','111.222.333-44','1992-02-02')")
            conn.commit(); chk("UNIQUE cpf rejeitou duplicata", False)
        except sqlite3.IntegrityError:
            chk("UNIQUE cpf rejeitou duplicata", True)

        # CHECK status
        try:
            cur.execute("INSERT INTO appointments(doctor_id,patient_id,scheduled_at,status) VALUES(?,?,'2026-05-01','invalid')", (doctor_id, patient_id))
            conn.commit(); chk("CHECK status rejeitou valor 'invalid'", False)
        except sqlite3.IntegrityError:
            chk("CHECK status rejeitou valor 'invalid'", True)

        # FK patient_id invalido
        try:
            cur.execute("INSERT INTO appointments(doctor_id,patient_id,scheduled_at,status) VALUES(?,9999,'2026-05-01','scheduled')", (doctor_id,))
            conn.commit(); chk("FK patient_id invalido rejeitado", False)
        except sqlite3.IntegrityError:
            chk("FK patient_id invalido rejeitado", True)

        # SELECT medico
        row = cur.execute("SELECT name,specialty,crm FROM doctors WHERE id=?", (doctor_id,)).fetchone()
        ok_sel = row is not None and row[0] == "Dr. QA Test" and row[2] == "CRM-123456"
        chk("medico recuperavel via SELECT com mesmos valores", ok_sel)

        conn.close()

    except Exception as e:
        status = "failed"; error = str(e); logs.append(f"[ERROR] {e}")

    duration_ms = int((datetime.now() - t0).total_seconds() * 1000)
    logs.append(f"-> STATUS: {status.upper()}")
    return {
        "id": tc_id, "title": title, "status": status, "duration_ms": duration_ms, "mode": "simulated",
        "details": {"connection": "sqlite://:memory:", "validations": checks},
        "logs": logs, "error": error
    }


log_lines.append(f"[{ts()}] Executando TC-DB-S6-001...")
r1 = test_elearning_schema()
results.append(r1)
for l in r1["logs"]: log_lines.append(f"[{ts()}]   {l}")
log_lines.append(f"[{ts()}] [TC-DB-S6-001] -> {r1['status'].upper()}")

log_lines.append(f"[{ts()}] Executando TC-DB-S6-002...")
r2 = test_health_schema()
results.append(r2)
for l in r2["logs"]: log_lines.append(f"[{ts()}]   {l}")
log_lines.append(f"[{ts()}] [TC-DB-S6-002] -> {r2['status'].upper()}")

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

summary = {"total": 2, "passed": passed, "failed": failed, "skipped": 0, "credentials_failed": False}
output = {
    "executor": "banco",
    "environment": "sqlite://:memory:",
    "credentials_failed": False,
    "generated_files": None,
    "results": results,
    "summary": summary
}

log_lines.append(f"[{ts()}] === Fim: {passed} passou, {failed} falhou ===")

with open(os.path.join(OUTPUT_DIR, "resultado.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
with open(os.path.join(OUTPUT_DIR, "execution.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print(json.dumps(output, ensure_ascii=False, indent=2))
