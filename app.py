from flask import Flask, render_template
from flask_apscheduler import APScheduler
from iso import get_iso
from votes import get_votecount, get_vote_history
from threading import Thread

from custom_types import Post
import re

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def replace(match):
        playername = match.group(1)
        url = match.group(2)
        return f'<a href="{url}">{playername}</a>'

@app.route('/')
def home():
    return("I'm alive!")

# Set up endpoint for votecount
@app.route('/<game>/votecount')
def vc(game):
    temp_vc = get_votecount(game, 100000)
    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    vc = re.sub(pattern, replace, temp_vc)
    vc = vc.replace("\n", "<br>")
    vc = vc.replace("**", "")
    vc = vc.replace("as of post 100000", "Most recent")
    return render_template('votecount.html', votecount=vc)

# Set up endpoint for retrospective votecount
@app.route('/<game>/votecount/<postnum>')
def past_vc(game, postnum):
    temp_vc = get_votecount(game, int(postnum))
    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    vc = re.sub(pattern, replace, temp_vc)
    vc = vc.replace("\n", "<br>")
    vc = vc.replace("**", "")
    return render_template('votecount.html', votecount=vc)

# Set up endpoint for vote history
@app.route('/<game>/votes')
def history(game):
    history = get_vote_history(game)
    return render_template('votehistory.html', history=history)

# Set up endpoint for targeted ISO
@app.route('/<game>/iso/<target>')
def iso(game, target):
    # take target, append it to a list of targets containing only that target
    targets = [target.lower()]
    posts = get_iso(targets, game)
    articles = []
    for post in posts:
        articles.append(post.HTML)

    return render_template('iso.html', posts=articles)

if __name__ == '__main__':
    app.run()
