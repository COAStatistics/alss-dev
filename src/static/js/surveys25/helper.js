/* rendered ui */
var GlobalUI = $.parseJSON($('#ui').val());
var FarmerIds = $.parseJSON($('#fid').val());

/* data */
var CloneData = null;
var MainSurveyId = 0;

$(document).ready(function () {
    /* jQuery Spinner */
    var Loading = $.loading();
    /* setup*/
    Setup(GlobalUI);

    /* autocomplete */
    $("#farmerId").typeahead({
        source: FarmerIds,
        autoSelect: true,
        fitToElement: true,
    })
})

var Reset = function () {
    $('#survey-wrapper').off();
    SurveyHelper.Reset();
    FarmLocationHelper.Reset();
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
    HireChannelHelper.Reset();
    LackResponseHelper.Reset();
    MaxHourlyPayHelper.Reset();
}
var Set = function (data, surveyId) {
    if (data.page == 1) {
        MainSurveyId = surveyId;
        SurveyHelper.Set(data);
        if(data.farm_location) FarmLocationHelper.Set(data.farm_location)
        if(data.land_areas) LandAreaHelper.Set(data.land_areas);
        if(data.businesses) BusinessHelper.Set(data.businesses);
        if(data.management_types) ManagementTypeHelper.Set(data.management_types);
        if(data.annual_incomes) AnnualIncomeHelper.Set(data.annual_incomes);
        if(data.population_ages) PopulationAgeHelper.Set(data.population_ages);
        if(data.short_term_hires) ShortTermHireHelper.Set(data.short_term_hires);
        if(data.no_salary_hires) NoSalaryHireHelper.Set(data.no_salary_hires);
        if(data.subsidy) SubsidyHelper.Set(data.subsidy);
        if(data.hire_channels) HireChannelHelper.Set(data.hire_channels);
        if(data.lack_responses) LackResponseHelper.Set(data.lack_responses);
        if(data.max_hourly_pays) MaxHourlyPayHelper.Set(data.max_hourly_pays);
    }
    /* need setting survey surveyId to locate which obj */
    if(data.crop_marketings) CropMarketingHelper.Set(data.crop_marketings, surveyId);
    if(data.livestock_marketings) LivestockMarketingHelper.Set(data.livestock_marketings, surveyId);
    if(data.populations) PopulationHelper.Set(data.populations, surveyId);
    if(data.long_term_hires) LongTermHireHelper.Set(data.long_term_hires, surveyId);
    if(data.long_term_lacks) LongTermLackHelper.Set(data.long_term_lacks, surveyId);
    if(data.short_term_lacks) ShortTermLackHelper.Set(data.short_term_lacks, surveyId);

    if(Helper.LogHandler.ValidationActive){
        /* Validators that interact with other Helper objects */
        CropMarketingHelper.Validation.IncomeChecked.Validate();
        CropMarketingHelper.Validation.WorkHourRange.Validate();
        LivestockMarketingHelper.Validation.IncomeChecked.Validate();
        BusinessHelper.Validation.MarketType4Checked.Validate();
        AnnualIncomeHelper.Validation.CropMarketingExist.Validate();
        AnnualIncomeHelper.Validation.LivestockMarketingExist.Validate();
        AnnualIncomeHelper.Validation.AnnualTotal.Validate();
        PopulationAgeHelper.Validation.MemberCount.Validate();
        PopulationHelper.Validation.MarketType3Checked.Validate();
        SurveyHelper.Hire.Validation.HireExist.Validate();
        SurveyHelper.Lack.Validation.LackExist.Validate();
    }
}

var Setup = function(globalUI){

    Helper.LogHandler.Setup();

    SurveyHelper.Setup();
    FarmLocationHelper.Setup();
    LandAreaHelper.Setup();
    BusinessHelper.Setup();
    ManagementTypeHelper.Setup();
    AnnualIncomeHelper.Setup();
    PopulationAgeHelper.Setup();
    SubsidyHelper.Setup();
    HireChannelHelper.Setup();
    LackResponseHelper.Setup();
    MaxHourlyPayHelper.Setup();

    CropMarketingHelper.Setup(globalUI.cropmarketing);
    LivestockMarketingHelper.Setup(globalUI.livestockmarketing);
    PopulationHelper.Setup(globalUI.population);
    LongTermHireHelper.Setup(globalUI.longtermhire);
    LongTermLackHelper.Setup(globalUI.longtermlack);
    ShortTermHireHelper.Setup(globalUI.shorttermhire);
    ShortTermLackHelper.Setup(globalUI.shorttermlack);
    NoSalaryHireHelper.Setup(globalUI.nosalaryhire);
}

