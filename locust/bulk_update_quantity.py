import random
import os
import json

    
def bulk_update_cart_quantity(self):
    
    change_url = "https://api.kurly.com/external-cart/v2/change"

    change_headers = self.session.headers.copy()
    cookie_dict = self.session.cookies.get_dict()
    cookie_str = "; ".join([f"{k} = {v}" for k,v in cookie_dict.items()])

    change_headers.update({
         "referer":"https://www.kurly.com/cart",
         "Cookie" : cookie_str
    })

    payload={
            "cartItems" : [{"dealProductNo": os.environ.get("CART_DEAL_PRODUCT_NO"), "quantity": random.randint(1,10)}]
        }

    print(f"\n🚀 [요청 발송] 보낸 데이터: {json.dumps(payload, ensure_ascii=False)}")
    
    with self.client.put(change_url,json=payload,headers = change_headers, catch_response = True ) as response:
        if response.status_code == 200 : 
                response.success()
        else : 
            if response.status_code == 0:
                error_reason = response.text if response.text else "Network Connection Refused (서버 꺼짐 등)"
                response.failure(f"❌네트워크 연결 실패 -> {error_reason}")
            else:
                response.failure(f"❌서버 응답 에러 -> 상태코드 : {response.status_code}")
                response.failure(f"❌서버 응답 메세지  -> {response.text}")