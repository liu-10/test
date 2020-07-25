window.onload = function(){
	var reg1 = /^\w{6,20}$/;
					var reg2 =/^[\w!@#$%^&*]{6,20}/;
					var reg3 =/^[\w!@#$%^&*]{6,20}/;
					var reg4 =/^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/i;


					//判断用户名
					$('.re-us').blur(function(){
						var us = $('.re-us').val();
						// alert(us);
						
						if(reg1.test(us)){
							$('.us-error').hide();
							$('.us-error1').hide();
						}
						else{
							$('.us-error1').show();
						}
						if(us == ''){
							$('.us-error').show();
							$('.us-error1').hide();
						}
					})

					$('.re-us').focus(function(){
						$('.us-error').hide();
					})


					//判断密码
					$('.re-pa').blur(function(){
						var pa = $('.re-pa').val();
						// alert(pa);
						
						if(reg2.test(pa)){
							$('.pa-error').hide();
							$('.pa-error1').hide();
						}
						else{
							$('.pa-error1').show();
						}
						if(pa == ''){
							$('.pa-error').show();
							$('.pa-error1').hide();
						}
					})

					$('.re-pa').focus(function(){
						$('.pa-error').hide();
					})

					//确认密码
					$('.check-pa').blur(function(){
						var pa2 = $('.check-pa').val();
						var pa = $('.re-pa').val();
						// alert(us);
						if(pa == pa2){
							//两次密码不一致
							$('.pac-error1').show();
							$('.pac-error2').hide();
							$('.pac-error').hide();
						}
						
						if(reg3.test(pa2)){
							$('.pac-error').hide();
							$('.pac-error1').hide();
							$('.pac-error2').hide();
						}
						else{
							$('.pac-error1').show();
						}
						if(pa2 == ''){
							$('.pac-error').show();
							$('.pac-error1').hide();
						}
					})

					$('.check-pa').focus(function(){
						$('.pac-error').hide();
						$('.pac-error1').hide();
						$('.pac-error2').hide();
					})

					//判断邮箱
					$('.re-em').blur(function(){
						var eam = $('.re-em').val();
						// alert(us);
						
						if(reg4.test(eam)){
							$('.em-error').hide();
							$('.em-error1').hide();
						}
						else{
							$('.em-error1').show();
						}
						if(eam == ''){
							$('.em-error').show();
							$('.em-error1').hide();
						}
					})

					$('.re-em').focus(function(){
						$('.em-error').hide();
						$('.em-error1').hide();
					})


					$('.comit').click(function(){

						var che = $('.comit').prop('checked');
						if(che != true){
							$('.che-error').show();
						}
						else{
							$('.che-error').hide();
						}

				})
}