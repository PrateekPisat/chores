<template>
  <q-page class="row items-center justify-evenly">
    <div class="content-layout">
      <h1 id="page-title" class="content__title">Home PAge</h1>
      <div class="content__body">
        <pre>
          {{ userStore.auth0User }}
        </pre>
      </div>
    </div>
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
