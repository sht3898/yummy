<template>
  <div class="map_wrap" id="selectedMap">
    <div class="search" style="background:white;">
        <div class="text-center">
            <v-menu offset-y>
            <template v-slot:activator="{ on }">
                <v-row>
                    <v-col class="py-0 pr-0" cols="10"><v-text-field v-model="searchCity" solo outlined /></v-col>
                    <v-col class="px-0" cols="2" @click="searchCities(searchCity)"><v-icon v-on="on">mdi-map-search</v-icon></v-col>
                </v-row>
            </template>
            <v-list>
                <v-list-item v-for="idx in searchResult.length" :key="idx" @click="selectCity(searchResult[idx-1])">
                    <v-list-item-title>{{ splitAddress(searchResult[idx-1].address) }}</v-list-item-title>
                </v-list-item>
            </v-list>
            </v-menu>
        </div>
    </div>
    <div id="map" style="width:100%;height:100%;position:relative;overflow:hidden;"></div>
      <div class="custom_typecontrol radius_border">
        <span id="btnRoadmap" class="selected_btn" @click="setMapType('roadmap')">지도</span>
        <span id="btnSkyview" class="btn" @click="setMapType('skyview')">스카이뷰</span>
      </div>
      <div class="custom_zoomcontrol radius_border">
        <span @click="zoomIn()">
          <img src="https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/ico_plus.png" alt="확대">
        </span>
        <span @click="zoomOut()">
          <img src="https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/ico_minus.png" alt="축소">
        </span>
    </div>
  </div>
</template>

<script>
import cities from '../../../public/city.json'
var dialog=false

export default {
    name: 'dmap',
    props:{
        datePlan:{
            type:Object,
            required:true
        },
        destinations:{
            type:Array,
            required:true
        }
    },
    data(){
        return {
            searchCity:"",
            showMenu:false,
            searchResult:[],
            map:null,
            dates:[],
            polyline:null,
        }
    },
    methods:{
        mapSetting(){
            var container = document.getElementById('map')
            var mapOptions = {
                center: new kakao.maps.LatLng(35.850701, 127.570667),
                level: 13
            }
            this.map = new kakao.maps.Map(container, mapOptions)
            this.polyline = new kakao.maps.Polyline({
                strokeWeight: 5,
                strokeColor: '#FFAE00',
                strokeOpacity: 0.7,
                strokeStyle: 'solid'
            })
            this.polyline.setMap(this.map)
        },
        setMarker(){
            if (Object.keys(this.datePlan).length){
                var map = this.map
                var clusterer = new kakao.maps.MarkerClusterer({
                    map: map,
                    averageCenter: true,
                    minLevel: 10
                })
                var markers = []
                for (var i = 0; i < cities.length; i ++) {
                    var marker = new kakao.maps.Marker({
                        map: map,
                        position: new kakao.maps.LatLng(cities[i].longitude, cities[i].latitude),
                    })
                    var infowindow = new kakao.maps.InfoWindow({
                        content: cities[i].cityName
                    })
                    kakao.maps.event.addListener(marker, 'mouseover', this.makeOverListener(map, marker, infowindow))
                    kakao.maps.event.addListener(marker, 'mouseout', this.makeOutListener(infowindow))
                    kakao.maps.event.addListener(marker, 'click', this.makeClickListener(cities[i].id, marker, infowindow, this.destinations, (this.datePlan.end) ? this.datePlan.end:this.datePlan.start))
                    markers.push(marker)
                }
                clusterer.addMarkers(markers)
            }
        },
        setMapType(maptype) {
            var map = this.map
            var roadmapControl = document.getElementById('btnRoadmap')
            var skyviewControl = document.getElementById('btnSkyview')
            if (maptype === 'roadmap') {
                map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP)
                roadmapControl.className = 'selected_btn'
                skyviewControl.className = 'btn'
                }
            else {
                map.setMapTypeId(kakao.maps.MapTypeId.HYBRID)
                skyviewControl.className = 'selected_btn'
                roadmapControl.className = 'btn'
            }
        },
        zoomIn() {
            var map = this.map
            map.setLevel(map.getLevel() - 1)
        },
        zoomOut() {
            var map = this.map
            map.setLevel(map.getLevel() + 1)
        },
        makeOverListener(map, marker, infowindow) {
            return function() {
                infowindow.open(map, marker)
            }
        },
        makeOutListener(infowindow) {
            return function() {
                infowindow.close()
            }
        },
        makeClickListener(id, marker, infowindow, destinations, start){
            return function() {
                var len = destinations.length - 1
                if (len > 0 && destinations[len][0] == id){
                    destinations.splice(len, 1)
                }
                else {
                    var end = new Date(start)
                    end.setDate(end.getDate() + 1)
                    end = end.toISOString().substr(0, 10)
                    destinations.push([id, infowindow.getContent(), start, end, 1, marker.getPosition()])
                }
            }
        },
        changeEnddate(){
            if (this.destinations.length){
                var len = this.destinations.length
                this.datePlan.end = this.destinations[len-1][3]
                
            }
            else{
                this.datePlan.end = null
            }
            if (this.polyline){
                var linePath = []
                for (var i=0; i<this.destinations.length; i++){
                    linePath.push(new kakao.maps.LatLng(this.destinations[i][5].Ha, this.destinations[i][5].Ga))
                }
                this.polyline.setPath(linePath)
            }
        },
        searchCities(searchValue){
            var result = []
            for (var i = 0; i < cities.length; i ++) {
                if (cities[i].cityName.indexOf(searchValue) > -1){
                    result.push(cities[i])
                }
            }
            this.searchResult = result
        },
        splitAddress(char){
            var tmp = char.split(" ")
            return (tmp[0].length <= 4)?tmp[0] + ' ' + tmp[1]:tmp[0]            
        },
        selectCity(city){
            var len = this.destinations.length - 1
            if (len > 0 && this.destinations[len][0] == city.id){
                this.destinations.splice(len, 1)
            }
            else {
                var start = (this.datePlan.end) ? this.datePlan.end:this.datePlan.start
                var end = new Date(start)
                end.setDate(end.getDate() + 1)
                end = end.toISOString().substr(0, 10)
                this.destinations.push([city.id, city.cityName, start, end, 1])
            }
        }
    },
    mounted(){
      this.mapSetting()
      this.setMarker()
    },
    watch:{
        datePlan:{
            deep:true,
            handler:"setMarker"
        },
        destinations:{
            deep:true,
            immediate: true,
            handler:"changeEnddate"
        },
    },
}
</script>

