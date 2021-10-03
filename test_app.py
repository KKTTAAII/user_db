from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserAppTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        img = "https://scontent.fbkk5-4.fna.fbcdn.net/v/t1.6435-9/235810571_10157989934241231_7656140103138915558_n.jpg?_nc_cat=110&ccb=1-5&_nc_sid=730e14&_nc_ohc=WakzplzzpnEAX_iuxbN&_nc_ht=scontent.fbkk5-4.fna&oh=00b41c4f8d160f14079244a5f828fe62&oe=617E3B26"
        user = User(first_name="Kratai", last_name="Gordon", image_url=img)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        self.client = app.test_client() 

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_users(self):
        with self.client as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Kratai Gordon", html)

    def test_show_form(self):
        with self.client as client:
            resp = client.get("/newform")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create a user", html)

    def test_new_user(self):
       with self.client as client:
           user = {"first_name": "Evie", "last_name": "Gordon", "img_url": "image.jpg"}
           resp = client.post("/users/new", data=user, follow_redirects=True)
           html = resp.get_data(as_text=True)

           self.assertEqual(resp.status_code, 200)
           self.assertIn("Evie Gordon", html)

    def test_user_details(self):
       with self.client as client:
           resp = client.get("/user/5/edit")
        #  I am not sure why the id is always 5 when we should drop all rows
        #  in the table so it should start with 1, shouldnt it?
           html = resp.get_data(as_text=True)

           self.assertEqual(resp.status_code, 200)
           self.assertIn("Kratai", html)
           self.assertIn("Cancel", html)
           self.assertIn("Save", html)
           
        
            
    