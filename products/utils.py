from django.conf import settings
import requests
import json


ZP_API_REQUEST = f"https://{'sandbox' if settings.SANDBOX else 'www'}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{'sandbox' if settings.SANDBOX else 'www'}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{'sandbox' if settings.SANDBOX else 'www'}.zarinpal.com/pg/StartPay/"

def send_request(amount, description, callback_url, phone=''):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "CallbackURL": callback_url,
        "Phone": phone,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        print(response)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {
                    'status': True,
                    'url': ZP_API_STARTPAY + str(response['Authority']),
                    'authority': response['Authority']
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
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return {'status': False, 'code': 'request failed'}
