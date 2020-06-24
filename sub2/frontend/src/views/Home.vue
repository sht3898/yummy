<template>
  <div>
    <header>
      <nav id="dis" class='fixedheader'>
        <ul style="background-color:#fcfcfc">
          <li style="float:left;">
            <button class="mx-1 navbtnlogo title" @click="goHome">
              Y
              <b style="color:#3498db">U</b> M M Y
            </button>
          </li>
          <v-spacer></v-spacer>
          <li>
            <button class="mx-1 navbtn" @click="goHome">홈</button>
          </li>
          <li>
            <button class="mx-1 navbtn" @click="GoStore">탐색</button>
          </li>
          <li>
            <button class="mx-1 navbtn" @click="GoPlannerList">플래너</button>
          </li>
          <li v-if="$store.state.isLogin==false">
            <button class="mx-1 navbtn" style="color:#3498db;" @click.stop="$store.state.dialog = true">로그인</button>
          </li>
        <li v-if="$store.state.isLogin==true">
            <button @click="goVerify" class="mx-1 navbtn">회원정보</button></li>
            <li v-if="$store.state.isLogin==true">
            <button @click="$store.dispatch('logout')" class="mx-1 navbtn">로그아웃</button>
          </li>
        </ul>
      </nav>
      <div class="header-banner">
        <carousel
          :per-page="1"
          :mouse-drag="false"
          :autoplay="true"
          :loop="true"
          :autoplayHoverPause="false"
          :pagination-enabled="false"
          :autoplay-timeout="5000"
        >
          <slide style="opacity: 0.9;" v-for="(bg,i) in backgrounds" :key="i">
            <div class="slide_1" :style="{ backgroundImage: 'url(' +bg.image + ')', }">
              <div class="mt-4 mb-4">
                <p>
                  {{ bg.description1 }}
                  <br />
                  {{ bg.description2 }}
                </p>
              </div>
            </div>
          </slide>
        </carousel>
      </div>
    </header>
    <v-dialog
      background-color="black"
      v-model="$store.state.dialog"
      z-index="3"
      overlay-opacity="1"
      width="50%"
      style="position:absolute; top:0; left:0; right:0; bottom:0; width:50%; height:50%;"
    >
      <LoginModal />
    </v-dialog>

    <v-container fluid class="py-3">
      <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
      <v-row no-gutters justify="space-between" align="center">
        <v-col md="6" sm="12" xs="12">
          <v-card
            outlined
            align="center"
            style="border:0px"
            @click="GoStore()"
            class="black--text cards"
            height="200px"
          >
            <v-list-item-content class="mx-2 my-4 pb-5">
              <div class="title my-1" style="color:#2c3e50">어디를 가야 좋을까</div>
              <v-list-item-title class="display-1 mb-1" style="color:#2c3e50">맛집 · 관광지 정보</v-list-item-title>
            </v-list-item-content>
            <v-btn outlined style="color:#2c3e50; width:150px;" large>보러가기</v-btn>
          </v-card>
        </v-col>
        <v-col md="6" sm="12" xs="12">
          <v-card
            outlined
            align="center"
            style="border:0px"
            @click="goPlanner()"
            class="black--text cards"
            height="200px"
          >
            <v-list-item-content class="mx-2 my-4 pb-5">
              <div class="title my-1" style="color:#2c3e50">모든게 계획대로야</div>
              <v-list-item-title class="display-1 mb-1" style="color:#2c3e50">나만의 여행플래너</v-list-item-title>
            </v-list-item-content>
            <v-btn outlined style="color:#2c3e50; width:150px;" large>계획짜기</v-btn>
          </v-card>
        </v-col>
      </v-row>
      <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
      <v-row no-gutters justify="space-between" align="center">
        <v-col @click="GoPlannerList()" cols="6">
          <div align="center" style="border:0px; #2c3e50" class="cards" height="400px">
            <div class="mx-2 pb-5" height="350px">
              <div class="title my-1" style="color:#2c3e50">지역별로 나눠보는</div>
              <div class="display-1 mb-1" style="color:#2c3e50">여행 리스트</div>
            </div>
            <v-btn outlined style="color:#2c3e50; width:150px;" large>구경가기</v-btn>
          </div>
        </v-col>
        <v-col @click="GoPlannerList()" cols="6">
          <v-card outlined align="right" style="border:0px" class="cards" height="400px">
            <v-img src="https://ifh.cc/g/AwkWYJ.png" style="background-size: cover; height:400px;"></v-img>
          </v-card>
        </v-col>
      </v-row>
      <hr style="border-top: 1px dashed lightgrey;" class="my-2"  v-if="$store.state.isLogin" />
      <v-row no-gutters justify="space-between" align="center" v-if="$store.state.isLogin">
        <v-col md="12" sm="12" xs="12">
          <div class="my-4 mx-2 mb-4 display-1" style="text-align:center;">내 경로</div>
        </v-col>
        <v-col md="12" sm="12" xs="12">
          <carousel :perPage="itemNum" :autoplay="true" :loop="true" :paginationEnabled="false" v-if="this.myPlans.length>0">
            <slide v-for="i in this.myPlans.length" :key="i">
              <plan-slide :plan="myPlans[i-1]" />
            </slide>
          </carousel>
          <div v-else class="my-4 title" style="text-align:center;">
            등록된 플랜이 없네요 ..
          </div>
        </v-col>
      </v-row>
      <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
      <v-row no-gutters justify="space-between" align="center">
        <v-col md="12" sm="12" xs="12">
          <div class="my-4 mx-2 mb-4 display-1" style="text-align:center;">다른 여행자들의 플래너</div>
        </v-col>
        <v-col md="12" sm="12" xs="12" class="my-4" v-if="isLoading" align="center">
          <v-progress-circular indeterminate color="#dddddd" ></v-progress-circular>
        </v-col>
        <v-col md="12" sm="12" xs="12" class="my-4" v-else>
          <carousel :perPage="itemNum" :autoplay="true" :loop="true" :paginationEnabled="false">
            <slide v-for="i in this.otherPlans.length" :key="i">
              <plan-slide :plan="otherPlans[i-1]" />
            </slide>
          </carousel>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
