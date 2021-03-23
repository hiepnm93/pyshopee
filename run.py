import os 
import sys 
import multiprocessing as mp
import codecs
import requests

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from hiepnm import fileDirectory
from hiepnm import util

def downloadData(*arguments):
    nameShop = arguments[0][1]
    items = arguments[2][1]
    shopId = arguments[1][1]
    directory = "shop/" + nameShop
    fileDirectory.checkAndCreadDirectory(directory)
    listShopAndItem = {}
    for x in items:
        listShopAndItem[x] = util.getItem(x, shopId)
        
    for x in items:
        for y in listShopAndItem[x]["item"]["images"]:
            print("https://cf.shopee.vn/file/" + y)
            saveImage(directory+ "/" +str(y) + ".jpg", "https://cf.shopee.vn/file/" + y)
        #print(x, listShopAndItem[x]["item"]["description"])
        #print("https://cf.shopee.vn/file/" + listShopAndItem[x]["item"]["images"])
        #saveImage(directory+ "/" + str(x) + listShopAndItem[x]["item"]["images"] + ".jpg", "https://cf.shopee.vn/file/" + listShopAndItem[x]["item"]["images"])
        # f = codecs.open(directory + "/" +nameShop+  str(x) +".txt", "w")
        # f.write(listShopAndItem[x]["item"]["description"])
        # f.close()
    #print("Done")
def saveImage(directory, pic_url):
    with open(directory, 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

if __name__ == '__main__':
    pool = mp.Pool(processes=4)
    try:
        f = open("list_url_shop.txt")
        listURLShop = f.readlines()
        results = pool.map_async(util.shopIdFromID,listURLShop)
        listInfoShop = results.get()
        rInfPool = pool.starmap_async(util.searchItemsShopee,listInfoShop)
        listID = rInfPool.get()
        listShopAndID = []
        for x in listID:
            objShop = dict()
            objShop["name"] = x[2]
            objShop["shopid"] = x[0]
            objShop["items"] = []
            for y in x[1]:
                objShop["items"].append(y["itemid"])
            listShopAndID.append(list(objShop.items()))
            
        rDownLoadPool = pool.starmap_async(downloadData,listShopAndID)
    except IOError:
        print("File list Shop khong the load")
    finally:
        f.close()
        pool.close()
        pool.join()

    #directory = "abc/cdf"
    #fileDirectory.checkAndCreadDirectory(directory)
