from flask import Flask
from flask_smorest import Api

from resources.products import blueprint as products_blueprint
from resources.orders import blueprint as orders_blueprint


app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'Products API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/api/docs'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_VERSION'] = '3.25.2'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'



api = Api(app)
api.register_blueprint(products_blueprint)
api.register_blueprint(orders_blueprint)



if __name__ == '__main__':
    app.run()