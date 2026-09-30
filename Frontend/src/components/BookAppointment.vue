<script>
import axios from 'axios';
import PatientNavbar from './PatientNavbar.vue'

export default {
  name: 'BookAppointment',
  components: {
    PatientNavbar
  },
  data() {
    return {
      doctor: null,
      schedule: [],
      isLoading: true,
      error:null
    }
  },
  async created(){
    const doctorId = this.$route.params.doctorId
    this.generateSchedule(doctorId)
  },
  methods: {
    async generateSchedule(doctorId) {
      this.isLoading = true,
      this.error = null
      try {
        const token = localStorage.getItem('accessToken');
        const headers= { 'Authorization': `Bearer ${token}` }
        const [doctorRes, appointmentRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/doctors',{headers}),
          axios.get(`http://127.0.0.1:5000/api/doctors/${doctorId}/schedule`, {headers})
        ])
        this.doctor = doctorRes.data.find(d => d.id == doctorId)
        if (!this.doctor || !this.doctor.availability){
            throw new Error('Doctor not found or availability not set.')
        } 

        const weeklyAvailability = JSON.parse(this.doctor.availability || '{}')
        const bookedSlots = appointmentRes.data.map(appt => `${appt.date}T ${appt.time}`)

        let tempSchedule = []
        const weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

        for (let i=0; i<7; i++){
          const day = new Date()
          day.setDate(day.getDate() +i)
          const dayName = weekdays[day.getDay()]
          const formattedDate = day.toISOString().split('T')[0]

          let daySlots = []
          if (weeklyAvailability[dayName]){
            daySlots = weeklyAvailability[dayName].map(time => {
              const slotIdentifier = `${formattedDate}T${time}:00`
              return {
                time: time,
                date: formattedDate,
                isBooked: bookedSlots.includes(slotIdentifier)
              }
            })
          }
          tempSchedule.push({
            date: formattedDate,
            dayName: dayName,
            slots: daySlots
          })
        }
        this.schedule = tempSchedule
      } catch (error) {
        this.error = "Failed to load doctors schedule.They may not have set their availability.";
      } finally {
        this.isLoading = false;
      }
    },
    async bookSlot(slot){
      if (slot.isBooked) return

      const confirmation = confirm(`Confirm appointment with Dr.${this.doctor.name}`)
      if (confirmation){
        try{
          const token = localStorage.getItem('accessToken')
          await axios.post('http://127.0.0.1:5000/api/appointments',{
            doctor_id: this.doctor.id,
            date : slot.date,
            time: slot.time
          },{
            headers: {'Authorization': `Bearer ${token}`}
          })
          alert('Appointment booked successfully!')
          this.$router.push('/patient')
        }catch(error){
          alert(error.response?.data?.message || 'Failed to book appointment.')
          console.error(error)
        }
      }
    }
  }
}
</script>

<template>
  <div>
    <PatientNavbar/>
    <main class="container mt-4">
      <div v-if="isLoading" class="text-center mt-5"><div class="spinner-border" role="status"></div></div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="!isLoading && doctor">
        <header class="p-3 mb-4 bg-light border rounded-3">
            <h1 class="display-6">Book Appointment with Dr. {{ doctor.name }}</h1>
            <p class="text-muted">{{ doctor.specialization }}</p>
            <router-link to="/patient" class="btn btn-sm btn-secondary">← Back to Dashboard</router-link>
        </header>

        <div class="row">
            <div v-for="day in schedule" :key="day.date" class="col-md-4 col-lg-3 mb-3">
                <div class="card h-100">
                    <div class="card-header text-center">
                        <strong>{{ day.dayName }}</strong><br>
                        <small>{{ day.date }}</small>
                    </div>
                    <div class="card-body">
                        <div v-if="day.slots.length === 0" class="text-center text-muted">No slots available</div>
                        <div v-else class="d-grid gap-2">
                            <button v-for="slot in day.slots" :key="slot.time" 
                                class="btn"
                                :class="slot.isBooked ? 'btn-danger disabled' : 'btn-outline-success'"
                                @click="bookSlot(slot)">
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