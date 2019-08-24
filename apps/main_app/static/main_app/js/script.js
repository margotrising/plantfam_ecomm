(function(){

    jQuery.easing['jswing']=jQuery.easing['swing'];jQuery.extend(jQuery.easing,{easeOutBounce:function(x,t,b,c,d){if((t/=d)<(1/2.75)){return c*(7.5625*t*t)+b}else if(t<(2/2.75)){return c*(7.5625*(t-=(1.5/2.75))*t+.75)+b}else if(t<(2.5/2.75)){return c*(7.5625*(t-=(2.25/2.75))*t+.9375)+b}else{return c*(7.5625*(t-=(2.625/2.75))*t+.984375)+b}}});

    $('.gHover').hover(function() {
        $(this).stop().animate({
            top: -50
        }, 900, "easeOutBounce");
    }, function() {
        $(this).stop().animate({
            top: 0
        }, 900, "easeOutBounce");
    });

  
    


})(jQuery); // End of use strict


