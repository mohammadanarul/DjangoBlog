$(document).ready(function(event){
	$('.reply-btn').click(function(){
		$(this).parent().parent().next('.replied-comments').fadeToggle()
	});
});