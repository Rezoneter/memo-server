from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
 
class MemoListREsource(Resource) :
     
    @jwt_required()
    def post(self):
        data = request.get_json()
 
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into memo
                    (userId, title, date, content)
                    values
                    ( %s, %s, %s, %s);'''
            record = (user_id,
                      data['title'],
                      data['date'],
                      data['content'])
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)}, 500
            
        
        return {"result":"success"}, 200

    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()
        # 클라이언트에서 쿼리스트링으로 보내는 데이터는
        # request.args 에 들어있다.
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select id, title, datetime, content, createdAt, updatedAt
                    from memo
                    where userId = %s
                    order by datetime desc
                    limit ''' + offset + ''', '''+ limit +''';'''

            record = (user_id, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
                result_list[i]['datetime'] = row['datetime'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)            
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500
                
        return {"result" : "success" ,
                "items" : result_list , 
                "count" : len(result_list)}, 200



class MemoResource(Resource):

    @jwt_required()
    def put(self,memo_id) :
        data = request.get_json()

        user_id = get_jwt_identity()

        try:
            connection = get_connection
            query ='''update memo
                    set title = %s,
                        date  = %s,
                        contetn = %s
                        where id = %s and userId = %s;'''
            record = (data['title'],data['date'],data['content'],
                      memo_id, user_id)
            cursor = connection.cursor()

            cursor.execute( query, record )

            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)}, 500

        return  {"result":"success"}, 200
    
    @jwt_required()
    def delete(self, memo_id):
        
        user_id = get_jwt_identity()

        try: 
            connection = get_connection()
            query = '''delete from memo
                    where id = %s and userId = %s;'''
            
            record = (memo_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        
        except Error as e: 
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)}, 500


        return {"result":"success"}

