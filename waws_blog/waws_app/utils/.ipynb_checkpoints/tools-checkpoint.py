import random
import datetime

url_category_dict = {
    1: "深度学习",
    2: "前端&后端",
    3: "CV&NLP",
    4: "爬虫",
    5: "官网",
    6: "其他"
}


def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


def get_category_list(mysql_):
    sql = "select id,category from category"
    category_list = []
    mysql_.cursor.execute(sql, )
    category_ = mysql_.cursor.fetchall()
    for category in category_:
        category_list.append({"id": category[0], "doc": category[1]})
    return category_list


def get_page_next_previous(count,page,every_page_count):
    page_next = 1
    page_previous = 1
    if count % every_page_count != 0:
        page_all = count//every_page_count + 1
    else:
        page_all = count//every_page_count
    if page <= 1:
        if page_all == 1:
            page_next = 1
            page_previous = 1
        else:
            page_next = 2
            page_previous = 1
    elif page < page_all:
        page_next = page + 1
        page_previous = page -1
    elif page >= page_all:
        page_next = page_all
        page_previous = page - 1
    return page_previous,page_next


def get_article_limit_20(page, mysql_):
    every_page_count = 10
    if page is None:
        page = 1
    else:
        page = int(page)
    sql = "select count(*) from article"
    mysql_.cursor.execute(sql,)
    count = mysql_.cursor.fetchone()[0]
    page_previous,page_next = get_page_next_previous(count,page,every_page_count)

    id_ = (int(page) - 1) * every_page_count
    sticky_list = []
    article_list = []
    sql = "select * from article limit 10 offset %s"
    mysql_.cursor.execute(sql, [id_])
    results = mysql_.cursor.fetchall()
    for result in results:
        id = result[0]
        title = result[1]
        author_id = result[2]
        info = result[3]
        category_id = result[5]
        pic_id = result[6]
        sticky = result[8]
        create_time = result[9]

        sql = "select name from author where id = %s"
        mysql_.cursor.execute(sql, [author_id])
        name = mysql_.cursor.fetchone()[0]

        sql = "select category from category where id = %s"
        mysql_.cursor.execute(sql, [category_id])
        category = mysql_.cursor.fetchone()[0]

        pic_url = ""
        if pic_id:
            sql = "select pic_url from picture where id = %s"
            mysql_.cursor.execute(sql, [pic_id])
            pic_url = mysql_.cursor.fetchone()[0]

        if sticky:
            sticky_list.append({
                "id": id,
                "style": 1,
                "title": title,
                "author": name,
                "info": info,
                "date": create_time,
                "category": category,
                "pics": []
            })
        else:
            if pic_id:
                article_list.append({
                    "id": id,
                    "style": 1,
                    "title": title,
                    "author": name,
                    "info": info,
                    "date": create_time,
                    "category": category,
                    "pic": pic_url
                })
            else:
                article_list.append({
                    "id": id,
                    "style": 0,
                    "title": title,
                    "author": name,
                    "category": category,
                    "info": info,
                    "date": create_time,
                })
    return sticky_list, article_list,page_previous,page_next


def get_article_info(article_id, mysql_):
    sql = "select * from article where id = %s"
    mysql_.cursor.execute(sql, [int(article_id)])
    result = mysql_.cursor.fetchone()
    id = result[0]
    title = result[1]
    author_id = result[2]
    info = result[3]
    content = result[4]
    category_id = result[5]
    sticky = result[8]
    create_time = result[9]

    sql = "select name from author where id = %s"
    mysql_.cursor.execute(sql, [author_id])
    name = mysql_.cursor.fetchone()[0]

    sql = "select category from category where id = %s"
    mysql_.cursor.execute(sql, [category_id])
    category = mysql_.cursor.fetchone()[0]
    article_dict = {
        "id": id,
        "style": 1,
        "title": title,
        "author": name,
        "info": info,
        "content": content,
        "date": create_time,
        "category_id":category_id,
        "category": category,
    }
    return article_dict


