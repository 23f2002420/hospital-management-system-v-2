<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'ManageDoctors',
  components: {
    Navbar
  },
  data() {
    return {
      doctors: [],
      departments: [],
      isLoading: true,
      error: null,
      editingDoctorId: null,
      editingDoctorData: {},
      searchQuery: ''
    };
  },
  methods: {
    async fetchAllData() {
      this.isLoading = true;
      this.error = null;
      this.cancelEdit();
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { 'Authorization': `Bearer ${token}` };
        
        let doctorsPromise;
        if (this.searchQuery.trim()) {
          doctorsPromise = axios.get(`http://127.0.0.1:5000/api/admin/search?role=doctor&query=${this.searchQuery}`, { headers });
        } else {
          doctorsPromise = axios.get('http://127.0.0.1:5000/api/admin/doctors', { headers });
        }

        const departmentsPromise = axios.get('http://127.0.0.1:5000/api/departments', { headers });
        
        const [doctorsRes, departmentsRes] = await Promise.all([doctorsPromise, departmentsPromise]);

        this.doctors = doctorsRes.data;
        this.departments = departmentsRes.data;
      } catch (error) {
        this.error = "Failed to load data.";
        console.error(error);
      } finally {
        this.isLoading = false
      }
    },
    editDoctor(doctor) {
      this.editingDoctorId = doctor.id;
      this.editingDoctorData = { ...doctor };
    },
    cancelEdit() {
      this.editingDoctorId = null;
      this.editingDoctorData = {};
    },
    async saveDoctor(doctorId) {
      try {
        const token = localStorage.getItem('accessToken');
        await axios.put(`http://127.0.0.1:5000/api/admin/doctors/${doctorId}`, this.editingDoctorData, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.fetchAllData();
      } catch (err) {
        alert(err.response?.data?.message || "Failed to update doctor.");
      }
    },
    async deleteDoctor(doctorId) {
      if (confirm("Are you sure you want to delete this doctor?")) {
        try {
          const token = localStorage.getItem('accessToken');
          await axios.delete(`http://127.0.0.1:5000/api/admin/doctors/${doctorId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          this.fetchAllData();
        } catch (error) {
          alert("Failed to delete doctor.");
        }
      }
    }
  },
  created() {
    this.fetchAllData();
  },
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
      <div class="card shadow-sm">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h2 class="mb-0">Manage Doctors</h2>
          <div>
            <router-link to="/admin/manage-departments" class="btn btn-secondary me-2">Manage Departments</router-link>
            <router-link to="/admin/create-doctor" class="btn btn-primary">+ Add New Doctor</router-link>
          </div>
        </div>
        <div class="card-body">
          <form @submit.prevent="fetchAllData" class="mb-4">
            <div class="input-group">
              <input type="text" v-model="searchQuery" class="form-control" placeholder="Search by name or specialization...">
              <button class="btn btn-primary" type="submit">Search</button>
            </div>
          </form>

          <div v-if="isLoading" class="text-center">
            <div class="spinner-border" role="status"></div>
          </div>
          <div v-if="error" class="alert alert-danger">{{ error }}</div>

          <div v-if="!isLoading && !error" class="table-responsive">
            <table class="table table-striped table-hover align-middle">
              <thead class="table-dark">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Specialization</th>
                  <th scope="col">Department</th>
                  <th scope="col" class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="doctors.length === 0">
                  <td colspan="5" class="text-center">No doctors found.</td>
                </tr>
                <tr v-for="doc in doctors" :key="doc.id">
                  <th scope="row">{{ doc.id }}</th>
                  <td>
                    <span v-if="editingDoctorId !== doc.id">{{ doc.name }}</span>
                    <input v-else type="text" class="form-control form-control-sm" v-model="editingDoctorData.name">
                  </td>
                  <td>
                    <span v-if="editingDoctorId !== doc.id">{{ doc.specialization }}</span>
                    <input v-else type="text" class="form-control form-control-sm" v-model="editingDoctorData.specialization">
                  </td>
                  <td>
                    <span v-if="editingDoctorId !== doc.id">{{ doc.department || 'N/A' }}</span>
                    <select v-else class="form-select form-select-sm" v-model="editingDoctorData.department_id">
                      <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                    </select>
                  </td>
                  <td class="text-center">
                    <div v-if="editingDoctorId === doc.id">
                      <button class="btn btn-sm btn-success me-2" @click="saveDoctor(doc.id)">Save</button>
                      <button class="btn btn-sm btn-secondary" @click="cancelEdit">Cancel</button>
                    </div>
                    <div v-else>
                      <button class="btn btn-sm btn-secondary me-2" @click="editDoctor(doc)">Edit Details</button>
                      <router-link :to="{ name: 'SetAvailability', params: { id: doc.id } }" class="btn btn-sm btn-info me-2">
                        Set Schedule
                      </router-link>
                      <button class="btn btn-sm btn-danger" @click="deleteDoctor(doc.id)">Delete</button>
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