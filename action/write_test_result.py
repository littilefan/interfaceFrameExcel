from config.public_data import *

def write_result(wbObj, sheetObj, responseData, errorKey, rowNum):
    try:
        # 写响应body
        wbObj.writeCell(sheet = sheetObj, content = "%s" %responseData,
                        rowNo = rowNum, colsNo = CASE_responseData)
        # 写校验结果状态及错误信息列
        if errorKey:
            wbObj.writeCell(sheet = sheetObj, content = "failed",
                            rowNo = rowNum, colsNo = CASE_status)
            wbObj.writeCell(sheet = sheetObj, content = "%s" %errorKey,
                            rowNo = rowNum, colsNo = CASE_errorInfo)
        else:
            wbObj.writeCell(sheet = sheetObj, content = "pass",
                            rowNo = rowNum, colsNo = CASE_status)
            wbObj.writeCell(sheet = sheetObj, content = "",
                            rowNo = rowNum, colsNo = CASE_errorInfo)
    except Exception as err:
        raise err