def get_category_article(page, category_id, mysql_):
    every_page_count = 20
    if not category_id:
        category_id = 1
    if page is None:
        page = 1
    else:
        page = int(page)
    sql = "select count(*) from article where category_id=(%s)"
    mysql_.cursor.execute(sql,[category_id])
    count = mysql_.cursor.fetchone()[0]
    page_previous, page_next = get_page_next_previous(count, page, every_page_count)
    id_ = (int(page) - 1) * 20
    sticky_list = []
    article_list = []
    sql = "select category from category where id = %s"
    mysql_.cursor.execute(sql, [category_id])
    category = mysql_.cursor.fetchone()[0]

    sql = "select * from article where category_id = %s limit 20 offset %s"
    mysql_.cursor.execute(sql, [category_id, id_])
    results = mysql_.cursor.fetchall()
    for result in results:
        id = result[0]
        title = result[1]
        author_id = result[2]
        info = result[3]
        pic_id = result[6]
        sticky = result[8]
        create_time = result[9]

        sql = "select name from author where id = %s"
        mysql_.cursor.execute(sql, [author_id])
        name = mysql_.cursor.fetchone()[0]

        pic_url = ""
        if pic_id:
            sql = "select pic_url from picture where id = %s"
            mysql_.cursor.execute(sql, [pic_id])
            pic_url = mysql_.cursor.fetchone()[0]

        if sticky:
            sticky_list.append({
                "id": id,
                "style": 1,
                "title": title,
                "author": name,
                "info": info,
                "date": create_time,
                "category": category,
                "pics": []
            })
        else:
            if pic_id:
                article_list.append({
                    "id": id,
                    "style": 1,
                    "title": title,
                    "author": name,
                    "info": info,
                    "date": create_time,
                    "category": category,
                    "pic": pic_url
                })
            else:
                article_list.append({
                    "id": id,
                    "style": 0,
                    "title": title,
                    "author": name,
                    "category": category,
                    "info": info,
                    "date": create_time,
                })
    return sticky_list, article_list,page_previous,page_next


def get_prefect_url(mysql_):
    sql = "select url,name,category from prefect_blog_url"
    mysql_.cursor.execute(sql, )
    results = mysql_.cursor.fetchall()
    url_dict = {}
    for result in results:
        url, name, category = result[0], result[1], result[2]
        if url_category_dict[int(category)] not in url_dict.keys():
            url_dict[url_category_dict[int(category)]] = []
        url_dict[url_category_dict[int(category)]].append({"url": url, "name": name})
    return url_dict

def get_article_by_time(page,mysql_):
    if page is None:
        page = 1
    id_ = (int(page) - 1) * 30
    article_list = []
    sql = "select id,title,update_time from article order by update_time desc limit 20 offset %s "
    mysql_.cursor.execute(sql, [id_])
    results = mysql_.cursor.fetchall()
    for result in results:
        id = result[0]
        title = result[1]
        update_time = result[2]
        u_time = str(update_time.year) + "-" + str(update_time.month) + "-" + str(update_time.day)
        article_list.append({"id":id,"title":title,"update_time":u_time})
    return article_list

def get_admin_article_list_limit_10(page, mysql_):
    every_page_count = 10
    if page is None:
        page = 1
    else:
        page = int(page)
    sql = "select count(*) from article"
    mysql_.cursor.execute(sql, )
    count = mysql_.cursor.fetchone()[0]
    page_previous, page_next = get_page_next_previous(count, page, every_page_count)

    id_ = (int(page) - 1) * every_page_count
    article_list = []
    sql = "select * from article limit 10 offset %s"
    mysql_.cursor.execute(sql, [id_])
    results = mysql_.cursor.fetchall()
    for result in results:
        id = result[0]
        title = result[1]
        author_id = result[2]
        info = result[3]
        category_id = result[5]
        is_del = result[7]
        create_time = result[9]

        sql = "select name from author where id = %s"
        mysql_.cursor.execute(sql, [author_id])
        name = mysql_.cursor.fetchone()[0]

        sql = "select category from category where id = %s"
        mysql_.cursor.execute(sql, [category_id])
        category = mysql_.cursor.fetchone()[0]
        article_list.append({
            "id": id,
            "title": title,
            "author": name,
            "category": category,
            "info": info,
            "is_del":is_del,
            "date": create_time,
        })
    article_dict = {}
    for index,data in enumerate(article_list):
        article_dict[index] = data
    return article_dict,page_previous,page_next



