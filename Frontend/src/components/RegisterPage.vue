<script>
import axios from 'axios'

export default{
    data(){
        return {
            name:"",
            username : "",
            password : "",
            errorMessage: ""
        }
    },
    methods:{
        async handleRegister(){
            this.errorMessage = "";

            try{
                const response = await axios.post("http://127.0.0.1:5000/api/register",{
                    name: this.name,
                    username: this.username,
                    password: this.password
                });
                
                alert('Registration successful! Please Login.')
                
                this.$router.push('/login')
            } catch(error){
                if (error.response){
                    this.errorMessage = error.response.data.message;
                }else{
                    this.errorMessage = "An error occurred. Please try again later."
                }
            }
        }
    }
}
</script>


<template>
   <div class="container-fluid d-flex justify-content-center align-items-center vh-100 bg-light">
        <div class="col-11 col-sm-8 col-md-6 col-lg-4 col-xl-3">
            <div class="card shadow-lg border-0 rounded-4">
                <div class="card-body p-4 p-md-5">
                    <h2 class = "card-title text-center fw-bold mb-4">Register Patient</h2>
                    <div v-if = "errorMessage" class = "alert alert-danger" role = "alert">
                        {{errorMessage}}
                    </div>
                    <form @submit.prevent = "handleRegister">

                        <div class = "form-floating mb-3">
                            <input type = "text" class = "form-control" id = "name" placeholder= "Full Name" v-model = "name" required>
                            <label for = "name">Name</label>
                        </div>

                        <div class = "form-floating mb-3">
                            <input type = "text" class = "form-control" id = "username" placeholder= "Username" v-model = "username" required>
                            <label for = "username">Username</label>
                        </div>

                        <div class = "form-floating mb-4">
                            <input type = "password" class = "form-control" id = "password" placeholder= "Password" v-model = "password" required>
                            <label for = "password">Password</label>
                        </div>

                        <div class = "d-grid">
                            <button type = "submit" class = "btn btn-primary btn-lg fw-bold">Register</button>
                        </div>
                    </form>
                    <div class = "text-center mt-4">
                        <small class = "text-muted">Already have an account?
                            <router-link to = "/login">Login Here</router-link>
                        </small>
                    </div>
                </div>
            </div>
        </div>
   </div>

</template>



<style scoped>
.card{
    transition : all 0.3s ease-in-out;
}

.card:hover{
    transform : translateY(-5px);
}

</style>