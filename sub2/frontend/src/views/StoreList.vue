<template>
<div>
  <input style="position:absolute; top:200px" v-model="changeitem">
  <v-container style="margin-top:40px">
    <v-row no-gutters justify="space-between" align="center">
      <v-col cols="8">
        <v-text-field
          @keyup.enter="loading"
          v-model="searchitem"
          label="검색"
          hide-details
          single-line>
        </v-text-field>
      </v-col>
        <loading :active.sync="isLoading" 
        ></loading>
      
      <v-col cols="4" style="line-height:4">
        <v-btn class="mx-4" @click="loading" small color="#2c3e50" dark>검색</v-btn>
      </v-col>
    </v-row>
  </v-container>
    <v-tabs v-model="tab"
    style="position: sticky;"
    background-color="transparent"
    color="basil"
    grow>
    <v-tab v-for="item in ['음식점','관광지']" :key="item.date">
      {{ item }}
    </v-tab>
  </v-tabs>
  <v-tabs-items v-model="tab">
    <v-tab-item>
    <div style="float:left; margin:20px">
  <v-container fluid>
     <v-row no-gutters justify="space-between" align="center">
      <v-col md="12" sm="12" xs="12" class="pt-2 pb-2">
        <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
      </v-col>
      <template v-for="store in stores">
        <v-col md="3" sm="6" xs="12" :key="store.id">
          <v-hover v-slot:default="{ hover }">
            <v-card 
              :class="{ 'on-hover': hover }" style="margin:2px 2px auto;"
              @click="GoStoreDetail(store.id)">
              <v-img
                class="white--text align-end"
                height="200px"
                style="background-size: cover; width:466px;"
                :src="store.thumbnail"
                gradient="to bottom, rgba(100,115,201,.13), rgba(25,32,72,.7)"
                alt="https://images.unsplash.com/photo-1498579809087-ef1e558fd1da?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80">
                <v-list-item-content class="mx-2 pb-5">
                  <div v-if="store.category_list[0] == 'nan'">미분류</div>
                  <div v-else>{{store.category_list[0]}}</div>
                  <v-list-item-title class="headline mb-1">{{store.store_name}}</v-list-item-title>
                </v-list-item-content>
              </v-img>
            </v-card>
          </v-hover>
        </v-col>
      </template>
    </v-row>
  </v-container>
    </div>
    <v-pagination
      style="margin:10px"
      @input="searchstore"
      v-model="storepage"
      :length="10"
      :total-visible="10">
    </v-pagination>
    </v-tab-item>
        <v-tab-item>
    <div style="float:left; margin:20px">
    <v-container fluid>
       <v-row no-gutters justify="space-between" align="center">
        <v-col md="12" sm="12" xs="12" class="pt-2 pb-2">
          <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
          </v-col>
          <template v-for="spot in spots">
            <v-col md="3" sm="6" xs="12" :key="spot.id">
              <v-hover v-slot:default="{ hover }">
                <v-card 
                  :class="{ 'on-hover': hover }" style="margin:2px 2px auto;"
                  @click="GoSpotDetail(spot.id)">
                  <v-img
                    class="white--text align-end"
                    height="200px"
                    :src="spot.image_url"
                    gradient="to bottom, rgba(100,115,201,.13), rgba(25,32,72,.7)"
                    alt="https://static.hubzum.zumst.com/hubzum/2019/02/25/10/054889f91efb4d89abcb42317c298504_780x0c.jpg">
                    <v-list-item-content class="mx-2 pb-5">
                      <!-- <div v-if="store.category_list[0] == 'nan'">미분류</div>
                      <div v-else>{{store.category_list[0]}}</div> -->
                      <v-list-item-title class="headline mb-1">{{spot.spot_name}}</v-list-item-title>
                    </v-list-item-content>
                  </v-img>
                </v-card>
              </v-hover>
            </v-col>
        </template>
      </v-row>
    </v-container>
    </div>
    <v-pagination
      style="margin:10px"
      @input="searchspot"
      v-model="spotpage"
      :length="10"
      :total-visible="7">
    </v-pagination>
    </v-tab-item>
  </v-tabs-items>
</div>
</template>


<script>
import axios from "axios";
import {mapState, mapActions} from "vuex"
import router from "../router";
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
export default {
  name:'StoreList',
  components: {
    Loading
  },
  data(){
    return{
      storepage:1,
      spotpage:1,
      stores:[],
      spots:[],
      searchitem:'',
      tab:null,
      naverpic: 'https://cdn.pixabay.com/photo/2020/04/22/14/20/sheep-5078377_960_720.jpg',
      tmp:'',
      changeitem:'',
      isLoading: false,
      fullPage: true

    }
  },
  created() {
    setTimeout(this.change, 1000)
  },

  mounted() {
      this.searchstore()
  },
  watch:{
    storepage:{
      handler:"loading"
    }
  },
  methods:{
    ...mapActions(['GoDetail']),
    loading(){
      this.searchstore()
      setTimeout(this.change, 1500)
    },
    change(){
      this.isLoading = false
      this.changeitem = this.storepage
    },
    naverimage(i) {
      if (this.stores[i].category_list[0] !=='nan' && this.stores[i].category_list[0]){
        var keyword = this.stores[i].category_list[0]
        axios.get(`http://i02b207.p.ssafy.io:8083/api/search/image?keyword=${keyword}`)
        .then(res => {
          if (res.data.items[0].link){
            this.stores[i].thumbnail = res.data.items[0].link
          }
          else{
            this.stores[i].thumbnail = 'https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
          }
        })
        .catch(Error=> {
          this.stores[i].thumbnail = 'https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        })
      }
      else{
        var keyword = this.stores[i].store_name
        axios.get(`http://i02b207.p.ssafy.io:8083/api/search/image?keyword=${keyword}`)
        .then(res => {
          if (res.data.items[0].link){
            this.stores[i].thumbnail = res.data.items[0].link
          }
          else{
            this.stores[i].thumbnail = 'https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
          }
        })
        .catch(Error=> {
          this.stores[i].thumbnail = 'https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        })
      }
    },
    GoStoreDetail(store){
      localStorage.setItem("store_detail", store)
      router.push({
        name:'storedetail',
        params:{
          "num" : store
        }
      })
    },
    GoSpotDetail(spot){
      localStorage.setItem("spot_detail", spot)
      router.push({
        name:'spotdetail',
        params:{
          "num" : spot
        }
      })
    },
    searchstore(){
      this.isLoading = true;
      axios.get('http://i02b207.p.ssafy.io:8083/api/stores/', {params:{page:this.storepage, name:this.searchitem}})
      .then(res=>{
          this.stores = res.data.results
          var i =0
         for (i; i < this.stores.length; i++){
           this.naverimage(i)
         }
      })
      .catch(()=> {
      })
      this.searchspot()
    },
    searchspot(){
      axios.get('http://i02b207.p.ssafy.io:8083/api/spots/', {params:{page:this.spotpage, name:this.searchitem}})
      .then(res=>{
          this.spots = res.data.results
      })
      .catch(()=> {
      })
    },
  }
}
</script>


<style lang="scss" scoped>
.v-card {
  transition: opacity .4s ease-in-out;
}

.on-hover {
  opacity: 0.7;
 }
</style>