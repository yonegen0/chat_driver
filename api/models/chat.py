from api.external import db
from datetime import datetime

# User モデルの定義
class User(db.Model):
    # テーブル名を設定
    __tablename__ = 'users'
    # テーブルに関する追加情報（コメント）
    __table_args__ = {
        'comment': 'ユーザー情報'
    }
    # ユーザーID
    id = db.Column(db.Integer, primary_key=True)

# Room モデルの定義
class Room(db.Model):
    # テーブル名を設定
    __tablename__ = 'rooms'
    # テーブルに関する追加情報（コメント）
    __table_args__ = {
        'comment': 'ルーム情報'
    }
    
    # ルーム情報ID
    id = db.Column(db.Integer, primary_key=True)
    # ルーム情報のテキスト
    messages = db.relationship('Message', backref='message', cascade="all, delete-orphan", lazy=True, uselist=True, foreign_keys='Message.user_id')


# Message モデルの定義
class Message(db.Model):
    # テーブル名を設定
    __tablename__ = 'messages'
    # テーブルに関する追加情報（コメント）
    __table_args__ = {
        'comment': 'メッセージ'
    }
    # メッセージID
    id = db.Column(db.Integer, primary_key=True)
    # ユーザーID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # メッセージのテキスト
    message_text = db.Column(db.String(255), nullable=False)