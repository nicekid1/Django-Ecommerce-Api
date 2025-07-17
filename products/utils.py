from django.conf import settings
import requests
import json


ZP_API_REQUEST = f"https://{'sandbox' if settings.SANDBOX else 'www'}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{'sandbox' if settings.SANDBOX else 'www'}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{'sandbox' if settings.SANDBOX else 'www'}.zarinpal.com/pg/StartPay/"

def send_request(amount, description, callback_url, phone=''):
    data = {
    "merchant_id": settings.MERCHANT,
    "amount": amount,
    "description": description,
    "callback_url": callback_url,
    "metadata": {
        "mobile": "09120000000"
      }
    }

    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            print(response)
            if response.get("data", {}).get("code") == 100:
                authority = response.get(data,{}).get("authority")
                print(authority)
                return {
                    'status': True,
                    'url': ZP_API_STARTPAY + str(authority),
                    'authority': authority
                }
            else:
                return {'status': False, 'code': str(response['Status'])}
        return {'status': False, 'code': 'request failed'}
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}

def verify_payment(amount, authority):
    data = {
        "merchant_id": settings.MERCHANT,  
        "amount": amount,
        "authority": authority,
    }
    print(authority)
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json', 'Content-Length': str(len(data_json))}

    try:
        response = requests.post(ZP_API_VERIFY, data=data_json, headers=headers)
        response.raise_for_status()  
        result = response.json()

        status = result.get('data', {}).get('code') or result.get('Status') or result.get('status')
        ref_id = result.get('data', {}).get('ref_id') or result.get('RefID') or result.get('refID')

        if status == 100:
            return {'status': True, 'RefID': ref_id}
        else:
            return {'status': False, 'code': str(status)}
    except requests.exceptions.RequestException as e:
        return {'status': False, 'code': 'request_failed', 'error': str(e)}
    except ValueError:
        return {'status': False, 'code': 'invalid_response'}