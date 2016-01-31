(function($){
    "use strict"; // Start of use strict
    /* ---------------------------------------------
     Owl carousel
     --------------------------------------------- */
    function init_carousel(){
        $('.owl-carousel').each(function(){
          var config = $(this).data();
          config.navText = ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'];
          var animateOut = $(this).data('animateout');
          var animateIn = $(this).data('animatein');
          if(typeof animateOut != 'undefined' ){
            config.animateOut = animateOut;
          }
          if(typeof animateIn != 'undefined' ){
            config.animateIn = animateIn;
          }

          var owl = $(this);
          owl.owlCarousel(config);
        });
    }
    
    /* ---------------------------------------------
     ScrollCompensate
     --------------------------------------------- */
    function scrollCompensate(){
        var inner = document.createElement('p');
        inner.style.width = "100%";
        inner.style.height = "200px";
        var outer = document.createElement('div');
        outer.style.position = "absolute";
        outer.style.top = "0px";
        outer.style.left = "0px";
        outer.style.visibility = "hidden";
        outer.style.width = "200px";
        outer.style.height = "150px";
        outer.style.overflow = "hidden";
        outer.appendChild(inner);
        document.body.appendChild(outer);
        var w1 = parseInt(inner.offsetWidth);
        outer.style.overflow = 'scroll';
        var w2 = parseInt(inner.offsetWidth);
        if (w1 == w2) w2 = outer.clientWidth;
        document.body.removeChild(outer);
        return (w1 - w2);
    }
    /* ---------------------------------------------
     Init popup
     --------------------------------------------- */
    function init_popup(){
        if($(window).width() + scrollCompensate() >= 768){
            if($('body').hasClass('home')){
                //Open directly via API
                $.magnificPopup.open({
                  items: {
                    src: '<div class="white-popup"><div class="leka-popup"><div class="popup-title"><h3>Newsletter Popup</h3><p class="notice">Sign up to our email newsletter to be the first to hear about great offers & more</p></div><form class="form-subscribe"><input placeholder="SIGN UP YOUR EMAIL..." type="text" /><button class="button">SUBSCRIBE</button></form><div class="checkbox"><label><input type="checkbox" value="">DON’T SHOW THIS POPUP AGAIN</label></div></div></div>',  //can be a HTML string, jQuery object, or CSS selector
                    type: 'inline'
                  }
                });
            }
        }
    }
    
    /* ---------------------------------------------
     Height Full
     --------------------------------------------- */
    function js_height_full(){
        (function($){
            var heightSlide = $(window).outerHeight();
            $(".full-height").css("height",heightSlide);
        })(jQuery);
    }
    /* ---------------------------------------------
     POSITION SIDEBAR FOOTER
     --------------------------------------------- */
    function positionFootersidebar(){
          var height2 = $('.sidebar-menu .footer-sidebar').outerHeight(),
              heightWin = $(window).height(),
              height1 = heightWin - height2 - 85 - 85 -100;
         $('.sidebar-menu .header-sidebar ').css('min-height',height1+'px')
    }
    
    /**==============================
    AUTO WIDTH VERTICAL MENU
    ===============================**/
    function auto_width_vertical(){
        var full_width = parseInt($('.container').innerWidth());
        
        //full_width = $( document ).width();
        var menu_width = parseInt($('.vertical-menu').actual('width'));
        var mega_width = ((full_width - menu_width)-30);
        $('.vertical-menu').find('.mega-menu').css('width',mega_width+'px');
    }

    function Scrollbar_header_sidebar(){
      //  Scrollbar
      if($('.sidebar-menu').length >0 ){
          $(".sidebar-menu").mCustomScrollbar();
      }
    }
    
    /* ---------------------------------------------
     Stick menu
     --------------------------------------------- */
     function stick_header(){
        if($('.header').length >0){
            var h = $(window).scrollTop();
            var width = $(window).width();
            if(width > 767){
                if(h > 0){
                    $('.header').addClass('stick').slideDown();
                }else{
                    $('.header').removeClass('stick');
                }
            }else{
                $('.header').removeClass('stick');
            }
        }
        
     }
    /* ---------------------------------------------
     Scripts initialization
     --------------------------------------------- */
    $(window).load(function() {
        // Vertical menu width
        auto_width_vertical();
        // Init popup
        //init_popup();
        Scrollbar_header_sidebar();
        stick_header();
        //MANSORY LOOKBOOK
        $('.grid-mansory').each(function(){
            var $layoutMode = $(this).attr('data-layoutmode');
            var $gutter = $(this).data('gutter');
            $(this).isotope({
              resizable: false, 
              itemSelector : '.grid',
              layoutMode: $layoutMode,
              transitionDuration: '0.6s',
              packery: {
                 gutter: $gutter
              },
            }).isotope( 'layout' );
        });
          
        //COLUMNS PORTFOLIO
        var $portfolio_columns = $('.portfolio-columns').isotope({
            resizable: false, 
            itemSelector : '.grid'
        });
        // filter items on button click
        $(document).on('click','.portfolio-nav a',function(){
            $(this).closest('.portfolio-nav').find('a').each(function(){
                $(this).removeClass('active');
            })
            $(this).addClass('active');
            var filterValue = $(this).data('filter');
            $portfolio_columns.isotope({ filter: filterValue });  
            return false;
        })
        
        //MASONRY PORTFOLIO
        var $portfolio_masonry = $('.portfolio-masonry').isotope({
              resizable: true, 
              itemSelector : '.grid',
              layoutMode: 'packery',
              transitionDuration: '0.6s',
              packery: {
                 gutter: 30
              },
        });
        // filter items on button click
        $(document).on('click','.portfolio-nav a',function(){
            $(this).closest('.portfolio-nav').find('a').each(function(){
                $(this).removeClass('active');
            })
            $(this).addClass('active');
            var filterValue = $(this).data('filter');
            $portfolio_masonry.isotope({ filter: filterValue });  
            return false;
        })
        
    });
    /* ---------------------------------------------
     Scripts resize
     --------------------------------------------- */
    $(window).resize(function(){
        // Vertical menu width
        auto_width_vertical();
        Scrollbar_header_sidebar();
        stick_header()
    });
    /* ---------------------------------------------
     Scripts scroll
     --------------------------------------------- */
    $(window).scroll(function(){
        // Vertical menu width
        auto_width_vertical();
        stick_header()
        // Show hide scrolltop button
        if( $(window).scrollTop() == 0 ) {
            $('.scroll_top').stop(false,true).fadeOut(600);
        }else{
            $('.scroll_top').stop(false,true).fadeIn(600);
        }
        Scrollbar_header_sidebar();
    });
    /* ---------------------------------------------
     Scripts ready
     --------------------------------------------- */
    $(document).ready(function() {
        // OWL CAROUSEL
        init_carousel();
        // Vertical menu width
        auto_width_vertical();
        Scrollbar_header_sidebar();
        stick_header()
        // bg-parallax
        if($('.bg-parallax').length >0){
            $('.bg-parallax').each(function(){
                $(this).parallax("50%",0.5);
            })  
        }
        // Category product
        $(document).on('click','.widget_product_categories a, .widget_categories a',function(){
        var paerent = $(this).closest('li');
        var t = $(this);
        if(paerent.children('ul').length > 0){
            $(this).closest('li').children('ul').slideToggle();
            return false;
        }
        })
        
        // CATEGORY FILTER 
        $('.slider-range-price').each(function(){
            var min             = $(this).data('min');
            var max             = $(this).data('max');
            var unit            = $(this).data('unit');
            var value_min       = $(this).data('value-min');
            var value_max       = $(this).data('value-max');
            var label_reasult   = $(this).data('label-reasult');
            var t               = $(this);
            $( this ).slider({
              range: true,
              min: min,
              max: max,
              values: [ value_min, value_max ],
              slide: function( event, ui ) {
                var result = label_reasult +" "+ unit + ui.values[ 0 ] +' - '+ unit +ui.values[ 1 ];
                t.closest('.price_slider_wrapper').find('.amount-range-price').html(result);
              }
            });
        })
        
        // Select single product
        $(document).on('click','.single-product-thumbnails span',function(){
            $(this).closest('.single-product-thumbnails').find('span').each(function(){
                $(this).removeClass('selected');
            });
            $(this).addClass('selected');
            var image_full = $(this).data('image_full');
            $(this).closest('.single-images').find('.main-image').attr('src',image_full);
            $(this).closest('.single-images').find('.popup-image').attr('href',image_full);
            
            return false;
        })
        // popup image
        if($('.popup-image').length >0 ){
            $('.popup-image').magnificPopup({type:'image'});
        }
        //SELECT CHOSEN
        $("select").chosen();
        
        // ACCORDION
        $( ".leka-accordion" ).accordion();
        // Popup add to cart
        $(document).on('click','.button-add-to-cart',function(){
            var result ='';
            result += '<div class="popup-add-to-cart">';
            result +='       <div class="message">';
            result +='          <i class="fa fa-check-circle-o"></i>';
            result +='          <p>YOU HAVE ADDED TO SHOPPING CART</p>';
            result +='      </div>';
            result +='      <div class="popup-product">';
            result +='          <a href="#"><img src="images/products/popup-product.png" alt="" /></a>';
            result +='          <h3 class="product-name"><a href="#">LONG Tube Dress</a></h3>';
            result +='          <a href="cart.html" class="button button-view-cart">VIEW SHOPPING CART</a>';
            result +='          <a href="" class="button button-continue-shop">CONTINUE SHOPPING</a>';
            result +='      </div>';
            result +='</div>';
            $.magnificPopup.open({
                  items: {
                    src: result, // can be a HTML string, jQuery object, or CSS selector
                    type: 'inline'
                  }
            });
            return false;
        });
        
        // Open form search
        $(document).on('click','.icon-search .icon',function(){
            $('#form-search').toggle();
            $('#form-search').find('input[type="text"]').focus();
            $('.main-header .logo,.main-header .main-menu, .main-header .mini-cart').css('opacity','0');
        })
        
        /* Close form search */
        $(document).on('click','*',function(e){
            var container = $("#form-search");
            var icon = $('.icon-search .icon');
            if (!container.is(e.target) && container.has(e.target).length === 0 && !icon.is(e.target) && icon.has(e.target).length === 0 ){
                container.hide();
                $('.main-header .logo,.main-header .main-menu, .main-header .mini-cart').css('opacity','1');
            }
        })
        
        //MENU RESPONSIVE
        var kt_is_mobile = (Modernizr.touch) ? true : false;
        if(kt_is_mobile === true){
        	$(document).on('click', '.main-menu .menu-item-has-children > a,.vertical-menu .menu-item-has-children > a', function(e){
        		var licurrent = $(this).closest('li');
        		var liItem = $('.main-menu .menu-item-has-children,.vertical-menu .menu-item-has-children');
        		if ( !licurrent.hasClass('show-submenu') ) {
  		            liItem.removeClass('show-submenu');
      		        licurrent.parents().each(function (){
      		            if($(this).hasClass('menu-item-has-children')){
      		             $(this).addClass('show-submenu');   
      		            }
                        if($(this).hasClass('main-menu') || $(this).hasClass('vertical-menu')){
                            return false;
                        }
      		        })
      		        
        			licurrent.addClass('show-submenu');
        
                    // Close all child submenu if parent submenu is closed
                    if ( !licurrent.hasClass('show-submenu') ) {
                        licurrent.find('li').removeClass('show-submenu');
                    }
                    return false;
                    e.preventDefault();
        		}else{
        			var href = $this.attr('href');
                    if ( $.trim( href ) == '' || $.trim( href ) == '#' ) {
                        licurrent.toggleClass('show-submenu');
                    }
                    else{
                        window.location = href;
                    } 
        		}
        		// Close all child submenu if parent submenu is closed
                if ( !licurrent.hasClass('show-submenu') ) {
                    //licurrent.find('li').removeClass('show-submenu');
                }
                e.stopPropagation();
       	});
        
    	$(document).on('click', function(e){
            var target = $( e.target );
            
            if ( !target.closest('.show-submenu').length || !target.closest('.navigation').length ) {
                $('.show-submenu').removeClass('show-submenu');
            }
        }); 
        // On Desktop
        }else{
            $(document).on('mousemove','.main-menu .menu-item-has-children,.vertical-menu .menu-item-has-children',function(){
                $(this).addClass('show-submenu');
            })
            $(document).on('mouseout','.main-menu .menu-item-has-children,.vertical-menu .menu-item-has-children',function(){
                $(this).removeClass('show-submenu');
            })
        }
        // Open main menu on mobile
        $(document).on('click','.mobile-navigation',function(){
            $('#main-menu').toggle();
            return false;
        })
        //Image product zoom
         $('.product-feture').each(function(){
            // Instantiate EasyZoom instances
            var $imageBig = $(this).find('.product-image img');
            // Setup thumbnails example
            $(this).find('.product-thumbnails').on('click', 'a', function(e) {
                $(this).parent().find('a').removeClass('selected');
                $(this).addClass('selected');

                var $this = $(this);
                e.preventDefault();

                var imgLink = $this.attr('href');
                $imageBig.attr('src',imgLink);
                

            });

          });

          //CLIENT SAY
            $('.leka-testimonial-2').each(function(){
              var owl = $(this).find('.client-carousel');
              owl.owlCarousel(
                {
                    margin:20,
                    autoplay:true,
                    dots:false,
                    loop:true,
                    items:3,
                    nav:false,
                    smartSpeed:1000,
                    navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
                }
              );
              owl.trigger('next.owl.carousel');
              owl.on('changed.owl.carousel', function(event) {
                  owl.find('.owl-item.active').removeClass('item-center');
                  var caption=owl.find('.owl-item.active').first().next().find('.client-quote').html();
                  owl.closest('.leka-testimonial-2').find('.leka-client-quote').html(caption).addClass('zoomIn animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                           $(this).removeClass('zoomIn animated');
                  });;
                  setTimeout(function(){
                      owl.find('.owl-item.active').first().next().addClass('item-center');
                  }, 100);
              })

            });
            
          //SLIDE FULL SCREEN
           var slideSection = $(".slide-fullscreen .item-slide");
            slideSection.each(function(){
                if ($(this).attr("data-background")){
                    $(this).css("background-image", "url(" + $(this).data("background") + ")");
                }
            });

          //Full height
          js_height_full();
          $(window).resize(function(){
            js_height_full();
          });

          //Background Cat
          $('.leka-list-cat .item-cat').each(function(){
              var imgBg = $(this).attr('data-background');
              $(this).css('background-image','url('+imgBg+')');
          })

          //Menu siderbar
          $('.sidebar-menu .main-menu li.dropdown > a').on('click',function(){
            $(this).toggleClass('active');
            $(this).parent().children('.dropdown-menu').slideToggle();

          })

          //SIDEBAR TEMP
          positionFootersidebar();
          $(document).resize(function(){
              positionFootersidebar();
          });

          $('.mobile-sidebar').on('click',function(){
              $('body').toggleClass('sidebar-active');
          });
          
          
          // PORTFOLIO IMMAGES POPUP
          $('.portfolio-images').magnificPopup({
              delegate: 'a',
              type: 'image',
              tLoading: 'Loading image #%curr%...',
              mainClass: 'mfp-img-mobile',
              gallery: {
                enabled: true,
                navigateByImgClick: true,
                preload: [0,1] // Will preload 0 - before current, and 1 after the current image
              },
              image: {
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
                titleSrc: function(item) {
                  //return item.el.attr('title') + '<small>by Marsel Van Oosten</small>';
                }
              }
          });
          
          // VETICAL MENU
          $(document).on('click','.header .vertical-menu .vertical-navigation',function(){
            $('.header .vertical-menu').find('.vertical-content').toggle();
          })
          
          // Scroll top 
          $(document).on('click','.scroll_top',function(){
            $('body,html').animate({scrollTop:0},400);
            return false;
          });

          // Open vertical menu
          $(document).on('click','.vertical-navigation',function(){
            $('#vertical-menu').fadeToggle();
          })
    });
})(jQuery); // End of use strict