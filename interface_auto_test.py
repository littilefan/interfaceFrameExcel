import requests
from config.public_data import *
from utils.ParseExcel import ParseExcel
from utils.HttpClient import HttpClient
from action.get_rely import GetRely
from action.data_store import RelyDataStore
from action.check_result import CheckResult
from action.write_test_result import write_result
import json
import os
import hashlib

def main():
    # 新建一个解析excel工具类的实例对象
    parseE = ParseExcel()
    parseE.loadWorkBook(FILEPATH)
    sheetObj = parseE.getSheetByName("API")

    # 获取Active列的列对象
    activeList = parseE.getColumn(sheetObj, API_active)
    for idx, cell in enumerate(activeList[1:], 2):  #去掉第一行，指定下标从2开始
        # print(idx,cell)
        if cell.value == "y":
            # 需要执行的接口所在行的行对象
            rowObj = parseE.getRow(sheetObj, idx)
            apiName = rowObj[API_apiName - 1].value
            requestUrl = rowObj[API_requestUrl - 1].value
            requestMethod =rowObj[API_requestMethod - 1].value
            paramsType = rowObj[API_paramsType - 1].value
            apiTestCaseFileName = rowObj[API_apiTestCaseFileName - 1].value

            # 下一步需要读取接口用例表，获取接口的测试用例
            caseSheetObj = parseE.getSheetByName(apiTestCaseFileName) # obj数据类型
            caseActiveObj = parseE.getColumn(caseSheetObj, CASE_active) # tuple 数据类型
            for c_idx, c_cell in enumerate(caseActiveObj[1:], 2):
                if c_cell.value == "y":
                    # 说明此case行需要被执行
                    caseRowObj = parseE.getRow(caseSheetObj, c_idx)
                    requestData = caseRowObj[CASE_requestData - 1].value
                    requestData = eval(requestData) if requestData else {}  #eval将字典数据的字符串当表达式来执行，返回执行结果字典，否则dumps时会报错
                    relyData = caseRowObj[CASE_relyData - 1].value
                    responseCode = caseRowObj[CASE_responseCode - 1].value
                    dataStore = caseRowObj[CASE_dataStore - 1].value
                    checkPoint = caseRowObj[CASE_checkPoint - 1].value

                    # 接口发送请求之前需要先做依赖数据的处理
                    if relyData:
                        requestData = GetRely.get(requestData, eval(relyData))

                    # 构造接口请求需要的数据
                    # response = requests.post(requestUrl, data=json.dumps(requestData))   #dumps将字典类型转换为json串

                    httpC = HttpClient()
                    response = httpC.request(requestUrl, requestMethod, paramsType, requestData)
                    http_code = response.status_code
                    print("response= ",response.json())

                    #下面是处理依赖数据存储
                    if http_code == responseCode:
                        if dataStore:
                            RelyDataStore.do(eval(dataStore), apiName, c_idx - 1, requestData, response.json())
                        else:
                            print("第%s个接口的第%s条用例不需要做依赖数据存储" % (idx - 1, c_idx - 1))
                    else:
                        print("第%s个接口的第%s条用例的状态码【%s】不符合预期值【%s】" %(idx - 1, c_idx - 1, http_code, responseCode))

                    # 下面进行校验点检测功能的实现
                    if checkPoint:
                        errInfo = CheckResult.check(response.json(), eval(checkPoint))
                        # print("errInfo= ",errInfo)
                        write_result(parseE, caseSheetObj, response.json(), errInfo, c_idx)

                    else:
                        print("第%s个接口的第%s条用例没有设置校验点！" % (idx - 1, c_idx - 1))
                else:
                    print("第%s个接口的第%s条用例被忽略执行！" %(idx - 1, c_idx - 1))
        else:
            print("第%s个接口被设置忽略执行！" %(idx - 1))


if __name__ == "__main__":
    main()
