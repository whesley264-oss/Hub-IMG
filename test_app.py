import unittest
import os
from app import app, db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.app.post('/register', data=dict(
            username='testuser_register',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        with app.app_context():
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('testpassword', method='pbkdf2:sha256')
            new_user = User(username='testuser_login', password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        response = self.app.post('/login', data=dict(
            username='testuser_login',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
