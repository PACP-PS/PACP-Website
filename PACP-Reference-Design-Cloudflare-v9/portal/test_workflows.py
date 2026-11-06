"""Local integration tests with synthetic users only; never run against production."""
import http.client
import importlib.util
import os
from pathlib import Path
import re
import secrets
import sqlite3
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pacp_local_portal', HERE / 'app.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        app.DB = str(Path(cls.temp.name) / 'test.sqlite3')
        with sqlite3.connect(app.DB) as db:
            db.executescript(app.SCHEMA)
            for role in ('member', 'reviewer', 'admin'):
                salt = secrets.token_hex(16)
                db.execute('INSERT INTO users VALUES (?,?,?,?)',
                           (role + '@example.test', salt, app.digest('synthetic-test-only', salt), role))
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), app.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)
        cls.temp.cleanup()

    def request(self, path='/', fields=None, cookie=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_address[1], timeout=5)
        headers = {}
        if cookie: headers['Cookie'] = cookie
        if fields is not None:
            body = urlencode(fields)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            conn.request('POST', path, body, headers)
        else:
            conn.request('GET', path, headers=headers)
        response = conn.getresponse()
        status, headers, content = response.status, dict(response.getheaders()), response.read().decode('utf-8')
        conn.close()
        return status, headers, content

    def login(self, role):
        status, headers, _ = self.request('/login', {'email': role+'@example.test','password':'synthetic-test-only'})
        self.assertEqual(status, 303)
        cookie = headers['Set-Cookie'].split(';')[0]
        with sqlite3.connect(app.DB) as db:
            csrf = db.execute('SELECT csrf FROM sessions WHERE email=?', (role+'@example.test',)).fetchone()[0]
        return cookie, csrf

    def test_end_to_end_permissions_and_workflow(self):
        member, mcsrf = self.login('member')
        reviewer, rcsrf = self.login('reviewer')
        admin, acsrf = self.login('admin')
        self.assertEqual(self.request('/apply', {'specialty':'Psychology','csrf':'bad'}, member)[0], 403)
        self.assertEqual(self.request('/decide', {'id':'1','decision':'approved','csrf':mcsrf}, member)[0], 403)
        self.assertEqual(self.request('/apply', {'specialty':'Clinical psychology','csrf':mcsrf}, member)[0], 303)
        self.assertEqual(self.request('/decide', {'id':'1','decision':'approved','csrf':rcsrf}, reviewer)[0], 303)
        status, _, html = self.request('/', cookie=member)
        self.assertEqual(status, 200)
        self.assertIn('التحقق من حالة البطاقة', html)
        with sqlite3.connect(app.DB) as db:
            code = db.execute("SELECT verification_token FROM applications WHERE id=1").fetchone()[0]
        self.assertTrue(code and len(code)>=20)
        self.assertEqual(self.request('/verify?code='+code)[0],200)
        self.assertEqual(self.request('/verify?code=invalid')[0],404)
        self.assertEqual(self.request('/revoke', {'id':'1','reason':'test','csrf':mcsrf}, member)[0],403)
        self.assertEqual(self.request('/course', {'title':'DBT Skills','points':'3','csrf':acsrf}, admin)[0], 303)
        self.assertEqual(self.request('/register', {'id':'1','csrf':mcsrf}, member)[0], 303)
        self.assertEqual(self.request('/complete', {'id':'1','email':'member@example.test','csrf':acsrf}, admin)[0], 303)
        self.assertIn('اكتمل الحضور', self.request('/', cookie=member)[2])
        with sqlite3.connect(app.DB) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM audit WHERE decision="approved"').fetchone()[0],1)
            self.assertEqual(db.execute('SELECT completed FROM registrations').fetchone()[0],1)
        self.assertEqual(self.request('/revoke', {'id':'1','reason':'Synthetic revocation','csrf':acsrf}, admin)[0],303)
        self.assertEqual(self.request('/verify?code='+code)[0],404)
        with sqlite3.connect(app.DB) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM audit WHERE decision='revoked'").fetchone()[0],1)
        self.assertEqual(self.request('/logout', {'csrf':mcsrf}, member)[0],303)
        self.assertIn('تسجيل الدخول',self.request('/',cookie=member)[2])

    def test_unauthenticated_and_invalid_login(self):
        self.assertEqual(self.request('/apply', {'specialty':'test','csrf':'x'})[0],403)
        self.assertEqual(self.request('/login', {'email':'member@example.test','password':'wrong'})[0],401)
        self.assertEqual(self.request('/')[0],200)

if __name__ == '__main__':
    unittest.main(verbosity=2)
