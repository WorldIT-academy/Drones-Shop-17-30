import home_app, shop_app

home_app.home.add_url_rule(rule = '/', view_func = home_app.render_home, methods = ["GET", "POST"])
home_app.home.add_url_rule(rule = '/reg', view_func = home_app.render_registation, methods = ["GET", "POST"])
home_app.home.add_url_rule(rule = '/login', view_func = home_app.render_login, methods = ["GET", "POST"])
home_app.home.add_url_rule(rule = '/logout', view_func = home_app.logout)

shop_app.shop_app.add_url_rule(rule = '/catalog', view_func = shop_app.render_catalog, methods = ["GET", "POST"])
shop_app.shop_app.add_url_rule(rule = '/delete/<int:id>', view_func = shop_app.delete, methods = ["GET"])
shop_app.shop_app.add_url_rule(rule = '/change/<int:id>', view_func = shop_app.render_change, methods = ["GET", "POST"])
shop_app.shop_app.add_url_rule(rule = '/buy/<int:id>', view_func = shop_app.buy, methods = ["GET"])
shop_app.shop_app.add_url_rule(rule = '/cart', view_func = shop_app.render_cart, methods = ["GET"])
# Path-параметри - обов'язкові параметри шляху (query-параметри не обов'язкові). 
# Для використання в urls "посилання/<int:назва>"
