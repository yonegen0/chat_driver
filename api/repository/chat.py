from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
import api.external as external
from api.models.chat import User, Room

# Blueprintを定義
app = Blueprint('chat_api', __name__)

@app.route('/rooms', methods=['GET'])
def get_rooms():
    """
    全てのルームの一覧を取得するAPIエンドポイント。
    """
    try:
        # データベースから全てのルームを取得
        rooms = Room.query.order_by(Room.id).all()
        
        # ルームのリストをJSON形式に変換
        rooms_list = [{'id': room.id, 'name': room.name} for room in rooms]
        
        return jsonify({'rooms': rooms_list}), 200

    except Exception as e:
        return jsonify({'error': f'ルームの取得中にエラーが発生しました: {str(e)}'}), 500

@app.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    """
    指定されたIDのルームを削除するAPIエンドポイント。
    """
    try:
        room = Room.query.get(room_id)
        
        # ルームが存在しない場合はエラー
        if not room:
            return jsonify({'error': '指定されたルームは見つかりませんでした。'}), 404
        
        # 「General」ルームは削除できないようにする
        if room.name == 'General':
            return jsonify({'error': '「General」ルームは削除できません。'}), 403

        external.db.session.delete(room)
        external.db.session.commit()
        
        return jsonify({'message': 'ルームが正常に削除されました。'}), 200

    except Exception as e:
        external.db.session.rollback()
        return jsonify({'error': f'サーバーでエラーが発生しました: {str(e)}'}), 500

@app.route('/addRooms', methods=['POST'])
def create_room():
    """
    新しいルームを作成するAPIエンドポイント。
    リクエストボディからルーム名を取得し、データベースに保存します。
    """
    try:
        data = request.get_json()
        room_name = data.get('name')

        if not room_name or not isinstance(room_name, str) or not room_name.strip():
            return jsonify({'error': '有効なルーム名が指定されていません。'}), 400

        # 重複チェックと新規作成
        new_room = Room(name=room_name)
        external.db.session.add(new_room)
        external.db.session.commit()
        
        return jsonify({
            'message': 'ルームが正常に作成されました。',
            'room': {
                'id': new_room.id,
                'name': new_room.name
            }
        }), 201
    
    except IntegrityError:
        external.db.session.rollback()
        return jsonify({'error': 'このルーム名はすでに存在します。'}), 409
    except Exception as e:
        external.db.session.rollback()
        return jsonify({'error': f'サーバーでエラーが発生しました: {str(e)}'}), 500
