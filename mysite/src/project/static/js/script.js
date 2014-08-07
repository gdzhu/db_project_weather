/**
 * 
 */
var padding = 70;

$( document ).ready(function() {
	navtoTag();
	changeIcon();
	paddingBody();
	focusActive();
	changeAffixPos();
});

// workaround for body padding
function paddingBody() {
	var styles = {
            "padding-top":padding
		};
    $('body').css(styles);
}

// navigation bar
function navtoTag() {
	// Attach the click event
	$('a.shift').click( function(e) {
	    e.preventDefault();
		var tar = $(this).attr("href"); //Get the target
		if(history.pushState) {
			var pos = $(tar).offset().top - 60;
			$('html').animate({ 'scrollTop': pos }, 500);
			history.pushState(null, null, tar);
		} else {
			location.hash = tar;
		}
	});
}

// expand/collapse button
function changeIcon() {
	$('button').click(function(event) {
		var id = $(this).attr('id').split('_')[0];
		if ($('#' + id).hasClass('in')) {
			$(this)[0].innerHTML = 'Expand&nbsp;&nbsp;<span class="glyphicon glyphicon-collapse-down"></span>';
		} else {
			$(this)[0].innerHTML = 'Collapse&nbsp;&nbsp;<span class="glyphicon glyphicon-collapse-up"></span>';
		}
	});
}

//
//$('#result').on('affixed.bs.affix', function(){
//    $(this).removeAttr('style');
//});

// TODO:fix for scroll bar of the affix navigation 
//function focusActive(){};
//function changeAffixPos(){};
