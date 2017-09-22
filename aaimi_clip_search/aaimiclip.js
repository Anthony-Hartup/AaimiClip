$('button#show').click(function (e) {
    $('button#show').attr('style', 'background-color:red'); 
    $('div.results').load('aaimiclipout.php');
});

$('#searchform').submit(function(event) {
    event.preventDefault();
    var $form = $( this ),
    fold = $form.find("select[name='folder']").val(),
    //alert(fold);
    searchterms = $form.find("input[name='keys']").val(),	    	
    url = $form.attr( "action" );
    $('div.results').load('aaimi_clip_read.php', {'folder':fold, 'keys':searchterms});
});

$('button#searchcol').click (function (e) {
	$('.addclip').attr('style', 'display:none');
	$('.searcharea').attr('style', 'display:block');
});


