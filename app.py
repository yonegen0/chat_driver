from flask import Flask
from flask_cors import CORS
import api.external as external

# Flask アプリケーションのインスタンスを作成する関数
def create_app():

    # インスタンス作成
    app = Flask(__name__)
    # MySQL データベースの接続に必要な情報を定義
    USER='root'           # データベースのユーザー名
    PASSWORD='sqlpass'    # データベースのパスワード
    HOST='localhost'      # データベースのホスト名
    DATABASE='chat_data'   # 使用するデータベース名
    SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://' + USER + ':' + PASSWORD + '@' + HOST + '/' + DATABASE + '?charset=utf8'

    # データベース URIの設定
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    import api
    # blueprintをアプリケーションに登録
    app.register_blueprint(api.chat_app)
    return app

# インスタンス作成
app = create_app()
# データベース初期化
external.init_db(app)
CORS(app)

# Flask 開発サーバーを起動
if __name__ == '__main__':
    app.run()