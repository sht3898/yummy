<template>
  <v-container class="py-0">
    <v-row>
      <v-col cols="3">
        <v-text-field v-model="planTitle" />
      </v-col>
      <v-col cols="5" align-self="center">
        <v-btn style="background-color:#2ecc71;" @click="setToggle" v-if="toggle">세부일정 선택</v-btn>
        <v-btn style="color:#2ecc71;" text @click="setToggle" v-else>전체일정 선택</v-btn>
        
        <v-btn class="ml-3" style="background-color:#3498db;" dark v-if="$store.state.isLogin" @click="savePlan">새로 저장하기</v-btn>
        <v-btn class="ml-3" style="color:#3498db;" disabled v-else>새로 저장하기</v-btn>
        <v-btn class="ml-3" style="color:#3498db;" outlined v-if="$store.state.isLogin && $store.state.userinfo.id == userId" @click="modifyPlan">수정하기</v-btn>
        <v-btn class="ml-3" style="color:#e74c3c;" outlined v-if="$store.state.isLogin && $store.state.userinfo.id == userId" @click="deletePlan">삭제하기</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5" md="2" class="py-0" style="bor">
          
        <date-plan :datePlan="datePlan" :destinations="destinations" />
        <time-line :destinations="destinations" :datePlan="datePlan" />
      </v-col>
      <v-col cols="7" md="10" class="py-0" v-if="toggle==true">
        <select-map :destinations="destinations" :datePlan="datePlan" />
      </v-col>
      <v-col cols="7" md="10" class="py-0"  v-if="toggle==false && destinations.length">
        <time-table @update="updateDetailPlan" :destinations="destinations" :datePlan="datePlan" :detailPlan="detailPlan" :events="events" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import router from '../router'
import DatePlan from "../components/commonplan/DatePlan"
import TimeLine from "../components/commonplan/TimeLine"
import SelectMap from "../components/commonplan/SelectMap"
import TimeTable from "../components/detailplan/TimeTable"


