<template>
    <v-row justify="center">
        <v-overlay :value="loading">
            <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
        <v-dialog v-model="dialog" width="60%" >
            <template v-slot:activator="{ on }">
                <v-container>
                <v-row>
                    <v-col cols="4" v-for="lodging in lodgings" :key="lodging.id">
                        <button v-on="on" @click="GoDetail(lodging.id)">

                        <v-card style="text-align:center">
                            <v-card-title  style="text-align:center">
                                {{lodging.lodging_name}}
                            </v-card-title>
                            <v-card-text>
                                <span v-for="category in lodging.category_list" :key="category.id">{{category}}</span>
                                <br>
                                {{ lodging.address }}
                            </v-card-text>
                        </v-card>
                            </button>
                        
                    </v-col>
                </v-row>
                </v-container>
            </template>
            <v-card style="height:100%;">
                <lodging-detail :lodgingnum="lodgingnum" :plandate="plandate" :events="events" @toggle="dialog=false" />
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
import cities from '../../../../public/city.json'
import axios from 'axios'
import {mapState, mapActions} from "vuex"
import 'vue-cal/dist/drag-and-drop.js'
import lodgingDetail from './lodgingDetail'
export default {
    name:"SearchItem",
       props:{
        lodgingpage:{
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
        }
    },
    components: {
        lodgingDetail
    },
   data(){
        return{
            lodgings:[],
            dialog: false,
            lodgingnum:0,
            event:{},
            loading:false,
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
            axios.get(`http://i02b207.p.ssafy.io:8083/api/lodgings/`, {params:{page:this.lodgingpage, name:this.searchitem, area:this.searcharea}})
            .then(res=>{
                this.lodgings = res.data.results
                this.$emit('lodginglist', this.lodgings)
            })
        },
        GoDetail(lodging){
            this.lodgingnum = lodging
        },
    },
    watch:{
        lodgingpage:{
            immediate:"true",
            handler:"getDetailInfo"
        },
        searchitem:{
            immediate:"true",
            handler:"getDetailInfo"
        }
    }

}
</script>

<style>

</style>