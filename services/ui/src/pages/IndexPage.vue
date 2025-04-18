<template>
  <q-page padding>
    <div>
      <p class="text-h3">Hello {{ userStore.appUser.firstName }} 👋</p>
      <p class="text-subtitle1 text-weight-light q-pl-sm text-primary">
        Let's get your tasks organized!
      </p>
    </div>
    <pre> {{ userStore.auth0User }} </pre>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
const userStore = userUserStore();

onMounted(() => {
  userStore.syncUser();
});
</script>
