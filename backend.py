from flask import Flask


app = Flask('ProphyTest')

@app.route('/')
def main_page():
    return "Prophy Science Test App"

if __name__ == '__main__':
    app.run() 