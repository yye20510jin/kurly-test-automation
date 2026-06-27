import os

def login_attempt(session):
    user_id = os.environ.get("MY_LOCAL_ID")
    user_pw = os.environ.get("MY_LOCAL_PW")

    login_url = "https://auth.kurly.com/login?addAddress=true"

    login_headers = {
        "referer" : "https://www.kurly.com/member/login",
    }

    login_payload = {
        "id": user_id,
        "password": user_pw,
        "clientCaptcha": False,
        "clientCaptchaAction": "login",
        "recaptchaToken": "",
        "recaptchaSiteKey": ""
    }

    try:
        login_res = session.post(login_url, json = login_payload, headers = login_headers, timeout = 5)
        if login_res.status_code == 200:
            return True
        else:
            print(f"❌ 로그인 실패: {login_res.status_code}")
            os._exit(1)
    except Exception as e:
        print(f"❌ 로그인 통신 에러: {e}")
        os._exit(1)