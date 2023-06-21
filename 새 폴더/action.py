import time

import pandas as pd
import requests

# 회원가입
# 반 변경

df = pd.read_excel('C:/Users/user/Desktop/새 폴더/2023.xlsm', sheet_name="데이터")
df = df.values.tolist()

errer = []
for i in df:
    # 회원가입
    url = "http://127.0.0.1:8000/user/registration/"
    if i[3] < 10:
        i[3] = "0" + str(i[3])
    email = str(i[1]) + str(i[2]) + str(i[3]) + "@gsm.hs.kr"
    password = "password" + str(i[1]) + str(i[2]) + str(i[3])

    data = {
        "email": email,
        "password1": password,
        "password2": password
    }
    response = requests.post(url, data=data)
    if response.status_code == 400:
        errer.append(str(i[1]) + str(i[2]) + str(i[3]))

    # 이름 변경
    c = str(i[1]) + str(i[2]) + str(i[3])
    url = "http://127.0.0.1:8000/user/rename/"+c
    data = {
        "name": str(i[4]),
        "Class": c
    }
    response = requests.post(url, data=data)
    if response.status_code == 400:
        errer.append(str(i[1]) + str(i[2]) + str(i[3]))

print(errer)
