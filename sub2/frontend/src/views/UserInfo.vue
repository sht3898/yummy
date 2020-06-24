<template>
<v-col md="12" sm="12" xs="12">
  <v-container class="mx-auto">
    <v-row class="mx-0 mb-5">
      <v-col><h2>{{ userinfo.nickname}}님의 회원 정보</h2></v-col>
    </v-row>
    <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
    <v-row>
        <v-col class="my-auto py-5" cols="3" style="text-align:center">아이디(이메일)</v-col>
        <v-col class="my-auto py-5" cols="8">{{userinfo.email}}</v-col>
    </v-row>
    <v-row v-if="!userinfo.isSocial">
        <v-col class="my-auto py-5" cols="3" style="text-align:center">비밀번호</v-col>
        <v-col class="my-auto py-5" cols="8">
            <v-text-field v-model="password" type="password" outlined/>
        </v-col>
    </v-row>
    <v-row>
        <v-col class="my-auto py-5" cols="3" style="text-align:center">이름</v-col>
        <v-col cols="8">
            <v-text-field v-model="nickname" outlined/>
        </v-col>
    </v-row>
    <v-row>
        <v-col class="my-auto py-5" cols="3" style="text-align:center">성별</v-col>
        <v-col cols="8">
            <v-select v-model="gender" :items="['남', '여']" :placeholder="userinfo.gender" outlined data-vv-name="select" required></v-select>
        </v-col>
    </v-row>
    <v-row>
        <v-col class="my-auto py-5" cols="3" style="text-align:center">출생년도</v-col>
        <v-col cols="8">
            <v-menu v-model="menu" close-on-click close-on-content-click >
                <template v-slot:activator="{ on }">
                    <v-text-field id="birthYear" v-model="birthYear" outlined v-on="on" readonly />
                </template>
                <v-date-picker ref="picker" @input="setBirthYear" :max="new Date().toISOString().substr(0, 10)" min="1920-01-01" reactive no-title></v-date-picker>
            </v-menu>
        </v-col>
    </v-row>
    <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
    <v-row class="my-4">
        <v-col cols="1"></v-col>
        <v-btn class="mr-3" text style="color:#e74c3c; font-weight:bold" @click="exit()">탈퇴하기</v-btn>
        <v-spacer></v-spacer>
        <v-btn class="mr-3" dark style="background-color:#3498db" @click="modify()">수정하기</v-btn>
        <v-col cols="1"></v-col>
    </v-row>

  </v-container>
  </v-col>
</template>

<script>
import {mapState, mapActions} from "vuex"
import router from "../router"
import axios from "axios"

export default {
    name:"userInfo",
    data(){
        return{
            menu:false,
            password:"",
            nickname:"",
            gender:"",
            birthYear:"",
        }
    },
    methods:{
        ...mapActions(["getUserInfo", "logout"]),
        setBirthYear(date){
            var saveDate = new Date(date)
            this.birthYear = saveDate.toISOString().substr(0, 4)
        },
        setUserInfo(){
            this.nickname = this.userinfo.nickname
            this.gender = this.userinfo.gender
            this.birthYear = this.userinfo.birth_year
        },
        modify(){
            const options = {headers: {Authorization : localStorage.getItem("access_token")}}
            let modifyForm = new FormData()
            if (this.password.length)
                modifyForm.append("password", this.password)
            if (this.birthYear != this.userinfo.birth_year)
                modifyForm.append("birth_year", this.birthYear)
            if (this.nickname != this.userinfo.nickname)
                modifyForm.append("nickname", this.nickname)
            if (this.gender != this.userinfo.gender)
                modifyForm.append("gender", this.gender)
            axios.patch("http://i02b207.p.ssafy.io:8083/auth/modify/", modifyForm, options)
            .then((response)=>{
                alert(response.data)
                this.getUserInfo()
            })
        },
        backPage(){
            router.go(-2)
        },
        exit(){
            const options = {headers: {Authorization : localStorage.getItem("access_token")}}
            axios.delete("http://i02b207.p.ssafy.io:8083/auth/modify/", options)
            .then((response)=>{
                alert(response.data)
                this.logout()
            })
        }
    },
    computed:{
        ...mapState(["userinfo"])
    },
    watch:{
        menu(val) {
            val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
        },
        userinfo:{
            deep:true,
            handler:"setUserInfo"
        }
    },
    mounted(){
        if (this.$store.passwordVerified){
            this.setUserInfo()
            this.$store.passwordVerified = false
        }
        else
            router.push({name:"verify"})
    }
}
</script>

<style>
.v-text-field__details{
    display: none;
}
.v-input__slot{
    margin-bottom: 0px;
}
</style>