import requests
import re
import hashlib
import json
import sys
def getUserNameShopeeFromLinkShop(link_shopee):
    try:
        x = re.match("^(https:\/\/shopee\.vn\/)([a-zA-Z0-9_]+)", link_shopee)
        return x.group(2)
    except :
        return ""

def renderIfNoneMatch(strIfNM, first = "55b03"):
    m = hashlib.md5()
    m.update(bytearray(first + strIfNM + first, "utf8") )
    return m.hexdigest()

def md5(strIfNM):
    m = hashlib.md5()
    m.update(bytearray(strIfNM, "utf8") )
    return m.hexdigest()

def shopIdFromID(link_shopee):
    try:
        user_name = getUserNameShopeeFromLinkShop(link_shopee)
        url = "https://shopee.vn/api/v4/shop/get_shop_detail?username=" + user_name
        payload={}
        headers = {
            "authority": "shopee.vn",
            "x-shopee-language": "vi",
            "dnt": "1",
            "if-none-match-": renderIfNoneMatch("username=" + user_name),
            "x-requested-with": "XMLHttpRequest",
            "user-agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "x-api-source": "pc",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://shopee.vn/" + user_name,
            "accept-language": "vi,vi-VN;q=0.9",
        }
        

        response = requests.request("GET", url, headers=headers, data=payload)
        get_shop_detail_object = json.loads(response.text)
        shopid  = get_shop_detail_object["data"]["shopid"]
        item_count  = get_shop_detail_object["data"]["item_count"]
        return shopid, item_count, user_name, get_shop_detail_object["data"]
    except :
        e = sys.exc_info()[0]
        print( "<p>Error shopIdFromID: %s</p>" % e )
        return "", ""

def searchItemsShopee(*arguments):
    shopid = arguments[0]
    start_number = 0
    end_number = arguments[1] -1
    shopName = arguments[2]
    try:
        url_searchItems = "https://shopee.vn/api/v2/search_items/?"
        urlGetListProduce = "by=pop&order=desc&page_type=shop&version=2&limit=" + str((end_number) - (start_number) + 1) + "&match_id=" + str(shopid) + "&newest=" + str((start_number) - 1)
        headers = {
            "authority": "shopee.vn",
            "x-shopee-language": "vi",
            "dnt": "1",
            "x-requested-with": "XMLHttpRequest",
            "if-none-match-": renderIfNoneMatch(urlGetListProduce),
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "x-api-source": "pc",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://shopee.vn",
            "accept-language": "vi,vi-VN;q=0.9"
        }
        payload= {}
        response = requests.request("GET", url_searchItems+urlGetListProduce, headers=headers, data=payload)
        
        get_iteam_detail_object = json.loads(response.text)
        return shopid, get_iteam_detail_object["items"], shopName
    except :
        e = sys.exc_info()[0]
        print( "<p>Error searchItemsShopee : %s</p>" % e )
        return shopid, [], shopName

def getItem(itemid, shopid):
    url_searchItems = "https://shopee.vn/api/v2/item/get?"
    urlGetListProduce = "itemid=" + str(itemid) + "&shopid=" + str(shopid)
    url = url_searchItems + urlGetListProduce
    headers = {
        "authority": "shopee.vn",
        "x-shopee-language": "vi",
        "dnt": "1",
        "x-requested-with": "XMLHttpRequest",
        "if-none-match-": "55b03-" + renderIfNoneMatch(md5(urlGetListProduce)),
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "x-api-source": "pc",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "vi,vi-VN;q=0.9",
    };
    payload= {}
    try:
        response = requests.request("GET",url, headers=headers, data=payload)
        get_iteam_detail_object = json.loads(response.text)
        return get_iteam_detail_object
    except :
        e = sys.exc_info()[0]
        print( itemid, shopid )
        print( "<p>Error getItem : %s</p>" % e )
        return []
