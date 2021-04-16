from flask import Blueprint, render_template, request, redirect, url_for, url_for, send_from_directory,session
from flask import Response, Flask
from waws_app.utils import tools

admin_blueprint = Blueprint('admin', __name__)
from flask_ckeditor import upload_fail, upload_success
import os
from waws_app.utils.tools import get_admin_article_list_limit_10,get_article_info,delete_article_by_id,restore_article_by_id
from . import PostForm
from . import mysql_
import time

basedir = "/static/uploads/images"

url_category_dict = {
    1:"深度学习",
    2:"前端&后端",
    3:"CV&NLP",
    4:"爬虫",
    5:"官网",
    6:"其他"
}

@admin_blueprint.before_request
def check_login():
    if request.path == '/admin/login':
        return None
    username = session.get('username')
    password = session.get('password')
    if not username or not password:
        if request.path == '/login':
            result = login()
            if result:
                return render_template("./admin/index.html")
            else:
                return render_template("./admin/error.html")
        else:
            return redirect('/admin/login')
    if username == "waws520" and password == "709103wei":
        return None
    else:
        return redirect('/admin/login')


@admin_blueprint.route("/admin")
def get_admin():
    return render_template("./admin/index.html")


@admin_blueprint.route("/admin/artile_list")
def get_buttons():
    page = request.args.get("page")
    article_dict,page_previous,page_next = get_admin_article_list_limit_10(page, mysql_)
    return render_template("./admin/artile_list.html",article_dict=article_dict,page_previous=page_previous,page_next=page_next)


@admin_blueprint.route("/admin/power_set")
def get_rabc():
    return render_template("./admin/power_set.html")

@admin_blueprint.route("/admin/delete")
def detele_article():
    article_id = request.args.get("article_id")
    delete_article_by_id(article_id, mysql_)
    return redirect("/admin/doc")


@admin_blueprint.route("/admin/restore")
def restore_article():
    article_id = request.args.get("article_id")
    restore_article_by_id(article_id, mysql_)
    return redirect("/admin/doc")


@admin_blueprint.route("/admin/profile")
def get_prefile():
    return render_template("./admin/profile.html")


@admin_blueprint.route("/admin/login")
def get_login():
    return render_template("./admin/login.html")


@admin_blueprint.route("/admin/gallery")
def get_gallery():
    return render_template("./admin/gallery.html")

@admin_blueprint.route("/admin/article_detail")
def get_article_detail():
    article_id = request.args.get("article_id")
    article_dict = get_article_info(article_id,mysql_)
    return render_template("./admin/article_detail.html",article_dict=article_dict)


@admin_blueprint.route("/admin/edit_pwd")
def get_pwd():
    return render_template("./admin/edit_pwd.html")

@admin_blueprint.route("/admin/modify_pwd",methods=['POST'])
def modify_pwd():
    oldpwd = request.form.get("oldpwd")
    newpwd = request.form.get("newpwd")
    confirmpwd = request.form.get("confirmpwd")
    if newpwd != confirmpwd:
        return render_template("./admin/error.html",message="两次密码不一致，修改失败")
    sql = "select password from author where id = 1"
    mysql_.cursor.execute(sql)
    password = mysql_.cursor.fetchone()[0]
    if oldpwd != password:
        return render_template("./admin/error.html", message="旧密码输入错误，修改失败")
    else:
        session['username'] = False
        session['password'] = False
        sql = "update author set password= %s where id = 1"
        mysql_.cursor.execute(sql,[newpwd])
        mysql_.conn.commit()
        return redirect("/admin/login")


@admin_blueprint.route("/admin/doc")
def get_doc():
    page = request.args.get("page")
    article_dict,page_previous,page_next = get_admin_article_list_limit_10(page, mysql_)
    return render_template("./admin/doc.html",article_dict=article_dict,page_previous=page_previous,page_next=page_next)


@admin_blueprint.route("/admin/add_prefect_url")
def add_prefect_url():
    category_list = [{"id":key,"doc":value}for key,value in url_category_dict.items()]
    return render_template("./admin/add_prefect_url.html",category_list=category_list)