export default {
  name:"detailPlan",
  components:{
    DatePlan,
    TimeLine,
    SelectMap,
    TimeTable,
  },
  data(){
    return{
    toggle:true,
    destinations:[],
    datePlan:{
      start : new Date().toISOString().substr(0, 10),
      end : null,
    },
    detailPlan:[],
    planTitle:"",
    userId : "",
    events:[]
    }
  },
  methods:{
    setDetailPlan(){
      let start = this.datePlan.start
      let end = this.datePlan.end
      let tmp = []
      if (end){
        let a = new Date(end)
        let b = new Date(start)
        let days = parseInt((a-b)/1000/3600/24)
        b.setDate(b.getDate() - 1)
        for (let i=0; i<=days; i++){
          var startDate = b
          startDate.setDate(startDate.getDate() + 1)
          var temp = []
          for (let j=0; j<this.destinations.length; j++){
            let c = new Date(this.destinations[j][2])
            let d = new Date(this.destinations[j][3])
            if (0 <= startDate-c && 0 <= d-startDate){
              temp.push(this.destinations[j][0])
            }
          }
          tmp.push({
            date:startDate.toISOString().substr(0, 10),
            area:temp,
            itinerarys:[]
          })
        }
      }
      this.detailPlan = tmp
    },
    setToggle(){
      if (this.toggle){
        if (this.destinations.length > 0)
          this.toggle = false
        else
          alert('여행지를 선택해주세요!!')
      }
      else
        this.toggle = true
    },
    savePlan(){
      var temp = {
        "plans": {
          "title": this.planTitle,
          "start_date": this.datePlan.start,
          "end_date": this.datePlan.end,
        },
        "user_id":this.$store.state.userinfo.id,
        "plan_id":this.$route.params.id,
        "days": this.detailPlan
      }
      axios.put("http://i02b207.p.ssafy.io:8083/api/plan/all/", temp)
      .then(res=>{
        alert("저장이 완료되었습니다.")
      })
      .catch(()=>{
        alert("저장중 문제가 발생하였습니다.")
      })
    },
    deletePlan(){
      axios.delete(`http://i02b207.p.ssafy.io:8083/api/plan/all/${this.$route.params.id}/`)
      .then(()=>{
        alert("삭제가 완료되었습니다.")
        router.push({name:"home"})
      })

    },
    modifyPlan(){
      var temp = {
        "plans": {
          "title": this.planTitle,
          "user":this.$store.state.userinfo.id,
          "start_date": this.datePlan.start,
          "end_date": this.datePlan.end,
        },
        "days": this.detailPlan
      }
      axios.patch(`http://i02b207.p.ssafy.io:8083/api/plan/all/${this.$route.params.id}/`, temp)
      .then(res=>{
        router.push({name:"detailplan", params:{id:this.$route.params.id}})
        alert("수정이 완료되었습니다.")
      })
      .catch(()=>{
        alert("수정 중 문제가 발생하였습니다.")
      })
    },
    updateDetailPlan(events){
      if (Array.isArray(events)){
        let b = new Date(this.destinations[0][2])
        for (var j=0; j < this.detailPlan.length; j++){
          this.detailPlan[j].itinerarys = []
        }
        for (var i = 0; i < events.length; i++){
          let a = new Date(events[i].start)
          let c = new Date(events[i].end)
          var days = parseInt((a-b)/1000/3600/24)
          
          this.detailPlan[days].itinerarys.push({
            "start_time" : a.toTimeString().substring(0, 5),
            "end_time" : c.toTimeString().substring(0, 5),
            "title" : events[i].title,
            "store" : events[i].class=="store"?events[i].content:null,
            "spot" : events[i].class=="spot"?events[i].content:null,
            "lodging" : events[i].class=="lodging"?events[i].content:null
          })
        }
      }
    }
  },
  mounted(){
    axios.get(`http://i02b207.p.ssafy.io:8083/api/plan/all/${this.$route.params.id}`)
    .then(response =>{
      this.userId = response.data.user
      this.planTitle = response.data.title
      this.datePlan.start = response.data.start_date
      this.datePlan.end = response.data.end_date
      for (var i=0; i < response.data.planday_plan.length; i++){
        for (var j=0; j < response.data.planday_plan[i].area.length; j++){
          if (this.destinations.length == 0 || this.destinations[this.destinations.length-1][0] != response.data.planday_plan[i].area[j].id){
            this.destinations.push([
              response.data.planday_plan[i].area[j].id,
              response.data.planday_plan[i].area[j].city_name,
              response.data.planday_plan[i].date,
              response.data.planday_plan[i].date,
              0,
              {
                Ga:response.data.planday_plan[i].area[j].latitude,
                Ha:response.data.planday_plan[i].area[j].longitude
              }
            ])
          }
          else {
            this.destinations[this.destinations.length-1][3] = response.data.planday_plan[i].date
            this.destinations[this.destinations.length-1][4] += 1
          }
        }
        let itineraryDay = response.data.planday_plan[i].itinerary_day
        for (var j=0; j < itineraryDay.length; j++){
          this.events.push({
            start: `${response.data.planday_plan[i].date} ${itineraryDay[j].start_time}`,
            end: `${response.data.planday_plan[i].date} ${itineraryDay[j].end_time}`,
            title: itineraryDay[j].title,
            class: itineraryDay[j].store?'store':itineraryDay[j].spot?"spot":"lodging",
            content: itineraryDay[j].store?itineraryDay[j].store.id:itineraryDay[j].spot?itineraryDay[j].spot.id:itineraryDay[j].lodging.id
          })
        }
      }
    })
    .catch(() => {
    })
  },
  watch:{
    datePlan:{
      deep:true,
      handler:"setDetailPlan"
    },
    destinations:{
      deep:true,
      handler:"setDetailPlan"
    },
  },
  created(){
    window.onbeforeunload = function () {
      return "저장되지 않은 정보는 삭제됩니다."
    }
  }

}
</script>

<style>

</style>