<template>
  <div v-if="tasks.length" class="q-mt-lg">
    <div class="text-h6 q-mb-sm" :class="pastDue ? 'text-negative' : ''">
      {{ title }}
    </div>
    <div class="row q-col-gutter-md">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        :completed="!!task.completedAt"
        :past-due="pastDue && !task.completedAt"
        :demo-mode="demoMode"
        @refresh="emit('refresh')"
        @update="(id, completed, dueDate) => emit('update', id, completed, dueDate)"
        @delete="(id) => emit('delete', id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import TaskCard from 'src/components/TaskCard.vue';
import { Task } from 'src/stores/taskStore';
import { PropType } from 'vue';

defineProps({
  title: {
    type: String,
    required: true,
  },
  tasks: {
    type: Array as PropType<Task[]>,
    required: true,
  },
  pastDue: {
    type: Boolean,
    default: false,
  },
  demoMode: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['refresh', 'update', 'delete']);
</script>
