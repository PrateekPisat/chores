<template>
  <q-form class="full-height" ref="formComponent">
    <q-card flat square>
      <q-card-section class="text-h3">Sign Up!</q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-input
          filled
          v-model="store.registerPayload.firstName"
          @blur="store.validateRegisterPayload()"
          label="First Name"
          type="text"
          :error="!!store.getErrors('firstName')"
          :error-message="store.getErrors('firstName')"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiAccount" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.registerPayload.lastName"
          @blur="store.validateRegisterPayload()"
          label="Last Name"
          type="text"
          :error="!!store.getErrors('lastName')"
          :error-message="store.getErrors('lastName')"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiAccount" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.registerPayload.email"
          @blur="store.validateRegisterPayload()"
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
          v-model="store.registerPayload.password"
          @blur="store.validateRegisterPayload()"
          label="Password"
          type="password"
          :error="!!store.getErrors('password')"
          :error-message="store.getErrors('password')"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiLock" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.registerPayload.confirmPassword"
          @blur="store.validateRegisterPayload()"
          label="Confirm Password"
          type="password"
          :error="!!store.getErrors('confirmPassword')"
          :error-message="store.getErrors('confirmPassword')"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiLock" />
          </template>
        </q-input>
        <q-btn
          class="full-width"
          label="Register"
          color="dark"
          :disable="!canRegister"
          @click="register()"
        >
          <template v-slot:loading>
            <q-spinner-pie color="secondary" />
          </template>
        </q-btn>
      </q-card-section>
      <q-card-section class="text-subtitle2">Already a Member?</q-card-section>
      <q-card-section>
        <q-btn
          class="full-width"
          label="Log In"
          color="secondary"
          @click="emit('login')"
        />
      </q-card-section>
    </q-card>
  </q-form>
</template>

<script setup lang="ts">
import { userRegisterStore } from 'src/stores/registerStore';
import { mdiAccount, mdiEmail, mdiLock } from '@quasar/extras/mdi-v7';
import { QForm } from 'quasar';
import { computed, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { VueCookies } from 'vue-cookies';

const emit = defineEmits(['login']);

const store = userRegisterStore();
const router = useRouter();
const cookies = inject<VueCookies>('$cookies');

const canRegister = computed(() => {
  return !!!store.errors && !store.loading;
});

onMounted(() => {
  store.reset();
});
function register() {
  store.register().then((response) => {
    if (response && cookies) {
      cookies?.set('user', response, '1d');
      router.push({ name: 'home' });
    }
  });
}
</script>
