import unittest
from app import create_app
from models import db, User

class UserViewsTestCase(unittest.TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'postgresql:///test_blogly'
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test the home page redirect."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_show_users(self):
        """Test showing all users."""
        with self.app.app_context():
            user = User(first_name="Test", last_name="User", image_url="")
            db.session.add(user)
            db.session.commit()

        response = self.client.get('/users')
        self.assertIn('Test User', response.get_data(as_text=True))

    def test_add_user(self):
        """Test adding a new user."""
        response = self.client.post('/users/new', data={'first_name': 'New', 'last_name': 'User', 'image_url': ''}, follow_redirects=True)
        self.assertIn('New User', response.get_data(as_text=True))

    def test_user_detail(self):
        """Test the user detail page."""
        with self.app.app_context():
            user = User(first_name="Detail", last_name="User", image_url="")
            db.session.add(user)
            db.session.commit()

        response = self.client.get(f'/users/{user.id}')
        self.assertIn('Detail User', response.get_data(as_text=True))

    def test_show_user_with_posts(self):
        """Test showing user detail with posts."""
        response = self.client.get('/users/1')
        self.assertIn('Test Post', response.get_data(as_text=True))

    def test_add_post_form(self):
        """Test display of the add post form."""
        response = self.client.get('/users/1/posts/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add New Post', response.get_data(as_text=True))

    def test_add_post(self):
        """Test adding a new post."""
        response = self.client.post('/users/1/posts/new', data={
            'title': 'New Post',
            'content': 'Content of the new post'
        }, follow_redirects=True)
        self.assertIn('New Post', response.get_data(as_text=True))

    def test_post_detail(self):
        """Test viewing in a post."""
        response = self.client.get('/posts/1')
        self.assertIn('This is a test post', response.get_data(as_text=True))

    def test_edit_post(self):
        """Test editing a post."""
        response = self.client.post('/posts/1/edit', data={
            'title': 'Updated Post',
            'content': 'Updated content'
        }, follow_redirects=True)
        self.assertIn('Updated Post', response.get_data(as_text=True))

    def test_delete_post(self):
        """Test deleting a post."""
        response = self.client.post('/posts/1/delete', follow_redirects=True)
        self.assertNotIn('Test Post', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()