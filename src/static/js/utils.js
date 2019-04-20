String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

var Helper = {
    DataTable: {
        ReviewLogRetrieve: {
            Container: $('.review-log-datatable'),
            Setup: function() {
                this.Container.each(function(){

                    if(!$.fn.DataTable.isDataTable($(this))){
                        var url = $(this).data('url');
                        var table = $(this).DataTable({
                            processing: true,
                            serverSide: true,
                            ajax: {
                                url: url,
                                type: "GET",
                            },
                            language: {
                                "processing":   "處理中...",
                                "loadingRecords": "載入中...",
                                "lengthMenu":   "顯示 _MENU_ 項結果",
                                "zeroRecords":  "沒有符合的結果",
                                "info":         "顯示第 _START_ 至 _END_ 項結果，共 _TOTAL_ 項",
                                "infoEmpty":    "顯示第 0 至 0 項結果，共 0 項",
                                "infoFiltered": "(從 _MAX_ 項結果中過濾)",
                                "infoPostFix":  "",
                                "search":       "搜尋:",
                                "paginate": {
                                    "first":    "第一頁",
                                    "previous": "上一頁",
                                    "next":     "下一頁",
                                    "last":     "最後一頁"
                                },
                                "aria": {
                                    "sortAscending":  ": 升冪排列",
                                    "sortDescending": ": 降冪排列"
                                }
                            },
                            columns: [
                                {
                                    title: '使用者名稱',
                                    data: 'user',
                                },
                                {
                                    title: '農戶編號',
                                    data: 'content_object',
                                },
                                {
                                    title: '原始錯誤數',
                                    data: 'initial_errors',
                                    sortable: false,
                                },
                                {
                                    title: '目前錯誤數',
                                    data: 'current_errors',
                                },
                                {
                                    title: '上次更新',
                                    data: 'update_datetime',
                                },
                            ],
                            order: [[ 4, "desc" ]],
                        });

                    }else $(this).DataTable().ajax.reload();
                })

            },
            Reload: function(){
                this.Container.each(function(){
                    if($.fn.DataTable.isDataTable($(this))) $(this).DataTable().ajax.reload();
                })
            },
        },
    },
    Counter: {
        UI: '<span class="badge alert-danger"></span>',
        Create: function(){
            var $ui = $(this.UI);
            $ui.bind('set', function(event, number){
                $(this).html(number);
            })
            return $ui;
        },
    },
    NumberValidate: function (number) {
        return $.isNumeric(number) && Math.floor(number) == number && number >= 0;
    },
    LogHandler: {
        Setup: function(){
            this.Bind();
            this.ValidationActive = true;
        },
        Bind: function(){
            $('.alert').on('click', '.btn-warning', function(){
                this.click();
            })
        },
        UI: '\
            <p data-guid="" data-group-guid="" style="line-height:30px;">\
                <span></span>\
                <button type="button" class="btn btn-warning btn-sm pull-right">\
                    <i class="fa fa-remove" aria-hidden="true"></i>例外\
                </button>\
            </p>\
        ',
        Create: function(alert, msg, guid, groupGuid, removeAble){
            removeAble = removeAble !== false;
            $ui = $(this.UI);
            $ui.attr('data-guid', guid);
            $ui.attr('data-group-guid', groupGuid);
            $ui.find('span').html(msg);
            $ui[0].Alert = alert;
            $ui.find('.btn')[0].click = function(){
                var $ui = $(this).parent();
                var guid = $ui.data('guid');
                var alert =  $ui[0].Alert;
                $ui.remove();
                alert.skippedErrorGuids.push(guid);
                alert.alert();
                alert.count();
            }
            if(!removeAble){
                $ui.find('.btn').remove();
            }
            return $ui;
        },
        Log: function (condition, alert, msg, guid, groupGuid, removeAble) {
            if(!this.ValidationActive) return;
            var guid = guid || '';
            var groupGuid = groupGuid || ''
            var $ui = this.Create(alert, msg, guid, groupGuid, removeAble);
            var finds = alert.message.find('p[data-guid="{0}"][data-group-guid="{1}"]'.format(guid, groupGuid));
            if (condition) {
                if (finds.length == 0 && alert.skippedErrorGuids.indexOf(guid) == -1) {
                    alert.message.append($ui);
                }
                if (finds.length == 1){
                    finds.replaceWith($ui); // update text
                }
            } else {
                finds.remove();
            }
            alert.alert();
            alert.count();
        },
        DeleteRow: function(alert, $row, $nextAll){
            function removeAlert($tr){
                var guid = $tr.data('guid');
                alert.message.find('[data-group-guid="{0}"]'.format(guid)).remove();
            }
            // remove current row alert
            removeAlert($row);
            // update nextAll row index
            $nextAll.each(function(){
                var guid = $(this).data('guid');
                alert.message.find('[data-group-guid="{0}"]'.format(guid)).each(function(){
                    var $index = $(this).find('.row-index');
                    var newIndex = parseInt($index.text()) - 1;
                    $index.html(newIndex);
                })
            })
            alert.alert();
        },
        CollectError: {
            InitialErrors: null,
            Init: function(){
                // init only once after get survey
                this.InitialErrors = this.GetCurrent();
            },
            GetCurrent: function(){
                var counter = 0;
                $('.alert-block.alert-danger').each(function(){
                    counter += this.alert.currentErrors;
                })
                return counter;
            },
            GetSkipped: function(){
                var counter = 0;
                $('.alert-block.alert-danger').each(function(){
                    counter += this.alert.skippedErrorGuids.length;
                })
                return counter;
            },
        },
    },
    Alert: function ($obj) {
        /* store skippedErrorGuids */
        this.currentErrors = 0;
        this.skippedErrorGuids = [];
        this.$object = $obj.addClass('alert-block');
        this.message = $('<div>');
        this.alert = function () {
            if (this.message.html()) {
                this.$object.html(this.message).show();
            }else {
                this.$object.hide();
            }
        };
        this.reset = function () {
            this.message = $('<div>');
            this.$object.html(this.message).hide();
            this.currentErrors = 0;
        }
        this.count = function(){
            /* count for self */
            this.currentErrors = this.message.find('p[data-guid]').length;
            /* count for panel */
            var panelId = $obj.closest('.panel').attr('id');
            var $tab = $('.js-tabs-control[data-target="#{0}"]'.format(panelId));
            if($tab){
                var $ui = $tab.find('.badge');
                if($ui.length == 0){
                    $ui = Helper.Counter.Create().appendTo($tab);
                }
                var errorCount = $('#{0} .alert-danger p[data-guid]'.format(panelId)).length;
                $ui.trigger('set', errorCount);
            }

        },
        this.$object[0].alert = this;
        this.$object.hide();
    },
    Dialog: {
        ShowAlert: function(message){
            BootstrapDialog.closeAll();
            BootstrapDialog.show({
                title: '錯誤訊息',
                message: message,
                type: BootstrapDialog.TYPE_DANGER,
                buttons: [{
                    label: '確定',
                    action: function (dialogRef) {
                       dialogRef.close();
                    }
                }]
            });
        },
        ShowInfo: function(message){
            BootstrapDialog.closeAll();
            BootstrapDialog.show({
                title: '訊息',
                message: message,
                type: BootstrapDialog.TYPE_INFO,
                buttons: [{
                    label: '確定',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }]
            });
        },
        DeleteRow: function(deferred){
            BootstrapDialog.confirm({
                title: '刪除資料列',
                message: '確定要刪除本筆資料？',
                callback: function(result){
                    if(result){
                        deferred.resolve();
                    };
                },
                type: BootstrapDialog.TYPE_WARNING,
            });
            return deferred.promise();
        },
    },
    Guid: {
        Create: function(){
            function s4() {
                return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
            }
            return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
        },
        CreateMulti: function(length){
            var length = length || 0;
            var array = [];
            for(var i = 0; i <= length; i++){
                array.push(Helper.Guid.Create())
            }
            return array;
        },
    },
    BindInterOnly: function($obj){
        $obj.keydown(function (e) {
            // Allow: backspace, delete, tab, escape, enter and .
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
                 // Allow: Ctrl+A, Command+A
                (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
                 // Allow: home, end, left, right, down, up
                (e.keyCode >= 35 && e.keyCode <= 40)) {
                     // let it happen, don't do anything
                     return;
            }
            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    },
    BindCreateIndex: function($tbody){
        $tbody[0].refreshIndex = function(){
            $(this).find('tr').each(function(i, row){
                $(row).find('[name="index"]').html(i+1);
            })
        }
    },
    ClearString: function(s){
        var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）&;|{}【】‘；：”“'。，、？]")
        var rs = "";
        for (var i = 0; i < s.length; i++) {
            rs = rs+s.substr(i, 1).replace(pattern, '');
        }
        return rs;
    },
    NumberWithCommas: function(num){
        return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
    },
}
