<script>
import axios from 'axios';
import Navbar from './Navbar.vue'

export default {
  name: 'AdminDashboard',
  components: {
    Navbar,
  },
  data() {
    return {
      stats: {
        total_doctors: 0,
        total_patients: 0,
        total_appointments: 0,
      },
      loading: true,
      error: null,
    };
  },
  async created() {
    this.fetchDashboardStats();
  },
  methods: {
    async fetchDashboardStats() {
      this.loading = true
      try {
        const token = localStorage.getItem('accessToken')
        const response = await axios.get('http://127.0.0.1:5000/api/admin/dashboard', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        this.stats = response.data;
      } catch (err) {
        this.error = 'Failed to load dashboard data.'
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <header class="p-3 mb-4 bg-light border rounded-3">
        <h1 class="display-5">Admin Dashboard</h1>
        <p class="text-muted">Welcome, Admin! Manage your hospital resources from here.</p>
      </header>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="!loading && !error">
        <section class="row mb-4">
          <div class="col-md-4 mb-3">
            <div class="card text-white bg-primary h-100">
              <div class="card-body">
                <h5 class="card-title">Total Doctors</h5>
                <p class="card-text display-4">{{ stats.total_doctors }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card text-white bg-info h-100">
              <div class="card-body">
                <h5 class="card-title">Total Patients</h5>
                <p class="card-text display-4">{{ stats.total_patients }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card text-dark bg-warning h-100">
              <div class="card-body">
                <h5 class="card-title">Total Appointments</h5>
                <p class="card-text display-4">{{ stats.total_appointments }}</p>
              </div>
            </div>
          </div>
        </section>

        <section class="row">
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">System Management</h5>
                <p class="card-text">Add, update, or remove doctors and patients from the system.</p>
                <div class="mt-auto">
                  <router-link to="/admin/manage-doctors" class="btn btn-primary me-2">Manage Doctors</router-link>
                  <router-link to="/admin/manage-patient" class="btn btn-secondary">Manage Patients</router-link>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">Appointments Overview</h5>
                <p class="card-text">View all scheduled, completed, and cancelled appointments across the hospital.</p>
                <div class="mt-auto">
                  <router-link to="/admin/all-appointments" class="btn btn-info">View All Appointments</router-link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>