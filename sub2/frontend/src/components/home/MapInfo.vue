<template>
  <div class="map_wrap" style="width:100%">
    <div :id="setMapId" style="width:100%;height:100%;position:relative;overflow:hidden;"></div>
  </div>
</template>

<script>
import cities from "../../../public/city.json"

export default {
  name:"mapView",
  props:{
    areaList:{
      type:Array
    },
    id:{
      type:Number
    }
  },
  data(){
    return{
      map:null
    }
  },
  methods:{
    mapSetting(){
      var container = document.getElementById(this.setMapId)
      var mapOptions = {
          center: new kakao.maps.LatLng(35.550701, 128.070667),
          level: 14,
          draggable: false,
      }
      this.map = new kakao.maps.Map(container, mapOptions)
      this.map.setZoomable(false)
    },
    setMarker(){
      var map = this.map
      var markers = []
      var linePath = []
      for (var i = 0; i < this.areaList.length; i ++) {
        var position = new kakao.maps.LatLng(cities[this.areaList[i]-1].longitude, cities[this.areaList[i]-1].latitude)
        var marker = new kakao.maps.Marker({
          map: map,
          position: position,
        })
        var infowindow = new kakao.maps.InfoWindow({
          content: cities[this.areaList[i]-1].cityName,
          position: position
        })
        linePath.push(position)
      }
      var polyline = new kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 5,
        strokeColor: '#FFAE00',
        strokeOpacity: 0.7,
        strokeStyle: 'solid'
      })
      polyline.setMap(map)
    },
  },
  mounted(){
    this.mapSetting()
    this.setMarker()
  },
  computed:{
    setMapId(){
      return "map" + this.id + this.$parent._uid
    }
  }
}
</script>

<style>
.map_wrap {position:relative;overflow:hidden;width:100%;height:300px;}
.radius_border{border:1px solid #919191;border-radius:5px;}
</style>