<template>
  <div class="content-layout">
    <h3 id="page-title" class="content__title">
      Hello {{ userStore.appUser.firstName }} 👋
    </h3>
    <div class="content__body">
      <pre>
          {{ userStore.auth0User }}
        </pre
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
const userStore = userUserStore();

onMounted(() => {
  userStore.syncUser();
});
</script>