def delete_article_by_id(article_id,mysql_):
    sql = "select is_delete from article where id = %s"
    mysql_.cursor.execute(sql, [article_id])
    is_delete = mysql_.cursor.fetchone()[0]
    if not is_delete:
        sql = "update article set is_delete = 1 where id = %s"
        mysql_.cursor.execute(sql, [article_id])
        mysql_.conn.commit()


def restore_article_by_id(article_id,mysql_):
    sql = "select is_delete from article where id = %s"
    mysql_.cursor.execute(sql, [article_id])
    is_delete = mysql_.cursor.fetchone()[0]
    if is_delete:
        sql = "update article set is_delete = 0 where id = %s"
        mysql_.cursor.execute(sql, [article_id])
        mysql_.conn.commit()

def get_article_by_click(mysql_):
    sql = "select a.id,a.title from article as a inner join statistics as s where a.id = s.article_id and a.is_delete = 0 ORDER BY s.view_count limit 9"
    mysql_.cursor.execute(sql,)
    article_list = mysql_.cursor.fetchall()
    result_list = []
    click_first_dict = {}
    for index,article in enumerate(article_list):
        id,title = article[0],article[1]
        if index == 0:
            click_first_dict = {"id":id,"title":title}
            continue
        result_list.append({"id":id,"title":title})
    return result_list,click_first_dict

def get_article_by_like(mysql_):
    sql = "select a.id,a.title from article as a inner join statistics as s where a.id = s.article_id and a.is_delete = 0 ORDER BY s.like_count limit 7"
    mysql_.cursor.execute(sql,)
    article_list = mysql_.cursor.fetchall()
    result_list = []
    like_first_dict = {}
    for index,article in enumerate(article_list):
        id,title = article[0],article[1]
        if index == 0:
            like_first_dict = {"id":id,"title":title}
            continue
        result_list.append({"id":id,"title":title})
    return result_list,like_first_dict


def get_cate_article_list(mysql_):
    category_id_list = [1,5,2,3,4]
    cate_articlelist = []
    for cate in  category_id_list:
        art_list = []
        sql = "select id,title,info from article where category_id = %s order by create_time DESC limit 7 "
        mysql_.cursor.execute(sql,[cate,])
        article_list = mysql_.cursor.fetchall()
        for article in article_list:
            art_list.append({"id":article[0],"title":article[1],"info":article[2]})
        cate_articlelist.append(art_list)
    return cate_articlelist

def get_cate_article_data_structure(mysql_):
    category_id = 1
    art_list = []
    sql = "select id,title,info from article where category_id = %s order by create_time DESC limit 6"
    mysql_.cursor.execute(sql,[category_id,])
    article_list = mysql_.cursor.fetchall()
    for article in article_list:
        art_list.append({"id":article[0],"title":article[1],"info":article[2]})

    return art_list

def get_article_guess_you_like(mysql_):
    sql = "select id from article"
    mysql_.cursor.execute(sql,)
    id_list = mysql_.cursor.fetchall()
    r_id_list = random.sample(id_list,8)
    art_list = []
    for r_id in r_id_list:
        sql = "select id,title from article where id = %s and is_delete = 0"
        try:
            mysql_.cursor.execute(sql, [r_id[0],])
        except:
            continue
        article = mysql_.cursor.fetchone()
        if article is None:
            continue
        else:
            art_list.append({"id":article[0],"title":article[1]})
    return art_list

