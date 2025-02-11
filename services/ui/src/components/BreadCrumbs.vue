<template>
  <div class="q-pa-md q-gutter-sm">
    <q-breadcrumbs>
      <template v-slot:separator>
        <q-icon size="1.25em" :name="mdiChevronRight" color="primary" />
      </template>
      <q-breadcrumbs-el
        v-for="element in props.elements"
        :key="element.label"
        :icon="element.icon"
        :to="element.to"
        :label="element.label"
      />
    </q-breadcrumbs>
  </div>
</template>
<script setup lang="ts">
import { mdiChevronRight } from '@quasar/extras/mdi-v7';
import { BreadcrumbsElement } from './models';

const props = defineProps({
  elements: {
    type: Array<BreadcrumbsElement>,
    required: true,
  },
});
</script>
