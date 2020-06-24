<template>
  <v-timeline dense>
    <draggable
      :list="destinations"
      @change="movePlan"
    >
        <v-timeline-item v-for="i in destinations.length" :key="i" right @dblclick.native.stop="deletePlan(i-1)" large>
            <template v-slot:icon ca >
                <v-select
                    v-model="destinations[i-1][4]"
                    :items="dateSelect"
                    item-text="day"
                    item-value="num"
                    append-icon=""
                    rounded
                    dark
                    style="text-align:center;"
                    @change="changeDate(i-1)"
                ></v-select>
            </template>
            <v-card>
                <v-card-title>{{destinations[i-1][1]}}</v-card-title>
                {{destinations[i-1][2]}} ~ {{destinations[i-1][3]}}
            </v-card>
        </v-timeline-item>
    </draggable>
  </v-timeline>
</template>

<script>
import draggable from 'vuedraggable'
export default {
    name:"timeline",
    props:{
        datePlan:{
            type:Object,
            required:true
        },
        destinations:{
            type:Array,
            required:true
        },
    },
    components:{
        draggable
    },
    data(){
        return{
            dateToggle:false,
            dateSelect:[
                {num:0,day:'0박'},
                {num:1,day:'1박'},
                {num:2,day:'2박'},
                {num:3,day:'3박'},
                {num:4,day:'4박'},
                {num:5,day:'5박'},
                {num:6,day:'6박'},
                {num:7,day:'7박'},
                {num:8,day:'8박'},
                {num:9,day:'9박'},
            ]
        }
    },
    methods:{
        deletePlan(i){
            var a = new Date(this.destinations[i][3])
            var b = new Date(this.destinations[i][2])
            var days = (a-b)/1000/3600/24
            for (var j=i+1; j < this.destinations.length; j++){
                var startDate = new Date(this.destinations[j][2])
                var endDate = new Date(this.destinations[j][3])
                startDate.setDate(startDate.getDate() - days)
                endDate.setDate(endDate.getDate() - days)
                this.destinations[j][2] = startDate.toISOString().substr(0, 10)
                this.destinations[j][3] = endDate.toISOString().substr(0, 10)
            }
            this.destinations.splice(i,1)
        },
        movePlan(e){
            let before = e.moved.oldIndex
            let after = e.moved.newIndex
            if (before > after){
                let startDate = new Date(this.destinations[after+1][2])
                for (var i=after; i<=before; i++){
                    let endDate = new Date(startDate)
                    endDate.setDate(startDate.getDate() + this.destinations[i][4])
                    this.destinations[i] = [
                        this.destinations[i][0],
                        this.destinations[i][1],
                        startDate.toISOString().substr(0, 10),
                        endDate.toISOString().substr(0, 10),
                        this.destinations[i][4],
                        this.destinations[i][5],
                        ]
                    startDate = endDate
                }
            }
            else{
                let endDate = new Date(this.destinations[after-1][3])
                for (var i=after; i>=before; i--){
                    this.destinations[i][3] = endDate.toISOString().substr(0, 10)
                    let startDate = new Date(this.destinations[i][3])
                    startDate.setDate(endDate.getDate() - this.destinations[i][4])
                    this.destinations[i][2] = startDate.toISOString().substr(0, 10)
                    this.destinations[i] = [
                        this.destinations[i][0],
                        this.destinations[i][1],
                        startDate.toISOString().substr(0, 10),
                        endDate.toISOString().substr(0, 10),
                        this.destinations[i][4],
                        this.destinations[i][5]
                        ]
                    endDate = startDate
                }
            }
            this.destinations.push()
        },
        changeDate(idx){
            let startDate = new Date(this.destinations[idx][2])
            for (var i=idx; i < this.destinations.length; i++){
                let endDate = new Date(startDate)
                endDate.setDate(startDate.getDate() + this.destinations[i][4])
                
                this.destinations[i][2] = startDate.toISOString().substr(0, 10)
                this.destinations[i][3] = endDate.toISOString().substr(0, 10)
                startDate = endDate
            }
        }
    },
}
</script>

<style>
.v-select__selections{
    width: 30px;
}
</style>