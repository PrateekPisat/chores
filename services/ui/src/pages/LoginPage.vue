<template>
  <q-page>
    <div class="row desktop-only q-gutter-xl q-pa-xl">
      <div class="col-3 bg-blue-grey-2 text-center">
        <q-form>
          <div class="full-height">
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
                <q-btn
                  class="full-width"
                  label="Login"
                  @click="login()"
                  color="dark"
                />
              </q-card-section>
              <q-card-section class="text-subtitle1"
                >Not A Member?</q-card-section
              >
              <q-card-section>
                <q-btn class="full-width" label="Sign Up" color="secondary" />
              </q-card-section>
            </q-card>
          </div>
        </q-form>
      </div>
      <div class="col bg-green-2">
        <q-img
          src="src\assets\LoginBackgroung.png"
          :ratio="16 / 9"
          loading="lazy"
          spinner-color="white"
          fit="cover"
        >
          <div class="absolute-bottom text-h4">Get Chores Done</div>
        </q-img>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useUserStore } from 'src/stores/userSotre';
import { mdiEmail, mdiLock } from '@quasar/extras/mdi-v7';
import { Ref, ref } from 'vue';
import { useRouter } from 'vue-router';

const store = useUserStore();
const router = useRouter();

const email: Ref<string> = ref('');
const password: Ref<string> = ref('');

function login() {
  store.login(email.value, password.value);
  router.push({ name: 'home' });
}
</script>
