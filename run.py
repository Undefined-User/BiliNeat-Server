from flask import Flask, make_response

app = Flask(__name__)


@app.route('/bilineat/version')
def newest_version():
    response = make_response('1.9.4')
    response.headers['Content-Type'] = 'text/html;charset=utf-8'
    return response


if __name__ == '__main__':
    app.run()
