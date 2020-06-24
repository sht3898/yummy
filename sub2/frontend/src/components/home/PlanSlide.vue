<template>
  <v-card style="z-index:5" max-width="300" class="mx-auto">
    <div @click="goDetailPage()">
    <map-info :areaList="this.plan.area_list" :id="this.plan.id" />
    </div>
    <v-card-title>
      <button @click="goDetailPage()"> 
      <p class="my-auto ml-2 title" > {{ this.altertitle }} </p>
      <v-chip class="my-auto" style="background-color:#3498db" dark label >일정 : {{ this.plan.days }}일 </v-chip>
      </button>
      <v-spacer />
      <button style="z-index:10" @click="kakaoshare()">
      <v-img src="//developers.kakao.com/assets/img/about/logos/kakaolink/kakaolink_btn_medium.png" width="40px" height="40px" contain />
      </button>

    </v-card-title>
    <v-card-text >
      
    </v-card-text>
  </v-card>
</template>

<script>
import router from '../../router'
import mapInfo from './MapInfo'

export default {
  name:"planslide",
  props:{
    plan:{ type:Object },
  },
   data() {
    return {
      altertitle:'',
    }
  },
  components:{
    mapInfo
  },
  created(){
    if (this.plan.title.length > 9){
      this.altertitle = this.plan.title.substr(0,9)+"..."
    }else{
      this.altertitle = this.plan.title;
    }
  },
  methods:{
    goDetailPage(){
      let id = this.plan.id
      router.push({name:"detailplan", params:{"id":id}})
    },
    kakaoshare(){
      Kakao.Link.sendDefault({
        objectType: 'feed',
        content: {
          title: this.plan.title, 
          description: '#여행 #맛집 #호텔 #음식 #분위기 #계획', 
          imageUrl: 'https://images.unsplash.com/photo-1502920514313-52581002a659?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1047&q=80', // 이미지
          link: { 
            mobileWebUrl:`http://i02b207.p.ssafy.io/planner/detail/${this.plan.id}`,
            webUrl: `http://i02b207.p.ssafy.io/planner/detail/${this.plan.id}` }
        },
        buttons: [
          {
            title: '플랜 확인',
            link: { 
              mobileWebUrl:`http://i02b207.p.ssafy.io/planner/detail/${this.plan.id}`,
              webUrl: `http://i02b207.p.ssafy.io/planner/detail/${this.plan.id}`}
          },
        ],
        success: function(response) {
          console.log(response);
        },
        fail: function(error) {
          console.log(error);
        }
      });
    }
  }
}
</script>

<style>

</style>