from flask import Flask, render_template, redirect, request, url_for
from models import db, User, Post, Tag

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
        """Redirect from main page to users list."""
        return redirect(url_for('show_users'))

    @app.route('/users')
    def show_users():
        """Show list of users."""
        users = User.query.all()
        return render_template('user_list.html', users=users)

    @app.route('/users/new', methods=['GET', 'POST'])
    def show_add_user_form():
        """Show form or handle creating a new user."""
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            image_url = request.form['image_url'] or None

            new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('show_users'))
        return render_template('add_user.html')

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        """Show the selected user."""
        user = User.query.get_or_404(user_id)
        return render_template('user_detail.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
    def edit_user(user_id):
        """Show form or handle editing user information."""
        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.image_url = request.form['image_url'] or user.image_url
            db.session.commit()
            return redirect(url_for('show_user', user_id=user_id))
        return render_template('edit_user.html', user=user)

    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    def delete_user(user_id):
        """Delete the current user."""
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
        """Show details of a created post."""
        post = Post.query.get_or_404(post_id)
        return render_template('post_detail.html', post=post)
    
    @app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
    def edit_post(post_id):
        """Show form or handle editing a post."""
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
    
    @app.route('/tags')
    def list_tags():
        """List all created tags."""
        tags = Tag.query.all()
        return render_template('list_tags.html', tags=tags)

    @app.route('/tags/new', methods=['GET', 'POST'])
    def add_tag():
        """Show form or handle adding a new tag."""
        if request.method == 'POST':
            name = request.form['name']
            new_tag = Tag(name=name)
            db.session.add(new_tag)
            db.session.commit()
            return redirect(url_for('list_tags'))
        return render_template('add_tag.html')
    
    @app.route('/tags/<int:tag_id>')
    def show_tag(tag_id):
        """Show details of a created tag."""
        tag = Tag.query.get_or_404(tag_id)
        return render_template('show_tag.html', tag=tag)
    
    @app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
    def edit_tag(tag_id):
        """Show form or handle editing a tag."""
        tag = Tag.query.get_or_404(tag_id)
        if request.method == 'POST':
            tag.name = request.form['name']
            db.session.commit()
            return redirect(url_for('show_tag', tag_id=tag_id))
        return render_template('edit_tag.html', tag=tag)
    
    @app.route('/tags/<int:tag_id>/delete', methods=['POST'])
    def delete_tag(tag_id):
        """Delete a tag."""
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return redirect(url_for('list_tags'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
