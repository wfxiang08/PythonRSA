# -*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test.testcases import TestCase
from rsa_api.alipay import check_with_rsa_ali, encrypt_with_rsa_chunyu, decrypt_with_rsa_chunyu

class AliPay(TestCase):
    '''
    python manage.py test --settings=settings rsa_api.AliPay
    '''
    def testAliCheck1(self):
        sig = "BIJ6PnC6qkQVP9as1hoxbXVNY1ygP4+Ce5qFGN9YuOB0AGKqlqjVFzT8xSr3C5PJn1GbWD/wLDO/CV7mPXXalJ6QgEaslhiTzde7mucVnpYdlhz+SUFxWjnXMzr/JIDRHYUy0/Umw61VLF8WXP0QJo2DxjByMAgWL1CVgg2xSE4="
        notify_data = "notify_data=<notify><seller_email>springhealth@163.com</seller_email><partner>2088701531699317</partner><payment_type>1</payment_type><buyer_email>xiaostone01@163.com</buyer_email><trade_no>2012022808842226</trade_no><buyer_id>2088002567022260</buyer_id><quantity>1</quantity><total_fee>0.01</total_fee><use_coupon>N</use_coupon><is_total_fee_adjust>Y</is_total_fee_adjust><price>0.01</price><gmt_create>2012-02-28 16:39:18</gmt_create><out_trade_no>U5R174GR8M68OYU</out_trade_no><seller_id>2088701531699317</seller_id><subject>珍珠项链</subject><trade_status>WAIT_BUYER_PAY</trade_status><discount>0.00</discount></notify>"
        
        result =  check_with_rsa_ali(notify_data, sig)
        print result
        self.assertTrue(result)

    def testEnDecrypt(self):
        '''
            python manage.py test --settings=settings rsa_api.AliPay.testEnDecrypt
        '''        
        ##msg = "hello"
        msg = "notify_data=<notify><seller_email>no</seller_email><partner>2088701531699317</partner><payment_type>1</payment_type><buyer_email>xiaostone01@163.com</buyer_email><trade_no>2012022808842226</trade_no><buyer_id>2088002567022260</buyer_id><quantity>1</quantity><total_fee>0.01</total_fee><use_coupon>N</use_coupon><is_total_fee_adjust>Y</is_total_fee_adjust><price>0.01</price><gmt_create>2012-02-28 16:39:18</gmt_create><out_trade_no>U5R174GR8M68OYU</out_trade_no><seller_id>2088701531699317</seller_id><subject>no</subject><trade_status>WAIT_BUYER_PAY</trade_status><discount>0.00</discount></notify>"
        encrypt = encrypt_with_rsa_chunyu(msg)
        print encrypt
        
        clearText = decrypt_with_rsa_chunyu(encrypt)
        print "recovered: ", clearText
