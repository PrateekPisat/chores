<template>
  <div class="q-pa-md" style="max-width: 400px">
    <q-form @submit="userStore.updateUser()" class="q-gutter-md">
      <q-input
        filled
        bottom-slots
        v-model="userStore.appUser.first_name"
        label="First Name"
        error-message="you fucked up"
        :error="true"
      >
        <template v-slot:prepend>
          <q-icon :name="mdiAlphaABox" />
        </template>
        <template v-slot:hint>
          <p>you fucked up</p>
        </template>
      </q-input>

      <q-input
        filled
        bottom-slots
        v-model="userStore.appUser.last_name"
        label="Last Name"
      >
        <template v-slot:prepend>
          <q-icon :name="mdiAlphaBBox" />
        </template>
        <template v-slot:hint> Your first name </template>
      </q-input>

      <div>
        <q-btn type="submit" color="primary" :icon="mdiCheck" label="Submit" />
      </div>
    </q-form>
  </div>
</template>
<script setup lang="ts">
import { mdiAlphaABox, mdiAlphaBBox, mdiCheck } from '@quasar/extras/mdi-v7';
import { userUserStore } from 'src/stores/userStore';

const userStore = userUserStore();
</script>
