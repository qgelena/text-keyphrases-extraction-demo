#!/usr/bin/env python3
from flask import Flask
import flask
from database import Database
from keyphrases import KeywordsExtractor

app = Flask('ProphyTest')

@app.route('/')
def main_page():
    return flask.render_template('main.htm')

@app.route('/text', methods=['POST'])
def text_form():
    text = flask.request.form['text']
    text_id = app.db.save_text(text)
    keywords = app.extractor.get_keywords(text)
    app.db.save_keywords(text_id, keywords)
    url = flask.url_for('text_page', id=text_id)
    return flask.redirect(url)

@app.route('/text/<int:id>')
def text_page(id):
    text = app.db.get_text(id)
    keywords = app.extractor.get_keywords(text)
    
    return flask.render_template('text.htm',
        id=id,
        text=text,
        keyphrases=keywords
    )

if __name__ == '__main__':
    app.db = Database('ProphyTest.db')
    app.extractor = KeywordsExtractor()
    app.run(debug=True) #main loop of the server / event loop 