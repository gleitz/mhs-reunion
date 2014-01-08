from flask import Flask, request, render_template, url_for

from flaskutil import ReverseProxied

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

@app.route('/')
def home():
    return render_template('base.html',
                           favicon_url = url_for('static', filename='favicon.ico'),
                           style_url = url_for('static', filename='style.css'),
                           wallpaper_url = url_for('static', filename='wallpaper.jpg'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
