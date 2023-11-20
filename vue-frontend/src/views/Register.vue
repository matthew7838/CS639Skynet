<template>
  <div style="height: 100vh; display: flex; align-items: center; justify-content: center; background-color: #669fef">
    <div style="display: flex; background-color: white; width: 50%; border-radius: 5px; overflow: hidden">
      <div style="flex: 1">
        <img src="@/assets/register.png" alt="" style="width: 100%">
      </div>
      <div style="flex: 1; display: flex; align-items: center; justify-content: center">
        <el-form :model="user" style="width: 80%" :rules="rules" ref="registerRef">
          <div style="font-size: 20px; font-weight: bold; text-align: center; margin-bottom: 20px">Welcome UCS Satellite System</div>
          <el-form-item prop="username">
            <el-input prefix-icon="el-icon-user" size="medium" placeholder="Please Enter Username" v-model="user.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input prefix-icon="el-icon-lock" size="medium" show-password placeholder="Please Enter Password" v-model="user.password"></el-input>
          </el-form-item>
          <el-form-item prop="confirmPass">
            <el-input prefix-icon="el-icon-lock" size="medium" show-password placeholder="Please Confirm Password" v-model="user.confirmPass"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="info" style="width: 100%" @click="register">Register</el-button>
          </el-form-item>
          <div style="display: flex">
            <div style="flex: 1">Having account？<span style="color: #6e77f2; cursor: pointer" @click="$router.push('/login')">Login</span></div>
          </div>
        </el-form>
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: "Register",
  data() {
    // Verification code verification
    const validatePassword = (rule, confirmPass, callback) => {
      if (confirmPass === '') {
        callback(new Error('Please Confirm Password'))
      } else if (confirmPass !== this.user.password) {
        callback(new Error('Passwords Are Inconsistent'))
      } else {
        callback()
      }
    }
    return {
      user: {
        username: '',
        password: '',
        confirmPass: ''
      },
      rules: {
        username: [
          { required: true, message: 'Please Enter Username', trigger: 'blur' },
        ],
        password: [
          { required: true, message: 'Please Enter Password', trigger: 'blur' },
        ],
        confirmPass: [
          { validator: validatePassword, trigger: 'blur' }
        ],
      }
    }
  },
  created() {

  },
  methods: {
    register() {
      this.$refs['registerRef'].validate((valid) => {
        if (valid) {
          // Verification passed
          this.$request.post('/register', this.user).then(res => {
            if (res.code === '200') {
              this.$router.push('/login')
              this.$message.success('Registration Success')
            } else {
              this.$message.error(res.msg)
            }
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>