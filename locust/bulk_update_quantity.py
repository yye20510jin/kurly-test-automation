import random
import os
from cartPage import get_all_cart_products

def cart_quantity():
    all_products = get_all_cart_products()
    quantity = [product.get("quantity") for product in all_products if str(product.get("dealProductNo")) == str(os.environ.get("CART_DEAL_PRODUCT_NO"))]
    return quantity[0] if quantity else None
    
    
def bulk_update_cart_quantity(self):
    existing_quantity = cart_quantity()
    add_quantity = random.randint(1,10)
    
    change_url = "https://api.kurly.com/external-cart/v2/change"

    self.custom_headers.update({
         "referer":"https://www.kurly.com/cart",
         "Cookie" : self.custom_cookie
    })

    payload={
            "cartItems" : [{"dealProductNo": os.environ.get("CART_DEAL_PRODUCT_NO"), "quantity": add_quantity}]
        }
    
    with self.client.put(change_url,json=payload,headers = self.custom_headers, catch_response = True ) as response:
        if response.status_code == 200 : 
                try:
                     res_json = response.json()
                     data_content = res_json.get("data",{})
                     current_cart_items = data_content.get("cartItems",[])
                     product_no = payload.get("cartItems")[0].get("dealProductNo")
                     
                     expect_quantity = int(existing_quantity) + int(add_quantity)

                     for item in current_cart_items:
                          if str(item.get("dealProductNo")) == str(product_no) :
                                if int(item.get("quantity")) == expect_quantity:
                                    response.success()
                                else:
                                    response.failure(f"❌ 데이터 정합성 실패 - 상품 수량이 일치하지 않습니다. (기존 수량: {existing_quantity}, 추가 수량:{add_quantity} ➡️ 기대 수량:{expect_quantity}, 실제 수량:{item.get("quantity")}) ")
                
                except Exception as e:
                     response.failure(f"❌응답 데이터 파싱 실패 - {str(e)}")
        else : 
            if response.status_code == 0:
                error_reason = response.text if response.text else "Network Connection Refused (서버 꺼짐 등)"
                response.failure(f"❌네트워크 연결 실패 -> {error_reason}")
            else:
                response.failure(f"❌서버 응답 에러 -> 상태코드 : {response.status_code}")
