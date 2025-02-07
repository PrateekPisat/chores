<template>
  <div class="q-pa-md">
    <q-layout class="shadow-2 rounded-borders">
      <q-header elevated>
        <q-toolbar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>

          <q-toolbar-title> Quasar Framework </q-toolbar-title>

          <q-btn flat round dense icon="whatshot" />
        </q-toolbar>
      </q-header>

      <q-page-container>
        <q-page padding>
          <p v-for="n in 15" :key="n">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil
            praesentium molestias a adipisci, dolore vitae odit, quidem
            consequatur optio voluptates asperiores pariatur eos numquam rerum
            delectus commodi perferendis voluptate?
          </p>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>
<script setup lang="ts">
import { onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
const userStore = userUserStore();

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

onMounted(() => {
  userStore.getUser(props.userId);
});
</script>
