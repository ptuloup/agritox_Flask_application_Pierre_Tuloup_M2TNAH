import flask_testing
import unittest
from flask_testing import TestCase
from website.models import User, Note, Classement, Ecotoxicite, Proprietespc

from website import create_app, db

class MyTest(TestCase): 

    SQLALCHEMY_DATABASE_URI = "sqlite:///unittests.db"
    TESTING = True

    def create_app(self):

        # pass in test configuration
        return create_app()

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()



class SomeTest(MyTest):

    def test_something(self):
        user = User()
        db.session.add(user)
        db.session.commit()

        # this works
        assert user in db.session

if __name__ == '__main__':
    unittest.main()
