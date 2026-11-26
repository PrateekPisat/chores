<template>
  <div class="col-12 col-sm-6">
    <q-card flat bordered>
      <q-card-section>
        <div class="row items-start no-wrap">
          <div>
            <div class="text-h6">{{ props.task.chore.name }}</div>
            <div class="text-caption text-grey">
              {{ props.task.chore.description }}
            </div>
          </div>
          <q-space />
          <q-btn
            flat
            round
            color="negative"
            :icon="mdiTrashCan"
            aria-label="Delete task"
            @click="confirmDelete"
          />
        </div>
        <q-badge
          class="q-mt-sm"
          :color="props.pastDue ? 'negative' : 'primary'"
          :outline="props.pastDue"
          :label="fluentFormatDatetime(task.dueDate)"
        />
      </q-card-section>
      <q-separator />
      <q-card-actions>
        <q-checkbox
          :model-value="completed"
          :color="completed ? 'positive' : 'primary'"
          @update:model-value="(value: boolean) => updateTask(value, props.task.dueDate)"
        >
          <span :class="completed ? 'text-positive' : ''">
            {{ completed ? 'Completed' : 'Mark as completed' }}
          </span>
        </q-checkbox>
      </q-card-actions>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import { mdiTrashCan } from '@quasar/extras/mdi-v7';
import { useQuasar } from 'quasar';
import { Task, taskStore } from 'src/stores/taskStore';
import { PropType } from 'vue';
import { fluentFormatDatetime } from 'src/utils';

const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true,
  },
  completed: {
    type: Boolean,
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
const tasksStore = taskStore();
const emit = defineEmits(['refresh', 'update', 'delete']);
const $q = useQuasar();

function confirmDelete() {
  $q.dialog({
    title: 'Delete task',
    message: `Delete ${props.task.chore.name}?`,
    cancel: true,
    persistent: true,
    ok: { label: 'Delete', color: 'negative' },
  }).onOk(() => {
    void deleteTask();
  });
}

async function deleteTask() {
  if (props.demoMode) {
    emit('delete', props.task.id);
    emit('refresh');
  } else {
    await tasksStore.deleteTask(props.task.id);
    emit('refresh');
  }
}

async function updateTask(completed: boolean, dueDate: string) {
  if (props.demoMode) {
    emit('update', props.task.id, completed, dueDate);
    emit('refresh');
  } else {
    await tasksStore.updateTask(props.task.id, completed, dueDate);
    emit('refresh');
  }
}
</script>
