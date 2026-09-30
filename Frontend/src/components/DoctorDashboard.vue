<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'DoctorDashboard',
  components: {
    Navbar
  },
  data() {
    return {
      doctorName: '',
      appointments: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    upcomingAppointments() {
      return this.appointments
        .filter(appt => appt.status === 'Booked')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
    },
    pastAppointments() {
      return this.appointments
        .filter(appt => appt.status !== 'Booked')
        .sort((a, b) => new Date(b.date) - new Date(a.date))
    }
  },
  async created() {
    this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { 'Authorization': `Bearer ${token}` }
        const [profileRes, appointmentsRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/doctor/profile', { headers }),
          axios.get('http://127.0.0.1:5000/api/doctor/appointments', { headers })
        ]);

        // Set the data from the API responses
        this.doctorName = profileRes.data.name;
        this.appointments = appointmentsRes.data;

      } catch (err) {
        this.error = 'Failed to fetch your dashboard data.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    getStatusClass(status) {
      if (status === 'Completed') return 'bg-success';
      if (status === 'Cancelled') return 'bg-danger';
      return 'bg-secondary';
    }
  }
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <header class="p-3 mb-4 bg-light border rounded-3">
        <h1 class="display-5">
          <span v-if="doctorName">Dr. {{ doctorName }}'s</span>
          <span v-else>Doctor</span>
          Dashboard
        </h1>
        <p class="text-muted">View and manage your patient appointments.</p>
      </header>
      
      <div v-if="loading" class="text-center mt-5">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="!loading && !error" class="row">
        <div class="col-lg-7 mb-4">
          <div class="card shadow-sm h-100">
            <div class="card-header"><h4>Upcoming Appointments</h4></div>
            <div class="card-body">
              <div v-if="upcomingAppointments.length === 0" class="text-center text-muted p-4">
                You have no upcoming appointments.
              </div>
              <ul v-else class="list-group list-group-flush">
                <li v-for="appt in upcomingAppointments" :key="appt.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="mb-1">Patient: {{ appt.patient_name }}</h6>
                    <small class="text-secondary">{{ appt.date }} at {{ appt.time }}</small>
                  </div>
                  <router-link :to="{ name: 'DoctorAppointmentDetails', params: { id: appt.id } }" class="btn btn-primary">
                    View & Update
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-lg-5 mb-4">
          <div class="card shadow-sm h-100">
            <div class="card-header"><h4>Past Appointments</h4></div>
            <div class="card-body">
              <div v-if="pastAppointments.length === 0" class="text-center text-muted p-4">
                No past appointment records found.
              </div>
              <ul v-else class="list-group list-group-flush">
                <li v-for="appt in pastAppointments" :key="appt.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <span class="me-2">{{ appt.patient_name }}</span>
                    <small class="text-muted">({{ appt.date }})</small>
                  </div>
                  <span class="badge" :class="getStatusClass(appt.status)">{{ appt.status }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>