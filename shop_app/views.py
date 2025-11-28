import flask, os, flask_login, math
from .models import *

def creat_pagination_buttons(count_page: int, curent_page: int) -> list:
    if count_page <= 7:
        return list(range(1, count_page + 1 ))
    else:
        numbers = [1]
        if curent_page >= 4:
            numbers.append("...")
        start = min(max(curent_page - 2, 2), count_page - 5)
        for i in range(5):
            numbers.append(start + i)
        if curent_page <= count_page - 4:
            numbers.append("...")
        numbers.append(count_page)
        return numbers

def check_admin() -> bool:
    if flask_login.current_user.is_authenticated and flask_login.current_user.is_admin:
        return True
    return False

PRODUCT_IN_PAGE = 4

def render_catalog():
    page_num = int(flask.request.args.get('page', 1))
    is_admin = check_admin()
    if flask.request.method == "POST" and is_admin:
        new_product = Product(
            name = flask.request.form.get("name"),
            price = flask.request.form.get("price"),
            description = flask.request.form.get("description"),
            count = flask.request.form.get("count"),
            discount = flask.request.form.get("discount"),
        )
        
        DB.session.add(new_product)
        DB.session.commit()
        image = flask.request.files.get('image')
        image.save(
            dst = os.path.abspath(os.path.join(__file__, '..', 'static', 'images', "products", f'{new_product.id}.png'))
        )
    all_products = Product.query.paginate(
        page = page_num, 
        per_page= PRODUCT_IN_PAGE
    )
    count_page = math.ceil(all_products.total/PRODUCT_IN_PAGE) 
    return flask.render_template(
        "catalog.html", 
        admin = is_admin, 
        products = all_products, 
        page=page_num,
        count_page=count_page,
        pagination = creat_pagination_buttons(count_page, page_num)
    )


def delete(id: int):
    if check_admin():
        product = Product.query.get(id)
        if product:
            DB.session.delete(product)
            DB.session.commit()
            image_path = os.path.abspath(os.path.join(__file__, '..', 'static', 'images', "products", f'{id}.png'))
            os.remove(image_path)
    return flask.redirect('/catalog')

def render_change(id: int):
    if check_admin():
        product = Product.query.get(id)
        # Модель.query.get(id) - отримує запис з моделі (БД) за id
        if flask.request.method == "POST":
            product.name = flask.request.form.get("name")
            product.price = flask.request.form.get("price")
            product.count = flask.request.form.get("count")
            product.discount = flask.request.form.get("discount")
            product.description = flask.request.form.get("description")
            DB.session.commit()
            image = flask.request.files.get('image')
            if image:
                image.save(
                    dst = os.path.abspath(os.path.join(__file__, '..', 'static', 'images', "products", f'{product.id}.png'))
                )
            return flask.redirect('/catalog')
        return flask.render_template("change.html", product = product)
        
def buy(id: int):
    product = Product.query.get(id)
    response = flask.make_response(flask.redirect('/catalog'))
    # flask.make_response - функція яка створює відповідь користувачу ( для змінення його cookie ). 
    # В дужках потрібно redirect або render_template
    
    # flask.request.cookies.get('назва') - отримує cookie
    # response.set_cookie('назва', 'значення') - вказує cookie
    if product:
        products = flask.request.cookies.get('list_products')
        if products:
            response.set_cookie('list_products', products + "|" + str(id))
        else:
            response.set_cookie('list_products', str(id))
    return response