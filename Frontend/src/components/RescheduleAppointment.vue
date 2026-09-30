<script>
import axios from 'axios';
import PatientNavbar from './PatientNavbar.vue';

export default {
  name: 'RescheduleAppointment',
  components: {
    PatientNavbar
  },
  data() {
    return {
      appointment: null,
      doctor: null,
      schedule: [],
      loading: true,
      error: null,
    };
  },
  async created() {
    const appointmentId = this.$route.params.appointmentId;
    this.fetchData(appointmentId);
  },
  methods: {
    async fetchData(appointmentId) {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('accessToken');
        const headers = { 'Authorization': `Bearer ${token}` };

        const apptRes = await axios.get(`http://127.0.0.1:5000/api/appointments/${appointmentId}`, { headers });
        this.appointment = apptRes.data;
        const doctorId = this.appointment.doctor_id;
        const [doctorRes, scheduleRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/doctors', { headers }),
          axios.get(`http://127.0.0.1:5000/api/doctors/${doctorId}/schedule`, { headers })
        ]);

        this.doctor = doctorRes.data.find(d => d.id == doctorId);
        if (!this.doctor || !this.doctor.availability) {
          throw new Error("Doctor not found or availability not set.");
        }

        const weeklyAvailability = JSON.parse(this.doctor.availability);
        const bookedSlots = scheduleRes.data.map(slot => `${slot.date}T${slot.time}`);
        
        let tempSchedule = [];
        const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        for (let i = 0; i < 7; i++) {
          const day = new Date();
          day.setDate(day.getDate() + i);
          const dayName = weekdays[day.getDay()];
          const formattedDate = day.toISOString().split('T')[0];
          let daySlots = [];
          if (weeklyAvailability[dayName]) {
            daySlots = weeklyAvailability[dayName].map(time => {
              const slotIdentifier = `${formattedDate}T${time.slice(0, 5)}:00`;
              return { time: time, date: formattedDate, isBooked: bookedSlots.includes(slotIdentifier) };
            });
          }
          tempSchedule.push({ date: formattedDate, dayName: dayName, slots: daySlots });
        }
        this.schedule = tempSchedule;

      } catch (err) {
        this.error = "Failed to load the reschedule page.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async pickNewSlot(slot) {
      if (slot.isBooked) return;
      
      const confirmation = confirm(`Reschedule appointment with Dr. ${this.doctor.name} to ${slot.date} at ${slot.time}?`);
      if (confirmation) {
        try {
          const token = localStorage.getItem('accessToken');
          await axios.put(`http://127.0.0.1:5000/api/appointments/${this.appointment.id}/reschedule`, {
            new_date: slot.date,
            new_time: slot.time
          }, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          alert('Appointment rescheduled successfully!');
          this.$router.push('/patient');
        } catch (error) {
          alert(error.response?.data?.message || 'Failed to reschedule appointment.');
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
      <div v-if="loading" class="text-center mt-5"><div class="spinner-border" role="status"></div></div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="!loading && doctor">
        <header class="p-3 mb-4 bg-light border rounded-3">
          <h1 class="display-6">Pick a New Time with Dr. {{ doctor.name }}</h1>
          <p v-if="appointment" class="text-muted">Current appointment is on {{ appointment.date }} at {{ appointment.time }}</p>
          <router-link to="/patient" class="btn btn-sm btn-secondary">← Back to Dashboard</router-link>
        </header>

        <div class="row">
          <div v-for="day in schedule" :key="day.date" class="col-12 col-md-6 col-lg-4 col-xl-3 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-header text-center fw-bold">{{ day.dayName }} <br><small class="fw-normal">{{ day.date }}</small></div>
              <div class="card-body">
                <div v-if="day.slots.length === 0" class="text-center text-muted d-flex align-items-center justify-content-center h-100"><span>No slots available</span></div>
                <div v-else class="d-grid gap-2">
                  <button v-for="slot in day.slots" :key="slot.time" 
                    class="btn"
                    :class="slot.isBooked ? 'btn-danger disabled' : 'btn-outline-success'"
                    @click="pickNewSlot(slot)">
                    {{ slot.time }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>