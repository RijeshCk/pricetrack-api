	
	var app = angular.module('AddtotrackApp',['ngCookies','infinite-scroll']);
	app.controller('Addtotrackcontroller',function($scope,$http,$timeout,$cookies,$cookieStore,$window)
		{
			$scope.AddtoTrack=function(){
				url1 = $scope.url;
				myregex = /[a-zA-Z]/;
				$http.get('http://127.0.0.1:8000/?url='+url1).then(
					function sucessCallback()
					{
					$scope.url='';
					$scope.message= "Product has been added to our Tracking system";
					$scope.clickthis=true;
					$scope.checkErrors=true
					$scope.btnClass ='warning-true'
					$timeout(function checkErrors(){
						$scope.checkErrors=false
						},3600);
				}, 
					function errorCallback()
					{
						console.log(url1);
						if (!url1){
						$scope.message="Please provide url"
					}
					else{
						$scope.message='Sorry we could\'t process your request. Please check your url'}     
						$scope.checkErrors=true
						$scope.btnClass ='error-true'
						$timeout(function checkErrors(){
						$scope.checkErrors=false
						},3600);
						$scope.url = ''
			 return false
			}
			);}
			$scope.Email = "username@exampledomain.com" 
			password1 = $scope.password1;
				password2 = $scope.password2;
				console.log(password1,password2);

			$scope.signup = function(){
				var csrf ='{{csrf_token}}';
				password1 = $scope.password1;
				password2 = $scope.password2;
				console.log(password1,password2);
				// if pass
			}
			
			$scope.login=function(){
				var csrf='{{ csrf_token }}';
				$http({method:'POST',url:'http://127.0.0.1:8000/login',data:{'username':$scope.username,'password':$scope.password,'type':$scope.aana},headers: {'X-CSRFToken' : csrf }}).then(function successCallback(response,status){
					console.log("login successfully");
					$cookies["username"] = $scope.username
					console.log($scope.loggedin_user);
					$window.location.reload();
					},
					function errorCallback(response,status){

						$scope.login_error_message='Invalid Credentials';
					}
					)
			}

			$scope.loggedin_user = $cookies["username"]
			if ($scope.loggedin_user){
				$scope.check_loggedin=$scope.loggedin_user;
				$scope.hehe='glyphicon glyphicon-user';
			}
			else{
			$scope.check_loggedin='Login/signup';
			$scope.hehe='glyphicon glyphicon-user'
			$scope.classlogout='hide-logout';
		}


			$scope.logout=function(){
				var csrf='{{ csrf_token }}';
				console.log(csrf);
				$http({method:'DELETE',url:'http://127.0.0.1:8000/login', headers: {'X-CSRFToken' : csrf }}).then(
					function successCallback(response,status)
					{
						console.log("logout sucessfully");
						$cookies["username"]='';
						$cookies.remove('username');
						$window.location.reload();
				},function errorCallback(){console.log('errrrr');
				$window.location.reload();
				$cookies['username']='';});
			}
			console.log($cookies["username"]);
			$scope.loading = true;
				console.log("listing section");
				$http.get("http://127.0.0.1:8000/getall")
				.success(function(response,status)
						{   $('#image-div').hide();
								pagination_data = response.pagination
								$scope.names = response.product_list;
								
						}
				).error($timeout(function(data, status, headers, config, statusText){
					if(status == 429)
						{
							$scope.error_message= "You have exceed daily Limit";
						}
						else if (status == 400)
						{
							$scope.error_message = "No products in tracklist"
						}
					$('#image-div').hide();
				 },3));
			$scope.check_loadmore = 'loadmore'
			$scope.loadMore = function(){
				$http.get(pagination_data.next_url)
				.success(function(response,status)
						{   $('#image-div').hide();
								console.log("sucess call");
								pagination_data = response.pagination
								s = response.product_list;
								
								for (var i=0 ;i<=s.length;i++){
								 	if ($scope.names.indexOf(s[i])==-1){
								 									
								 		$scope.names.push(s[i]);
								 	}
								 }
								
								return $scope.names
								
						}
				).error(function(data, status, headers, config, statusText){
					$scope.check_loadmore = 'no_loadmore'
					if(status == 429)
						{
							$scope.error_message= "You have exceed daily Limit";
						}
						else if (status == 400)
						{
							$scope.error_message = "No products in tracklist"
						}
						else
						{
							console.log(statusText+'sssssss');
						}
					$('#image-div').hide();
				 });
			}

			}); 