<template>
<div style="height:100%">
  <v-tabs v-model="datetab"
    style="position: sticky;"
    background-color="transparent"
    color="basil"
    grow>
    <v-tab v-for="item in detailPlan" :key="item.date">
      {{ item.date }}
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="datetab">
    <v-tab-item v-for="i in detailPlan.length" :key="i"> 
      <v-container class="pb-0">
        <v-row>
          <v-col cols="3">
            <h2> {{detailPlan[i-1].date}} 일정</h2>
          </v-col>
          <v-col cols="9">
            <v-container style="padding:0;">
              <v-row>
                <v-col cols="3">
                  <v-select
                    v-model="location"
                    :items="selectarea"
                    item-text="state"
                    label="지역"
                    return-object
                    single-line>
                  </v-select>
                </v-col>
                <v-col cols="5">
                  <v-text-field
                    @keyup.enter="searchresult"
                      v-model="tmpitem"
                      label="검색"
                      hide-details
                      single-line>
                  </v-text-field>
                </v-col>
                <v-col style="line-height:4">
                    <v-btn style="margin-right:10px" @click="searchresult" color="secondary" small dark>검색</v-btn>
                    <v-btn @click="allresult" color="secondary" small outlined>전체보기</v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </v-container>
        <v-dialog width="60%" v-model="showDialog">
          <v-card class="updateevent" style="padding:20px">
            <v-card-title>
              <v-text-field v-model="title" />
              <v-spacer></v-spacer>
              <v-btn class="mr-2" @click="modifyPlan" style="float:right" big color="#3498db" dark>변경</v-btn>
              <v-btn @click="deletePlan" style="float:right" big color="#e74c3c" outlined>삭제</v-btn>
            </v-card-title>
            <v-card-text>
              <v-container class="pt-0">
                <v-row>
                  <v-col class="timeInfo" cols="12" md="6">
                    <p class="mb-4" style="font-size:1.6vw">일정시작시간</p>
                    <v-time-picker v-model="startTime" :max="endTime" full-width landscape></v-time-picker>
                  </v-col>
                  <v-col>
                    <p class="mb-4" style="font-size:1.6vw">일정종료시간</p>
                    <v-time-picker v-model="endTime" :min="startTime" full-width landscape></v-time-picker>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-dialog>
 
    <v-container>
      <v-row>
        <v-col @mouseup="confirmData(i-1)" @dragend="confirmData(i-1)" @mouseleave="confirmData(i-1)" cols="4">
          <vue-cal
            @mouseout="confirmData(i-1)"
            ref="vuecal"
            :selected-date="detailPlan[i-1].date"
            :time-cell-height="60"
            :time-from="6 * 60"
            :time-to="23 * 60"
            hide-weekends
            active-view="day"
            :disable-views="['years', 'year', 'month']"
            :dblclick-to-navigate="false"
            :cell-click-hold="true"
            :startWeekOnSunday="false"
            :deletable-events="true"
            editable-events
            :events="events"
            :on-event-dblclick="onEventClick"
            >
          </vue-cal>
        </v-col>
        <v-col cols="8">          
          <v-tabs v-model="tab"
          style="position: sticky;"
            background-color="transparent"
            color="basil"
            grow>
            <v-tab v-for="item in ['맛집', '관광명소', '숙박']" :key="item">
              {{ item }}
            </v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item> 
              <search-store v-if="switchlist == true" :searchitem="searchitem" :events="events" :location="location"
              :storepage="storepage" :area="detailPlan" :plandate="detailPlan[i-1].date" />

              <store-list  v-if="switchlist == false" :events="events" :storepage="storepage" 
              :area="detailPlan[i-1].area" :plandate="detailPlan[i-1].date" />
              <v-pagination
                style="margin:10px"
                v-model="storepage"
                :length="10"
                :total-visible="7">
              </v-pagination>
            </v-tab-item>
            <v-tab-item> 
              <search-spot v-if="switchlist == true" :searchitem="searchitem" :events="events" :location="location"
              :spotpage="spotpage" :area="detailPlan" :plandate="detailPlan[i-1].date" />

              <spot-list v-if="switchlist == false" :events="events" :spotpage="spotpage" 
              :area="detailPlan[i-1].area" :plandate="detailPlan[i-1].date" />
              <v-pagination
                style="margin:10px"
                v-model="spotpage"
                :length="10"
                :total-visible="7">
              </v-pagination>
            </v-tab-item>
            <v-tab-item> 
              <search-lodging v-if="switchlist == true" :searchitem="searchitem" :events="events" :location="location"
              :lodgingpage="lodgingpage" :area="detailPlan" :plandate="detailPlan[i-1].date" />

              <lodging-list v-if="switchlist == false" :events="events" :lodgingpage="lodgingpage" 
              :area="detailPlan[i-1].area" :plandate="detailPlan[i-1].date" />
              <v-pagination
                style="margin:10px"
                v-model="lodgingpage"
                :length="10"
                :total-visible="7">
              </v-pagination>
            </v-tab-item>
          </v-tabs-items>
        </v-col>
      </v-row>
    </v-container>
  </v-tab-item>
  </v-tabs-items>
    
</div>
</template>


