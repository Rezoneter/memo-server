# flask 프레임워크를 이용한, Restful API 서버 개발

from flask import Flask
from flask_restful import Api

from resources.user import UserRegisterResource
from memo import MemoListREsource
from memo import MemoResource
# 기본 구조
app = Flask(__name__)

api = Api (app)

# APU 를 구분해서 실행시키는 것은,
# HTTP METHOD 와 URL 의 조합이다.

# 경로와 리소스(API코드)를 연결한다
api.add_resource( UserRegisterResource, '/user/register')
api.add_resource( UserRegisterResource, '/user/login')
api.add_resource( MemoListREsource, '/memo')
api.add_resource( MemoResource, '/memo/<int:memo_id>')

if __name__ == '__main__':
    app.run()



