"""Local PACP review server. Run from the repository root."""
import hashlib
import hmac
import os
from pathlib import Path
import secrets
import sqlite3
from contextlib import closing
from html import escape
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit, quote

DB = os.environ.get("PACP_DB", "portal-review.sqlite3")
SCHEMA = """
CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, salt TEXT, password TEXT, role TEXT);
CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, email TEXT, csrf TEXT, expiry INTEGER);
CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY, email TEXT UNIQUE, specialty TEXT, status TEXT, verification_token TEXT UNIQUE, revoked INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, application INTEGER, actor TEXT, decision TEXT, reason TEXT, time TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY, title TEXT, points INTEGER CHECK(points BETWEEN 0 AND 100));
CREATE TABLE IF NOT EXISTS registrations(course INTEGER, email TEXT, completed INTEGER DEFAULT 0, PRIMARY KEY(course,email));
"""

def digest(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600000).hex()

def init():
    with closing(sqlite3.connect(DB)) as db, db:
        db.executescript(SCHEMA)
        columns = {row[1] for row in db.execute("PRAGMA table_info(applications)")}
        if "verification_token" not in columns:
            db.execute("ALTER TABLE applications ADD COLUMN verification_token TEXT")
        if "revoked" not in columns:
            db.execute("ALTER TABLE applications ADD COLUMN revoked INTEGER NOT NULL DEFAULT 0")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS applications_verification_token_unique ON applications(verification_token)")
        for name, role in (("member", "member"), ("reviewer", "reviewer"), ("admin", "admin")):
            email = name + "@pacp.example"
            if not db.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
                password, salt = secrets.token_urlsafe(18), secrets.token_hex(16)
                db.execute("INSERT INTO users VALUES(?,?,?,?)", (email, salt, digest(password, salt), role))
                print(email, password, flush=True)

def form(action, csrf, body, label):
    return (f'<form method="post" action="/{action}"><input type="hidden" name="csrf" '
            f'value="{csrf}">{body}<button>{label}</button></form>')

