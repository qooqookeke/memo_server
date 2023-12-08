from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error


class MemoListResource(Resource):
    # 메모 생성
    @jwt_required()
    def post(self):

        data = request.get_json()

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''insert into memo_list
                        (userId, title, date, content)
                        values
                        (%s, %s, %s, %s);'''
            
            record = (user_id, data['title'], data['date'], data['content'])

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 500
        

        return {"result":"success"}, 200
    

    # 내 메모 리스트 가져오기
    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        # 쿼리 스트링 (쿼리 파라미터) 데이터를 받아온다.
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        

        try:
            connection = get_connection()
            query = '''select id, title, date, content
                    from memo_list
                    where userId = %s
                    order by date
                    limit '''+str(offset)+''', '''+str(limit)+''';'''
            record = (user_id, )
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            # result_list의 타임 부분을 문자열로 변환하는 것
            i = 0
            for row in result_list :
                result_list[i]['date'] = row['date'].isoformat()
                i = i + 1 

            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error':str(e)}, 500


        return {'result':'success',
                'items':result_list, 
                'count':len(result_list)}, 200
    


class MemoResource(Resource):
    # 메모 삭제
    @jwt_required()
    def delete(self, memo_id):
        
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''delete from memo_list
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
            return {"error":str(e)}, 500

        return {"result":"success"}, 200
    

    # 메모 수정
    @jwt_required()
    def put(self, memo_id):
        
        data = request.get_json()

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''update memo_list
                        set title = %s, 
                        date = %s, 
                        content = %s 
                        where id = %s and userId = %s;'''
            record = (data['title'], data['date'], data['content'],
                      memo_id, user_id)
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error':str(e)}, 500
        
        return {'result':'success'}, 200

