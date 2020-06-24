<template>
  <v-container fluid class="py-2">
    <v-row class="mb-0 ml-2">
      <v-col cols="4">
        <v-text-field v-model="planTitle"
             label="여행 계획 제목"
          ></v-text-field>
      </v-col>
      <v-col cols="5" class="mt-2">
        <v-btn style="background-color:#2ecc71;" large dark @click="setToggle" v-if="toggle">세부일정 선택</v-btn>
        <v-btn style="color:#2ecc71;" large text @click="setToggle" v-else>전체일정 선택</v-btn>
        <v-btn class="ml-3" large style="background-color:#3498db" dark v-if="$store.state.isLogin && detailPlan.length" @click="savePlan">저장하기
        </v-btn>
        <v-btn class="ml-3" large color="success" disabled v-else>저장하기</v-btn>
      </v-col>
    </v-row>
        <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
    <v-row class="my-1">
      <v-col cols="5" md="2" class="py-0" style="bor">
        <date-plan :datePlan="datePlan" :destinations="destinations" />
        <time-line :destinations="destinations" :datePlan="datePlan" />
      </v-col>
      <v-col cols="7" md="10" class="py-0" v-if="toggle==true">
        <select-map :destinations="destinations" :datePlan="datePlan" />
      </v-col>
      <v-col cols="7" md="10" class="py-0" v-if="toggle==false && destinations.length">
        <time-table @update="updateDetailPlan" :destinations="destinations" :datePlan="datePlan"
          :detailPlan="detailPlan" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import axios from "axios"
  import router from "../router"
  import DatePlan from "../components/commonplan/DatePlan"
  import TimeLine from "../components/commonplan/TimeLine"
  import SelectMap from "../components/commonplan/SelectMap"
  import TimeTable from "../components/createplan/TimeTable"
  import {
    EventBus
  } from "../main"
  export default {
    name: "createplan",
    components: {
      SelectMap,
      TimeLine,
      DatePlan,
      TimeTable,
    },
    data() {
      return {
        toggle: true,
        destinations: [],
        datePlan: {
          start: new Date().toISOString().substr(0, 10),
          end: null,
        },
        detailPlan: {},
        planTitle: ""
      }
    },
    methods: {
      setToggle() {
          if (this.toggle) {
            if (this.destinations.length > 0)
              this.toggle = false
            else
              alert('여행지를 선택해주세요!!')
          } else
            this.toggle = true
        },
        savePlan() {
          if (!this.planTitle) {
            alert('여행계획 제목을 써주세요!!')
          } else {
            var temp = {
              "plans": {
                "title": this.planTitle,
                "user": this.$store.state.userinfo.id,
                "start_date": this.datePlan.start,
                "end_date": this.datePlan.end,
              },
              "days": this.detailPlan
            }
            axios.post("http://i02b207.p.ssafy.io:8083/api/plan/all/", temp)
              .then(res => {
                alert("저장이 완료되었습니다.")
                EventBus.$emit('AllPlan', temp)
                router.push({
                  name: "detailplan",
                  params: {
                    id: res.data.id
                  }
                })
              })
              .catch(() => {
                alert("저장중 문제가 발생하였습니다.")
              })
          }
        },
        setDetailPlan() {
          let start = this.datePlan.start
          let end = this.datePlan.end
          let tmp = []
          if (end) {
            let a = new Date(end)
            let b = new Date(start)
            let days = (a - b) / 1000 / 3600 / 24
            b.setDate(b.getDate() - 1)
            for (let i = 0; i <= days; i++) {
              var startDate = b
              startDate.setDate(startDate.getDate() + 1)
              var temp = []
              for (let j = 0; j < this.destinations.length; j++) {
                let c = new Date(this.destinations[j][2])
                let d = new Date(this.destinations[j][3])
                if (0 <= startDate - c && 0 <= d - startDate) {
                  temp.push(this.destinations[j][0])
                }
              }
              tmp.push({
                date: startDate.toISOString().substr(0, 10),
                area: temp,
                itinerarys: []
              })
            }
          }
          this.detailPlan = tmp
        },
        updateDetailPlan(events) {
          if (Array.isArray(events)) {
            let b = new Date(this.destinations[0][2])
            for (var j = 0; j < this.detailPlan.length; j++) {
              this.detailPlan[j].itinerarys = []
            }
            for (var i = 0; i < events.length; i++) {
              let a = new Date(events[i].start)
              let c = new Date(events[i].end)
              var days = parseInt((a - b) / 1000 / 3600 / 24)

              this.detailPlan[days].itinerarys.push({
                "start_time": a.toTimeString().substring(0, 5),
                "end_time": c.toTimeString().substring(0, 5),
                "title": events[i].title,
                "store": events[i].class == "store" ? events[i].content : null,
                "spot": events[i].class == "spot" ? events[i].content : null,
                "lodging": events[i].class == "lodging" ? events[i].content : null
              })
            }
          }
          tmp.push({
            date: startDate.toISOString().substr(0, 10),
            area: temp,
            itinerarys: []
          })
          this.detailPlan = tmp
        },
        updateDetailPlan(events) {
          if (Array.isArray(events)) {
            let b = new Date(this.destinations[0][2])
            for (var j = 0; j < this.detailPlan.length; j++) {
              this.detailPlan[j].itinerarys = []
            }
            for (var i = 0; i < events.length; i++) {
              let a = new Date(events[i].start)
              let c = new Date(events[i].end)
              var days = parseInt((a - b) / 1000 / 3600 / 24)

              this.detailPlan[days].itinerarys.push({
                "start_time": a.toTimeString().substring(0, 5),
                "end_time": c.toTimeString().substring(0, 5),
                "title": events[i].title,
                "store": events[i].class == "store" ? events[i].content : null,
                "spot": events[i].class == "spot" ? events[i].content : null,
                "lodging": events[i].class == "lodging" ? events[i].content : null
              })
            }
          }
        },
    },
    watch: {
      datePlan: {
        deep: true,
        handler: "setDetailPlan"
      },
      destinations: {
        deep: true,
        handler: "setDetailPlan"
      },
    },
    created() {
      window.onbeforeunload = function () {
        return "저장되지 않은 정보는 삭제됩니다."
      }
    }
  }
</script>

<style>

</style>