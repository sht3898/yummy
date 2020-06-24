<template>
<v-row justify="center">
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
            <lodging-detail @addplan="addplan" :lodgingnum="lodgingnum" :plandate="plandate"></lodging-detail>
        
      </v-card>
    </v-dialog>
</v-row>
</template>

<script>
import cities from '../../../public/city.json'
import axios from 'axios'
import {mapState, mapActions} from "vuex"
import 'vue-cal/dist/drag-and-drop.js'
import lodgingDetail from '../createplan/TimeTable/lodgingDetail'
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
        destinations:{
            type:Array,
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
            searcharea:''
        }
    },
    methods:{
        getDetailInfo(){
            var i = 0
            for (i; i < this.area.length; i++){
                if (i == this.area.length){
                    this.searcharea += this.area[i]
                }
                else{
                    this.searcharea += this.area[i] + ','
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
            localStorage.setItem("lodging_detail", lodging)
        },
        addplan(plan, date, starthour, startminute, endhour, endminute, explain){        
            this.$emit('addplan', plan, date, starthour, startminute, endhour, endminute, explain)
            this.dialog =! this.dialog
        },
  
    },
    watch:{
        lodgingpage:{
            immediate:"true",
            handler:"getDetailInfo"
        }
    }

}
</script>

<style>

</style>