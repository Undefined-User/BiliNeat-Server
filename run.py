import configparser
import os

from flask import Flask, request, make_response

from config import Config

app = Flask(__name__)
app.config.from_object(Config())


def get_content(version):
    # 版本号都是没有还查个毛线
    if version is None:
        return None

    static_folder = str(app.static_folder)
    filename = 'adapter_' + version + '.cfg'
    listdir = os.listdir(static_folder)

    if filename in listdir:
        # 有适配文件
        parser = configparser.ConfigParser()
        parser.read(os.path.join(static_folder, filename), encoding='utf-8')

        list_content = parser.items(app.config['ADAPTER_FILE_SECTIONS'])
        return dict(list_content)


def make_json(content):
    pass


@app.route('/bilineat/version')
def newest_version():
    response = make_response(app.config['BILINEAT_NEWEST_VERSION'])
    response.headers['Content-Type'] = 'text/html;charset=utf-8'
    return response


@app.route('/bilineat/adapterfile')
def get_adapter_file():
    bili_version = request.args.get('bili')
    dict_content = get_content(bili_version)
    make_json(dict_content)

    return '111111111111'


if __name__ == '__main__':
    app.run()