@admin_blueprint.route("/admin/add_prefect_url_action",methods=['GET', 'POST'])
def add_prefect_url_action():
    type = request.form.get("type")
    name = request.form.get("name")
    url = request.form.get("url")
    sql = "insert into prefect_blog_url(name,url,category) VALUES(%s,%s,%s)"
    mysql_.cursor.execute(sql,[name,url,type])
    mysql_.conn.commit()
    return render_template("./admin/index.html")


@admin_blueprint.route('/admin/add_doc', methods=['GET', 'POST'])
def index():
    sql = "select id,category from category"
    category_list = []
    mysql_.cursor.execute(sql, )
    category_ = mysql_.cursor.fetchall()
    for category in category_:
        category_list.append({"id": category[0], "doc": category[1]})

    sql = "select id,name from author"
    author_list = []
    mysql_.cursor.execute(sql, )
    author_ = mysql_.cursor.fetchall()
    for author in author_:
        author_list.append({"id": author[0], "name": author[1]})
    form = PostForm()
    return render_template('./admin/add_doc.html', form=form, category_list=category_list, author_list=author_list)


@admin_blueprint.route("/login", methods={"POST"})
def login():
    username_ = session.get('username')
    password_ = session.get('password')
    if username_ == "waws520" and password_ == "709103wei":
        return redirect("/admin")
    username = request.form.get("username")
    password = request.form.get("password")
    captcha = request.form.get("captcha")
    sql = "select password from author where id = 1"
    mysql_.cursor.execute(sql)
    pwd = mysql_.cursor.fetchone()[0]
    if username == "waws520" and password == pwd:
        session['username'] = "waws520"
        session['password'] = "709103wei"
        return True
    return False


@admin_blueprint.route("/admin/add_article", methods={"POST"})
def add_article():
    form = PostForm()
    type = request.form.get("type")
    author = request.form.get("author")
    title = request.form.get("title")
    seo_keywords = request.form.get("seo_keywords")
    tags = request.form.get("tags")
    tag_list = tags.split(",")
    f = request.files.get('file')
    pic_id = 0
    if f.filename.split(".")[-1] != "":
        print(f.filename.split(".")[-1])
        filename = tools.create_uuid() + "." + f.filename.split(".")[-1]
        file_sql_path = os.path.join(basedir, filename)
        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/static/uploads/images/" + filename
        f.save(file_path)

        sql = "insert into picture(pic_url) values(%s)"
        mysql_.cursor.execute(sql, [file_sql_path])
        mysql_.conn.commit()
        pic_id = mysql_.cursor.lastrowid

    if form.validate_on_submit():
        body = form.body.data
        if pic_id:
            sql = "insert into article(title,author_id,info,content,category_id,pic_id) values(%s,%s,%s,%s,%s,%s)"
            mysql_.cursor.execute(sql, [title, author, seo_keywords, body, type, pic_id])
        else:
            sql = "insert into article(title,author_id,info,content,category_id) values(%s,%s,%s,%s,%s)"
            mysql_.cursor.execute(sql, [title, author, seo_keywords, body, type])
        last_id = mysql_.cursor.lastrowid
        sql = "insert into statistics(article_id) value(%s)"
        mysql_.cursor.execute(sql, [last_id,])
        for tag in tag_list:
            sql = "insert into tag(name,article_id) value(%s,%s)"
            mysql_.cursor.execute(sql, [tag,last_id])
        mysql_.conn.commit()
        return render_template("./admin/index.html")
    else:
        return render_template("./admin/error.html")


@admin_blueprint.route('/static/uploads/images_/<filename>')
def uploaded_files(filename):
    path = os.path.join(basedir, filename)
    return send_from_directory(path, filename)


@admin_blueprint.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    filename = tools.create_uuid() + "." + f.filename.split(".")[-1]
    file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/static/uploads/images_/" + filename
    f.save(file_path)
    time.sleep(2)
    url = url_for('admin.uploaded_files', filename=filename)
    return upload_success(url=url)
