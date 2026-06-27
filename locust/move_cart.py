import os

def move_cart(session):
    cart_url = "https://www.kurly.com/cart"

    try:
        cart_res = session.get(cart_url, timeout = 5)
        if cart_res.status_code == 200:
            return True
        else: 
            print(f"❌ 장바구니 접근 실패: {cart_res.status_code}")
    except Exception as e:
        print(f"❌ 장바구니 통신 에러: {e}")
        os._exit(1)
