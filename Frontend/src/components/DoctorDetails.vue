<script>
import axios from 'axios'
import PatientNavbar from './PatientNavbar.vue'

export default{
    name: 'DoctorDetails',
    components:{
        PatientNavbar
    },
    data(){
        return {
            doctor: null,
            isLoading: true,
            error: null,
        }
    },
    async created(){
        const doctorId = this.$route.params.id
        this.fetchDoctor(doctorId)
    },
    methods:{
        async fetchDoctor(id){
            this.isLoading = true
            try{
                const token = localStorage.getItem('accessToken')
                const response = await axios.get('http://127.0.0.1:5000/api/doctors',{
                    headers: {'Authorization': `Bearer ${token}`}
                })
                this.doctor = response.data.find(d => d.id == id)
                if (!this.doctor){
                    throw new Error("Doctor not found")
                }
            }catch(error){
                this.error = "Failed to load doctor details."
            }finally{
                this.isLoading = false
            }
        },
        goBack(){
            this.$router.go(-1)
        }
    }
}
</script>

<template>
    <div>
        <PatientNavbar/>
        <main class = "container mt-4">
            <div v-if="isLoading" class="text-center"><div class="spinner-border"></div></div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            
            <div v-if = "!isLoading && doctor" class = "card shadow-sm">
                <div class = "card-body">
                    <div class = "row">
                        <div class="col-md-2 text-center">
                            <img src="https://i.imgur.com/C51m22s.png" class="img-fluid rounded-circle" alt="Doctor Profile">
                        </div>
                        <div class = "col-md-10">
                            <h3>Dr. {{doctor.name}}</h3>
                            <p class="text-muted mb-1">{{ doctor.specialization }}</p>
                            <p class="text-muted">{{ doctor.department }}</p>
                            <hr>
                            <p>
                                <strong>20 Years Experience Overall</strong><br>
                                Dr. {{ doctor.name }} is a specialist in {{ doctor.specialization }} with many years of experience in the field.
                            </p>
                            <div class="mt-3">
                                <router-link :to="{ name: 'BookAppointment', params: { doctorId: doctor.id } }" class="btn btn-success me-2">
                                Check Availability
                                </router-link>
                                <button @click="goBack" class="btn btn-secondary">Go Back</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

</template>

<style></style>