import router from "../router";
import { mapState, mapActions } from "vuex";
import { Carousel, Slide } from "vue-carousel";
import LoginModal from "../components/header/appbar/LoginModal";
import planSlide from "../components/home/PlanSlide";


export default {
  components: {
    Carousel,
    Slide,
    LoginModal,
    planSlide
  },
  methods: {
    goPlanner() {
      router.push({
        name: "createplan"
      });
    },
    GoStore() {
      router.push({
        name: "storelist"
      });
    },
    GoPlannerList() {
      router.push({
        name: "plannerlist"
      });
    },
    fixheader() {
      if (this.scroll >= 500) {
        this.isfixed = true;
      } else {
        this.isfixed = false;
      }
    },
    goHome() {
      router.push({ name: "home" });
    },
    goVerify() {
      router.push({
        name: "verify"
      });
    },
    Modaloff(val) {
      this.dialog = val;
    },
    fixheader() {
      this.scroll >= 500 ? (this.isfixed = true) : (this.isfixed = false);
    },
    otherPlanLoader() {
      axios.get('http://i02b207.p.ssafy.io:8083/api/plans/')
        .then(response => {
          this.otherPlans = response.data.results
          this.isLoading=false
        })
    },
    myPlanLoader() {
      if (this.$store.state.userinfo){
        axios.get('http://i02b207.p.ssafy.io:8083/api/plans/', {params: { user: this.$store.state.userinfo.id}})
          .then(response => {
            this.myPlans = response.data.results
            this.isLoading = false
          })
      }
    },
    calItemNum() {
      if (window.innerWidth > 1280) this.itemNum = 4;
      else if (window.innerWidth > 640) this.itemNum = 2;
      else this.itemNum = 1;
    }
  },
  data() {
    return {
      scroll: 0,
      isfixed: false,
      drawer: false,
      dialog: false,
      otherPlans: [],
      myPlans: [],
      searchtext:'',
      itemNum: 4,
      isLoading:true,
      backgrounds: [
        {
          image: "https://ifh.cc/g/JKKI63.jpg",
          description1: "여행 계획 세울땐 ?",
          description2: " Y U M M Y "
        },
        {
          image: "https://ifh.cc/g/D4JrY6.jpg",
          description1: "맛있는",
          description2: "여행을 떠나자"
        },
        {
          image: "https://ifh.cc/g/yn0r40.jpg",
          description1: "일 상 탈 출",
          description2: "어 디 갈 까"
        }
      ]
    };
  },
  created() {
    this.scroll = window.scrollY;
    window.addEventListener("scroll", () => {
      this.scroll = window.scrollY;
    });
    this.$store.state.viewnav = false;
    window.addEventListener("resize", () => {
      this.calItemNum();
    });
  },
  destroyed() {
    this.$store.state.viewnav = true;
  },
  mounted() {
    Kakao.Link.createDefaultButton, this.otherPlanLoader();
    this.myPlanLoader();
    this.calItemNum();
  },
  watch: {
    scroll: {
      handler: "fixheader"
    }
  }
};
</script>
<style lang="scss" scoped>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: 0.6;
  position: absolute;
  width: 100%;
}

