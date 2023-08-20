from flask import Flask

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Ruta de inicio (página principal)
@app.route('/')
def home():
    return "¡Bienvenido a mi aplicación Flask!"

if __name__ == '__main__':
    app.run()
