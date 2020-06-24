import Vue from "vue";
import Vuex from "vuex";
import router from "../router";
import axios from "axios";


Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userinfo:null, //db로부터 얻어온 정보가 여기에 저장(회원정보)
        isLogin:false,
        dialog:false,
        passwordVerified:false,
        detailpage:0,
        viewnav:true
    },
    mutations: {
        loginsuccess(state, payload){
            state.isLogin = true
            state.dialog = false
            state.userinfo = payload
        },
        logout(state){
            state.isLogin = false
            state.userinfo = null
            localStorage.removeItem('access_token')
        },
        pagenum(state, payload){
            state.detailpage = payload
        }
        
    },
    actions: {
        //로그인을 시도
        login({dispatch, commit}, loginObj){ //커밋으로 mutations 실행
            var form = new FormData()
            form.append('email', loginObj.email)
            form.append('password', loginObj.password)
            axios.post("http://i02b207.p.ssafy.io:8083/auth/login/", form)
            .then(response=>{
                localStorage.setItem("access_token", response.data.token)
                dispatch("getUserInfo")
            })
            .catch(()=>{
                alert("아이디 혹은 비밀번호를 확인해주세요.")
            })
        },
        logout({commit}){
            commit("logout")
            router.push({name:"home"})
        },
        getUserInfo({commit}){
            let token = localStorage.getItem("access_token")
            if(token){
                axios.post("http://i02b207.p.ssafy.io:8083/auth/userinfo/", {token:token})
                .then(response=>{
                    let userinfo = {
                        id:response.data.user.id,
                        email: response.data.user.email,
                        gender: response.data.user.gender,
                        birth_year: response.data.user.birth_year,
                        nickname: response.data.user.nickname,
                        isSocial: response.data.user.is_social,
                    }
                    commit("loginsuccess", userinfo)
                })
                .catch(()=>{
                    localStorage.removeItem("access_token")
                    alert("접속 시간이 만료되거나 유효하지 않은 접근입니다.\n다시 로그인 해주세요")
                })
            }
        },
        GoDetail({commit}, store){
            commit("pagenum", store)
            localStorage.setItem("store_detail", store)
          },

    },
})