def get_tag_random_10(mysql_):
    result = []
    sql = "select id,name from tag"
    mysql_.cursor.execute(sql, )
    id_list = mysql_.cursor.fetchall()
    if len(id_list) < 10:
        r_id_list = id_list
    else:
        r_id_list = random.sample(id_list, 10)
    for r_id in r_id_list:
        result.append({"id":r_id[0],"name":r_id[1]})
    return result

def get_article_list_limit_6(mysql_,category_id):
    result = []
    sql = "select id,title,info,pic_id from article where is_delete = 0 and category_id = %s limit 6"
    mysql_.cursor.execute(sql,[category_id,])
    article_list = mysql_.cursor.fetchall()
    for article in article_list:
        id = article[0]
        title = article[1]
        info = article[2]
        pic_id = article[3]
        if  pic_id:
            sql = "select pic_url from picture where id = %s"
            mysql_.cursor.execute(sql, [pic_id, ])
            pic_url = mysql_.cursor.fetchone()[0]
        else:
            index = random.randint(1,5)
            pic_url = "../../static/blog/images/" + str(index) +".jpg"
        result.append({"id":id,"title":title,"info":info,"pic_url":pic_url})
    return result

def update_like_count(mysql_,ip,article_id):
    sql = "select id from `like` where ip = %s and article_id = %s"
    mysql_.cursor.execute(sql, [ip,article_id])
    id = mysql_.cursor.fetchone()
    if id:
        return "liked"
    else:
        sql = "insert into `like`(article_id,ip) VALUES(%s,%s)"
        mysql_.cursor.execute(sql, [article_id,ip])
        sql = "select like_count from statistics where article_id = %s"
        mysql_.cursor.execute(sql, [article_id,])
        like = mysql_.cursor.fetchone()[0]
        sql = "update statistics set like_count = %s where article_id = %s"
        mysql_.cursor.execute(sql, [int(like) + 1, article_id])
        mysql_.conn.commit()
        return "liking"

def get_statistics(mysql_,article_id):
    sql = "select like_count,view_count from statistics where article_id = %s"
    mysql_.cursor.execute(sql, [article_id, ])
    data = mysql_.cursor.fetchone()
    like_count,view_count = data[0],data[1]
    return like_count,view_count

def update_view_count(mysql_,article_id):
    sql = "select view_count from statistics where article_id = %s"
    mysql_.cursor.execute(sql, [article_id, ])
    view = mysql_.cursor.fetchone()[0]
    sql = "update statistics set view_count = %s where article_id = %s"
    mysql_.cursor.execute(sql, [int(view) + 1, article_id])
    mysql_.conn.commit()

def get_category_article_list(mysql_,category_id):
    result = []
    sql = "select id,title from article where is_delete = 0 and category_id = %s limit 10"
    mysql_.cursor.execute(sql,[category_id,])
    article_list = mysql_.cursor.fetchall()
    for article in article_list:
        id = article[0]
        title = article[1]
        result.append({"id":id,"title":title})
    return result

def get_previous_and_next_article(mysql_,article_id):
    sql = "select create_time from article where id = %s"
    mysql_.cursor.execute(sql, [article_id, ])
    article_c_time = mysql_.cursor.fetchone()[0]
    sql = "select id,title from article where create_time > %s ORDER BY create_time limit 1"
    mysql_.cursor.execute(sql, [article_c_time, ])
    next_article = mysql_.cursor.fetchone()
    if next_article is not None:
        next_dict = {"id":next_article[0],"title":next_article[1]}
    else:
        next_dict = {"id":None,"title":"#@#"}
    sql = "select id,title from article where create_time < %s ORDER BY create_time DESC limit 1"
    mysql_.cursor.execute(sql, [article_c_time, ])
    pre_article = mysql_.cursor.fetchone()
    if pre_article:
        pre_dict = {"id":pre_article[0],"title":pre_article[1]}
    else:
        pre_dict = {"id":None,"title":"#@#"}
    return pre_dict,next_dict
