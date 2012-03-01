@csrf_exempt
def alipay_notify(request):
    def ensure_utf8(s):
        if isinstance(s, unicode):
            return s.encode('utf8')
        return s

    notify_data = ensure_utf8(request.POST.get("notify_data", ""))
    sign = ensure_utf8(request.POST.get("sign", ""))
    content = ensure_utf8("notify_data=" + notify_data)
    
    sign_result = check_with_rsa_ali(content, sign)
    print "Sign valid: ", sign_result
    print "Sign: ", sign
    print "Content: ", content
      
    if sign_result:
        alipay = parse_notify_data(notify_data)
        if alipay and alipay.trade_status == "TRADE_FINISHED":
            ## TODO: 服务器进行商品买卖
            
            return HttpResponse(content="success", mimetype="application/json; charset=UTF-8")

    return HttpResponse(content="", mimetype="application/json; charset=UTF-8")