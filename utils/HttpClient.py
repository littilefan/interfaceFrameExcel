import requests
import json

class HttpClient(object):
    def __init__(self):
        pass

    def request(self,requestUrl,requestMethod,paramsType,requestData,headers = None, cookies = None):
        #处理http请求，包括get、post
        if requestMethod.lower() == "post":
            if paramsType == "form":
                response = self.__post(requestUrl, data = json.dumps(requestData), headers = headers)
                return response
            elif paramsType == "json":
                response = self.__post(requestUrl, json = json.dumps(requestData), headers = headers, cookies = cookies)
                return response
        elif requestMethod.lower() == "get":
            if paramsType == "url":
                requestUrl = "%s%s" %(requestUrl,requestData)
                response = self.__get(requestUrl, headers = headers, cookies = cookies)
                return response
            elif paramsType == "params":
                response = self.__get(requestUrl, params = requestData, headers=headers, cookies=cookies)
                return response
        elif requestMethod.lower() == "put/delete/head...":
            pass
    # 私有方法post,私有方法不能再加其他修饰
    def __post(self, url, data = None, json = None, **kwargs):
        # 处理post类各种情况的请求
        response = requests.post(url, data = data, json = json, **kwargs)
        return response

    # 私有方法get
    def __get(self, url, params = None, **kwargs):
        # 处理get类各种情况的请求
        response = requests.get(url, params = params, **kwargs)
        return response

if __name__ == "__main__":
    hc = HttpClient()
    res = hc.request("http://39.100.104.214:8080/register/","post","form",
               eval('{"username":"fan110202","password":"fan1102123","email":"fan@qq.com"}'))
    print(res.status_code)
    print(res.json())

