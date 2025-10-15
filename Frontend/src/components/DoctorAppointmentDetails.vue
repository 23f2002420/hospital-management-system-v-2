<script>
import axios from 'axios'
import Navbar from './Navbar.vue'

export default{
    name: 'DoctorAppointmentDetails',
    components: {
        Navbar
    },
    data(){
        return {
            appointment: null,
            patientHistory : [],
            treatment: {
                diagnosis: '',
                prescription: '',
                notes: ''
            },
            isLoading: true,
            error: null
        }
    },
    async created(){
        const appointmentId = this.$route.params.id
        this.fetchAppointmentDetails(appointmentId)
    },
    methods:{
        async fetchAppointmentDetails(id){
            this.isLoading = true
            this.error= null
            try{
                const token = localStorage.getItem('accessToken')
                const response = await axios.get(`http://127.0.0.1:5000/api/doctor/appointment/${id}`,{
                    headers : {'Authorization': `Bearer ${token}`}
                })
                this.appointment = response.data

                if (this.appointment.patient_id){
                    await this.fetchPatientHistory(this.appointment.patient_id)
                }
            } catch(error){
                this.error = "Failed to fetch appointment details."
                console.error(error)
            }finally{
              this.isLoading = false
            }
        },
        async fetchPatientHistory(patientId){
            try{
                const token = localStorage.getItem('accessToken')
                const response = await axios.get(`http://127.0.0.1:5000/api/patients/${patientId}/history`,{
                    headers : {'Authorization': `Bearer ${token}`}
                })
                this.patientHistory = response.data
            }catch(error){
                console.error('Could not fetch patient history:', error)
            }
        },
        async completeAppointment(){
            if (!this.treatment.diagnosis || !this.treatment.prescription){
                alert('Diagnosis and prescription are required to complete the appointment.')
                return 
            }
            try{
                const token = localStorage.getItem('accessToken')
                await axios.put(`http://127.0.0.1:5000/api/appointments/${this.appointment.id}/complete`, this.treatment,{
                    headers: {'Authorization': `Bearer ${token}`}
                })
                this.$router.push('/doctor')
            }catch(error){
                alert("Failed to update the appointment.")
                console.error(error)
            }
        }
    }
}

</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <div v-if="isLoading" class="text-center mt-5">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="!isLoading && appointment">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="mb-0">Update Appointment</h1>
            <router-link to="/doctor" class="btn btn-secondary">← Back to Dashboard</router-link>
        </div>

        <div class="card mb-4 shadow-sm">
          <div class="card-header">
            <h4>Patient: {{ appointment.patient_name }}</h4>
          </div>
          <div class="card-body">
            <p><strong>Date & Time:</strong> {{ appointment.date }} at {{ appointment.time }}</p>
            <p><strong>Current Status:</strong> {{ appointment.status }}</p>
          </div>
        </div>

        <div v-if="appointment.status === 'Booked'" class="card mb-4 shadow-sm">
          <div class="card-header">
            <h4>Provide Treatment Notes</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="completeAppointment">
              <div class="mb-3">
                <label for="diagnosis" class="form-label fw-bold">Diagnosis</label>
                <textarea class="form-control" id="diagnosis" rows="3" v-model="treatment.diagnosis" required></textarea>
              </div>
              <div class="mb-3">
                <label for="prescription" class="form-label fw-bold">Prescription</label>
                <textarea class="form-control" id="prescription" rows="3" v-model="treatment.prescription" required></textarea>
              </div>
              <div class="mb-3">
                <label for="notes" class="form-label fw-bold">Additional Notes (Optional)</label>
                <textarea class="form-control" id="notes" rows="2" v-model="treatment.notes"></textarea>
              </div>
              <button type="submit" class="btn btn-success w-100">Mark as Complete & Save</button>
            </form>
          </div>
        </div>
        <div v-else class="alert alert-info">This appointment has already been completed or cancelled.</div>


        <div class="card shadow-sm">
          <div class="card-header">
            <h4>Patient's Past Medical History</h4>
          </div>
          <div class="card-body">
            <div v-if="patientHistory.length === 0" class="text-muted">No past history found for this patient.</div>
            <div v-else class="table-responsive">
              <table class="table table-striped">
                <thead class="table-light">
                  <tr>
                    <th>Date</th>
                    <th>Attending Doctor</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in patientHistory" :key="record.appointment_id">
                    <td>{{ record.date }}</td>
                    <td>{{ record.doctor_name }}</td>
                    <td>{{ record.diagnosis }}</td>
                    <td>{{ record.prescription }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<style></style>