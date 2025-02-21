<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">Personal Info</div>
      <div class="text-caption text-grey ellipsis">
        You can change your personal information here
      </div>
      <div class="q-mt-md">
        <q-form
          @submit="userStore.updateUser(firstName, lastName)"
          @reset="reset()"
          class="q-gutter-xs"
        >
          <q-input
            filled
            bottom-slots
            v-model="firstName"
            label="First Name"
            @blur="userStore.updateUser(firstName, lastName)"
            :error-message="userStore.getErrors('first_name')"
            :error="!!userStore.getErrors('first_name')"
          >
            <template v-slot:prepend>
              <q-icon :name="mdiAlphaABox" />
            </template>
          </q-input>

          <q-input
            filled
            bottom-slots
            v-model="lastName"
            label="Last Name"
            @blur="userStore.updateUser(firstName, lastName)"
            :error-message="userStore.getErrors('lastName')"
            :error="!!userStore.getErrors('lastName')"
          >
            <template v-slot:prepend>
              <q-icon :name="mdiAlphaBBox" />
            </template>
          </q-input>

          <div class="q-gutter-sm">
            <q-btn
              type="submit"
              color="primary"
              :icon="mdiCheck"
              label="Save"
              rounded
            />
            <q-btn
              type="reset"
              color="dark"
              :icon="mdiCancel"
              label="Cancel"
              rounded
            />
          </div>
        </q-form>
      </div>
    </q-card-section>
  </q-card>
</template>
<script setup lang="ts">
import {
  mdiAlphaABox,
  mdiAlphaBBox,
  mdiCancel,
  mdiCheck,
} from '@quasar/extras/mdi-v7';
import { userUserStore } from 'src/stores/userStore';
import { ref } from 'vue';

const userStore = userUserStore();
const firstName = ref(userStore.appUser.firstName);
const lastName = ref(userStore.appUser.lastName);

function reset() {
  firstName.value = userStore.appUser.firstName;
  lastName.value = userStore.appUser.lastName;
  userStore.reset();
}
</script>
