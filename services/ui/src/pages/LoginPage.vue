<template>
  <q-page>
    <div class="row desktop-only q-gutter-x-xl q-pa-xl">
      <div class="col-3 text-center">
        <RegisterComponent @login="newUser = false" v-if="newUser" />
        <LoginComponent @register="newUser = true" v-else />
      </div>
      <div class="col">
        <q-img
          src="src\assets\LoginBackgroung.png"
          loading="lazy"
          spinner-color="white"
          fit="cover"
        >
        </q-img>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import LoginComponent from 'src/components/LoginComponent.vue';
import RegisterComponent from 'src/components/RegisterComponent.vue';
import { ref } from 'vue';

const newUser = ref(false);
</script>
