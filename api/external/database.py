from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy のインスタンスを作成
db = SQLAlchemy()

# データベース初期化
def init_db(app):
    # SQLAlchemy インスタンスに紐付ける
    db.init_app(app)
    with app.app_context():
        # 定義されたモデルに基づいてデータベースのテーブル作成
        db.create_all()