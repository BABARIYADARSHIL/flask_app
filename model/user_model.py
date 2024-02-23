import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig
class user_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except:
            print("Some error")

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            res =  make_response ({"payload":result} ,200)  #Return all the data in JSON Format with HTTP Response Code 2
            res.headers['Acces-Control-Allow-origin'] = "*"
            return res
            
            # return json.dumps(result)
        else:
            return make_response ({"message":"No Data Found"}, 204)
        
    def user_addone_model(self, data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, role_id, password)VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role_id']}','{data['password']}')" )
        return make_response( {"message":"user Created Successfully"}, 201)
    
    def user_add_multiple_model(self, data):
        qry = "INSERT INTO users(name, email, phone, role_id, password) VALUES"
        for userdata in data:
            qry += f"('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['role_id']}, '{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"MULTIPLE_USER_CREATED"},201)

    def user_update_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role_id='{data['role_id']}', password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response( {"message":"User Updated Successfully"}, 201)
        else:
            return make_response( {"message":"User Not Updated Successfully"}, 202)
    
    
    def user_update_multiple_model(self, data):
        for user_data in data:
           qry = f"UPDATE users SET name='{user_data['name']}', email='{user_data['email']}', phone='{user_data['phone']}', password='{user_data['password']}', avatar='{user_data['avatar']}', role_id={user_data['role_id']} WHERE id={user_data['id']}"
           self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message": "MULTIPLE_USER_UPDATE"}, 201)
        else:
            return make_response({"message": "No users updated successfully"}, 202)
        
    
    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM users  WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response( {"message":"User Deleted Successfully"}, 200 )
        else:
            return make_response( {"message":"User Not deleted Successfully"}, 202)
        
    def user_delete_multiple_model(self,data):
        # ----->
        for user_data_d in data:
           qry = (f"DELETE FROM users WHERE id={user_data_d}")
           self.cur.execute(qry)
                                #    Or
        # for id in ids:
            # self.cur.execute(f"DELETE FROM users WHERE id = {id}")
        # -------->
        if self.cur.rowcount > 0:
            return make_response({"message": "MULTIPLE_USER_DELETE"}, 200)
        else:
            return make_response({"message": "No users delete successfully"}, 202)


    def user_patch_model(self, data , id):
        qry = "UPDATE users SET "
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry =qry[:-1]+ f" WHERE id={id}"

        self.cur.execute(qry)
        
        if self.cur.rowcount>0:
            return make_response( {"message":"User Updated Successfully"}, 201)
        else:
            return make_response( {"message":"User Not Updated Successfully"}, 202)

    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            res =  make_response ({"payload":result, "pae_no":page, "limit":limit} ,200)  #Return all the data in JSON Format with HTTP Response Code 2
            return res
        else:
            return make_response ({"message":"No Data Found"}, 204)
    
    def user_uplode_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response( {"message":"File uploaded Successfully"}, 201)
        else:
            return make_response( {"message":"User Not Updated Successfully"}, 202)
        
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload":userdata,
            "exp":exp_epoch_time
        }
        jwtoken = jwt.encode(payload, "darshil", algorithm="HS256")
        return make_response({"token":jwtoken}, 200)