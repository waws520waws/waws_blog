from flask import Blueprint, render_template, request, redirect
from flask import Response, Flask

blog_blueprint = Blueprint('blog', __name__)
from . import mysql_
from waws_app.utils.tools import get_category_list, get_article_limit_20, get_article_info, get_category_article, \
    get_prefect_url, get_article_by_time, get_article_by_click, get_article_by_like, get_cate_article_list, \
    get_cate_article_data_structure, get_article_guess_you_like, get_tag_random_10, get_article_list_limit_6, \
    update_like_count, get_statistics, update_view_count, get_category_article_list,get_previous_and_next_article

numberperpage = 20


@blog_blueprint.route("/")
def get_index():
    guess_list = get_article_guess_you_like(mysql_)
    art_list = get_cate_article_data_structure(mysql_)
    cate_articlelist = get_cate_article_list(mysql_)
    click_list, first_click_dict = get_article_by_click(mysql_)
    like_list, first_like_dict = get_article_by_like(mysql_)
    category_list = get_category_list(mysql_)
    page = request.args.get("page")
    sticky_list, article_list, page_previous, page_next = get_article_limit_20(page, mysql_)
    return render_template("./blog/index.html", sticky_list=sticky_list, article_list=article_list,
                           category_list=category_list, page_next=page_next, page_previous=page_previous,
                           click_list=click_list, first_click_dict=first_click_dict, like_list=like_list,
                           first_like_dict=first_like_dict, cate_articlelist=cate_articlelist,
                           art_list=art_list, guess_list=guess_list)


@blog_blueprint.route("/daohang")
def get_daohang():
    category_list = get_category_list(mysql_)
    url_prefect_dict = get_prefect_url(mysql_)
    return render_template("./blog/daohang.html", category_list=category_list, url_prefect_dict=url_prefect_dict)


@blog_blueprint.route("/info")
def get_info():
    guess_list = get_article_guess_you_like(mysql_)
    click_list, first_click_dict = get_article_by_click(mysql_)
    like_list, first_like_dict = get_article_by_like(mysql_)
    category_list = get_category_list(mysql_)
    article_id = request.args.get("article_id")
    previous,next = get_previous_and_next_article(mysql_,article_id)
    article_dict = get_article_info(article_id, mysql_)
    category_id = article_dict["category_id"]
    category_article_list = get_category_article_list(mysql_, category_id)
    update_view_count(mysql_, article_id)
    like_count, view_count = get_statistics(mysql_, article_id)
    return render_template("./blog/info.html", article_dict=article_dict, category_list=category_list,
                           click_list=click_list,
                           first_click_dict=first_click_dict, like_list=like_list, first_like_dict=first_like_dict,
                           guess_list=guess_list, like_count=like_count, view_count=view_count,article_id=article_id,
                           category_article_list=category_article_list,previous=previous,next=next)


@blog_blueprint.route("/add_like")
def add_like():
    ip = request.remote_addr
    article_id = request.args.get("article_id")
    like = update_like_count(mysql_, ip, article_id)
    return redirect("/info?article_id={}".format(article_id))


@blog_blueprint.route("/about")
def get_about():
    category_list = get_category_list(mysql_)
    return render_template("./blog/about.html", category_list=category_list)


@blog_blueprint.route("/list")
def get_list():
    tag_list = get_tag_random_10(mysql_)
    guess_list = get_article_guess_you_like(mysql_)
    click_list, first_click_dict = get_article_by_click(mysql_)
    like_list, first_like_dict = get_article_by_like(mysql_)
    category_list = get_category_list(mysql_)
    page = request.args.get("page", None)
    sticky_list, article_list, page_previous, page_next = get_article_limit_20(page, mysql_)
    return render_template("./blog/list.html", sticky_list=sticky_list, article_list=article_list,
                           category_list=category_list, page_next=page_next, page_previous=page_previous,
                           click_list=click_list, first_click_dict=first_click_dict, like_list=like_list,
                           first_like_dict=first_like_dict, guess_list=guess_list, tag_list=tag_list)


@blog_blueprint.route("/list2")
def get_list2():
    tag_list = get_tag_random_10(mysql_)
    guess_list = get_article_guess_you_like(mysql_)
    click_list, first_click_dict = get_article_by_click(mysql_)
    like_list, first_like_dict = get_article_by_like(mysql_)
    category_list = get_category_list(mysql_)
    category_id = request.args.get("category_id", None)
    if category_id is None or category_id == "None":
        page = request.args.get("page", None)
        sticky_list, article_list, page_next, page_previous = get_article_limit_20(page, mysql_)
    else:
        page = request.args.get("page", None)
        sticky_list, article_list, page_previous, page_next = get_category_article(page, category_id, mysql_)
    return render_template("./blog/list2.html", category_list=category_list, sticky_list=sticky_list,
                           article_list=article_list, page_next=page_next, page_previous=page_previous,
                           category_id=category_id, click_list=click_list, first_click_dict=first_click_dict
                           , like_list=like_list, first_like_dict=first_like_dict, guess_list=guess_list,
                           tag_list=tag_list)


@blog_blueprint.route("/list3")
def get_list3():
    tag_list = get_tag_random_10(mysql_)
    guess_list = get_article_guess_you_like(mysql_)
    click_list, first_click_dict = get_article_by_click(mysql_)
    like_list, first_like_dict = get_article_by_like(mysql_)
    category_list = get_category_list(mysql_)
    article_dict = {}
    for category_id in [1, 2, 3, 4]:
        article_list = get_article_list_limit_6(mysql_, category_id)
        if category_id == 1:
            article_dict["python基础"] = article_list
        elif category_id == 2:
            article_dict["深度学习"] = article_list
        elif category_id == 3:
            article_dict["机器学习"] = article_list
        else:
            article_dict["爬虫"] = article_list
    return render_template("./blog/list3.html", category_list=category_list, click_list=click_list,
                           first_click_dict=first_click_dict, like_list=like_list,
                           first_like_dict=first_like_dict, guess_list=guess_list, tag_list=tag_list,
                           article_dict=article_dict)


@blog_blueprint.route("/time")
def get_time():
    category_list = get_category_list(mysql_)
    page = request.args.get("page", None)
    article_list = get_article_by_time(page, mysql_)
    return render_template("./blog/time.html", category_list=category_list, article_list=article_list)
