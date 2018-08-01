
/***** script.js: custom jQuery functions *****/

/****OUTLINE:
=================================

0.	Page-loader
1.  Isotope.js (Portfolio grid)
2. 	Drop-down nav
3.  Responsive nav
4.  Centering .overlayinfo (portfolio)
--> 5.  Fitvids --> discarded from HTML/CSS
--> 6.  responsive jPlayer --> discarded from HTML/CSS
--> 7.  background Videos (bGvids) --> discarded from HTML/CSS
--> 8.  smoothShow for elements that become visible --> yet to be applied to HTML/CSS
9. Flexslider (slideshow in portfolio)

=================================****/

jQuery(window).load(function($) {

	/*** 0. Hides page-loader after page is done loading
	-----------------------------------------------------***/
	jQuery("#page-loader .page-loader-inner").delay(1000).fadeOut(500, function(){
		jQuery("#page-loader").fadeOut(500);
	});


	/*** 1. Isotope (Portfolio grid)
	-----------------------------------------------------***/
	if( jQuery().isotope ) {

		/** 1.1 Call Isotope **/
		jQuery('.masonry').each(function(){
			var $container = jQuery(this);

			$container.imagesLoaded( function(){
				$container.isotope({
					itemSelector : '.masonry-item',
					transformsEnabled: true // !important; for videos
				});
			});
		});


		/** 1.2 Filter portfolio grid according to selection **/
		jQuery('.filter li a').click(function(){

			var parentul = jQuery(this).parents('ul.filter').data('related-grid');
			jQuery(this).parents('ul.filter').find('li a').removeClass('active');
			jQuery(this).addClass('active');

			var selector = jQuery(this).attr('data-option-value');
			jQuery('#'+parentul).isotope({
				filter: selector
				}, function(){
			});

			return(false);
		});


		/** 1.3 Reorganizes Isotope **/
		function reorganizeIsotope() {
			jQuery('.masonry').each(function(){
				$container = jQuery(this);
				var maxitemwidth = $container.data('maxitemwidth');
				if (!maxitemwidth) {
					maxitemwidth = 370;
				}
				var containerwidth = $container.width();
				var containerwidth = (containerwidth / 110) * 100;
				var itemrightmargin = parseInt($container.children('div').css('marginRight'));
				var rows = Math.ceil(containerwidth/maxitemwidth);
				var marginperrow = (rows-1)*itemrightmargin;
				var newitemmargin = marginperrow / rows;
				var itemwidth = Math.floor((containerwidth/rows)-newitemmargin+1);
				$container.css({
					'width': '110%'
				});
				$container.children('div').css({
					'width': itemwidth+'px'
				});
				if ($container.children('div').hasClass('isotope-item')) {
					$container.isotope( 'reLayout' );
				}
			});
		}
		reorganizeIsotope();

		jQuery(window).resize(function() {
			reorganizeIsotope();
		});


	}


	/*** 2. Drop-down nav
	-----------------------------------------------------***/
	var timer = [];
   	var timerout= [];
	jQuery("nav#main-nav li").each(function(index) {
        if (jQuery(this).find("ul").length > 0) {
            var element = jQuery(this);

            /** 2.1 Shows Subnav on hover  **/
            jQuery(this).mouseenter(function() {
				if(timer[index]) {
                	clearTimeout(timer[index]);
                	timer[index] = null;
                }
                timer[index] = setTimeout(function() {
                	jQuery(element).children('ul').fadeIn(200);
                }, 150)
            });

            /** 2.2 Hides submenus on exit **/
            jQuery(this).mouseleave(function() {
				if(timer[index]) {
                	clearTimeout(timer[index]
                	);
                	timer[index] = null;
              }
              timer[index] = setTimeout(function() {
                	jQuery(element).children('ul').fadeOut(200);
              }, 150)
            });
        }
    });

	jQuery('nav#main-nav').on("click", "li", function() {
		if (jQuery(window).width() < 1025) {
			if (jQuery(this).find("ul").length > 0) {
				if (jQuery(this).find("ul").css('display') !== 'block') {
					jQuery(this).children("ul").fadeIn(200);
					return false;
				}
			}
		}
	});


	/*** 3. Responsive nav
	-----------------------------------------------------***/
	jQuery('<a class="open-responsive-nav" href=""><span></span></a>').appendTo(".header-inner .menu");
	jQuery("body #page-content").prepend('<div id="menu-responsive"><div id="menu-responsive-inner"><a href="" class="close-responsive-nav"><span></span></a><nav id="responsive-nav"><ul></ul></nav></div></div>');
	jQuery("nav#responsive-nav > ul").html(jQuery("nav#main-nav > ul").html());

	jQuery('header').on("click", ".open-responsive-nav", function() {
		if (jQuery('#menu-responsive').css('right') == 0 || jQuery('#menu-responsive').css('right') == '0px') {
			hideResponsiveNav();
		} else {
			jQuery('#menu-responsive').animate({
				'right': '0'
			}, 800, 'easeInOutQuart');
			jQuery('html, body').animate({
				scrollTop: 0 // @1 remove this when I make the nav options pop-up depending on user screen position
			}, 1000, 'easeInOutQuart');
		}
		return false;
	});

	jQuery('#page-content').on("click", "#menu-responsive", function() {
		hideResponsiveNav();
	});

	function hideResponsiveNav(){
		var right = jQuery('#menu-responsive').width()+10;
		jQuery('#menu-responsive').animate({
			'right': '-'+right+'px'
		}, 800, 'easeInOutQuart');
	}



	/*** 4. Centering .overlayinfo (portfolio)
	-----------------------------------------------------***/
	jQuery('.overlayinfo').each(function(){
		var infoHeight = parseInt(jQuery(this).height() / 2);
		jQuery(this).css({
			'marginTop': '-'+infoHeight+'px'
		});
	});



	/*** 5. fitVids.js call
	-----------------------------------------------------***/
	if(jQuery().fitVids) {
		jQuery("body").fitVids();
	}





	/*** 6. responsive jPlayer.js
	-----------------------------------------------------***/
	if(jQuery().jPlayer && jQuery('.jp-interface').length){
		jQuery('.jp-interface').each(function(){
			var playerwidth = jQuery(this).width();
			var newwidth = playerwidth - 175;
			jQuery(this).find('.jp-progress-container').css({
				width: newwidth+'px'
			});
		});
	}



	/*** 7. backgroundVideo.js
	-----------------------------------------------------***/
	if(jQuery().bgVideo) {
		jQuery('.videobg-section').bgVideo();
	}

	smoothShow();
	flexInit('body');

});


