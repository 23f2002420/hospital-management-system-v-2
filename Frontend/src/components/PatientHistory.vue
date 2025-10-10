<script>
import axios from 'axios'
import PatientNavbar from './PatientNavbar.vue'

export default{
    name: 'PatientHistory',
    components: {
        PatientNavbar
    },
    data(){
        return {
            history: [],
            isLoading : true,
            error : null
        }
    },
    async created(){
        this.fetchPatientHistory()
    },
    methods: {
        async fetchPatientHistory(){
            this.isLoading = true,
            this.error = null
            try{
                const token = localStorage.getItem('accessToken')
                const response = await axios.get('http://127.0.0.1:5000/api/patient/appointments',{
                    headers: {'Authorization': `Bearer ${token}`}
                })
                this.history = response.data
                    .filter(appt => appt.status === 'Completed' && appt.treatment)
                    .sort((a,b) => new Date(b.date) - new Date(a.date))
            }catch(error){
                this.error = "Failed to fetch your medical history."
                console.error(error)
            }finally{
                this.isLoading = false
            }
        }
    }
}
</script>

<template>
    <div>
        <PatientNavbar/>
        <main class = "container mt-4">
            <header class = "d-flex justify-content-between align-items-center mb-4">
                <h1 class = "mb-0">My Medical History</h1>
                <router-link to= "/patient" class = "btn btn-secondary">Back to Dashboard</router-link>
            </header>

            <div v-if="isLoading" class="text-center mt-5">
                <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
            </div>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if = "!isLoading && !error">
                <div v-if = "history.length ===0" class = "card card-body bg-light text-center">
                    <p class = "mb-0 text-muted">You have no past medical records.</p>
                </div>
                
                <div v-else class="accordion" id="historyAccordion">
                    <div v-for="(record, index) in history" :key="record.id" class="accordion-item">
                        <h2 class="accordion-header" :id="'heading' + index">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse' + index" aria-expanded="false" :aria-controls="'collapse' + index">
                                <strong>{{ record.date }}</strong> <span class="mx-2 text-muted">|</span> Dr. {{ record.doctor_name }}
                            </button>
                        </h2>
                        <div :id="'collapse' + index" class="accordion-collapse collapse" :aria-labelledby="'heading' + index" data-bs-parent="#historyAccordion">
                            <div class="accordion-body">
                                <div class="mb-3">
                                    <h6 class="text-primary">Diagnosis</h6>
                                    <p>{{ record.treatment.diagnosis }}</p>
                                </div>
                                <div>
                                    <h6 class="text-primary">Prescription</h6>
                                    <p>{{ record.treatment.prescription }}</p>
                                </div>
                                <div v-if="record.treatment.notes" class="mt-3">
                                    <h6 class="text-primary">Additional Notes</h6>
                                    <p class="text-muted fst-italic">{{ record.treatment.notes }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>  
            </div>
        </main>
    </div>
</template>

<style></style>