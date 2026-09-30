<script></script>

<template>
  <div class="d-flex vh-100 text-center text-bg-dark">
    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
      <header class="mb-auto">
        <div>
          <h3 class="float-md-start mb-0">Hospital Management System</h3>
        </div>
      </header>

      <main class="px-3">
        <h1>Your Health, Our Priority.</h1>
        <p class="lead">
          Efficiently manage appointments, view your medical history, and connect with your doctors.
        </p>
        <p class="lead">
          <router-link to="/login" class="btn btn-lg btn-light fw-bold border-white bg-white me-1">Login</router-link>
          <router-link to="/register" class="btn btn-lg btn-light fw-bold border-white">Register</router-link>
        </p>
      </main>

      <footer class="mt-auto text-white-50">
        <p>&copy; 2025 HMS</p>
      </footer>
    </div>
  </div>
</template>


<style scoped>
.cover-container{
    max-width : 42em;
}
</style>