<template>
  <q-drawer
    v-model="open"
    show-if-above
    bordered
    :breakpoint="1024"
    aria-label="Main"
  >
    <q-list padding>
      <q-item
        v-for="link in links"
        :key="link.label"
        clickable
        :to="link.to"
        :exact="link.exact"
        :disable="link.disable"
        active-class="bg-secondary text-primary"
      >
        <q-item-section avatar>
          <q-icon :name="link.icon" />
        </q-item-section>
        <q-item-section>{{ link.label }}</q-item-section>
      </q-item>
    </q-list>
  </q-drawer>
</template>

<script setup lang="ts">
import { RouteLocationRaw } from 'vue-router';

export interface DrawerLink {
  label: string;
  icon: string;
  to: RouteLocationRaw;
  exact?: boolean;
  disable?: boolean;
}

defineProps<{
  links: DrawerLink[];
}>();

const open = defineModel<boolean>({ required: true });
</script>
