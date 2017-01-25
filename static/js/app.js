$.fn.editable.defaults.mode = 'inline';
$.fn.editable.defaults.ajaxOptions = {type: 'POST'};

$(document).ready(function(){
	$('.set-guide-number').editable()
	$('.select-status').editable({
		source: [
			{value: "creado", text:"Creado"},
			{value: "enviado", text:"Enviado"},
			{value: "recibido", text:"Recibido"},
		]
	})
	$('.add-to-cart').on('submit', function(ev){
		ev.preventDefault();

		var $form = $(this);
		var $button = $form.find("[type='submit']");

			$.ajax({
				url: $form.attr('action'),
				method: $form.attr('method'),
				data: $form.serialize(),
				beforeSend: function(){
					$button.val('Cargando...');
				},
				success: function(data){
					//console.log(data)
					$('.circle-shopping-cart').html(data.products_count).addClass('highlight');
					$button.css('background-color', '#00c853').val('Agregado')
					setTimeout(function(){
						restartButton($button)
					}, 2000)
				},
				error: function(err){
					console.log(err)
					$button.css('background-color', '#d50000').val('Hubo un error.')
					setTimeout(function(){
						restartButton($button)
					}, 2000)
				},
			});

		return false
	});

	function restartButton($button){
		$button.val("Agregar al carrito").attr("style", "");
		$('.circle-shopping-cart').removeClass('highlight');
	}

});