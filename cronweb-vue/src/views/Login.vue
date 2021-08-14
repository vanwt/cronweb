<template>
    <div style="width: 100%;height: 100vh;background-color: darkslateblue;overflow: hidden">
        <div style="width: 400px;margin: 200px auto;padding: 50px">
            <h1 style="color: white;text-align: center;padding-bottom: 30px">用户登陆</h1>
            <el-form ref="form" :model="form" size="normal">
                <el-form-item>
                    <el-input prefix-icon="el-icon-lock" v-model="form.username" clearable></el-input>
                </el-form-item>

                <el-form-item>
                    <el-input prefix-icon="el-icon-user" v-model="form.password" show-password></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button style="width: 100%" type="primary" @click="login">登陆</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>

    import request from "../utils/request";

    export default {
        name: "Login",
        data() {
            return {
                form: {}
            }
        },
        methods: {
            login() {
                request.post("/login", this.form).then(resp => {
                    if (resp.code === 0) {
                        console.log(JSON.stringify(resp.data))
                        this.$message({
                            type: 'success',
                            message: '登陆成功',
                            duration: 1300,
                            onClose: () => {
                                this.$router.push("/cron")
                            }
                        })

                    } else {
                        this.$message({
                            type: 'error',
                            message: resp.msg
                        })
                    }
                    console.log(resp)
                }).catch(err => {
                    console.log(err)
                })
            }
        }
    }
</script>

<style scoped>

</style>