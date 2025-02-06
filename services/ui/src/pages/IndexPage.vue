<template>
  <q-page class="row items-center justify-evenly">
    <div class="content-layout">
      <h1 id="page-title" class="content__title">Profile Page</h1>
      <div class="content__body">
        <p id="page-description">
          <span>
            You can use the <strong>ID Token</strong> to get the profile
            information of an authenticated user.
          </span>
          <span>
            <strong> Only authenticated users can access this page.</strong>
          </span>
        </p>
        <div class="profile-grid">
          <div class="profile__header">
            <img :src="user?.picture" alt="Profile" class="profile__avatar" />
            <div class="profile__headline">
              <h2 class="profile__title">{{ user?.name }}</h2>
              <span class="profile__description">{{ user?.email }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue';
import { computed } from 'vue';
const auth0 = useAuth0();

const user = computed(() => auth0.user.value);
</script>
