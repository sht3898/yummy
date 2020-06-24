<template>
  <!-- <v-card>
    <v-tabs
      v-model="tab"
      background-color="transparent"
      color="basil"
      grow>
      <v-tab v-for="item in ['로그인', '회원가입']" :key="item">
        {{ item }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item> 
        <ValidationObserver ref="observer" v-slot="{ handleSubmit }">
          <form @submit.prevent="handleSubmit(login({email:email, password:password}))">
            <ValidationProvider name="email" rules="required|email" v-slot="{ errors }">
              <v-text-field v-model="email" :error-messages="errors" label="이메일" id="email" required />
            </ValidationProvider>
            <ValidationProvider name="password" rules="required" v-slot="{ errors }">
              <v-text-field v-model="password" label="비밀번호" type="password" :error-messages="errors" id="password" />
            </ValidationProvider>
            <v-btn type="submit" color="primary">로그인</v-btn>
          </form>
        </ValidationObserver>
      </v-tab-item>
      <v-tab-item> 
        <ValidationObserver ref="observer" v-slot="{ handleSubmit, reset }">
          <form @submit.prevent="handleSubmit(submitSignup)" @reset.prevent="reset">
            <ValidationProvider name="email" rules="required|email" v-slot="{ errors }">
              <v-text-field v-model="email" :error-messages="errors" label="이메일" id="email" required />
            </ValidationProvider>
            <ValidationProvider name="password" rules="required|min:6|confirm:@confirmation" v-slot="{ errors }">
              <v-text-field v-model="password" label="비밀번호" type="password" :error-messages="errors" id="password" />
            </ValidationProvider>
            <ValidationProvider name="passwordConfirm" vid="confirmation" rules="required" v-slot="{ errors }">
              <v-text-field v-model="passwordConfirm" label="비밀번호확인" type="password" :error-messages="errors" id="passwordComfirm" />
            </ValidationProvider>
            <ValidationProvider name="nickname" rules="required" v-slot="{ errors }">
              <v-text-field id="nickname" v-model="nickname" label="닉네임" :error-messages="errors" />
            </ValidationProvider>
            <ValidationProvider name="gender" rules="required" v-slot="{ errors }">
              <v-select v-model="gender" :items="['남', '여']" :error-messages="errors" label="성별" data-vv-name="select" required></v-select>
            </ValidationProvider>
            <ValidationProvider name="birthYear" rules="required" v-slot="{ errors }">
              <v-menu v-model="menu" close-on-click close-on-content-click >
                <template v-slot:activator="{ on }">
                  <v-text-field id="birthYear" v-model="birthYear" label="생년월일" v-on="on" :error-messages="errors" readonly />
                </template>
                <v-date-picker ref="picker" @input="setBirthYear" :max="new Date().toISOString().substr(0, 10)" min="1920-01-01" reactive no-title></v-date-picker>
              </v-menu>
            </ValidationProvider>
            <v-btn type="submit" color="primary">회원가입</v-btn>
            <v-btn type="reset" @click="resetSignup">다시 입력하기</v-btn>
          </form>
        </ValidationObserver>
      </v-tab-item>
      
    </v-tabs-items>
  </v-card> -->
  <div>
    <div class="cotn_principal">
<div class="cont_centrar">

  <div class="cont_login">
<div class="cont_info_log_sign_up">
      <div class="col_md_login">
<div class="cont_ba_opcitiy">
        
        <h2>LOGIN</h2>  
  <button class="btn_login" @click="cambiar_login()">LOGIN</button>
  </div>
  </div>
<div class="col_md_sign_up">
<div class="cont_ba_opcitiy">
  <h2>SIGN UP</h2>

  <button class="btn_sign_up" @click="cambiar_sign_up()">SIGN UP</button>
</div>
  </div>
       </div>

    
    <div class="cont_back_info">
       <div class="cont_img_back_grey">
       <img src="https://images.unsplash.com/42/U7Fc1sy5SCUDIu4tlJY3_NY_by_PhilippHenzler_philmotion.de.jpg?ixlib=rb-0.3.5&q=50&fm=jpg&crop=entropy&s=7686972873678f32efaf2cd79671673d" alt="" />
       </div>
       
    </div>
<div class="cont_forms" >
    <div class="cont_img_back_">
       <img src="https://images.unsplash.com/42/U7Fc1sy5SCUDIu4tlJY3_NY_by_PhilippHenzler_philmotion.de.jpg?ixlib=rb-0.3.5&q=50&fm=jpg&crop=entropy&s=7686972873678f32efaf2cd79671673d" alt="" />
       </div>
 <div class="cont_form_login">
<a href="#" @click="ocultar_login_sign_up()" ><i class="material-icons">&#xE5C4;</i></a>
   <h2>LOGIN</h2>
     <ValidationObserver ref="observer" v-slot="{ handleSubmit }">
         <form @submit.prevent="handleSubmit(login({email:email, password:password}))">
              <ValidationProvider name="email" rules="required|email" v-slot="{ errors }">
                 <input v-model="email" :error-messages="errors" type="text" placeholder="Email" required />
            </ValidationProvider>
            <ValidationProvider name="password" rules="required" v-slot="{ errors }">
                <input v-model="password" type="password" :error-messages="errors" placeholder="Password" />
            </ValidationProvider>
            <button type="submit" class="btn_login" @click="cambiar_login()">LOGIN</button>
         </form>
     </ValidationObserver>
  </div>
  
   <div class="cont_form_sign_up">
<a href="#" @click="ocultar_login_sign_up()"><i class="material-icons">&#xE5C4;</i></a>
     <h2>SIGN UP</h2>
<input type="text" placeholder="Email" />
<input type="text" placeholder="User" />
<input type="password" placeholder="Password" />
<input type="password" placeholder="Confirm Password" />
<button class="btn_sign_up" @click="cambiar_sign_up()">SIGN UP</button>

  </div>

    </div>
    
  </div>
 </div>
</div>
  </div>
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
      }
  },
  computed:{
    ...mapState(["isLogin","isLoginError"])
  },
  methods: {
    // 뷰엑스
    ...mapActions(["login"]),
    // CSS
    cambiar_login() {
      document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_login";  
      document.querySelector('.cont_form_login').style.display = "block";
      document.querySelector('.cont_form_sign_up').style.opacity = "0";               

      setTimeout(function(){  document.querySelector('.cont_form_login').style.opacity = "1"; },400);  
        
      setTimeout(function(){    
      document.querySelector('.cont_form_sign_up').style.display = "none";
      },200);  
    },
    cambiar_sign_up(at) {
      document.querySelector('.cont_forms').className = "cont_forms cont_forms_active_sign_up";
      document.querySelector('.cont_form_sign_up').style.display = "block";
      document.querySelector('.cont_form_login').style.opacity = "0";
        
      setTimeout(function(){  document.querySelector('.cont_form_sign_up').style.opacity = "1";
      },100);  

      setTimeout(function(){   document.querySelector('.cont_form_login').style.display = "none";
      },400);  
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