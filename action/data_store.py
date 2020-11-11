from config.public_data import REQUEST_DATA,RESPONSE_DATA

class RelyDataStore(object):
    def __init__(self):
        pass
    # 存redis的两种参考格式
    # key = "register->1->username" value = "zhangsan"
    # key = "register->1->password" value = "zhangsan01"
    # key = "register->1" value = {"username": "zhangsan", "password": "zhangsan01"}

    #{"register": {"1": {"username": "zhangsan01", "password": "zhangsang111"}}} 自定义的存储格式
    @classmethod
    def do(self, storePoint, apiName, caseId, requestSource, responsSource):
        #{"request": ["username", "password"], "response": ["code"]} 表格中DataStore字段
        for key, value in storePoint.items():
            if key == 'request':
                #说明依赖的存储数据是来自于请求参数
                for i in value:
                    if i in requestSource:
                        if apiName not in REQUEST_DATA:
                            # 说明存储数据的结构还未生成，需要指明数据存储结构
                            REQUEST_DATA[apiName] = {str(caseId):{i:requestSource[i]}}
                        else:
                            # 说明存储数据结构中的最外层结构是存在的
                            if str(caseId) in REQUEST_DATA[apiName]:
                                REQUEST_DATA[apiName][str(caseId)][i] = requestSource[i]
                            else:
                                REQUEST_DATA[apiName][str(caseId)] = {i:requestSource[i]}
                    else:
                        print("请求参数中不存在字段"+i)
            elif key == 'response':
                # 说明依赖的存储数据是来自于响应body
                for j in value:
                    if j in responsSource:
                        if apiName not in RESPONSE_DATA:
                            # 说明存储数据的结构还未生成，需要指明数据存储结构
                            RESPONSE_DATA[apiName] = {str(caseId):{j:responsSource[j]}}
                        else:
                            # 说明存储数据结构中的最外层结构是存在的
                            if str(caseId) in RESPONSE_DATA[apiName]:
                                RESPONSE_DATA[apiName][str(caseId)][j] = responsSource[j]
                            else:
                                RESPONSE_DATA[apiName][str(caseId)] = {j:responsSource[j]}
                    else:
                        print("响应body中不存在字段"+j)
        # print('REQUEST_DATA = ', REQUEST_DATA)
        # print('RESPONSE_DATA = ', RESPONSE_DATA)

if __name__ == '__main__':
    r = {"username": "srwcc01", "password": "wse123wac1", "email": "wsddw@qq.com"}
    s = {"request": ["username", "password"], "response": ["userid"]}
    res = {"userid": 12, "code": "00"}
    RelyDataStore.do(s, "register", 1, r, res)

