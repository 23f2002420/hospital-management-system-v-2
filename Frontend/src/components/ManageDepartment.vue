<script>
import axios from 'axios'
import Navbar from './Navbar.vue'

export default{
    name: 'ManageDepartments',
    components: {
        Navbar
    },
    data(){
        return {
            departments:[],
            newDepartment:{
                name: '',
                description: ''
            },
            isLoading: true,
            error: null
        }
    },
    async created(){
        this.fetchDepartments()
    },
    methods: {
        async fetchDepartments(){
            this.isLoading = true
            try{
            const token = localStorage.getItem('accessToken')
            const response = await axios.get('http://127.0.0.1:5000/api/departments',{
                headers: {'Authorization': `Bearer ${token}`}
            })
            this.departments = response.data
            }catch(error){
                this.error = "Failed to load departments."
            }finally{
                this.isLoading = false
            }    
        },
        async createDepartment(){
            try{
                const token = localStorage.getItem('accessToken')
                await axios.post('http://127.0.0.1:5000/api/admin/departments', this.newDepartment,{
                    headers: {'Authorization': `Bearer ${token}`}
                })
                this.newDepartment.name = '',
                this.newDepartment.description = '',
                this.fetchDepartments();
            }catch(error){
                alert(error.response?.data?.message || "Failed to create department.")
            }
        }
    }
}
</script>

<template>
    <div>
        <Navbar/>
        <main class = "container mt-4">
            <h1 class = "mb-4">Manage Departments</h1>
            <div class= "row">
                <div class = "col-md-5">
                    <div class = "card shadow-sm">
                        <div class= "card-header">
                            <h4>Add New Department</h4>
                            <router-link to="/admin/manage-doctors" class="btn btn-sm btn-secondary">← Back</router-link>
                        </div>
                        <div class= "card-body">
                            <form @submit.prevent = "createDepartment">
                                <div class = "mb-3">
                                    <label for = "dept-desc" class = "form-label">Department Name</label>
                                    <input type = "text" id = "dept-name" class = "form-control" v-model = "newDepartment.name" required>
                                </div>

                                <div class="mb-3">
                                    <label for="dept-desc" class="form-label">Description</label>
                                    <textarea id="dept-desc" class="form-control" rows="3" v-model="newDepartment.description"></textarea>
                                </div>

                                <button type = "submit" class = "btn btn-primary w-100">Add Department</button>
                            </form>
                        </div>
                    </div>
                </div>
                <div class = "col-md-7">
                    <div class = "card-shadow-sm">
                        <div class = "card-header">
                            <h4>Existing Departments</h4>
                        </div>

                        <div class = "card-body">
                            <div v-if="isLoading" class="text-center"><div class="spinner-border"></div></div>
                            <div v-if="error" class="alert alert-danger">{{ error }}</div>
                            <ul v-if="!isLoading && !error" class="list-group">
                                <li v-if="departments.length === 0" class="list-group-item">No departments found.</li>
                                <li v-for="dept in departments" :key="dept.id" class="list-group-item">
                                <strong>{{ dept.name }}</strong>
                                <p class="mb-0 text-muted">{{ dept.description }}</p>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<style>

</style>