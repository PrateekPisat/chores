<template>
  <q-form class="full-height" ref="formComponent">
    <q-card flat square>
      <q-card-section class="text-h3">Sign Up!</q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-input
          filled
          v-model="store.registerPayload.firstName"
          @update:model-value="store.validateRegisterPayload()"
          label="First Name"
          type="text"
          clearable
        >
          <template v-slot:prepend>
            <q-icon :name="mdiAccount" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.registerPayload.lastName"
          @update:model-value="store.validateRegisterPayload()"
          label="Last Name"
          type="text"
          clearable
        >
          <template v-slot:prepend>
            <q-icon :name="mdiAccount" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.registerPayload.email"
          @update:model-value="store.validateRegisterPayload()"
          label="Email"
          type="email"
          clearable
        >
          <template v-slot:prepend>
            <q-icon :name="mdiEmail" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="store.registerPayload.password"
          @update:model-value="store.validateRegisterPayload()"
          label="Password"
          type="password"
          clearable
        >
          <template v-slot:prepend>
            <q-icon :name="mdiLock" />
          </template>
        </q-input>
        <q-input
          filled
          v-model=""
          @update:model-value="store.validateRegisterPayload()"
          label="Confirm Password"
          type="password"
          clearable
        >
          <template v-slot:prepend>
            <q-icon :name="mdiLock" />
          </template>
        </q-input>
        <q-btn
          class="full-width"
          label="Register"
          color="dark"
          :disable="store.hasRegisterErrors"
          @click="store.register()"
        />
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
import { useUserStore } from 'src/stores/userStore';
import { mdiAccount, mdiEmail, mdiLock } from '@quasar/extras/mdi-v7';
import { QForm } from 'quasar';

const emit = defineEmits(['login']);

const store = useUserStore();
</script>
