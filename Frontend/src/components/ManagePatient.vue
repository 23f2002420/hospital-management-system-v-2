<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'ManagePatient',
  components: {
    Navbar
  },
  data() {
    return {
      patients: [],
      loading: true,
      error: null,
      editingPatientId: null,
      editingPatientData: {},
      searchQuery: ''
    };
  },
  async created() {
    this.fetchPatients();
  },
  methods: {
    async fetchPatients() {
      this.loading = true;
      this.error = null
      this.cancelEdit()
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { 'Authorization': `Bearer ${token}` };
        let response;

        if (this.searchQuery.trim()) {
          response = await axios.get(`http://127.0.0.1:5000/api/admin/search?role=patient&query=${this.searchQuery}`, { headers });
        } else {
          response = await axios.get('http://127.0.0.1:5000/api/admin/patients', { headers });
        }
        this.patients = response.data;
      } catch (err) {
        this.error = 'Failed to fetch patients.';
        this.patients = [];
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    editPatient(patient){
      this.editingPatientId = patient.id 
      this.editingPatientData = {...patient}
    },
    cancelEdit(){
      this.editingPatientId = null,
      this.editingPatientData = {}
    },
    async savePatient(patientId) {
      try {
        const token = localStorage.getItem('accessToken');
        await axios.put(`http://127.0.0.1:5000/api/admin/patients/${patientId}`, this.editingPatientData, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.cancelEdit()
        this.fetchPatients()
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to update patient.');
      }
    },
    async deletePatient(patientId) {
      if (confirm('Are you sure you want to delete this patient? This action is permanent.')) {
        try {
          const token = localStorage.getItem('accessToken');
          await axios.delete(`http://127.0.0.1:5000/api/admin/patients/${patientId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          this.fetchPatients();
        } catch (err) {
          alert('Failed to delete patient.');
          console.error(err);
        }
      }
    }
  }
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <div class="card shadow-sm">
        <div class="card-header">
          <h2 class="mb-0">Manage Patients</h2>
          <router-link to="/admin" class="btn btn-sm btn-secondary">← Back</router-link>
        </div>
        <div class="card-body">
          <form @submit.prevent="fetchPatients" class="mb-4">
            <div class="input-group">
              <input type="text" v-model="searchQuery" class="form-control" placeholder="Search by patient name...">
              <button class="btn btn-primary" type="submit">Search</button>
            </div>
          </form>
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
                  <th scope="col">Patient ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Profile Notes</th>
                  <th scope="col" class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="patients.length === 0">
                  <td colspan="4" class="text-center">No patients found.</td>
                </tr>
                <tr v-for="pat in patients" :key="pat.id">
                  <th scope="row">{{ pat.id }}</th>
                  <td>
                    <span v-if="editingPatientId !== pat.id">{{ pat.name }}</span>
                    <input v-else type="text" class="form-control form-control-sm" v-model="editingPatientData.name">
                  </td>
                  <td>
                    <span v-if="editingPatientId !== pat.id">{{ pat.profile || 'N/A' }}</span>
                    <input v-else type="text" class="form-control form-control-sm" v-model="editingPatientData.profile">
                  </td>
                  <td class="text-center">
                    <div v-if="editingPatientId === pat.id">
                      <button class="btn btn-sm btn-success me-2" @click="savePatient(pat.id)">Save</button>
                      <button class="btn btn-sm btn-secondary" @click="cancelEdit">Cancel</button>
                    </div>
                    <div v-else>
                      <button class="btn btn-sm btn-secondary me-2" @click="editPatient(pat)">Edit</button>
                      <button class="btn btn-sm btn-danger" @click="deletePatient(pat.id)">Delete</button>
                    </div>
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
</style>