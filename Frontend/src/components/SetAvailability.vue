<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'SetAvailability',
  components: {
     Navbar
  },
  data() {
    return {
      doctorId: null,
      doctorName: '',
      isLoading: true,
      schedule: {
        Monday: { morning: false, evening: false },
        Tuesday: { morning: false, evening: false },
        Wednesday: { morning: false, evening: false },
        Thursday: { morning: false, evening: false },
        Friday: { morning: false, evening: false },
        Saturday: { morning: false, evening: false },
        Sunday: { morning: false, evening: false },
      },
      slotTimes: {
        morning: ["09:00", "10:00", "11:00", "12:00"],
        evening: ["16:00", "17:00", "18:00", "19:00"],
      },
    };
  },
  async created() {
    this.doctorId = this.$route.params.id;
    this.fetchDoctorAvailability();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async fetchDoctorAvailability() {
      this.isLoading = true;
      try {
        const token = localStorage.getItem('accessToken');
        const response = await axios.get('http://127.0.0.1:5000/api/admin/doctors', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const doctor = response.data.find(d => d.id == this.doctorId);
        if (doctor) {
          this.doctorName = doctor.name;
          if (doctor.availability) {
            const currentAvailability = JSON.parse(doctor.availability);
            for (const day in currentAvailability) {
              if(this.schedule[day]){
                if (currentAvailability[day].includes("09:00")) this.schedule[day].morning = true;
                if (currentAvailability[day].includes("16:00")) this.schedule[day].evening = true;
              }
            }
          }
        }
      } catch (e) {
        alert("Failed to load doctor's data.");
      } finally {
        this.isLoading = false;
      }
    },
    toggleSlot(day, period) {
      this.schedule[day][period] = !this.schedule[day][period];
    },
    async saveAvailability() {
      const availabilityJson = {};
      for (const day in this.schedule) {
        let slots = [];
        if (this.schedule[day].morning) slots.push(...this.slotTimes.morning);
        if (this.schedule[day].evening) slots.push(...this.slotTimes.evening);
        if (slots.length > 0) {
          availabilityJson[day] = slots;
        }
      }
      
      try {
        const token = localStorage.getItem('accessToken');
        await axios.put(`http://127.0.0.1:5000/api/admin/doctors/${this.doctorId}`, 
          { availability: JSON.stringify(availabilityJson) },
          { headers: { 'Authorization': `Bearer ${token}` } }
        );
        alert("Availability saved successfully!");
        this.$router.push('/admin/manage-doctors');
      } catch (e) {
        alert("Failed to save availability.");
      }
    }
  }
};
</script>

<template>
  <div>
    <Navbar />
    <main class="container mt-4">
       <div v-if="isLoading" class="text-center"><div class="spinner-border"></div></div>
       <div v-else class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow-sm">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h4 class="mb-0">Set Availability for {{ doctorName }}</h4>
              <button @click="goBack" class="btn btn-sm btn-secondary">← Back</button>
            </div>
            <div class="card-body">
              <div v-for="(periods, day) in schedule" :key="day" class="row border-bottom py-2 align-items-center">
                <div class="col-3 fw-bold">{{ day }}</div>
                <div class="col-9 d-flex">
                  <button class="btn me-2 flex-fill" :class="periods.morning ? 'btn-success' : 'btn-outline-secondary'" @click="toggleSlot(day, 'morning')">
                    Morning (9am - 1pm)
                  </button>
                  <button class="btn flex-fill" :class="periods.evening ? 'btn-success' : 'btn-outline-secondary'" @click="toggleSlot(day, 'evening')">
                    Evening (4pm - 8pm)
                  </button>
                </div>
              </div>
            </div>
            <div class="card-footer text-end">
              <button class="btn btn-primary" @click="saveAvailability">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>