class Handler(BaseHTTPRequestHandler):
    def page(self, body, status=200, cookie=None):
        html = ("""<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>البوابة الرقمية | PACP</title><link rel="stylesheet" href="/portal.css">
            <header><div class="bar"><img class="official-logo" src="/pacp-logo-original.png" alt=""><div class="brand"><strong>PACP</strong>
            الجمعية الفلسطينية لاختصاصيي علم النفس العيادي</div><span class="badge">معاينة محلية</span></div></header>
            <main><div class="hero"><div><span class="kicker">العضوية والتطوير المهني</span>
            <h1>البوابة الرقمية</h1><p>تابعي طلب العضوية والبطاقة والدورات من حسابك.</p></div>
            <div class="scene" tabindex="0" aria-label="بطاقة PACP تفاعلية">
            <div class="sculpture" aria-hidden="true"><span>PACP</span></div></div></div>
            <div class="content">""" + body + """</div></main>
            <footer>بيئة مراجعة محلية · استخدمي بيانات اصطناعية فقط</footer></html>""").encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'self'; img-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(html)

    def session(self, db):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        token = cookie.get("pacp")
        if token:
            return db.execute("""SELECT email,role,csrf,token FROM sessions JOIN users USING(email)
                                 WHERE token=? AND expiry>unixepoch()""", (token.value,)).fetchone()

    def do_GET(self):
        target = urlsplit(self.path)
        if target.path == "/verify":
            code = parse_qs(target.query).get("code", [""])[0]
            if not (20 <= len(code) <= 90) or not all(c.isalnum() or c in "-_" for c in code):
                return self.page("<h2>تعذر التحقق من البطاقة</h2><p>رمز التحقق غير صالح.</p>", 404)
            with closing(sqlite3.connect(DB)) as db:
                found = db.execute("""SELECT 1 FROM applications
                    WHERE verification_token=? AND status='approved' AND revoked=0""", (code,)).fetchone()
            if found:
                return self.page("<h2>حالة البطاقة: سارية في البيئة التجريبية</h2><p>هذه نتيجة تحقق محلية توضيحية، وليست إثبات عضوية رسمية.</p>")
            return self.page("<h2>البطاقة غير سارية</h2><p>الرمز غير معروف أو تم إلغاء صلاحية البطاقة.</p>", 404)
        if self.path == "/pacp-logo-original.png":
            logo = (Path(__file__).resolve().parent.parent / "assets/pacp-logo-original.png").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            self.wfile.write(logo)
            return
        if self.path == "/portal.css":
            css = Path(__file__).with_name("portal.css").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(css)
            return

        with closing(sqlite3.connect(DB)) as db:
            user = self.session(db)
            if not user:
                return self.page("<h2>تسجيل الدخول</h2>" + form("login", "", '<label>البريد <input name="email" type="email" required></label>'
                    '<label>كلمة المرور <input name="password" type="password" required></label>', "دخول"))
            email, role, csrf, _ = user
            role_labels = {"member": "مساحة العضو", "reviewer": "مراجعة العضوية", "admin": "إدارة البوابة"}
            body = f"<h2>{role_labels[role]}</h2><p dir='ltr'>{escape(email)}</p>" + form("logout", csrf, "", "خروج")
            if role == "member":
                row = db.execute("SELECT id,specialty,status,verification_token,revoked FROM applications WHERE email=?", (email,)).fetchone()
                if row:
                    ident, specialty, status, verification_token, revoked = row
                    body += f"<section>طلب العضوية · {escape(specialty)} · {status}"
                    if status == "approved" and not revoked:
                        body += f'<img class="official-logo" src="/pacp-logo-original.png" alt="شعار الجمعية">'
                        body += f'<p>بطاقة تجريبية · <a href="/verify?code={quote(verification_token or "")}">التحقق من حالة البطاقة</a></p>' 
                    for decision, reason in db.execute("SELECT decision,reason FROM audit WHERE application=? ORDER BY id", (ident,)):
                        body += f"<p>{escape(decision)} · {escape(reason)}</p>"
                    body += "</section>"
                if not row or row[2] == "needs_changes":
                    body += form("apply", csrf, '<label>التخصص <input name="specialty" required maxlength="120"></label>', "إرسال الطلب")
                for ident, title, points, completed in db.execute("""
                    SELECT c.id,c.title,c.points,r.completed FROM courses c
                    LEFT JOIN registrations r ON r.course=c.id AND r.email=? ORDER BY c.id
                """, (email,)):
                    body += f"<section>{escape(title)} · {points} نقاط"
                    if completed is None and row and row[2] == "approved":
                        body += form("register", csrf, f'<input type="hidden" name="id" value="{ident}">', "تسجيل")
                    elif completed == 1:
                        body += "<p>اكتمل الحضور واعتمدت النقاط</p>"
                    elif completed == 0:
                        body += "<p>مسجل</p>"
                    body += "</section>"
            if role in ("reviewer", "admin"):
                for ident, applicant, specialty, status in db.execute("SELECT id,email,specialty,status FROM applications ORDER BY id"):
                    body += f"<section>{escape(applicant)} · {escape(specialty)} · {status}"
                    if status == "submitted" and role == "reviewer":
                        body += form("decide", csrf, f'<input type="hidden" name="id" value="{ident}">'
                            '<label>القرار <select name="decision"><option value="approved">اعتماد</option>'
                            '<option value="needs_changes">استكمال</option><option value="rejected">رفض</option></select></label>'
                            '<label>السبب <input name="reason" maxlength="240"></label>', "حفظ القرار")
                    body += "</section>"
            if role == "admin":
                for ident, applicant in db.execute("SELECT id,email FROM applications WHERE status='approved' AND revoked=0"):
                    body += form("revoke", csrf, f'<input type="hidden" name="id" value="{ident}">'
                        f'<span>{escape(applicant)}</span><label>سبب إلغاء البطاقة <input name="reason" maxlength="240" required></label>',
                        "إلغاء صلاحية البطاقة التجريبية")
                body += form("course", csrf, '<label>الدورة <input name="title" required maxlength="120"></label>'
                    '<label>النقاط <input name="points" type="number" min="0" max="100" required></label>', "إضافة دورة")
                for ident, title, applicant in db.execute("""SELECT c.id,c.title,r.email FROM registrations r
                                                             JOIN courses c ON c.id=r.course WHERE r.completed=0"""):
                    body += form("complete", csrf, f'{escape(title)} · {escape(applicant)}'
                        f'<input type="hidden" name="id" value="{ident}"><input type="hidden" name="email" value="{escape(applicant, quote=True)}">', "اعتماد الحضور والنقاط")
            self.page(body)

    def redirect(self, cookie=None):
        self.send_response(303)
        self.send_header("Location", "/")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError()
            data = parse_qs(self.rfile.read(length).decode(), max_num_fields=12)
            self.act(lambda key: data.get(key, [""])[0].strip())
        except (ValueError, sqlite3.IntegrityError):
            self.page('<p>تعذر تنفيذ الإجراء بالحالة أو البيانات الحالية.</p><a href="/">عودة</a>', 400)

    def act(self, field):
        with closing(sqlite3.connect(DB)) as db, db:
            if self.path == "/login":
                user = db.execute("SELECT salt,password FROM users WHERE email=?", (field("email"),)).fetchone()
                if not user or not hmac.compare_digest(digest(field("password"), user[0]), user[1]):
                    return self.page('<p>بيانات الدخول غير صحيحة.</p><a href="/">عودة</a>', 401)
                token = secrets.token_urlsafe(32)
                db.execute("INSERT INTO sessions VALUES(?,?,?,unixepoch()+3600)",
                           (token, field("email"), secrets.token_urlsafe(32)))
                db.commit()
                return self.redirect(f"pacp={token}; HttpOnly; SameSite=Strict; Path=/")
            user = self.session(db)
            if not user or not hmac.compare_digest(user[2], field("csrf")):
                return self.page("الدخول مطلوب أو انتهت صلاحية الطلب.", 403)
            email, role, _, token = user
            if self.path == "/logout":
                db.execute("DELETE FROM sessions WHERE token=?", (token,))
                db.commit()
                return self.redirect("pacp=; Max-Age=0; HttpOnly; SameSite=Strict; Path=/")
            permissions = {"/apply":"member", "/register":"member", "/decide":"reviewer", "/course":"admin", "/complete":"admin", "/revoke":"admin"}
            if permissions.get(self.path) != role:
                return self.page("هذا الإجراء غير متاح لصلاحيات حسابك.", 403)
            db.execute("BEGIN IMMEDIATE")
            if self.path == "/apply":
                specialty = field("specialty")
                if not 0 < len(specialty) <= 120:
                    raise ValueError()
                result = db.execute("""INSERT INTO applications(email,specialty,status) VALUES(?,?,'submitted')
                    ON CONFLICT(email) DO UPDATE SET specialty=excluded.specialty,status='submitted'
                    WHERE applications.status='needs_changes'""", (email,specialty))
            elif self.path == "/decide":
                decision, reason, ident = field("decision"), field("reason"), int(field("id"))
                if decision not in ("approved","rejected","needs_changes") or len(reason) > 240 or (decision != "approved" and not reason):
                    raise ValueError()
                if decision == "approved":
                    result = db.execute("""UPDATE applications SET status=?, verification_token=?, revoked=0
                        WHERE id=? AND status='submitted'""", (decision, secrets.token_urlsafe(24), ident))
                else:
                    result = db.execute("UPDATE applications SET status=? WHERE id=? AND status='submitted'", (decision,ident))
                if result.rowcount:
                    db.execute("INSERT INTO audit(application,actor,decision,reason) VALUES(?,?,?,?)", (ident,email,decision,reason))
            elif self.path == "/course":
                title = field("title")
                if not 0 < len(title) <= 120:
                    raise ValueError()
                result = db.execute("INSERT INTO courses(title,points) VALUES(?,?)", (title,int(field("points"))))
            elif self.path == "/register":
                result = db.execute("""INSERT OR IGNORE INTO registrations(course,email)
                    SELECT courses.id,applications.email FROM courses CROSS JOIN applications
                    WHERE courses.id=? AND applications.email=? AND applications.status='approved'""", (int(field("id")),email))
            elif self.path == "/revoke":
                ident = int(field("id"))
                reason = field("reason")
                if not 0 < len(reason) <= 240:
                    raise ValueError()
                result = db.execute("""UPDATE applications SET revoked=1,verification_token=NULL
                    WHERE id=? AND status='approved' AND revoked=0""", (ident,))
                if result.rowcount:
                    db.execute("INSERT INTO audit(application,actor,decision,reason) VALUES(?,?,?,?)",
                               (ident,email,"revoked",reason))
            else:
                result = db.execute("UPDATE registrations SET completed=1 WHERE course=? AND email=? AND completed=0",
                                    (int(field("id")),field("email")))
            if result.rowcount != 1:
                raise ValueError()
            db.commit()
            self.redirect()

if __name__ == "__main__":
    init()
    print("http://127.0.0.1:8765", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
