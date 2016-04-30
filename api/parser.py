from dragline.parser import HtmlParser
from dragline.http import Request, RequestError
import re
import json

def parse(url):
	
	request_headers = {"Accept-Encoding":"gzip","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"}
	response = Request(url,headers=request_headers).send().text
	print "processed : ",url
	parser=HtmlParser(response)
	raw_price1 = parser.xpath("//span[@id='priceblock_saleprice']/text()")
	raw_price2 = parser.xpath("//span[@id='priceblock_ourprice']/text()")
	raw_availability = parser.xpath("//div[@id='availability']//text()")
	raw_name = parser.xpath("//h1//text()")
	raw_brand = parser.xpath("//a[@id='brand']//text()")
	raw_img = parser.xpath("//div[@class='imgTagWrapper']//img/@data-a-dynamic-image")
	if raw_img:
		img = json.loads(raw_img[0]).keys()[0]
	else:
		img = '' 
	name = ''.join(raw_name).strip()
	price=0.0
	if raw_price1:
		price = float(raw_price1[0].replace(',','').strip())
	if raw_price2:
		price = float(raw_price2[0].replace(',','').strip())
	
	brand = ''.join(raw_brand).strip()
	availability = ''.join(raw_availability).strip()
	raw_product_id = re.findall("dp/([A-Z0-9]{,10})",url)
	if raw_product_id:
		product_id = raw_product_id[0]
	elif raw_product_id :
		product_id = re.findall("product/(.*)/ref",url)[0]
	else:
		product_id = re.findall("product/(.*)",url)[0]

	data={
			"price":price,
			"availability":availability,
			"product_id":product_id,
			"name":name,
			"image":img,
			"brand":brand
		}
	return data