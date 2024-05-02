from flask import Flask, render_template, redirect, request, url_for
from models import db, User, Post

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        """From main page, redirect to users list."""
        return redirect(url_for('show_users'))

    @app.route('/users')
    def show_users():
        """Show list of users."""
        users = User.query.all()
        return render_template('user_list.html', users=users)

    @app.route('/users/new', methods=['GET'])
    def show_add_user_form():
        """Show the form to create a new user."""
        return render_template('add_user.html')

    @app.route('/users/new', methods=['POST'])
    def add_user():
        """Create a new user through form."""
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('show_users'))

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        """Show the selected user."""
        user = User.query.get_or_404(user_id)
        return render_template('user_detail.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
    def edit_user(user_id):
        """Options to edit user information, including name and image."""
        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.image_url = request.form['image_url']
            db.session.commit()
            return redirect(url_for('show_user', user_id=user_id))
        return render_template('edit_user.html', user=user)

    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    def delete_user(user_id):
        """Option to delete current user."""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('show_users'))
    
    @app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
    def add_post(user_id):
        """Form to add a new post."""
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_post = Post(title=title, content=content, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('show_user', user_id=user_id))
        return render_template('add_post.html', user_id=user_id)
        
    @app.route('/posts/<int:post_id>')
    def show_post(post_id):
        """Show created post."""
        post = Post.query.get_or_404(post_id)
        return render_template('post_detail.html', post=post)
    
    @app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
    def edit_post(post_id):
        """Edit a post that already exists."""
        post = Post.query.get_or_404(post_id)
        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))
        return render_template('edit_post.html', post=post)
        
    @app.route('/posts/<int:post_id>/delete', methods=['POST'])
    def delete_post(post_id):
        """Delete a post."""
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('show_users'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)