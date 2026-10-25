from flask import Flask, render_template
from data import TEAM, PROJECTS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS)

@app.route('/project/connect')
def project_connect():
    # Вставили твою реальную ссылку на Render
    app_link = "https://connect-z2kl.onrender.com" 
    return render_template('project_connect.html', app_link=app_link)

@app.route('/team')
def team():
    return render_template('team.html', team=TEAM)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/wip')
def wip():
    return render_template('wip.html')

if __name__ == '__main__':
    app.run(port=5005, debug=True)