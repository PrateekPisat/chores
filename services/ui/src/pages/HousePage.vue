<template>
  <div>HOuse PAge {{ props.userId }}</div>
</template>
<script setup lang="ts">
const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});
</script>
