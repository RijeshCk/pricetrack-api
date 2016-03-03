from rest_framework import serializers
 
class ProductSerializer(serializers.Serializer):
	crawl_date = serializers.DateTimeField(auto_now_add=True)
	product_name = serializers.CharField(max_length=200,blank=True,)
	product_price =serializers.DoubleField()
	product_url = serializers.URLField(max_length=200, min_length=None, allow_blank=False)
	product_id = serializers.CharField()  
	procuct_extra_data = serializers.DictField(child=CharField())
	