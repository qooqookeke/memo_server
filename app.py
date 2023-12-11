from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from Resources.follow import FollowMemoResource, FollowResource
from Resources.memo import MemoListResource, MemoResource

from Resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource
from config import Config

app = Flask(__name__)

# 환경 변수 셋팅
app.config.from_object(Config)

# JWT 매니저 초기화
jwt = JWTManager(app)

api = Api(app)

# 경로와 리소스 연결한다.
api.add_resource(UserRegisterResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserLogoutResource, '/user/logout')
api.add_resource(MemoListResource, '/memo')
api.add_resource(MemoResource, '/memo/<int:memo_id>')
api.add_resource(FollowResource, '/follow/<int:followee_id>')
api.add_resource(FollowMemoResource, '/follow/memo')


if __name__ == '__main__':
    app.run()