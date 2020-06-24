<template>
  <v-container>
    <h2>유사 관광지 추천</h2>
    <v-row>
      <v-col cols="4" v-for="spot in spots" :key="spot.id">
        <v-card style="text-align:center" height="160">
          <v-card-title style="text-align:center">
            {{spot.spot_name}}
          </v-card-title>
          <v-card-text>
            <span v-for="category in spot.category_list" :key="category.id">{{category}}</span>
            <br>
            {{ spot.address }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: "spotRecommend",
  props: {
    spotnum: {
      type: Number,
      required: true
    }
  },
  mounted() {
    this.getDetailInfo()
  },
  data() {
    return {
      spots: [],
    }
  },
  methods: {
    getDetailInfo() {
      axios.get(`http://i02b207.p.ssafy.io:8083/api/spots/recommendations/${this.spotnum}/`)
        .then(res => {
          this.spots = res.data
        })
        .catch(() => {
        })
    },
  },
}
</script>