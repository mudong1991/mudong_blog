$(document).ready(function(){
	//去掉a标签点击后的虚线边框
	$("a").bind("focus",function() {
		if(this.blur) {this.blur()};
	});
	//	下雪效果
	//$(document).snowfall('clear');
    //$(document).snowfall({
	//	image: "/static/images/snow.gif",
	//	flakeColor:'#fff',
     //   flakeCount:40,
     //   minSize: 5,
     //   maxSize: 16
    //});

    //顶部导航
	var nav_top=$(window).scrollTop();
	top_action();
	function top_action(){
		if(nav_top>106){
			$(".mynavbar").addClass('navbar-fixed-top');
		}
		else{
			$(".mynavbar").removeClass('navbar-fixed-top');
		}
	};
	$(window).scroll(function(){
		nav_top=$(window).scrollTop();
		top_action();
	});
	//轮播
	$( '#myslider' ).sliderPro({
		width: '96%',
		orientation: 'horizontal',
		loop: true,
		arrows: true,
		buttons: false,
		thumbnailsPosition: 'bottom',
		thumbnailPointer: true,
		thumbnailWidth: 179,
		breakpoints: {
			800: {
				thumbnailsPosition: 'bottom',
				thumbnailWidth: 158,
				thumbnailHeight: 100
			},
			500: {
				thumbnailsPosition: 'bottom',
				thumbnailWidth: 116,
				thumbnailHeight: 80
			}
		}
	});
	//页底置顶按钮
	if($(window).scrollTop() > 106){  //判断页面刷新时候的高度来觉得显示或者隐藏
		$('.turntop').show();
	}
	else{
		$('.turntop').hide().css('bottom','-40px');
	}
	$(window).scroll(function(){
		$('.turntop').show();
		if($(window).scrollTop() > 106){
			$('.turntop').css('bottom','5px');
		}
		else{
			$('.turntop').css('bottom','-40px');
		}
	});
	$('.turntop').on('click',function(){
		$('html,body').animate({'scrollTop':$('#top').offset().top},500); //html body解决所有浏览的都可以用的问题
	});


	//文章页-评论表单弹出用户表单
	$('.comment-content').on('focusin', function(){
		$('.comment-userform').fadeIn(1000);
	});
	$('.comment-userform-remove').on('click', function(){
		$('.comment-userform').fadeOut(1000);
	});
	$('.article-content img').addClass('img-response');

	//点击弹出登录窗口
	$('#user_login').on('click', function(){
		$('.box').show(1000).css('display', 'table');
	});
	$('.login-title i').on('click', function(){
		$('.box').hide(1000);
	})
})
