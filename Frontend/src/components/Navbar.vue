<script>
export default {
  name: 'Navbar',
  data(){
    return {
      userRole: null,
      username: ''
    }
  },
  created(){
    this.userRole = localStorage.getItem('userRole')
    if (this.userRole === 'doctor'){
      this.fetchDoctorName
    }
  },
  methods: {
    async fetchDoctorName() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await axios.get('http://127.0.0.1:5000/api/doctor/profile', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.username = response.data.name;
      } catch (error) {
        console.error("Could not fetch doctor's name for navbar.");
        this.userName = 'Doctor'
      }
    },
    handleLogout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole');
      this.$router.push('/login');
    }
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container-fluid">
      <router-link class="navbar-brand fw-bold" to="/">Hospital Management</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        
        <ul v-if="userRole === 'admin'" class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/admin">Dashboard</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/manage-doctors">Manage Doctors</router-link></li>
          </ul>
        
        <ul v-if="userRole === 'doctor'" class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/doctor">Dashboard</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/doctor/availability">My Availability</router-link></li>
        </ul>

        <div class="navbar-nav ms-auto d-flex align-items-center">
          <span v-if="userRole === 'doctor' && username" class="navbar-text me-3">
            Welcome, Dr. {{ username }}
          </span>

          <button class="btn btn-outline-light" @click="handleLogout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>