<script>
import axios from 'axios';

export default {
  name: 'PatientNavbar',
  data() {
    return {
      patientName: 'Patient' 
    }
  },
  async created() {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await axios.get('http://127.0.0.1:5000/api/patient/profile', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      this.patientName = response.data.name;
    } catch (error) {
      console.error("Could not fetch patient name for navbar.");
    }
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole')
      this.$router.push('/login');
    }
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container-fluid">
      <router-link class="navbar-brand fw-bold" to="/patient">
        Welcome {{ patientName }}
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/patient">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/patient/history">My History</router-link>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <button class="btn btn-outline-light" @click="handleLogout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>