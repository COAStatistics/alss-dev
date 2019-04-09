/* pace settings */
Pace.options = {
  ajax: false,
}

/* jQuery loading settings */
$.loading.default.tip = '請稍後';
$.loading.default.imgPath = '../static/vendor/ajax-loading/img/ajax-loading.gif';


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function FixAffixWidth() {
    if ($(window).width() > 768) {
        /* Fix affix width in Firefox */
        var affixMaxWidth = $('#wrapper > .row > .col-lg-2').outerWidth();
        $('#wrapper .affix').css('max-width', affixMaxWidth - 30).css('width', '100%');

    }else{
        $('#wrapper .affix').css('max-width', 'none');
    }
}

$(document).ready(function() {

    $(window).resize(function(){
        FixAffixWidth();
    });

    /* Loading Animation */
    Pace.on('done',function(){
        $('#wrapper').fadeIn(300);
        FixAffixWidth();
    });

    /* jQuery Spinner */
    var Loading = $.loading();

    /* autocomplete */
    $("#farmerId").typeahead({
        source: FarmerIds,
        autoSelect: true,
        fitToElement: true,
    })

    /* panel control */
    $('.js-tabs-control').on('click', function() {
        $(this).siblings().removeClass('active');
        $(this).toggleClass('active');

        var target = $(this).data('target');
        var $partial = $('.js-panel-contents [data-partial="survey"]');
        $partial.find('.panel').hide();
        $('.js-panel-contents [data-partial]').hide();
        $partial.show();
        $(target).show();
    })
    $('.js-partial-control').click(function(){
        var target = $(this).data('target');
        if(target == 'datatable'){
            Helper.DataTable.ReviewLogRetrieve.Setup();
        }
        $('[data-partial]').hide();
        $('[data-partial="{0}"]'.format(target)).show();
    });

    function showLoading(deferred){
        Loading.open();
        setTimeout(function(){
            deferred.resolve();
        }, 500);
        return deferred.promise();
    }


    /* get farmer data*/
    $('.js-get-survey').click(function () {

        var $btn = $(this);

        var farmerId = $('#farmerId').val().trim();
        var url = $(this).data('url');
        var readonly = $(this).data('readonly');

        if($btn.data('ajax-sending')){
            return;
        }

        if (farmerId) {
            $.when(
                $btn.data('ajax-sending', true),
                $.Deferred(showLoading)
            ).done(function(){
                // it resolves itself after 1 seconds
                var timer = $.Deferred();
                setTimeout(timer.resolve, 1000);

                // turn on or turn off validation
                Helper.LogHandler.ValidationActive = true; //readonly != true;

                var ajax = GetFarmerData(url, farmerId, readonly).fail(function(){
                    Helper.Dialog.ShowAlert('很抱歉，當筆資料查詢錯誤，請稍後再試。');
                });

                $.when(timer, ajax).done(function(timer, ajax){
                    if(ajax[0].length > 0){
                        $('[data-partial]').hide();
                        $('[data-partial="survey"]').show();
                        $('[data-partial="survey"] .panel').show();
                        $('.js-tabs-control').removeClass('active');
                        if(readonly) $('.js-set-survey').hide();
                        else $('.js-set-survey').show();
                    }
                    $btn.data('ajax-sending', false);
                })
            }).done(function(){
                Helper.LogHandler.CollectError.Init();
                Loading.close();
                $(window).scrollTop(0);
            })
        } else {
            Helper.Dialog.ShowAlert('請輸入農戶編號！');
        }
    });

    /* set farmer data*/
    $('.js-set-survey').click(function () {
        $btn = $(this);
        if($btn.data('ajax-sending')){
            return;
        }
        if(CloneData){
            if(!CloneData[MainSurveyId].readonly){
                var url = $(this).data('url');
                $.when(
                    $btn.data('ajax-sending', true),
                    $.Deferred(showLoading)
                ).done(function(){

                    // it resolves itself after 1 seconds
                    var timer = $.Deferred();
                    setTimeout(timer.resolve, 1000);

                    var jobs = [timer]
                    Object.keys(CloneData).forEach(function(pk, i){
                        var ajax = SetFarmerData(url, JSON.stringify(CloneData[pk])).fail(function(){
                            Helper.Dialog.ShowInfo('很抱歉，更新時發生錯誤，請稍後重試或與我們聯繫！');
                        });
                        jobs.push(ajax);
                    })

                    $.when.apply(
                        undefined,
                        jobs
                    ).done(function(){
                        // this won't be called until *all* the AJAX and the timer have finished
                        Reset();
                        Object.keys(CloneData).forEach(function(key, i){
                            Set(CloneData[key], CloneData[key].id);
                        });
                        // create or update review log
                        data = {
                            initial_errors: Helper.LogHandler.CollectError.InitialErrors,
                            current_errors: Helper.LogHandler.CollectError.GetCurrent(),
                            object_id: CloneData[MainSurveyId].id,
                            app_label: 'surveys19',
                            model: 'survey',
                        }
                        var ajax = SetLogData(JSON.stringify(data));
                        Helper.DataTable.ReviewLogRetrieve.Reload();
                        Helper.Dialog.ShowInfo('成功更新調查表！');

                        $btn.data('ajax-sending', false);
                    })
                }).done(function(){
                    Loading.close();
                })
            }
        }
    });
})

var GetFarmerData = function (url, fid, readonly) {
    return $.ajax({
        url: url,
        async: false,
        type: 'GET',
        data: {
            fid: fid,
            readonly: readonly,
        },
        success: function (data) {
            if (data.length > 0) {
                var firstPageObj = $.grep(data, function (survey) {
                    return survey.page == 1
                });
                if (firstPageObj.length > 0) {
                    Reset();
                    CloneData = {};
                    /* set surveys */
                    data.forEach(function(survey, i){
                        CloneData[survey.id] = survey;
                        Set(survey, survey.id);
                    })
                } else {
                    Helper.Dialog.ShowInfo('查無農戶資料！');
                }
            }
            else {
                Helper.Dialog.ShowInfo('查無農戶資料！');
            }
        },
    });
}

var SetFarmerData = function (url, data) {
    return $.ajax({
        url: url,
        async: false,
        type: 'PATCH',
        data: {
            data: data
        },
        success: function (data) {
            if ('id' in data) {
                CloneData[data.id] = data;
            }
            else{
                console.log(data);
            }
        },
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    })
}

var SetLogData = function (data) {
    return $.ajax({
        url: 'logs/api/update/',
        async: false,
        type: 'PATCH',
        data: {
            data: data
        },
        success: function (data) {
            if ('id' in data) {
                console.log('A review log has been updated/created in backend.')
            }
        },
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    })
}


