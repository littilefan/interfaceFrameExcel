import os

# 整个项目的根目录绝对路径
BASEDTR = os.path.dirname(os.path.dirname(__file__))  #__file__当前文件

# 测试数据文件excel的绝对路径
FILEPATH = BASEDTR + "\\TestData\\inter_test_data.xlsx"

API_apiName = 2
API_requestUrl = 3
API_requestMethod = 4
API_paramsType = 5
API_apiTestCaseFileName = 6
API_active = 7

CASE_requestData = 1
CASE_relyData = 2
CASE_responseCode = 3
CASE_responseData = 4
CASE_dataStore = 5
CASE_checkPoint = 6
CASE_active = 7
CASE_status = 8
CASE_errorInfo = 9

#自定义case执行完后数据存储的格式，即怎么存的；DataStore只是说明存哪些字段，具体怎么存不管；不是一回事
#{"接口名":{"用例编号":{"username":"xxx", "password": "xxx"}},
#"register":{"1":{"username":"zhangsan01", "password":"zhangsang111"}}
#}
REQUEST_DATA = {} # 存request
RESPONSE_DATA = {} # 存response