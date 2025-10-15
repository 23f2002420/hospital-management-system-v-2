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
        this.fetchDoctorDetails(doctorId)
    },
    methods:{
        async fetchDoctorDetails(id){
            this.isLoading = true
            this.error = null
           try {
                const token = localStorage.getItem('accessToken');
                // Call the new, more detailed API endpoint
                const response = await axios.get(`http://127.0.0.1:5000/api/doctors/${id}/details`, {
                headers: { 'Authorization': `Bearer ${token}` }
                });
                this.doctor = response.data;
            } catch (error) {
                this.error = "Failed to load doctor details.";
                console.error(error);
            } finally {
                this.isLoading = false;
            }
        }
    }
}
</script>

<template>
  <div>
    <PatientNavbar />
    <main class="container mt-4">
      <div v-if="isLoading" class="text-center mt-5">
        <div class="spinner-border" role="status"></div>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="!isLoading && doctor" class="card shadow-sm">
        <div class="card-body p-4">
          <div class="row align-items-center">
            <div class="col-md-2 text-center">
              <img :src="doctor.profile_image_url" class="img-fluid rounded-circle border" alt="Doctor Profile">
            </div>
            <div class="col-md-7">
              <h2 class="mb-0">Dr. {{ doctor.name }}</h2>
              <p class="text-muted mb-1">{{ doctor.specialization }}</p>
              <p class="text-muted">{{ doctor.department }}</p>
              <span class="badge bg-primary">{{ doctor.experience_years }} Years Experience</span>
            </div>
            <div class="col-md-3 text-end">
              <router-link :to="{ name: 'BookAppointment', params: { doctorId: doctor.id } }" class="btn btn-success btn-lg">
                Book Appointment
              </router-link>
            </div>
          </div>

          <hr class="my-4">

          <div>
            <ul class="nav nav-tabs mb-3">
              <li class="nav-item">
                <a class="nav-link active" data-bs-toggle="tab" href="#about">About</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-bs-toggle="tab" href="#services">Services & Specialization</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-bs-toggle="tab" href="#reviews">Patient Reviews</a>
              </li>
            </ul>

            <div class="tab-content">
              <div class="tab-pane fade show active" id="about">
                <h5>Bio</h5>
                <p>{{ doctor.bio }}</p>
                
                <h5 class="mt-4">Education & Qualifications</h5>
                <ul>
                  <li v-for="edu in doctor.education" :key="edu">{{ edu }}</li>
                </ul>

                <h5 class="mt-4">Languages Spoken</h5>
                <p>
                  <span v-for="lang in doctor.languages" :key="lang" class="badge bg-secondary me-2">{{ lang }}</span>
                </p>
              </div>

              <div class="tab-pane fade" id="services">
                <h5>Commonly Treated Conditions</h5>
                <ul class="list-group list-group-flush">
                  <li v-for="service in doctor.services" :key="service" class="list-group-item">{{ service }}</li>
                </ul>
              </div>

              <div class="tab-pane fade" id="reviews">
                <p class="text-muted">Patient reviews are coming soon.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>