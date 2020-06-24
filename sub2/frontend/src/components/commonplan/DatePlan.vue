<template>
  <v-container>
    <v-row @click.prevent="dialog_start=true">
      <v-text-field
        v-model="start"
        label="출발일"
        prepend-icon="mdi-calendar"
        readonly
      />
    </v-row>
    <v-dialog v-model="dialog_start" z-index="3" overlay-opacity="1" max-width="300">
      <v-date-picker v-model="datePlan.start" scrollable @input="changePlan" locale="ko-kr" />
    </v-dialog>
    <v-row>
      <v-text-field v-model="end"
        label="도착일"
        prepend-icon="mdi-calendar"
        readonly
        disabled
        @click.prevent="dialog_end=true"
      />
    </v-row>
  </v-container>
</template>

<script>
export default {
  name:"dateplan",
  props: {
    datePlan:{
      type:Object,
      require:true
    },
    destinations:{
      type:Array,
      required:true
    }
  },
  data(){
    return{
      dialog_start:false,
      dialog_end:false,
      start: "",
      end: ""
    }
  },
  methods: {
    updateDate(){
      if (this.datePlan.start){
        this.start = this.datePlan.start
      }
      if (this.datePlan.end){
        this.end = this.datePlan.end
      }
      else{
        this.end = ""
      }
    },
    changePlan(e){
      let startDate = new Date(e)
      this.datePlan.start = e
      for (var i=0; i < this.destinations.length; i++){
        let a = new Date(this.destinations[i][2])
        let b = new Date(this.destinations[i][3])
        let days = (b - a)/1000/3600/24
        b.setDate(startDate.getDate() + days)
        this.destinations[i][2] = startDate.toISOString().substr(0, 10)
        this.destinations[i][3] = b.toISOString().substr(0, 10)
        startDate = b
      }
      this.dialog_start=false
      this.destinations.push()
    }
  },
  watch:{
    datePlan:{
      deep:true,
      immediate:true,
      handler:"updateDate"
    }
  }

}
</script>

<style>

</style>