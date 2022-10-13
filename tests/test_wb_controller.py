import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from c import *

def test_verify_user():
    print(verifyUser_("santicr21", "21"))
    print(verifyUser_("santicr", "1"))

def test_delete_cart_item():
    deleteCartItem_(10, "santicr21")
    deleteCartItem_(11, "santicr21")

def main():
    test_delete_cart_item()

main()