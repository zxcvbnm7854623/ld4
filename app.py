from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_scores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义玩家信息和得分的模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Player {self.name}>'
    

# 创建数据库
with app.app_context():
    db.create_all()

# 首页，加载游戏界面
@app.route('/')
def index():
    return render_template('index.html')

# 获取玩家的历史得分记录
@app.route('/api/scores', methods=['GET'])
def get_scores():
    players = Player.query.all()
    scores = [{"name": player.name, "score": player.score} for player in players]
    return jsonify(scores)

# 提交玩家分数
@app.route('/api/submit_score', methods=['POST'])
def submit_score():
    player_name = request.json.get('name')
    player_score = request.json.get('score')

    # 创建新的玩家记录
    new_player = Player(name=player_name, score=player_score)
    db.session.add(new_player)
    db.session.commit()

    return jsonify({"message": "Score submitted successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