body {
  margin: 0px;
  padding: 0px;
}

@import "https://fonts.googleapis.com/css?family=Baloo+Paaji";

p {
  text-align: right;
  font-size: 55px;
  color: white;
  font-weight: bold;
  margin-right: 50px;
}
/* main */
header {
  height: 500px;
  position: relative;
  top: 0;
}

.header-banner {
  // background-color: #333;
  // background-image: url('https://37.media.tumblr.com/8b4969985e84b2aa1ac8d3449475f1af/tumblr_n3iftvUesn1snvqtdo1_1280.jpg');
  // background-position: center;
  // background-repeat: no-repeat;
  // background-size: cover;
  width: 100%;
  height: 480px;
  margin-bottom: 0;
  position: relative;
  top: 0;
}

.slide_1 {
  background-size: cover;
  text-align: center;
  height: 450px;
  padding-top: 10%;
}

.fixedheader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
}

nav {
  width: 100%;
  height: 60px;
  z-index: 10;
}
.navbtnlogo {
  color: black;
  width: 130px;
  font-weight: bold;
}
.navbtn {
  color: #2c3e50;
  width: 80px;
  font-weight: bold;
}
.navbtn:hover {
  font-weight: bold;
  color: #3498db;
}
nav div {
  font-size: 2rem;
  line-height: 60px;
  position: absolute;
  top: 0;
  left: 2%;
  visibility: hidden;
}

nav ul {
  list-style-type: none;
  padding: 0 2% auto 0;
  padding-left: 0;
  text-align: right;
  max-width: 100%;
}

nav ul li {
  display: inline-block;
  line-height: 60px;
  margin: 0px 10px 0px;
}
.cards {
  margin: 2px 2px auto;
  background-color: transparent;
}
 .search{
  position: relative;
}
.search input {
  background-color: transparent;
  -webkit-transition: all 100ms ease-in-out;
     -moz-transition: all 100ms ease-in-out;
      -ms-transition: all 100ms ease-in-out;
       -o-transition: all 100ms ease-in-out;
          transition: all 100ms ease-in-out;
  position:relative;
  color: transparent;
  border: 2px solid rgb(0, 0, 0);
  border-radius: 20px;
  padding: 10px 30px 10px 15px;
  outline: 0 none;
  width: 60px;
  height: 40px;
  
  -webkit-transform: translateZ(1px);
     -moz-transform: translateZ(1px);
      -ms-transform: translateZ(1px);
       -o-transform: translateZ(1px);
          transform: translateZ(1px);
  z-index: 2;
}
.search input:focus {
  width: 200px;
  color: rgb(7, 7, 7);
}
</style>