jQuery( window ).scroll(function() {

	smoothShow();

});



/*** 8. smoothShow function (for when certain elements are visible)
-----------------------------------------------------***/
function smoothShow() {


	/** 8.1 for .sr-animation classes **/
	jQuery('.sr-animation').each(function() {
		if (jQuery(window).width() > 700) {
			var visible = jQuery(this).visible(true);
			var delay = jQuery(this).attr("data-delay");
			if (!delay) {
				delay = 0;
			}
			if (jQuery(this).hasClass( "animated" )) {
				//
			}
			else if (visible) {
				jQuery(this).delay(delay).queue(function(){
					jQuery(this).addClass('animated')
				});
			}
		} else {
			jQuery(this).addClass('animated');
		}
	});


	/** 8.2 for animating skill bars **/
	/** (add back to index + style.css + mqueries.css) **/
	jQuery('.skill').each(function() {
		var visible = jQuery(this).visible(true);
		var percent = jQuery(this).find('.skill-bar .skill-active ').attr('data-perc');
		if (jQuery(this).hasClass( "anim" )) {
			//
		}
		else if (visible) {
			var randomval = Math.floor(Math.random() * (300 - 50 + 1)) + 50;
			jQuery(this).addClass("anim");
			jQuery(this).find('.skill-bar .skill-active ').animate({
				'width': percent+'%',
			}, 2000, 'easeInOutQuart', function(){
				jQuery(this).find('.tooltip').delay(randomval).animate({
					'top':'-28px','opacity':1
				}, 500);
			}).css('overflow', 'visible');
		}
	});

}



/*** 9. Flexslider for portfolio slideshows
-----------------------------------------------------***/

/** 9.1 Initiative function because it has to be reinitatilized after portfolio item has loaded **/
function flexInit(el) {
	if(jQuery().flexslider) {
		jQuery(el+" .flexslider").flexslider({
			animation: "slide",
			animationSpeed: 300,
			slideshow: false,
			directionNav: true,
			controlNav: true,
			smoothHeight: true,
			touch: true,
			video: true,
			randomize: false
		});
	}

}


/*
   	     _
     .__(.)< ("Quack. Don't mind me, I'm just a duck swimming on the source code")
      \___)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*/
