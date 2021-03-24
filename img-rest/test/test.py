
import os
import tempfile
import sys
import flask_unittest

sys.path.append(os.getcwd())
from app import runner


class TestImgRest(flask_unittest.AppTestCase):

    # https://github.com/TotallyNotChase/flask-unittest
    def create_app(self):
        self.app = runner.app
        return self.app


    def test_blank_load(self, app):
        with app.test_client() as client:
            rv = client.get('/' )
        self.assertEqual(rv.status, "200 OK")


    def test_resize_empty_file(self, app):
        fp = tempfile.TemporaryFile()
        with app.test_client() as client:
            rv = client.post('/resize/', data={"file": (fp, "fake_name") } )
        print( rv )
        self.assertEqual(rv.status, "200 OK")


    def test_resize_bad_input(self, app):
        fp = tempfile.TemporaryFile()
        with app.test_client() as client:
            rv = client.post('/resize/' )
        print( rv )
        self.assertEqual(rv.status, "400 BAD REQUEST")

