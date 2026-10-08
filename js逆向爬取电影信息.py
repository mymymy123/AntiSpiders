import hashlib  #提供sha1方法
import time
import base64  #能够进行base64编码
import requests
from typing import List,Any


'''
#hook函数
(function(){
    "use strict"
    function hook(object,attr){
        var func=object[attr]
        object[attr]=function(){
            console.log('hooked',object,attr,arguments)
            var ret = func.apply(object,arguments)
            debugger
            return ret
        }
    }
    hook('window','btoa')
})()
'''



INDEX_URL='https://spa6.scrape.center/api/movie/?limit={limit}&offset={offset}&token={token}'
DETAIL_URL='https://spa6.scrape.center/api/movie/{id}/?token={token}'
LIMIT=10
OFFSET=0
SECRET='ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'

def get_token(args:List[Any]):
    timestamp=str(int(time.time()))
    args.append(timestamp)
    #.encode('utf-8') 的作用：把 str → bytes，让 SHA1 能处理。
    sign=hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    #base64.b64encode() 也只接受 bytes,
    # .decode('utf-8')	bytes → str，因为最终要拼接到 URL 或 JSON 中传输
    return base64.b64encode(','.join([sign,timestamp]).encode('utf-8')).decode('utf-8')

args=['/api/movie']
token=get_token(args=args)
index_url=INDEX_URL.format(limit=LIMIT,offset=OFFSET,token=token)
response=requests.get(index_url)
result=response.json()
for item in result['results']:
    id=item['id']
    encrypt_id=base64.b64encode((SECRET+str(id)).encode('utf-8')).decode('utf-8')
    args=[f'/api/movie/{encrypt_id}']
    token=get_token(args=args)
    detail_url=DETAIL_URL.format(id=encrypt_id,token=token)
    response=requests.get(detail_url)
    print(response.json())
