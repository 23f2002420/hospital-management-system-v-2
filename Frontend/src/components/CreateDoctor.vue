<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'CreateDoctor',
  components: {
    Navbar
  },
  data() {
    return {
      doctor: {
        username: '',
        password: '',
        name: '',
        specialization: '',
        department_id: null
      },
      departments: [],
      error: null,
    };
  },
  async created() {
    this.fetchDepartments();
  },
  methods: {
    async fetchDepartments() {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await axios.get('http://127.0.0.1:5000/api/departments', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.departments = response.data
      } catch (err) {
        this.error = 'Failed to fetch departments. Please create a department first.';
        console.error(err);
      }
    },
    async handleCreateDoctor() {
      this.error = null;
      if (!this.doctor.department_id) {
        this.error = "Please select a department.";
        return;
      }
      try {
        const token = localStorage.getItem('accessToken');
        await axios.post('http://127.0.0.1:5000/api/admin/doctors', this.doctor, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.$router.push('/admin/manage-doctors');
      } catch (err) {
        this.error = err.response?.data?.message || 'An unexpected error occurred.';
        console.error(err);
      }
    }
  }
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow-sm">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h2 class="mb-0">Add New Doctor</h2>
              <router-link to="/admin/manage-doctors" class="btn btn-sm btn-secondary">← Back</router-link>
            </div>
            <div class="card-body">
              <div v-if="error" class="alert alert-danger">{{ error }}</div>
              
              <form @submit.prevent="handleCreateDoctor">
                <div class="mb-3">
                  <label for="name" class="form-label">Full Name</label>
                  <input type="text" class="form-control" id="name" v-model="doctor.name" required>
                </div>
                
                <div class="mb-3">
                  <label for="specialization" class="form-label">Specialization</label>
                  <input type="text" class="form-control" id="specialization" v-model="doctor.specialization" required>
                </div>

                <div class="mb-3">
                  <label for="department" class="form-label">Department</label>
                  <select class="form-select" id="department" v-model="doctor.department_id" required>
                    <option :value="null" disabled>Select a department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                </div>
                
                <hr>
                <h5 class="text-muted">Login Credentials</h5>

                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" class="form-control" id="username" v-model="doctor.username" required>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model="doctor.password" required>
                </div>
                
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-primary">Create Doctor</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>