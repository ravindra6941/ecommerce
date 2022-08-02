import mysql.connector 
import mysql

from PIL import Image, ImageDraw, ImageFont


class library:
    #constructor
    def __init__(self):
        self.conn=mysql.connector.connect(host="localhost",user="root",password="",database="ecommerce")

    def __fire(self,qry):
        mycursor=self.conn.cursor()
        result=mycursor.execute(qry)
        return mycursor,result

   

    #insert data into table
    def insert(self, table,dic):
        qry=" insert into " + table + " set " 
        i=1
        for key,value in dic.items():
            if(len(dic)==i):
                if(str(value).isdigit()):
                    qry = qry + key + " = " + str(value)
                else:
                    qry = qry + key + " = '" + str(value) + "' "
            else:
                if(str(value).isdigit()):
                    qry = qry + key + " = " + str(value) + ", "
                else:
                    qry = qry + key + " = '" + str(value) + "', "
            i=i+1
        cur,res = self.__fire(qry)
        self.conn.commit()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Insert given data","status":True}
        else:
            ret={"mess":"Problem to Inserting given data","status":False}
        return ret


            
    #delete data from table
    def deldata(self,table,field="",value=""):
        if(len(field)==0 and len(value)==0):
            qry="delete from " + table
        elif(value.isnumeric()):
            qry="delete from " + table + " where " + field + " = " + str(value)
        else:
            qry="delete from " + table + " where " + field + " = '" + str(value) + "'"
        cur,res = self.__fire(qry)
        self.conn.commit()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Delete given data","status":True}
        else:
            ret={"mess":"Problem to Delete given data","status":False}
        return ret

    #check or get data from multiple condition
    def getalldata(self,table,condition=""):
        cond=" where "
        i=1
        if(len(condition)>=1):
            for key,value in condition.items():
                if(str(value).isdigit()):
                    if(len(condition)==i):
                        cond = cond + key + " = "+ str(value)
                    else:
                        cond = cond + key + " = "+ str(value) + " and "
                else:
                    if(len(condition)<=i):
                        cond = cond + key + " = '"+ str(value) + "' "
                    else:
                        cond = cond + key + " = '"+ str(value) + "' and "
                i=i+1

        if(len(condition)<=0):
            qry="select * from " + table
        else:
            qry= "select * from " + table + cond

        cur,res = self.__fire(qry)
        lst=cur.fetchall()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Execute query ","status":True,"count":cur.rowcount,"data":lst,"qry":qry}
        else:
            ret={"mess":"Problem to Delete given data","status":False,"count":0,"data":False,"qry":qry}
        
        return ret

            
    
    #check data is available
    def getdata(self,table, field="", value=""):
        if(len(field)==0 and len(value)==0):
            qry="select * from " + table
        elif(value.isdigit()):
            qry="select * from " + table + " where " + field + " = " + str(value)
        else:
            qry="select * from " + table + " where " + field + " = '" + str(value) + "'"
        cur,res = self.__fire(qry)
        lst=cur.fetchall()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Delete given data","status":True,"count":cur.rowcount,"data":lst}
        else:
            ret={"mess":"Problem to Delete given data","status":False,"count":0,"data":False}
        
        return ret


    #update data in table
    def update(self,table, dic, field,val):
        qry="update " + table + " set "
        i=1
        for key,value in dic.items():
            if(len(dic)==i):
                if(str(value).isdigit()):
                    qry = qry + key + " = " + str(value)
                else:
                    qry = qry + key + " = '" + str(value) + "' "
            else:
                if(str(value).isdigit()):
                    qry = qry + key + " = " + str(value) + ", "
                else:
                    qry = qry + key + " = '" + str(value) + "', "
            i=i+1
        qry = qry + " where " + field + " = '" + str(val) + "'"
        cur,res= self.__fire(qry)
        self.conn.commit()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Insert given data","status":True,"result":qry}
        else:
            ret={"mess":"Problem to Inserting given data","status":False,"result":qry}
        return ret



    #update data in table
    def updateQuery(self,table, dic, condition):
        qry="update " + table + " set "
        i=1
        for key,value in dic.items():
            if(len(dic)==i):
                if(str(value).isnumeric()):
                    qry = qry + key + " = " + str(value)
                else:
                    qry = qry + key + " = '" + str(value) + "' "
            else:
                if(str(value).isnumeric()):
                    qry = qry + key + " = " + str(value) + ", "
                else:
                    qry = qry + key + " = '" + str(value) + "', "
            i=i+1

        qry = qry + " where "
        i=1
        for key,value in condition.items():
            if(len(condition)==i):
                if(str(value).isnumeric()):
                    qry = qry + key + " = " + str(value)
                else:
                    qry = qry + key + " = '" + str(value) + "' "
            else:
                if(str(value).isnumeric()):
                    qry = qry + key + " = " + str(value) + " and "
                else:
                    qry = qry + key + " = '" + str(value) + "' and "
            i=i+1

        cur,res= self.__fire(qry)
        self.conn.commit()
        if(cur.rowcount >= 1):
             ret={"mess":"Successfully Insert given data","status":True,"qry":qry}
        else:
             ret={"mess":"Problem to Inserting given data","status":False,"qry":qry}
        return ret


    def getdata_limit(self,table,start,record):
        qry="select * from " + table + " limit " + str(start)  + "," + str(record)
        cur,res = self.__fire(qry)
        lst=cur.fetchall()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Delete given data","status":True,"count":cur.rowcount,"data":lst}
        else:
            ret={"mess":"Update Query is not fire","status":False,"count":0,"data":False}
        
        return ret



    def dblogin(self,tab,where):
        qry="select * from " + tab + where
        self.conn=connect()
        mycursor=conn.cursor(buffered=True)
        mycursor.execute(qry)
        self.conn.commit()
        return mycursor.rowcount


    def getQryData(self,qry):
        cur,res = self.__fire(qry)
        lst=cur.fetchall()
        if(cur.rowcount >= 1):
            ret={"mess":"Successfully Execute query ","status":True,"count":cur.rowcount,"data":lst}
        else:
            ret={"mess":"Problem to Delete given data","status":False,"count":0,"data":False}
            
        return ret

