from flask import current_app
import datetime
from flask_login import UserMixin
from flaskApp import login_manager, db



from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import psycopg2



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

book = db.Table('book',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

likes = db.Table('likes',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('upload_id', db.Integer, db.ForeignKey('upload.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    role = db.Column('role', db.Integer, default=0)
    sub_role = db.Column('sub role', db.Integer, default=1)
    fullname = db.Column('fullname', db.String(20))
    username = db.Column('username', db.String(20), unique=True, nullable=True)
    password = db.Column('password', db.String(60), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    id_type = db.Column('id_type', db.String(60), nullable=True)
    id_number = db.Column('id_number', db.String(), nullable=True)
    id_document = db.Column('id_document', db.String(60), nullable=True)
    nationality = db.Column('nationality', db.String(60), nullable=True)
    occupation = db.Column('occupation', db.String(60), nullable=True)
    email = db.Column('email', db.String(60), nullable=True,unique=True)
    province = db.Column('province', db.String(60), nullable=True)
    city = db.Column('city', db.String(60), nullable=True)
    phone = db.Column('phone', db.BIGINT(), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    uploads = db.relationship('Upload', backref='uploader', lazy=True)
    lesson = db.relationship('Lesson', backref=db.backref('user_lessons'))
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    book = db.relationship('Post', secondary=book,backref=db.backref('bookers', lazy='dynamic'))
    likes = db.relationship('Upload', secondary=likes,backref=db.backref('liked', lazy='dynamic'))


    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

    #   def book(self,post):
    #       if not self.booked(post):
    #           self.has_booked.append(post)
    #   def unbook(self,post):
    #       if self.has_booked(post):
    #           self.booked.remove(post)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    # is_admin = db.Column(db.Boolean,default=False)

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self, user_id, role, sub_role, fullname, username, password, image_file, id_type, id_number,
                 id_document, nationality, occupation, email, province, city, phone):
        self.user_id = user_id
        self.role = role
        self.sub_role = sub_role
        self.fullname = fullname
        self.username = username
        self.password = password
        self.image_file = image_file

        self.id_type = id_type
        self.id_number = id_number
        self.id_document = id_document
        self.nationality = nationality
        self.occupation = occupation
        self.email = email
        self.province = province
        self.city = city
        self.phone = phone


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column('id', db.Integer, primary_key=True)
    verified = db.Column('verified', db.Integer, default=0, nullable=True)
    title = db.Column('title', db.String(70), nullable=True)
    category = db.Column('category', db.String(10), nullable=True)
    description = db.Column('description', db.String(100), nullable=True)
    files = db.Column('file', db.String)
    date = db.Column('Date', db.String, nullable=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=True)
    start_time = db.Column("Start Time", db.String, nullable=True)
    end_time = db.Column('End time', db.String, nullable=True)
    lesson = db.relationship('Lesson', backref=db.backref('lessons'))

    def __repr__(self, id, verified, title, category, description, files, date, user_id, start_time,
                 end_time):
        self.id = id
        self.verified = verified
        self.title = title
        self.category = category
        self.files = files
        self.description = description
        self.date = date
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time


#

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(100), nullable=True)
    description = db.Column('description', db.String(100), nullable=True)
    post_id = db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self, id, title, description, post_id):
        self.id = id
        self.title = title
        self.description = description
        self.post_id = post_id


class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(30))
    category = db.Column('category', db.String(30))
    description = db.Column('description', db.String(600))
    price = db.Column('price', db.Integer)
    upload_ref = db.Column('upload_ref', db.VARCHAR)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='upload', lazy='dynamic')

    def __repr__(self, id, title, category, description, price, upload_ref, user_id):
        self.id = id
        self.title = title
        self.category = category
        self.description = description
        self.price = price
        self.upload_ref = upload_ref
        self.user_id = user_id


#

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Comment(db.Model):
   __tablename__ = 'comment'
   id = db.Column(db.Integer, primary_key=True)
   content = db.Column(db.Text)
   timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))

