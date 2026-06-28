import os

cart_res = None

def move_cart(session):
    global cart_res
    cart_url = "https://api.kurly.com/external-cart/v4/detail"
    try:
        payload = {
            "address" : "",
            "addressDetail" : ""
        }

        cart_res = session.post(cart_url,json = payload, timeout = 5)
        if cart_res.status_code == 200:
            return True
        else: 
            print(f"❌ 장바구니 접근 실패: {cart_res.status_code}")
            os._exit(1)
    except Exception as e:
        print(f"❌ 장바구니 통신 에러: {e}")
        os._exit(1)

def get_all_cart_products():
    res_json = cart_res.json() if hasattr(cart_res, 'json') else cart_res
    
    data = res_json.get("data",{})
    kurly_delivery = data.get("kurlyDelivery",{})
    storage_types = kurly_delivery.get("storageTypes",[])

    all_products = []

    for storage in storage_types:
        products = storage.get("products",[])
        all_products.extend(products)
    return all_products
        

