import json
from pathlib import Path
from typing import Dict, Optional, Union

import requests
from yamawrapper import dev_utils as du


def send_data_to_api(pdf_path: Union[str, Path],
                     url: str, api_key: str,
                     webhook_url: Optional[str] = None,
                     metadata: Optional[Dict[str, str]] = None
                     ) -> Dict:
    """APIにデータを送信する関数

    Args:
        pdf_path (Union[str, Path]): pdfファイルのパス
        url (str): url
        api_key (str): api_key
        webhook_url (str, optional): webhook_url. Defaults to None.
        metadata (Dict[str, str], optional): metadata. Defaults to None.

    Returns:
        requests.Response: _description_
    """
    test_dict = create_post_json(
        pdf_path, webhook_url=webhook_url, metadata=metadata)
    # dictをjson文字列に変換
    js_str = json.dumps(test_dict).encode('utf-8')
    # postする
    response = requests.post(url, data=js_str, headers={'x-api-key': api_key})
    return json.loads(response.text)


def create_post_json(pdf_path: Union[str, Path],
                     output_path: Optional[Union[str, Path]] = None,
                     webhook_url: Optional[str] = None,
                     metadata: Optional[Dict[str, str]] = {"hoge": "test"}
                     ) -> Dict:
    """postするjsonを作成する関数

    Args:
        pdf_path (Union[str, Path]): pdfファイルのパス
        output_path (Union[str, Path]): 出力先のパス(jsonファイル)

    Returns:
        Dict: postするjson
    """
    # pdfをbyte型→base64エンコード
    plan = du.encode_to_str(open(pdf_path, "rb").read())
    data_dict = {}
    pdf_infos = du.create_plan_pix_plansize(pdf_path)
    data_dict['plan'] = plan
    # data_dict['plan'] = pdf_infos["plan"].replace('\n', '')
    data_dict['plan_size'] = pdf_infos['plan_size']
    data_dict['webhook_url'] = webhook_url
    data_dict["metadata"] = metadata
    if output_path:
        with open(output_path, "w") as f:  # indent=指定なし=改行なし
            json.dump(data_dict, f, indent=4)
    return data_dict

# class CreateApp():
#     ana_js = None

#     def __init__(self, dbname: str, on_colab: bool = False) -> None:
#         os.environ["FLASK_DEBUG"] = "development"

#         app = Flask(__name__)
#         # logging設定
#         config.dictConfig(LOGGING_CONFIG)
#         logger = logging.getLogger()

#         def get_db():
#             # データベースを開いてFlaskのグローバル変数に保存する
#             if 'db' not in g:
#                 g.db = sqlite3.connect(dbname)
#             return g.db

#         # Open a ngrok tunnel to the HTTP server
#         port = 8888  # ポート番号
#         self.public_url = ngrok.connect(port).public_url
#         print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(
#             self.public_url, port))

#         # Update any base URLs to use the public ngrok URL
#         app.config["BASE_URL"] = self.public_url
#         app.config["ENV"] = "development"
#         app.config['JSON_AS_ASCII'] = False  # JSON日本語文字化け対策
#         # .. Update inbound traffic via APIs to use the public-facing ngrok URL

#         # Define Flask routes
#         @app.route("/", methods=['GET'])
#         def index():
#             return "Web App with Python Flask!"

#         # Start the Flask server in a new thread
#         if on_colab is False:
#             threading.Thread(
#                 target=lambda: run_simple('localhost', port, app)).start()
#         else:
#             # on Colab, you can use the following code instead of the above
#             # line
#             threading.Thread(
#                 target=app.run, kwargs={"use_reloader": False}).start()

#         @app.route('/receiver', methods=['POST'])
#         def get_json():
#             js = request.get_json()
#             if js is not None:  # JSONが送られてきた場合、DB & ローカルに保存
#                 logger.error('ERROR')
#                 print(f'js: {js.keys()}')
#                 self.ana_js = js  # class変数に保存
#                 with open(f'./result/{js["metadata"]["pdf_name"]}.json',
#                           'w') as f:
#                     json.dump(js, f, indent=4)
#                 # DBに保存
#                 con = get_db()  # DB接続
#                 cur = con.cursor()
#                 sql = 'INSERT INTO api_result (id, status, result, ' +\
#                     'message, metadata) values (?,?,?,?,?)'
#                 data = [js['id'], js['status'], json.dumps(js['result']),
#                         js['message'], json.dumps(js['metadata'])]

#                 cur.execute(sql, data)
#                 con.commit()
#                 con.close()
#                 # cur.close()
#             return jsonify(js)

#     def receive(self) -> dict:
#         while True:
#             if self.ana_js is not None:
#                 return self.ana_js
#             else:
#                 continue
