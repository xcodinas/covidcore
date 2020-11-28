import unittest

from app import app, db


class DeletosApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        cls.app = app
        cls.client = app.test_client()

        db.create_all()

        super().setUpClass()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_example_page_unlogged(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        DeletosApiTestCase))
    return suite
