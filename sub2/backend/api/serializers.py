from .models import Store, User, Spot, Lodging, SpotReview, LodgingReview ,StoreReview, Plan, PlanDay, Itinerary,Area
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_jwt.serializers import VerificationBaseSerializer
from rest_framework_jwt.compat import get_username_field, PasswordField
from rest_framework.serializers import ValidationError


# Store
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
        ]
class StoreListSerializer(serializers.ModelSerializer):
#     review_store = serializers.StringRelatedField(many=True)
#     review_count = serializers.IntegerField(
#     source='review_store.count'
# )
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = [
        "id",
        "store_name",
        "branch",
        "area",
        "address",
        "latitude",
        "longitude",
        "category_list",
        "review_count",
        "review_total_score",
        "review_avg_score",
        ]
    def get_review_avg_score(self, obj):
        if(obj.review_count==0):
            return 0
        else:
            return obj.review_total_score/obj.review_count

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    gender = serializers.CharField()
    birth_year = serializers.IntegerField()
    nickname = serializers.CharField()

    class Meta:
        model = User
        fields = ["id","email", "gender", "password1", "password2", "birth_year", "nickname", "is_social"]
        

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data["email"],
            gender = validated_data["gender"],
            birth_year = validated_data["birth_year"],
            nickname = validated_data["nickname"]
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
       
    def validate(self, data):
        non_alpha = set([s for s in "!@#$%^&*()|-=_+\[]{};':\",./?><"])
        error = dict({'email' : [], 'password': []})
        if data['password1'] != data['password2']: # confirm error: 1
            error['password'].append('비밀번호 같게 해주세요')
        if not 8 <= len(data['password1']) < 16:   # password length error: 2
            error['password1'].append('비밀번호를 8 ~ 16자로 작성해주세요!')
        if data['password1'].isdigit():  # password is only numbers: 3
            error['password'].append('비밀번호를 다른 문자와 조합해주세요!')
        if get_user_model().objects.filter(email= data['email']): # same username in db : 4
            error['email'].append('중복된 ID가 있습니다.')
        # if non_alpha not in data['password1']: # non_alph in username: 6
        #     error['password'].append('비밀번호에 특수문자를 넣어주세요!')
        return error

class UserConfirmSerializer(VerificationBaseSerializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data, token):
        payload = self._check_payload(token=token)
        tokenuser = self._check_user(payload=payload)
        credentials = {
            'email': tokenuser.email,
            'password': data.get('password')
        }
        if all(credentials.values()):
            user = authenticate(**credentials)
            if user==tokenuser:
                return {"user":user}
            else:
                return {"error":"잘못된 비밀번호 입니다. 비밀번호를 다시 입력해주세요"}
        return {"error":"비밀번호를 입력해주세요"}

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "gender", "password1", "password2", "birth_year", "nickname", "is_social"]
        
    def validate(self, data):
        non_alpha = set([s for s in "!@#$%^&*()|-=_+\[]{};':\",./?><"])
        error = dict({'password': []})
        if not 8 <= len(data['password']) < 16:   # password length error: 2
            error['password'].append('비밀번호를 8 ~ 16자로 작성해주세요!')
        if data['password'].isdigit():  # password is only numbers: 3
            error['password'].append('비밀번호를 다른 문자와 조합해주세요!')
        return error

    def update(self, data, token):
        payload = UserConfirmSerializer._check_payload(self, token=token)
        user = UserConfirmSerializer._check_user(self, payload=payload)
        for field, value in data.items():
            if field == "password" and value:
                user.set_password(value)
            elif field == "nickname" and value:
                user.nickname = value
            elif field == "gender" and value:
                user.gender = value
            elif field == "birth_year" and value:
                user.birth_year = value
            elif field == "is_staff":
                user.is_staff = value
            elif field == "is_active":
                user.is_active = value
        user.save()
        return "수정이 완료되었습니다."

    def delete(self, token):
        payload = UserConfirmSerializer._check_payload(self, token=token)
        user = UserConfirmSerializer._check_user(self, payload=payload)
        user.delete()
        return "삭제가 완료되었습니다."

class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "gender", "birth_year", "nickname", "is_social"]
        

    def create(self, data):
        user = User.objects.create(
            email = data,
            is_social = True,
        )
        user.set_password(data)
        user.save()
        return user

