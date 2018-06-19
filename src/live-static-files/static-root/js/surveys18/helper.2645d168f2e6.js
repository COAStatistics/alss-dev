/* rendered ui */
var GlobalUI = $.parseJSON($('#ui').val());
var FarmerIds = $.parseJSON($('#fid').val());

/* data */
var CloneData = null;
var MainSurveyId = 0;

/* Validate */
var Validate = true;

/* jQuery Loading settings */
$.loading.default.tip = '請稍後';
$.loading.default.imgPath = '../static/vendor/ajax-loading/img/ajax-loading.gif';

/* BootstrapDialog settings */
BootstrapDialog.DEFAULT_TEXTS['OK'] = '確定';
BootstrapDialog.DEFAULT_TEXTS['CANCEL'] = '取消';
BootstrapDialog.DEFAULT_TEXTS['CONFIRM'] = '確認';

$(document).ready(function () {
    /* jQuery Spinner */
    var Loading = $.loading();
    /* setup*/
    Setup(GlobalUI);
})

var Reset = function () {
    SurveyHelper.Reset();
    LandAreaHelper.Reset();
    BusinessHelper.Reset();
    ManagementTypeHelper.Reset();
    CropMarketingHelper.Reset();
    LivestockMarketingHelper.Reset();
    AnnualIncomeHelper.Reset();
    PopulationAgeHelper.Reset();
    PopulationHelper.Reset();
    LongTermHireHelper.Reset();
    ShortTermHireHelper.Reset();
    NoSalaryHireHelper.Reset();
    LongTermLackHelper.Reset();
    ShortTermLackHelper.Reset();
    SubsidyHelper.Reset();
}
var Set = function (data, surveyId) {
    if (data.page == 1) {
        MainSurveyId = surveyId;
        SurveyHelper.Set(data);
        LandAreaHelper.Set(data.land_areas);
        BusinessHelper.Set(data.businesses);
        ManagementTypeHelper.Set(data.management_types);
        AnnualIncomeHelper.Set(data.annual_incomes);
        PopulationAgeHelper.Set(data.population_ages);
        ShortTermHireHelper.Set(data.short_term_hires);
        NoSalaryHireHelper.Set(data.no_salary_hires);
        SubsidyHelper.Set(data.subsidy);
    }
    /* need setting survey surveyId to locate which obj */
    CropMarketingHelper.Set(data.crop_marketings, surveyId);
    LivestockMarketingHelper.Set(data.livestock_marketings, surveyId);
    PopulationHelper.Set(data.populations, surveyId);
    LongTermHireHelper.Set(data.long_term_hires, surveyId);
    LongTermLackHelper.Set(data.long_term_lacks, surveyId);
    ShortTermLackHelper.Set(data.short_term_lacks, surveyId);

    if(Validate){
        CropMarketingHelper.Validation.IncomeChecked.Validate();
        LivestockMarketingHelper.Validation.IncomeChecked.Validate();
        AnnualIncomeHelper.Validation.CropMarketingExist.Validate();
        AnnualIncomeHelper.Validation.LivestockMarketingExist.Validate();
        SurveyHelper.Hire.Validation.HireExist.Validate();
        SurveyHelper.Lack.Validation.LackExist.Validate();
    }
}

var Setup = function(globalUI){
    SurveyHelper.Setup();
    LandAreaHelper.Setup();
    BusinessHelper.Setup();
    ManagementTypeHelper.Setup();
    AnnualIncomeHelper.Setup();
    PopulationAgeHelper.Setup();
    SubsidyHelper.Setup();

    CropMarketingHelper.Setup(globalUI.cropmarketing);
    LivestockMarketingHelper.Setup(globalUI.livestockmarketing);
    PopulationHelper.Setup(globalUI.population);
    LongTermHireHelper.Setup(globalUI.longtermhire);
    LongTermLackHelper.Setup(globalUI.longtermlack);
    ShortTermHireHelper.Setup(globalUI.shorttermhire);
    ShortTermLackHelper.Setup(globalUI.shorttermlack);
    NoSalaryHireHelper.Setup(globalUI.nosalaryhire);
}

var Helper = {
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
    LogHandler: function (condition, alert, msg) {
        var tag = msg.prop('tagName');
        var guid = msg.data('guid');
        var text = msg.text();
        var finds = alert.message.find('{0}[data-guid="{1}"]:contains({2})'.format(tag, guid, text));
        if (condition) {
            if (finds.length == 0) {
                alert.message.append(msg);
            }
        } else {
            finds.remove();
        }
        alert.alert();
        alert.count();
    },
    Alert: function ($obj) {
        this.$object = $obj;
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
        }
        this.count = function(){
            var panelId = $obj.closest('.panel').attr('id');
            var $tab = $('.js-tabs-control[data-target="#{0}"]'.format(panelId));
            if($tab){
                var $ui = $tab.find('.badge');
                if($ui.length == 0){
                    $ui = Helper.Counter.Create().appendTo($tab);
                }
                var errorCount = $('#{0} .alert p[data-guid]'.format(panelId)).length;
                $ui.trigger('set', errorCount);
            }
        },
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
        }
    },
    CreateGuid: function(){
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
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
}

