import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from c import *

#Func 1
def test_verify_user_statement():
    verifyUser_("santicr21", "21")
    verifyUser_("santicr", "1")

def test_verify_user_decision():
    verifyUser_("santicr21", "21")
    verifyUser_("santicr", "1")
    verifyUser_("santicr", "12")

#Func 2
def test_delete_cart_item_statement():
    deleteCartItem_("10", "santicr21")
    deleteCartItem_("11", "santicr21")

def test_delete_cart_item_decision():
    deleteCartItem_("10", "santicr21")
    deleteCartItem_("11", "santicr21")

#Func 3
def test_verify_pay_cart_statement():
    verifyPayCart_(10, 1)
    verifyPayCart_(11, 1)

def test_verify_pay_cart_decision():
    verifyPayCart_(10, 1)
    verifyPayCart_(11, 1)

#Func 4
def test_exist_user_statement():
    existUser_("adsad")
    existUser_("santicr21")

def test_exist_user_decision():
    existUser_("adsad")
    existUser_("santicr21")

#Func 5
def test_verify_user_passw_statement():
    verifyUserPassword_("admin")
    verifyUserPassword_("Admin1234@")

def test_verify_user_passw_decision():
    verifyUserPassword_("admin")
    verifyUserPassword_("Admin1234@")
    verifyUserPassword_("admin1234")

#Func 6
def test_discount_statement():
    discount_("52345678901230", "12", 10000)

def test_discount_desicion():
    discount_("52345678901230", "12", 10000)
    discount_("12345678901233", "11", 10000)

test_discount_desicion()