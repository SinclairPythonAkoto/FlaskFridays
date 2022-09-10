from flask.views import MethodView
from ..extension import app


class HelloWorld(MethodView):
    def get(self):
        return 'Hello world!'


app.add_url_rule('/', view_func=HelloWorld.as_view(name='hello_world'))