toggle = function(source) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    	for (var i = 0; i < checkboxes.length; i++) {
    	if (checkboxes[i] != source)
    	checkboxes[i].checked = source.checked;
    	}
}

$(document).ready(function(){
	$('#delete').click(function(event){
		var id = []
		var csrf = $('input[name=csrfmiddlewaretoken]').val();
		$('.select:checked').each(function(i){
			id[i] = $(this).val()
		})
		if(id.length != 0){
			// console.log(id)
			// console.log(csrf)
			$.ajax({
				url:'.',
				method:"POST",
				data:{
					id,
					csrfmiddlewaretoken:csrf 
				},
				success:function(response){
					for (var i = 0; i < id.length; i++) {
						$('tr#'+id[i]+'').hide()
					}
				}
			})
		}
	})
})

$(document).ready(function(){
	$('#enrollDelete').click(function(event){
		var id = []
		var csrf = $('input[name=csrfmiddlewaretoken]').val();
		var classcourse = $('#classcourse').val()
		$('.select:checked').each(function(i){
			id[i] = $(this).val()
		})
		if(id.length != 0){
			// console.log(id)
			// console.log(csrf)
			$.ajax({
				url:'/class_detail/'+classcourse,
				method:"POST",
				data:{
					id,
					classcourse,
					csrfmiddlewaretoken:csrf 
				},
				success:function(response){
					for (var i = 0; i < id.length; i++) {
						$('tr#'+id[i]+'').hide()
					}
				}
			})
		}
	})
})

$(document).ready(function(){
	$('#enroll_student').click(function(event){
		var id = []
		var csrf = $('input[name=csrfmiddlewaretoken]').val();
		var classname = $('#classname').val()
		$('.select:checked').each(function(i){
			id[i] = $(this).val()
		})
		if(id.length != 0){
			// console.log(id)
			// console.log(csrf)
			$.ajax({
				url:'.',
				method:"POST",
				data:{
					id,
					csrfmiddlewaretoken:csrf,
					classname
				},
				success:function(response) {
					 window.location.href = "/class"
				}
			})
		}
	})
})

$(document).ready(function(){
	$('#deleteAttendance').click(function(event){
		var id = []
		var csrf = $('input[name=csrfmiddlewaretoken]').val();
		$('.select:checked').each(function(i){
			id[i] = $(this).val()
		})
		if(id.length != 0){
			// console.log(id)
			// console.log(csrf)
			$.ajax({
				url:'.',
				method:"POST",
				data:{
					id,
					csrfmiddlewaretoken:csrf 
				},
				success:function(response){
					window.location.href = "/attendance"
				}
			})
		}
	})
})


$(document).ready(function(){
	$('#face_encode').click(function(){
		var message = "face_encode"
		$.ajax({
			url:'.',
			method:"GET",
			data:{
				message
			}
		})
	})
})		