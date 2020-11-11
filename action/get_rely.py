from utils.md5_encrypt import md5_encrypt
from config.public_data import REQUEST_DATA, RESPONSE_DATA
# REQUEST_DATA = {} # request
# RESPONSE_DATA = {} # response

# case执行后数据存储时怎么存的格式；datastore只是说明存哪些，具体怎么存不管；不是一回事
# {"接口名":{"用例编号":{"username":"xxx", "password": "xxx"}},
# "register":{"1":{"username":"zhangsan01", "password":"zhangsang111"}}
# }

#relyData
# "{""request"":{""username"":""register->1"",""password"":""register->1""},
# ""response"":{""userid"":""login->1"", ""token"":""login-1""}
# }"

#处理依赖的类
class GetRely(object):
    def __init__(self):
        pass

    @classmethod
    def get(cls, dataSource, relyData): #根据原始requestdata+relydata得到最终请求参数requestdata
        dataS = dataSource.copy()     #原始数据requestdata不动
        for key, value in relyData.items():
            if key == "request":
                # 说明应该去REQUEST_DATA获取数据
                for k, v in value.items():
                    interfaceName, case_id = v.split("->")
                    try:
                        val = REQUEST_DATA[interfaceName][case_id][k]
                        if k == "password":
                            dataS[k] = md5_encrypt(val)
                        else:
                            dataS[k] = val
                    except Exception as err:
                        pass
            elif key == "response":
                # 说明需要去RESPONSE_DATA获取数据
                for k, v in value.items():
                    interfaceName, case_id = v.split("->")
                    try:
                        dataS[k] = RESPONSE_DATA[interfaceName][case_id][k]
                    except Exception as err:
                        pass
        return dataS

if __name__ == "__main__":
    #数据量大时，存redis时的格式
    #{"request-用户注册->1":{"username": "zhangsan", "password": "zhangsan01"}}
    REQUEST_DATA = {"用户注册": {"1": {"username": "zhangsan", "password": "zhangsan01"}}}  # request
    RESPONSE_DATA = {}  # response
    s = {"username": "", "password": ""}   #原始数据
    rely = {"request": {"username": "用户注册->1", "password": "用户注册->1"}} #依赖数据
    print(GetRely.get(s, rely))