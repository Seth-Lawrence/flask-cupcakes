from models import db, Cupcake
from app import app
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        """testing if route returns single cupcake json"""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """testing if route creates an instances of cupcake"""
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json['cupcake']['id']

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """testing if route successfully updates cupcake instance if not all fields
        are inputted"""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(url, json={"flavor": "UpdatedFlavor",
                                           "size": "UpdatedSize"})

            # cupcake_id = resp.json['cupcake']['id']
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "UpdatedFlavor",
                    "size": "UpdatedSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })
            self.assertEqual(Cupcake.query.count(), 1)


    def test_delete_cupcake(self):
        """testing if cupcake instance is succesfully deleted"""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(resp.json, {
                "deleted": [self.cupcake_id]
            })

    #test_update_cupcake_404
    #test 404s for both routes
    def test_update_cupcake_404(self):
        """testing if route successfully updates cupcake instance if not all fields
        are inputted"""
        with app.test_client() as client:
            url = f"/api/cupcakes/99"
            resp = client.patch(url, json={"flavor": "UpdatedFlavor",
                                           "size": "UpdatedSize"})


            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake_404(self):
        """testing if cupcake instance is succesfully deleted"""
        with app.test_client() as client:
            url = f"/api/cupcakes/99"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)
