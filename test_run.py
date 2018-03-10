from CompanyInfor import CompanyInfor
from BYSModel import BYSModel
from collections import Counter


test_list = [
    "中国移动通信集团四川有限公司",
    "吉林市群龙科技有限公司",
    "北京大成律师事务所武汉分所",
    "大连万达集团商业管理有限公司",
    "腾冲恒益矿产实业有限公司",
    "四川智博联想物流有限公司",
    "北京百度网讯科技有限公司",
    "北京摩拜科技有限公司",
    "天津一汽丰田汽车有限公司",
]


model = BYSModel()
fenciku, countVectorizer, textVector = model.modelData()

for eve in test_list:
    company = CompanyInfor()
    companyInfor = company.getCompanyInfor(company.getCompanyUrl(eve))
    if "未公开" in companyInfor:
        print(eve, "无法分类")
    else:
        temp_data = companyInfor.split("；")
        category = model.predictModel(model.setModel(textVector, fenciku),temp_data, countVectorizer)
        print(eve,Counter(category))

