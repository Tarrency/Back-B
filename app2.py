from flask import Flask, jsonify
# import settings
# from snownlp import sentiment
import snownlp
from flask_mongoengine import MongoEngine
from flask import request
from flask_cors import CORS
# import mongoengine as me
app = Flask(__name__)
# Flask 是一个类，我们可以点进去看详细的描述。app是Flask这个类创建出来的对象。
# __name__是获取当前文件的名字，我们可以尝试print(__name__)，就会看见结果是：__main__。
#print(app.config)                               # 可以通过app.config查看所有参数。
# app.config.from_object(settings)

# app.config.from_mapping({
#     MONGODB_SETTINGS = {
#         'db': 'product1',
#         'host': 'localhost',
#         'port': 27017,
#         'connect': True,
#         # 'username': 'test',
#         # 'password': '123456',
#         # 'authentication_source': 'admin'
#     }
# })

app.config['MONGODB_SETTINGS']={    #通过MONGOD_SETTINGS配置MongoEngine
    'db':'product1',
    'host': 'localhost',
    'port': 27017,
    'connect': True,
}

# 初始化 MongoEngine
db = MongoEngine(app)

# class Users(db.Document):    #创建Student学生模型类并继承Document类
#     username=db.StringField()    #学生名字段，字段类型为StringField
#     password=db.StringField()

class Product(db.DynamicDocument):    #创建Student学生模型类并继承Document类
    name=db.StringField()    #学生名字段，字段类型为StringField
    jd=db.StringField()
    jdscore=db.FloatField()

class Comment(db.DynamicDocument):    #创建Student学生模型类并继承Document类
    name=db.StringField()    #学生名字段，字段类型为StringField
    wb=db.StringField()
    wbscore=db.FloatField()

# @app.route('/test')                             # 路由
# def hello_world():                              # 在此路由下的视图（函数）
#     user=Users.objects().all()
# # user = UserInfo.objects(_id=1)
#     for i in user:
#         print(i.username, i.password) 
#     return jsonify(user)

@app.route('/jdnlp', methods=["POST"])                             # 路由
def sentiment():                              # 在此路由下的视图（函数）
    str = request.json
    pro = str['product'] 
    comment=Product.objects(name=pro).first()
    comments=Product.objects(name=pro).all()
    # print('comments', comments)
    if not comment['jdscore']:            #数据不存在时，返回数据不存在
        # return '数据不存在'
        for i in comments:
        # print(i.name, i.jd) 
            s = snownlp.SnowNLP(i.jd)
            i.jdscore = s.sentiments
            i.save()
        # print(s.sentiments)
    # comments.save()
    return jsonify({"data": comments, "code": 200, "message": '评价情感分析'})

@app.route('/wbnlp', methods=["POST"])                             # 路由
def sentiment():                              # 在此路由下的视图（函数）
    str = request.json
    pro = str['product'] 
    comment=Product.objects(name=pro).first()
    comments=Product.objects(name=pro).all()
    # print('comments', comments)
    if not comment['wbscore']:            #数据不存在时，返回数据不存在
        # return '数据不存在'
        for i in comments:
        # print(i.name, i.jd) 
            s = snownlp.SnowNLP(i.wb)
            i.wbscore = s.sentiments
            i.save()
        # print(s.sentiments)
    # comments.save()
    return jsonify({"data": comments, "code": 200, "message": '舆情情感分析'})

# cors = CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
CORS(app, supports_credentials=True)
if __name__ == '__main__':
    #app.run()                                  # 启动flask内部服务器，主机地址和端口号选取默认值
    app.run(port=3300,host="localhost")        # 启动flask内部服务器，主机地址和端口号可自定义
