<template>
  <div class="font">
    <div style="padding:20px">
      <v-container>
        <v-row>
          <v-col class="mb-3">
            <p style="font-size:3vw">{{detail.spot_name}}</p>
            <p style="font-size:1vw">{{detail.spot_name}}</p>
            <p v-html="detail.description"></p>
          </v-col>
        </v-row>
        <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
        <v-row class="my-5">
          <v-col cols="9" md="10" style="height:54px">
            <v-text-field v-model="explain" single-line label="다른 계획 이름이 필요하다면 입력해주세요" />
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="2" md="1" align-self="center" style="height:54px">
            <v-btn @click="addplan()" dark color="#3498db">일정 추가</v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class="mb-0" style="font-size:1.6vw">일정시작시간</p>
            <v-time-picker v-model="startTime" :max="endTime" full-width color="#3498db"></v-time-picker>
          </v-col>
          <v-col>
            <p class="mb-0" style="font-size:1.6vw">일정종료시간</p>
            <v-time-picker v-model="endTime" :min="startTime" full-width color="#3498db"></v-time-picker>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="storeInfo" style="text-align:center; margin-top:5px;">
            <div class="map_wrap" style="height:22vw">
              <div id="map" style="width:100%;height:100%;position:relative;overflow:hidden;"></div>
            </div>
          </v-col>
        </v-row>
      </v-container>
      <spotRecommend :spotnum="spotnum" />
      <div class="comments-container">
        <p style="font-size:2.5vw">평가</p>

        <ul id="comments-list" class="comments-list" v-if="reviews.length">
          <li v-for="review in reviews" :key="review.id">
            <div class="comment-main-level">
              <!-- Avatar -->
              <div class="comment-avatar"><img src="../../../img/default.jpg" alt=""></div>
              <!-- Contenedor del Comentario -->
              <div class="comment-box">
                <div class="comment-head">
                  <h6 v-if="review.user == $store.state.userinfo.id" class="comment-name by-author">{{review.nickname}}
                  </h6>
                  <h6 v-else class="comment-name">{{review.nickname}}</h6>
                  <h6 class="comment-name">평점 : {{review.total_score}}</h6>
                  <button v-if="review.user == $store.state.userinfo.id" @click="RemoveReview(review.id)"
                    style="float:right; color:#e74c3c;">삭제</button>
                </div>
                <div class="comment-head">
                  {{review.content}}
                </div>
              </div>
            </div>
          </li>
        </ul>
        <div v-else style="text-align:center" class="px-auto">
          작성된 평가가 없습니다.
        </div>
      </div>
      <v-container style="margin-top:60px">
        <v-row>
          <v-col class="px-0">
            <span style="text-align:center;">별 점 : </span>
            <span v-for="i in stars.length" :key="i">
              <v-btn v-if="stars[i-1]==1" small icon style="color:#3498db" @click="checkStar(i-1)">
                <v-icon>mdi-star</v-icon>
              </v-btn>
              <v-btn v-else small icon @click="checkStar(i-1)">
                <v-icon>mdi-star</v-icon>
              </v-btn>
            </span>
          </v-col>
          <v-spacer></v-spacer>
          <v-col class="px-0" cols="2" md="1">
            <v-btn v-on:click="submit" :disabled="!issubmit" :class="{disabled : !issubmit}" outlined color="#3498db">
              작성하기
            </v-btn>
          </v-col>

        </v-row>
        <v-row>
          <v-col class="px-0">
            <v-textarea outlined label="댓글 입력" single-line v-model="content" no-resize></v-textarea>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import spotRecommend from './spotRecommend'
