from rest_framework.routers import DefaultRouter

from .views import (
    ContentTypeViewSet,
    SurveyViewSet,
    PhoneViewSet,
    AddressMatchViewSet,
    CityTownCodeViewSet,
    FarmLocationViewSet,
    LandStatusViewSet,
    LandTypeViewSet,
    LandAreaViewSet,
    BusinessViewSet,
    FarmRelatedBusinessViewSet,
    ManagementTypeViewSet,
    CropMarketingViewSet,
    LivestockMarketingViewSet,
    ProductTypeViewSet,
    ProductViewSet,
    UnitViewSet,
    LossViewSet,
    ContractViewSet,
    AnnualIncomeViewSet,
    MarketTypeViewSet,
    IncomeRangeViewSet,
    AgeScopeViewSet,
    PopulationAgeViewSet,
    PopulationViewSet,
    RelationshipViewSet,
    GenderViewSet,
    EducationLevelViewSet,
    FarmerWorkDayViewSet,
    LifeStyleViewSet,
    LongTermHireViewSet,
    ShortTermHireViewSet,
    NoSalaryHireViewSet,
    NumberWorkersViewSet,
    LackViewSet,
    LongTermLackViewSet,
    ShortTermLackViewSet,
    WorkTypeViewSet,
    SubsidyViewSet,
    RefuseViewSet,
    RefuseReasonViewSet,
    MonthViewSet,
)

api = DefaultRouter()
api.trailing_slash = '/?'

api.register(r'contenttype', ContentTypeViewSet)
api.register(r'survey', SurveyViewSet)
api.register(r'phone', PhoneViewSet)
api.register(r'addressmatch', AddressMatchViewSet)
api.register(r'citytowncode', CityTownCodeViewSet)
api.register(r'farmlocation', FarmLocationViewSet)
api.register(r'landstatus', LandStatusViewSet)
api.register(r'landtype', LandTypeViewSet)
api.register(r'landarea', LandAreaViewSet)
api.register(r'business', BusinessViewSet)
api.register(r'farmrelatedbusiness', FarmRelatedBusinessViewSet)
api.register(r'managementtype', ManagementTypeViewSet)
api.register(r'cropmarketing', CropMarketingViewSet)
api.register(r'livestockmarketing', LivestockMarketingViewSet)
api.register(r'producttype', ProductTypeViewSet)
api.register(r'product', ProductViewSet)
api.register(r'unit', UnitViewSet)
api.register(r'loss', LossViewSet)
api.register(r'contract', ContractViewSet)
api.register(r'annualincome', AnnualIncomeViewSet)
api.register(r'markettype', MarketTypeViewSet)
api.register(r'incomerange', IncomeRangeViewSet)
api.register(r'agescope', AgeScopeViewSet)
api.register(r'populationage', PopulationAgeViewSet)
api.register(r'population', PopulationViewSet)
api.register(r'relationship', RelationshipViewSet)
api.register(r'gender', GenderViewSet)
api.register(r'educationlevel', EducationLevelViewSet)
api.register(r'farmerworkday', FarmerWorkDayViewSet)
api.register(r'lifestyle', LifeStyleViewSet)
api.register(r'longtermhire', LongTermHireViewSet)
api.register(r'shorttermhire', ShortTermHireViewSet)
api.register(r'nosalaryhire', NoSalaryHireViewSet)
api.register(r'numberworkers', NumberWorkersViewSet)
api.register(r'lack', LackViewSet)
api.register(r'longtermlack', LongTermLackViewSet)
api.register(r'shorttermlack', ShortTermLackViewSet)
api.register(r'worktype', WorkTypeViewSet)
api.register(r'subsidy', SubsidyViewSet)
api.register(r'refuse', RefuseViewSet)
api.register(r'refusereason', RefuseReasonViewSet)
api.register(r'month', MonthViewSet)
