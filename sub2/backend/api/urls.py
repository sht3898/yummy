from rest_framework import permissions
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="YUMMY - 맛있는 여행의 아름다움",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # STORE, SPOTS, LODGING
    # [NAME]/ -> GET, POST
    # [NAME]/<INT:PK>/ -> GET, PATCH, DELETE

   # STOREREVIEW, SPOTREVIEW, LODGINGREVIEW
   # [NAME]/ -> POST
   # [NAME]/REVIEWS/<INT:PK>/ -> GET, PATCH, DELETE
   # [NAME]/REVIEWS/USER/<INT:PK>/ -> GET

    path('stores/', views.Store.as_view()),
    path('stores/<int:pk>/', views.StoreDetail.as_view()),
    # 메뉴 추천
    path('stores/recommendations/<int:pk>/', views.StoreRecommendations),

    path('stores/reviews/', views.StoreReview.as_view()),
    path('stores/reviews/<int:pk>/', views.StoreReviewDetail.as_view()),
    path('stores/reviews/user/<int:pk>/', views.StoreReviewByUser.as_view()),

    path('spots/', views.Spot.as_view()),
    path('spots/<int:pk>/', views.SpotDetail.as_view()),
    # 장소 추천
    path('spots/recommendations/<int:pk>/', views.SpotRecommendations),

    path('spots/reviews/', views.SpotReview.as_view()),
    path('spots/reviews/<int:pk>/', views.SpotReviewDetail.as_view()),
    path('spots/reviews/user/<int:pk>/', views.SpotReviewByUser.as_view()),
    
    path('lodgings/', views.Lodging.as_view()),
    path('lodgings/<int:pk>/', views.LodgingDetail.as_view()),

    path('lodgings/reviews/', views.LodgingReview.as_view()),
    path('lodgings/reviews/<int:pk>/', views.LodgingReviewDetail.as_view()),
    path('lodgings/reviews/user/<int:pk>/', views.LodgingReviewByUser.as_view()),

    # 유저아이디로 작성한 전체 리뷰 검색
    path('reviews/user/<int:pk>/', views.ReviewByUser), # GET
    #plan id로 스크랩하기, 한번에 plan 저장하기
    path('plan/all/', views.AllPlansGetandSave.as_view()), # PUT : 스크랩, POST : 한번에 저장
    path('plan/all/<int:pk>/', views.AllPlansDetail.as_view()), # GET, PATCH, DELETE

    path('plans/', views.Plan.as_view()),
    path('plans/<int:pk>/', views.PlanDetail.as_view()),

   #  path('plans/days/', views.PlanDay.as_view()),
   #  path('plans/days/<int:pk>/', views.PlanDayDetail.as_view()),

   #  path('plans/days/itinerarys/', views.Itinerary.as_view()),
   #  path('plans/days/itinerarys/<int:pk>/', views.ItineraryDetail.as_view()),

    #naver blog search
    path('search/blog/', views.NaverSearchBlogReview),
    path('search/image/', views.NaverSearchPlace),
    path('search/plans/', views.SearchPlanByArea.as_view()),

]