export default {
  name: "spotdetail",
  components:{
    spotRecommend
  },
  props:{
    spotnum:{
        type:Number,
        required:true
    },
    events:{
      type:Array,
      
    },
    plandate:{
      type:String,
    }
  },
  data(){
    return{
      startTime:null,
      endTime:null,
      content:'',
      next:0,
      detail:[],
      stars:[0,0,0,0,0],
      issubmit:false,
      check: {
      },
      selectdialog:false,
      reviews:[],
      map:null,
      explain:'',
      recommend:[],
    }
  },
  mounted() {
    this.LoadDetail(this.spotnum)
  },
  watch: {
    content: function (v) {
        this.checkForm();
    },
    spotnum: function(v) {
      this.LoadDetail(this.spotnum)
    }
  },

  methods:{
    checkForm() {
      if(this.content.length < 1){
        this.check.content = '1자이상'
      }
      else{
        this.check.content = false;
      }
      let issubmit = true
      Object
      .values(this.check)
      .map(v => {
        if (v) 
        issubmit = false;
      })
      this.issubmit = issubmit;
    },

    LoadDetail(page){
      axios.get(`http://i02b207.p.ssafy.io:8083/api/spots/${page}`)
      .then(res => {
        this.detail = res.data.detail
        this.reviews = res.data.review
        var container = document.getElementById('map')
        var mapOptions = {
          center: new kakao.maps.LatLng(this.detail.latitude, this.detail.longitude),
          level: 5
        }
        var marker = new kakao.maps.Marker({
            position: new kakao.maps.LatLng(this.detail.latitude, this.detail.longitude),
        })
        this.map = new kakao.maps.Map(container, mapOptions)
        marker.setMap(this.map)
      })
      .catch(() => {
      })
    },

    RemoveReview(id){
      axios.delete(`http://i02b207.p.ssafy.io:8083/api/spots/reviews/${id}`)
      .then(res => {
        axios.get(`http://i02b207.p.ssafy.io:8083/api/spots/${this.spotnum}`)
        .then(res => {
          this.reviews = res.data.review
        })
      })
    },

    addplan() {
      if (this.startTime && this.endTime){
        this.events.push({
          start: `${this.plandate} ${this.startTime}`,
          end: `${this.plandate} ${this.endTime}`,
          title: this.explain?this.explain:this.detail.spot_name,
          class: 'spot',
          content: this.spotnum
        })
        this.startTime = null
        this.endTime = null
        this.explain = null
        this.$emit('toggle')
      }
      else{
        alert('시간을 선택해주세요')
      }
    },

    submit(){
      if(this.issubmit){
        let form = new FormData()
        form.append('spot', this.spotnum)
        form.append('user', this.$spot.state.userinfo.id) 
        let rate = this.stars.reduce(( accumulator, currentValue ) => accumulator + currentValue, 0)
        form.append('total_score', rate)
        form.append('content', this.content)
        axios.post(`http://i02b207.p.ssafy.io:8083/api/spots/reviews/`, form)
        .then(Response => {
          axios.get(`http://i02b207.p.ssafy.io:8083/api/spots/${this.spotnum}`)
          .then(res => {
            this.reviews = res.data.review
            this.content = ''
            this.stars = [0,0,0,0,0]
          })
        })
        .catch(() => {
        })
      }
    },
    checkStar(idx){
      for (var i=0; i<=idx; i++){
        this.stars[i] = 1
      }
      for (var i=idx+1; i<5; i++){
        this.stars[i] = 0
      }
      this.stars.push()
    },
  },
}
</script>

