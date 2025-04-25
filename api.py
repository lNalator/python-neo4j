from flask import Flask
from controllers.users_controller import users_bp
from controllers.posts_controller import posts_bp
from controllers.comments_controller import comments_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(comments_bp, url_prefix='/comments')

if __name__ == '__main__':
    app.run(debug=True)
