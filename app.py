from flask import Flask, jsonify
import snownlp
from flask_mongoengine import MongoEngine
from flask import request
from flask_cors import CORS
app = Flask(__name__)

app.config['MONGODB_SETTINGS']={   
    'db':'product1',
    'host': 'localhost',
    'port': 27017,
    'connect': True,
}

db = MongoEngine(app)

class Product(db.DynamicDocument):    
    name=db.StringField()   
    jd=db.StringField()
    jdscore=db.FloatField()

class Comment(db.DynamicDocument):   
    name=db.StringField()    
    wb=db.StringField()
    wbscore=db.FloatField()

@app.route('/jdnlp', methods=["POST"])                      
def sentiment():                           
    str = request.json
    pro = str['product'] 
    comment=Product.objects(name=pro).first()
    comments=Product.objects(name=pro).all()
    if not comment['jdscore']:           
        for i in comments:
            s = snownlp.SnowNLP(i.jd)
            i.jdscore = s.sentiments
            i.save()
    return jsonify({"data": comments, "code": 200, "message": '评价情感分析'})

@app.route('/wbnlp', methods=["POST"])                      
def analysis():                              
    str = request.json
    pro = str['product'] 
    comment=Comment.objects(name=pro).first()
    comments=Comment.objects(name=pro).all()
    if not comment['wbscore']:            
        for i in comments:
            s = snownlp.SnowNLP(i.wb)
            i.wbscore = s.sentiments
            i.save()
    return jsonify({"data": comments, "code": 200, "message": '舆情情感分析'})

CORS(app, supports_credentials=True)
if __name__ == '__main__':                         
    app.run(port=3300,host="localhost")        
