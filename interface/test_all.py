# coding:utf-8
import requests
import json
import ssl
import urllib3
import unittest
import re
import base64

import struct
urllib3.disable_warnings()

class Test(unittest.TestCase):
    def test01(self):
        #header = {"User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}
        r = requests.get('https://cattle.test.druidtech.net',verify=False)
        print(r.status_code)
        print(r.headers)

        #定义登录参数数组
        logindata1 = {"password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea","username":"ceshiwushan"}
        #转为json格式
        uspw_data1 = json.dumps(logindata1)
        #post登录请求
        login1 = requests.post('https://cattle.test.druidtech.net/api/v1/login',uspw_data1,verify=False)
        print("loginheader",login1.headers)
        print("responsedata",login1.headers)
        print("xd",login1.headers['X-Druid-Authentication'])

        #创建header
        header1 = {
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login1.headers['X-Druid-Authentication'],
            "Host": "cattle.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        password1={"password":"daafcceb72ec0cc8c8c6eade8e4249a144f3318916ccadf22026dc7f57e67aee","old_password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea"}
        passworddata1=json.dumps(password1)
        change1=requests.put('https://cattle.test.druidtech.net/api/v1/user/password',passworddata1,headers=header1,verify=False)
        print("status",change1.status_code)
        print(change1.text)



        #定义登录参数数组
        logindata2 = {"password":"daafcceb72ec0cc8c8c6eade8e4249a144f3318916ccadf22026dc7f57e67aee","username":"ceshiwushan"}
        #转为json格式
        uspw_data2 = json.dumps(logindata2)
        #post登录请求
        login2 = requests.post('https://cattle.test.druidtech.net/api/v1/login',uspw_data2,verify=False)
        print("loginheader",login2.headers)
        print("responsedata",login2.headers)

        #创建header
        header2 = {
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login2.headers['X-Druid-Authentication'],
            "Host": "cattle.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        password2={"password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea","old_password":"daafcceb72ec0cc8c8c6eade8e4249a144f3318916ccadf22026dc7f57e67aee"}
        passworddata2=json.dumps(password2)
        change2=requests.put('https://cattle.test.druidtech.net/api/v1/user/password',passworddata2,headers=header2,verify=False)
        print("status",change2.status_code)
        print(change2.text)

        #post登录请求
        login3 = requests.post('https://cattle.test.druidtech.net/api/v1/login',uspw_data1,verify=False)
        print("loginheader",login3.headers)
        print("responsedata",login3.headers)

        #创建header
        header = {
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login3.headers['X-Druid-Authentication'],
            "Host": "cattle.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        #getmyself
        getmyself = requests.get('https://cattle.test.druidtech.net/api/v1/user/myself',headers=header,verify=False)
        print(getmyself.status_code)
        self.assertEquals(getmyself.status_code,200)
        print("myinfo",getmyself.text)
        self.assertIn("ceshiwushan",getmyself.text)

        #updateUserInfo
        userinfo = {"address":u"四川省成都市高新区","id_card":"511014199011116666","phone":"13523456789","email":"123244142@163.com"}
        upuserinfo = json.dumps(userinfo)
        info = requests.put('https://cattle.test.druidtech.net/api/v1/user/info',upuserinfo,headers=header,verify=False)
        #断言返回状态码
        code0 = str(info.status_code)
        self.assertIn("20",code0)
        #由于返回内容为空，暂时不做其他判断
        print("userinfo",info.text)

        #getcompany
        getcompany = requests.get('https://cattle.test.druidtech.net/api/v1/company/',headers=header,verify=False)
        print(getcompany.status_code)
        self.assertEquals(getcompany.status_code,200)
        self.assertIn(u"成都德鲁伊科技有限公司",getcompany.text)

        #getDevices
        getdevices = requests.get('https://cattle.test.druidtech.net/api/v1/device/',headers=header,verify=False)
        print("devices",getdevices.text)
        self.assertIn("5965885a0059ea0a31887f12",getdevices.text)
        #正则表达式获取Deviceid
        devices1 = re.findall(r'"id":"([^","]+)?', getdevices.text)
        str1=str(devices1)
        deviceid=str1[2:26]
        print("deviceid",deviceid)


        #GET Device By ID
        getbyid = requests.get('https://cattle.test.druidtech.net/api/v1/device/id/'+deviceid,headers=header,verify=False)
        #self.assertIn(20,getbyid.status_code)
        print("getbyid",getbyid.text)
        ##正则表达式获取Deviceuuid
        devices2 = re.findall(r'"uuid":"([^","]+)?', getbyid.text)
        print("uuid",devices2)
        str2=str(devices2)
        deviceuuid=str2[2:26]
        print("uuid",deviceuuid)
        #正则表达式获取Devicespecies
        str00=str(getbyid.text)
        devices3 = re.findall(r'"species":([^}]+)?', str00)
        print("species",devices3)
        str3=str(devices3)
        devicespecies=str3[2:3]
        print("species",devicespecies)
        #正则表达式获取Devicemark
        str12=str(getbyid.text)
        devices4 = re.findall(r'"mark":([^,"]+)?', str00)
        print("mark",devices4)
        str4=str(devices4)
        devicemark=str4[2:-2]
        print("mark",devicemark)

        #Get Device By UUID
        getbyuuid = requests.get('https://cattle.test.druidtech.net/api/v1/device/uuid/'+deviceuuid,headers=header,verify=False)
        self.assertIn("id",getbyuuid.text)

        #GET Area By DeivceID
        getarea = requests.get('https://cattle.test.druidtech.net/api/v1/device/id/'+deviceid+'/area',headers=header,verify=False)
        self.assertEquals(200,getarea.status_code)
        print(getarea.text)

        #Search Device By mark
        searchbymark = requests.get('https://cattle.test.druidtech.net/api/v1/device/search/mark/'+devicemark,headers=header,verify=False)
        self.assertEquals(200,searchbymark.status_code)
        print(searchbymark.text)

        #GET Room Is idle
        getroom = requests.get('https://cattle.test.druidtech.net/api/v1/device/idle/room',headers=header,verify=False)
        self.assertEquals(200,getroom.status_code)
        self.assertIn("updated_at",getroom.text)

        #List Many Devices By id
        iddata={
	"id":[
		deviceid
	]
}
        idjs=json.dumps(iddata)
        listmany = requests.post('https://cattle.test.druidtech.net/api/v1/device/many',idjs,headers=header,verify=False)
        self.assertEquals(200,listmany.status_code)
        print("listmany",listmany.text)
        self.assertIn("firmware_version",listmany.text)
        #根据返回的listmany.text获取各种信息，为Update Cattle Info By DeviceID准备
        #获取owner_id
        str55=str(listmany.text)
        devices5 = re.findall(r'owner_id":"([^",]+)?', str55)
        print("owner_id",devices5)
        str5=str(devices5)
        ownerid=str5[2:-2]
        print("owner_id",ownerid)
        #获取ownername
        str66=str(listmany.text)
        devices6 = re.findall(r'owner_name":"([^",]+)?', str66)
        print("owner_name",devices6)
        str6=str(devices5)
        ownername=str6[2:-2]
        print("owner_name",ownername)
        #获取mark
        str77=str(listmany.text)
        devices6 = re.findall(r'mark":([^,"]+)?', str77)
        print("mark",devices6)
        str7=str(devices6)
        mark=str7[2:-2]
        print("mark",mark)
        #获取gender
        str88=str(listmany.text)
        devices7 = re.findall(r'gender":([^,"]+)?', str88)
        print("gender",devices7)
        str8=str(devices7)
        gender=str8[2:-2]
        print("gender",gender)
        #获取bust
        str99=str(listmany.text)
        devices8 = re.findall(r'bust":([^,"]+)?', str99)
        print("bust",devices8)
        str99=str(devices8)
        bust=str99[2:-2]
        print("bust",bust)
        #获取image
        strim=str(listmany.text)
        devicesim = re.findall(r'images([^,"]+)?', strim)
        print("image",devicesim)
        strima=str(devicesim)
        image=strima[1:-1]
        print("image",image)


        #Regsier
        regsierdata={
        "uuid": "3e0033000651353334393332",
        "device_type": 1,
        "hardware_version": 2,
        "firmware_version": 0,
        "company_id": "57b66fb6ec7e90884efbad92",
        "company_name": "成都德鲁伊科技有限公司",
        "mark": 0,
        "battery_voltage": 0,
        "temperature": 23,
        "longitude": 22.8911513,
        "latitude": 22.6051139,
        "point_location": 0,
        "total_gps": 1,
        "total_behavior": 5,
        "total_behavior2": 0,
        "total_area": 0,
        "room_id": "",
        "room_name": "",
        "owner_id": "59a76fff415bac49aa828ceb",
        "owner_name": "doudou",
        "survive": 0,
        "activity": 1,
        "signal_strength": 13,
        "nickname": "禽流感",
        "birth_date": "2007-03-16T00:00:00Z",
        "gender": 0,
        "weight": 122,
        "height": 0,
        "bust": 0,
        "cannon": 0,
        "coat_color": "",
        "description": "",
        "images": [],
        "behavior": 0,
        "species": 4
    }
        redata = json.dumps(regsierdata)
        regsier = requests.post('https://cattle.test.druidtech.net/api/v1/device/many',redata,headers=header,verify=False)
        print(regsier.status_code)
        self.assertEquals(200,regsier.status_code)
        print(regsier.text)

        #List Devices By Exclude
        exdata={
    "id":[
    deviceid
    ]
}
        exid=json.dumps(exdata)
        exclude = requests.post('https://cattle.test.druidtech.net/api/v1/device/exclude',exid,headers=header,verify=False)
        print("exclude",exclude.status_code)
        self.assertIn("uuid",exclude.text)
        self.assertEquals(200,exclude.status_code)

        #Get Device GPS
        getgps = requests.get('https://cattle.test.druidtech.net/api/v1/gps/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getgps.status_code)
        print("gps",getgps.text)

        #Get Device Behavior
        getbehavior = requests.get('https://cattle.test.druidtech.net/api/v1/behavior/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getbehavior.status_code)

        #Get Behavior analyze
        analyze={"time_start":"2018-01-31T16:00:00Z","time_end":"2018-02-28T16:00:00Z","time_cell":120,"species":-1,"time":"month"}
        analyzedata=json.dumps(analyze)
        getanalyze = requests.post('https://cattle.test.druidtech.net/api/v1/behavior/analyze/',analyzedata,headers=header,verify=False)
        self.assertEquals(200,getanalyze.status_code)
        #self.assertIn("motion_other_low_num",getanalyze.text)

        #Get ODBA Analyze Data
        odba={"time_start":"2018-01-31T16:00:00Z","time_end":"2018-02-28T16:00:00Z","time_cell":1,"species":-1,"time":"month"}
        odbadata=json.dumps(odba)
        getodba=requests.post('https://cattle.test.druidtech.net/api/v1/odba/analyze/',odbadata,headers=header,verify=False)
        self.assertEquals(200,getodba.status_code)

        #Get Loving Analyze Data
        loving= {
"device_ids":[
	deviceid
	],
"room_id":"11231231231231",
"time_start":"2014-11-12T11:45:26.371Z",
"time_end":"2014-11-12T11:45:26.371Z",
"survive":6,
"time_cell":3,
"species": -1
   }
        lovingdata=json.dumps(loving)
        getloving=requests.post('https://cattle.test.druidtech.net/api/v1/odba/loving/',lovingdata,headers=header,verify=False)
        self.assertEqual(200,getloving.status_code)

        #Search Device
        #searchdevice=requests.post('https://cattle.test.druidtech.net/api/v1/search/device/',headers=header,verify=False)

        #Create area
        area={"msg_type":2,"type":"Round","area_name":"API测试","point":{"lat":30.552367387998355,"lng":104.0488353988973},"distance":7825}
        areadata=json.dumps(area)
        createarea=requests.post('https://cattle.test.druidtech.net/api/v1/ditu/',areadata,headers=header,verify=False)
        self.assertIn("id",createarea.text)
        #提取areaid
        print("createarea.text",createarea.text)
        strr=str(createarea.text)
        areai = re.findall(r'"id":"([^",]+)?', strr)
        print("areai",areai)
        rooms=str(areai)
        areaid=rooms[2:-2]
        print("areaid",areaid)

        #Add Device to Area
        adddevicetoarea = requests.put('https://cattle.test.druidtech.net/api/v1/ditu/area/'+areaid+'/adddevice/'+deviceid,headers=header,verify=False)
        self.assertIn("Connection",adddevicetoarea.headers)
        print("adddevicetoareaCode",adddevicetoarea.status_code)
        #self.assertEquals(200,adddevicetoarea.status_code)

        #List Area
        listarea = requests.get('https://cattle.test.druidtech.net/api/v1/ditu/area',headers=header,verify=False)
        self.assertIn("area_name",listarea.text)
        self.assertEquals(200,listarea.status_code)

        #Update Area Info  api/v1/ditu/area/${areaid}
        areainfo={"area_name":"修改后","distance":4850,"msg_type":1,"point":{"lng":104.0488353988973,"lat":30.552367387998355},"type":"Round"}
        areainfodata=json.dumps(areainfo)
        updatearea=requests.put('https://cattle.test.druidtech.net/api/v1/ditu/area/'+areaid,areainfodata,headers=header,verify=False)
        #self.assertEqual(200,updatearea.status_code)
        self.assertIn("Connection",updatearea.headers)

        #Get Area info with ID
        getareainfo=requests.get('https://cattle.test.druidtech.net/api/v1/ditu/area/'+areaid,headers=header,verify=False)
        self.assertIn(areaid,getareainfo.text)
        self.assertEqual(200,getareainfo.status_code)

        #Delete Area
        deletearea=requests.delete('https://cattle.test.druidtech.net/api/v1/ditu/area/'+areaid,headers=header,verify=False)
        self.assertIn("Connection",deletearea.headers)

        #Create Room
        room={
	"description":"我是分组2",
	"room_name":"分组2"
}
        roomdata=json.dumps(room)
        createroom=requests.post('https://cattle.test.druidtech.net/api/v1/room/',roomdata,headers=header,verify=False)
        self.assertEquals(200,createroom.status_code)
        self.assertIn("user_id",createroom.text)
        #获取roomid
        #获取image
        str15=str(createroom.text)
        q1 = re.findall(r'"id":"([^",]+)?', str15)
        print("roomid",q1)
        roomidq=str(q1)
        roomid=roomidq[2:-2]
        print("roomid",roomid)

        #Add Device to Room
        addinfo={
   "id":[
        deviceid
   ]
}
        adddata=json.dumps(addinfo)
        print(adddata)
        adddevicetoroom=requests.put('https://cattle.test.druidtech.net/api/v1/room/id/'+roomid+'/adddevice',adddata,headers=header,verify=False)
        self.assertEquals(201,adddevicetoroom.status_code)

        #Get Device in Room
        getdeviceinroom=requests.get('https://cattle.test.druidtech.net/api/v1/room/id/'+roomid+'/device',headers=header,verify=False)
        self.assertIn(deviceid,getdeviceinroom.text)
        self.assertEquals(200,getdeviceinroom.status_code)

        #Delete Device From Room
        deleteinfo={"id":[deviceid]}
        deletedata=json.dumps(deleteinfo)
        deletefromroom=requests.put('https://cattle.test.druidtech.net/api/v1/room/id/'+roomid+'/deldevice',deletedata,headers=header,verify=False)
        self.assertEquals(204,deletefromroom.status_code)
        self.assertIn("Connection",deletefromroom.headers)

        #Update room Info
        roominfo={
	"description":"我是分组3",
	"room_name":"分组3"
}
        roominfodata=json.dumps(roominfo)
        updateroom=requests.put('https://cattle.test.druidtech.net/api/v1/room/id/'+roomid,roominfodata,headers=header,verify=False)
        self.assertEquals(201,updateroom.status_code)

        #List Room
        lisroom=requests.get('https://cattle.test.druidtech.net/api/v1/room/',headers=header,verify=False)
        self.assertIn(roomid,lisroom.text)

        #Get Room info
        getroominfo=requests.get('https://cattle.test.druidtech.net/api/v1/room/id/'+roomid+'/info',headers=header,verify=False)
        self.assertIn(roomid,getroominfo.text)

        #Delete Room
        deleteroom=requests.delete('https://cattle.test.druidtech.net/api/v1/room/id/'+roomid,headers=header,verify=False)
        self.assertEquals(204,deleteroom.status_code)

        #Update Cattle Info By DeviceID
        #处理数据的引号？
        cattleinfo={
    "device_id": "5965885a0059ea0a31887f12",
    "owner_id": "5ab2024da32d8003377330e3",
    "owner_name": "ceshiwushan",
    "mark": 2028,
    "nickname": "cattle",
    "birth_date": "2018-02-07T06:22:15Z",
    "gender": 0,
    "weight": 67,
    "height": 88,
    "bust": 0,
    "cannon": 0,
    "coat_color": "",
    "description": "",
    "images": [""],
    "behavior": 0,
    "species": 0
}
        cattledata=json.dumps(cattleinfo)
        print("cattledata",cattledata)
        updatecattle=requests.put('https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid,cattledata,headers=header,verify=False)
        print(updatecattle.status_code)
        print("updatecattle.text",updatecattle.text)
        self.assertIn(deviceid,updatecattle.text)

        #Update image by Device
        #f=open("C:\\Users\\liugc\\PycharmProjects\\cattleuser\\dog.jpg","rb")
        f=open("/var/lib/jenkins/workspace/cattleuserAPItest/interface/new.jpg","rb")
        data=f.read()
        pictureupdate=requests.put('https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid+'/image/dog.jpg',data,headers=header,verify=False)
        self.assertEquals(201,pictureupdate.status_code)

        #List Many Devices By id
        iddata2={
	"id":[
		deviceid
	]
}
        idjs2=json.dumps(iddata2)
        listmany2 = requests.post('https://cattle.test.druidtech.net/api/v1/device/many',idjs2,headers=header,verify=False)
        self.assertEquals(200,listmany2.status_code)
        print("listmany",listmany2.text)
        self.assertIn("firmware_version",listmany2.text)
        #获取image
        strim2=str(listmany2.text)
        devicesim2 = re.findall(r'images(.+?)behavior', strim2)
        print("imageids",devicesim2)
        strima2=str(devicesim2)
        imageid=strima2[6:30]
        print("imageid",imageid)

        #Get image
        getimage=requests.get('https://cattle.test.druidtech.net/api/v1/file/device/'+deviceid+'/image/'+imageid,headers=header,verify=False)
        self.assertEquals(200,getimage.status_code)

        #Get thumbnail Images 缩略图
        getthumbnail=requests.get('https://cattle.test.druidtech.net/api/v1/file/device/'+deviceid+'/image/'+imageid+'/thumbnail',headers=header,verify=False)
        print("getthumbnail url: ",'https://cattle.test.druidtech.net/api/v1/file/device/'+deviceid+'/image/'+imageid+'/thumbnail')
        self.assertEquals(200,getthumbnail.status_code)

        #Get Cattle By DeviceId
        getbydeviceid=requests.get('https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid,headers=header,verify=False)
        getm1 = re.findall(r'id(.+?)updated_at', getbydeviceid.text)
        print("biologicalid",getm1)
        getm2=str(getm1)
        biologicalid=getm2[5:29]
        print("biologicalid",biologicalid)

        #Delete Image by biological
        #deletimage=requests.delete('https://cattle.test.druidtech.net/api/v1/biological/cattle/id/'+biologicalid+'/image/'+imageid,headers=header,verify=False)
        #print("deletimage url:",'https://cattle.test.druidtech.net/api/v1/biological/cattle/id/'+biologicalid+'/image/'+imageid)
        #self.assertEquals(200,deletimage.status_code)
        #删除图片 暂时代替
        deleteimagebydevice2=requests.delete('https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid+'/image/'+imageid,headers=header,verify=False)
        print("deleteimagebydevice url: ",'https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid+'/image/'+imageid)
        self.assertEquals(204,deleteimagebydevice2.status_code)


        #Delete Image By device
        #Update image by Device再次上传一张图片
        #f2=open("C:\\Users\\liugc\\PycharmProjects\\cattleuser\\new.jpg","rb")
        f2=open("/var/lib/jenkins/workspace/cattleuserAPItest/interface/new.jpg","rb")
        data2=f2.read()
        pictureupdate2=requests.put('https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid+'/image/new.jpg',data2,headers=header,verify=False)
        print("url: ",'https://cattle.test.druidtech.net/api/v1/device/cattle/device/'+deviceid+'/image/new.jpg')
        self.assertEquals(201,pictureupdate2.status_code)
        #List Many Devices By id
        iddata3={
        "id":[
		 deviceid
		 ]
		 }
        idjs3=json.dumps(iddata3)
        listmany3 = requests.post('https://cattle.test.druidtech.net/api/v1/device/many',idjs3,headers=header,verify=False)
        self.assertEquals(200,listmany3.status_code)
        print("listmany",listmany3.text)
        self.assertIn("firmware_version",listmany3.text)
        #获取imageid
        strim3=str(listmany3.text)
        devicesim3 = re.findall(r'images(.+?)behavior', strim3)
        print("imageids",devicesim3)
        strima3=str(devicesim3)
        imageid2=strima3[6:30]
        print("imageid",imageid2)
        #删除图片
        deleteimagebydevice=requests.delete('https://cattle.test.druidtech.net/api/v1/biological/cattle/device/'+deviceid+'/image/'+imageid2,headers=header,verify=False)
        self.assertEquals(204,deleteimagebydevice.status_code)


        '''
        #Get Unread Message
        getunreadmessage=requests.get('https://cattle.test.druidtech.net/api/v1/message/unread',headers=header,verify=False)
        print("Unread Message",getunreadmessage.text)
        self.assertIn("msg_type",getunreadmessage.text)
        self.assertEquals(200,getunreadmessage.status_code)
        #dst
        strm1=str(getunreadmessage.text)
        m1 = re.findall(r'dst[\s\S]*?type?', strm1)
        print("dst",m1)
        strme1=str(m1)
        dst=strme1[8:32]
        print("dst",dst)
        #unreadmessageid
        m11=re.findall(r'id[\s\S]*?dst?', strm1)
        print("unreadmessageid",m11)
        strme11=str(m11)
        unreadmessageid=strme11[7:31]
        print("unreadmessageid",unreadmessageid)
        #type
        m2=re.findall(r'type[\s\S]*?level?', strm1)
        print("type",m2)
        strme2=str(m2)
        type=strme2[8:9]
        print("type",type)
        #level
        m3=re.findall(r'level[\s\S]*?target?', strm1)
        print("level",m3)
        strme3=str(m3)
        level=strme3[9:10]
        print("level",level)
        """#target_str
        m5=re.findall(r'target_str[\s\S]*?msg.?', strm1)
        print("target_str",m5)
        strme5=str(m5)
        target_str=strme5[1:-1]
        print("target_str",target_str)"""
        #msg
        m6=re.findall(r'msg[\s\S]*?msg_cn.?', strm1)
        print("msg",m6)
        strme6=str(m6)
        msg=strme6[8:31]
        print("msg",msg)
        #msg_cn
        m7=re.findall(r'msg_cn[\s\S]*?msg_type.?', strm1)
        print("msg_cn",m7)
        strme7=str(m7)
        msg_cn=strme7[1:-1]
        print("msg_cn",msg_cn)
        '''
        '''#msg_type
        m8=re.findall(r'msg_cn[\s\S]*?msg_type.?', strm1)
        print("msg_type",m8)
        strme8=str(m8)
        msg_type=strme8[1:-1]
        print("msg_type",msg_type)
        #src
        m9=re.findall(r'src(.+?)src_name', strm1)
        print("src",m9)
        strme9=str(m9)
        src=strme9[1:-1]
        print("src",src)
        #src_name
        m10=re.findall(r'src_name(.+?)timestamp', strm1)
        print("src_name",m10)
        strme10=str(m10)
        src_name=strme10[1:-1]
        print("src_name",src_name)'''


        '''
        #List message
        listmessage=requests.get('https://cattle.test.druidtech.net/api/v1/message/',headers=header,verify=False)
        self.assertIn("msg_type",listmessage.text)
        self.assertEquals(200,listmessage.status_code)

        #PUT message 标记已读
        message={"id":[unreadmessageid]}
        putdata=json.dumps(message)
        putmessage=requests.put('https://cattle.test.druidtech.net/api/v1/message/',putdata,headers=header,verify=False)
        self.assertEquals(201,putmessage.status_code)

        #Delete message
        deletemessage=requests.delete('https://cattle.test.druidtech.net/api/v1/message/id/'+unreadmessageid,headers=header,verify=False)
        self.assertEquals(204,deletemessage.status_code)
        #Get Unread Message
        getunreadmessage2=requests.get('https://cattle.test.druidtech.net/api/v1/message/unread',headers=header,verify=False)
        #unreadmessageid
        m12=re.findall(r'id[\s\S]*?dst?', getunreadmessage2.text)
        print("unreadmessageid",m12)
        strme12=str(m12)
        unreadmessageid2=strme12[7:31]
        print("unreadmessageid",unreadmessageid2)
        self.assertNotEquals(unreadmessageid,unreadmessageid2)

        #Deltet Many message
        manymessage={
    "id":[
		 unreadmessageid2
		 ]
}
        data3=json.dumps(manymessage)
        deletemanymessage=requests.put('https://cattle.test.druidtech.net/api/v1/message/delete',data3,headers=header,verify=False)
        self.assertEquals(204,deletemanymessage.status_code)
        '''









