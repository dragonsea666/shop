
$(function(){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/carts/show_cart_count/',
        type:'POST',
        dataType:'json',
		headers:{'X-CSRFToken': csrf},
		success:function(data){
		    if (data.code == 200){
		        $('#show_count').text(data.goods_count)
		    }
		},
		error:function(data){
		    alert('添加失败')
		}
    })
})