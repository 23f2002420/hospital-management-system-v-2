import { createWebHistory, createRouter } from "vue-router";

import LandingPage from './components/LandingPage.vue'
import LoginPage from "./components/LoginPage.vue"
import RegisterPage from './components/RegisterPage.vue'

import AdminDashboard from './components/AdminDashboard.vue'
import ManageDepartment from './components/ManageDepartment.vue'
import ManageDoctors from './components/ManageDoctors.vue'
import CreateDoctor from './components/CreateDoctor.vue'
import setAvailability from './components/SetAvailability.vue'
import ManagePatient from './components/ManagePatient.vue'
import ViewAllAppointments from './components/ViewAllAppointments.vue'

import DoctorDashboard from './components/DoctorDashboard.vue'
import DoctorAppointmentDetails from './components/DoctorAppointmentDetails.vue'
import PatientDashboard from './components/PatientDashboard.vue'
import BookAppointment from './components/BookAppointment.vue'
import PatientHistory from './components/PatientHistory.vue'
import DoctorAvailability from './components/DoctorAvailability.vue'
import RescheduleAppointment from './components/RescheduleAppointment.vue'
import DoctorDetails from './components/DoctorDetails.vue'

const routes = [
    {path: "/", component: LandingPage},
    {path : "/login", component: LoginPage},
    {path: "/register", component: RegisterPage},
    
    {path: "/admin", component: AdminDashboard},
    {path: "/admin/manage-departments", name: 'ManageDepartments', component: ManageDepartment},
    {path: "/admin/manage-doctors", name: 'ManageDoctors', component: ManageDoctors},
    {path: "/admin/create-doctor", name:'CreateDoctor', component: CreateDoctor},
    {path: "/admin/doctor/:id/availability", name: 'SetAvailability', component: setAvailability},
    {path: "/admin/manage-patient", name:"ManagePatient", component: ManagePatient},
    {path: "/admin/all-appointments",name: "ViewAllAppointments" , component: ViewAllAppointments},

    {path: "/doctor", component: DoctorDashboard},
    {path: "/doctor/appointment/:id", name :"DoctorAppointmentDetails", component: DoctorAppointmentDetails},
    {path: "/patient", component: PatientDashboard},
    {path : "/book-appointment/:doctorId",name:'BookAppointment', component: BookAppointment},
    {path: '/patient/history', name : 'PatientHistory', component: PatientHistory},
    
    { path: "/doctor/availability", name: "DoctorAvailability", component: DoctorAvailability },
    {path: '/reschedule-appointment/:appointmentId', name: 'RescheduleAppointment',component: RescheduleAppointment },
    {path: '/doctor-details/:id', name: 'DoctorDetails', component: DoctorDetails}
]
export const router = createRouter({
    history: createWebHistory(),
    routes: routes

})