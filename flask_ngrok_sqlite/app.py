import json
import logging
import os
import sqlite3
import threading
from logging import config

from flask import Flask, g, jsonify, request
from pyngrok import ngrok
from werkzeug.serving import run_simple

from config.logging_config import LOGGING_CONFIG


class CreateApp():
    ana_js = None

    def __init__(self, dbname: str, on_colab: bool = False) -> None:
        os.environ["FLASK_DEBUG"] = "development"

        app = Flask(__name__)
        # logging設定
        config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger()

        def get_db():
            # データベースを開いてFlaskのグローバル変数に保存する
            if 'db' not in g:
                g.db = sqlite3.connect(dbname)
            return g.db

        # Open a ngrok tunnel to the HTTP server
        port = 8888  # ポート番号
        self.public_url = ngrok.connect(port).public_url
        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(
            self.public_url, port))

        # Update any base URLs to use the public ngrok URL
        app.config["BASE_URL"] = self.public_url
        app.config["ENV"] = "development"
        app.config['JSON_AS_ASCII'] = False  # JSON日本語文字化け対策
        # .. Update inbound traffic via APIs to use the public-facing ngrok URL

        # Define Flask routes
        @app.route("/", methods=['GET'])
        def index():
            return "Web App with Python Flask!"

        # Start the Flask server in a new thread
        if on_colab is False:
            threading.Thread(
                target=lambda: run_simple('localhost', port, app)).start()
        else:
            # on Colab, you can use the following code instead of the above
            # line
            threading.Thread(
                target=app.run, kwargs={"use_reloader": False}).start()

        @app.route('/receiver', methods=['POST'])
        def get_json():
            js = request.get_json()
            if js is not None:  # JSONが送られてきた場合、DB & ローカルに保存
                # logger.error('ERROR')
                self.ana_js = js  # class変数に保存
                with open(f'./result/{js["metadata"]["pdf_name"]}.json',
                          'w') as f:
                    json.dump(js, f, indent=4)
                # DBに保存
                con = get_db()  # DB接続
                cur = con.cursor()
                sql = 'INSERT INTO api_result (id, status, result, ' +\
                    'message, metadata) values (?,?,?,?,?)'
                data = [js['id'], js['status'], json.dumps(js['result']),
                        js['message'], json.dumps(js['metadata'])]

                cur.execute(sql, data)
                con.commit()
                con.close()
                # cur.close()
            return jsonify(js)

    def receive(self) -> dict:
        while True:
            if self.ana_js is not None:
                return self.ana_js
            else:
                continue
