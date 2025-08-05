import requests
from Crypto.Cipher import AES
import base64
import json

# 固定IV和初始密钥
FIXED_IV = b'UQchmmrXQhbPVqOl'
INITIAL_KEY = b'UQchmmrXQhbPVqOl'

def pkcs7_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

def pkcs7_pad(data: bytes) -> bytes:
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def aes_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return pkcs7_unpad(decrypted).decode('utf-8')

def aes_cbc_encrypt(plaintext: str, key: bytes, iv: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pkcs7_pad(plaintext.encode('utf-8'))
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode('utf-8')

# Step 1: 获取初始数据并解密
json_data1 = {
    'method': 'SidFilter',
    'str': '0H4UhCHQ8j40NGKx2Ghieg==',
}

resp = requests.post(
    'https://www.sva.org.cn/SZWSLDServer/restservices/api/WSLDCloudWebRestT/query',
    json=json_data1
)

if resp.status_code != 200 or not resp.text:
    raise Exception("初始请求失败")

# 解密第一步响应
data = resp.text
datatype = resp.headers.get('datatype')
if not datatype:
    raise Exception("响应头中无datatype")

datatype_int = int(datatype)
t = (datatype_int // 16) - 2
o = datatype_int % 16

s = data
key_block = s[t:t+32]
iv_str = key_block[o:o+16]
iv = iv_str.encode('utf-8')
encrypted_payload = s[:t] + s[t+32:]

try:
    encrypted_bytes = base64.b64decode(encrypted_payload)
except:
    encrypted_bytes = bytes.fromhex(encrypted_payload)

decrypted_json_str = aes_cbc_decrypt(encrypted_bytes, INITIAL_KEY, iv)
decrypted_data = json.loads(decrypted_json_str)

# 提取 LSID 和 key
LSID = decrypted_data["result"]["result"]["key"]
key = decrypted_data["result"]["result"]["value"]

# Step 2: 构造查询项目的加密请求，通过改变pagesize的数值以改变爬取的项目的数量
query_dict = {
    "pagesize": 2,
    "pagenum": 1,
    "areaid": "440300000000000000",
    "prosubject": "",
    "ordertype": "",
    "isfull": "",
    "timestype": "",
    "joinlevel": "",
    "protype": "0",
    "minage": "",
    "maxage": "",
    "start": "",
    "end": "",
    "projectname": "",
    "status": "0",
    "dataform": "Web",
    "tocount": False
}

query_json_str = json.dumps(query_dict, separators=(',', ':'))
encrypted_query = aes_cbc_encrypt(query_json_str, key.encode('utf-8'), FIXED_IV)

# Step 3: 发送项目请求
headers2 = {
    'sid': LSID
}

json_data2 = {
    'method': 'wsld_projectPage',
    'str': encrypted_query,
}

project_resp = requests.post(
    'https://www.sva.org.cn/SZWSLDServer/restservices/api/WSLDCloudWebRestT/query',
    headers=headers2,
    json=json_data2,
)

if project_resp.status_code != 200 or not project_resp.text:
    raise Exception("项目请求失败")

# Step 4: 解密项目响应
project_data = project_resp.text
datatype = project_resp.headers.get('datatype')
if not datatype:
    raise Exception("项目响应中无datatype")

datatype_int = int(datatype)
t = (datatype_int // 16) - 2
o = datatype_int % 16

s = project_data
key_block = s[t:t+32]
iv_str = key_block[o:o+16]
iv = iv_str.encode('utf-8')
encrypted_payload = s[:t] + s[t+32:]

try:
    encrypted_bytes = base64.b64decode(encrypted_payload)
except:
    encrypted_bytes = bytes.fromhex(encrypted_payload)

decrypted_project_str = aes_cbc_decrypt(encrypted_bytes, key.encode('utf-8'), iv)
decrypted_project_json = json.loads(decrypted_project_str)

# Step 5: 输出项目数据
print(json.dumps(decrypted_project_json, indent=2, ensure_ascii=False))
