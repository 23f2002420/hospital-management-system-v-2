<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'ViewAllAppointments',
  components: {
    Navbar
  },
  data() {
    return {
      appointments: [],
      filterStatus: '',
      loading: true,
      error: null
    };
  },
  async created() {
    this.fetchAppointments();
  },
  methods: {
    async fetchAppointments() {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('accessToken');
        let url = 'http://127.0.0.1:5000/api/admin/appointments';
      
        if (this.filterStatus) {
          url += `?status=${this.filterStatus}`;
        }
        
        const response = await axios.get(url, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.appointments = response.data;
      } catch (err) {
        this.error = 'Failed to fetch appointments.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    getStatusClass(status) {
      if (status === 'Completed') return 'bg-success';
      if (status === 'Cancelled') return 'bg-danger';
      if (status === 'Booked') return 'bg-primary';
      return 'bg-secondary';
    }
  }
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <div class="card shadow-sm">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h2 class="mb-0">All Hospital Appointments</h2>
          <router-link to="/admin" class="btn btn-sm btn-secondary">← Back</router-link>
          
          <div class="col-md-3">
            <select class="form-select" v-model="filterStatus" @change="fetchAppointments">
              <option value="">All Statuses</option>
              <option value="Booked">Booked</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          
          <div v-if="!loading && !error" class="table-responsive">
            <table class="table table-striped table-hover align-middle">
              <thead class="table-dark">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Patient</th>
                  <th scope="col">Doctor</th>
                  <th scope="col">Department</th>
                  <th scope="col">Date</th>
                  <th scope="col">Time</th>
                  <th scope="col" class="text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="appointments.length === 0">
                  <td colspan="7" class="text-center">No appointments match the criteria.</td>
                </tr>
                <tr v-for="appt in appointments" :key="appt.id">
                  <th scope="row">{{ appt.id }}</th>
                  <td>{{ appt.patient_name }}</td>
                  <td>{{ appt.doctor_name }}</td>
                  <td>{{ appt.department }}</td>
                  <td>{{ appt.date }}</td>
                  <td>{{ appt.time }}</td>
                  <td class="text-center">
                    <span class="badge" :class="getStatusClass(appt.status)">
                      {{ appt.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}
.badge {
  font-size: 0.9em;
}
</style>