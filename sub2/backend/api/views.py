from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, UserConfirmSerializer, UserUpdateSerializer, SocialUserSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from api.pagination import PaginationHandlerMixin
from rest_framework.authtoken.models import Token

from api import models, serializers
from django.db.models import Count

from django.db.models import Q
from api.MF import set_algo
from api.spot import recommend

from django.db import transaction

import os
import sys
import urllib.request
import json

class SmallPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50

"""
Store API
 class Store            [stores/] [get, post]
 class StoreDetail      [stores/<int:pk>] [get, patch, delete]
"""
# stores/

class Store(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.StoreSerializer

# 가게 리스트를 불러오는 API
# query parameter [name, area]
# name=1987&area=세종
    def get(self, request, format=None, *args, **kwargs):

        area = request.query_params.get("area",None)
        name = request.query_params.get("name", None)
        order_by = request.query_params.get("order_by",None)
        desc = request.query_params.get("desc",None)
        gte = request.query_params.get("gte", None)
# TODO : 유저 아이디가 있는 경우, 없는 경우
        # TODO : 추천알고리즘이 여기 들어오면 자리만들어줘야해
        # FIXME: 추천알고리즘을 과연 여기에 넣을 것인가 ...! 두둥탁

        # user_id = request.query_params.get("user",None)

        # user = get_object_or_404(models.User, pk=user_id)
    
        q = Q()
        if area is not None:
            area_list = area.split(",")
            for area in area_list:
                if area.strip() is '':
                    continue
                try:
                    t = models.Area.objects.get(pk=area).address.split(" ")
                except:
                    continue
                keyword = ""
                if len(t[0]) >=5 :
                    keyword = t[0]
                else:
                    keyword = t[0]+" "+t[1]

                q.add(Q(addr__contains=keyword), q.OR)
            instance = models.Store.objects.filter(q)
            # print(str(instance.query)) #질의 확인
        else:
            instance = models.Store.objects.all()

        if name is not None:
            instance = instance.filter(store_name__contains=name)

        # 커스텀 필드는 소트가 않데...
        if order_by is not None:
            # 이름 정렬
            if order_by =="name":
                if desc=='True' or desc is None:
                    instance = instance.order_by("store_name")
                elif desc=='False':
                    instance = instance.order_by("-store_name")

            # 리뷰 수에 따른 정렬
            elif order_by=="review":
                if gte is not None:
                    if desc =='True' or desc is None:
                        instance = instance.filter(review_count__gte=gte).order_by("review_count")
                    else:
                        instance = instance.filter(review_count__gte=gte).order_by("-review_count")
                else:
                    if desc=='True' or desc is None:
                        instance = instance.order_by("review_count")
                    else:
                        instance = instance.order_by("-review_count")

            # 평균 점수에 따른 정렬
            elif order_by =="score":
                if desc =='True' or desc is None:
                    instance = instance.extra(select={'avg':'review_total_score / review_count'}, order_by=('avg',))
                elif desc=='False':
                    instance = instance.extra(select={'avg':'review_total_score / review_count'}, order_by=('-avg',))

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.StoreListSerializer(page,
 many=True).data)
        else:
            serializer = serializers.StoreListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# 가게를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# stores/<int:pk>
class StoreDetail(APIView):
    serializer_class = serializers.StoreSerializer

    def get_object(self, id):
            store = get_object_or_404(models.Store, pk=id)
            return store
