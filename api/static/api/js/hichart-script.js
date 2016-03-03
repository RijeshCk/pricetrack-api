function Test(id){
$(function () {
								var processed_json = new Array();   
														var k=new Array(),d;
														var j =new Array();
														id=$(id).attr("data")
														console.log('http://127.0.0.1:8000/pricehistory/id='+id+'?format=json')
								$.getJSON('http://127.0.0.1:8000/pricehistory/id='+id+'?format=json', function(data) {
										// Populate series
										$.each(data,function(key,val)
												{   

													var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
													d = new Date(val.date).getDate()+' '+month[new Date(val.date).getMonth()]


														f=d
														if(val.price=='')
															{
																k.push(null)
															}
															else{ 
														k.push(parseFloat(val.price.replace(',','')));
														}
														j.push(f);
														console.log(k)
														processed_json.push(k);
														k=[]
												});
	 
						}).success(function() { 
						// draw chart
										$('#container').highcharts({
										chart: {
												type: "line"
										},
										chart: {
								zoomType: 'x'
						},
								
										title: {
												text: ""
										},
										xAxis: {
											tickInterval: 5,
												gridLineWidth: .1,
												crosshair:true,
												categories:j,
												allowDecimals: true,
												title: {
																text: "date"
																},
						
				
										},
										yAxis: {
												allowDecimals: true,
												title: {
														text: "Price"
												},
												tickInterval: 1000,
										plotLines: [{
								value: 0,
								width: .001,
								color: '#808080'


						}]
										},credits: {
												enabled: false
												 },

										 

										 tooltip: {
	 
						shared: true,
						crosshairs: true
				},
										series: [{
												name: 'Price',
												data: processed_json,
										}]
								}); })




.error(function() {  
	$('#container').highcharts().destroy();
	$('#container').html('no data');
	});
						
				});
}