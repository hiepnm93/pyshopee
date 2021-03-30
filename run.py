# encoding: utf-8
import os 
import sys 
import multiprocessing as mp
import codecs
import requests
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from pyshopee import fileDirectory
from pyshopee import util


def downloadData(*arguments):
    try:
        nameShop = arguments[2]
        items = arguments[1]
        shopId = arguments[0]
        directory = "shop/" + nameShop
        fileDirectory.checkAndCreadDirectory(directory)
        listShopAndItem = {}
        f = open("shop/"+str(nameShop)+".txt", "a", encoding="utf-8")
        
        for x in items:
            
            try:
                infoItemFull = util.getItem(x["itemid"], shopId)
            except:
                infoItemFull = []
                print("error")
            if(len(infoItemFull) == 0):
                break
            try:
                strImage = ",".join(x["images"])
            except:
                break
            
            f.writelines(str(x["itemid"]) + "|" + str(strImage))

            f.writelines(str(x["itemid"]) + "|" + x["name"] + "|" + (infoItemFull["item"]["description"] ))    
            for y in x["images"]:
                if(len(str(y)) < 32):
                    print(x["itemid"])
                else:
                    print("https://cf.shopee.vn/file/" + y)
                    saveImage(directory+ "/" +str(y) + ".jpg", "https://cf.shopee.vn/file/" + y)
            
        print("Done")
    except :
        print(sys.exc_info())
    finally:
        f.close()

def saveImage(directory, pic_url):
    try:
        with open(directory, 'wb') as handle:
            response = requests.get(pic_url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    except :
        e = sys.exc_info()[0]
        print( "<p>Error saveImage : %s</p>" % e )

if __name__ == '__main__':
    
    try:
        f = open("list_url_shop.txt")
        listURLShop = f.readlines()
        f.close()

        pool = mp.Pool(processes=12)
        results = pool.map_async(util.shopIdFromID,listURLShop)
        listInfoShop = results.get()
        pool.close()
        pool.join()


        pool = mp.Pool(processes=12)
        rInfPool = pool.starmap_async(util.getAllItemsShopee,listInfoShop)
        listID = rInfPool.get()
        pool.close()
        pool.join()


        with open('data.txt', 'w') as outfile:
            json.dump(listID, outfile)

        pool = mp.Pool(processes=12)
        rDownLoadPool = pool.starmap_async(downloadData,listID)
        pool.close()
        pool.join()
    except:
        e = sys.exc_info()[0]
        print( "<p>Error __main__ : %s</p>" % e )

    #directory = "abc/cdf"
    #fileDirectory.checkAndCreadDirectory(directory)
