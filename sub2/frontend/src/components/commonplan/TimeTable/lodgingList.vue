<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" width="60%">
      <template v-slot:activator="{ on }">
        <v-container>
          <v-row>
            <v-col cols="4" v-for="lodging in lodgings" :key="lodging.id">
              <button v-on="on" @click="GoDetail(lodging.id)" style="width:100%;">
                <v-card style="text-align:center"  height="200">
                  <v-card-title style="text-align:center; padding:16px 16px 8px 16px">
                    {{lodging.lodging_name}}
                  </v-card-title>
                  <hr style="border-top: 1px dashed lightgrey;" class="my-2" />

                  <v-card-text>
                    <p>{{lodging.address}}</p>
                    <p>평점 : {{lodging.review_avg_score}}</p>
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
import {
  mapState,
  mapActions
} from "vuex"
import 'vue-cal/dist/drag-and-drop.js'
import lodgingDetail from './lodgingDetail'

export default {
  name: "lodgingList",
  components: {
    lodgingDetail
  },
  props: {
    lodgingpage: {
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
      lodgings: [],
      dialog: false,
      lodgingnum: 0,
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
      axios.get(`http://i02b207.p.ssafy.io:8083/api/lodgings/`, {
          params: {
            page: this.lodgingpage,
            area: this.planarea
          }
        })
        .then(res => {
          this.lodgings = res.data.results
          this.$emit('lodginglist', this.lodgings)
          this.planarea = ''
        })
        .catch(() => {})
    },
    GoDetail(lodging) {
      this.lodgingnum = lodging
    },
  },
  watch: {
    lodgingpage: {
      immediate: "true",
      handler: "getDetailInfo"
    }
  }
}
</script>

<style lang="scss" scoped>
  @import url('https://fonts.googleapis.com/css?family=Lato');
  *,
  *::after,
  *::before {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  /* body */
  body {
    min-height: 100vh;
    padding: 40px;

    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;

    background: hsl(220, 10%, 12%);
    font-family: "Lato", "Segoe Ui", -apple-system, BlinkMacSystemFont, sans-serif;
  }

  /* .flip-card-container */
  .flip-card-container {
    --hue: 150;
    --primary: hsl(var(--hue), 50%, 50%);
    --white-1: hsl(0, 0%, 90%);
    --white-2: hsl(0, 0%, 80%);
    --dark: hsl(var(--hue), 25%, 10%);
    --grey: hsl(0, 0%, 50%);

    width: 150px;
    height: 250px;
    margin: 10px;

    perspective: 1000px;
  }

  /* .flip-card */
  .flip-card {
    width: inherit;
    height: inherit;

    position: relative;
    transform-style: preserve-3d;
    transition: .6s .1s;
  }

  /* hover and focus-within states */
  .flip-card-container:hover .flip-card,
  .flip-card-container:focus-within .flip-card {
    transform: rotateY(180deg);
  }

  /* .card-... */
  .card-front,
  .card-back {
    width: 100%;
    height: 100%;
    border-radius: 24px;

    background: var(--dark);
    position: absolute;
    top: 0;
    left: 0;
    overflow: hidden;

    backface-visibility: hidden;

    display: flex;
    justify-content: center;
    align-items: center;
  }

  /* .card-front */
  .card-front {
    transform: rotateY(0deg);
    z-index: 2;
  }

  /* .card-back */
  .card-back {
    transform: rotateY(180deg);
    z-index: 1;
  }

  /* figure */
  figure {
    z-index: -1;
  }

  /* figure, .img-bg */
  figure,
  .img-bg {
    position: absolute;
    top: 0;
    left: 0;

    width: 100%;
    height: 100%;
  }

  /* img */
  img {
    height: 100%;
    border-radius: 24px;
  }

  /* figcaption */
  figcaption {
    display: block;
    text-align: center;
    margin-top: 12%;
    text-align: center;
    font-weight: bold;
    line-height: 1.6;

    position: absolute;
    top: 0;
    color: var(--white-1);
    background: hsla(var(--hue), 25%, 10%, .5);
  }

  /* .img-bg */
  .img-bg {
    background: hsla(var(--hue), 25%, 10%, .5);
  }

  .card-front .img-bg {
    clip-path: polygon(0 20%, 100% 40%, 100% 100%, 0 100%);
  }



  .card-back .img-bg {
    clip-path: polygon(0 0, 100% 0, 100% 80%, 0 60%);
  }

  /* hover state */
  .flip-card-container:hover .card-front .img-bg::before {
    width: 6px;
    border-left-color: var(--primary);
    border-right-color: var(--primary);
  }

  /* ul */
  ul {
    padding-top: 50%;
    margin: 0 auto;
    width: 70%;
    height: 100%;

    list-style: none;
    color: var(--white-1);

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  /* li */
  li {
    width: 100%;
    margin-top: 12px;
    padding-bottom: 12px;

    font-size: 14px;
    text-align: center;

    position: relative;
  }

  li:nth-child(2n) {
    color: var(--white-2);
  }

  li:not(:last-child)::after {
    content: "";

    position: absolute;
    bottom: 0;
    left: 0;

    width: 100%;
    height: 1px;

    background: currentColor;
    opacity: .2;
  }

  /* button */
  button {
    font-family: inherit;
    font-weight: bold;
    color: var(--white-1);

    letter-spacing: 2px;

    padding: 9px 20px;
    border: 1px solid var(--grey);
    border-radius: 1000px;
    background: transparent;
    transition: .3s;

    cursor: pointer;
  }

  button:hover,
  button:focus {
    color: var(--primary);
    background: hsla(var(--hue), 25%, 10%, .2);
    border-color: currentColor;
  }

  button:active {
    transform: translate(2px);
  }

  /* .design-container */
  .design-container {
    --tr: 90;
    --op: .5;

    width: 100%;
    height: 100%;

    background: transparent;
    position: absolute;
    top: 0;
    left: 0;

    pointer-events: none;
  }


  /* states */
  button:hover+.design-container,
  button:active+.design-container,
  button:focus+.design-container {
    --tr: 20;
    --op: .7;
  }

  .abs-site-link {
    position: fixed;
    bottom: 20px;
    left: 20px;
    color: hsla(0, 0%, 100%, .6);
    font-size: 16px;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
  }
</style>