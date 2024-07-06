# tests/test_rbac.py

import unittest
from hbnb import create_app, db
from src.models.user import User
from flask_jwt_extended import create_access_token

class TestRBAC(unittest.TestCase):

    def setUp(self):
        self.app = create_app("src.config.TestConfig")
        self.client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            db.create_all()
            admin_user = User(username="admin", password="adminpass", is_admin=True)
            normal_user = User(username="user", password="userpass", is_admin=False)
            db.session.add(admin_user)
            db.session.add(normal_user)
            db.session.commit()
            self.admin_token = create_access_token(identity=admin_user.id, additional_claims={"is_admin": True})
            self.user_token = create_access_token(identity=normal_user.id, additional_claims={"is_admin": False})

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_admin_access(self):
        response = self.client.post('/api/v1/admin/amenities', headers={"Authorization": f"Bearer {self.admin_token}"}, json={"name": "WiFi"})
        self.assertEqual(response.status_code, 201)

    def test_user_access_to_admin_endpoint(self):
        response = self.client.post('/api/v1/admin/amenities', headers={"Authorization": f"Bearer {self.user_token}"}, json={"name": "WiFi"})
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()

