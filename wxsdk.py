#-*- coding:utf-8 -*-
import requests
import json

class wxsdk (object):
    
    def __init__(self, agentid=3):
        CORPID = '企业ID'
        CORPSECRET = '企业秘钥'
        self.corpid = CORPID
        self.corpsecret = CORPSECRET
        self.agentid = agentid
        self.url_prefix = 'https://qyapi.weixin.qq.com/cgi-bin'
        self.access_token = self.__get_access_token()

    def __get_access_token(self):
        # access_token 有效期为 7200秒
        url = "%s/gettoken?corpid=%s&corpsecret=%s" % (self.url_prefix, self.corpid, self.corpsecret)
        res = requests.get(url)
        access_token = res.json().get("access_token")
        return access_token

    @staticmethod
    def __response(res):
        errcode = res.get("errcode")
        if errcode is 0:
            return True, res
        else:
            return False, res

    def __post(self, url, data):
        res = requests.post(url, data=json.dumps(data).decode('unicode-escape').encode("utf-8")).json()
        return self.__response(res)

    def __get(self, url):
        res = requests.get(url).json()
        return self.__response(res)


    def sendmsg (self,touser=None,toparty=None,totag=None,msgtype='text',safe=0,content=None,**kwargs):
        url = '%s/message/send?access_token=%s'%(self.url_prefix,self.access_token)

        msgdata = {
            "safe": safe,
            "msgtype": msgtype,
            "agentid": self.agentid
        }

        if touser is None:
            touser = '@all'
        else:
            touser = (touser)
        msgdata['touser'] = touser
        if toparty is not None:
            msgdata['toparty'] = toparty
        if totag is not None:
            msgdata['totag'] = totag
        if msgtype == "text":
            msgdata['text'] = {"content": content}

        status,res = self.__post(url,msgdata)

        return status,res
