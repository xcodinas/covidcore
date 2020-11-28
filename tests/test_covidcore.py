import unittest

from covidcore import covidcore, db
from manage import create_user

TEST_DB = 'test.db'


class covidcoreTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        covidcore.config['TESTING'] = True
        covidcore.config['WTF_CSRF_ENABLED'] = False
        covidcore.config['DEBUG'] = False
        covidcore.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        cls.covidcore = covidcore
        cls.client = covidcore.test_client()

        db.create_all()
        with covidcore.app_context():
            cls.admin = create_user()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        db.drop_all()

    def tearDown(self):
        self.logout()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_main_page_unlogged(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_after_login(self):
        self.login('admin@admin.com', 'admin')
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.logout()


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            covidcoreTestCase))
    return suite
