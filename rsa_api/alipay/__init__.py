# -*- coding:utf-8 -*-
from Crypto import Signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_Cipher
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util import number
from Crypto.Util._number_new import ceil_div
from xml.dom.minidom import parseString
import Crypto
import base64
import binascii
import os


'''
   参考文档: 
   1. https://www.dlitz.net/software/pycrypto/api/current/
   2. https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html

   模块依赖: sudo easy_install pycrypto
'''

_private_rsa_key = None
_public_rsa_key = None
_public_rsa_key_ali = None

def module_init():
    module_path = os.path.dirname(__file__)
    priv_path = os.path.abspath(os.path.join(module_path, "rsa_private_key.pem"))
    pub_path = os.path.abspath(os.path.join(module_path, "rsa_public_key.pem"))
    pub_path_ali = os.path.abspath(os.path.join(module_path, "rsa_public_key_ali.pem"))

    prik = open(priv_path, "r").read()
    pubk = open(pub_path, "r").read()
    pubk_ali = open(pub_path_ali, "r").read()
    #print "prik: ", prik
    #print "pubk: ", pubk
    #print "pubk_ali: ", pubk_ali
    return (prik, pubk, pubk_ali)

_private_rsa_key, _public_rsa_key, _public_rsa_key_ali = module_init()

def ensure_utf8(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    return s

def base64ToString(s):
    try:
        return base64.decodestring(s)
    except binascii.Error, e:
        raise SyntaxError(e)
    except binascii.Incomplete, e:
        raise SyntaxError(e)

def stringToBase64(s):
    return base64.encodestring(s).replace("\n", "")

def encrypt_with_rsa_chunyu(msg):
    '''
    msg必须采用utf8编码
    '''
    msg = ensure_utf8(msg)

    key = RSA.importKey(_public_rsa_key)
    cipher = PKCS1_v1_5_Cipher.new(key)
    
    modBits = number.size(key.n)
    k = ceil_div(modBits,8) - 28 ## 11 # Convert from bits to bytes
    print "K: ", k

    msglen = len(msg)
    msg_encryted = ""
    start_idx = 0
    ## 处理过长的加密
    while msglen > 0:
        len1 = min([msglen, k])
        encrypt = cipher.encrypt(msg[start_idx: (start_idx + len1)])
        msg_encryted = msg_encryted + encrypt
        start_idx = start_idx + len1
        msglen = msglen - len1
    return stringToBase64(msg_encryted)

def decrypt_with_rsa_chunyu(msg):
    '''
    msg必须采用base64编码，　注意: base64编码的数据经过URLDecoder处理之后，可能不正确，其中的＋会变成' '
    '''    
    msg = base64ToString(msg)
    key = RSA.importKey(_private_rsa_key)
    cipher = PKCS1_v1_5_Cipher.new(key)
    
    modBits = number.size(key.n)
    k = ceil_div(modBits,8) # Convert from bits to bytes
    print "K: ", k

    msglen = len(msg)
    msg_encryted = ""
    start_idx = 0
    ## 处理过长的加密
    while msglen > 0:
        len1 = min([msglen, k])
        cleartext = cipher.decrypt(msg[start_idx: (start_idx + len1)], "")
        msg_encryted = msg_encryted + cleartext
        start_idx = start_idx + len1
        msglen = msglen - len1
    return msg_encryted

def sign_with_rsa_chunyu(msg):
    '''
    将msg使用当前文件中定义的_private_rsa_key来签名, 返回base64编码的字符串
    '''
    key = RSA.importKey(_private_rsa_key)
    h = SHA.new(msg)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    signature = stringToBase64(signature)
    return signature

def check_with_rsa_chunyu(msg, signature):
    '''
    使用当前文件中定义的_public_rsa_key来验证签名是否正确
    '''
    signature = base64ToString(signature)
    key = RSA.importKey(_public_rsa_key)
    h = SHA.new(msg)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, signature)

def check_with_rsa_ali(msg, signature):
    '''
    使用当前文件中定义的_public_rsa_key来验证签名是否正确
    '''
    signature = base64ToString(signature)
    key = RSA.importKey(_public_rsa_key_ali)
    h = SHA.new(msg)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, signature)

def getNodesText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def getNodeTextByTagName(node, tagName):
    selected = node.getElementsByTagName(tagName)
    if selected:
        return getNodesText(selected[0].childNodes)
    else:
        return ""

class AliNotifyData(object):
    def __init__(self, trade_no, out_trade_no, buyer_email, total_fee, gmt_payment, trade_status, subject):
        self.trade_no = trade_no
        self.out_trade_no = out_trade_no
        self.buyer_email = buyer_email

        self.total_fee = total_fee
        self.gmt_payment = gmt_payment
        self.trade_status = trade_status
        self.subject = subject
        
def parse_notify_data(data):
    '''
    通过minixml解析data
    '''
    dom = parseString(data)
    notify = dom.getElementsByTagName("notify")[0]
    trade_status = getNodeTextByTagName(notify, "trade_status") 
    if not (trade_status == "TRADE_FINISHED" or trade_status == "TRADE_SUCCESS"):
        return None

    trade_status = "TRADE_FINISHED"
    trade_no = getNodeTextByTagName(notify, "trade_no")
    out_trade_no = getNodeTextByTagName(notify, "out_trade_no")
    buyer_email = getNodeTextByTagName(notify, "buyer_email")
    total_fee = int(float(getNodeTextByTagName(notify, "total_fee")) * 100 + 0.5)
    
    gmt_payment = getNodeTextByTagName(notify, "gmt_payment")
    subject = getNodeTextByTagName(notify, "subject")

    return AliNotifyData(trade_no=trade_no, out_trade_no=out_trade_no, buyer_email=buyer_email, 
                         total_fee=total_fee, gmt_payment=gmt_payment, trade_status=trade_status, 
                         subject=subject)
    