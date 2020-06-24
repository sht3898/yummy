<template>
  <div>
    <header v-if="$store.state.viewnav == true">
      <nav>
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
            <button class="mx-1 navbtn"  style="color:#3498db;" @click.stop="$store.state.dialog = true">로그인</button>
          </li>
          <li v-if="$store.state.isLogin==true">
            <button @click="goVerify" class="mx-1 navbtn">회원정보</button></li>
            <li v-if="$store.state.isLogin==true">
            <button @click="$store.dispatch('logout')" class="mx-1 navbtn">로그아웃</button>
          </li>
        </ul>
      </nav>
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
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import LoginModal from "./appbar/LoginModal";
import router from "../../router";
import { Carousel, Slide } from "vue-carousel";
export default {
  name: "AppBar",
  components: {
    LoginModal,
    Carousel,
    Slide
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    goHome() {
      router.push({ name: "home" });
    },
    goplanner() {
      router.push({ name: "planner" });
    },
    goVerify() {
      router.push({ name: "verify" });
    },
    Modaloff(val) {
      this.dialog = val;
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
    }
  }
};
</script>

<style lang="scss" scoped>
 @import 'https://fonts.googleapis.com/css?family=Baloo+Paaji';

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

</style>