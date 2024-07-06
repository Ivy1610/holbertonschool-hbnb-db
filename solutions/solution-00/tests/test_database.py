import os
import unittest
from flask import Flask
from src.create_app import create_app
from src.persistence.db import db
from src.models.user import User
from dotenv import load_dotenv

load_dotenv()

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        """
        Configurer un environnement de test avant chaque test.
        """
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'sqlite:///test.db')
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """
        Nettoyer après chaque test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_sqlite_connection(self):
        """
        Test de connexion et d'opérations CRUD avec SQLite.
        """
        user = User(email="test@example.com", password="password")
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

            fetched_user = User.query.first()
            self.assertIsNotNone(fetched_user)
            self.assertEqual(fetched_user.email, "test@example.com")

    def test_postgresql_connection(self):
        """
        Test de connexion et d'opérations CRUD avec PostgreSQL.
        """
        # Changez les variables d'environnement pour PostgreSQL
        os.environ['DATABASE_URL'] = 'postgresql://user:password@localhost:5432/test_db'

        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

        user = User(email="test_pg@example.com", password="password")
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

            fetched_user = User.query.first()
            self.assertIsNotNone(fetched_user)
            self.assertEqual(fetched_user.email, "test_pg@example.com")

if __name__ == '__main__':
    unittest.main()

