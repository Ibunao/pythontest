from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '15706468'
API_KEY = 'ObzUMqNa4NinfbjS93LvqCtB'
SECRET_KEY = 'B6lMPGeZ32MzMqCDKc1A65glcfBfhF6b'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result  = client.synthesis('你好百度', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)