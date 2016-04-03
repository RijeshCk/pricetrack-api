function Test(id){
$(function () {
								var processed_json = new Array();   
														var k=new Array(),d;
														var j =new Array();
														id=$(id).attr("data")
														
								$.getJSON('https://pricetrack-api.herokuapp.com/pricehistory/id='+id+'?format=json', function(data) {
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
														k.push(parseInt(val.price));
														}
														j.push(f);
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
												text: "Price history"
										},
										xAxis: {
											tickInterval: 5,
												// gridLineWidth: .1,
												// crosshair:true,
												categories:j,
												allowDecimals: true,
												title: {
															text: "date"
														},
												plotLines: [{
														value: 0,
														width: 1,
													}]
						
				
										},
										yAxis: {
												allowDecimals: true,
												title: {
														text: "Price"
												},
												tickInterval: 10,
										plotLines: [{
														value: 0,
														width: 1,
													}]
										},credits: {
												enabled: false
												 },

										 

										 tooltip: {crosshairs: [{
            width: 1.5,
            dashStyle: 'solid',
            color: 'gray'
        }, false]
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
/**
 * Grid-light theme for Highcharts JS
 * @author Torstein Honsi
 */

// Load the fonts
Highcharts.createElement('link', {
   href: '//fonts.googleapis.com/css?family=Dosis:400,600',
   rel: 'stylesheet',
   type: 'text/css'
}, null, document.getElementsByTagName('head')[0]);

Highcharts.theme = {
   colors: ["#000000"],
   // colors: ['7cb5ec','#0066FF', '#00CCFF'],
   chart: {
      backgroundColor: null,
      style: {
         fontFamily: "Dosis, sans-serif"
      }
   },
   title: {
      style: {
         fontSize: '16px',
         fontWeight: 'bold',
         textTransform: 'uppercase'
      }
   },
   tooltip: {
      borderWidth: 0,
      backgroundColor: 'rgba(219,219,216,0.8)',
      shadow: false
   },
   legend: {
      itemStyle: {
         fontWeight: 'bold',
         fontSize: '13px'
      }
   },
   xAxis: {
      gridLineWidth: 1,
      labels: {
         style: {
            fontSize: '12px'
         }
      }
   },
   yAxis: {
      minorTickInterval: 'auto',
      title: {
         style: {
            textTransform: 'uppercase'
         }
      },
      labels: {
         style: {
            fontSize: '12px'
         }
      }
   },
   plotOptions: {
      candlestick: {
         lineColor: '#404048'
      }
   },


   // General
   background2: '#c0c0c0'

};

// Apply the theme
Highcharts.setOptions(Highcharts.theme);