<script>
import VueCal from 'vue-cal'
import axios from 'axios'
import 'vue-cal/dist/drag-and-drop.js'
import 'vue-cal/dist/vuecal.css'
import storeList from '../commonplan/TimeTable/storeList'
import SearchStore from '../commonplan/TimeTable/SearchStore'
import SearchSpot from '../commonplan/TimeTable/SearchSpot'
import SearchLodging from '../commonplan/TimeTable/SearchLodging'
import spotList from '../commonplan/TimeTable/spotList'
import lodgingList from '../commonplan/TimeTable/lodgingList'
import moment from 'moment'
import cities from '../../../public/city.json'

export default {
  name:"timetable",
  props:{
    detailPlan:{
      type:Array,
      required:true
    },
    
    destinations:{
      type:Array,
      required:true
    }
  },
  components: {
    VueCal,
    storeList,
    spotList,
    lodgingList,
    SearchStore,
    SearchSpot,
    SearchLodging
  },
  data(){
    return{
      selectarea:[],
      location:'',
      switchlist: false,
      
      selectedEvent:null,
      title:'',
      startTime:null,
      endTime:null,
      events:Array,
      
      showDialog: false,
      storepage:1,
      spotpage:1,
      lodgingpage:1,
      datetab:null,
      tab:null,
      selectdate:0,
      searchitem:'',
      tmpitem:''
    }
  },

  mounted() { 
    this.loadlocation()
  },
  methods:{
    loadlocation(){
      console.log(this.detailPlan)
      var i=0
      for (i; i < this.detailPlan.length; i++){
        var j=0
        for (j; j< this.detailPlan[i].area.length; j++){
          this.selectarea.push(cities[this.detailPlan[i].area[j]-1].cityName)
        }
      }
    },
    searchresult(){
      if (this.location){
        this.switchlist = true
        this.searchitem = this.tmpitem
      }
      else{
        alert('검색지역을 설정하세요')
      }
    },
    allresult(){
      this.switchlist = false
    },
    onEventClick (event, e) {
      this.showDialog = true
      this.selectedEvent = event
      this.title = event.title
      let tmp = new Date(event.start)
      this.startTime = tmp.toTimeString().substring(0, 5)
      tmp = new Date(event.end)
      this.endTime = tmp.toTimeString().substring(0, 5)
      e.stopPropagation()
    },
    modifyPlan() {
      var startdate = this.$moment(this.selectedEvent.start).format(`YYYY-MM-DD ${this.startTime}:00`)
      var enddate = this.$moment(this.selectedEvent.start).format(`YYYY-MM-DD ${this.endTime}:00`)
      for (var i = 0; i < this.events.length; i++){
        if (this.events[i]._eid == this.selectedEvent._eid){
          this.events[i].start = startdate
          this.events[i].end = enddate
          this.events[i].title = this.title
          this.showDialog = false
          break
        }
      }
      this.selectedEvent = null
      this.title = '',
      this.startTime = null
      this.endTime = null
    },
    deletePlan(){
      for (var i = 0; i < this.events.length; i++){
        if (this.events[i]._eid == this.selectedEvent._eid){
          this.events.splice(i, 1)
          this.showDialog = false
          break
        }
      }
    },
    confirmData(i){
      console.log(this.$data)
    },
    addplan(startTime, endTime, explain, storeNum, spotNum, lodgingNum){
      var date = this.detailPlan[this.datetab].date
      this.events.push({
      start: `${date} ${startTime}`,
      end: `${date} ${endTime}`,
      title: explain,
      content: explain,
      })
      this.detailPlan[this.datetab].itinerarys.push({
        "start_time" : startTime,
        "end_time" : endTime,
        "title" : explain,
        "store" : storeNum,
        "spot" : spotNum,
        "lodging" : lodgingNum
      })
    },
    updateEvents(){
      this.$emit('update', this.events)
    },
    itemini(){
      this.tmpitem=''
    }
  },
  created(){
    this.events = []
  },
  watch:{
    events:{
      deep:true,
      handler:"updateEvents"
    },
    location:{
      handler:"itemini"
    }
  }
}
</script>

<style>
.vuecal__header{
  display: none;
}

.updateevent{
  height: 500px;
}

.vuecal__event--dragging {background-color: rgba(52, 10, 240, 0.932);}
.vuecal--day-view .vuecal__bg .vuecal__event--all-day.pink-event {right: 50%;}
.vuecal__event{
  color:black;
  opacity: 1.5;
  font-weight: bold;
}
.vuecal__event.store{
  /* background-image: url("../../img/storeimg2.jpg");
  opacity: 0.5; */
  background-color:#e67e22;
  color:white;
  font-size: 18px;
  font-weight: bold;
}
.vuecal__event.lodging{
  /* background-image: url("../../img/hotelimg2.jpg");
  opacity: 0.5; */
  background-color:#f1c40f;
  color:white;
  font-size: 20 px;
  font-weight: bold;
}
.vuecal__event.spot{
  /* background-image: url("../../img/placeimg2.jpg");
  opacity: 0.5; */
  background-color:#2ecc71;
  color:white;
  font-size: 20 px;
  font-weight: bold;
}
.vuecal__now-line {
  display: none;
}
.vuecal__event {cursor: pointer;}

.vuecal__event-title {
  font-size: 1.2em;
  font-weight: bold;
  margin: 4px 0 8px;
}

.vuecal__event-time {
  display: inline-block;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.vuecal__event-content{
  display: none;
}


</style>