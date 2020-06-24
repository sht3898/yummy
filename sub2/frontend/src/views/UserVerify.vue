<template>
  <v-container>
      <v-row class="mx-0">
        <v-col><h2>비밀번호 확인</h2></v-col>
      </v-row>
      <v-divider class="mx-2"></v-divider>
      <v-col md="12" sm="12" xs="12">
      <v-container style="width:60%">
        <v-card>
          <v-card-title class="mt-4">
            <p class="mx-auto" style="text-align:center">개인정보 조회를 위해서는 인증이 필요합니다.<br>비밀번호 입력 후 확인 버튼을 눌러주세요.</p>
          </v-card-title>
          <v-card-text>
            <v-row class="mx-auto">
              <v-col align="center" justify="center">
                <ValidationObserver ref="observer" v-slot="{ handleSubmit }">
                  <form @submit.prevent="handleSubmit(validatePassword({password:password}))">
                    <ValidationProvider name="password" rules="required|min:6" v-slot="{ errors }">
                      <v-text-field v-model="password" outlined label="비밀번호" type="password" :error-messages="errors" id="password" />
                    </ValidationProvider>
                    <br>
                    <v-btn large class="white--text" type="submit" color="#3498db" style="width:100%">확인</v-btn>
                  </form>
                </ValidationObserver>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-container>
    </v-col>
  </v-container>
</template>

<script>
import { required, min } from 'vee-validate/dist/rules'
import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
import router from "../router"
import axios from 'axios'

setInteractionMode('eager')
extend('required', {
  ...required,
  message: '{_field_}는 필수 입력항목입니다.',
})
extend('min', {
  ...min,
  message: '비밀번호는 6자리 이상이여야 합니다!',
})

export default {
    name:"PasswordValidation",
    components: {
        ValidationProvider,
        ValidationObserver,
    },
    data: () => {
        return {
            password: '',
        }
    },
    methods:{
        validatePassword(password){
            let validationForm = new FormData()
            validationForm.append('password', this.password)
            const options = {headers: {Authorization : localStorage.getItem("access_token")}}
            axios.post("http://i02b207.p.ssafy.io:8083/auth/verify/", validationForm, options)
            .then(()=> {
                this.$store.passwordVerified = true
                router.push({name: "userinfo"})
            })
            .catch((err)=> {
                alert(err.response.data)
            })
        }
    },
    created(){
        if (!localStorage.getItem("access_token")){
          alert('로그인이 만료되었거나 정상적이지 않은 접근입니다.\n다시 로그인해주세요')
          router.go(-1)
        }
    },
    mounted(){
      if (this.$store.state.userinfo.isSocial){
        this.$store.passwordVerified = true
        router.push({name: "userinfo"})
      }
    }
}
</script>

<style>
</style>