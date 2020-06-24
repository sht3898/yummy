<template>
  <v-container fluid class="py-0">
    <div>
    <v-row no-gutters justify="space-between" align="center">
          <v-col md="12" sm="12" xs="12">
             <div class="body-2" style="text-align:center;"> </div>
           <v-card style="margin:2px 2px auto;" outlined>
      <carousel :per-page="1" :mouse-drag="false" :autoplay='true' :loop='true' :autoplayHoverPause='false' :pagination-enabled='false' :autoplay-timeout='5000'>
        <slide v-for="(rec,idx) in recommend" :key="idx">
          <div class="slide" :style='{ backgroundImage: "url(" +rec.image + ")", }'> 
            <v-list-item-content class="mx-2 white--text font-weight-black">
              <div class="body-1" style="margin-top: 140px;" >{{rec.description}}</div>
              <v-list-item-title class="display-1 font">{{rec.title}}</v-list-item-title>
              
            </v-list-item-content>
            <v-btn outlined class="mx-2 xt-1" color="white" large @click="detailPage(rec.url)">둘러보기</v-btn>
          </div>
        </slide>
      </carousel>
        </v-card>
          </v-col>
          <v-col md="12" sm="12" xs="12" class="pt-2 pb-2">
            <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
          </v-col>
        <template v-for="(item,i) in area">
      <v-col md="3" sm="6" xs="12" :key="i">
        <v-hover v-slot:default="{ hover }">
        <v-card 
              :class="{ 'on-hover': hover }" style="margin:2px 2px auto;"
              @click="goto(i)">
          <v-img
            class="white--text align-end"
            height="200px"
            :src="item.image"
            gradient="to bottom, rgba(100,115,201,.13), rgba(25,32,72,.7)"
          >
            <v-list-item-content class="mx-2 pb-5">
              <div class="caption">{{item.description}}</div>
              <v-list-item-title class="headline mb-1">{{item.name}}</v-list-item-title>
            </v-list-item-content>
          </v-img>
        </v-card>
        </v-hover>
      </v-col>
        </template>
    </v-row>
  </div>
  </v-container>
</template>

<script>
  import router from "../router";
export default {
  name: "PlannerList",
  data() {
    return {
      area: [
              {
        name:"서울",
        image:"https://korean.visitseoul.net/comm/getImage?srvcId=MEDIA&parentSn=22372&fileTy=MEDIA&fileNo=1",
        description:"I SEOUL YOU",
      },
        {
        name:"대전 세종",
        image:"https://t1.daumcdn.net/cfile/tistory/18041F36500868CB27",
        description:"첨단 과학도시, 행정도시",
      },
        {
        name:"인천",
        image:"https://www.1gan.co.kr/news/photo/201909/182087_123517_2036.jpg",
        description:"all ways INCHEON",
      },
        {
        name:"대구",
        image:"https://post-phinf.pstatic.net/MjAxODA3MDNfMjAy/MDAxNTMwNjE4NDU0NTcx.-KGHAhc6SH6VB_128mnJ81HXn5nlNN4xYWlSG7GreIwg.iut9GwpNstFQUQnIdv6Bgf8zhZG5e3RJezgZzVZfxv4g.JPEG/%EB%8C%80%EA%B5%AC%EC%97%AC%ED%96%89_%283%29.jpg?type=w1200",
        description:"colorful DAEGU",
      },
        {
        name:"광주",
        image:"http://www.gjtravel.or.kr/user/default/data/2019/01/003001_15477703900.042122001547770390.jpg",
        description:"Your Partner GWANGJU",
      },
        {
        name:"부산",
        image:"https://tour.busan.go.kr/upload_data/manage_img//136572869986325.jpg",
        description:"dynamic BUSAN",
      },
        {
        name:"울산",
        image:"https://file.mk.co.kr/meet/neds/2018/05/image_readtop_2018_309701_15264109223314742.jpg",
        description:"ULSAN for you",
      },
       
        {
        name:"충청",
        image:"https://img-wishbeen.akamaized.net/plan/1445586978961_%EB%8B%A8%EC%96%91%ED%8C%A8%EB%9F%AC%EA%B8%80%EB%9D%BC%EC%9D%B4%EB%94%A9.jpg",
        description:"놀러오세유",
      },
        {
        name:"전라",
        image:"https://img-wishbeen.akamaized.net/plan/1465249292998_plan_cover_image_ios.png",
        description:"또 가고싶은",
      },
        {
        name:"경상",
        image:"data:image/jpeg;base64,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",
        description:"아름다움을 간직한",
      },
        {
        name:"제주도",
        image:"https://post-phinf.pstatic.net/MjAxOTAyMTFfMTQ2/MDAxNTQ5ODQ4NDA1NTQy.WrpA1AaRhBTh1RTN5hSClmRaPWEId-0c1KtoI7vf--og.7_mEuBRmj3tz9aVUGrD44Yu-DfQPb6BYHKBnVsUd0Xkg.JPEG/%EC%A0%9C%EC%A3%BC%EB%8F%84-iStock-900801586.jpg?type=w1200",
        description:"내가 가고 싶은",
      },
        {
        name:"경기 강원",
        image:"https://t1.daumcdn.net/cfile/tistory/9915E7455CECF2EB38",
        description:"은근하게 빠져드는",
      },
        
      ],
      recommend:[
        {image:"https://t1.daumcdn.net/cfile/tistory/999CF54B5D97530B10",
        description:"친구랑 우정찾아",
        url:"4",
        title:"경주 1박 2일"},
        {image:"https://img.insight.co.kr/static/2017/10/18/700/11bg8ybgz1vywur2r4ty.jpg",
        description:"가족끼리 떠나는",
        url:"12",
        title:"순천 2박 3일"},
        {image:"https://post-phinf.pstatic.net/MjAxNzA4MTBfMjg4/MDAxNTAyMzQ5MDQxOTg0.lydkxATEPhMnmjYAbc7BsOTZRBJ8fSdCpOgZ27R7Q9Ug.ns3Ei7QWpjq_lOhGt_2twmjkokTQr3Oe84RBHeReBzgg.JPEG/%EB%8C%80%EC%A0%84_%2810%29.jpg?type=w1200",
        description:"노잼도시 아니라구 ..",
        title:"대전 당일치기",
        url:"14"},
      ]
    };
  },
  created() {},
  methods: {
    detailPage(id,url,description){
      router.push({name:"detailplan", params:{id:id}})
    },
    goto(idx){
      router.push({name:"plannerlistdetail", params:{where:this.area[idx].name, image:this.area[idx].image, description:this.area[idx].description}})
    }
  },
};
</script>

<style lang="scss" scoped>

.v-card {
  transition: opacity .4s ease-in-out;
}

.on-hover {
  opacity: 0.7;
 }
 .slide{
  background-size: cover;
  height:400px;
  width:auto;
  text-align: center;
}
</style>