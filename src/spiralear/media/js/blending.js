(function () {
  var SWITCH_TIMEOUT = 4000;
  var SWITCH_FADE = 3000;
  var timeoutId;
  var switchRunning;

  var updateControl = function (newIndex) {
    var spans = $(".ad-control span").removeClass("selected");
    $(spans[newIndex]).addClass("selected");
  };

  var switchTimerAction = function () {
    var adverts = $("#banner a");
    var displayed = $("#banner a:visible");
    var next = (displayed.index() + 1) % adverts.length;
    updateControl(next);
    displayed.fadeOut(SWITCH_FADE);
    switchRunning = false;
    $(adverts[next]).fadeIn(SWITCH_FADE, function () {
      if (!switchRunning && timeoutId !== null) {
        startSwitchTimer();
      }
    });
  };

  var startSwitchTimer = function () {
    switchRunning = true;
    timeoutId = setTimeout(switchTimerAction, SWITCH_TIMEOUT);
  };

  var switchNow = function (upDown, index) {
    var adverts = $("#banner a").stop(true, true);
    var newIndex = index;
    var displayed = $("#banner a:visible"); 
    if (upDown) {
      newIndex = (displayed.index() + upDown + adverts.length) % adverts.length;
    } 
    displayed.hide();
    $(adverts[newIndex]).show();
    updateControl(newIndex);
  }

  var stopSwitchOnMouseover = function () {
    $("#banner").
      live("mouseenter", function () {
        clearTimeout(timeoutId);
        timeoutId = null;
      }).
      live("mouseleave", function () {
        startSwitchTimer();
      });
  };

  var addAdvertControl = function () {
    var arrow = function (clazz, url) {
      return '<img class="' + clazz + '" src="' + url + '"/>';
    }
    $("#banner").append('<div class="ad-control-left"><div class="ad-control-right"><div class="ad-control"></div></div></div>');
    var adControl= $(".ad-control");
    adControl.append(arrow("left", '/media/img/blend_arrow_left.png'));
    $("#banner a").each(function (i) {
      adControl.append('<span>' + (i + 1) + '</span>');
    });
    adControl.append(arrow("right", '/media/img/blend_arrow_right.png'));
    $(".ad-control span:eq(0)").addClass("selected");
    $(".ad-control img").click(function () {
      switchNow($(this).hasClass("left") ? -1 : 1);
    });
    var spans = $(".ad-control span");
    spans.click(function () {
      switchNow(0, spans.index(this));
    });
  };

  startSwitchTimer();
  stopSwitchOnMouseover();

  $(function () {
    addAdvertControl();
  });
})();