# 가게 id로 불러오는 API
    def get(self, request, pk):
        store = self.get_object(pk)
        serializer = self.serializer_class(store)
        # 해당 가게의 메뉴, 리뷰를 받아옴
        review = store.review_store.all()
        # print(store_detail.get('store_name'))
        sum=0
        for i in serializers.StoreReviewSerializer(review,many=True).data:
            sum+=i.get("total_score")
        # store 조회할때
        # id, detail(store정보), reviews, avg(평균 평점)
        avg = None if len(review)==0 else sum/len(review)
        result = {
        "id": pk,
        "detail":serializer.data,
        "review":serializers.StoreReviewSerializer(review, many=True).data,
        "avg_score" : avg
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        store = get_object_or_404(models.Store, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=store, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        store = get_object_or_404(models.Store, pk=pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def StoreRecommendations(request,pk):
    # stores/recommendations/<int:pk>?area=대전광역시
    # pk -> user_id
    area = request.query_params.get("area", None)
    # 없는 유저에게는 추천을 해줄수가 없다규...
    user = get_object_or_404(models.User, pk=pk)
    print("1")
    final_area_list = []
    if area is not None:
        area_list = area.split(",")
        for area in area_list:
            if area.strip() is '':
                continue
            try:
                t = models.Area.objects.get(pk=area).address.split(" ")
            except:
                continue
            keyword = ""
            if len(t[0]) >=5 :
                keyword = t[0]
            else:
                keyword = t[0]+" "+t[1]
            final_area_list.append(keyword)


    pred_result = set_algo(pk,final_area_list)
    print(pred_result)
    result = []
    # 예상평점 없어 ~!
    for store_id in pred_result:
        result.append(serializers.StoreSerializer(models.Store.objects.get(pk=store_id)).data)
    return Response(result, status=status.HTTP_200_OK)

"""
Review API
class StoreReview            [stores/reivews/] [post]
class StoreReviewDetail      [stores/reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class StoreReview(APIView, PaginationHandlerMixin):
    serializer_class = serializers.StoreReviewSerializer

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            review_store = serializer.validated_data['store']
            store_update_data = {
            "review_count" : review_store.review_count+1,
            "review_total_score" : review_store.review_total_score + serializer.validated_data['total_score']
            }
            store_update = serializers.StoreListSerializer(data=store_update_data,instance=review_store,partial=True)
            if store_update.is_valid():
                store_update.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # stores/reviews/<int:pk>
class StoreReviewDetail(APIView):
    serializer_class = serializers.StoreReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.StoreReview, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.StoreReview, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)

        if serializer.is_valid():
            if 'total_score' in serializer.validated_data : # 평점을 변경하고 싶을 경우

                store_id = self.serializer_class(review).data['store']
                review_store = models.Store.objects.get(pk=store_id)
                review_store_serializer = serializers.StoreListSerializer(review_store)
                store_update_data = {
                "review_total_score" : review_store_serializer.data['review_total_score'] - review.total_score + serializer.validated_data['total_score']
                }
                store_update = serializers.StoreListSerializer(data=store_update_data, instance=review_store,partial=True)
                if store_update.is_valid():
                    store_update.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
                
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.StoreReview, pk=pk)
        store_id = self.serializer_class(review).data['store']
        review_store = models.Store.objects.get(pk=store_id)
        review_store_serializer = serializers.StoreListSerializer(review_store)

        store_update_data = {
        "review_count" : review_store_serializer.data['review_count']-1,
        "review_total_score" : review_store_serializer.data['review_total_score'] - review.total_score
        }

        store_update = serializers.StoreListSerializer(data=store_update_data,instance=review_store,partial=True)
        if store_update.is_valid():
            store_update.save()
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# 유저  id에 따른 작성 리뷰 리스트
class StoreReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.StoreReviewSerializer

    def get(self, request, pk):
        instance = models.StoreReview.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


"""
Spot API
 class Spot            [spots/] [get, post]
 class SpotDetail      [spots/<int:pk>] [get, patch, delete]
"""
class Spot(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.SpotSerializer

# 관광지 리스트를 불러오는 API
# query parameter [name, area]
    def get(self, request, format=None, *args, **kwargs):

        name = request.query_params.get("name", None)
        area = request.query_params.get("area", None)
        order_by = request.query_params.get("order_by",None)
        desc = request.query_params.get("desc",None)

        q = Q()
        if area is not None:
            area_list = area.split(",")
            for area in area_list:
                if area.strip() is '':
                    continue
                try:
                    t = models.Area.objects.get(pk=area).address.split(" ")
                except:
                    continue
                keyword = ""
                if len(t[0]) >=5 :
                    keyword = t[0]
                else:
                    keyword = t[0]+" "+t[1]

                q.add(Q(addr__contains=keyword), q.OR)
            instance = models.Spot.objects.filter(q)
            # print(str(instance.query)) #질의 확인
        else:
            instance = models.Spot.objects.all()
        # 기본 전체 spot objects
        
        if name is not None:
            instance = instance.filter(spot_name__contains=name)

        if order_by is not None:
            # 이름 정렬
            if order_by =="name":
                if desc=='True' or desc is None:
                    instance = instance.order_by("spot_name")
                elif desc=='False':
                    instance = instance.order_by("-spot_name")

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.SpotListSerializer(page,
 many=True).data)
        else:
            serializer = self.serializers.SpotListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# 관광지를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# spots/<int:pk>
class SpotDetail(APIView):
    serializer_class = serializers.SpotSerializer

    def get_object(self, id):
            spot = get_object_or_404(models.Spot, pk=id)
            return spot
# 관광지 id로 불러오는 API
    def get(self, request, pk):
        spot = self.get_object(pk)
        serializer = self.serializer_class(spot)
        review = spot.spotreview_spot.all()
        result = {
            "detail" : serializer.data,
            "review" : serializers.SpotReviewSerializer(review, many=True).data
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        spot = get_object_or_404(models.Spot, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=spot, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        spot = get_object_or_404(models.Spot, pk=pk)
        spot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def SpotRecommendations(request,pk):
    # pk -> 장소 아이디
    # 장소가 등록된거 아니면은 오바자너 ~~!!!
    spot = get_object_or_404(models.Spot, pk=pk)
    # loaddata()
    pred_result = recommend(pk)
    # print(pred_result)
    result = []
    # 예상평점 없어 ~!
    for spot_id in pred_result:
        result.append(serializers.SpotSerializer(models.Spot.objects.get(pk=spot_id)).data)
    return Response(result, status=status.HTTP_200_OK)


"""
 Spot Review API
class SpotReview            [spots/reivews/] [post]
class SpotReviewDetail      [spots/reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class SpotReview(APIView, PaginationHandlerMixin):
    serializer_class = serializers.SpotReviewSerializer

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # stores/reviews/<int:pk>
class SpotReviewDetail(APIView):
    serializer_class = serializers.SpotReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.SpotReview, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.SpotReview, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.SpotReview, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 유저  id에 따른 작성 리뷰 리스트
class SpotReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.SpotReviewSerializer

    def get(self, request, pk):
        instance = models.SpotReview.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


"""
Lodging API
 class Lodging            [lodgings/] [get, post]
 class LodgingDetail      [lodgings/<int:pk>] [get, patch, delete]
"""
class Lodging(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.LodgingSerializer

# 관광지 리스트를 불러오는 API
# query parameter [name, area]
    def get(self, request, format=None, *args, **kwargs):

        name = request.query_params.get("name", None)
        area = request.query_params.get("area", None)
        order_by = request.query_params.get("order_by",None)
        desc = request.query_params.get("desc",None)

        q = Q()
        if area is not None:
            area_list = area.split(",")
            for area in area_list:
                if area.strip() is '':
                    continue
                try:
                    t = models.Area.objects.get(pk=area).address.split(" ")
                except:
                    continue
                keyword = ""
                if len(t[0]) >=5 :
                    keyword = t[0]
                else:
                    keyword = t[0]+" "+t[1]

                q.add(Q(addr__contains=keyword), q.OR)
            instance = models.Lodging.objects.filter(q)
            # print(str(instance.query)) #질의 확인
        else:
            instance = models.Lodging.objects.all()

        # 기본 전체 spot objects
        if name is not None:
            instance = instance.filter(lodging_name__contains=name)

        if order_by is not None:
            # 이름 정렬
            if order_by =="name":
                if desc=='True' or desc is None:
                    instance = instance.order_by("lodging_name")
                elif desc=='False':
                    instance = instance.order_by("-lodging_name")

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.LodgingListSerializer(page,
 many=True).data)
        else:
            serializer = serializers.LodgingListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# 숙박시설를 추가하는 API
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# lodgings/<int:pk>
class LodgingDetail(APIView):
    serializer_class = serializers.LodgingSerializer

    def get_object(self, id):
            lodging = get_object_or_404(models.Lodging, pk=id)
            return lodging
# 숙박업소 id로 불러오는 API
    def get(self, request, pk):
        lodging = self.get_object(pk)
        serializer = self.serializer_class(lodging)
        review = lodging.lodgingreview_lodging.all()
        result = {
            "detail" : serializer.data,
            "review" : serializers.LodgingReviewSerializer(review, many=True).data
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        lodging = get_object_or_404(models.Lodging, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=lodging, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        lodging = get_object_or_404(models.Lodging, pk=pk)
        lodging.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



"""
Lodging Review API
class LodgingReview            [lodgings/reivews/] [post]
class LodgingReviewDetail      [lodgings/reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class LodgingReview(APIView, PaginationHandlerMixin):
    serializer_class = serializers.LodgingReviewSerializer

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # lodgings/reviews/<int:pk>
class LodgingReviewDetail(APIView):
    serializer_class = serializers.SpotReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.LodgingReview, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.LodgingReview, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.LodgingReview, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def create_user(request):
    error = UserSerializer.validate(get_user_model(), data=request.data)
    if error['password'] or error['email']:
        return Response(error, status=400)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = UserSerializer.create(get_user_model(), request.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(["POST"])
def verify_user(request):
    msg =  UserConfirmSerializer().validate(data=request.data, token=request.headers.get("Authorization"))
    if msg.get('user'):
        serializers = UserSerializer(msg['user'])
        return Response(serializers.data)
    else:
        return Response(msg['error'], status=400)

@api_view(["PATCH", "DELETE"])
def modify_user(request):
    if request.method == "PATCH":
        msg = UserUpdateSerializer.update(get_user_model(), data=request.data, token=request.headers.get("Authorization"))
    else:
        msg = UserUpdateSerializer.delete(get_user_model(), token=request.headers.get("Authorization"))
    return Response(msg)

from oauth2client import client
import requests
import json
CLIENT_ID = '963253194499-2k348321r9loaq9p1878dd0lf9vs0cj8.apps.googleusercontent.com'
CLIENT_SECRET = 'rx4FcK2BVvkN5cDyRVRNS8Xt'

@api_view(["POST"])
def google_user(request):
    auth_code = request.data['code']
    credentials = client.credentials_from_code(CLIENT_ID, CLIENT_SECRET, scope='', code=auth_code)
    authorization_header = {"Authorization": f"OAuth {credentials.access_token}"}
    response = json.loads(requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=authorization_header).text)
    user = get_user_model().objects.filter(email= response["email"])
    if not user:
        user = SocialUserSerializer.create(get_user_model(), response["email"])
    else:
        user=user[0]
    serializer = SocialUserSerializer(user)
    return Response(serializer.data)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


# 유저  id에 따른 작성 리뷰 리스트
class LodgingReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.LodgingReviewSerializer

    def get(self, request, pk):
        instance = models.LodgingReview.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def ReviewByUser(request,pk):
    store_reviews = models.StoreReview.objects.filter(user=pk)
    spot_reviews = models.SpotReview.objects.filter(user=pk)
    lodging_reviews = models.LodgingReview.objects.filter(user=pk)
    result = {
        "store" : serializers.StoreReviewSerializer(store_reviews, many=True).data,
        "spot" : serializers.SpotReviewSerializer(spot_reviews, many=True).data,
        "lodging" : serializers.LodgingReviewSerializer(lodging_reviews, many=True).data
    }
    return Response(result, status=status.HTTP_200_OK)


# 일정 
"""
Plan API
class Plan            [plans/] [get/post]
class PlanDetail      [plans/<int:pk>] [get, patch, delete]
"""
class Plan(APIView, PaginationHandlerMixin):
    serializer_class = serializers.PlanListSerializer
    pagination_class = SmallPagination

    def get(self, request, format=None, *args, **kwargs):

        user_id = request.query_params.get("user", None)
        if user_id is not None:
            instance = models.Plan.objects.filter(user=user_id).order_by('-id') # 해당 유저가 작성한 여행계획 조회용
        else:
            instance = models.Plan.objects.all().order_by('-id')

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.PlanListSerializer(page,
 many=True).data)
        else:
            serializer = serializers.PlanListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, format=None):
    #     serializer = serializers.PlanSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

# TODO : 지울것
# plans/<int:pk>
class PlanDetail(APIView):
    serializer_class = serializers.PlanSerializer

    def get_object(self, id):
            plan = get_object_or_404(models.Plan, pk=id)
            return plan

    def get(self, request, pk):
        plan = self.get_object(pk)
        serializer = self.serializer_class(plan)
        plan_day = plan.planday_plan.all()
        result = {
            "detail" : serializer.data,
            "day" : serializers.PlanDaySerializer(plan_day, many=True).data,
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        plan = get_object_or_404(models.Plan, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=plan, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # # 삭제
    # def delete(self, request, pk, format=None):
    #     plan = get_object_or_404(models.Plan, pk=pk)
    #     plan.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# # TODO : Delete
# # 일정 일자 계획
# """
# PlanDay API
# class PlanDay            [plans/days/] [post]
# class PlanDayDetail      [plans/days/<int:pk>] [get, patch, delete]
# """
# class PlanDay(APIView, PaginationHandlerMixin):
#     serializer_class = serializers.PlanDaySerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

# # plans/days/<int:pk>
# class PlanDayDetail(APIView):
#     serializer_class = serializers.PlanDaySerializer

#     def get_object(self, id):
#             planday = get_object_or_404(models.PlanDay, pk=id)
#             return planday

#     def get(self, request, pk):
#         planday = self.get_object(pk)
#         serializer = self.serializer_class(planday)
#         itinerary = planday.itinerary_day.all()
#         result = {
#             "detail" : serializer.data,
#             "itinerary" : serializers.ItinerarySerializer(itinerary, many=True).data
#         }
#         return Response(result, status=status.HTTP_200_OK)

#     def patch(self, request, pk):
#         planday = get_object_or_404(models.PlanDay, pk=pk)

#         area_list = request.data.get("area_list","")
#         planday.area.clear() # 전부지우고 새로쓴다...
#         # 지역 등록하기... 이래도 대나
#         for area in area_list:
#             planday.area.add(models.Area.objects.get(pk=area))

#         serializer = self.serializer_class(data=request.data, instance=planday, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

#     # 삭제
#     def delete(self, request, pk, format=None):
#         planday = get_object_or_404(models.PlanDay, pk=pk)
#         planday.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # TODO : Delete
# # 일정 일자 세부계획
# """
# Itinerary API
# class Itinerary            [plans/days/itinerarys] [post]
# class ItineraryDetail      [plans/days/itinerarys/<int:pk>] [get, patch, delete]
# """
# class Itinerary(APIView, PaginationHandlerMixin):
#     serializer_class = serializers.ItinerarySerializer

# # 한번에 등록하기
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data['itinerarys'], many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else : 
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
#         return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# class ItineraryDetail(APIView):
#     serializer_class = serializers.ItinerarySerializer

#     def get_object(self, id):
#             itin = get_object_or_404(models.Itinerary, pk=id)
#             return itin

#     def get(self, request, pk):
#         itin = self.get_object(pk)
#         serializer = self.serializer_class(itin)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def patch(self, request, pk):
#         itin = get_object_or_404(models.Itinerary, pk=pk)
#         serializer = self.serializer_class(data=request.data, instance=itin, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

#     # 삭제
#     def delete(self, request, pk, format=None):
#         itin = get_object_or_404(models.Itinerary, pk=pk)
#         itin.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class AllPlansGetandSave(APIView):
    @transaction.atomic
    def put(self, request): # 다른 유저가 만들어놓은 플랜을 스크랩 하는 것
        user_id = request.data.get("user_id",None)
        plan_id = request.data.get("plan_id", None)
        if user_id is None or plan_id is None: # 둘다 없으면 않데
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            p = -1
            target_user = get_object_or_404(models.User, pk=user_id) # 누구 아이디로 옮겨올건지
            origin_plan = get_object_or_404(models.Plan, pk=plan_id) # 복사하려는 플랜
            new_plan = models.Plan() # 복사하려는 플랜
            new_plan.title = "[스크랩] "+origin_plan.title
            new_plan.start_date = origin_plan.start_date
            new_plan.end_date = origin_plan.end_date
            new_plan.user = target_user
            new_plan.save() # 새로 저장
            p = new_plan
            origin_plandays = origin_plan.planday_plan.all() # each day of travel
            plandays = origin_plan.planday_plan.all() # each day of travel
            for op,tp in zip(origin_plandays,plandays):
                tp.pk=None
                tp.plan = new_plan
                tp.save()
                tp.area.add(*op.area.all())
                for i in op.itinerary_day.all():
                    i.pk=None
                    i.day = tp
                    i.save()

        if p== -1: # 결과적으로 저장한게 없어? 사요나라..
            return Response(status =status.HTTP_400_BAD_REQUEST)
        else :
            return Response(status=status.HTTP_200_OK)

    
# 헌번에 등록하기 !
    def post(self, request):
        plans = request.data.get("plans", None)
        days = request.data.get("days", None)
        if 'user' in plans:
            user_id = plans['user']
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        p = -1
        user = get_object_or_404(models.User, pk=user_id)
        plan = serializers.PlanSerializer(data = plans)
        try:
            if plan.is_valid(raise_exception = True):
                p = plan.save()
                for day in days:
                    new_day = models.PlanDay()
                    new_day.date = day['date']
                    new_day.plan = p
                    new_day.save()
                    for area in day['area']:
                        new_day.area.add(models.Area.objects.get(pk=area))
                    for itin in day['itinerarys']:
                        itin['day']=new_day.pk
                        itin_s = serializers.ItinerarySerializer(data=itin)
                        if itin_s.is_valid(raise_exception=True):
                            ti = itin_s.save()
        except :
            if p != -1:
                p.delete()
            return Response(status =status.HTTP_400_BAD_REQUEST)

        return Response(plan.data, status=status.HTTP_200_OK)


# 일정 모든 세부 한번에 불러오는 친구...
class AllPlansDetail(APIView):
    def get(self,request,pk):
        plan = get_object_or_404(models.Plan, pk=pk)
        serializer = serializers.AllPlanSerializer(plan)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        plan = get_object_or_404(models.Plan, pk=pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def patch(self, request, pk):
        origin_plan = get_object_or_404(models.Plan, pk=pk)
        plans = request.data.get("plans", None)
        days = request.data.get("days", None)
        if plans is None or days is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if 'user' in plans:
            user_id = plans['user']
        if origin_plan.user.id != user_id: # 유저아이디가 다르면 않데
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            changed_plan = serializers.PlanSerializer(data=plans, instance=origin_plan, partial=True)
            if changed_plan.is_valid(raise_exception=True):
                p =changed_plan.save()
                origin_days = origin_plan.planday_plan.all()
                tmp_origin_days = list(origin_days)
                target=None
                diff = abs(len(tmp_origin_days)-len(days)) # 두 일정 크기의 차이
                if len(tmp_origin_days) >= len(days):
                    target = days
                else:
                    target = tmp_origin_days
                for i in range(diff):
                    target.append(None)
                for op, np in zip(tmp_origin_days, days):
                    if op is None:
                        # 새 day를 만들어야해
                        new_day = models.PlanDay()
                        new_day.date = np['date']
                        new_day.plan = p
                        new_day.save()
                        for area in np['area']:
                            new_day.area.add(models.Area.objects.get(pk=area))
                        if 'itinerarys' in np:
                            for itin in np['itinerarys']:
                                itin['day']=new_day.pk
                                itin_s = serializers.ItinerarySerializer(data=itin)
                                if itin_s.is_valid(raise_exception=True):
                                    ti = itin_s.save()
                    elif np is None:
                        # op 제거
                        op.delete()
                    else:
                        # 수정 반영
                        day_s = serializers.PlanDaySerializer(data=np, instance=op, partial=True)
                        if day_s.is_valid():
                            changed_day = day_s.save()
                            changed_day.area.clear()
                            for area in np['area']:
                                changed_day.area.add(models.Area.objects.get(pk=area))
                            origin_itin = list(changed_day.itinerary_day.all())
                            if 'itinerarys' in np:
                                new_itin = np['itinerarys']
                                i_target = None
                                i_diff = abs(len(origin_itin)-len(new_itin))
                                if len(origin_itin) >= len(new_itin):
                                    i_target = new_itin
                                else:
                                    i_target = origin_itin
                                for i in range(i_diff):
                                    i_target.append(None)
                                for oi, ni in zip(origin_itin, new_itin):
                                    if oi is None:
                                        ni['day'] = changed_day.pk
                                        ni_s = serializers.ItinerarySerializer(data=ni)
                                        if ni_s.is_valid(raise_exception=True):
                                            ni_s.save()
                                        pass
                                    elif ni is None:
                                        # 기존거 삭제
                                        oi.delete()
                                    else:
                                        # 업데이트 반영
                                        ni['day']=changed_day.pk
                                        ni_s = serializers.ItinerarySerializer(data=ni, instance=op,partial=True)
                                        if ni_s.is_valid():
                                            ni_s.save()
                            else:
                                changed_day.itinerary_day.all().delete()

                            
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def NaverSearchBlogReview(request):
    target_type = request.query_params.get("type", None)
    target_id = request.query_params.get("id", None)

    if target_type is None or target_id is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    client_id = "dWDwvJNIbIqNt_9iTf8P" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "0J1Q_FYVzb" # 개발자센터에서 발급받은 Client Secret 값
    if target_type == "store":
        target = get_object_or_404(models.Store, pk=target_id)
        target_name = target.store_name
        target_area = target.addr
    elif target_type == "lodging":
        target = get_object_or_404(models.Lodging, pk=target_id)
        target_name = target.lodging_name
        target_area = target.addr
    elif target_type == "spot":
        target = get_object_or_404(models.Spot, pk=target_id)
        target_name = target.Spot_name
        target_area = target.addr
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    query =  target_name+" "+ target_area
    # print(query)
    encText = urllib.parse.quote(query) # 한글 파싱
    url = "https://openapi.naver.com/v1/search/blog.json?query=" + encText + "&display=3"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        json_rt = response_body.decode('utf-8')
        results = json.loads(json_rt) # 결과값 json 파싱
        return Response(results, status=status.HTTP_200_OK)
    else:
        results = {}
        return Response(results, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def NaverSearchPlace(request):
    keyword = request.query_params.get("keyword", None)
    if keyword is None:
        return Response("keyword required. ", status=status.HTTP_400_BAD_REQUEST)

    client_id = "dWDwvJNIbIqNt_9iTf8P" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "0J1Q_FYVzb" # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(keyword) # 한글 파싱
    url = "https://openapi.naver.com/v1/search/image.json?display=1&sort=sim&query=" + encText 

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        json_rt = response_body.decode('utf-8')
        results = json.loads(json_rt) # 결과값 json 파싱
        return Response(results, status=status.HTTP_200_OK)
    else:
        results = {}
        return Response(results, status=status.HTTP_400_BAD_REQUEST)


# 지역을 키워드로 줘서 해당 지역들을 포함하는 여행목록을 조회하는고야
class SearchPlanByArea(APIView, PaginationHandlerMixin):
    serializer_class = serializers.PlanListSerializer
    pagination_class = SmallPagination

    def get(self, request, format=None, *args, **kwargs):

        area = request.query_params.get("area", None) # required.
        if area is not None:
            area_list = area.split(",")
            final_area = []
            for aa in area_list:
                if aa.strip() is '':
                    continue
                try:
                    t = models.Area.objects.get(pk=aa)
                    final_area.append(aa)
                except:
                    continue
            final_plans = []
            tmp = models.AreaPlanday.objects.filter(area__in=final_area)
            for inst in tmp:
                if inst.planday.plan.id not in final_plans:
                    final_plans.append(inst.planday.plan.id)
            instance = models.Plan.objects.filter(id__in=final_plans)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
 many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)