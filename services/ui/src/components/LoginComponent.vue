<template>
  <q-form class="full-height">
    <q-card flat square>
      <q-card-section class="text-h3">Welcome Back!</q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-input
          filled
          v-model="store.loginPayload.email"
          @blur="store.validateLoginPayload()"
          label="Email"
          type="email"
          :error="!!store.getErrors('email')"
          :error-message="store.getErrors('email')"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiEmail" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.loginPayload.password"
          @blur="store.validateLoginPayload()"
          label="Password"
          type="password"
          :error="!!store.getErrors('password')"
          :error-message="store.getErrors('password')"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiLock" />
          </template>
        </q-input>
        <q-btn
          class="full-width"
          label="Login"
          color="dark"
          :disable="!canRegister"
          @click="login()"
        >
          <template v-slot:loading>
            <q-spinner-pie color="secondary" />
          </template>
        </q-btn>
      </q-card-section>
      <q-card-section class="text-subtitle1">Not A Member?</q-card-section>
      <q-card-section>
        <q-btn
          class="full-width"
          label="Sign Up"
          color="secondary"
          @click="emit('register')"
        >
        </q-btn>
      </q-card-section>
    </q-card>
  </q-form>
</template>

<script setup lang="ts">
import { userLoginStore, LoginResponse } from 'src/stores/loginStore';
import { mdiEmail, mdiLock } from '@quasar/extras/mdi-v7';
import { QForm } from 'quasar';
import { computed, inject } from 'vue';
import { useRouter } from 'vue-router';
import { VueCookies } from 'vue-cookies';
import { z } from 'zod';

const emit = defineEmits(['register']);

const store = userLoginStore();
const canRegister = computed(() => {
  return !!!store.errors && !store.loading;
});
const router = useRouter();
const cookies = inject<VueCookies>('$cookies');

function login() {
  store.login().then((response: z.infer<typeof LoginResponse>) => {
    if (response && cookies) {
      cookies?.set('user', response, '1d');
      router.push({ name: 'home' });
    }
  });
}
</script>
