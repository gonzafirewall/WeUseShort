from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
app.debug = True


app.config['SECRET_KEY'] = 'Si buscas resultados distintos, no hagas siempre lo mismo.'

from views import *


if __name__ == "__main__":
    app.run(debug=True)