# store review
class StoreReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = StoreReview
        fields = [
            "id",
            "store",
            "user",
            "nickname",
            "total_score",
            "content",
            "reg_time",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname

# 장소
# 장소 리스트
class SpotListSerializer(serializers.ModelSerializer):
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Spot
        fields = [
            "id",
            "spot_name",
            "address",
            "image_url",
            "latitude",
            "longitude",
            "review_avg_score",
            "image_url"
        ]
    def get_review_avg_score(self, obj):
        if(obj.spotreview_spot.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.spotreview_spot.all():
                sum+=rev.total_score
            return sum/obj.spotreview_spot.count()

 # 장소
class SpotSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(
    source='spotreview_spot.count'
)
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Spot
        fields = [
            "id",
            "spot_name",
            "address",
            "latitude",
            "longitude",
            "description",
            "image_url",
            "overview",
            "review_avg_score",
            "review_count"
        ]
    def get_review_avg_score(self, obj):
        if(obj.spotreview_spot.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.spotreview_spot.all():
                sum+=rev.total_score
            return sum/obj.spotreview_spot.count()

# 숙박 리스트
class LodgingListSerializer(serializers.ModelSerializer):
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Lodging
        fields = [
            "id",
            "lodging_name",
            "lodging_type",
            "address",
            "latitude",
            "longitude",
            "review_avg_score",
        ]
    def get_review_avg_score(self, obj):
        if(obj.lodgingreview_lodging.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.lodgingreview_lodging.all():
                sum+=rev.total_score
            return sum/obj.lodgingreview_lodging.count()

# 숙박
class LodgingSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(
    source='lodgingreview_lodging.count'
)
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Lodging
        fields = [
            "id",
            "lodging_name",
            "lodging_type",
            "address",
            "latitude",
            "longitude",
            "description",
            "review_avg_score",
            "review_count"
        ]
    def get_review_avg_score(self, obj):
        if(obj.lodgingreview_lodging.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.lodgingreview_lodging.all():
                sum+=rev.total_score
            return sum/obj.lodgingreview_lodging.count()

# 장소 리뷰
class SpotReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = SpotReview
        fields = [
            "id",
            "spot",
            "user",
            "nickname",
            "total_score",
            "content",
            "reg_time",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname
# 숙박 리뷰
class LodgingReviewSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = LodgingReview
        fields = [
            "id",
            "lodging",
            "user",
            "nickname",
            "total_score",
            "content",
            "reg_time",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "id",
            "city_name",
            "latitude",
            "longitude"
        ]

class PlanSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True, many=True)
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = [
            "id",
            "user",
            "nickname",
            "title",
            "area",
            "start_date",
            "end_date",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname

class PlanListSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    area_list = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = [
            "id",
            "user",
            "nickname",
            "title",
            "days",
            "month", #계획 시작일 달
            "area_list",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname
    def get_days(self, obj):
        return (obj.end_date - obj.start_date).days+1

    def get_month(self, obj):
        return (obj.start_date).month
    def get_area_list(self, obj):
        result = []
        for day in obj.planday_plan.all():
            for arealist in day.area_planday.all():
                if arealist.area.id not in result:
                    result.append(arealist.area.id)
        return result


class PlanDaySerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True, many=True)
    class Meta:
        model = PlanDay
        fields = [
            "id",
            "plan",
            "date",
            "area"
        ]


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = [
            "id",
            "day",
            "title",
            "start_time",
            "end_time",
            "store",
            "spot",
            "lodging"
        ]
    def validate(self, data):
        cnt=0
        cnt = cnt+1 if data['store'] is not None else cnt
        cnt = cnt+1 if data['spot'] is not None else cnt
        cnt = cnt+1 if data['lodging'] is not None else cnt
        if cnt ==0 or cnt > 1:
            raise serializers.ValidationError("Selection only allowed 1 (Spot, Store, Lodging) ")
        else:
            return data   


# 상세정보를 위한 시리얼라이저 친구들...1
class ItineraryDetailSerializer(serializers.ModelSerializer):
    store = StoreListSerializer(read_only=True)
    spot = SpotSerializer(read_only=True)
    lodging = LodgingSerializer(read_only=True)
    class Meta:
        model = Itinerary
        fields = [
            "id",
            "title",
            "start_time",
            "end_time",
            "store",
            "spot",
            "lodging"
        ]

#상세정보를 위한 시리얼라이저 2
class PlanDayDetailSerializer(serializers.ModelSerializer):
    itinerary_day = ItineraryDetailSerializer(read_only=True, many=True)
    area = AreaSerializer(read_only=True, many=True)
    class Meta:
        model = PlanDay
        fields = [
            "id",
            "date",
            "itinerary_day",
            "area"
        ]

class AllPlanSerializer(serializers.ModelSerializer):
    planday_plan= PlanDayDetailSerializer(read_only=True, many=True)
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = [
            "id",
            "user",
            "nickname",
            "start_date",
            "end_date",
            "title",
            "planday_plan",
        ]
    def get_nickname(self, obj):
        return obj.user.nickname
