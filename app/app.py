from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from services.knight import find_steps_to_target

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'Article {self.id}'


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('posts-detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'There was an issue deleting your article'


# http://localhost:5000/knight/steps/3/4
@app.route('/knight/steps/<int:target_x>/<int:target_y>')
def knight_steps(target_x, target_y):
    steps = find_steps_to_target(target_x, target_y)
    return f'Steps of Knight to target ({target_x}, {target_y}): {steps}'


# http://localhost:5000/user/John/123
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'Hello, {name}, your id is {id}!'


# http://localhost:5000/create-article
@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def post_update(id):
    article = Article.query.get(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'There was an issue updating your article'
    else:
        return render_template('post-update.html', article=article)


# http://localhost:5000/create-article
@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title=title, content=content)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
            # return f'Article "{title}" created successfully!'
        except:
            return 'There was an issue adding your article'
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    app.run()