<style lang="scss" scoped>
  .map_wrap {
    position: relative;
    overflow: hidden;
    width: 100%;
    height: 30vh;
  }

  .btn--ok {
    width: 30%;
    font-weight: 500;
    font-size: 1em;
    background-color: rgb(0, 0, 0);
    color: #fff;
    text-align: center;
    cursor: pointer;
    height: 40px;
    line-height: 30px;
    border-radius: 20px;
    box-shadow: 8px 8px 15px rgba(0, 0, 0, 0.35);

    &.disabled {
      background: #ccc;
    }
  }

  * {
    margin: 0;
    padding: 0;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }

  a {
    color: #03658c;
    text-decoration: none;
  }

  ul {
    list-style-type: none;
  }


  /** ====================
 * Lista de Comentarios
 =======================*/
  .comments-container {
    margin: 30px 0px 15px;
  }

  .comments-container h1 {
    font-size: 36px;
    color: #283035;
    font-weight: 400;
  }

  .comments-container h1 a {
    font-size: 18px;
    font-weight: 700;
  }

  .comments-list {
    margin-top: 30px;
    position: relative;
  }

  /**
 * Lineas / Detalles
 -----------------------*/

  .comments-list li {
    margin-bottom: 15px;
    display: block;
    position: relative;
  }

  .comments-list li:after {
    content: '';
    display: block;
    clear: both;
    height: 0;
    width: 0;
  }

  .comments-list .comment-avatar {
    width: 65px;
    height: 65px;
    position: relative;
    z-index: 99;
    float: left;
    border: 3px solid #FFF;
    -webkit-border-radius: 4px;
    -moz-border-radius: 4px;
    border-radius: 4px;
    -webkit-box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    -moz-box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    overflow: hidden;
  }

  .comments-list .comment-avatar img {
    width: 100%;
    height: 100%;
  }

  .comment-main-level:after {
    content: '';
    width: 0;
    height: 0;
    display: block;
    clear: both;
  }

  /**
 * Caja del Comentario
 ---------------------------*/
  .comments-list .comment-box {
    width: 98vh;
    float: right;
    position: relative;
    -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
    -moz-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
  }

  .comments-list .comment-box:before,
  .comments-list .comment-box:after {
    content: '';
    height: 0;
    width: 0;
    position: absolute;
    display: block;
    border-width: 10px 12px 10px 0;
    border-style: solid;
    border-color: transparent #FCFCFC;
    top: 8px;
    left: -11px;
  }

  .comments-list .comment-box:before {
    border-width: 11px 13px 11px 0;
    border-color: transparent rgba(0, 0, 0, 0.05);
    left: -12px;
  }

  .comment-box .comment-head {
    background: #FCFCFC;
    padding: 10px 12px;
    border-bottom: 1px solid #E5E5E5;
    overflow: hidden;
    -webkit-border-radius: 4px 4px 0 0;
    -moz-border-radius: 4px 4px 0 0;
    border-radius: 4px 4px 0 0;
  }

  .comment-box .comment-head i {
    float: right;
    margin-left: 14px;
    position: relative;
    top: 2px;
    color: #A6A6A6;
    cursor: pointer;
    -webkit-transition: color 0.3s ease;
    -o-transition: color 0.3s ease;
    transition: color 0.3s ease;
  }

  .comment-box .comment-head i:hover {
    color: #03658c;
  }

  .comment-box .comment-name {
    color: #283035;
    font-size: 14px;
    font-weight: 700;
    float: left;
    margin-right: 10px;
  }

  .comment-box .comment-name a {
    color: #283035;
  }

  .comment-box .comment-head span {
    float: left;
    color: #999;
    font-size: 13px;
    position: relative;
    top: 1px;
  }

  .comment-box .comment-content {
    background: #FFF;
    padding: 12px;
    font-size: 15px;
    color: #595959;
    -webkit-border-radius: 0 0 4px 4px;
    -moz-border-radius: 0 0 4px 4px;
    border-radius: 0 0 4px 4px;
  }

  .comment-box .comment-name.by-author,
  .comment-box .comment-name.by-author a {
    color: #03658c;
  }

  .comment-box .comment-name.by-author:after {
    content: 'autor';
    background: #03658c;
    color: #FFF;
    font-size: 12px;
    padding: 3px 5px;
    font-weight: 700;
    margin-left: 10px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
  }

  /** =====================
 * Responsive
 ========================*/
  @media only screen and (max-width: 766px) {
    .comments-container {
      width: 480px;
    }

    .comments-list .comment-box {
      width: 390px;
    }
  }
</style>