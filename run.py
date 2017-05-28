import configparser
import os

from flask import Flask, request, make_response, jsonify

from config import Config


class OriginalConfigParser(configparser.ConfigParser):
    """
    重写 optionxform() 解决 ConfigParser 不区分大小写，MDZZ... 
    """

    def __init__(self):
        configparser.ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr


app = Flask(__name__)
app.config.from_object(Config())


def get_content(version):
    static_folder = str(app.static_folder)
    filename = 'adapter_' + version + '.cfg'
    listdir = os.listdir(static_folder)

    if filename in listdir:
        # 有适配文件
        parser = OriginalConfigParser()
        parser.read(os.path.join(static_folder, filename), encoding='utf-8')

        list_content = parser.items(app.config['ADAPTER_FILE_SECTIONS'])
        return dict(list_content)


def get_not_found_response():
    json_dict = {'code': 404, 'message': 'Adapter file not found'}
    return jsonify(json_dict)


def add_json_header(agrs):
    response = make_response(agrs)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/bilineat/version')
def newest_version():
    file = open(os.path.join(app.static_folder, 'newest'))
    response = add_json_header(file.read())
    return response


@app.route('/bilineat/adapterfile')
def get_adapter_file():
    bili_version = request.args.get('bili')
    if bili_version is None:
        return get_not_found_response()

    content_dict = get_content(bili_version)

    if content_dict is None:
        return get_not_found_response()
    else:
        official_version = content_dict['officialVersion']
        # 移除原 dict 里的 key
        content_dict.pop('officialVersion')

        content_dict = {'code': 200, 'officialVersion': official_version, 'hook_info': content_dict}

        return jsonify(content_dict)


if __name__ == '__main__':
    app.run()