var SurveyHelper = {
    Alert: null,
    Setup: function() {
        this.Alert = new Helper.Alert($('.alert[name="survey"]'));

        this.Hire.Setup();
        this.Lack.Setup();

        this.FarmerName.Bind();
        this.Phone.Bind();
        this.AddressMatch.Bind();
        this.Address.Bind();
        this.Hire.Bind();
        this.Lack.Bind();
        this.Note.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.FarmerId.Reset();
        this.FarmerName.Reset();
        this.Phone.Reset();
        this.AddressMatch.Reset();
        this.Address.Reset();
        this.Hire.Reset();
        this.Lack.Reset();
        this.Note.Reset();
    },
    Set: function (obj) {
        this.FarmerId.Set(obj);
        this.Phone.Set(obj);
        this.FarmerName.Set(obj);
        this.AddressMatch.Set(obj);
        this.Address.Set(obj);
        this.Hire.Set(obj);
        this.Lack.Set(obj);
        this.Note.Set(obj);
    },
    FarmerId: {
        Container: $('#panel1 input[name="farmerid"]'),
        Set: function(obj){
            this.Container.val(obj.farmer_id);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    FarmerName: {
        Container: $('#panel1 input[name="farmername"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData) {
                    CloneData[MainSurveyId].farmer_name = $(this).val();

                    if(Validate){
                        SurveyHelper.FarmerName.Validation.Empty.Validate();
                    }
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.farmer_name);
            if(Validate){
                SurveyHelper.FarmerName.Validation.Empty.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Validation: {
            Empty: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var empty = CloneData[MainSurveyId].farmer_name == '';
                    var msg = $('<p data-guid="{0}">受訪人不可漏填</p>'.format(this.Guid));
                    Helper.LogHandler(empty, SurveyHelper.Alert, msg);
                },
            },
        },
    },
    Phone: {
        Object: {
            Filter: function(id){
                var objects = CloneData[MainSurveyId].phones.filter(function(obj){
                    return obj.id == id;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel1 input[name="phone"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData) {
                    var id = $(this).data('phone-id');
                    SurveyHelper.Phone.Object.Filter(id).phone = $(this).val();

                    if(Validate){
                        SurveyHelper.Phone.Validation.Empty.Validate();
                    }
                }
            })
        },
        Set: function(obj){
            obj.phones.forEach(function(phone, i){
                SurveyHelper.Phone.Container.eq(i)
                .attr('data-phone-id', phone.id)
                .val(phone.phone);
            })
            if(Validate){
                SurveyHelper.Phone.Validation.Empty.Validate();
            }
        },
        Reset: function(){
                SurveyHelper.Phone.Container.val('');
        },
        Validation: {
            Empty: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var empty = true;
                    CloneData[MainSurveyId].phones.forEach(function(obj, i){
                        if(obj.phone){
                            empty = false;
                        }
                    });
                    var msg = $('<p data-guid="{0}">聯絡電話不可漏填</p>'.format(this.Guid));
                    Helper.LogHandler(empty, SurveyHelper.Alert, msg);
                },
            },
        },
    },
    Hire: {
        Alert: null,
        Setup: function(){
            this.Alert = new Helper.Alert($('.alert[name="hire"]'));
        },
        Container: $('#panel4 input[name="hire"]'),
        Bind: function(){
            this.Container.change(function(){

                /* make it radio */
                var deChecked = function(input){
                    var deferred = $.Deferred();
                    SurveyHelper.Hire.Container.not(input).prop('checked', false);
                    deferred.resolve();
                }

                if(CloneData) {
                    $.when(deChecked(this)).then(function(){
                        var field = $(this).data('field');
                        if(field == 'hire')
                            CloneData[MainSurveyId].hire = this.checked;
                        else if(field == 'nonhire')
                            CloneData[MainSurveyId].non_hire = this.checked;

                        if(Validate){
                            SurveyHelper.Hire.Validation.Empty.Validate();
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                        }
                    })
                }
            })
        },
        Set: function (obj) {
            this.Container.filter('[data-field="hire"]').prop('checked', obj.hire);
            this.Container.filter('[data-field="nonhire"]').prop('checked', obj.non_hire);

            if(Validate){
                SurveyHelper.Hire.Validation.Empty.Validate();
                SurveyHelper.Hire.Validation.SingleSelection.Validate();
            }
        },
        Reset: function(){
            if (this.Alert) { this.Alert.reset(); }
            this.Container.prop('checked', false);
        },
        Validation: {
            Empty: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var con = SurveyHelper.Hire.Container.filter(':checked').length == 0;
                    var msg = $('<p data-grid="{0}">不可漏填此問項</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Hire.Alert, msg);
                },
            },
            SingleSelection: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var con = SurveyHelper.Hire.Container.filter(':checked').length > 1;
                    var msg = $('<p data-grid="{0}">限註記一個項目</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Hire.Alert, msg);
                },
            },
            HireExist: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var checked = SurveyHelper.Hire.Container.filter('[data-field="nonhire"]').prop('checked');
                    var exists = LongTermHireHelper.LongTermHire.Container.find('tr').length +
                                 ShortTermHireHelper.ShortTermHire.Container.find('tr').length +
                                 NoSalaryHireHelper.NoSalaryHire.Container.find('tr').length > 0;
                    var con = checked && exists;
                    msg = $('<p data-guid="{0}">勾選無外僱人力，【問項3.1.2及3.1.3及3.1.4】應為空白</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Hire.Alert, msg);

                    var con = !checked && !exists;
                    msg = $('<p data-guid="{0}">若全年無外僱人力，應勾選無</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Hire.Alert, msg);
                },
            },
        },
    },
    Lack: {
        Alert: null,
        Setup: function(){
            this.Alert = new Helper.Alert($('.alert[name="lack"]'));
        },
        Container: $('#panel4 input[name="lack"]'),
        Bind: function(){
            this.Container.change(function(){
                var id = $(this).data('lack-id');
                if(CloneData){
                    /* make it radio */
                    var deChecked = function(){
                        var deferred = $.Deferred();
                        SurveyHelper.Lack.Container.not('[data-lack-id="{0}"]'.format(id)).prop('checked', false)
                        deferred.resolve();
                    }
                    $.when(deChecked()).then(function(){
                        var lacks = []
                        SurveyHelper.Lack.Container.each(function(){
                            var id = $(this).data('lack-id');
                            if($(this).prop('checked')) lacks.push(id);
                        })
                        CloneData[MainSurveyId].lacks = lacks;
                    })

                    if(Validate){
                        SurveyHelper.Lack.Validation.Empty.Validate();
                        SurveyHelper.Lack.Validation.SingleSelection.Validate();
                        SurveyHelper.Lack.Validation.LackExist.Validate();
                    }
                }
            })
        },
        Set: function(obj) {
            obj.lacks.forEach(function(lack, i){
                SurveyHelper.Lack.Container
                .filter('[data-lack-id="{0}"]'.format(lack))
                .prop('checked', true);
            })

            if(Validate){
                SurveyHelper.Lack.Validation.Empty.Validate();
                SurveyHelper.Lack.Validation.SingleSelection.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Validation: {
            Empty: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var con = SurveyHelper.Lack.Container.filter(':checked').length == 0;
                    var msg = $('<p data-grid="{0}">不可漏填此問項</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Lack.Alert, msg);
                },
            },
            SingleSelection: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var con = SurveyHelper.Lack.Container.filter(':checked').length > 1;
                    var msg = $('<p data-grid="{0}">限註記一個項目</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Lack.Alert, msg);
                },
            },
            LackExist: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var checked = SurveyHelper.Lack.Container.filter('[data-islack="false"]:checked').length == 1;
                    var exists = LongTermLackHelper.LongTermLack.Container.find('tr').length +
                                 ShortTermLackHelper.ShortTermLack.Container.find('tr').length > 0;
                    var con = checked && exists;
                    msg = $('<p data-guid="{0}">勾選無短缺人力，【問項3.2.2及3.2.3】應為空白</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Lack.Alert, msg);

                    var con = !checked && !exists;
                    msg = $('<p data-guid="{0}">若全年無短缺人力，應勾選無</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Lack.Alert, msg);
                },
            },
        },
    },
    Note: {
        Container: $('#panel1 textarea[name="note"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    CloneData[MainSurveyId].note = $(this).val();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.note);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    AddressMatch: {
        Container: $('#panel1 input[name="addressmatch"]'),
        Bind: function(){
            this.Container.change(function(){
                /* make it radio */
                SurveyHelper.AddressMatch.Container.not($(this)).prop('checked', false);

                if(CloneData){
                    var field = $(this).data('field');
                    if(field == 'match')
                        CloneData[MainSurveyId].address_match.match = $(this).prop('checked');
                    else if(field == 'mismatch')
                        CloneData[MainSurveyId].address_match.mismatch = $(this).prop('checked');
                }
                if(Validate) {
                    SurveyHelper.Address.Validation.AddressRequire.Validate();
                    SurveyHelper.AddressMatch.Validation.AddressMatchRequire.Validate();
                }
            })
        },
        Set: function(obj){
            this.Container.filter('[data-field="match"]').prop('checked', obj.address_match.match);
            this.Container.filter('[data-field="mismatch"]').prop('checked', obj.address_match.mismatch);
            if(Validate){
                SurveyHelper.Address.Validation.AddressRequire.Validate();
                SurveyHelper.AddressMatch.Validation.AddressMatchRequire.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Validation: {
            AddressMatchRequire: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var checked = SurveyHelper.AddressMatch.Container
                                 .filter('[data-field="mismatch"]')
                                 .prop('checked');
                    var empty = !SurveyHelper.Address.Container.val();
                    var con = !checked && !empty;
                    var msg = $('<p data-guid="{0}">填寫地址，請勾選地址與調查名冊不同</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Alert, msg);
                },
            },
        },
    },
    Address: {
        Container: $('#panel1 input[name="address"]'),
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    CloneData[MainSurveyId].address_match.address = $(this).val();
                }
                if(Validate) {
                    SurveyHelper.Address.Validation.AddressRequire.Validate();
                    SurveyHelper.AddressMatch.Validation.AddressMatchRequire.Validate();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.address_match.address);
            if(Validate) {
                SurveyHelper.Address.Validation.AddressRequire.Validate();
                SurveyHelper.AddressMatch.Validation.AddressMatchRequire.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Validation: {
            AddressRequire: {
                Guid: Helper.CreateGuid(),
                Validate: function(){
                    var checked = SurveyHelper.AddressMatch.Container
                                 .filter('[data-field="mismatch"]')
                                 .prop('checked');
                    var empty = !SurveyHelper.Address.Container.val();
                    var con = checked && empty;
                    var msg = $('<p data-guid="{0}">勾選地址與調查名冊不同，地址不可為空白</p>'.format(this.Guid));
                    Helper.LogHandler(con, SurveyHelper.Alert, msg);
                },
            },
        }
    },
    NumberWorker : {
        Object: {
            New: function(ageScopeId, count, id){
                var obj = {
                    age_scope: ageScopeId,
                    count: count,
                }
                if(id) obj.id = id;
                return obj;
            },
            Collect: function($objects){
                var objects = []
                $objects.each(function(){
                    var count = parseInt($(this).val());
                    var ageScopeId = $(this).data('agescope-id');
                    var id = $(this).data('numberworker-id');
                    if(parseInt(count) > 0 && Helper.NumberValidate(count)){
                        objects.push(
                            SurveyHelper.NumberWorker.Object.New(ageScopeId, count, id ? id : null)
                        );
                    }
                })
                return objects;
            },
        }
    }
}
var LandAreaHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert[name="landarea"]'));
        this.LandStatus.Bind();
        this.LandType.Bind();
        this.Validation.Setup();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LandType.Reset();
        this.LandStatus.Reset();
    },
    Set: function (array) {
        this.LandType.Set(array);
        this.LandStatus.Set(array);
    },
    LandType: {
        Container: $('#panel2 input[name="landtype"]'),
        Set: function(array){
            array.forEach(function(land_area, i){
                LandAreaHelper.LandType.Container
                .filter('[data-landtype-id="{0}"]'.format(land_area.type))
                .prop('checked', true);
            })

            if(Validate){
                LandAreaHelper.Validation.Empty.Validate();
                LandAreaHelper.Validation.LandStatusEmpty.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                var checked = $(this).prop('checked');
                var type = $(this).data('landtype-id');
                if(!checked){
                    LandAreaHelper.LandStatus.Container
                    .filter('[data-landtype-id="{0}"]'.format(type))
                    .val('').trigger('change');
                }

                if(CloneData){
                    LandAreaHelper.Object.Collect();
                    if(Validate){
                        LandAreaHelper.Validation.Empty.Validate();
                        LandAreaHelper.Validation.LandStatusEmpty.Validate();
                    }
                }
            })
        },
    },
    LandStatus: {
        Container: $('#panel2 input[name="landstatus"]'),
        Set: function(array){
            array.forEach(function(land_area){
                LandAreaHelper.LandStatus.Container
                .filter('[data-landtype-id="{0}"]'.format(land_area.type))
                .filter('[data-landstatus-id="{0}"]'.format(land_area.status))
                .val(land_area.value)
            })

            if(Validate){
                LandAreaHelper.Validation.Empty.Validate();
                LandAreaHelper.Validation.LandStatusEmpty.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            Helper.BindInterOnly(this.Container);
            this.Container.keydown(function(e){
                /* make sure checked when inputs add value */
                var typeId = $(this).data('landtype-id');
                var typeChecked = LandAreaHelper.LandType.Container
                                  .filter('[data-landtype-id="{0}"]'.format(typeId))
                                  .prop('checked');
                if(!typeChecked){
                    Helper.Dialog.ShowAlert('請先勾選耕作地類型選項');
                    e.preventDefault();
                }
            })
            this.Container.change(function(){
                if(CloneData){
                    LandAreaHelper.Object.Collect();
                    if(Validate){
                        LandAreaHelper.Validation.Empty.Validate();
                        LandAreaHelper.Validation.LandStatusEmpty.Validate();
                    }
                }
            })
        }
    },
    Object: {
        New: function(surveyId, typeId, statusId, value){
            var obj = {
                survey: surveyId,
                type: typeId,
            }
            if(statusId) obj.status = statusId;
            if(value) obj.value = value;
            return obj;
        },
        Collect: function(){
            var landAreas = [];
            LandAreaHelper.LandType.Container
            .filter(':checked')
            .each(function(){
                var typeId = $(this).data('landtype-id');

                var hasAnyValuedStatus = false;
                /* collect multiple object if has status */
                LandAreaHelper.LandStatus.Container
                .filter('[data-landtype-id="{0}"]'.format(typeId))
                .each(function(){
                    var statusId = $(this).data('landstatus-id');
                    var value = $(this).val();
                    if(Helper.NumberValidate(value)){
                        hasAnyValuedStatus = true;
                        landAreas.push(
                            LandAreaHelper.Object.New(MainSurveyId, typeId, statusId, value)
                        )
                    }
                })
                /* collect one object if none status */
                if(!hasAnyValuedStatus){
                    landAreas.push(
                        LandAreaHelper.Object.New(MainSurveyId, typeId)
                    )
                }
            })
            CloneData[MainSurveyId].land_areas = landAreas;
        }
    },
    Validation: {
        Setup: function(){
            this.LandStatusEmpty.Guid.Setup();
        },
        Empty: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var empty = CloneData[MainSurveyId].land_areas.length == 0;
                var msg = $('<p data-guid="{0}">不可漏填此問項</p>'.format(this.Guid));
                Helper.LogHandler(empty, LandAreaHelper.Alert, msg);
            },
        },
        LandStatusEmpty: {
            Guid: {
                Object: {},
                Setup: function(){
                    obj = this.Object;
                    LandAreaHelper.LandType.Container.each(function(){
                        var landTypeId = $(this).data('landtype-id');
                        obj[landTypeId] = Helper.CreateGuid();
                    })
                },
                Filter: function(landTypeId){
                    return this.Object[landTypeId];
                },
            },
            Validate: function(){
                LandAreaHelper.LandType.Container.each(function(){
                    var landTypeName = $(this).data('landtype-name');
                    var landTypeId = $(this).data('landtype-id');
                    var checked = $(this).prop('checked');
                    var statuses = LandAreaHelper.LandStatus.Container.filter('[data-landtype-id="{0}"]'.format(landTypeId));
                    var has_status = statuses.length > 0;
                    var empty = true;
                    statuses.each(function(){
                        if($(this).val()){
                            empty = false;
                        }
                    })
                    var con = checked && (has_status && empty);
                    var guid = LandAreaHelper.Validation.LandStatusEmpty.Guid.Filter(landTypeId);
                    var msg = $('<p data-guid="{0}">有勾選{1}應填寫對應面積</p>'.format(guid, landTypeName));
                    Helper.LogHandler(con, LandAreaHelper.Alert, msg);
                })
            }
        },
    },
}
var BusinessHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert[name="business"]'));
        this.FarmRelatedBusiness.Bind();
        this.Extra.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         this.FarmRelatedBusiness.Reset();
         this.Extra.Reset();
    },
    Set: function(array){
        this.FarmRelatedBusiness.Set(array);
        this.Extra.Set(array);
    },
    FarmRelatedBusiness: {
        Container: $('#panel2 input[name="farmrelatedbusiness"]'),
        Set: function(array){
            array.forEach(function(business, i){
                BusinessHelper.FarmRelatedBusiness.Container
                .filter('[data-farmrelatedbusiness-id="{0}"]'.format(business.farm_related_business))
                .prop('checked', true);
            })
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                var checked = $(this).prop('checked');
                var farmerRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                if(!checked){
                    BusinessHelper.Extra.Container
                    .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farmerRelatedBusinessId))
                    .val('');
                }

                if(CloneData){
                    BusinessHelper.Object.Collect();
                    if(Validate){
                        BusinessHelper.Validation.Empty.Validate();
                        BusinessHelper.Validation.Duplicate.Validate();
                    }
                }
            })
        },
    },
    Extra: {
        Container: $('#panel2 input[name="extra"]'),
        Set: function(array){
            array.forEach(function(business, i){
                BusinessHelper.Extra.Container
                .filter('[data-farmrelatedbusiness-id="{0}"]'.format(business.farm_related_business))
                .val(business.extra);
            })
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            this.Container.keydown(function(e){
                /* make sure checked when inputs add value */
                var farmRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                var checked = BusinessHelper.FarmRelatedBusiness.Container
                              .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farmRelatedBusinessId))
                              .prop('checked');
                if(!checked){
                    Helper.Dialog.ShowAlert('請先勾選農業相關事業選項');
                    e.preventDefault();
                }
            })
            this.Container.change(function(){
                if(CloneData){
                    BusinessHelper.Object.Collect();
                    if(Validate){
                        BusinessHelper.Validation.Empty.Validate();
                        BusinessHelper.Validation.Duplicate.Validate();
                    }
                }
            })
        },
    },
    Object: {
        New: function(surveyId, farmRelatedBusinessId, extra){
            var obj = {
                survey: surveyId,
                farm_related_business: farmRelatedBusinessId,
            }
            if(extra) obj.extra = extra;
            return obj;
        },
        Collect: function(){
            businesses = []
            BusinessHelper.FarmRelatedBusiness.Container
            .filter(':checked')
            .each(function(){
                var farmRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                var extra = BusinessHelper.Extra.Container
                            .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farmRelatedBusinessId)).val();
                businesses.push(
                    BusinessHelper.Object.New(MainSurveyId, farmRelatedBusinessId, extra ? extra : null)
                )
            })

            CloneData[MainSurveyId].businesses = businesses;
        },
    },
    Validation: {
        Empty: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var con = CloneData[MainSurveyId].businesses.length == 0;
                var msg = $('<p data-guid="{0}">不可漏填此問項</p>'.format(this.Guid));
                Helper.LogHandler(con, BusinessHelper.Alert, msg);
            }
        },
        Duplicate: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var trueChecked = false;
                var falseChecked = false;
                BusinessHelper.FarmRelatedBusiness.Container
                .filter(':checked')
                .each(function(){
                    var hasBusiness = $(this).data('has-business');
                    if(hasBusiness) trueChecked = true;
                    else falseChecked = true;
                })
                var con = trueChecked && falseChecked;
                var msg = $('<p data-guid="{0}">無兼營與有兼營不可重複勾選</p>'.format(this.Guid));
                Helper.LogHandler(con, BusinessHelper.Alert, msg);
            },
        },

    },
}
var ManagementTypeHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert[name="managementtype"]'));
        this.ManagementType.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         this.ManagementType.Reset();
    },
    Set: function(array){
        this.ManagementType.Set(array);
    },
    ManagementType: {
        Container: $('#panel2 input[name=managementtype]'),
        Set: function(array){
            array.forEach(function(management_type, i){
                ManagementTypeHelper.ManagementType.Container
                .filter('[data-managementtype-id="{0}"]'.format(management_type))
                .prop('checked', true);
            })

            if(Validate){
                ManagementTypeHelper.Validation.Empty.Validate();
                ManagementTypeHelper.Validation.SingleSelection.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    managementTypes = [];
                    ManagementTypeHelper.ManagementType.Container
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('managementtype-id');
                        managementTypes.push(id);
                    });
                    CloneData[MainSurveyId].management_types = managementTypes;

                    if(Validate){
                        ManagementTypeHelper.Validation.Empty.Validate();
                        ManagementTypeHelper.Validation.SingleSelection.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Empty: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var con = CloneData[MainSurveyId].management_types.length == 0;
                var msg = $('<p data-guid="{0}">不可漏填此問項</p>'.format(this.Guid));
                Helper.LogHandler(con, ManagementTypeHelper.Alert, msg);
            },
        },
        SingleSelection: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var con = CloneData[MainSurveyId].management_types.length > 1;
                var msg = $('<p data-guid="{0}">限註記一個項目</p>'.format(this.Guid));
                Helper.LogHandler(con, ManagementTypeHelper.Alert, msg);
            }
        },
    },
}
var CropMarketingHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="cropmarketing"]'));
        var $row = $(row);
        this.CropMarketing.Bind($row);
        this.CropMarketing.$Row = $row;
        this.Adder.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.CropMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.CropMarketing.Set(array, surveyId);
        if(Validate){
            CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                CropMarketingHelper.Validation.RequiredField.Validate($(this));
            })
        }
    },
    CropMarketing: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                objects = CloneData[surveyId].crop_marketings.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel2 table[name="cropmarketing"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(crop_marketing, i){
                var $row = CropMarketingHelper.CropMarketing.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', crop_marketing.product);
                $row.find('input[name="landnumber"]').val(crop_marketing.land_number);
                $row.find('input[name="landarea"]').val(crop_marketing.land_area);
                $row.find('input[name="planttimes"]').val(crop_marketing.plant_times);
                $row.find('select[name="unit"]').selectpicker('val', crop_marketing.unit);
                $row.find('input[name="totalyield"]').val(crop_marketing.total_yield);
                $row.find('input[name="unitprice"]').val(crop_marketing.unit_price);
                $row.find('select[name="hasfacility"]').selectpicker('val', crop_marketing.has_facility);
                $row.find('select[name="loss"]').selectpicker('val', crop_marketing.loss);

                $row.attr('data-survey-id', surveyId);

                crop_marketing.guid = Helper.CreateGuid();
                $row.attr('data-guid', crop_marketing.guid);

                CropMarketingHelper.CropMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));

            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].crop_marketings = CloneData[surveyId].crop_marketings.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();

                        if(Validate){
                            var guid = $tr.data('guid');
                            CropMarketingHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            CropMarketingHelper.Alert.alert();
                            AnnualIncomeHelper.Validation.CropMarketingExist.Validate();
                        }
                    })
                }

            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId =$tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = CropMarketingHelper.CropMarketing.Object.Filter(surveyId, guid);
                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.land_number = parseInt($tr.find('[name="landnumber"]').val());
                    obj.loss = parseInt($tr.find('[name="loss"]').val());
                    obj.plant_times = parseInt($tr.find('[name="planttimes"]').val());
                    obj.unit = parseInt($tr.find('[name="unit"]').val());
                    obj.has_facility = parseInt($tr.find('[name="hasfacility"]').val());
                    obj.unit_price = parseInt($tr.find('[name="unitprice"]').val());
                    obj.land_area = parseInt($tr.find('[name="landarea"]').val());
                    obj.total_yield = parseInt($tr.find('[name="totalyield"]').val());

                    if(Validate){
                        CropMarketingHelper.Validation.RequiredField.Validate($tr);
                    }
                }
            })



            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="cropmarketing"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = CropMarketingHelper.CropMarketing.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].crop_marketings.push(obj);

                    $row = CropMarketingHelper.CropMarketing.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    CropMarketingHelper.CropMarketing.Container.append($row);

                    if(Validate){
                        CropMarketingHelper.Validation.RequiredField.Validate($row);
                        CropMarketingHelper.Validation.IncomeChecked.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = CropMarketingHelper.CropMarketing.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="product"]').val(), CropMarketingHelper.Alert, makeString('作物名稱'));
                Helper.LogHandler(!$row.find('[name="landnumber"]').val(), CropMarketingHelper.Alert, makeString('耕作地代號'));
                Helper.LogHandler(!$row.find('[name="landarea"]').val(), CropMarketingHelper.Alert, makeString('種植面積'));
                Helper.LogHandler(!$row.find('[name="planttimes"]').val(), CropMarketingHelper.Alert, makeString('種植次數'));
                Helper.LogHandler(!$row.find('[name="unit"]').val(), CropMarketingHelper.Alert, makeString('單位'));
                Helper.LogHandler(!$row.find('[name="totalyield"]').val(), CropMarketingHelper.Alert, makeString('全年產量'));
                Helper.LogHandler(!$row.find('[name="unitprice"]').val(), CropMarketingHelper.Alert, makeString('平均單價'));
                Helper.LogHandler(!$row.find('[name="hasfacility"]').val(), CropMarketingHelper.Alert, makeString('是否使用農業設施'));
                Helper.LogHandler(!$row.find('[name="loss"]').val(), CropMarketingHelper.Alert, makeString('特殊情形'));
            },
        },
        IncomeChecked: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="1"]')
                              .filter(':checked').length > 0;
                var exists = CropMarketingHelper.CropMarketing.Container.find('tr').length > 0;
                var con = !checked && exists;
                var msg = $('<p data-guid="{0}">有生產農產品，【問項1.6】應有勾選『農作物及其製品』之銷售額區間</p>'.format(this.Guid));
                Helper.LogHandler(con, CropMarketingHelper.Alert, msg);
            },
        },
    },
}
var LivestockMarketingHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="livestockmarketing"]'));
        var $row = $(row);
        this.LivestockMarketing.Bind($row);
        this.LivestockMarketing.$Row = $row;
        this.Adder.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LivestockMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.LivestockMarketing.Set(array, surveyId);
        if(Validate){
            LivestockMarketingHelper.LivestockMarketing.Container.find('tr').each(function(){
                LivestockMarketingHelper.Validation.RequiredField.Validate($(this));
            })
        }
    },
    LivestockMarketing: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                objects = CloneData[surveyId].livestock_marketings.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel2 table[name="livestockmarketing"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(livestock_marketing, i){
                var $row = LivestockMarketingHelper.LivestockMarketing.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', livestock_marketing.product);
                $row.find('select[name="unit"]').selectpicker('val', livestock_marketing.unit);
                $row.find('input[name="raisingnumber"]').val(livestock_marketing.raising_number);
                $row.find('input[name="totalyield"]').val(livestock_marketing.total_yield);
                $row.find('input[name="unitprice"]').val(livestock_marketing.unit_price);
                $row.find('select[name="contract"]').selectpicker('val', livestock_marketing.contract);
                $row.find('select[name="loss"]').selectpicker('val', livestock_marketing.loss);

                $row.attr('data-survey-id', surveyId);

                livestock_marketing.guid = Helper.CreateGuid();
                $row.attr('data-guid', livestock_marketing.guid);

                LivestockMarketingHelper.LivestockMarketing.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].livestock_marketings = CloneData[surveyId].livestock_marketings.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();

                        if(Validate){
                            var guid = $tr.data('guid');
                            LivestockMarketingHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            LivestockMarketingHelper.Alert.alert();
                            AnnualIncomeHelper.Validation.LivestockMarketingExist.Validate();
                        }
                    })
                }

            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId =$tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = LivestockMarketingHelper.LivestockMarketing.Object.Filter(surveyId, guid);
                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.contract = parseInt($tr.find('[name="contract"]').val());
                    obj.loss = parseInt($tr.find('[name="loss"]').val());
                    obj.raising_number = parseInt($tr.find('[name="raisingnumber"]').val());
                    obj.total_yield = parseInt($tr.find('[name="totalyield"]').val());
                    obj.unit = parseInt($tr.find('[name="unit"]').val());
                    obj.unit_price = parseInt($tr.find('[name="unitprice"]').val());

                    if(Validate){
                        LivestockMarketingHelper.Validation.RequiredField.Validate($tr);
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="livestockmarketing"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = LivestockMarketingHelper.LivestockMarketing.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].livestock_marketings.push(obj);

                    $row = LivestockMarketingHelper.LivestockMarketing.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LivestockMarketingHelper.LivestockMarketing.Container.append($row);

                    if(Validate){
                        LivestockMarketingHelper.Validation.RequiredField.Validate($row);
                        LivestockMarketingHelper.Validation.IncomeChecked.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="product"]').val(), LivestockMarketingHelper.Alert, makeString('作物名稱'));
                Helper.LogHandler(!$row.find('[name="unit"]').val(), LivestockMarketingHelper.Alert, makeString('單位'));
                Helper.LogHandler(!$row.find('[name="raisingnumber"]').val(), LivestockMarketingHelper.Alert, makeString('年底在養數量'));
                Helper.LogHandler(!$row.find('[name="totalyield"]').val(), LivestockMarketingHelper.Alert, makeString('全年銷售數量'));
                Helper.LogHandler(!$row.find('[name="unit"]').val(), LivestockMarketingHelper.Alert, makeString('單位'));
                Helper.LogHandler(!$row.find('[name="unitprice"]').val(), LivestockMarketingHelper.Alert, makeString('平均單價'));
                Helper.LogHandler(!$row.find('[name="contract"]').val(), LivestockMarketingHelper.Alert, makeString('契約飼養'));
                Helper.LogHandler(!$row.find('[name="loss"]').val(), LivestockMarketingHelper.Alert, makeString('特殊情形'));
            },
        },
        IncomeChecked: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="2"]')
                              .filter(':checked').length > 0;
                var exists = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').length > 0;
                var con = !checked && exists;
                var msg = $('<p data-guid="{0}">有生產畜產品，【問項1.6】應有勾選『畜禽作物及其製品』之銷售額區間</p>'.format(this.Guid));
                Helper.LogHandler(con, LivestockMarketingHelper.Alert, msg);
            },
        },
    },
}
var AnnualIncomeHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert[name="annualincome"]'));
        this.AnnualIncome.Bind();
    },
    Set: function(array) {
        this.AnnualIncome.Set(array);
    },
    Reset: function() {
        this.AnnualIncome.Reset();
    },
    AnnualIncome: {
        Object: {
            New: function(surveyId, marketTypeId, incomeRangeId){
                return {
                    survey: surveyId,
                    market_type: marketTypeId,
                    income_range: incomeRangeId,
                }
            },
        },
        Container: $('#panel2 input[name="annualincome"]'),
        Set: function(array){
            array.forEach(function(annual_income, i){
                AnnualIncomeHelper.AnnualIncome.Container
                .filter('[data-incomerange-id="{0}"]'.format(annual_income.income_range))
                .filter('[data-markettype-id="{0}"]'.format(annual_income.market_type))
                .attr('data-annualincome-id', annual_income.id)
                .prop('checked', true);
            })
            if(Validate){
                AnnualIncomeHelper.Validation.IncomeTotal.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.change(function(){
                if(CloneData){
                    var annualIncomes = []

                    /* make it radio */
                    var deChecked = function($input){
                        var deferred = $.Deferred();
                        $input.closest('td').siblings().find('input').prop('checked', false)
                        deferred.resolve();
                    }

                    $.when(deChecked($(this))).then(function(){
                        AnnualIncomeHelper.AnnualIncome.Container
                        .filter(':checked')
                        .each(function(){
                            var marketTypeId = $(this).data('markettype-id');
                            var incomeRangeId = $(this).data('incomerange-id');
                            var id = $(this).data('annualincome-id');
                            var obj = AnnualIncomeHelper.AnnualIncome.Object.New(MainSurveyId, marketTypeId, incomeRangeId);
                            if(id) obj.id = id;
                            annualIncomes.push(obj);

                            if(Validate){
                                AnnualIncomeHelper.Validation.IncomeTotal.Validate();
                                AnnualIncomeHelper.Validation.CropMarketingExist.Validate();
                                AnnualIncomeHelper.Validation.LivestockMarketingExist.Validate();
                                CropMarketingHelper.Validation.IncomeChecked.Validate();
                                LivestockMarketingHelper.Validation.IncomeChecked.Validate();
                            }
                        })
                        CloneData[MainSurveyId].annual_incomes = annualIncomes;
                    })
                }
            })
        },
    },
    Validation: {
        CropMarketingExist: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="1"]')
                              .filter(':checked').length > 0;
                var exists = CropMarketingHelper.CropMarketing.Container.find('tr').length > 0;
                var con = checked && !exists;
                var msg = $('<p data-guid="{0}">有勾選『農作物及其製品』之銷售額區間，【問項1.4】應有生產農產品</p>'.format(this.Guid));
                Helper.LogHandler(con, AnnualIncomeHelper.Alert, msg);
            },
        },
        LivestockMarketingExist: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="2"]')
                              .filter(':checked').length > 0;
                var exists = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').length > 0;
                var con = checked && !exists;
                var msg = $('<p data-guid="{0}">有勾選『畜禽作物及其製品』之銷售額區間，【問項1.5】應有生產畜產品</p>'.format(this.Guid));
                Helper.LogHandler(con, AnnualIncomeHelper.Alert, msg);
            },
        },
        IncomeTotal: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var totalMin = 0;
                var totalMax = 0;
                AnnualIncomeHelper.AnnualIncome.Container
                .filter(':checked')
                .each(function(){
                    var marketTypeId = $(this).data('markettype-id');
                    if(marketTypeId == "5") return; // exclude total input
                    var min = parseInt($(this).data('min'));
                    var max = parseInt($(this).data('max'));
                    totalMin += min;
                    totalMax += max;
                })

                // get total input
                $input = AnnualIncomeHelper.AnnualIncome.Container
                       .filter(':checked')
                       .filter('[data-markettype-id="5"]')
                checkedMin = parseInt($input.data('min'));
                checkedMax = parseInt($input.data('max'));

                var con = checkedMax <= totalMin || checkedMin > totalMax;
                var msg = $('<p data-guid="{0}">銷售額總計之區間，應與各類別區間加總相對應</p>'.format(this.Guid));
                Helper.LogHandler(con, AnnualIncomeHelper.Alert, msg);
            },
        },
    },
}
var PopulationAgeHelper = {
    Alert: null,
    Set: function(array) {
        this.PopulationAge.Set(array);
    },
    Reset: function() {
        this.PopulationAge.Reset();
    },
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert[name="populationage"]'));
        this.PopulationAge.Bind();
    },
    PopulationAge: {
        Object: {
            Filter: function(age_scope, gender){
                var objects = CloneData[MainSurveyId].population_ages.filter(function(obj){
                    return obj.age_scope == age_scope && obj.gender == gender
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel3 input[name="populationage"]'),
        Set: function(array){
            array.forEach(function(population_age, i){
                PopulationAgeHelper.PopulationAge.Container
                .filter('[data-gender-id="{0}"]'.format(population_age.gender))
                .filter('[data-agescope-id="{0}"]'.format(population_age.age_scope))
                .val(population_age.count).trigger("change");
            })
        },
        Reset: function(){
            this.Container.val('');
            $('#panel3 input[name="sumcount"]').val('');
        },
        Bind: function(){
            Helper.BindInterOnly(this.Container);
            this.Container.change(function(){
                /* display sum */
                var sumCount = 0;
                $(this).closest('tr').find('input[name="populationage"]').map(function(){
                    parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);

                if(CloneData){
                    var ageScopeId = $(this).data('agescope-id');
                    var genderId = $(this).data('gender-id');
                    var obj = PopulationAgeHelper.PopulationAge.Object.Filter(ageScopeId, genderId);
                    if(obj){
                        obj.count = parseInt($(this).val());
                    }

                    if(Validate){
                        PopulationAgeHelper.Validation.MemberCount.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        MemberCount: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var over15Count = 0;
                PopulationAgeHelper.PopulationAge.Container
                .filter('[data-age-scope="5"]')
                .each(function(){
                    var count = parseInt($(this).val());
                    if(count) over15Count += count;
                })
                var con = over15Count != PopulationHelper.Population.Container.find('tr').length;
                var msg = $('<p data-guid="{0}">滿15歲以上男、女性人數，應等於【問項2.2】總人數</p>'.format(this.Guid));
                Helper.LogHandler(con, PopulationAgeHelper.Alert, msg);
            },
        },

    },
}
var PopulationHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="population"]'));
        var $row = $(row);
        this.Population.Bind($row);
        this.Adder.Bind();
        this.Population.$Row = $row;

    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.Population.Reset();
    },
    Set: function(array, surveyId){
        this.Population.Set(array, surveyId);
        if(Validate){
            PopulationHelper.Population.Container.find('tr').each(function(){
                PopulationHelper.Validation.RequiredField.Validate($(this));
                PopulationHelper.Validation.BirthYear.Validate($(this));
                PopulationHelper.Validation.LifeStyleWorkDayLimit.Validate($(this));
            })
            PopulationHelper.Validation.AtLeastOne65Worker.Validate();
        }
    },
    Population: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].populations.filter(function(obj){
                    return obj.guid == guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel3 table[name="population"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(population, i){
                var $row = PopulationHelper.Population.$Row.clone(true, true);
                $row.find('select[name="relationship"]').selectpicker('val', population.relationship);
                $row.find('select[name="gender"]').selectpicker('val', population.gender);
                $row.find('input[name="birthyear"]').val(population.birth_year);
                $row.find('select[name="educationlevel"]').selectpicker('val', population.education_level);
                $row.find('select[name="farmerworkday"]').selectpicker('val', population.farmer_work_day);
                $row.find('select[name="lifestyle"]').selectpicker('val', population.life_style);
                $row.find('select[name="otherfarmwork"]').selectpicker('val', population.other_farm_work);
                $row.attr('data-survey-id', surveyId);

                population.guid = Helper.CreateGuid();
                $row.attr('data-guid', population.guid);

                PopulationHelper.Population.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId =$tr.data('survey-id');
                        CloneData[surveyId].populations = CloneData[surveyId].populations.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        if(Validate){
                            var guid = $tr.data('guid');
                            PopulationHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            PopulationHelper.Alert.alert();
                            PopulationAgeHelper.Validation.MemberCount.Validate();
                            PopulationHelper.Validation.AtLeastOne65Worker.Validate();
                        }
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = PopulationHelper.Population.Object.Filter(surveyId, guid);
                    obj.relationship = parseInt($tr.find('[name="relationship"]').val());
                    obj.gender = parseInt($tr.find('[name="gender"]').val());
                    obj.birth_year = parseInt($tr.find('[name="birthyear"]').val());
                    obj.education_level = parseInt($tr.find('[name="educationlevel"]').val());
                    obj.farmer_work_day = parseInt($tr.find('[name="farmerworkday"]').val());
                    obj.life_style = parseInt($tr.find('[name="lifestyle"]').val());
                    obj.other_farm_work = parseInt($tr.find('[name="otherfarmwork"]').val());


                    if(Validate){
                        PopulationHelper.Validation.RequiredField.Validate($tr);
                        PopulationHelper.Validation.BirthYear.Validate($tr);
                        PopulationHelper.Validation.LifeStyleWorkDayLimit.Validate($tr);
                        PopulationHelper.Validation.AtLeastOne65Worker.Validate();
                    }
                }
            })

            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="population"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = PopulationHelper.Population.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].populations.push(obj);

                    $row = PopulationHelper.Population.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    PopulationHelper.Population.Container.append($row);
                    if(Validate){
                        PopulationHelper.Validation.RequiredField.Validate($row);
                        PopulationAgeHelper.Validation.MemberCount.Validate();
                        PopulationHelper.Validation.AtLeastOne65Worker.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="relationship"]').val(), PopulationHelper.Alert, makeString('與戶長關係'));
                Helper.LogHandler(!$row.find('[name="gender"]').val(), PopulationHelper.Alert, makeString('性別'));
                Helper.LogHandler(!$row.find('[name="birthyear"]').val(), PopulationHelper.Alert, makeString('出生年次'));
                Helper.LogHandler(!$row.find('[name="educationlevel"]').val(), PopulationHelper.Alert, makeString('教育程度'));
                Helper.LogHandler(!$row.find('[name="farmerworkday"]').val(), PopulationHelper.Alert, makeString('全年自家農牧業工作日數'));
                Helper.LogHandler(!$row.find('[name="lifestyle"]').val(), PopulationHelper.Alert, makeString('全年主要生活型態'));
                Helper.LogHandler(!$row.find('[name="otherfarmwork"]').val(), PopulationHelper.Alert, makeString('是否有從事農牧業外工作'));
            },
        },
        BirthYear: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                var year = $row.find('[name="birthyear"]').val()
                if(year == '') return;
                var con = parseInt(year) < 1 || parseInt(year) > 91 || !Helper.NumberValidate(year);
                var msg = $('<p data-guid="{0}">第{1}列出生年次應介於1年至91年之間（實足年齡滿15歲）</p>'.format(guid, index))
                Helper.LogHandler(con, PopulationHelper.Alert, msg);
            },
        },
        LifeStyleWorkDayLimit: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                var farmerWorkdayId = $row.find('[name="farmerworkday"]').val();
                var lifeStyleId = $row.find('[name="lifestyle"]').val();
                var con = farmerWorkdayId == 1 &&  lifeStyleId == 1;
                var msg = $('<p data-guid="{0}">第{1}列全年從事工作勾選無，主要生活型態不得勾選自營農牧業工作</p>'.format(guid, index));
                Helper.LogHandler(con, PopulationHelper.Alert, msg);
            }
        },
        AtLeastOne65Worker: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var con = true;
                PopulationHelper.Population.Container.find('tr').each(function(){
                    var birthYear = $(this).find('[name="birthyear"]').val();
                    var farmerWorkdayId = $(this).find('[name="farmerworkday"]').val();
                    if(birthYear <= 91 && birthYear >=42 && Helper.NumberValidate(birthYear) && farmerWorkdayId > 1){
                        con = false;
                    }
                })
                var msg = $('<p data-guid="{0}">各戶至少應有1位65歲以下(出生年次42年至91年)全年從事自家農牧業工作日數達1日以上</p>'.format(this.Guid));
                Helper.LogHandler(con, PopulationHelper.Alert, msg);
            },
        },
    },
}
var LongTermHireHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="longtermhire"]'));
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermHire.Bind($row);
        this.Adder.Bind();
        this.LongTermHire.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LongTermHire.Reset();
    },
    Set: function(array, surveyId){
        this.LongTermHire.Set(array, surveyId);
        if(Validate){
            LongTermHireHelper.LongTermHire.Container.find('tr').each(function(){
                LongTermHireHelper.Validation.RequiredField.Validate($(this));
                LongTermHireHelper.Validation.AvgWorkDay.Validate($(this));
            })
        }
    },
    LongTermHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].long_term_hires.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="longtermhire"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(long_term_hire, i){
                var $row = LongTermHireHelper.LongTermHire.$Row.clone(true, true);

                $row.find('select[name="worktype"]').selectpicker('val', long_term_hire.work_type);
                long_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .attr('data-numberworker-id', number_worker.id)
                    .val(number_worker.count).trigger('change');
                });
                $row.find('select[name="month"]').selectpicker('val', long_term_hire.months);
                $row.find('input[name="avgworkday"]').val(long_term_hire.avg_work_day);

                $row.attr('data-survey-id', surveyId);

                long_term_hire.guid = Helper.CreateGuid();
                $row.attr('data-guid', long_term_hire.guid);

                LongTermHireHelper.LongTermHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){

            Helper.BindInterOnly($row.find('input'));
            $row.find('input[name="numberworker"]').change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="numberworker"]').map(function(){
                    var parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);
            })
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_hires = CloneData[surveyId].long_term_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        
                        if(Validate){
                            var guid = $tr.data('guid');
                            LongTermHireHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            LongTermHireHelper.Alert.alert();
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                        }
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = LongTermHireHelper.LongTermHire.Object.Filter(surveyId, guid);

                    obj.work_type = parseInt($tr.find('[name="worktype"]').val());
                    obj.number_workers = SurveyHelper.NumberWorker.Object.Collect($tr.find('[name="numberworker"]'));
                    obj.months = $tr.find('[name="month"]').val();
                    obj.avg_work_day = parseInt($tr.find('[name="avgworkday"]').val());

                    if(Validate){
                        LongTermHireHelper.Validation.RequiredField.Validate($tr);
                        LongTermHireHelper.Validation.AvgWorkDay.Validate($tr);
                    }
                }
            })

            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="longtermhire"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = LongTermHireHelper.LongTermHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].long_term_hires.push(obj);

                    $row = LongTermHireHelper.LongTermHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LongTermHireHelper.LongTermHire.Container.append($row);

                    if(Validate){
                        LongTermHireHelper.Validation.RequiredField.Validate($row);
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermHireHelper.LongTermHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="worktype"]').val(), LongTermHireHelper.Alert, makeString('主要僱用工作類型'));
                Helper.LogHandler(!$row.find('[name="sumcount"]').val(), LongTermHireHelper.Alert, makeString('人數'));
                Helper.LogHandler($row.find('[name="month"]').val().length == 0, LongTermHireHelper.Alert, makeString('僱用月份'));
                Helper.LogHandler(!$row.find('[name="avgworkday"]').val(), LongTermHireHelper.Alert, makeString('平均每月工作日數'));
            },
        },
        AvgWorkDay: {
            Guid: Helper.CreateGuid(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermHireHelper.LongTermHire.Container.find('tr').index($row) + 1;
                var avgWorkDay = $row.find('[name="avgworkday"]').val();
                var con = avgWorkDay > 30 && Helper.NumberValidate(avgWorkDay);
                var msg = $('<p data-guid="{0}">第{1}列每月工作日數應小於30日</p>'.format(guid, index));
                Helper.LogHandler(con, LongTermHireHelper.Alert, msg);
            },
        },
    },
}
var ShortTermHireHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="shorttermhire"]'));
        var $row = $(row);
        $row.find('select[name="worktype"]').attr('multiple', '');
        this.ShortTermHire.Bind($row);
        this.Adder.Bind();
        this.ShortTermHire.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.ShortTermHire.Reset();
    },
    Set: function(array){
        this.ShortTermHire.Set(array);
        if(Validate){
            ShortTermHireHelper.ShortTermHire.Container.find('tr').each(function(){
                ShortTermHireHelper.Validation.RequiredField.Validate($(this));
                ShortTermHireHelper.Validation.AvgWorkDay.Validate($(this));
            })
        }
    },
    ShortTermHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(guid){
                var objects = CloneData[MainSurveyId].short_term_hires.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="shorttermhire"] > tbody'),
        Set: function (array) {
            array.forEach(function(short_term_hire, i){
                var $row = ShortTermHireHelper.ShortTermHire.$Row.clone(true, true);

                $row.find('select[name="month"]').selectpicker('val', short_term_hire.month);
                short_term_hire.number_workers.forEach(function(number_worker, j){
                    $row.find('input[name="numberworker"]')
                    .filter('[data-agescope-id="{0}"]'.format(number_worker.age_scope))
                    .attr('data-numberworker-id', number_worker.id)
                    .val(number_worker.count).trigger('change');
                })
                $row.find('select[name="worktype"]').selectpicker('val', short_term_hire.work_types);
                $row.find('input[name="avgworkday"]').val(short_term_hire.avg_work_day);

                short_term_hire.guid = Helper.CreateGuid();
                $row.attr('data-guid', short_term_hire.guid);

                ShortTermHireHelper.ShortTermHire.Container.append($row);
            })

        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('input[name="numberworker"]').change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="numberworker"]').map(function(){
                    var parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);
            })
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].short_term_hires = CloneData[MainSurveyId].short_term_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();

                        if(Validate){
                            var guid = $tr.data('guid');
                            ShortTermHireHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            ShortTermHireHelper.Alert.alert();
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                        }
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!guid){
                        return;
                    }
                    var obj = ShortTermHireHelper.ShortTermHire.Object.Filter(guid);

                    obj.work_type = $tr.find('[name="worktype"]').val();
                    obj.number_workers = SurveyHelper.NumberWorker.Object.Collect($tr.find('[name="numberworker"]'));
                    obj.month = parseInt($tr.find('[name="month"]').val());
                    obj.avg_work_day = parseInt($tr.find('[name="avgworkday"]').val());
                    
                    if(Validate){
                        ShortTermHireHelper.Validation.RequiredField.Validate($tr);
                        ShortTermHireHelper.Validation.AvgWorkDay.Validate($tr);
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="shorttermhire"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = ShortTermHireHelper.ShortTermHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].short_term_hires.push(obj);

                    $row = ShortTermHireHelper.ShortTermHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    ShortTermHireHelper.ShortTermHire.Container.append($row);
                    
                    if(Validate){
                        ShortTermHireHelper.Validation.RequiredField.Validate($row);
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermHireHelper.ShortTermHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="month"]').val(), ShortTermHireHelper.Alert, makeString('僱用月份'));
                Helper.LogHandler(!$row.find('[name="sumcount"]').val(), ShortTermHireHelper.Alert, makeString('人數'));
                Helper.LogHandler($row.find('[name="worktype"]').val().length == 0, ShortTermHireHelper.Alert, makeString('主要僱用工作類型'));
                Helper.LogHandler(!$row.find('[name="avgworkday"]').val(), ShortTermHireHelper.Alert, makeString('平均每月工作日數'));
            },
        },
        AvgWorkDay: {
            Guid: Helper.CreateGuid(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermHireHelper.ShortTermHire.Container.find('tr').index($row) + 1;
                var avgWorkDay = $row.find('[name="avgworkday"]').val();
                var con = avgWorkDay > 30 && Helper.NumberValidate(avgWorkDay);
                var msg = $('<p data-guid="{0}">第{1}列每月工作日數應小於30日</p>'.format(guid, index));
                Helper.LogHandler(con, ShortTermHireHelper.Alert, msg);
            },
        },
    },
}
var NoSalaryHireHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="nosalaryhire"]'));
        var $row = $(row);
        $row.find('select[name="month"]');
        this.NoSalaryHire.Bind($row);
        this.Adder.Bind();
        this.NoSalaryHire.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.NoSalaryHire.Reset();
    },
    Set: function(array){
        this.NoSalaryHire.Set(array);
        if(Validate){
            NoSalaryHireHelper.NoSalaryHire.Container.find('tr').each(function(){
                NoSalaryHireHelper.Validation.RequiredField.Validate($(this));
            })
        }
    },
    NoSalaryHire: {
        Object: {
            New: function(guid){
                guid = guid || null;
                return {
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(guid){
                var objects = CloneData[MainSurveyId].no_salary_hires.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="nosalaryhire"] > tbody'),
        Set: function (array) {
            array.forEach(function(no_salary_hire, i){
                var $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone(true, true);
                $row.find('select[name="month"]').selectpicker('val', no_salary_hire.month);
                $row.find('input[name="count"]').val(no_salary_hire.count);

                no_salary_hire.guid = Helper.CreateGuid();
                $row.attr('data-guid', no_salary_hire.guid);

                NoSalaryHireHelper.NoSalaryHire.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].no_salary_hires = CloneData[MainSurveyId].no_salary_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();

                        if(Validate){
                            var guid = $tr.data('guid');
                            NoSalaryHireHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            NoSalaryHireHelper.Alert.alert();
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                        }
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!guid){
                        return;
                    }
                    var obj = NoSalaryHireHelper.NoSalaryHire.Object.Filter(guid);

                    obj.month = parseInt($tr.find('[name="month"]').val());
                    obj.count = parseInt($tr.find('[name="count"]').val());

                    if(Validate){
                        NoSalaryHireHelper.Validation.RequiredField.Validate($tr);
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="nosalaryhire"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = NoSalaryHireHelper.NoSalaryHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].no_salary_hires.push(obj);

                    $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    NoSalaryHireHelper.NoSalaryHire.Container.append($row);

                    if(Validate){
                        NoSalaryHireHelper.Validation.RequiredField.Validate($row);
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = NoSalaryHireHelper.NoSalaryHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="month"]').val(), NoSalaryHireHelper.Alert, makeString('月份'));
                Helper.LogHandler(!$row.find('[name="count"]').val(), NoSalaryHireHelper.Alert, makeString('人數'));
            },
        },
    },
}
var LongTermLackHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="longtermlack"]'));
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermLack.Bind($row);
        this.Adder.Bind();
        this.LongTermLack.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LongTermLack.Reset();
    },
    Set: function(array, surveyId){
        this.LongTermLack.Set(array, surveyId);
        if(Validate){
            LongTermLackHelper.LongTermLack.Container.find('tr').each(function(){
                LongTermLackHelper.Validation.RequiredField.Validate($(this));
            })
        }
    },
    LongTermLack: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].long_term_lacks.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="longtermlack"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(long_term_lack, i){
                var $row = LongTermLackHelper.LongTermLack.$Row.clone(true, true);

                $row.find('select[name="worktype"]').selectpicker('val', long_term_lack.work_type);
                $row.find('input[name="count"]').val(long_term_lack.count);
                $row.find('select[name="month"]').selectpicker('val', long_term_lack.months);
                $row.attr('data-survey-id', surveyId);
                
                long_term_lack.guid = Helper.CreateGuid();
                $row.attr('data-guid', long_term_lack.guid);

                LongTermLackHelper.LongTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_lacks = CloneData[surveyId].long_term_lacks.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();

                        if(Validate){
                            var guid = $tr.data('guid');
                            LongTermLackHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            LongTermLackHelper.Alert.alert();
                            SurveyHelper.Lack.Validation.LackExist.Validate();
                        }
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = LongTermLackHelper.LongTermLack.Object.Filter(surveyId, guid);

                    obj.work_type = parseInt($tr.find('[name="worktype"]').val());
                    obj.months = $tr.find('[name="month"]').val();
                    obj.count = parseInt($tr.find('[name="count"]').val());

                    if(Validate){
                        LongTermLackHelper.Validation.RequiredField.Validate($tr);
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="longtermlack"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = LongTermLackHelper.LongTermLack.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].long_term_lacks.push(obj);

                    $row = LongTermLackHelper.LongTermLack.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LongTermLackHelper.LongTermLack.Container.append($row);

                    if(Validate){
                        LongTermLackHelper.Validation.RequiredField.Validate($row);
                        SurveyHelper.Lack.Validation.LackExist.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermLackHelper.LongTermLack.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="worktype"]').val(), LongTermLackHelper.Alert, makeString('主要短缺工作類型'));
                Helper.LogHandler(!$row.find('[name="count"]').val(), LongTermLackHelper.Alert, makeString('人數'));
                Helper.LogHandler($row.find('[name="month"]').val().length == 0, LongTermLackHelper.Alert, makeString('缺工月份'));
            },
        },
    },
}
var ShortTermLackHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert[name="shorttermlack"]'));
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.ShortTermLack.Bind($row);
        this.Adder.Bind();
        this.ShortTermLack.$Row = $row;
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.ShortTermLack.Reset();
    },
    Set: function(array, surveyId){
        this.ShortTermLack.Set(array, surveyId);
        if(Validate){
            ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                ShortTermLackHelper.Validation.RequiredField.Validate($(this));
            })
        }
    },
    ShortTermLack: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.CreateGuid(),
                }
            },
            Filter: function(surveyId, guid){
                var objects = CloneData[surveyId].short_term_lacks.filter(function(obj){
                    return obj.guid === guid;
                })
                if(objects.length > 0) return objects[0]
                else return null
            },
        },
        Container: $('#panel4 table[name="shorttermlack"] > tbody'),
        Set: function (array, surveyId) {
            array.forEach(function(short_term_lack, i){
                var $row = ShortTermLackHelper.ShortTermLack.$Row.clone(true, true);

                $row.find('select[name="product"]').selectpicker('val', short_term_lack.product);
                $row.find('select[name="worktype"]').selectpicker('val', short_term_lack.work_type);
                $row.find('input[name="count"]').val(short_term_lack.count);
                $row.find('select[name="month"]').selectpicker('val', short_term_lack.months);

                $row.attr('data-survey-id', surveyId);

                short_term_lack.guid = Helper.CreateGuid();
                $row.attr('data-guid', short_term_lack.guid);

                ShortTermLackHelper.ShortTermLack.Container.append($row);
            })
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindInterOnly($row.find('input'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].short_term_lacks = CloneData[surveyId].short_term_lacks.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        
                        if(Validate){
                            var guid = $tr.data('guid');
                            ShortTermLackHelper.Alert.message.find('[data-guid="{0}"]'.format(guid)).remove();
                            ShortTermLackHelper.Alert.alert();
                            SurveyHelper.Lack.Validation.LackExist.Validate();
                        }
                    })
                }
            })
            $row.find('select, input').change(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    var surveyId = $tr.data('survey-id');
                    var guid = $tr.data('guid');
                    /* trigger change before set attribute to dom should return */
                    if(!surveyId || !guid){
                        return;
                    }
                    var obj = ShortTermLackHelper.ShortTermLack.Object.Filter(surveyId, guid);

                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.work_type = $tr.find('[name="worktype"]').val();
                    obj.months = $tr.find('[name="month"]').val();
                    obj.count = parseInt($tr.find('[name="count"]').val());
                    
                    if(Validate){
                         ShortTermLackHelper.Validation.RequiredField.Validate($tr);                   
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="shorttermlack"]'),
        Bind: function(){
            this.Container.click(function(){
                if(CloneData && MainSurveyId){
                    obj = ShortTermLackHelper.ShortTermLack.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].short_term_lacks.push(obj);

                    $row = ShortTermLackHelper.ShortTermLack.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    ShortTermLackHelper.ShortTermLack.Container.append($row);
                    
                    if(Validate){
                        ShortTermLackHelper.Validation.RequiredField.Validate($row);
                    }
                }
            })
        },
    },
    Validation: {
        RequiredField: {
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermLackHelper.ShortTermLack.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return $('<p data-guid="{0}">第{1}列{2}不可空白</p>'.format(guid, index, name))
                }
                Helper.LogHandler(!$row.find('[name="product"]').val(), ShortTermLackHelper.Alert, makeString('農畜產品名稱'));
                Helper.LogHandler(!$row.find('[name="worktype"]').val(), ShortTermLackHelper.Alert, makeString('主要短缺工作類型'));
                Helper.LogHandler(!$row.find('[name="count"]').val(), ShortTermLackHelper.Alert, makeString('人數'));
                Helper.LogHandler($row.find('[name="month"]').val().length == 0, ShortTermLackHelper.Alert, makeString('缺工月份'));
            },
        },
    },
}
var SubsidyHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert[name="subsidy"]'));
        this.Bind();
    },
    Container: {
        HasSubsidy: $('#panel4 input[name="hassubsidy"]'),
        NoneSubsidy: $('#panel4 input[name="nonesubsidy"]'),
        Count: $('#panel4 input[name="count"]'),
        Month: $('#panel4 input[name="monthdelta"]'),
        Day: $('#panel4 input[name="daydelta"]'),
        Hour: $('#panel4 input[name="hourdelta"]'),
        RefuseReason: $('#panel4 input[name="refusereason"]'),
        Extra: $('#panel4 input[name="extra"]'),
    },
    Set: function(obj){
        this.Container.HasSubsidy.prop('checked', obj.has_subsidy);
        this.Container.NoneSubsidy.prop('checked', obj.none_subsidy);
        this.Container.Count.val(obj.count);
        this.Container.Month.val(obj.month_delta);
        this.Container.Day.val(obj.day_delta);
        this.Container.Hour.val(obj.hour_delta);
        obj.refuses.forEach(function(refuse, i){
            SubsidyHelper.Container.RefuseReason
            .filter('[ data-refusereason-id="{0}"]'.format(refuse.reason))
            .attr('data-refuse-id', refuse.id)
            .prop('checked', true);

            SubsidyHelper.Container.Extra
            .filter('[ data-refusereason-id="{0}"]'.format(refuse.reason))
            .attr('data-refuse-id', refuse.id)
            .val(refuse.extra);
        })
        if(Validate){
            SubsidyHelper.Validation.Empty.Validate();
        }
    },
    Reset: function(){
        this.Container.HasSubsidy.prop('checked', false);
        this.Container.NoneSubsidy.prop('checked', false);
        this.Container.Count.val('');
        this.Container.Month.val('');
        this.Container.Day.val('');
        this.Container.Hour.val('');
        this.Container.RefuseReason.prop('checked', false);
        this.Container.Extra.val('');
    },
    Bind: function(){
        Helper.BindInterOnly(this.Container.Count);
        Helper.BindInterOnly(this.Container.Month);
        Helper.BindInterOnly(this.Container.Day);
        Helper.BindInterOnly(this.Container.Hour);
        this.Container.HasSubsidy.change(function(){
            if(CloneData){
                var checked = $(this).prop('checked');
                CloneData[MainSurveyId].subsidy.has_subsidy = checked;
                if(!checked){
                    SubsidyHelper.Container.Count.val('').trigger('change');
                    SubsidyHelper.Container.Month.val('').trigger('change');
                    SubsidyHelper.Container.Day.val('').trigger('change');
                    SubsidyHelper.Container.Hour.val('').trigger('change');
                }
                if(Validate){
                    SubsidyHelper.Validation.Empty.Validate();
                }
            }
        })
        this.Container.NoneSubsidy.change(function(){
            if(CloneData){
                var checked = $(this).prop('checked');
                CloneData[MainSurveyId].subsidy.none_subsidy = checked;
                if(!checked){
                    SubsidyHelper.Container.RefuseReason.prop('checked', false).trigger('change');
                    SubsidyHelper.Container.Extra.val('').trigger('change');
                }
                if(Validate){
                    SubsidyHelper.Validation.Empty.Validate();
                }
            }
        })
        this.Container.Count.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.count = parseInt($(this).val());
            }
        })
        this.Container.Month.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.month_delta = parseInt($(this).val());
            }
        })
        this.Container.Day.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.day_delta = parseInt($(this).val());
            }
        })
        this.Container.Hour.change(function(){
            if(CloneData){
                CloneData[MainSurveyId].subsidy.hour_delta = parseInt($(this).val());
            }
        })
        this.Container.RefuseReason.change(function(){
            SubsidyHelper.Object.Refuse.Collect();
        })
        this.Container.Extra.change(function(e){
            /* make sure checked before change textbox value */
            var refuseReasonId = $(this).data('refusereason-id');
            var noneSubsidyChecked = SubsidyHelper.Container.NoneSubsidy.prop('checked');
            var reasonChecked = SubsidyHelper.Container.RefuseReason
                          .filter('[data-refusereason-id="{0}"]'.format(refuseReasonId))
                          .prop('checked');
            if(noneSubsidyChecked && !reasonChecked){
                Helper.Dialog.ShowAlert('請先勾選無申請之原因');
                e.preventDefault();
            }
            SubsidyHelper.Object.Refuse.Collect();
        })
    },
    Object: {
        Refuse: {
            New: function(refuseReasonId, extra, id){
                var obj = {
                    reason: refuseReasonId,
                    extra: extra,
                }
                if(id) obj.id = id;
                return obj;
            },
            Collect: function(){
                if(CloneData){
                    var refuses = [];
                    SubsidyHelper.Container.RefuseReason
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('refuse-id');
                        var refuseReasonId = $(this).data('refusereason-id');
                        var extra = SubsidyHelper.Container.Extra
                                    .filter('[data-refusereason-id="{0}"]'.format(refuseReasonId))
                                    .val();
                        refuses.push(
                            SubsidyHelper.Object.Refuse.New(refuseReasonId, extra, id ? id : null)
                        )
                    })
                    CloneData[MainSurveyId].subsidy.refuses = refuses;
                }
            },
        }
    },
    Validation: {
        Empty: {
            Guid: Helper.CreateGuid(),
            Validate: function(){
                var hasSubsidy = SubsidyHelper.Container.HasSubsidy.prop('checked');
                var noneSubsidy = SubsidyHelper.Container.NoneSubsidy.prop('checked');
                var con = !hasSubsidy && !noneSubsidy;
                var msg = $('<p data-guid="{0}">不可漏填此問項</p>'.format(this.Guid));
                Helper.LogHandler(con, SubsidyHelper.Alert, msg);
            },
        },
    },
}



