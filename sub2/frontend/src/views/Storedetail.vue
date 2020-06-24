<template>
  <div style="padding:20px">
   <v-container fluid class="py-3">
     <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
      <v-row no-gutters justify="space-between" align="center">

        <v-col class="storeInfo" style="text-align:center; margin-top:5px;" cols="5">
          <div >
           <p style="font-size:3vw">{{detail.store_name}}</p>
            <p style="font-size:1vw">주 소 : {{detail.address}}</p>
            <p style="font-size:1vw">전화번호 : {{detail.tel}}</p>
            <v-chip v-for="category in detail.category_list" :key="category.id" class="mr-3 pa-2" color="#3498db"
              outlined pill>{{category}}</v-chip>
              <br />
            <p>사용자 평점 : {{avgscore}}</p>
          </div>
          <br />
  <p style="font-size:2.5vw; text-align:left;">블로그 리뷰</p>
          <div class="my-2" v-for="blog in blogs" :key="blog.id">
            <a :href="blog.link" target="_blank">
            <div v-html="blog.title"></div>
            </a>
            <div class="wordlimit" v-html="blog.description"></div>
            <!-- {{blog.title}} -->
          </div>
        </v-col>
        <v-col cols="2">

        </v-col>
          <v-col cols="4">
          <div class="map_wrap" style="height:30vw">
            <div id="map" style="width:100%;height:100%;position:relative;overflow:hidden;"></div>
          </div>
          </v-col>
          <v-col cols="1">

          </v-col>
      </v-row>
    </v-container>
  <div class="comments-container">
    
        <p style="font-size:2.5vw">평가</p>

        <ul id="comments-list" class="comments-list" v-if="reviews.length">
          <li v-for="review in reviews" :key="review.id">
            <div class="comment-main-level">
              <!-- Avatar -->
              <div class="comment-avatar"><img src="../img/default.jpg" alt=""></div>
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
export default {
  name: "StoreDetail",
    data(){
      return{
        next:0,
        detail:[],
        stars:[0,0,0,0,0],
        issubmit:false,
        check: {
        },
        blogs:[],
        selectdialog:false,
        reviews:[],
        map:null,
        explain:'',
        storenum:0,
        content:'',
        avgscore:0,
      }
    },
    created() {
      this.storenum = parseInt(localStorage.getItem("store_detail"))
      this.LoadDetail(this.storenum)
      },
    watch: {
      content: function (v) {
          this.checkForm();
      },
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
        axios.get(`http://i02b207.p.ssafy.io:8083/api/stores/${page}`)
        .then(res => {
          if (res.data.avg_score){
            this.avgscore = res.data.avg_score
            this.avgscore = this.avgscore.toFixed(1)
          }
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
          this.naverreview()
          this.naverimage()
        })
        .catch(() =>{
        })
      },

      RemoveReview(id){
        axios.delete(`http://i02b207.p.ssafy.io:8083/api/stores/reviews/${id}`)
        .then(res => {
          axios.get(`http://i02b207.p.ssafy.io:8083/api/stores/${this.storenum}`)
          .then(res => {
            this.reviews = res.data.review
            if (res.data.avg_score){
              this.avgscore = res.data.avg_score
              this.avgscore = this.avgscore.toFixed(1)
            }
          })
        })
      },

      naverreview() {
        axios.get(`http://i02b207.p.ssafy.io:8083/api/search/blog?type=store&id=${this.storenum}`)
        .then(res => {
          this.blogs = res.data.items
        })
      },
      submit(){
        if(this.issubmit){
          let form = new FormData()
          form.append('store', this.storenum)
          form.append('user', this.$store.state.userinfo.id)
          let rate = this.stars.reduce(( accumulator, currentValue ) => accumulator + currentValue, 0)
          form.append('total_score', rate)
          form.append('content', this.content)
          axios.post(`http://i02b207.p.ssafy.io:8083/api/stores/reviews/`, form)
          .then(Response => {
            axios.get(`http://i02b207.p.ssafy.io:8083/api/stores/${this.storenum}`)
            .then(res => {
              this.reviews = res.data.review
              this.content = ''
              this.stars = [0,0,0,0,0]
              if (res.data.avg_score){
                this.avgscore = res.data.avg_score
                this.avgscore = this.avgscore.toFixed(1)
              }
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
.map_wrap {position:relative;overflow:hidden;width:100%;height:30vh;}
.btn--ok {
    width: 30%;
    font-weight: 500;
    font-size: 1em;
    background-color: rgb(0, 0, 0);
    color: #fff;
    text-align:center;
    cursor:pointer;
    height: 40px;
    line-height: 30px;
    border-radius: 20px;
    box-shadow: 8px 8px 15px rgba(0, 0, 0, 0.35);
    &.disabled{
        background:#ccc;
    }
}
.wordlimit{
  white-space: normal; 
  line-height: 1.2; 
  height: 5em; 
  text-align: left;
  word-wrap: break-word; 
  display: -webkit-box;
  -webkit-line-clamp: 3; 
  -webkit-box-orient: vertical;
}
.comments-container {
	margin-top: 30px;
	width: 768px;
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
.comments-list:before {
	content: '';
	width: 2px;
	height: 100%;
	background: #c7cacb;
	position: absolute;
	left: 32px;
	top: 0;
}

.comments-list:after {
	content: '';
	position: absolute;
	background: #c7cacb;
	bottom: 0;
	left: 27px;
	width: 7px;
	height: 7px;
	border: 3px solid #dee1e3;
	-webkit-border-radius: 50%;
	-moz-border-radius: 50%;
	border-radius: 50%;
}
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
	-webkit-box-shadow: 0 1px 2px rgba(0,0,0,0.2);
	-moz-box-shadow: 0 1px 2px rgba(0,0,0,0.2);
	box-shadow: 0 1px 2px rgba(0,0,0,0.2);
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
	width: 680px;
	float: right;
	position: relative;
	-webkit-box-shadow: 0 1px 1px rgba(0,0,0,0.15);
	-moz-box-shadow: 0 1px 1px rgba(0,0,0,0.15);
	box-shadow: 0 1px 1px rgba(0,0,0,0.15);
}

.comments-list .comment-box:before, .comments-list .comment-box:after {
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
	border-color: transparent rgba(0,0,0,0.05);
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

.comment-box .comment-name.by-author, .comment-box .comment-name.by-author a {color: #03658c;}
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