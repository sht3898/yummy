<template>
  <v-app id="app">
    <app-bar class="mx-0" />
    <route-view class="mx-0" />
    <go-top />
    <!-- footer -->
    <v-footer dark padless class="mt-7">
      <v-card class="flex" flat tile>
        <v-card-text class="py-2 white--text text-center">
          <p class="overline white--text">SSAFY 7팀 김성훈 김인성 김홍주 서현택</p>
        </v-card-text>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script>
import AppBar from "@/components/header/AppBar";
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import "../src/css/app.css";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    AppBar,
    RouteView,
    GoTop
  },
  data: () => ({
  }),
  methods: {
    ...mapActions(["getUserInfo"])
  },
  mounted() {
    if (localStorage.getItem("access_token")) {
      this.getUserInfo();
    }
  }
};
</script>

<style lang="scss" scoped>


</style>
