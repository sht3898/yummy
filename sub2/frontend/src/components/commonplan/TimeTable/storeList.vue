<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" width="60%">
      <template v-slot:activator="{ on }">
        <v-container>
          <v-row>
            <v-col cols="4" v-for="store in stores" :key="store.id">
              <button v-on="on" @click="GoDetail(store.id)" class="mx-auto" style="width:100%;">
                <v-card height="200">
                  <v-card-title style="text-align:center">
                    {{store.store_name}}
                  </v-card-title>
                  <hr style="border-top: 1px dashed lightgrey;" class="my-2" />

                  <v-card-text>
                    <span v-for="category in store.category_list" :key="category.id">{{category}},</span>
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
  import {
    mapState,
    mapActions
  } from "vuex"
  import 'vue-cal/dist/drag-and-drop.js'
  import storeDetail from './storeDetail'

  export default {
    name: "storeList",
    components: {
      storeDetail
    },
    props: {
      storepage: {
        type: Number,
        required: true
      },
      area: {
        type: Array,
        required: true,
      },
      events: {
        type: Array,

      },
      plandate: {
        type: String
      },
      destinations: {
        type: Array,
        // required:true
      }
    },
    data() {
      return {
        stores: [],
        dialog: false,
        storenum: 0,
        event: {},
        planarea: '',
      }
    },
    methods: {
      getDetailInfo() {
        var i = 0
        for (i; i < this.area.length; i++) {
          if (i == 0) {
            this.planarea += this.area[i]
          } else {
            this.planarea += ',' + this.area[i]
          }
        }
        axios.get(`http://i02b207.p.ssafy.io:8083/api/stores/`, {
            params: {
              page: this.storepage,
              area: this.planarea
            }
          })
          .then(res => {
            this.stores = res.data.results
            this.$emit('storelist', this.stores)
            this.planarea = ''
          })
          .catch(() => {})
      },
      GoDetail(store) {
        this.storenum = store
      },
    },
    watch: {
      storepage: {
        immediate: "true",
        handler: "getDetailInfo"
      }
    }
  }
</script>

<style>

</style>