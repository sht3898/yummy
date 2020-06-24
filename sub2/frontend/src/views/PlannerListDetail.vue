<template>
  <v-container fluid>
    <v-row no-gutters justify="space-between" align="center" class="py-3">
      <v-col md="12" sm="12" xs="12">
        <v-card style="margin:2px 2px auto;" outlined>
          <div :style='{ backgroundImage: "url(" +image + ")",}' id="img"> 
            <div class="picture">

            <v-list-item-content class="mx-2 white--text font-weight-black">
              <div class="body-1" style="margin-top: 140px;" >{{description}}</div>
              <v-list-item-title class="display-1">{{id}} 여행 플래너</v-list-item-title>
            </v-list-item-content>
            </div>
          </div>
        </v-card>
      </v-col>

        <v-progress-linear indeterminate color="grey" v-if="!isLoading"></v-progress-linear>
    </v-row>
    <hr style="border-top: 1px dashed lightgrey;" class="my-2"/>
    <v-row no-gutters justify="space-between" align="center" class="py-3" v-if="isLoading&noContent">
      <v-col md="12" sm="12" xs="12" class="pa-2" align="center" >
        등록된 플래너 중 '{{id}}'을 여행하는 일정이 없어요😥 <br/>나만의 여행을 만들러 가볼까요 ?<br>
        <v-btn large outlined class="mt-3" @click="Goplanner()">
          만들러 가기
        </v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters justify="space-between" align="center" class="py-3" v-if="isLoading&!noContent">
    <v-col md="3" sm="6" xs="12" class="pa-2 mb-3" v-for="i in this.results.length" :key="i">
      <plan-slide :plan="results[i-1]" />
    </v-col>
    <v-col cols="12">
      <v-pagination
                style="margin:10px"
                v-model="planpage"
                :length="pages"
                :total-visible="7"
                >
              </v-pagination>
    </v-col>
    </v-row>
  </v-container>
</template>

<script>
import router from "../router";
import axios from "axios";
import planSlide from "../components/home/PlanSlide"
export default {
  components:{
    planSlide
  },
  data() {
    return {
      id: -1,
      image:"",
      description:"",
      isLoading: false,
      noContent:true,
      area: {
        서울: [1],
        "대전 세종": [6, 8],
        인천: [4],
        대구: [3],
        광주: [5],
        부산: [2],
        울산: [7],
        충청: [
          58,
          59,
          60,
          61,
          62,
          63,
          64,
          65,
          66,
          67,
          68,
          69,
          70,
          71,
          72,
          73,
          74,
          75,
          76,
          77,
          78,
          79,
          80,
          81,
          82,
          83
        ],
        전라: [
          84,
          85,
          86,
          87,
          88,
          89,
          90,
          91,
          92,
          93,
          94,
          95,
          96,
          97,
          98,
          99,
          100,
          101,
          102,
          103,
          104,
          105,
          106,
          107,
          108,
          109,
          110,
          111,
          112,
          113,
          114,
          115,
          116,
          117,
          118,
          119
        ],
        경상: [
          120,
          121,
          122,
          123,
          124,
          125,
          126,
          127,
          128,
          129,
          130,
          131,
          132,
          133,
          134,
          135,
          136,
          137,
          138,
          139,
          140,
          141,
          142,
          143,
          144,
          145,
          146,
          147,
          148,
          149,
          150,
          151,
          152,
          153,
          154,
          155,
          156,
          157,
          158,
          159,
          160
        ],
        제주도: [161],
        "경기 강원": [
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30,
          31,
          32,
          33,
          34,
          35,
          36,
          37,
          38,
          39,
          40,
          41,
          42,
          43,
          44,
          45,
          46,
          47,
          48,
          49,
          50,
          51,
          52,
          53,
          54,
          55,
          56,
          57
        ]
      },
      pages:0,
      results: [],
      planpage:1,
      area_list:[],
    };
  },
  create() {
    this.isLoading = false;
  },
  mounted() {
    this.id = this.$route.params.where;
    this.description = this.$route.params.description;
    this.image = this.$route.params.image;
    if (typeof this.id === "undefined" || this.id === null) {
      router.push({ name: "plannerlist" });
    }
    else{
      this.area_list = this.area[this.id].join(",");
    axios
      .get(`http://i02b207.p.ssafy.io:8083/api/search/plans/?area=${this.area_list}`)
      .then(res => {
        this.isLoading = true;
        this.results = []
        this.pages = Math.ceil(res.data.count/12)
        if (res.data.count ==0){
          this.noContent=true;
        }else{
          this.noContent=false;
        }
        this.results = res.data.results
      })
      .catch(Error => {

        alert("잠시 후에 다시 시도해주세요.");
        router.push({
          name: "plannerlist"
      });
      });
    }
  },
  methods: {
    Goplanner() {
      router.push({
        name:"createplan"
      })
    },
  },
  watch:{
    planpage:function (val){
      axios
      .get(`http://i02b207.p.ssafy.io:8083/api/search/plans/?area=${this.area_list}&page=${this.planpage}`)
      .then(res => {
        this.isLoading = true;
        this.results = []
        this.pages = Math.ceil(res.data.count/12)
        if (res.data.count ==0){
          this.noContent=true;
        }else{
          this.noContent=false;
        }
        this.results = res.data.results
      })
      .catch(Error => {
        alert("잠시 후에 다시 시도해주세요.");
        router.push({
          name: "plannerlist"
      });
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.v-card {
  transition: opacity 0.4s ease-in-out;
}

.on-hover {
  opacity: 0.7;
}
#img {
  background-size: cover;
  height: 400px;
  width: auto;
  text-align: center;
  z-index:1;
}

.picture {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
 border: 10px solid rgba(255, 255, 255, 0.5);
        margin: 10px;
        z-index: 2;

}
</style>