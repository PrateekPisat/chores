<template>
  <q-form class="full-height" :ref="formComponent">
    <q-card flat square>
      <q-card-section class="text-h3">Welcome Back!</q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-input
          filled
          v-model="email"
          label="Email"
          type="email"
          clearable
          :rules="[(val) => !!val || 'Field is required']"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiEmail" />
          </template>
        </q-input>
        <q-input
          filled
          v-model="password"
          label="Password"
          type="password"
          clearable
          :rules="[(val) => !!val || 'Field is required']"
        >
          <template v-slot:prepend>
            <q-icon :name="mdiLock" />
          </template>
        </q-input>
        <q-btn class="full-width" label="Login" color="dark" />
      </q-card-section>
      <q-card-section class="text-subtitle1">Not A Member?</q-card-section>
      <q-card-section>
        <q-btn
          class="full-width"
          label="Sign Up"
          color="secondary"
          @click="emit('register')"
        />
      </q-card-section>
    </q-card>
  </q-form>
</template>

<script setup lang="ts">
import { mdiEmail, mdiLock } from '@quasar/extras/mdi-v7';
import { Ref, ref } from 'vue';
import { QForm } from 'quasar';

const emit = defineEmits(['register']);

const email: Ref<string> = ref('');
const password: Ref<string> = ref('');
const formComponent: Ref<QForm | undefined> = ref();
</script>
