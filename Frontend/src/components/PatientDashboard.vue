<script>
import axios from 'axios';
import PatientNavbar from './PatientNavbar.vue';

export default {
  name: 'PatientDashboard',
  components: {
    PatientNavbar
  },
  data() {
    return {
      upcomingAppointments: [],
      allDoctors: [],
      searchQuery: '',
      isLoading: true,
      error: null
    };
  },
  computed: {
    filteredDoctors() {
      if (!this.searchQuery) return this.allDoctors;
      const lowerCaseQuery = this.searchQuery.toLowerCase();
      return this.allDoctors.filter(doc => 
        doc.name.toLowerCase().includes(lowerCaseQuery) || 
        doc.specialization.toLowerCase().includes(lowerCaseQuery)
      );
    }
  },
  async created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.isLoading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { 'Authorization': `Bearer ${token}` };
        const [appointmentsRes, doctorsRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/patient/appointments', { headers }),
          axios.get('http://127.0.0.1:5000/api/doctors', { headers })
        ]);
      
        this.upcomingAppointments = appointmentsRes.data.filter(a => a.status === 'Booked');
        this.allDoctors = doctorsRes.data;

      } catch (error) {
        this.error = "Failed to load dashboard data.";
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },
    async cancelAppointment(appointmentId) {
      if (confirm('Are you sure you want to cancel this appointment?')) {
        try {
          const token = localStorage.getItem('accessToken')
          await axios.put(`http://127.0.0.1:5000/api/appointments/${appointmentId}/cancel`, {}, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          this.fetchData()
        } catch (error) {
          alert('Failed to cancel appointment.');
        }
      }
    }
  }
};
</script>

<template>
  <div>
    <PatientNavbar />
    <main class="container mt-4">
      <header class="p-3 mb-4 bg-light border rounded-3">
        <h1 class="display-5">Patient Dashboard</h1>
        <p class="text-muted">Book appointments and view your schedule.</p>
      </header>

      <div v-if="isLoading" class="text-center mt-5"><div class="spinner-border" role="status"></div></div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="!isLoading && !error" class="row">
        <div class="col-lg-6 mb-4">
          <div class="card h-100 shadow-sm">
            <div class="card-header">
              <h4>Upcoming Appointments</h4>
            </div>
            <div class="card-body">
              <div v-if = "upcomingAppointments.length ===0" class = "text-muted">
                You have no upcoming appointments.
              </div>
              <div v-else class = "table-responsive">
                <table class = "table table-hover align-middle">
                  <thead>
                    <tr>
                      <th>Sr.No</th>
                      <th>Doctor</th>
                      <th>Department</th>
                      <th>Date & Time</th>
                      <th class="text-center">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(appt, index) in upcomingAppointments" :key="appt.id">
                      <th>{{ index + 1 }}</th>
                      <td>Dr.{{ appt.doctor_name }}</td>
                      <td>{{ appt.department }}</td>
                      <td>{{ appt.date }} at {{ appt.time}}</td>
                      <td class="text-center">
                        <router-link :to="{ name: 'RescheduleAppointment', params: { appointmentId: appt.id } }" class="btn btn-sm btn-outline-primary me-2">
                          Reschedule
                        </router-link>
                        <button class="btn btn-sm btn-outline-danger" @click="cancelAppointment(appt.id)">
                          Cancel
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-6 mb-4">
          <div class="card h-100 shadow-sm">
            <div class="card-header"><h4>Find a Doctor</h4></div>
            <div class="card-body">
              <input type="text" class="form-control mb-3" placeholder="Search by name or specialization..." v-model="searchQuery">
              <div v-if="filteredDoctors.length === 0" class="text-muted">No doctors found.</div>
              <div v-else class="list-group" style="max-height: 300px; overflow-y: auto;">
                <div v-for="doc in filteredDoctors" :key="doc.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <strong>Dr. {{ doc.name }}</strong><br>
                    <small class="text-muted">{{ doc.specialization }}</small>
                  </div>
                  <div>
                    <router-link :to="{ name: 'DoctorDetails', params: { id: doc.id } }" class="btn btn-sm btn-outline-primary me-2">
                      View Details
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>