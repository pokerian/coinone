import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
ACCESS_TOKEN = config["COINONE_V2"]["ACCESS_TOKEN"]
SECRET_KEY = config["COINONE_V2"]["SECRET_KEY"]

URL = 'https://api.coinone.co.kr/v2/account/user_info/'
PAYLOAD = {
  "access_token": ACCESS_TOKEN,
}

def get_encoded_payload(payload):
  payload[u'nonce'] = int(time.time()*1000)

  dumped_json = json.dumps(payload)
  encoded_json = base64.b64encode(dumped_json)
  return encoded_json

def get_signature(encoded_payload, secret_key):
  signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
  return signature.hexdigest()

def get_response(url, payload):
  encoded_payload = get_encoded_payload(payload)
  headers = {
    'Content-type': 'application/json',
    'X-COINONE-PAYLOAD': encoded_payload,
    'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
  }
  http = httplib2.Http()
  response, content = http.request(URL, 'POST', headers=headers, body=encoded_payload)
  return content

def get_result():
  content = get_response(URL, PAYLOAD)
  content = json.loads(content)

  return content

if __name__   == "__main__":
    dic = get_result()

    for k1 in dic.iterkeys():
        if k1 == 'userInfo':
            for k2 in dic[k1].iterkeys():
                if k2 == 'mobileInfo':
                    print '\n[' + k2 + ']'
                    for k3, v3 in dic[k1][k2].iteritems():
                        print '\t' + k3 + ':' + v3
                if k2 == 'emailInfo':
                    print '\n[' + k2 + ']'
                    for k3, v3 in dic[k1][k2].iteritems():
                        print '\t' + k3 + ':' + v3