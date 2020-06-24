from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models

class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump_with_rev_store.pkl") # review정보 포함한것
    DATA_FILE_STORE = str(DATA_DIR / "dump_store.pkl") # store 주소 라벨링
    DATA_FILE_LODGING = str(DATA_DIR / "dump_lodging.pkl") # 숙박
    DATA_FILE_SPOT = str(DATA_DIR / "dump_spot.pkl") # 관광지(한국관광공사)
    DATA_FILE_AREA = str(DATA_DIR / "dump_area.pkl") # 지역 

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
            data_lodging = pd.read_pickle(Command.DATA_FILE_LODGING)
            data_spot = pd.read_pickle(Command.DATA_FILE_SPOT)
            data_area = pd.read_pickle(Command.DATA_FILE_AREA)
            data_store = pd.read_pickle(Command.DATA_FILE_STORE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data, data_spot, data_lodging, data_area,data_store

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes, dataframes_spot, dataframes_lodging, dataframes_area, dataframes_store = self._load_dataframes()
# load store dataframe with reviewcount , total_score
# store
        print("[*] Initializing stores...( + review : score, count)")
        models.Store.objects.all().delete()
        stores = dataframes_store["stores"]
        stores_bulk = [
            models.Store(
                id=store.id,
                store_name=store.store_name,
                branch=store.branch,
                area=store.area,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
                category=store.category,
                review_count=store.count,
                review_total_score=store.total,
                addr = store.addr,
            )
            for store in stores.itertuples()
        ]
        models.Store.objects.bulk_create(stores_bulk)

        print("[+] Done")


# user
        print("[*] Initializing users...")
        models.User.objects.all().delete()
        users = dataframes["users"]
        users_bulk = [
            models.User(
                id = user.id,
                email="None"+str(user.id)+"@co.co",
                birth_year=user.age,
                gender=user.gender,
                nickname="user"+str(user.id),
            )
            for user in users.itertuples()
        ]
        models.User.objects.bulk_create(users_bulk)

        print("[+] Done")

# review
        print("[*] Initializing reviews...")
        models.StoreReview.objects.all().delete()
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.StoreReview(
                id=review.id,
                store=models.Store.objects.get(id=review.store),
                user=models.User.objects.get(id=review.user),
                total_score=review.score,
                content=review.content,
                reg_time=review.reg_time,
            )
            for review in reviews.itertuples()
        ]
        models.StoreReview.objects.bulk_create(reviews_bulk)

        print("[+] Done")

# spot
        print("[*] Initializing spot...")
        models.Spot.objects.all().delete()
        spots = dataframes_spot["spots"]
        spots_bulk = [
            models.Spot(
                id = spot.contentid,
                spot_name=spot.title,
                spot_type = spot.category,
                address=spot.address,
                latitude=spot.mapy,
                longitude=spot.mapx,
                description=spot.description,
                overview = spot.overview,
                addr = spot.addr,
                image_url = spot.firstimage

            )
            for spot in spots.itertuples()
        ]
        models.Spot.objects.bulk_create(spots_bulk)

        print("[+] Done")

# lodging
        print("[*] Initializing lodging...")
        models.Lodging.objects.all().delete()
        lodgings = dataframes_lodging["lodgings"]
        lodgings_bulk = [
            models.Lodging(
                lodging_name=lodging.lodging_name,
                lodging_type=lodging.lodging_type,
                address=lodging.new_address,
                latitude=lodging.latitude,
                longitude=lodging.longitude,
                description=lodging.description,
                addr = lodging.addr
            )
            for lodging in lodgings.itertuples()
        ]
        models.Lodging.objects.bulk_create(lodgings_bulk)

        print("[+] Done")

# area
        print("[*] Initializing area...")
        models.Area.objects.all().delete()
        areas = dataframes_area["area"]
        area_bulk = [
            models.Area(
                id = area.id,
                city_name=area.cityName,
                address=area.address,
                latitude=area.latitude,
                longitude=area.longitude
            )
            for area in areas.itertuples()
        ]
        models.Area.objects.bulk_create(area_bulk)

        print("[+] Done")


    def handle(self, *args, **kwargs):
        self._initialize()