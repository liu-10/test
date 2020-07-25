window.onload = function(){
	
			var gnum = $('.gd-text').val();
			if(gnum == '' || isNaN(gnum)){
				gnum = 1;
				$('.gd-text').val(gnum);
			}
			
			$('.up').click(function(){
				var gnum = $('.gd-text').val();
				// alert(gnum);
				gnum ++;
				
				$('.gd-text').val(gnum);
				// alert(gnum);
				var total = $('.total-text span').html();
				var unit  =$('.detail-price span').html();
				$('.total-text span').html(parseFloat(gnum * unit).toFixed(2));
			})

			$('.down').click(function(){
				var gnum = $('.gd-text').val();
				// alert(gnum);
				gnum --;

				if(gnum < 1){
					gnum = 1;
					$('.gd-text').val(gnum);
					return;
				}
				$('.gd-text').val(gnum);
				// alert(gnum);
				var total = $('.total-text span').html();
				var unit  =$('.detail-price span').html();
				$('.total-text span').html(parseFloat(gnum * unit).toFixed(2));
			})

			$('.gd-text').blur(function(){
				var gnum = $('.gd-text').val();
				if(isNaN(gnum)){
					alert('输入错误，请重新输入');
					return;
				}
				if(gnum == ''){
					gnum = 1;
					$('.gd-text').val(gnum);
					var unit  =$('.detail-price span').html();
					$('.total-text span').html(parseFloat(gnum * unit).toFixed(2));
					return;
				}
				else{
					var total = $('.total-text span').html();
					var unit  =$('.detail-price span').html();
					$('.total-text span').html(parseFloat(gnum * unit).toFixed(2));
				}	
			})
}