var SurveyHelper = {
    Alert: null,
    Setup: function() {
        this.Alert = new Helper.Alert($('.alert-danger[name="survey"]'));
        this.Hire.Setup();
        this.Lack.Setup();
        this.FarmOutsource.Setup();
        this.MainIncomeSource.Setup();

        this.FarmerName.Bind();
        this.IntervieweeRelationship.Bind();
        this.Phone.Bind();
        this.AddressMatch.Bind();
        this.Address.Bind();
        this.Hire.Bind();
        this.Lack.Bind();
        this.FarmOutsource.Bind();
        this.Note.Bind();
        this.IsInvalid.Bind();
        this.InvalidReason.Bind();
        this.MainIncomeSource.Bind();
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.Investigator.Reset();
        this.Reviewer.Reset();
        this.FarmerId.Reset();
        this.FarmerName.Reset();
        this.IntervieweeRelationship.Reset();
        this.Phone.Reset();
        this.AddressMatch.Reset();
        this.Address.Reset();
        this.Hire.Reset();
        this.Lack.Reset();
        this.FarmOutsource.Reset();
        this.Note.Reset();
        this.IsInvalid.Reset();
        this.InvalidReason.Reset();
        this.MainIncomeSource.Reset();
    },
    Set: function (obj) {
        this.Investigator.Set(obj);
        this.Reviewer.Set(obj);
        this.FarmerId.Set(obj);
        this.Phone.Set(obj);
        this.FarmerName.Set(obj);
        this.IntervieweeRelationship.Set(obj);
        this.AddressMatch.Set(obj);
        this.Address.Set(obj);
        this.Hire.Set(obj);
        this.Lack.Set(obj);
        this.FarmOutsource.Set(obj);
        this.Note.Set(obj);
        this.IsInvalid.Set(obj);
        this.InvalidReason.Set(obj);
        this.MainIncomeSource.Set(obj);
    },
    Investigator: {
        Container: $('#panel1 input[name="investigator"]'),
        Set: function(obj) {
            this.Container.val(obj.investigator);
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    Reviewer: {
        Container: $('#panel1 input[name="reviewer"]'),
        Set: function(obj) {
            this.Container.val(obj.reviewer);
        },
        Reset: function(){
            this.Container.val('');
        },
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
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData) {
                    CloneData[MainSurveyId].farmer_name = $(this).val();

                    if(Helper.LogHandler.ValidationActive){
                        SurveyHelper.FarmerName.Validation.Empty.Validate();
                    }
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.farmer_name);
            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.FarmerName.Validation.Empty.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var empty = CloneData[MainSurveyId].farmer_name == '';
                    var msg = '受訪人不可漏填';
                    Helper.LogHandler.Log(empty, SurveyHelper.Alert, msg, this.Guids[0], null, false);
                },
            },
        },
    },
    IntervieweeRelationship: {
        Container: $('#panel1 input[name="intervieweerelationship"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData) {
                    CloneData[MainSurveyId].interviewee_relationship = $(this).val();

                    if(Helper.LogHandler.ValidationActive){
                        SurveyHelper.IntervieweeRelationship.Validation.Empty.Validate();
                    }
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.interviewee_relationship);
            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.IntervieweeRelationship.Validation.Empty.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var empty = CloneData[MainSurveyId].interviewee_relationship == '';
                    var msg = '受訪者與名冊戶長關係不可漏填';
                    Helper.LogHandler.Log(empty, SurveyHelper.Alert, msg, this.Guids[0], null, false);
                },
            },
        },
    },
    Phone: {
        Object: {
            New: function(surveyId, phone){
                return {
                    survey: surveyId,
                    phone: phone ? phone : null,
                }
            },
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
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData) {
                    var id = $(this).data('phone-id');
                    var obj = SurveyHelper.Phone.Object.Filter(id);
                    if(!obj){
                        // cannot locate which obj should remove, so reset all 2 phones
                        CloneData[MainSurveyId].phones = [];
                        SurveyHelper.Phone.Container.each(function(){
                            var new_obj = SurveyHelper.Phone.Object.New(MainSurveyId);
                            new_obj.phone = $(this).val();
                            CloneData[MainSurveyId].phones.push(new_obj);
                        })
                    }else {
                        obj.phone = $(this).val();
                    }
                    if(Helper.LogHandler.ValidationActive){
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
            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.Phone.Validation.Empty.Validate();
            }
        },
        Reset: function(){
            SurveyHelper.Phone.Container.val('');
            SurveyHelper.Phone.Container.attr('data-phone-id', '');
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var empty = true;
                    CloneData[MainSurveyId].phones.forEach(function(obj, i){
                        if(obj.phone){
                            empty = false;
                        }
                    });
                    var msg = '聯絡電話不可漏填';
                    Helper.LogHandler.Log(empty, SurveyHelper.Alert, msg, this.Guids[0], null, false);
                },
            },
        },
    },
    Hire: {
        Success: null,
        Alert: null,
        Info: null,
        Setup: function(){
            this.Success = new Helper.Alert($('.alert-success[name="hire"]'));
            this.Info = new Helper.Alert($('.alert-info[name="hire"]'));
            this.Alert = new Helper.Alert($('.alert-danger[name="hire"]'));
        },
        Container: $('#panel4 input[name="hire"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData) {
                    var field = $(this).data('field');
                    if(field == 'hire')
                        CloneData[MainSurveyId].hire = this.checked;
                    else if(field == 'nonhire')
                        CloneData[MainSurveyId].non_hire = this.checked;

                    if(Helper.LogHandler.ValidationActive){
                        SurveyHelper.Hire.Validation.Empty.Validate();
                        SurveyHelper.Hire.Validation.HireExist.Validate();
                        SurveyHelper.Hire.Validation.Duplicate.Validate();
                        HireChannelHelper.Validation.ConflictToHire.Validate();
                    }
                }
            })
        },
        Set: function (obj) {
            this.Container.filter('[data-field="hire"]').prop('checked', obj.hire);
            this.Container.filter('[data-field="nonhire"]').prop('checked', obj.non_hire);

            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.Hire.Validation.Empty.Validate();
                SurveyHelper.Hire.Validation.Duplicate.Validate();
                HireChannelHelper.Validation.ConflictToHire.Validate();
            }
        },
        Reset: function(){
            if (this.Success) { this.Success.reset(); }
            if (this.Alert) { this.Alert.reset(); }
            if (this.Info) { this.Info.reset(); }
            this.Container.prop('checked', false);
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.Hire.Container.filter(':checked').length == 0;
                    var msg = '不可漏填此問項';
                    Helper.LogHandler.Log(con, SurveyHelper.Hire.Alert, msg, this.Guids[0], null, false);
                },
            },
            Duplicate: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.Hire.Container.filter(':checked').length > 1;
                    var msg = '有外僱及無外僱人力不得重複勾選';
                    Helper.LogHandler.Log(con, SurveyHelper.Hire.Alert, msg, this.Guids[0], null, false);
                },
            },
            HireExist: {
                Guids: Helper.Guid.CreateMulti(1),
                Validate: function(){
                    var checked = SurveyHelper.Hire.Container.filter('[data-field="nonhire"]').prop('checked');
                    var exists = LongTermHireHelper.LongTermHire.Container.find('tr').length +
                                 ShortTermHireHelper.ShortTermHire.Container.find('tr').length +
                                 NoSalaryHireHelper.NoSalaryHire.Container.find('tr').length > 0;
                    var con = checked && exists;
                    var msg = '勾選無外僱人力，【問項3.1.2及3.1.3及3.2】應為空白';
                    Helper.LogHandler.Log(con, SurveyHelper.Hire.Alert, msg, this.Guids[0]);

                    var con = !checked && !exists;
                    var msg = '若全年無外僱人力，應勾選無';
                    Helper.LogHandler.Log(con, SurveyHelper.Hire.Alert, msg, this.Guids[1]);
                },
            },
        },
    },
    Lack: {
        Alert: null,
        Setup: function(){
            this.Alert = new Helper.Alert($('.alert-danger[name="lack"]'));
        },
        Container: $('#panel4 input[name="lack"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
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

                    if(Helper.LogHandler.ValidationActive){
                        SurveyHelper.Lack.Validation.Empty.Validate();
                        SurveyHelper.Lack.Validation.Duplicate.Validate();
                        SurveyHelper.Lack.Validation.LackExist.Validate();
                        SubsidyHelper.Validation.HasLack.Validate();
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

            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.Lack.Validation.Empty.Validate();
                SurveyHelper.Lack.Validation.Duplicate.Validate();
                SubsidyHelper.Validation.HasLack.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.Lack.Container.filter(':checked').length == 0;
                    var msg = '不可漏填此問項';
                    Helper.LogHandler.Log(con, SurveyHelper.Lack.Alert, msg, this.Guids[0], null, false);
                },
            },
            Duplicate: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.Lack.Container.filter(':checked').length > 1;
                    var msg = '限註記一個項目';
                    Helper.LogHandler.Log(con, SurveyHelper.Lack.Alert, msg, this.Guids[0], null, false);
                },
            },
            LackExist: {
                Guids: Helper.Guid.CreateMulti(1),
                Validate: function(){
                    var checked = SurveyHelper.Lack.Container.filter('input:checked');
                    var text = checked.parent().text().trim();
                    var exists = LongTermLackHelper.LongTermLack.Container.find('tr').length +
                                 ShortTermLackHelper.ShortTermLack.Container.find('tr').length > 0;
                    var con = checked.length == 1 && [2, 3, 4].indexOf(checked.data('lackId')) != -1 && !exists;
                    msg = '若勾選「{0}」，【問項3.3.3及3.3.4】不應為空白'.format(text);
                    Helper.LogHandler.Log(con, SurveyHelper.Lack.Alert, msg, this.Guids[0]);

                    var con = checked.length == 1 && checked.data('lackId') == 1 && exists;
                    msg = '若勾選「{0}」，【問項3.3.3及3.3.4】應為空白'.format(text);
                    Helper.LogHandler.Log(con, SurveyHelper.Lack.Alert, msg, this.Guids[1]);
                },
            },
        },
    },
    FarmOutsource: {
        Alert: null,
        Setup: function(){
            this.Alert = new Helper.Alert($('.alert-danger[name="farmoutsource"]'));
            this.Info = new Helper.Alert($('.alert-info[name="farmoutsource"]'));
        },
        Container: $('#panel4 input[name="farmoutsource"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData) {
                    var field = $(this).data('field');
                    if(field == 'hasfarmoutsource')
                        CloneData[MainSurveyId].has_farm_outsource = this.checked;
                    else if(field == 'nonhasfarmoutsource')
                        CloneData[MainSurveyId].non_has_farm_outsource = this.checked;

                    if(Helper.LogHandler.ValidationActive){
                        SurveyHelper.FarmOutsource.Validation.Empty.Validate();
                        SurveyHelper.FarmOutsource.Validation.Duplicate.Validate();
                        HireChannelHelper.Validation.ConflictHasFarmOutSource.Validate();
                    }
                }
            })
        },
        Set: function (obj) {
            this.Container.filter('[data-field="hasfarmoutsource"]').prop('checked', obj.has_farm_outsource);
            this.Container.filter('[data-field="nonhasfarmoutsource"]').prop('checked', obj.non_has_farm_outsource);

            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.FarmOutsource.Validation.Empty.Validate();
                SurveyHelper.FarmOutsource.Validation.Duplicate.Validate();
                SurveyHelper.FarmOutsource.Validation.hasRiceProduct.Validate();
                HireChannelHelper.Validation.ConflictHasFarmOutSource.Validate();
            }
        },
        Reset: function(){
            if (this.Alert) { this.Alert.reset(); }
            if (this.Info) { this.Info.reset(); }
            this.Container.prop('checked', false);
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.FarmOutsource.Container.filter(':checked').length == 0;
                    var msg = '不可漏填此問項';
                    Helper.LogHandler.Log(con, SurveyHelper.FarmOutsource.Alert, msg, this.Guids[0], null, false);
                },
            },
            Duplicate: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.FarmOutsource.Container.filter(':checked').length > 1;
                    var msg = '有無委託農事及畜牧服務業者不得重複勾選';
                    Helper.LogHandler.Log(con, SurveyHelper.FarmOutsource.Alert, msg, this.Guids[0], null, false);
                },
            },
            hasRiceProduct: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var hasCrop = false;
                    CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                        var $product = $(this).find('[name="product"] > option[data-name]:selected');
                        if($product.length == 0) return true; // continue
                        code = $product.data('code');
                        if(code == 102 || code == 103){
                            hasCrop = true;
                            return false;  // break
                        }
                    })
                    var notChecked = SurveyHelper.FarmOutsource.Container.filter('[data-field="nonhasfarmoutsource"]').filter(':checked').length == 1;
                    var con = notChecked && hasCrop;
                    var msg = '【問項3.3】:若【問項1.4】中有種稻作(作物代碼102或103者)，請確認是否有委託代耕';
                    Helper.LogHandler.Log(con, SurveyHelper.FarmOutsource.Info, msg, this.Guids[0], null, false);
                },
            }
        },
    },
    Note: {
        Container: $('#panel1 textarea[name="note"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
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
    IsInvalid: {
        Container: $('#panel1 input[name="isinvalid"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    CloneData[MainSurveyId].is_invalid = $(this).prop('checked');
                }
                if(Helper.LogHandler.ValidationActive) {
                    SurveyHelper.IsInvalid.Validation.ReasonProvided.Validate();
                }
            })
        },
        Set: function(obj){
            this.Container.prop('checked', obj.is_invalid);
            if(Helper.LogHandler.ValidationActive) {
                SurveyHelper.IsInvalid.Validation.ReasonProvided.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Validation: {
            ReasonProvided: {
                Guids: Helper.Guid.CreateMulti(1),
                Validate: function(){
                    var isInvalid = SurveyHelper.IsInvalid.Container.prop('checked');
                    var reasonEmpty = SurveyHelper.InvalidReason.Container.val() == '';

                    var con = isInvalid && reasonEmpty;
                    var msg = '如有句選無效戶，原因不能空白';
                    Helper.LogHandler.Log(con, SurveyHelper.Alert, msg, this.Guids[0], null, false);

                    var con = !isInvalid && !reasonEmpty;
                    var msg = '如未句選無效戶，原因應為空白';
                    Helper.LogHandler.Log(con, SurveyHelper.Alert, msg, this.Guids[1], null, false);
                },
            },
        },
    },
    InvalidReason: {
        Container: $('#panel1 input[name="invalidreason"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    CloneData[MainSurveyId].invalid_reason = $(this).val();
                }
                if(Helper.LogHandler.ValidationActive) {
                    SurveyHelper.IsInvalid.Validation.ReasonProvided.Validate();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.invalid_reason);
             if(Helper.LogHandler.ValidationActive) {
                SurveyHelper.IsInvalid.Validation.ReasonProvided.Validate();
             }
        },
        Reset: function(){
            this.Container.val('');
        },
    },
    AddressMatch: {
        Container: $('#panel1 input[name="addressmatch"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    var field = $(this).data('field');
                    if(field == 'match')
                        CloneData[MainSurveyId].address_match.match = $(this).prop('checked');
                    else if(field == 'mismatch')
                        CloneData[MainSurveyId].address_match.mismatch = $(this).prop('checked');
                }

                if(Helper.LogHandler.ValidationActive) {
                    SurveyHelper.Address.Validation.AddressRequire.Validate();
                    SurveyHelper.AddressMatch.Validation.Duplicate.Validate();
                    SurveyHelper.AddressMatch.Validation.Required.Validate();
                }
            })
        },
        Set: function(obj){
            this.Container.filter('[data-field="match"]').prop('checked', obj.address_match.match);
            this.Container.filter('[data-field="mismatch"]').prop('checked', obj.address_match.mismatch);
            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.Address.Validation.AddressRequire.Validate();
                SurveyHelper.AddressMatch.Validation.Duplicate.Validate();
                SurveyHelper.AddressMatch.Validation.Required.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Validation: {
            Required: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.AddressMatch.Container.filter(':checked').length == 0;
                    var msg = '地址與調查名冊是否相同不可漏填';
                    Helper.LogHandler.Log(con, SurveyHelper.Alert, msg, this.Guids[0], null, false);
                },
            },
            Duplicate: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.AddressMatch.Container.filter(':checked').length > 1;
                    var msg = '地址與調查名冊是否相同限填一個項目';
                    Helper.LogHandler.Log(con, SurveyHelper.Alert, msg, this.Guids[0], null, false);
                },
            },
        },
    },
    Address: {
        Container: $('#panel1 input[name="address"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    CloneData[MainSurveyId].address_match.address = $(this).val();
                }
                if(Helper.LogHandler.ValidationActive) {
                    SurveyHelper.Address.Validation.AddressRequire.Validate();
                }
            })
        },
        Set: function(obj){
            this.Container.val(obj.address_match.address);
            if(Helper.LogHandler.ValidationActive) {
                SurveyHelper.Address.Validation.AddressRequire.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Validation: {
            AddressRequire: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var checked = SurveyHelper.AddressMatch.Container
                                 .filter('[data-field="mismatch"]')
                                 .prop('checked');
                    var empty = !SurveyHelper.Address.Container.val();
                    var con = checked && empty;
                    var msg = '勾選地址與調查名冊不同，地址不可為空白';
                    Helper.LogHandler.Log(con, SurveyHelper.Alert, msg, this.Guids[0]);
                },
            },
        }
    },
    MainIncomeSource: {
        Alert: null,
        Setup: function(){
            this.Alert = new Helper.Alert($('.alert-danger[name="mainincomesource"]'));
        },
        Container: $('#panel2 input[name="mainincomesource"]'),
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData) {
                    var field = $(this).data('field');
                    if(field == 'mainincomesource')
                        CloneData[MainSurveyId].main_income_source = this.checked;
                    else if(field == 'nonmainincomesource')
                        CloneData[MainSurveyId].non_main_income_source = this.checked;

                    if(Helper.LogHandler.ValidationActive){
                        SurveyHelper.MainIncomeSource.Validation.Empty.Validate();
                        SurveyHelper.MainIncomeSource.Validation.Duplicate.Validate();
                        PopulationHelper.Validation.MainIncomeSource.Validate();
                    }
                }
            })
        },
        Set: function (obj) {
            this.Container.filter('[data-field="mainincomesource"]').prop('checked', obj.main_income_source);
            this.Container.filter('[data-field="nonmainincomesource"]').prop('checked', obj.non_main_income_source);

            if(Helper.LogHandler.ValidationActive){
                SurveyHelper.MainIncomeSource.Validation.Empty.Validate();
                SurveyHelper.MainIncomeSource.Validation.Duplicate.Validate();
            }
        },
        Reset: function(){
            if (this.Alert) { this.Alert.reset(); }
            this.Container.prop('checked', false);
        },
        Validation: {
            Empty: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.MainIncomeSource.Container.filter(':checked').length == 0;
                    var msg = '不可漏填此問項';
                    Helper.LogHandler.Log(con, SurveyHelper.MainIncomeSource.Alert, msg, this.Guids[0], null, false);
                },
            },
            Duplicate: {
                Guids: Helper.Guid.CreateMulti(),
                Validate: function(){
                    var con = SurveyHelper.MainIncomeSource.Container.filter(':checked').length > 1;
                    var msg = '全年主要淨收入來源情形不得重複勾選';
                    Helper.LogHandler.Log(con, SurveyHelper.MainIncomeSource.Alert, msg, this.Guids[0], null, false);
                },
            },
        },
    },
    NumberWorker: {
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
var FarmLocationHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = SurveyHelper.Alert;
        this.Bind();
    },
    Container: {
        City: $('#panel1 input[name="city"]'),
        Town: $('#panel1 input[name="town"]'),
        CityTownCode: $('#panel1 select[name="citytowncode"]'),
    },
    Set: function(obj){
        this.Container.City.val(obj.city);
        this.Container.Town.val(obj.town);
        this.Container.CityTownCode.selectpicker('val', obj.code);
        if(Helper.LogHandler.ValidationActive){
            this.Validation.Empty.Validate();
            this.Validation.SameName.Validate();
        }
    },
    Reset: function(){
        this.Container.City.val('');
        this.Container.Town.val('');
        this.Container.CityTownCode.selectpicker('val', '');
    },
    Bind: function(){
        this.Container.City.unbind('change.ns1').on('change.ns1', function(){
            if(CloneData){
                CloneData[MainSurveyId].farm_location.city = $(this).val();
                if(Helper.LogHandler.ValidationActive){
                    FarmLocationHelper.Validation.Empty.Validate();
                    FarmLocationHelper.Validation.SameName.Validate();
                }
            }
        })
        this.Container.Town.unbind('change.ns1').on('change.ns1', function(){
            if(CloneData){
                CloneData[MainSurveyId].farm_location.town = $(this).val();
                if(Helper.LogHandler.ValidationActive){
                    FarmLocationHelper.Validation.Empty.Validate();
                    FarmLocationHelper.Validation.SameName.Validate();
                }
            }
        })
        this.Container.CityTownCode.unbind('change.ns1').on('change.ns1', function(){
            if(CloneData){
                CloneData[MainSurveyId].farm_location.code = parseInt($(this).val());
                if(Helper.LogHandler.ValidationActive){
                    FarmLocationHelper.Validation.Empty.Validate();
                    FarmLocationHelper.Validation.SameName.Validate();
                }
            }
        })
    },
    Validation: {
        Empty: {
            Guids: Helper.Guid.CreateMulti(2),
            Validate: function(){
                var con = FarmLocationHelper.Container.City.val() == '';
                var msg = '不可漏填可耕作地或畜牧用地所在縣市';
                Helper.LogHandler.Log(con, FarmLocationHelper.Alert, msg, this.Guids[0], null, false);

                var con = FarmLocationHelper.Container.Town.val() == '';
                var msg = '不可漏填可耕作地或畜牧用地所在鄉鎮';
                Helper.LogHandler.Log(con, FarmLocationHelper.Alert, msg, this.Guids[1], null, false);

                var con = FarmLocationHelper.Container.CityTownCode.val() == '';
                var msg = '不可漏填可耕作地或畜牧用地代號';
                Helper.LogHandler.Log(con, FarmLocationHelper.Alert, msg, this.Guids[2], null, false);
            },
        },
        SameName: {
            Guids: Helper.Guid.CreateMulti(2),
            Validate: function(){
                var city = FarmLocationHelper.Container.City.val().replace('台', '臺');
                var town = FarmLocationHelper.Container.Town.val().replace('台', '臺');
                var selectedData = FarmLocationHelper.Container.CityTownCode.find('option:selected').data();

                var con = !$.isEmptyObject(selectedData) && (city != selectedData.cityName || town != selectedData.townName);
                var msg = '可耕作地或畜牧用地所在地區之中文與所選代號({0}/{1})不一致'.format(selectedData.cityName, selectedData.townName);
                Helper.LogHandler.Log(con, FarmLocationHelper.Alert, msg, this.Guids[0]);
            },
        },
    },
}
var LandAreaHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="landarea"]'));
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

            if(Helper.LogHandler.ValidationActive){
                LandAreaHelper.Validation.Empty.Validate();
                LandAreaHelper.Validation.LandStatusEmpty.Validate();
                LandAreaHelper.Validation.Duplicate.Validate();
                LandAreaHelper.Validation.SumAreaCheck.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                var checked = $(this).prop('checked');
                var type = $(this).data('landtype-id');
                if(!checked){
                    LandAreaHelper.LandStatus.Container
                    .filter('[data-landtype-id="{0}"]'.format(type))
                    .val('').trigger('change');
                }

                if(CloneData){
                    LandAreaHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        LandAreaHelper.Validation.Empty.Validate();
                        LandAreaHelper.Validation.LandStatusEmpty.Validate();
                        LandAreaHelper.Validation.Duplicate.Validate();
                        LandAreaHelper.Validation.SumAreaCheck.Validate();
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

            if(Helper.LogHandler.ValidationActive){
                LandAreaHelper.Validation.Empty.Validate();
                LandAreaHelper.Validation.LandStatusEmpty.Validate();
                LandAreaHelper.Validation.SumAreaCheck.Validate();
            }
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            Helper.BindIntegerOnly(this.Container);
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
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    LandAreaHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        LandAreaHelper.Validation.Empty.Validate();
                        LandAreaHelper.Validation.LandStatusEmpty.Validate();
                        LandAreaHelper.Validation.SumAreaCheck.Validate();
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
            this.LandStatusEmpty.Guids.Setup();
        },
        Empty: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var empty = CloneData[MainSurveyId].land_areas.length == 0;
                var msg = '不可漏填此問項';
                Helper.LogHandler.Log(empty, LandAreaHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        Duplicate: {
            Guids: Helper.Guid.Create(),
            Validate: function(){
                var trueChecked = LandAreaHelper.LandType.Container.filter('[data-has-land="true"]:checked').length > 0;
                var falseChecked = LandAreaHelper.LandType.Container.filter('[data-has-land="false"]:checked').length > 0;
                var con = trueChecked && falseChecked;
                var msg = '有耕作地及無耕作地不得重複勾選';
                Helper.LogHandler.Log(con, LandAreaHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        LandStatusEmpty: {
            Guids: {
                Object: {},
                Setup: function(){
                    obj = this.Object;
                    LandAreaHelper.LandType.Container.each(function(){
                        var landTypeId = $(this).data('landtype-id');
                        obj[landTypeId] = Helper.Guid.CreateMulti();
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
                    var guid = LandAreaHelper.Validation.LandStatusEmpty.Guids.Filter(landTypeId);
                    var msg = '有勾選{0}應填寫對應面積'.format(landTypeName);
                    Helper.LogHandler.Log(con, LandAreaHelper.Alert, msg, guid, false);
                })
            }
        },
        SumAreaCheck: {
            Guids: Helper.Guid.Create(),
            Validate: function(){
                var landAreaSum = 0;
                LandAreaHelper.LandStatus.Container.each(function(){
                    var landTypeId = $(this).data('landtype-id');
                    var value = parseInt($(this).val());
                    if(Helper.NumberValidate(value)) {
                        if(landTypeId == 2) value = Helper.Round(value * 0.034, 1);
                        landAreaSum += value;
                    }
                })
                landAreaSum = Math.ceil(landAreaSum);

                var cropMarketingAreaMap = {};
                CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                    var landNumber = $(this).find('input[name="landnumber"]').val();
                    var landArea = parseInt($(this).find('input[name="landarea"]').val());
                    if(landNumber in cropMarketingAreaMap){
                        if(landArea && cropMarketingAreaMap[landNumber] < landArea) cropMarketingAreaMap[landNumber] = landArea;
                    }
                    else cropMarketingAreaMap[landNumber] = landArea;
                })
                var cropMarketingAreaSum = Object.values(cropMarketingAreaMap).length > 0 ? Object.values(cropMarketingAreaMap).reduce((a,b)=>a+b) : 0;

                var con = landAreaSum < cropMarketingAreaSum;
                var msg = '【問項1.1】年底耕作地面積總和({0}公畝)應大於或等於【問項1.5】總種植面積({1}公畝)'.format(landAreaSum, cropMarketingAreaSum);
                Helper.LogHandler.Log(con, LandAreaHelper.Alert, msg, this.Guids[0]);
            },
        },
    },
}
var BusinessHelper = {
    Alert: null,
    Info: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="business"]'));
        this.Info = new Helper.Alert($('.alert-info[name="business"]'));
        this.FarmRelatedBusiness.Bind();
        this.Extra.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         if (this.Info) { this.Info.reset(); }
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
            if(Helper.LogHandler.ValidationActive){
                BusinessHelper.Validation.Empty.Validate();
                BusinessHelper.Validation.Duplicate.Validate();
                BusinessHelper.Validation.FarmRelatedBusiness2Checked.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                var checked = $(this).prop('checked');
                var farmRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                if(!checked){
                    BusinessHelper.Extra.Container
                    .filter('[data-farmrelatedbusiness-id="{0}"]'.format(farmRelatedBusinessId))
                    .val('');
                }

                if(CloneData){
                    BusinessHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        BusinessHelper.Validation.Empty.Validate();
                        BusinessHelper.Validation.Duplicate.Validate();
                        BusinessHelper.Validation.MarketType4Checked.Validate();
                        BusinessHelper.Validation.FarmRelatedBusiness2Checked.Validate();
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
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    BusinessHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
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
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = CloneData[MainSurveyId].businesses.length == 0;
                var msg = '不可漏填此問項';
                Helper.LogHandler.Log(con, BusinessHelper.Alert, msg, this.Guids[0], null, false);
            }
        },
        Duplicate: {
            Guids: Helper.Guid.CreateMulti(),
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
                var msg = '無兼營與有兼營不可重複勾選';
                Helper.LogHandler.Log(con, BusinessHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        MarketType4Checked: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var marketType4Checked = AnnualIncomeHelper.AnnualIncome.Container
                                         .filter('[data-markettype-id="4"]:checked').length > 0;
                var farmRelatedBusiness357Checked = false;
                BusinessHelper.FarmRelatedBusiness.Container
                .filter(':checked')
                .each(function(){
                    var farmRelatedBusinessId = $(this).data('farmrelatedbusiness-id');
                    if(farmRelatedBusinessId == 3 ||
                       farmRelatedBusinessId == 4 ||
                       farmRelatedBusinessId == 5 ||
                       farmRelatedBusinessId == 7 ||
                       farmRelatedBusinessId == 8)
                    {
                        farmRelatedBusiness357Checked = true;
                    }
                })
                var con = !marketType4Checked && farmRelatedBusiness357Checked;
                var msg = '若勾選3.、4.、5.、7.、8選項有兼營休閒農場、觀光果園、農村民宿、餐飲店、販售門市、攤販，並運用自家初級農畜產品時，應有勾選【問項1.6】之「休閒、餐飲及相關事業」。';
                Helper.LogHandler.Log(con, BusinessHelper.Info, msg, this.Guids[0], null, false);
            },
        },
        FarmRelatedBusiness2Checked: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = BusinessHelper.FarmRelatedBusiness.Container.filter('[data-farmrelatedbusiness-id="2"]').prop('checked');
                var msg = '勾選『農產品加工』者，應於【問項1.4】【問項1.5】【問項1.6】『農產品』或『畜禽產品』之銷售額計入其加工收入';
                Helper.LogHandler.Log(con, BusinessHelper.Info, msg, this.Guids[0], null, false);
            },
        }
    },
}
var ManagementTypeHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="managementtype"]'));
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

            if(Helper.LogHandler.ValidationActive){
                ManagementTypeHelper.Validation.Empty.Validate();
                ManagementTypeHelper.Validation.Duplicate.Validate();
                ManagementTypeHelper.Validation.MostValuedType.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    managementTypes = [];
                    ManagementTypeHelper.ManagementType.Container
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('managementtype-id');
                        managementTypes.push(id);
                    });
                    CloneData[MainSurveyId].management_types = managementTypes;

                    if(Helper.LogHandler.ValidationActive){
                        ManagementTypeHelper.Validation.Empty.Validate();
                        ManagementTypeHelper.Validation.Duplicate.Validate();
                        ManagementTypeHelper.Validation.MostValuedType.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Empty: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = CloneData[MainSurveyId].management_types.length == 0;
                var msg = '不可漏填此問項';
                Helper.LogHandler.Log(con, ManagementTypeHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        Duplicate: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = CloneData[MainSurveyId].management_types.length > 1;
                var msg = '限註記一個項目';
                Helper.LogHandler.Log(con, ManagementTypeHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        MostValuedType: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var checkedManagementType = ManagementTypeHelper.ManagementType.Container.filter(':checked');
                var checkedManagementTypeId = checkedManagementType.data('managementtype-id');

                var groupedYearSales = {};

                var rows = $.merge(CropMarketingHelper.CropMarketing.Container.find('tr'), LivestockMarketingHelper.LivestockMarketing.Container.find('tr'));
                rows.each(function(){
                    var yearSales = parseInt($(this).find('[name="yearsales"]').val());
                    var managementTypeName = $(this).find('[name="product"] > option:selected').data('managementtype-name');
                    var managementTypeId = $(this).find('[name="product"] > option:selected').data('managementtype-id');
                    if(!managementTypeId || !yearSales) return;
                    if(managementTypeId in groupedYearSales) groupedYearSales[managementTypeId]['yearSales'] += yearSales;
                    else {
                        groupedYearSales[managementTypeId] = {
                            'id': managementTypeId,
                            'name': managementTypeName,
                            'yearSales': yearSales,
                        }
                    }
                })

                var highestObj = null;

                Object.keys(groupedYearSales).forEach(function (managementTypeId) {
                    if(!highestObj || groupedYearSales[managementTypeId]['yearSales'] > highestObj['yearSales']){
                        highestObj = groupedYearSales[managementTypeId];
                    }
                });

                if(highestObj){
                    var con = checkedManagementType.length == 1 && highestObj['id'] != checkedManagementTypeId;
                    var msg = '全年主要經營型態應與【問項1.4及1.5】各作物(畜禽)代碼對應的經營類別銷售額總計最高者({0})相符'.format(highestObj['name']);
                    Helper.LogHandler.Log(con, ManagementTypeHelper.Alert, msg, this.Guids[0]);
                }
            },
        },
    },
}
var CropMarketingHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="cropmarketing"]'));
        var $row = $(row);
        this.CropMarketing.Bind($row);
        this.CropMarketing.$Row = $row;
        this.Adder.Bind();
        Helper.BindCreateIndex(this.CropMarketing.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.CropMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.CropMarketing.Set(array, surveyId);
        if(Helper.LogHandler.ValidationActive){
            CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                CropMarketingHelper.Validation.Required.Validate($(this));
                CropMarketingHelper.Validation.GreaterThanZero.Validate($(this));
                LandAreaHelper.Validation.SumAreaCheck.Validate();
                ManagementTypeHelper.Validation.MostValuedType.Validate();
            })
            CropMarketingHelper.Validation.WorkHourRange.Validate();
            SurveyHelper.FarmOutsource.Validation.hasRiceProduct.Validate();
            MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
            ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
            })
        }
    },
    CropMarketing: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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
                $row.find('input[name="name"]').val(crop_marketing.name);
                $row.find('input[name="landnumber"]').val(crop_marketing.land_number);
                $row.find('input[name="landarea"]').val(crop_marketing.land_area);
                $row.find('input[name="planttimes"]').val(crop_marketing.plant_times);
                $row.find('select[name="unit"]').selectpicker('val', crop_marketing.unit);
                $row.find('input[name="yearsales"]').val(crop_marketing.year_sales);
                $row.find('select[name="hasfacility"]').selectpicker('val', crop_marketing.has_facility);
                $row.find('select[name="loss"]').selectpicker('val', crop_marketing.loss);

                $row.attr('data-survey-id', surveyId);

                crop_marketing.guid = Helper.Guid.Create();
                $row.attr('data-guid', crop_marketing.guid);

                CropMarketingHelper.CropMarketing.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="landnumber"], [name="planttimes"], [name="yearsales"]'));
            Helper.BindFloatOnly($row.find('[name="landarea"]'));
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $nextAll = $tr.nextAll();
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].crop_marketings = CloneData[surveyId].crop_marketings.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        CropMarketingHelper.CropMarketing.Container[0].refreshIndex();

                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(CropMarketingHelper.Alert, $tr, $nextAll);
                            AnnualIncomeHelper.Validation.CropMarketingExist.Validate();
                            AnnualIncomeHelper.Validation.AnnualTotal.Validate();
                            LandAreaHelper.Validation.SumAreaCheck.Validate();
                            ManagementTypeHelper.Validation.MostValuedType.Validate();
                            CropMarketingHelper.Validation.WorkHourRange.Validate();
                            SurveyHelper.FarmOutsource.Validation.hasRiceProduct.Validate();
                            MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
                            ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                                ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
                            })
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
                    var obj = CropMarketingHelper.CropMarketing.Object.Filter(surveyId, guid);
                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.name = $tr.find('[name="name"]').val();
                    obj.land_number = parseInt($tr.find('[name="landnumber"]').val());
                    obj.land_area = parseFloat($tr.find('[name="landarea"]').val());
                    obj.loss = parseInt($tr.find('[name="loss"]').val());
                    obj.plant_times = parseInt($tr.find('[name="planttimes"]').val());
                    obj.unit = parseInt($tr.find('[name="unit"]').val());
                    obj.has_facility = parseInt($tr.find('[name="hasfacility"]').val());
                    obj.year_sales = parseInt($tr.find('[name="yearsales"]').val());

                    if(Helper.LogHandler.ValidationActive){
                        CropMarketingHelper.Validation.Required.Validate($tr);
                        CropMarketingHelper.Validation.GreaterThanZero.Validate($tr);
                        AnnualIncomeHelper.Validation.AnnualTotal.Validate();
                        LandAreaHelper.Validation.SumAreaCheck.Validate();
                        ManagementTypeHelper.Validation.MostValuedType.Validate();
                        CropMarketingHelper.Validation.WorkHourRange.Validate();
                        SurveyHelper.FarmOutsource.Validation.hasRiceProduct.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
                        ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                            ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
                        })
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="cropmarketing"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = CropMarketingHelper.CropMarketing.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].crop_marketings.push(obj);

                    $row = CropMarketingHelper.CropMarketing.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    CropMarketingHelper.CropMarketing.Container.append($row);
                    CropMarketingHelper.CropMarketing.Container[0].refreshIndex();

                    if(Helper.LogHandler.ValidationActive){
                        CropMarketingHelper.Validation.Required.Validate($row);
                        CropMarketingHelper.Validation.GreaterThanZero.Validate($row);
                        CropMarketingHelper.Validation.IncomeChecked.Validate();
                        SurveyHelper.FarmOutsource.Validation.hasRiceProduct.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(8),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = CropMarketingHelper.CropMarketing.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name);
                }
                Helper.LogHandler.Log(!$row.find('[name="product"]').val(), CropMarketingHelper.Alert, makeString('作物代碼'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="name"]').val(), CropMarketingHelper.Alert, makeString('作物名稱'), this.Guids[1], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="landnumber"]').val(), CropMarketingHelper.Alert, makeString('耕作地代號'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="landarea"]').val(), CropMarketingHelper.Alert, makeString('種植面積'), this.Guids[3], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="planttimes"]').val(), CropMarketingHelper.Alert, makeString('種植次數'), this.Guids[4], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="unit"]').val(), CropMarketingHelper.Alert, makeString('計量單位'), this.Guids[5], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="yearsales"]').val(), CropMarketingHelper.Alert, makeString('全年銷售額'), this.Guids[6], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="hasfacility"]').val(), CropMarketingHelper.Alert, makeString('是否使用農業設施'), this.Guids[7], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="loss"]').val(), CropMarketingHelper.Alert, makeString('特殊情形'), this.Guids[8], guid, false);
            },
        },
        GreaterThanZero: {
            Guids: Helper.Guid.CreateMulti(2),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = CropMarketingHelper.CropMarketing.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可為0'.format(index, name);
                }
                Helper.LogHandler.Log(parseInt($row.find('[name="landnumber"]').val()) === 0, CropMarketingHelper.Alert, makeString('耕作地代號'), this.Guids[0], guid);
                Helper.LogHandler.Log(parseFloat($row.find('[name="landarea"]').val()) === 0, CropMarketingHelper.Alert, makeString('種植面積'), this.Guids[1], guid);
                Helper.LogHandler.Log(parseInt($row.find('[name="planttimes"]').val()) === 0, CropMarketingHelper.Alert, makeString('種植次數'), this.Guids[2], guid);
            },
        },
        IncomeChecked: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="1"]')
                              .filter(':checked').length > 0;
                var exists = CropMarketingHelper.CropMarketing.Container.find('tr').length > 0;
                var con = !checked && exists;
                var msg = '有生產農產品，【問項1.7】應有勾選『農作物及其製品』之銷售額區間';
                Helper.LogHandler.Log(con, CropMarketingHelper.Alert, msg, this.Guids[0]);
            },
        },
        WorkHourRange: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function(){

                var selfWorkHour = 0;
                var longTermWorkHour = 0;
                var shortTermWorkHour = 0;
                var noSalaryWorkHour = 0;

                PopulationHelper.Population.Container.find('tr').each(function(){
                    var farmerWorkday = $(this).find('[name="farmerworkday"] > option:selected').data('minDay');
                    if(farmerWorkday > 0){
                        result = parseInt(farmerWorkday) * 8
                        selfWorkHour += result;
                    }
                })
                LongTermHireHelper.LongTermHire.Container.find('tr').each(function(){
                    var sumCount = $(this).find('[name="sumcount"]').val();
                    var month = $(this).find('[name="month"]').val().length;
                    var avgWorkDay = $(this).find('[name="avgworkday"]').val();

                    if(sumCount > 0 && month > 0 && avgWorkDay > 0){
                        result = parseInt(sumCount) * month * parseFloat(avgWorkDay) * 8;
                        longTermWorkHour += result;
                    }
                })
                ShortTermHireHelper.ShortTermHire.Container.find('tr').each(function(){
                    var sumCount = $(this).find('[name="sumcount"]').val();
                    var avgWorkDay = $(this).find('[name="avgworkday"]').val();

                    if(sumCount > 0 && avgWorkDay > 0){
                        result = parseInt(sumCount) * parseFloat(avgWorkDay) * 8;
                        shortTermWorkHour += result;
                    }
                })
                NoSalaryHireHelper.NoSalaryHire.Container.find('tr').each(function(){
                    var count = $(this).find('[name="count"]').val();
                    var avgWorkDay = $(this).find('[name="avgworkday"]').val();

                    if(count > 0 && avgWorkDay > 0){
                        result = parseInt(count) * parseFloat(avgWorkDay) * 8;
                        noSalaryWorkHour += result;
                    }
                })

                selfWorkHour = Helper.Round(selfWorkHour);
                longTermWorkHour = Helper.Round(longTermWorkHour);
                shortTermWorkHour = Helper.Round(shortTermWorkHour);
                noSalaryWorkHour = Helper.Round(noSalaryWorkHour);

                var workHours = selfWorkHour + longTermWorkHour + shortTermWorkHour + noSalaryWorkHour;

                var reasonableWorkHourMin = 0;
                var reasonableWorkHourMax = 0;

                var minMsgs = [];
                var maxMsgs = [];

                /* Count from crops */

                CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                    var $product = $(this).find('[name="product"] > option[data-name]:selected');
                    if($product.length == 0) return;

                    var landNumber = $(this).find('[name="landnumber"]').val();
                    var landArea = $(this).find('[name="landarea"]').val();
                    var plantTimes = $(this).find('[name="planttimes"]').val();

                    var minHour = $product.data('minHour');
                    var maxHour = $product.data('maxHour');
                    var productName = $product.data('name');
                    var productId = $product.val();
                    var managementTypeId = $product.data('managementtypeId');
                    var userInputProductName = $(this).find('[name="name"]').val();

                    /* Only count max land area */
                    if(managementTypeId == 6){
                        var nextAllRowHasEqual = $(this).nextAll().filter(function(){
                            return parseInt($(this).find('[name="landnumber"]').val()) == landNumber &&
                                   $(this).find('[name="product"] > option:selected').data('name') == productName &&
                                   parseInt($(this).find('[name="landarea"]').val()) == landArea;
                        }).length > 0;
                        if (nextAllRowHasEqual) return;

                        var anyRowHasGreater = CropMarketingHelper.CropMarketing.Container.find('tr').filter(function(){
                            return parseInt($(this).find('[name="landnumber"]').val()) == landNumber &&
                                   $(this).find('[name="product"] > option:selected').data('name') == productName &&
                                   parseInt($(this).find('[name="landarea"]').val()) > landArea;
                        }).length > 0;
                        if (anyRowHasGreater) return;
                    }

                    /* Replace min, max if user input product name match sub-product */
                    /* Sub-product not display in dropdown UI */
                    var matchingRate = 0.6;
                    $(this).find('[name="product"] > option[data-parent-id="{0}"]'.format(productId)).each(function(){
                        var name = $(this).data('name');
                        if(!name) return;

                        mr = compareTwoStrings(Helper.ClearString(name), Helper.ClearString(userInputProductName));

                        if(mr > matchingRate){
                            console.log('Find sub product {0} for {1}'.format(userInputProductName, name));
                            minHour = $(this).data('minHour');
                            maxHour = $(this).data('maxHour');
                            matchingRate = mr;
                            productName = name;
                        }
                    })

                    if(!minHour || !maxHour){
                        console.log('Min or max work hour for {0} is not found.'.format(productName));
                        minMsgs.push('<b class="text-primary">{0}({1})</b>'.format(productName, 0));
                        maxMsgs.push('<b class="text-primary">{0}({1})</b>)'.format(productName, 0));
                        return;
                    }

                    if(landArea > 0 && plantTimes > 0){
                        var resultMin = Helper.Round(parseFloat(landArea)/100 * parseFloat(plantTimes) * parseFloat(minHour), 1);
                        var resultMax = Helper.Round(parseFloat(landArea)/100 * parseFloat(plantTimes) * parseFloat(maxHour), 1);

                        if(minHour > 0) reasonableWorkHourMin += resultMin;
                        if(maxHour > 0) reasonableWorkHourMax += resultMax;

                        minMsgs.push('<b class="text-primary">{0}({1})</b>'.format(productName, resultMin));
                        maxMsgs.push('<b class="text-primary">{0}({1})</b>'.format(productName, resultMax));
                    }

                })

                /* Count from livestocks */

                LivestockMarketingHelper.LivestockMarketing.Container.find('tr').each(function(){
                    var $product = $(this).find('[name="product"] > option[data-name]:selected');
                    if($product.length == 0) return;

                    var raisingNumber = $(this).find('[name="raisingnumber"]').val();
                    var minHour = $product.data('minHour');
                    var maxHour = $product.data('maxHour');
                    var productName = $product.data('name');

                    if(!minHour || !maxHour){
                        console.log('Min or max work hour for {0} is not found.'.format(productName));
                        minMsgs.push('<b class="text-warning">{0}({1})</b>'.format(productName, 0));
                        maxMsgs.push('<b class="text-warning">{0}({1})</b>'.format(productName, 0));
                        return;
                    }

                    if(raisingNumber > 0){
                        var resultMin = Helper.Round(parseFloat(raisingNumber) * parseFloat(minHour), 1);
                        var resultMax = Helper.Round(parseFloat(raisingNumber) * parseFloat(maxHour), 1);

                        if(minHour > 0) reasonableWorkHourMin += resultMin;
                        if(maxHour > 0) reasonableWorkHourMax += resultMax;

                        minMsgs.push('<b class="text-warning">{0}({1})</b>'.format(productName, resultMin));
                        maxMsgs.push('<b class="text-warning">{0}({1})</b>'.format(productName, resultMax));
                    }

                })

                reasonableWorkHourMin = Helper.Round(reasonableWorkHourMin, 1);
                reasonableWorkHourMax = Helper.Round(reasonableWorkHourMax, 1);

                var con = reasonableWorkHourMin > workHours || reasonableWorkHourMax < workHours;

                var workHourMsg = '\
                    自家工與僱工工作時數：自家工({0}) + 常僱工({1}) + 臨時工({2}) + 不支薪({3}) = {4}小時</br>\
                    合理工作時數下限：{5} = {6}小時</br>\
                    合理工作時數上限：{7} = {8}小時</br>\
                ';
                var msg = '填列之自家工與僱工工作時數不在合理工作時數區間，請確認：</br>'
                workHourMsg = workHourMsg.format(selfWorkHour,
                                                 longTermWorkHour,
                                                 shortTermWorkHour,
                                                 noSalaryWorkHour,
                                                 workHours,
                                                 minMsgs.join(' + '),
                                                 reasonableWorkHourMin,
                                                 maxMsgs.join(' + '),
                                                 reasonableWorkHourMax)
                Helper.LogHandler.Log(con, SurveyHelper.Hire.Info, msg + workHourMsg, this.Guids[0], null, false);

                msg = '很好！填列之自家工與僱工工作時數「符合」合理工作時數區間：</br>';
                Helper.LogHandler.Log(!con, SurveyHelper.Hire.Success, msg + workHourMsg, this.Guids[1], null, false);

            },
        },
    },
}
var LivestockMarketingHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="livestockmarketing"]'));
        var $row = $(row);
        this.LivestockMarketing.Bind($row);
        this.LivestockMarketing.$Row = $row;
        this.Adder.Bind();
        Helper.BindCreateIndex(this.LivestockMarketing.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.LivestockMarketing.Reset();
    },
    Set: function(array, surveyId){
        this.LivestockMarketing.Set(array, surveyId);
        if(Helper.LogHandler.ValidationActive){
            LivestockMarketingHelper.LivestockMarketing.Container.find('tr').each(function(){
                LivestockMarketingHelper.Validation.Required.Validate($(this));
                LivestockMarketingHelper.Validation.RaiseNumberYearSalesChecked.Validate($(this));
                ManagementTypeHelper.Validation.MostValuedType.Validate();
            })
            CropMarketingHelper.Validation.WorkHourRange.Validate();
            ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
            })
        }
    },
    LivestockMarketing: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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
                $row.find('input[name="name"]').val(livestock_marketing.name);
                $row.find('select[name="unit"]').selectpicker('val', livestock_marketing.unit);
                $row.find('input[name="raisingnumber"]').val(livestock_marketing.raising_number);
                $row.find('input[name="yearsales"]').val(livestock_marketing.year_sales);
                $row.find('select[name="contract"]').selectpicker('val', livestock_marketing.contract);
                $row.find('select[name="loss"]').selectpicker('val', livestock_marketing.loss);

                $row.attr('data-survey-id', surveyId);

                livestock_marketing.guid = Helper.Guid.Create();
                $row.attr('data-guid', livestock_marketing.guid);

                LivestockMarketingHelper.LivestockMarketing.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="raisingnumber"], [name="yearsales"]'));
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $nextAll = $tr.nextAll();
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].livestock_marketings = CloneData[surveyId].livestock_marketings.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        LivestockMarketingHelper.LivestockMarketing.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(LivestockMarketingHelper.Alert, $tr, $nextAll);
                            AnnualIncomeHelper.Validation.LivestockMarketingExist.Validate();
                            AnnualIncomeHelper.Validation.AnnualTotal.Validate();
                            ManagementTypeHelper.Validation.MostValuedType.Validate();
                            CropMarketingHelper.Validation.WorkHourRange.Validate();
                            ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                                ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
                            })
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
                    var obj = LivestockMarketingHelper.LivestockMarketing.Object.Filter(surveyId, guid);
                    obj.product = parseInt($tr.find('[name="product"]').val());
                    obj.name = $tr.find('[name="name"]').val();
                    obj.contract = parseInt($tr.find('[name="contract"]').val());
                    obj.loss = parseInt($tr.find('[name="loss"]').val());
                    obj.raising_number = parseInt($tr.find('[name="raisingnumber"]').val());
                    obj.year_sales = parseInt($tr.find('[name="yearsales"]').val());
                    obj.unit = parseInt($tr.find('[name="unit"]').val());

                    if(Helper.LogHandler.ValidationActive){
                        LivestockMarketingHelper.Validation.Required.Validate($tr);
                        LivestockMarketingHelper.Validation.RaiseNumberYearSalesChecked.Validate($tr);
                        AnnualIncomeHelper.Validation.AnnualTotal.Validate();
                        ManagementTypeHelper.Validation.MostValuedType.Validate();
                        CropMarketingHelper.Validation.WorkHourRange.Validate();
                        ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                            ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
                        })
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="livestockmarketing"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = LivestockMarketingHelper.LivestockMarketing.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].livestock_marketings.push(obj);

                    $row = LivestockMarketingHelper.LivestockMarketing.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LivestockMarketingHelper.LivestockMarketing.Container.append($row);
                    LivestockMarketingHelper.LivestockMarketing.Container[0].refreshIndex();

                    if(Helper.LogHandler.ValidationActive){
                        LivestockMarketingHelper.Validation.Required.Validate($row);
                        LivestockMarketingHelper.Validation.RaiseNumberYearSalesChecked.Validate($row);
                        LivestockMarketingHelper.Validation.IncomeChecked.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(4),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name)
                }
                Helper.LogHandler.Log(!$row.find('[name="product"]').val(), LivestockMarketingHelper.Alert, makeString('畜禽代碼'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="name"]').val(), LivestockMarketingHelper.Alert, makeString('畜禽名稱'), this.Guids[1], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="unit"]').val(), LivestockMarketingHelper.Alert, makeString('計量單位'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="contract"]').val(), LivestockMarketingHelper.Alert, makeString('契約飼養'), this.Guids[3], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="loss"]').val(), LivestockMarketingHelper.Alert, makeString('特殊情形'), this.Guids[4], guid, false);
            },
        },
        RaiseNumberYearSalesChecked: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').index($row) + 1;
                var msg = '第<i class="row-index">{0}</i>列年底在養數量及全年銷售額不可同時空白或為0'.format(index)
                var raisingNumber = $row.find('[name="raisingnumber"]').val();
                var yearSales = $row.find('[name="yearsales"]').val();
                var con = (raisingNumber == 0 && yearSales == 0) || (raisingNumber == '' && yearSales == '');
                Helper.LogHandler.Log(con, LivestockMarketingHelper.Alert, msg, this.Guids[0], guid);
            },
        },
        IncomeChecked: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="2"]')
                              .filter(':checked').length > 0;
                var exists = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').length > 0;
                var con = !checked && exists;
                var msg = '有生產畜產品，【問項1.7】應有勾選『畜禽作物及其製品』之銷售額區間';
                Helper.LogHandler.Log(con, LivestockMarketingHelper.Alert, msg, this.Guids[0]);
            },
        },
    },
}
var AnnualIncomeHelper = {
    Success: null,
    Alert: null,
    Info: null,
    Setup: function(){
        this.Success = new Helper.Alert($('.alert-success[name="annualincome"]'));
        this.Alert = new Helper.Alert($('.alert-danger[name="annualincome"]'));
        this.Info = new Helper.Alert($('.alert-info[name="annualincome"]'));
        this.AnnualIncome.Bind();
    },
    Set: function(array) {
        this.AnnualIncome.Set(array);
    },
    Reset: function() {
        if (this.Success) { this.Success.reset(); }
        if (this.Alert) { this.Alert.reset(); }
        if (this.Info) { this.Info.reset(); }
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
            if(Helper.LogHandler.ValidationActive){
                AnnualIncomeHelper.Validation.IncomeTotal.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
            this.Container.attr('data-annualincome-id', '')
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
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
                            var id = $(this).attr('data-annualincome-id');
                            var obj = AnnualIncomeHelper.AnnualIncome.Object.New(MainSurveyId, marketTypeId, incomeRangeId);
                            if(id) obj.id = id;
                            annualIncomes.push(obj);

                            if(Helper.LogHandler.ValidationActive){
                                AnnualIncomeHelper.Validation.IncomeTotal.Validate();
                                AnnualIncomeHelper.Validation.CropMarketingExist.Validate();
                                AnnualIncomeHelper.Validation.LivestockMarketingExist.Validate();
                                AnnualIncomeHelper.Validation.AnnualTotal.Validate();
                                CropMarketingHelper.Validation.IncomeChecked.Validate();
                                LivestockMarketingHelper.Validation.IncomeChecked.Validate();
                                BusinessHelper.Validation.MarketType4Checked.Validate();
                                PopulationHelper.Validation.MarketType3Checked.Validate();
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
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="1"]')
                              .filter(':checked').length > 0;
                var exists = CropMarketingHelper.CropMarketing.Container.find('tr').length > 0;
                var con = checked && !exists;
                var msg = '有勾選『農作物及其製品』之銷售額區間，【問項1.5】應有生產農產品';
                Helper.LogHandler.Log(con, AnnualIncomeHelper.Alert, msg, this.Guids[0]);
            },
        },
        LivestockMarketingExist: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var checked = AnnualIncomeHelper.AnnualIncome.Container
                              .filter('[data-markettype-id="2"]')
                              .filter(':checked').length > 0;
                var exists = LivestockMarketingHelper.LivestockMarketing.Container.find('tr').length > 0;
                var con = checked && !exists;
                var msg = '有勾選『畜禽作物及其製品』之銷售額區間，【問項1.6】應有生產畜產品';
                Helper.LogHandler.Log(con, AnnualIncomeHelper.Alert, msg, this.Guids[0]);
            },
        },
        IncomeTotal: {
            Guids: Helper.Guid.CreateMulti(2),
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

                var con = checkedMax <= totalMin || checkedMin > (totalMax - 1);
                var msg = '銷售額總計之區間，應與各類別區間加總相對應';
                Helper.LogHandler.Log(con, AnnualIncomeHelper.Alert, msg, this.Guids[0]);

                var con = $input.length == 0;
                var msg = '銷售額總計不可漏填';
                Helper.LogHandler.Log(con, AnnualIncomeHelper.Alert, msg, this.Guids[1]);
            },
        },
        AnnualTotal: {
            Guids: Helper.Guid.CreateMulti(3),
            Validate: function(){
                function getYearSales($row){
                    var value = parseInt($row.find('[name="yearsales"]').val());
                    if(Helper.NumberValidate(value)){
                        return value;
                    }
                    else return 0;
                }

                /* Crop Marketing */
                checkedTotal = AnnualIncomeHelper.AnnualIncome.Container.filter('[data-markettype-id="1"]:checked');
                // check total
                var countTotal = 0;
                CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                    countTotal += getYearSales($(this));
                })

                var checkedMin = checkedTotal.data('min') * 10000;
                var checkedMax = checkedTotal.data('max') * 10000 - 1;

                var con = countTotal < checkedMin || countTotal > checkedMax;
                var msg = '【問項1.5】農作物產銷情形之全年銷售額總計({0}元)與勾選農作物之全年銷售額區間不符'.format(Helper.NumberWithCommas(countTotal));
                Helper.LogHandler.Log(checkedTotal.length == 1 && con, AnnualIncomeHelper.Alert, msg, this.Guids[0]);
                // show total
                var msg ='目前農作物產銷情形之全年銷售額總計：{0}元'.format(Helper.NumberWithCommas(countTotal));
                Helper.LogHandler.Log(countTotal > 0, AnnualIncomeHelper.Success, msg, this.Guids[1], null, false);

                /* Livestock Marketing */
                checkedTotal = AnnualIncomeHelper.AnnualIncome.Container.filter('[data-markettype-id="2"]:checked');
                // check total
                var countTotal = 0;
                LivestockMarketingHelper.LivestockMarketing.Container.find('tr').each(function(){
                    countTotal += getYearSales($(this));
                })

                var checkedMin = checkedTotal.data('min') * 10000;
                var checkedMax = checkedTotal.data('max') * 10000 - 1;

                var con = countTotal < checkedMin  || countTotal >= checkedMax;
                var msg = '【問項1.6】畜禽產銷情形之全年銷售額總計({0}元)與勾選畜禽產品之全年銷售額區間不符'.format(Helper.NumberWithCommas(countTotal));
                Helper.LogHandler.Log(checkedTotal.length == 1 && con, AnnualIncomeHelper.Alert, msg, this.Guids[2]);
                // show total
                var msg ='目前畜禽產銷情形之全年銷售額總計：{0}元'.format(Helper.NumberWithCommas(countTotal));
                Helper.LogHandler.Log(countTotal > 0, AnnualIncomeHelper.Success, msg, this.Guids[3], null, false);
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
        this.Alert = new Helper.Alert($('.alert-danger[name="populationage"]'));
        this.PopulationAge.Bind();
    },
    PopulationAge: {
        Object: {
            New: function(surveyId, ageScopeId, genderId){
                return {
                    survey: surveyId,
                    age_scope: ageScopeId,
                    gender: genderId,
                }
            },
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
            Helper.BindIntegerOnly(this.Container);
            this.Container.unbind('change.ns1').on('change.ns1', function(){
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
                    if(!obj){
                        obj = PopulationAgeHelper.PopulationAge.Object.New(MainSurveyId, ageScopeId, genderId);
                        CloneData[MainSurveyId].population_ages.push(obj);
                    }
                    obj.count = parseInt($(this).val());
                    if(Helper.LogHandler.ValidationActive){
                        PopulationAgeHelper.Validation.MemberCount.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        MemberCount: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var over15Male = 0;
                var over15Female = 0;
                PopulationAgeHelper.PopulationAge.Container
                .filter('[data-agescope-id="5"]')
                .each(function(){
                    var count = parseInt($(this).val());
                    var genderId = $(this).attr('data-gender-id');
                    if(count){
                        if(genderId == 1) over15Male += count;
                        if(genderId == 2) over15Female += count
                    }
                })
                var male = PopulationHelper.Population.Container.find('[name="gender"] > option[value="1"]:selected').length;
                var female = PopulationHelper.Population.Container.find('[name="gender"] > option[value="2"]:selected').length;
                var con = (over15Male != male) || (over15Female != female);
                var msg = '滿15歲以上男、女性人數，應等於【問項2.2】男、女性人數';
                Helper.LogHandler.Log(con, PopulationAgeHelper.Alert, msg, this.Guids[0]);
            },
        },

    },
}
var PopulationHelper = {
    Alert: null,
    Info: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="population"]'));
        this.Info = new Helper.Alert($('.alert-info[name="population"]'));
        var $row = $(row);
        this.Population.Bind($row);
        this.Adder.Bind();
        this.Population.$Row = $row;
        Helper.BindCreateIndex(this.Population.Container);

    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.Population.Reset();
    },
    Set: function(array, surveyId){
        this.Population.Set(array, surveyId);
        if(Helper.LogHandler.ValidationActive){
            PopulationHelper.Validation.Init.Validate();
            PopulationHelper.Population.Container.find('tr').each(function(){
                PopulationHelper.Validation.Required.Validate($(this));
                PopulationHelper.Validation.BirthYear.Validate($(this));
                PopulationHelper.Validation.FarmerWorkDay.Validate($(this));
                PopulationHelper.Validation.RelationShip.Validate($(this));
            })
            PopulationHelper.Validation.AtLeastOneWorker.Validate();
            PopulationHelper.Validation.FarmerWorkDayOver150.Validate();
            CropMarketingHelper.Validation.WorkHourRange.Validate();
            PopulationHelper.Validation.MainIncomeSource.Validate();
        }
    },
    Population: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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
                $row.attr('data-survey-id', surveyId);

                population.guid = Helper.Guid.Create();
                $row.attr('data-guid', population.guid);
                PopulationHelper.Population.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="birthyear"]'));
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $nextAll = $tr.nextAll();
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].populations = CloneData[surveyId].populations.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        PopulationHelper.Population.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(PopulationHelper.Alert, $tr, $nextAll);
                            PopulationAgeHelper.Validation.MemberCount.Validate();
                            PopulationHelper.Validation.AtLeastOneWorker.Validate();
                            PopulationHelper.Validation.FarmerWorkDayOver150.Validate();
                            CropMarketingHelper.Validation.WorkHourRange.Validate();
                            PopulationHelper.Validation.MainIncomeSource.Validate();
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

                    if(Helper.LogHandler.ValidationActive){
                        PopulationHelper.Validation.Required.Validate($tr);
                        PopulationHelper.Validation.BirthYear.Validate($tr);
                        PopulationHelper.Validation.FarmerWorkDay.Validate($tr);
                        PopulationHelper.Validation.RelationShip.Validate($tr);
                        PopulationHelper.Validation.AtLeastOneWorker.Validate();
                        PopulationHelper.Validation.MarketType3Checked.Validate();
                        PopulationHelper.Validation.FarmerWorkDayOver150.Validate();
                        PopulationAgeHelper.Validation.MemberCount.Validate();
                        CropMarketingHelper.Validation.WorkHourRange.Validate();
                        PopulationHelper.Validation.MainIncomeSource.Validate();
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="population"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = PopulationHelper.Population.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].populations.push(obj);

                    $row = PopulationHelper.Population.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    PopulationHelper.Population.Container.append($row);
                    PopulationHelper.Population.Container[0].refreshIndex();
                    if(Helper.LogHandler.ValidationActive){
                        PopulationHelper.Validation.Required.Validate($row);
                        PopulationAgeHelper.Validation.MemberCount.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Init: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var msg = '請檢視「全年從事自家農牧業工作日數」是否有換算，並確認工作日數與經營規模之合理性'
                Helper.LogHandler.Log(true, PopulationHelper.Info, msg, this.Guids[0], null, false);
            },
        },
        Required: {
            Guids: Helper.Guid.CreateMulti(6),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name)
                }
                Helper.LogHandler.Log(!$row.find('[name="relationship"]').val(), PopulationHelper.Alert, makeString('與戶長關係'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="gender"]').val(), PopulationHelper.Alert, makeString('性別'), this.Guids[1], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="birthyear"]').val(), PopulationHelper.Alert, makeString('出生年次'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="educationlevel"]').val(), PopulationHelper.Alert, makeString('教育程度'), this.Guids[3], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="farmerworkday"]').val(), PopulationHelper.Alert, makeString('全年自家農牧業工作日數'), this.Guids[4], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="lifestyle"]').val(), PopulationHelper.Alert, makeString('全年主要生活型態'), this.Guids[5], guid, false);
            },
        },
        BirthYear: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                var year = $row.find('[name="birthyear"]').val();
                if(year == '') return;
                var con = parseInt(year) < 1 || parseInt(year) > 98 || !Helper.NumberValidate(year);
                var msg = '第<i class="row-index">{0}</i>列出生年次應介於1年至98年之間（實足年齡滿15歲）'.format(index);
                Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[0], guid);
            },
        },
        RelationShip: {
            Guids: Helper.Guid.CreateMulti(3),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                var $hosts = $row.siblings().find('[name="relationship"] > option[value="1"]:selected').parents('tr');
                if($hosts.length == 1){
                    var relationship = $row.find('[name="relationship"]').val();
                    var gender = $row.find('[name="gender"]').val();
                    var year = $row.find('[name="birthyear"]').val();

                    $host = $hosts.first();
                    var hostGender = $host.find('[name="gender"]').val();
                    var hostYear = $host.find('[name="birthyear"]').val();

                    var con = relationship == 2 && gender == hostGender;
                    var msg = '第<i class="row-index">{0}</i>列與經濟戶長關係代號為2者，性別應與經濟戶長不同'.format(index);
                    Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[0], guid);

                    var con = (relationship == 3 || relationship == 7) && year && hostYear && year > hostYear;
                    var msg = '第<i class="row-index">{0}</i>列與經濟戶長關係代號為3或7者，出生年次應小於經濟戶長出生年次'.format(index);
                    Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[1], guid, false);

                    var con = (relationship == 5 || relationship == 6) && year && hostYear && year < hostYear;
                   var msg = '第<i class="row-index">{0}</i>列與經濟戶長關係代號為5或6者，出生年次應大於經濟戶長出生年次'.format(index);
                    Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[2], guid, false);
                }
            },
        },
        FarmerWorkDay: {
            Guids: Helper.Guid.CreateMulti(4),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = PopulationHelper.Population.Container.find('tr').index($row) + 1;
                var farmerWorkdayId = $row.find('[name="farmerworkday"]').val();
                var lifeStyleId = $row.find('[name="lifestyle"]').val();
                var birthYear = $row.find('[name="birthyear"]').val();
                var con = farmerWorkdayId >=  7 && lifeStyleId != 1;
                var msg = '第<i class="row-index">{0}</i>列全年從事自家農牧業工作日數大於180日，主要生活型態應勾選『自營農牧業工作』'.format(index);
                Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[0], guid);

                var con = farmerWorkdayId == 1 && lifeStyleId == 1;
                var msg = '第<i class="row-index">{0}</i>列全年從事自家農牧業工作日數勾選『無』，主要生活型態不得勾選『自營農牧業工作』'.format(index);
                Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[1], guid);

                var con = farmerWorkdayId < 3 && lifeStyleId == 1;
                var msg = '第<i class="row-index">{0}</i>列全年主要生活型態勾選『自營農牧業工作』，全年從事自家農牧業工作日數應超過30日，惟種稻或果樹採粗放式經營者不在此限'.format(index);
                Helper.LogHandler.Log(con, PopulationHelper.Info, msg, this.Guids[2], guid, false);

                var con = farmerWorkdayId >= 7 && (lifeStyleId == 6 || lifeStyleId == 7);
                var msg = '第<i class="row-index">{0}</i>列全年主要生活型態勾選『料理家務、育兒』或『其他』，全年從事自家農牧業工作日數應小於180日'.format(index);
                Helper.LogHandler.Log(con, PopulationHelper.Info, msg, this.Guids[3], guid, false);

                var con = birthYear <= 31 && farmerWorkdayId >= 4 && lifeStyleId == 1;
                var msg = '第<i class="row-index">{0}</i>列超過80歲（出生年次小於33），從事自家農牧業工作日數超過60日，請確認'.format(index);
                Helper.LogHandler.Log(con, PopulationHelper.Info, msg, this.Guids[4], guid, false);

            },
        },
        AtLeastOneWorker: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = true;
                PopulationHelper.Population.Container.find('tr').each(function(){
                    var farmerWorkdayId = $(this).find('[name="farmerworkday"]').val();
                    var birthYear = $(this).find('[name="birthyear"]').val();
                    if(farmerWorkdayId > 1 && birthYear >= 44 && birthYear <= 98){
                        con = false;
                    }
                })
                var msg = '至少應有1位未滿70歲（出生年次介於44年至98年）從事自家農牧業工作日數1日以上。';
                Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[0]);
            },
        },
        MarketType3Checked: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var lifeStyleChecked = PopulationHelper.Population.Container.find('[name="lifestyle"] > option[value="3"]:selected').length > 0;
                var marketTypeChecked = AnnualIncomeHelper.AnnualIncome.Container.filter('[data-markettype-id="3"]:checked').length > 0;
                var con = lifeStyleChecked && !marketTypeChecked;
                var msg = '戶內人口主要生活型態有勾選『受託提供農事及畜牧服務』，【問項1.7】應有勾選『受託提供農事及畜牧服務』之銷售額區間';
                Helper.LogHandler.Log(con, PopulationHelper.Alert, msg, this.Guids[0]);
            },
        },
        FarmerWorkDayOver150: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = false;
                PopulationHelper.Population.Container.find('tr').each(function(){
                    var farmerWorkdayId = $(this).find('[name="farmerworkday"]').val();
                    if(farmerWorkdayId >= 6) {
                        con = true;
                        return false;
                    }
                })
                var msg = '全年從事自家農牧業工作日數達150日以上，請確認經營類型及規模之合理性';
                Helper.LogHandler.Log(con, PopulationHelper.Info, msg, this.Guids[0], null, false);
            },
        },
        MainIncomeSource: {
            Guids: Helper.Guid.CreateMulti(2),
            Validate: function(){
                var mainIncomeSourceChecked = SurveyHelper.MainIncomeSource.Container.filter(
                    '[data-field=mainincomesource]:checked'
                ).length > 0;
                var lifeStyle1Seleted = PopulationHelper.Population.Container.find(
                    '[name="lifestyle"] > option[value="1"]:selected'
                ).length > 0;
                var con = mainIncomeSourceChecked && !lifeStyle1Seleted;
                var msg = '勾選「以自家農牧業淨收入為主」，則【問項2.2】應至少有一位勾選「1.自營農牧業工作」';
                Helper.LogHandler.Log(con, SurveyHelper.MainIncomeSource.Alert, msg, this.Guids[0], null, true);

                var nonMainIncomeSourceChecked = SurveyHelper.MainIncomeSource.Container.filter(
                    '[data-field=nonmainincomesource]:checked'
                ).length > 0;
                var lifeStyle2345Seleted = [2,3,4,5].some(function(value, index, array){
                    return PopulationHelper.Population.Container.find(
                        '[name="lifestyle"] > option[value="{0}"]:selected'.format(value),
                    ).length > 0;
                })
                var con = nonMainIncomeSourceChecked && !lifeStyle2345Seleted;
                var msg = '勾選「以自家農牧業外淨收入為主」，則【問項2.2】應至少有一位勾選「2.受僱農牧業工作」或「3. 受託提供農事及畜牧服務」或「4.自營農牧業外工作」或「5.受僱農牧業外工作」';
                Helper.LogHandler.Log(con, SurveyHelper.MainIncomeSource.Alert, msg, this.Guids[1], null, true);
            }
        },
    },
}
var LongTermHireHelper = {
    Alert: null,
    Info: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="longtermhire"]'));
        this.Info = new Helper.Alert($('.alert-info[name="longtermhire"]'));
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermHire.Bind($row);
        this.Adder.Bind();
        this.LongTermHire.$Row = $row;
        Helper.BindCreateIndex(this.LongTermHire.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        if (this.Info) { this.Info.reset(); }
        this.LongTermHire.Reset();
    },
    Set: function(array, surveyId){
        this.LongTermHire.Set(array, surveyId);
        if(Helper.LogHandler.ValidationActive){
            LongTermHireHelper.LongTermHire.Container.find('tr').each(function(){
                LongTermHireHelper.Validation.Required.Validate($(this));
                LongTermHireHelper.Validation.GreaterThanZero.Validate($(this));
                LongTermHireHelper.Validation.AvgWorkDay.Validate($(this));
                LongTermHireHelper.Validation.LongTerm.Validate($(this));
            })
            CropMarketingHelper.Validation.WorkHourRange.Validate();
            MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
            HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
        }
    },
    LongTermHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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

                long_term_hire.guid = Helper.Guid.Create();
                $row.attr('data-guid', long_term_hire.guid);

                LongTermHireHelper.LongTermHire.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="numberworker"]'));
            Helper.BindFloatOnly($row.find('[name="avgworkday"]'));
            $row.find('input[name="numberworker"]').change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="numberworker"]').map(function(){
                    var parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);

                if(Helper.LogHandler.ValidationActive){
                    LongTermHireHelper.LongTermHire.Container.find('tr').each(function(){
                        LongTermHireHelper.Validation.Required.Validate($(this));
                        LongTermHireHelper.Validation.GreaterThanZero.Validate($(this));
                    })
                    CropMarketingHelper.Validation.WorkHourRange.Validate();
                    MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                }
            })
            $row.find('button[name="remove"]').click(function(){
                if(CloneData){
                    $tr = $(this).closest('tr');
                    $nextAll = $tr.nextAll();
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_hires = CloneData[surveyId].long_term_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        LongTermHireHelper.LongTermHire.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(LongTermHireHelper.Alert, $tr, $nextAll);
                            LongTermHireHelper.Alert.alert();
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                            CropMarketingHelper.Validation.WorkHourRange.Validate();
                            MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                            HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
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
                    obj.avg_work_day = parseFloat($tr.find('[name="avgworkday"]').val());

                    if(Helper.LogHandler.ValidationActive){
                        LongTermHireHelper.Validation.Required.Validate($tr);
                        LongTermHireHelper.Validation.GreaterThanZero.Validate($tr);
                        LongTermHireHelper.Validation.AvgWorkDay.Validate($tr);
                        LongTermHireHelper.Validation.LongTerm.Validate($tr);
                        CropMarketingHelper.Validation.WorkHourRange.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="longtermhire"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = LongTermHireHelper.LongTermHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].long_term_hires.push(obj);

                    $row = LongTermHireHelper.LongTermHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LongTermHireHelper.LongTermHire.Container.append($row);
                    LongTermHireHelper.LongTermHire.Container[0].refreshIndex();
                    if(Helper.LogHandler.ValidationActive){
                        LongTermHireHelper.Validation.Required.Validate($row);
                        SurveyHelper.Hire.Validation.HireExist.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                        HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(3),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermHireHelper.LongTermHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name)
                }
                Helper.LogHandler.Log(!$row.find('[name="worktype"]').val(), LongTermHireHelper.Alert, makeString('主要僱用工作類型'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="sumcount"]').val(), LongTermHireHelper.Alert, makeString('人數'), this.Guids[1], guid, false);
                Helper.LogHandler.Log($row.find('[name="month"]').val().length == 0, LongTermHireHelper.Alert, makeString('僱用月份'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="avgworkday"]').val(), LongTermHireHelper.Alert, makeString('平均每月工作日數'), this.Guids[3], guid, false);
            },
        },
        GreaterThanZero: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermHireHelper.LongTermHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可為0'.format(index, name)
                }
                Helper.LogHandler.Log(parseInt($row.find('[name="sumcount"]').val()) === 0, LongTermHireHelper.Alert, makeString('人數'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(parseFloat($row.find('[name="avgworkday"]').val()) === 0, LongTermHireHelper.Alert, makeString('平均每月工作日數'), this.Guids[1], guid, false);
            },
        },
        AvgWorkDay: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermHireHelper.LongTermHire.Container.find('tr').index($row) + 1;
                var avgWorkDay = $row.find('[name="avgworkday"]').val();
                var con = avgWorkDay > 30;
                var msg = '第<i class="row-index">{0}</i>列每月工作日數應小於30日'.format(index);
                Helper.LogHandler.Log(con, LongTermHireHelper.Alert, msg, this.Guids[0], guid, false);

                var con = avgWorkDay > 26;
                var msg = '第<i class="row-index">{0}</i>列平均每月工作日數大於26日，請確認其合理性'.format(index);
                Helper.LogHandler.Log(con, LongTermHireHelper.Info, msg, this.Guids[1], guid, false);
            },
        },
        LongTerm: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermHireHelper.LongTermHire.Container.find('tr').index($row) + 1;
                var con = $row.find('[name="month"]').val().length < 6;
                var msg = '第<i class="row-index">{0}</i>列填列之月份應大於等於6個月'.format(index);
                Helper.LogHandler.Log(con, LongTermHireHelper.Alert, msg, this.Guids[0], guid);
            }
        },
    },
}
var ShortTermHireHelper = {
    Alert: null,
    Info: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="shorttermhire"]'));
        this.Info = new Helper.Alert($('.alert-info[name="shorttermhire"]'));
        var $row = $(row);
        $row.find('select[name="worktype"]').attr('multiple', '');
        this.ShortTermHire.Bind($row);
        this.Adder.Bind();
        this.ShortTermHire.$Row = $row;
        Helper.BindCreateIndex(this.ShortTermHire.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        if (this.Info) { this.Info.reset(); }
        this.ShortTermHire.Reset();
    },
    Set: function(array){
        this.ShortTermHire.Set(array);
        if(Helper.LogHandler.ValidationActive){
            ShortTermHireHelper.ShortTermHire.Container.find('tr').each(function(){
                ShortTermHireHelper.Validation.Required.Validate($(this));
                ShortTermHireHelper.Validation.GreaterThanZero.Validate($(this));
                ShortTermHireHelper.Validation.AvgWorkDay.Validate($(this));
            })
            ShortTermHireHelper.Validation.Over6Month.Validate();
            CropMarketingHelper.Validation.WorkHourRange.Validate();
            MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
            HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
        }
    },
    ShortTermHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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

                short_term_hire.guid = Helper.Guid.Create();
                $row.attr('data-guid', short_term_hire.guid);

                ShortTermHireHelper.ShortTermHire.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindFloatOnly($row.find('[name="avgworkday"]'));
            $row.find('input[name="numberworker"]').change(function(){
                var sumCount = 0;
                $(this).closest('tr').find('input[name="numberworker"]').map(function(){
                    var parse = parseInt($(this).val());
                    if(parse == $(this).val()) sumCount += parse;
                })
                $(this).closest('tr').find('input[name="sumcount"]').val(sumCount);

                if(Helper.LogHandler.ValidationActive){
                    ShortTermHireHelper.ShortTermHire.Container.find('tr').each(function(){
                        ShortTermHireHelper.Validation.Required.Validate($(this));
                        ShortTermHireHelper.Validation.GreaterThanZero.Validate($(this));
                    })
                    CropMarketingHelper.Validation.WorkHourRange.Validate();
                    MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                }

            })
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                $nextAll = $tr.nextAll();
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].short_term_hires = CloneData[MainSurveyId].short_term_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        ShortTermHireHelper.ShortTermHire.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(ShortTermHireHelper.Alert, $tr, $nextAll);
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                            ShortTermHireHelper.Validation.Over6Month.Validate();
                            CropMarketingHelper.Validation.WorkHourRange.Validate();
                            MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                            HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
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

                    obj.work_types = $tr.find('[name="worktype"]').val();
                    obj.number_workers = SurveyHelper.NumberWorker.Object.Collect($tr.find('[name="numberworker"]'));
                    obj.month = parseInt($tr.find('[name="month"]').val());
                    obj.avg_work_day = parseFloat($tr.find('[name="avgworkday"]').val());

                    if(Helper.LogHandler.ValidationActive){
                        ShortTermHireHelper.Validation.Required.Validate($tr);
                        ShortTermHireHelper.Validation.GreaterThanZero.Validate($tr);
                        ShortTermHireHelper.Validation.AvgWorkDay.Validate($tr);
                        CropMarketingHelper.Validation.WorkHourRange.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="shorttermhire"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = ShortTermHireHelper.ShortTermHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].short_term_hires.push(obj);

                    $row = ShortTermHireHelper.ShortTermHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    ShortTermHireHelper.ShortTermHire.Container.append($row);
                    ShortTermHireHelper.ShortTermHire.Container[0].refreshIndex();
                    if(Helper.LogHandler.ValidationActive){
                        ShortTermHireHelper.Validation.Required.Validate($row);
                        ShortTermHireHelper.Validation.GreaterThanZero.Validate($row);
                        ShortTermHireHelper.Validation.Over6Month.Validate();
                        SurveyHelper.Hire.Validation.HireExist.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                        HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(3),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermHireHelper.ShortTermHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name);
                }
                Helper.LogHandler.Log(!$row.find('[name="month"]').val(), ShortTermHireHelper.Alert, makeString('僱用月份'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="sumcount"]').val(), ShortTermHireHelper.Alert, makeString('人數'), this.Guids[1], guid, false);
                Helper.LogHandler.Log($row.find('[name="worktype"]').val().length == 0, ShortTermHireHelper.Alert, makeString('主要僱用工作類型'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="avgworkday"]').val(), ShortTermHireHelper.Alert, makeString('平均每月工作日數'), this.Guids[3], guid, false);
            },
        },
        GreaterThanZero: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermHireHelper.ShortTermHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可為0'.format(index, name)
                }
                Helper.LogHandler.Log(parseInt($row.find('[name="sumcount"]').val()) === 0, ShortTermHireHelper.Alert, makeString('人數'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(parseFloat($row.find('[name="avgworkday"]').val()) === 0, ShortTermHireHelper.Alert, makeString('平均每月工作日數'), this.Guids[1], guid, false);
            },
        },
        AvgWorkDay: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermHireHelper.ShortTermHire.Container.find('tr').index($row) + 1;
                var avgWorkDay = $row.find('[name="avgworkday"]').val();
                var con = avgWorkDay > 30;
                var msg = '第<i class="row-index">{0}</i>列平均每月工作日數應小於30日'.format(index);
                Helper.LogHandler.Log(con, ShortTermHireHelper.Alert, msg, this.Guids[0], guid, false);

                var con = avgWorkDay > 25;
                var msg = '第<i class="row-index">{0}</i>列平均每月工作日數大於25日，請確認其合理性'.format(index);
                Helper.LogHandler.Log(con, ShortTermHireHelper.Info, msg, this.Guids[1], guid, false);
            },
        },
        Over6Month: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var length = ShortTermHireHelper.ShortTermHire.Container.find('tr').length;
                var con = length >= 6;
                var msg = '填列之月份超過6個月，請確認是否為常僱而非臨時工，並於備註說明';
                Helper.LogHandler.Log(con, ShortTermHireHelper.Info, msg, this.Guids[0], null, false);
            },
        },
    },
}
var NoSalaryHireHelper = {
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="nosalaryhire"]'));
        var $row = $(row);
        $row.find('select[name="month"]');
        this.NoSalaryHire.Bind($row);
        this.Adder.Bind();
        this.NoSalaryHire.$Row = $row;
        Helper.BindCreateIndex(this.NoSalaryHire.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        this.NoSalaryHire.Reset();
    },
    Set: function(array){
        this.NoSalaryHire.Set(array);
        if(Helper.LogHandler.ValidationActive){
            NoSalaryHireHelper.NoSalaryHire.Container.find('tr').each(function(){
                NoSalaryHireHelper.Validation.Required.Validate($(this));
                NoSalaryHireHelper.Validation.AvgWorkDay.Validate($(this));
            })
        }
    },
    NoSalaryHire: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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
                $row.find('input[name="avgworkday"]').val(no_salary_hire.avg_work_day);

                no_salary_hire.guid = Helper.Guid.Create();
                $row.attr('data-guid', no_salary_hire.guid);

                NoSalaryHireHelper.NoSalaryHire.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="count"]'));
            Helper.BindFloatOnly($row.find('[name="avgworkday"]'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                $nextAll = $tr.nextAll();
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        CloneData[MainSurveyId].no_salary_hires = CloneData[MainSurveyId].no_salary_hires.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        NoSalaryHireHelper.NoSalaryHire.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(NoSalaryHireHelper.Alert, $tr, $nextAll);
                            SurveyHelper.Hire.Validation.HireExist.Validate();
                            HireChannelHelper.Validation.ConflictToNoSalaryHire.Validate();
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
                    obj.avg_work_day = parseFloat($tr.find('[name="avgworkday"]').val());

                    if(Helper.LogHandler.ValidationActive){
                        NoSalaryHireHelper.Validation.Required.Validate($tr);
                        NoSalaryHireHelper.Validation.AvgWorkDay.Validate($tr);
                        SurveyHelper.Hire.Validation.HireExist.Validate();
                        CropMarketingHelper.Validation.WorkHourRange.Validate();
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="nosalaryhire"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = NoSalaryHireHelper.NoSalaryHire.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].no_salary_hires.push(obj);

                    $row = NoSalaryHireHelper.NoSalaryHire.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    NoSalaryHireHelper.NoSalaryHire.Container.append($row);
                    NoSalaryHireHelper.NoSalaryHire.Container[0].refreshIndex();
                    if(Helper.LogHandler.ValidationActive){
                        NoSalaryHireHelper.Validation.Required.Validate($row);
                        HireChannelHelper.Validation.ConflictToNoSalaryHire.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = NoSalaryHireHelper.NoSalaryHire.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name)
                }
                Helper.LogHandler.Log(!$row.find('[name="month"]').val(), NoSalaryHireHelper.Alert, makeString('月份'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="count"]').val(), NoSalaryHireHelper.Alert, makeString('人數'), this.Guids[1], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="avgworkday"]').val(), NoSalaryHireHelper.Alert, makeString('平均每月工作日數'), this.Guids[3], guid, false);
            },
        },
        AvgWorkDay: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = NoSalaryHireHelper.NoSalaryHire.Container.find('tr').index($row) + 1;
                var avgWorkDay = $row.find('[name="avgworkday"]').val();
                var con = avgWorkDay > 30 || avgWorkDay == 0;
                var msg = '第<i class="row-index">{0}</i>列每月工作日數應小於30日，且不得為0'.format(index);
                Helper.LogHandler.Log(con, NoSalaryHireHelper.Alert, msg, this.Guids[0], guid, false);
            },
        },
    },
}
var LongTermLackHelper = {
    Info: null,
    Alert: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="longtermlack"]'));
        this.Info = new Helper.Alert($('.alert-info[name="longtermlack"]'));
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.LongTermLack.Bind($row);
        this.Adder.Bind();
        this.LongTermLack.$Row = $row;
        Helper.BindCreateIndex(this.LongTermLack.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        if (this.Info) { this.Info.reset(); }
        this.LongTermLack.Reset();
    },
    Set: function(array, surveyId){
        this.LongTermLack.Set(array, surveyId);
        if(Helper.LogHandler.ValidationActive){
            LongTermLackHelper.LongTermLack.Container.find('tr').each(function(){
                LongTermLackHelper.Validation.Required.Validate($(this));
                LongTermLackHelper.Validation.GreaterThanZero.Validate($(this));
                LongTermLackHelper.Validation.AvgLackDay.Validate($(this));
                LongTermLackHelper.Validation.LongTerm.Validate($(this));
            })
        }
    },
    LongTermLack: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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
                $row.find('input[name="avglackday"]').val(long_term_lack.avg_lack_day);
                $row.attr('data-survey-id', surveyId);

                long_term_lack.guid = Helper.Guid.Create();
                $row.attr('data-guid', long_term_lack.guid);

                LongTermLackHelper.LongTermLack.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="count"]'));
            Helper.BindFloatOnly($row.find('[name="avglackday"]'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                $nextAll = $tr.nextAll();
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].long_term_lacks = CloneData[surveyId].long_term_lacks.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        LongTermLackHelper.LongTermLack.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(LongTermLackHelper.Alert, $tr, $nextAll);
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
                    obj.avg_lack_day = parseFloat($tr.find('[name="avglackday"]').val());

                    if(Helper.LogHandler.ValidationActive){
                        LongTermLackHelper.Validation.Required.Validate($tr);
                        LongTermLackHelper.Validation.GreaterThanZero.Validate($tr);
                        LongTermLackHelper.Validation.AvgLackDay.Validate($tr);
                        LongTermLackHelper.Validation.LongTerm.Validate($tr);
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="longtermlack"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = LongTermLackHelper.LongTermLack.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].long_term_lacks.push(obj);

                    $row = LongTermLackHelper.LongTermLack.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    LongTermLackHelper.LongTermLack.Container.append($row);
                    LongTermLackHelper.LongTermLack.Container[0].refreshIndex();
                    if(Helper.LogHandler.ValidationActive){
                        LongTermLackHelper.Validation.Required.Validate($row);
                        LongTermLackHelper.Validation.GreaterThanZero.Validate($row);
                        LongTermLackHelper.Validation.AvgLackDay.Validate($row);
                        SurveyHelper.Lack.Validation.LackExist.Validate();
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(3),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermLackHelper.LongTermLack.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name)
                }
                Helper.LogHandler.Log(!$row.find('[name="worktype"]').val(), LongTermLackHelper.Alert, makeString('主要短缺工作類型'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="count"]').val(), LongTermLackHelper.Alert, makeString('人數'), this.Guids[1], guid, false);
                Helper.LogHandler.Log($row.find('[name="month"]').val().length == 0, LongTermLackHelper.Alert, makeString('缺工月份'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="avglackday"]').val(), LongTermLackHelper.Alert, makeString('平均每月短缺日數'), this.Guids[3], guid, false);
            },
        },
        GreaterThanZero: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermLackHelper.LongTermLack.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可為0'.format(index, name)
                }
                Helper.LogHandler.Log(parseInt($row.find('[name="count"]').val()) === 0, LongTermLackHelper.Alert, makeString('人數'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(parseFloat($row.find('[name="avglackday"]').val()) === 0, LongTermLackHelper.Alert, makeString('平均每月短缺日數'), this.Guids[1], guid, false);
            },
        },
        AvgLackDay: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermLackHelper.LongTermLack.Container.find('tr').index($row) + 1;
                var avgLackDay = $row.find('[name="avglackday"]').val();
                var con = avgLackDay > 30;
                var msg = '第<i class="row-index">{0}</i>列平均每月短缺日數應小於等於30'.format(index);
                Helper.LogHandler.Log(con, LongTermLackHelper.Alert, msg, this.Guids[0], guid);

                con = avgLackDay > 25;
                msg = '第<i class="row-index">{0}</i>列平均每月短缺日數大於25日，請確認其合理性'.format(index);
                Helper.LogHandler.Log(con, LongTermLackHelper.Info, msg, this.Guids[1], guid, false);
            }
        },
        LongTerm: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = LongTermLackHelper.LongTermLack.Container.find('tr').index($row) + 1;
                var con = $row.find('[name="month"]').val().length < 6;
                var msg = '第<i class="row-index">{0}</i>列填列之月份應大於等於6個月'.format(index);
                Helper.LogHandler.Log(con, LongTermLackHelper.Alert, msg, this.Guids[0], guid);
            }
        },
    },
}
var ShortTermLackHelper = {
    Alert: null,
    Info: null,
    Setup: function(row){
        this.Alert = new Helper.Alert($('.alert-danger[name="shorttermlack"]'));
        this.Info = new Helper.Alert($('.alert-info[name="shorttermlack"]'));
        $row = $(row);
        $row.find('select[name="month"]').attr('multiple', '');
        this.ShortTermLack.Bind($row);
        this.Adder.Bind();
        this.ShortTermLack.$Row = $row;
        Helper.BindCreateIndex(this.ShortTermLack.Container);
    },
    Reset: function () {
        if (this.Alert) { this.Alert.reset(); }
        if (this.Info) { this.Info.reset(); }
        this.ShortTermLack.Reset();
    },
    Set: function(array, surveyId){
        this.ShortTermLack.Set(array, surveyId);
        if(Helper.LogHandler.ValidationActive){
            ShortTermLackHelper.ShortTermLack.Container.find('tr').each(function(){
                ShortTermLackHelper.Validation.Required.Validate($(this));
                ShortTermLackHelper.Validation.GreaterThanZero.Validate($(this));
                ShortTermLackHelper.Validation.AvgLackDay.Validate($(this));
                ShortTermLackHelper.Validation.Over6Month.Validate($(this));
                ShortTermLackHelper.Validation.MatchProduct.Validate($(this));
            })
        }
    },
    ShortTermLack: {
        Object: {
            New: function(surveyId, guid){
                guid = guid || null;
                return {
                    survey: surveyId,
                    guid: guid ? guid : Helper.Guid.Create(),
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
                $row.find('input[name="avglackday"]').val(short_term_lack.avg_lack_day);
                $row.find('input[name="name"]').val(short_term_lack.name);

                $row.attr('data-survey-id', surveyId);

                short_term_lack.guid = Helper.Guid.Create();
                $row.attr('data-guid', short_term_lack.guid);

                ShortTermLackHelper.ShortTermLack.Container.append($row);
            })
            this.Container[0].refreshIndex();
        },
        Reset: function() {
            this.Container.html('');
        },
        Bind: function($row){
            Helper.BindIntegerOnly($row.find('[name="count"]'));
            Helper.BindFloatOnly($row.find('[name="avglackday"]'));
            $row.find('button[name="remove"]').click(function(){
                $tr = $(this).closest('tr');
                $nextAll = $tr.nextAll();
                if(CloneData){
                    $.when($.Deferred(Helper.Dialog.DeleteRow)).then(function(){
                        var surveyId = $tr.data('survey-id');
                        CloneData[surveyId].short_term_lacks = CloneData[surveyId].short_term_lacks.filter(function(obj){
                            return obj.guid != $tr.data('guid');
                        })
                        $tr.remove();
                        ShortTermLackHelper.ShortTermLack.Container[0].refreshIndex();
                        if(Helper.LogHandler.ValidationActive){
                            Helper.LogHandler.DeleteRow(ShortTermLackHelper.Alert, $tr, $nextAll);
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
                    obj.work_type = parseInt($tr.find('[name="worktype"]').val());
                    obj.months = $tr.find('[name="month"]').val();
                    obj.count = parseInt($tr.find('[name="count"]').val());
                    obj.avg_lack_day = parseFloat($tr.find('[name="avglackday"]').val());
                    obj.name = $tr.find('[name="name"]').val();

                    if(Helper.LogHandler.ValidationActive){
                         ShortTermLackHelper.Validation.Required.Validate($tr);
                         ShortTermLackHelper.Validation.GreaterThanZero.Validate($tr);
                         ShortTermLackHelper.Validation.AvgLackDay.Validate($tr);
                         ShortTermLackHelper.Validation.Over6Month.Validate($tr);
                         ShortTermLackHelper.Validation.MatchProduct.Validate($tr);
                    }
                }
            })
            return $row;
        },
    },
    Adder: {
        Container: $('.js-add-row[name="shorttermlack"]'),
        Bind: function(){
            this.Container.unbind('click.ns1').on('click.ns1', function(){
                if(CloneData && MainSurveyId){
                    obj = ShortTermLackHelper.ShortTermLack.Object.New(MainSurveyId);
                    CloneData[MainSurveyId].short_term_lacks.push(obj);

                    $row = ShortTermLackHelper.ShortTermLack.$Row.clone(true, true);
                    $row.attr('data-guid', obj.guid);
                    $row.find('select').selectpicker();
                    $row.attr('data-survey-id', MainSurveyId);
                    ShortTermLackHelper.ShortTermLack.Container.append($row);
                    ShortTermLackHelper.ShortTermLack.Container[0].refreshIndex();
                    if(Helper.LogHandler.ValidationActive){
                        ShortTermLackHelper.Validation.Required.Validate($row);
                        ShortTermLackHelper.Validation.GreaterThanZero.Validate($row);
                        ShortTermLackHelper.Validation.AvgLackDay.Validate($row);
                    }
                }
            })
        },
    },
    Validation: {
        Required: {
            Guids: Helper.Guid.CreateMulti(5),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermLackHelper.ShortTermLack.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可空白'.format(index, name)
                }
                Helper.LogHandler.Log(!$row.find('[name="product"]').val(), ShortTermLackHelper.Alert, makeString('農畜產品代碼'), this.Guids[0], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="name"]').val(), ShortTermLackHelper.Alert, makeString('農畜產品名稱'), this.Guids[1], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="worktype"]').val(), ShortTermLackHelper.Alert, makeString('主要短缺工作類型'), this.Guids[2], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="count"]').val(), ShortTermLackHelper.Alert, makeString('人數'), this.Guids[3], guid, false);
                Helper.LogHandler.Log($row.find('[name="month"]').val().length == 0, ShortTermLackHelper.Alert, makeString('缺工月份'), this.Guids[4], guid, false);
                Helper.LogHandler.Log(!$row.find('[name="avglackday"]').val(), ShortTermLackHelper.Alert, makeString('平均每月短缺日數'), this.Guids[5], guid, false);
            },
        },
        GreaterThanZero: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermLackHelper.ShortTermLack.Container.find('tr').index($row) + 1;
                function makeString(name){
                    return '第<i class="row-index">{0}</i>列{1}不可為0'.format(index, name)
                }
                Helper.LogHandler.Log(parseInt($row.find('[name="count"]').val()) == 0, ShortTermLackHelper.Alert, makeString('人數'), this.Guids[0], guid, false);
                Helper.LogHandler.Log($row.find('[name="avglackday"]').val() == 0, ShortTermLackHelper.Alert, makeString('平均每月短缺日數'), this.Guids[1], guid, false);
            },
        },
        AvgLackDay: {
            Guids: Helper.Guid.CreateMulti(1),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermLackHelper.ShortTermLack.Container.find('tr').index($row) + 1;
                var avgLackDay = $row.find('[name="avglackday"]').val();
                var con = avgLackDay > 30;
                var msg = '第<i class="row-index">{0}</i>列平均每月短缺日數應小於等於30'.format(index);
                Helper.LogHandler.Log(con, ShortTermLackHelper.Alert, msg, this.Guids[0], guid);

                con = avgLackDay > 25;
                msg = '第<i class="row-index">{0}</i>列平均每月短缺日數大於25日，請確認其合理性'.format(index);
                Helper.LogHandler.Log(con, ShortTermLackHelper.Info, msg, this.Guids[1], guid, false);
            }
        },
        Over6Month: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermLackHelper.ShortTermLack.Container.find('tr').index($row) + 1;
                var msg = '第<i class="row-index">{0}</i>列填列之月份超過6個月，請確認是否為常僱而非臨時工，並於備註說明'.format(index);
                var con = $row.find('[name="month"]').val().length >= 6;
                Helper.LogHandler.Log(con, ShortTermLackHelper.Info, msg, this.Guids[0], guid, false);
            },
        },
        MatchProduct: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function($row){
                var guid = $row.data('guid');
                var index = ShortTermLackHelper.ShortTermLack.Container.find('tr').index($row) + 1;
                var selectedProduct = $row.find('[name="product"] > option:selected').data("code");
                cropMatch = false;
                livestockMatch = false;
                CropMarketingHelper.CropMarketing.Container.find('tr').each(function(){
                    var $product = $(this).find('[name="product"] > option[data-name]:selected');
                    if($product.length == 0) return true; // continue
                    val = $product.data("code");
                    if(selectedProduct == val){
                        cropMatch = true;
                        return false;  // break
                    }
                })
                LivestockMarketingHelper.LivestockMarketing.Container.find('tr').each(function(){
                    var $product = $(this).find('[name="product"] > option[data-name]:selected');
                    if($product.length == 0) return true; // continue
                    val = $product.data("code");
                    if(selectedProduct == val){
                        livestockMatch = true;
                        return false;  // break
                    }
                })
                var con = !(cropMatch || livestockMatch);
                var msg = '第<i class="row-index">{0}</i>列農畜產品代碼應有對應【問項1.4或1.5】生產之農畜產品。'.format(index);
                Helper.LogHandler.Log(con, ShortTermLackHelper.Alert, msg, this.Guids[0], guid);
            }
        },
    },
}
var SubsidyHelper = {
    Alert: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="subsidy"]'));
        this.Bind();
    },
    Container: {
        Apply: $('#panel4 input[name="apply"'),
        Refuse: $('#panel4 input[name="refuse"]'),
        Extra: $('#panel4 input[name="extra"]'),
        ApplyMethod: $('#panel4 .apply-method'),
    },
    Set: function(obj){
        obj.applies.forEach(function(apply, i){
            SubsidyHelper.Container.Apply
            .filter('[ data-result-id="{0}"]'.format(apply.result))
            .filter('[ data-method-id="{0}"]'.format(apply.method))
            .attr('data-apply-id', apply.id)
            .prop('checked', true);
        })
        obj.refuses.forEach(function(refuse, i){
            SubsidyHelper.Container.Refuse
            .filter('[ data-reason-id="{0}"]'.format(refuse.reason))
            .filter('[ data-method-id="{0}"]'.format(refuse.method))
            .attr('data-refuse-id', refuse.id)
            .prop('checked', true);

            SubsidyHelper.Container.Extra
            .filter('[ data-reason-id="{0}"]'.format(refuse.reason))
            .filter('[ data-method-id="{0}"]'.format(refuse.method))
            .attr('data-refuse-id', refuse.id)
            .val(refuse.extra);
        })
        if(Helper.LogHandler.ValidationActive){
            SubsidyHelper.Validation.Empty.Validate();
            SubsidyHelper.Validation.Duplicate.Validate();
            SubsidyHelper.Validation.HasLack.Validate();
            HireChannelHelper.Validation.ConflictToApply.Validate();
        }
    },
    Reset: function(){
        if (this.Alert) { this.Alert.reset(); }
        this.Container.Apply.prop('checked', false);
        this.Container.Apply.attr('data-apply-id', '');
        this.Container.Refuse.prop('checked', false);
        this.Container.Refuse.attr('data-refuse-id', '');
        this.Container.Extra.val('');
        this.Container.Extra.attr('data-refuse-id', '');
    },
    Bind: function(){
        this.Container.Apply.unbind('change.ns1').on('change.ns1', function(e){
            SubsidyHelper.Object.Apply.Collect();
            if(CloneData){
                if(Helper.LogHandler.ValidationActive){
                    SubsidyHelper.Validation.Empty.Validate();
                    SubsidyHelper.Validation.Duplicate.Validate();
                    SubsidyHelper.Validation.HasLack.Validate();
                    HireChannelHelper.Validation.ConflictToApply.Validate();
                }
            }
        })
        this.Container.Refuse.unbind('change.ns1').on('change.ns1', function(e){
            SubsidyHelper.Object.Refuse.Collect();
            if(CloneData){
                if(Helper.LogHandler.ValidationActive){
                    SubsidyHelper.Validation.Empty.Validate();
                    SubsidyHelper.Validation.Duplicate.Validate();
                    SubsidyHelper.Validation.HasLack.Validate();
                }
            }
        })
        this.Container.Extra.unbind('change.ns1').on('change.ns1', function(e){
            /* make sure checked before change textbox value */
            var reasonId = $(this).data('reason-id');
            var methodId = $(this).data('method-id');
            var checked = SubsidyHelper.Container.Refuse
                          .filter('[data-reason-id="{0}"]'.format(reasonId))
                          .filter('[data-method-id="{0}"]'.format(methodId))
                          .prop('checked');
            if(!checked && $(this).val() != ""){
                Helper.Dialog.ShowAlert('您尚未勾選無申請之原因');
                e.preventDefault();
            }
            SubsidyHelper.Object.Refuse.Collect();
            if(CloneData){
                if(Helper.LogHandler.ValidationActive){
                    SubsidyHelper.Validation.Empty.Validate();
                }
            }
        })
    },
    Object: {
        Apply: {
            New: function(resultId, methodId, id){
                var obj = {
                    result: resultId,
                    method: methodId,
                }
                if(id) obj.id = id;
                return obj;
            },
            Collect: function(){
                if(CloneData){
                    var applies = [];
                    SubsidyHelper.Container.Apply
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('apply-id');
                        var resultId = $(this).data('result-id');
                        var methodId = $(this).data('method-id');
                        applies.push(
                            SubsidyHelper.Object.Apply.New(resultId, methodId, id ? id : null)
                        )
                    })
                    CloneData[MainSurveyId].subsidy.applies = applies;
                }
            },
        },
        Refuse: {
            New: function(reasonId, methodId, extra, id){
                var obj = {
                    reason: reasonId,
                    method: methodId,
                    extra: extra,
                }
                if(id) obj.id = id;
                return obj;
            },
            Collect: function(){
                if(CloneData){
                    var refuses = [];
                    SubsidyHelper.Container.Refuse
                    .filter(':checked')
                    .each(function(){
                        var id = $(this).data('refuse-id');
                        var reasonId = $(this).data('reason-id');
                        var methodId = $(this).data('method-id');
                        var extra = SubsidyHelper.Container.Extra
                                    .filter('[data-reason-id="{0}"]'.format(reasonId))
                                    .filter('[data-method-id="{0}"]'.format(methodId))
                                    .val();
                        refuses.push(
                            SubsidyHelper.Object.Refuse.New(reasonId, methodId, extra, id ? id : null)
                        )
                    })
                    CloneData[MainSurveyId].subsidy.refuses = refuses;
                }
            },
        }
    },
    Validation: {
        Empty: {
            Guids: Helper.Guid.CreateMulti(5),
            Validate: function(){
                // check refuse reason.id=0
                SubsidyHelper.Container.ApplyMethod.each(function(i, element){
                    var methodId = $(this).data("method-id");
                    var name = $(this).text();
                    var hasReason0Refuse = SubsidyHelper.Container.Refuse
                                           .filter('[data-method-id="{0}"]'.format(methodId))
                                           .filter('[data-reason-id="0"]')
                                           .filter(':checked').length > 0;
                    var hasOtherRefuse = SubsidyHelper.Container.Refuse
                                         .filter('[data-method-id="{0}"]'.format(methodId))
                                         .not('[data-reason-id="0"]')
                                         .filter(':checked').length > 0;
                    var hasApply = SubsidyHelper.Container.Apply
                                   .filter('[data-method-id="{0}"]'.format(methodId))
                                   .filter(':checked').length > 0;
                    var con = (hasReason0Refuse && hasOtherRefuse) || (hasReason0Refuse && hasApply);
                    var msg = '{0}: 勾選「沒聽過」，有聽過處應為空白'.format(name);
                    Helper.LogHandler.Log(con, SubsidyHelper.Alert, msg, SubsidyHelper.Validation.Empty.Guids[i], null, false);
                })
                // check all empty
                SubsidyHelper.Container.ApplyMethod.each(function(i, element){
                    var methodId = $(this).data("method-id");
                    var name = $(this).text();
                    var hasApply = SubsidyHelper.Container.Apply
                                   .filter(':checked')
                                   .filter('[data-method-id="{0}"]'.format(methodId)).length > 0;
                    var hasRefuse = SubsidyHelper.Container.Refuse
                                    .filter(':checked')
                                    .filter('[data-method-id="{0}"]'.format(methodId)).length > 0;
                    var con = !hasApply && !hasRefuse;
                    var msg = "{0}: 不可漏填".format(name);
                    Helper.LogHandler.Log(con, SubsidyHelper.Alert, msg, SubsidyHelper.Validation.Empty.Guids[3 + i], null, false);
                })

                // check extra
                var con = false;
                SubsidyHelper.Container.Extra.each(function() {
                    var reasonId = $(this).data('reason-id');
                    var methodId = $(this).data('method-id');
                    refuseChecked = SubsidyHelper.Container.Refuse
                                    .filter(':checked')
                                    .filter('[data-reason-id="{0}"]'.format(reasonId))
                                    .filter('[data-method-id="{0}"]'.format(methodId)).length == 1;
                    hasText = $(this).val() != "";
                    if (hasText && !refuseChecked || refuseChecked && !hasText) {
                        con = true;
                    }
                });
                var msg = '「沒有申請」原因不可為空白';
                Helper.LogHandler.Log(con, SubsidyHelper.Alert, msg, this.Guids[5], null, false);
            },
        },
        Duplicate: {
            Guids: Helper.Guid.CreateMulti(5),
            Validate: function(){
                // check apply and refuse duplicate
                SubsidyHelper.Container.ApplyMethod.each(function(i, element){
                    var methodId = $(this).data("method-id");
                    var name = $(this).text();
                    var hasApply = SubsidyHelper.Container.Apply
                                   .filter('[data-method-id="{0}"]'.format(methodId))
                                   .filter(':checked').length > 0;
                    var hasRefuse = SubsidyHelper.Container.Refuse
                                    .filter('[data-method-id="{0}"]'.format(methodId))
                                    .filter(':checked').not('[data-reason-id="0"]').length > 0;
                    con = hasApply && hasRefuse;
                    var msg = '{0}:「有申請」、「沒有申請」不得重複勾選'.format(name);
                    Helper.LogHandler.Log(con, SubsidyHelper.Alert, msg, SubsidyHelper.Validation.Duplicate.Guids[i], null, false);
                });
                // check apply result distinct
                SubsidyHelper.Container.ApplyMethod.each(function(i, element){
                    var methodId = $(this).data("method-id");
                    var name = $(this).text();
                    var con = SubsidyHelper.Container.Apply
                              .filter('[data-method-id="{0}"]'.format(methodId))
                              .filter(':checked').length > 1;
                     var msg = '{0}:「有申請」情形限註記一項'.format(name);
                    Helper.LogHandler.Log(con, SubsidyHelper.Alert, msg,
                                          SubsidyHelper.Validation.Duplicate.Guids[i + 3], null, false);
                });
            },
        },
        HasLack: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var hasReason1Refuse = SubsidyHelper.Container.Refuse
                                       .filter('[data-reason-id="1"]')
                                       .filter(':checked').length > 0;
                var lackChecked = SurveyHelper.Lack.Container.filter('input:checked');
                var con = hasReason1Refuse && lackChecked.length == 1 && lackChecked.data('lackId') == 4;
                var msg = '【問項4.1】有勾選「無缺工」，【問項3.4】不可勾選「113年有缺工」';
                Helper.LogHandler.Log(con, SubsidyHelper.Alert, msg, this.Guids[0], null, false);
            }
        },
    },
}
var HireChannelHelper = {
    Alert: null,
    Info: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="hirechannel"]'));
        this.Info = new Helper.Alert($('.alert-info[name="hirechannel"]'));
        this.HireChannelItems.Bind();
        this.Extra.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         if (this.Info) { this.Info.reset(); }
         this.HireChannelItems.Reset();
         this.Extra.Reset();
    },
    Set: function(array){
        this.HireChannelItems.Set(array);
        this.Extra.Set(array);
    },
    HireChannelItems: {
        Container: $('#panel4 input[name="hirechannelitem"]'),
        Set: function(array){
            array.forEach(function(hireChannel, i){
                HireChannelHelper.HireChannelItems.Container
                .filter('[data-hirechannelitem-id="{0}"]'.format(hireChannel.item))
                .prop('checked', true);
            })
            if(Helper.LogHandler.ValidationActive){
                HireChannelHelper.Validation.Empty.Validate();
                HireChannelHelper.Validation.Duplicate.Validate();
                HireChannelHelper.Validation.ConflictToHire.Validate();
                HireChannelHelper.Validation.ConflictToNoSalaryHire.Validate();
                HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
                HireChannelHelper.Validation.ConflictToApply.Validate();
                HireChannelHelper.Validation.ConflictHasFarmOutSource.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                var checked = $(this).prop('checked');
                var hireChannelItemId = $(this).data('hirechannelitem-id');
                if(!checked){
                    HireChannelHelper.Extra.Container
                    .filter('[data-hirechannelitem-id="{0}"]'.format(hireChannelItemId))
                    .val('');
                }
                if(CloneData){
                    HireChannelHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        HireChannelHelper.Validation.Empty.Validate();
                        HireChannelHelper.Validation.Duplicate.Validate();
                        HireChannelHelper.Validation.ConflictToHire.Validate();
                        HireChannelHelper.Validation.ConflictToNoSalaryHire.Validate();
                        HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
                        HireChannelHelper.Validation.ConflictToApply.Validate();
                        HireChannelHelper.Validation.ConflictHasFarmOutSource.Validate();
                    }
                }
            })
        },
    },
    Extra: {
        Container: $('#panel4 input[name="hirechannelitem-extra"]'),
        Set: function(array){
            array.forEach(function(hireChannel, i){
                HireChannelHelper.Extra.Container
                .filter('[data-hirechannelitem-id="{0}"]'.format(hireChannel.item))
                .val(hireChannel.extra);
            })
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    HireChannelHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        HireChannelHelper.Validation.Empty.Validate();
                        HireChannelHelper.Validation.Duplicate.Validate();
                        HireChannelHelper.Validation.ConflictToHire.Validate();
                        HireChannelHelper.Validation.ConflictToNoSalaryHire.Validate();
                        HireChannelHelper.Validation.ConflictToLongShortTermHire.Validate();
                        HireChannelHelper.Validation.ConflictToApply.Validate();
                        HireChannelHelper.Validation.ConflictHasFarmOutSource.Validate();
                    }
                }
            })
        },
    },
    Object: {
        New: function(surveyId, hireChannelItemId, extra){
            var obj = {
                survey: surveyId,
                item: hireChannelItemId,
            }
            if(extra) obj.extra = extra;
            return obj;
        },
        Collect: function(){
            hireChannels = []
            HireChannelHelper.HireChannelItems.Container
            .filter(':checked')
            .each(function(){
                var hireChannelItemId = $(this).data('hirechannelitem-id');
                var extra = HireChannelHelper.Extra.Container
                            .filter('[data-hirechannelitem-id="{0}"]'.format(hireChannelItemId)).val();
                hireChannels.push(
                    HireChannelHelper.Object.New(MainSurveyId, hireChannelItemId, extra ? extra : null)
                )
            })
            CloneData[MainSurveyId].hire_channels = hireChannels;
        },
    },
    Validation: {
        Empty: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = CloneData[MainSurveyId].hire_channels.length == 0;
                var msg = '不可漏填此問項';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            }
        },
        Duplicate: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var trueChecked = false;
                var falseChecked = false;
                HireChannelHelper.HireChannelItems.Container
                .filter(':checked')
                .each(function(){
                    var hasChannel = $(this).data('has-channel');
                    if(hasChannel) trueChecked = true;
                    else falseChecked = true;
                })
                var con = trueChecked && falseChecked;
                var msg = '無僱用人力與有僱用人力不可重複勾選';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictToHire: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var nonHireChecked = SurveyHelper.Hire.Container.filter('[data-field="nonhire"]').prop('checked');
                var itemChecked = false;
                HireChannelHelper.HireChannelItems.Container
                .filter(':checked')
                .each(function(){
                    var itemId = $(this).data('hirechannelitem-id');
                    if(itemId == 2 || itemId == 3 || itemId == 4) itemChecked = true;
                    return false;
                })
                var con = itemChecked && nonHireChecked;
                var msg = '若有勾選「2. 自行招募」、「3. 親友介紹」、「4. 非戶內親友或換工」，【問項 3.1】不可勾選「無僱用員工及不支薪資人員」。';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictToNoSalaryHire: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var hasNoSalaryHire = NoSalaryHireHelper.NoSalaryHire.Container.find('tr').length > 0;
                var itemChecked = HireChannelHelper.HireChannelItems.Container.filter('[data-hirechannelitem-id="4"]').prop('checked');
                var con = hasNoSalaryHire && !itemChecked;
                var msg = '若【問項 3.2】有不支薪人員，應有勾選「4. 非戶內親友或換工」。';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictToLongShortTermHire: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var itemChecked = HireChannelHelper.HireChannelItems.Container.filter('[data-hirechannelitem-id="5"]').prop('checked');
                var longTermHireCount = LongTermHireHelper.LongTermHire.Container.find('tr').length;
                var shortTermHireCount = ShortTermHireHelper.ShortTermHire.Container.find('tr').length;
                var noHire = (longTermHireCount + shortTermHireCount) == 0;
                var con = itemChecked && noHire;
                var msg = '若有勾選「5. 政府協助」，【問項 3.1.2~3.1.3】應有填僱用人力。';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictToApply: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var itemChecked = HireChannelHelper.HireChannelItems.Container.filter('[data-hirechannelitem-id="5"]').prop('checked');
                var hasApply = false;
                SubsidyHelper.Container.Apply.filter('[ data-result-id="1"]').each(function(){
                    if($(this).prop("checked")){
                        hasApply = true;
                        return false;
                    }
                })
                var con = !itemChecked && hasApply;
                var msg = '若【問項4.1】註記「有申請到」人力團或農業外籍移工，應有勾選「5.政府協助」。';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictHasFarmOutSource: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var itemChecked = HireChannelHelper.HireChannelItems.Container.filter('[data-hirechannelitem-id="6"]').prop('checked');
                var hasFarmOutSource = SurveyHelper.FarmOutsource.Container.filter('[data-field="hasfarmoutsource"]').filter(':checked').length == 1;
                var con = !itemChecked && hasFarmOutSource;
                var msg = '若【問項3.3】註記有委託農事及畜牧服務業者，應有勾選「6.農事服務業者或工頭」。';
                Helper.LogHandler.Log(con, HireChannelHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
    }
}
var LackResponseHelper = {
    Alert: null,
    Info: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="lackresponse"]'));
        this.Info = new Helper.Alert($('.alert-info[name="lackresponse"]'));
        this.LackResponseItems.Bind();
        this.Extra.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         if (this.Info) { this.Info.reset(); }
         this.LackResponseItems.Reset();
         this.Extra.Reset();
    },
    Set: function(array){
        this.LackResponseItems.Set(array);
        this.Extra.Set(array);
    },
    LackResponseItems: {
        Container: $('#panel4 input[name="lackresponseitem"]'),
        Set: function(array){
            array.forEach(function(lackResponse, i){
                LackResponseHelper.LackResponseItems.Container
                .filter('[data-lackresponseitem-id="{0}"]'.format(lackResponse.item))
                .prop('checked', true);
            })
            if(Helper.LogHandler.ValidationActive){
                LackResponseHelper.Validation.Empty.Validate();
                LackResponseHelper.Validation.Duplicate.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                var checked = $(this).prop('checked');
                var lackResponseItemId = $(this).data('lackresponseitem-id');
                if(!checked){
                    LackResponseHelper.Extra.Container
                    .filter('[data-lackresponseitem-id="{0}"]'.format(lackResponseItemId))
                    .val('');
                }
                if(CloneData){
                    LackResponseHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        LackResponseHelper.Validation.Empty.Validate();
                        LackResponseHelper.Validation.Duplicate.Validate();
                    }
                }
            })
        },
    },
    Extra: {
        Container: $('#panel4 input[name="lackresponseitem-extra"]'),
        Set: function(array){
            array.forEach(function(lackResponse, i){
                LackResponseHelper.Extra.Container
                .filter('[data-lackresponseitem-id="{0}"]'.format(lackResponse.item))
                .val(lackResponse.extra);
            })
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    LackResponseHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        LackResponseHelper.Validation.Empty.Validate();
                        LackResponseHelper.Validation.Duplicate.Validate();
                    }
                }
            })
        },
    },
    Object: {
        New: function(surveyId, lackResponseItemId, extra){
            var obj = {
                survey: surveyId,
                item: lackResponseItemId,
            }
            if(extra) obj.extra = extra;
            return obj;
        },
        Collect: function(){
            lackResponses = []
            LackResponseHelper.LackResponseItems.Container
            .filter(':checked')
            .each(function(){
                var lackResponseItemId = $(this).data('lackresponseitem-id');
                var extra = LackResponseHelper.Extra.Container
                            .filter('[data-lackresponseitem-id="{0}"]'.format(lackResponseItemId)).val();
                lackResponses.push(
                    LackResponseHelper.Object.New(MainSurveyId, lackResponseItemId, extra ? extra : null)
                )
            })
            CloneData[MainSurveyId].lack_responses = lackResponses;
        },
    },
    Validation: {
        Empty: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = CloneData[MainSurveyId].lack_responses.length == 0;
                var msg = '不可漏填此問項';
                Helper.LogHandler.Log(con, LackResponseHelper.Alert, msg, this.Guids[0], null, false);
            }
        },
        Duplicate: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var trueChecked = false;
                var falseChecked = false;
                LackResponseHelper.LackResponseItems.Container
                .filter(':checked')
                .each(function(){
                    var hasChannel = $(this).data('has-response');
                    if(hasChannel) trueChecked = true;
                    else falseChecked = true;
                })
                var con = trueChecked && falseChecked;
                var msg = '勾選「1.從未遇過」，不可同時勾選2.~9.。';
                Helper.LogHandler.Log(con, LackResponseHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
    }
}
var MaxHourlyPayHelper = {
    Alert: null,
    Info: null,
    Setup: function(){
        this.Alert = new Helper.Alert($('.alert-danger[name="maxhourlypay"]'));
        this.Info = new Helper.Alert($('.alert-info[name="maxhourlypay"]'));
        this.MaxHourlyPayItems.Bind();
        this.Extra.Bind();
    },
    Reset: function(){
         if (this.Alert) { this.Alert.reset(); }
         if (this.Info) { this.Info.reset(); }
         this.MaxHourlyPayItems.Reset();
         this.Extra.Reset();
    },
    Set: function(array){
        this.MaxHourlyPayItems.Set(array);
        this.Extra.Set(array);
    },
    MaxHourlyPayItems: {
        Container: $('#panel4 input[name="maxhourlypayitem"]'),
        Set: function(array){
            array.forEach(function(maxHourlyPay, i){
                MaxHourlyPayHelper.MaxHourlyPayItems.Container
                .filter('[data-maxhourlypayitem-id="{0}"]'.format(maxHourlyPay.item))
                .prop('checked', true);
            })
            if(Helper.LogHandler.ValidationActive){
                MaxHourlyPayHelper.Validation.Empty.Validate();
                MaxHourlyPayHelper.Validation.Duplicate.Validate();
                MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
                MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
            }
        },
        Reset: function(){
            this.Container.prop('checked', false);
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                var checked = $(this).prop('checked');
                var maxHourlyPayItemId = $(this).data('maxhourlypayitem-id');
                if(!checked){
                    MaxHourlyPayHelper.Extra.Container
                    .filter('[data-maxhourlypayitem-id="{0}"]'.format(maxHourlyPayItemId))
                    .val('');
                }
                if(CloneData){
                    MaxHourlyPayHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        MaxHourlyPayHelper.Validation.Empty.Validate();
                        MaxHourlyPayHelper.Validation.Duplicate.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                    }
                }
            })
        },
    },
    Extra: {
        Container: $('#panel4 input[name="maxhourlypayitem-extra"]'),
        Set: function(array){
            array.forEach(function(maxHourlyPay, i){
                MaxHourlyPayHelper.Extra.Container
                .filter('[data-maxhourlypayitem-id="{0}"]'.format(maxHourlyPay.item))
                .val(maxHourlyPay.extra);
            })
        },
        Reset: function(){
            this.Container.val('');
        },
        Bind: function(){
            this.Container.unbind('change.ns1').on('change.ns1', function(){
                if(CloneData){
                    MaxHourlyPayHelper.Object.Collect();
                    if(Helper.LogHandler.ValidationActive){
                        MaxHourlyPayHelper.Validation.Empty.Validate();
                        MaxHourlyPayHelper.Validation.Duplicate.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToCropMarketing.Validate();
                        MaxHourlyPayHelper.Validation.ConflictToHire.Validate();
                    }
                }
            })
        },
    },
    Object: {
        New: function(surveyId, maxHourlyPayItemId, extra){
            var obj = {
                survey: surveyId,
                item: maxHourlyPayItemId,
            }
            if(extra) obj.extra = extra;
            return obj;
        },
        Collect: function(){
            maxHourlyPays = []
            MaxHourlyPayHelper.MaxHourlyPayItems.Container
            .filter(':checked')
            .each(function(){
                var maxHourlyPayItemId = $(this).data('maxhourlypayitem-id');
                var extra = MaxHourlyPayHelper.Extra.Container
                            .filter('[data-maxhourlypayitem-id="{0}"]'.format(maxHourlyPayItemId)).val();
                maxHourlyPays.push(
                    MaxHourlyPayHelper.Object.New(MainSurveyId, maxHourlyPayItemId, extra ? extra : null)
                )
            })
            CloneData[MainSurveyId].max_hourly_pays = maxHourlyPays;
        },
    },
    Validation: {
        Empty: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = CloneData[MainSurveyId].max_hourly_pays.length == 0;
                var msg = '不可漏填此問項';
                Helper.LogHandler.Log(con, MaxHourlyPayHelper.Alert, msg, this.Guids[0], null, false);
            }
        },
        Duplicate: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var con = MaxHourlyPayHelper.MaxHourlyPayItems.Container.filter(':checked').length > 1;
                var msg = '限註記一項';
                Helper.LogHandler.Log(con, MaxHourlyPayHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictToCropMarketing: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var hasCropMarketing = CropMarketingHelper.CropMarketing.Container.find('tr').length > 0;
                var itemChecked = MaxHourlyPayHelper.MaxHourlyPayItems.Container.filter('[data-maxhourlypayitem-id="1"]').prop('checked');
                var con = itemChecked && hasCropMarketing;
                var msg = '【問項1.4】有生產農產品者，不可勾選「1.無經營農耕業」。';
                Helper.LogHandler.Log(con, MaxHourlyPayHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
        ConflictToHire: {
            Guids: Helper.Guid.CreateMulti(),
            Validate: function(){
                var hasShortTermHire = ShortTermHireHelper.ShortTermHire.Container.find('tr').length > 0;
                var hasLongTermHIre = LongTermHireHelper.LongTermHire.Container.find('tr').length > 0;
                var itemChecked = MaxHourlyPayHelper.MaxHourlyPayItems.Container.filter('[data-maxhourlypayitem-id="2"]').prop('checked');
                var con = itemChecked && (hasShortTermHire || hasLongTermHIre);
                var msg = '【問項3.1.2或問項3.1.3】若有僱用常僱或臨時員工，不可勾選「2.無僱用人力」。';
                Helper.LogHandler.Log(con, MaxHourlyPayHelper.Alert, msg, this.Guids[0], null, false);
            },
        },
    }
}