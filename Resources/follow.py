from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error


class FollowResource(Resource):
    # 친구 맺기
    @jwt_required()
    def post(self, followee_id):
        
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into follow
                        (followerID, followeeId)
                        values
                        (%s, %s);'''
            record = (user_id, followee_id)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 500


        return {"result":"success"}, 200
    
    # 친구 끊기
    @jwt_required()
    def delete(self, followee_id):
        
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''delete from follow
                        where followerId = %s and followeeID = %s;'''
            record = (user_id, followee_id)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 500


        return {"result":"success"}, 200
    


class FollowMemoResource(Resource):
    # 친구 메모 가져오기
    @jwt_required()
    def get(self) :

        offset = request.args.get('offset')
        limit = request.args.get('limit')
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''select m.id as memoId, m.userId, 
                        m.title, m.date, m.content, 
                        m.createdAt, m.updatedAt, u.nickname
                        from follow f
                        join memo_list m
                        on f.followeeId = m.userId
                        join user u
                        on m.userId = u.id
                        where f.followerId = %s and m.date > now()
                        order by m.date asc
                        limit '''+offset+''', '''+limit+''';'''
            record = (user_id, )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['date'] = row['date'].isoformat()
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
                i = i + 1 
            
            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 500
        
        return {"result":"success",
                "items":result_list, 
                "count":len(result_list)}, 200
    

    