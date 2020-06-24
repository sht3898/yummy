<template>
   <v-responsive style="background:white;" class="pa-2">
    <v-row class="pt-0" align="start" justify="center">
      <v-col cols=12>
        <div style="text-align:center;" class="mt-1 mb-2">
        <span class ="title">
          맛있는 여행의 아름다움
          </span>
            <br>
          <span class="headline" style="font-weight: bold; ">
          Y <b style="color:#3498db">U</b> M M Y
        </span>
        </div>
         <hr style="border-top: 1px dashed lightgrey;" class="my-2" />
    <v-tabs
      v-model="tab"
      background-color="transparent"
      color="basil"
      centered
      fixed
      grow>
      <v-tab v-for="item in ['로그인', '회원가입']" :key="item" class="mx-0">
        {{ item }}
      </v-tab>
    </v-tabs>
      </v-col>
      <v-col cols=12 class="my-2">
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <ValidationObserver ref="observer" v-slot="{ handleSubmit }">
          <form @submit.prevent="handleSubmit(login({email:email, password:password}))">
            <ValidationProvider name="email" rules="required|email" v-slot="{ errors }">
              <v-text-field 
              outlined
              v-model="email" :error-messages="errors" label="이메일" id="email" required />
            </ValidationProvider>
            <ValidationProvider name="password" rules="required" v-slot="{ errors }">
              <v-text-field outlined v-model="password" label="비밀번호" type="password" :error-messages="errors" id="password" />
            </ValidationProvider>
            <v-btn type="submit" large block color="primary">로그인</v-btn>
            <br>
            <v-btn large @click="googleAuth" block color="white">
               <v-avatar size="36">
      <img
        src="https://t1.daumcdn.net/thumb/R720x0/?fname=http://t1.daumcdn.net/brunch/service/user/5rH/image/LHUiJV1nog0BqnOJ8Mtj5UbNTjQ"
       alt='G'>
    </v-avatar>
              oogle 로그인</v-btn>
          </form>
        </ValidationObserver>
      </v-tab-item>
      <v-tab-item> 
        <ValidationObserver ref="observer" v-slot="{ handleSubmit, reset }">
          <form @submit.prevent="handleSubmit(submitSignup)" @reset.prevent="reset">
            <ValidationProvider name="email" rules="required|email" v-slot="{ errors }">
              <v-text-field outlined v-model="email" :error-messages="errors" label="이메일" id="email" required />
            </ValidationProvider>
            <ValidationProvider name="password" rules="required|min:6|confirm:@confirmation" v-slot="{ errors }">
              <v-text-field outlined v-model="password" label="비밀번호" type="password" :error-messages="errors" id="password" />
            </ValidationProvider>
            <ValidationProvider name="passwordConfirm" vid="confirmation" rules="required" v-slot="{ errors }">
              <v-text-field outlined v-model="passwordConfirm" label="비밀번호확인" type="password" :error-messages="errors" id="passwordComfirm" />
            </ValidationProvider>
            <ValidationProvider name="nickname" rules="required" v-slot="{ errors }">
              <v-text-field outlined id="nickname" v-model="nickname" label="닉네임" :error-messages="errors" />
            </ValidationProvider>
            <ValidationProvider name="gender" rules="required" v-slot="{ errors }">
              <v-select outlined v-model="gender" :items="['남', '여']" :error-messages="errors" label="성별" data-vv-name="select" required></v-select>
            </ValidationProvider>
            <ValidationProvider name="birthYear" rules="required" v-slot="{ errors }">
              <v-menu v-model="menu" close-on-click close-on-content-click >
                <template v-slot:activator="{ on }">
                  <v-text-field outlined id="birthYear" v-model="birthYear" label="생년월일" v-on="on" :error-messages="errors" readonly />
                </template>
                <v-date-picker ref="picker" @input="setBirthYear" :max="new Date().toISOString().substr(0, 10)" min="1920-01-01" reactive no-title></v-date-picker>
              </v-menu>
            </ValidationProvider>
              <v-row class="pt-0" align="start" justify="center">
                <v-col cols=6>

            <v-btn large type="reset" @click="resetSignup" outlined block color="primary">재입력</v-btn>
                </v-col>
                <v-col cols=6>
            <v-btn large type="submit" color="primary" block>회원가입</v-btn>
                </v-col>
              </v-row>
          </form>
        </ValidationObserver>
      </v-tab-item>
      
    </v-tabs-items>
      </v-col>
    </v-row>
   </v-responsive>
</template>

<script>
import { required, email, min } from 'vee-validate/dist/rules'
import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
import router from "../../../router"
import axios from 'axios'
import {mapState, mapActions} from "vuex"
import '../../../css/login.css'


setInteractionMode('eager')
extend('confirm', {
  params: ['target'],
  validate(value, { target }) {
    return value === target;
  },
  message: '비밀번호가 일치하지 않습니다'
})

extend('required', {
  ...required,
  message: '{_field_}는 필수 입력항목입니다.',
})

extend('email', {
  ...email,
  message: '유효한 이메일을 적어주세요!',
})

extend('min', {
  ...min,
  message: '비밀번호는 6자리 이상이여야 합니다!',
})


export default {
  name: "loginModal",
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => {
      return {
        menu: false,
        modal: false,
        tab: null,
        birthYear:'',
        email: '',
        password: '',
        passwordConfirm: '',
        nickname: '',
        gender:'',
        kakao:process.env.VUE_APP_KAKAO,

      }
  },
  computed:{
    ...mapState(["isLogin","isLoginError"])
  },
  methods: {
    // 뷰엑스
    ...mapActions(["login"]),
    // 구글 로그인
    googleAuth(){
      this.$gAuth.getAuthCode()
      .then(authCode => {
        axios.post('http://i02b207.p.ssafy.io:8083/auth/google', {code: authCode, redirect_uri: 'postmessage'})
        .then(res => {
          this.login({email:res.data.email, password:res.data.email})
        })
      })
      .catch(error => {
        //on fail do something
      })
    },
    
    // 로그인 폼 관련 함수
    setBirthYear(date){
      var saveDate = new Date(date)
      this.birthYear = saveDate.toISOString().substr(0, 4)
    },
    resetSignup(){
      this.birthYear=''
      this.email=''
      this.password=''
      this.passwordConfirm=''
      this.nickname=''
      this.gender=''
    },
    submitSignup() {
      let createForm = new FormData()
      createForm.append('gender', this.gender)
      createForm.append('nickname', this.nickname)
      createForm.append('birth_year', this.birthYear)
      createForm.append('email', this.email)
      createForm.append('password1', this.password)
      createForm.append('password2', this.passwordConfirm)
      
      axios.post("http://i02b207.p.ssafy.io:8083/auth/signup/", createForm)
        .then(() => {
          this.$store.state.dialog = true
          if (confirm("회원가입이 완료되었습니다 즉시 로그인 하시겠습니까?")){
            this.login({email:this.email, password:this.password})
          }
          this.birthYear=''
          this.email=''
          this.password=''
          this.passwordConfirm=''
          this.nickname=''
          this.gender=''
        })
        .catch((err)=>{
          var msg = ""
          var emailError = err.response.data.email
          var passwordError = err.response.data.password
          for (var i = 0; i < emailError.length; i++){
            msg = msg.concat("\n", emailError[i])
          }
          for (var i = 0; i< passwordError.length; i++){
            msg = msg.concat("\n", passwordError[i])
          }
          alert(msg)
          
        })
    },
  },
  watch:{
    menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  },
  
}
</script>
