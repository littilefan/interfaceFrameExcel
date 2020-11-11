import re

class CheckResult(object):
    def __init__(self):
        pass

    @classmethod
    def check(cls, responseObj, checkPoint):
        #自定义校验规则
        #{"code": "00", "userid": {"type": "N"},  "id": {"value": "^\d+$"}}  N整型S字符串
        errorKey = {} #存储校验失败的
        for key, value in checkPoint.items():
            sourceData = responseObj[key] if key in responseObj else ""
            if isinstance(value,str):
                #说明是等值校验
                if key in responseObj:
                    if not sourceData == value:
                        errorKey[key] = sourceData
                else:
                    errorKey[key] = "not exists"
            elif isinstance(value, dict):
                #说明是需要通过正则校验或数据类型校验
                if "type" in value:
                    #说明是数据类型校验
                    typeS = value["type"]
                    if typeS == "N":
                        #说明是整型
                        if not isinstance(sourceData, int):
                            errorKey[key] = sourceData
                    elif typeS == "S":
                        # 说明是字符串类型
                        if not isinstance(sourceData, str):
                            errorKey[key] = sourceData
                    elif typeS == "xxx":
                        pass
                elif "value" in value:
                    #说明是正则表达式校验
                    regStr = value["value"]
                    rg = re.match(regStr, "%s" %sourceData)  #为了健壮性，将sourceData强转字符串
                    if not rg:
                        errorKey[key] = sourceData
        return errorKey

if __name__ == "__main__":
    r = {"code": "01", "userid": 12, "id": "12"}
    c = {"code": "01", "userid": {"type": "N"}, "id": {"value": "\d+"}}
    print(CheckResult.check(r, c))