<style>
#selectedMap {position:relative;overflow:hidden;width:100%;height:90vh;}
.radius_border{border:1px solid #919191;border-radius:5px;}
.search {position:absolute;top:10px;left:10px;overflow:hidden;width:300px;height:80px;margin:0;padding:10px;z-index:2;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
.custom_typecontrol {position:absolute;top:10px;right:10px;overflow:hidden;width:130px;height:30px;margin:0;padding:0;z-index:1;font-size:12px;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
.custom_typecontrol span {display:block;width:64px;height:30px;float:left;text-align:center;line-height:30px;cursor:pointer;}
.custom_typecontrol .btn {background:#fff;background:linear-gradient(#fff,  #e6e6e6);}       
.custom_typecontrol .btn:hover {background:#f5f5f5;background:linear-gradient(#f5f5f5,#e3e3e3);}
.custom_typecontrol .btn:active {background:#e6e6e6;background:linear-gradient(#e6e6e6, #fff);}    
.custom_typecontrol .selected_btn {color:#fff;background:#425470;background:linear-gradient(#425470, #5b6d8a);}
.custom_typecontrol .selected_btn:hover {color:#fff;}   
.custom_zoomcontrol {position:absolute;top:60px;right:10px;width:36px;height:80px;overflow:hidden;z-index:1;background-color:#f5f5f5;} 
.custom_zoomcontrol span {display:block;width:36px;height:40px;text-align:center;cursor:pointer;}     
.custom_zoomcontrol span img {width:15px;height:16px;margin:12px 0;border:none;}             
.custom_zoomcontrol span:first-child{border-bottom:1px solid #bfbfbf;} 
</style>