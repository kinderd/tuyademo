# 从云开发项目获得的授权密钥
client_id = 'cy7mwgcjamcx5wjv1lvy'
secret = 'ca8be38333c648fbb0740a5b1f31cfaa'

# 各接口使用方请根据自身所在区域调用相应接口。
# 中国区 https://openapi.tuyacn.com  
# 美洲区 https://openapi.tuyaus.com  
# 欧洲区 https://openapi.tuyaeu.com   
# 印度区 https://openapi.tuyain.com

base = 'https://openapi.tuyacn.com'

# 签名算法函数
def calc_sign(msg,key):
  import hmac
  import hashlib

  sign = hmac.new(msg=bytes(msg, 'latin-1'),key = bytes(key, 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()
  return sign

import time
import requests
from requests.models import Response
t = str(int(time.time()*1000))
r = requests.get(base+'/v1.0/token?grant_type=1',
                 headers={
                    'client_id':client_id,
                    'sign':calc_sign(client_id+t, secret),
                    'secret':secret,
                    't':t,
                    'sign_method':'HMAC-SHA256',
                  })

res = r.json()['result']
print(res)

import json
import time
# get 请求函数
def GET(url, headers={}):

  t = str(int(time.time()*1000))
  default_par={
      'client_id':client_id,
      'access_token':res['access_token'],
      'sign':calc_sign(client_id+res['access_token']+t, secret),
      't':t,
      'sign_method':'HMAC-SHA256',  
      }
  r = requests.get(base + url, headers=dict(default_par,**headers))

  r = json.dumps(r.json(), indent=2, ensure_ascii=False) # 美化request结果格式，方便打印查看
  return r

# post 请求函数
def POST(url, headers={}, body={}):
  import json
  t = str(int(time.time()*1000))

  default_par={
      'client_id':client_id,
      'access_token':res['access_token'],
      'sign':calc_sign(client_id+res['access_token']+t, secret),
      't':t,
      'sign_method':'HMAC-SHA256',  
      }
  r = requests.post(base + url, headers=dict(default_par,**headers), data=json.dumps(body))

  r = json.dumps(r.json(), indent=2, ensure_ascii=False) # 美化request结果格式，方便打印查看
  return r
  # 云开发项目里关联设备的ID
device_id = 'vdevo162218846176019'#彩灯四路
r = GET(url=f'/v1.0/devices/{device_id}/status')#状态集
print(r)
r = GET(url=f'/v1.0/devices/{device_id}/functions')#指令集
print(r)
r = GET(url=f'/v1.0/devices/{device_id}/specifications') #指令集状态集
# 根据该设备的控制指令集组装参数
d = {"commands":[{"code":"temp_set","value":18},]}
r=POST(url=f'/v1.0/devices/{device_id}/commands', body=d)
#延时执行程序
time.sleep(5)
d = {"commands":[{"code":"mode","value":"hot"},]}
r=POST(url=f'/v1.0/devices/{device_id}/commands', body=d)
print(r)