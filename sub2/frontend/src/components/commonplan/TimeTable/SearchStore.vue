<template>
<v-row justify="center">
    <v-dialog v-model="dialog" width="60%" >
    <template v-slot:activator="{ on }">
        <v-container>
        <v-row>
            <v-col cols="4" v-for="store in stores" :key="store.id">
                <button v-on="on" @click="GoDetail(store.id)">

                <v-card style="text-align:center">
                    <v-card-title  style="text-align:center">
                        {{store.store_name}}
                    </v-card-title>
                    <v-card-text>
                        <span v-for="category in store.category_list" :key="category.id">{{category}}</span>
                        <br>
                        {{ store.address }}
                    </v-card-text>
                </v-card>
                    </button>
                
            </v-col>
        </v-row>
        </v-container>
    </template>
      <v-card style="height:100%;">
          <store-detail :storenum="storenum" :plandate="plandate" :events="events" @toggle="dialog=false" />
      </v-card>
    </v-dialog>
</v-row>
</template>

<script>
import cities from '../../../../public/city.json'
import axios from 'axios'
import {mapState, mapActions} from "vuex"
import 'vue-cal/dist/drag-and-drop.js'
import storeDetail from './storeDetail'
export default {
    name:"SearchItem",
       props:{
        storepage:{
            type:Number,
            required:true
        },
        area:{
            type:Array,
            required:true,
        },
        events:{
            type:Array,
        },
        plandate:{
            type:String
        },
        searchitem:{
            type:String
        },
        location:{
            type:String
        },
    },
    components: {
        storeDetail
    },
   data(){
        return{
            stores:[],
            dialog: false,
            storenum:0,
            event:{},
            searcharea:''
        }
    },
    methods:{
        getDetailInfo(){
            var i = 0
            var j = 0
            for (i; i < this.area.length; i++){
                for(j; j < this.area[i].area.length; j++){
                    if (cities[this.area[i].area[j]-1].cityName == this.location){
                        this.searcharea = this.area[i].area[j]
                    }
                }
            }
            axios.get(`http://i02b207.p.ssafy.io:8083/api/stores/`, {params:{page:this.storepage, name:this.searchitem, area:this.searcharea}})
            .then(res=>{
                this.stores = res.data.results
                this.$emit('storelist', this.stores)
            })
        },
        GoDetail(store){
            this.storenum = store
        },
    },
    watch:{
        storepage:{
            immediate:"true",
            handler:"getDetailInfo"
        },
        searchitem:{
            handler:"getDetailInfo"
        }
    }

}
</script>

<style>

</style>