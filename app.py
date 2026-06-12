from flask import Flask
from db import init_db,seed_food
from routes.user_routes import user_bp
from routes.food_routes import food_bp
from routes.restaurant_routes import restaurant_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.analytics_routes import analytics_bp

app=Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(food_bp)
app.register_blueprint(restaurant_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(analytics_bp)


init_db()
seed_food()
print(app.url_map)
if __name__=="__main__":
    app.run(debug=True)