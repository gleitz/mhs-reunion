from flask import Flask, request, render_template, url_for
import json
import os
import signal

from flaskutil import ReverseProxied

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

# Logger
import logging
logging.basicConfig()
log = logging.getLogger('mhs')

@app.route('/')
def home():
    return render_template('base.html',
                           favicon_url = url_for('static', filename='favicon.ico'),
                           style_url = url_for('static', filename='style.css'),
                           wallpaper_url = url_for('static', filename='wallpaper.jpg'))

@app.route('/fhqwhgads',methods=['POST'])
def github_hook():
    try:
        data = json.loads(request.form['payload'])
        site_url = 'https://github.com/gleitz/mhs-reunion'
        site_branch = 'master'
        data_url = data.get('repository', {}).get('url')
        data_branch = data.get('ref')
        log.error(data_url)
        log.error(data_branch)
        if data_url == site_url and site_branch in data_branch:
            log.error("Post-receive trigger. Exiting in 1 second")
            os.system('git pull')
            with open('/home/gleitz/projects/webapps/pid/mhs-reunion.pid', 'r') as f:
                pid = int(f.read())
                os.kill(pid, signal.SIGHUP)
    except ValueError:
        log.error("no object decoded")

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
