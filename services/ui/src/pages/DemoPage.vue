<template>
  <q-page class="q-pa-md">
    <div class="page-wrap">
      <q-banner class="bg-secondary text-primary q-mb-lg" rounded>
        <template v-slot:avatar>
          <q-icon name="info" color="primary" />
        </template>
        <div class="text-h6">Demo mode</div>
        <div class="text-body2">
          You're viewing sample data. No account is required.
          <strong>Changes stay in this browser tab.</strong>
        </div>
        <template v-slot:action>
          <q-btn flat color="primary" label="Create an account" @click="$router.push('/')" />
        </template>
      </q-banner>

      <div class="text-h4">Hello {{ demoUser.firstName }}</div>
      <p class="text-subtitle1 text-primary q-mb-lg">Let's get your tasks organized!</p>

      <div class="row q-col-gutter-md">
        <div v-for="stat in stats" :key="stat.label" class="col-12 col-sm-4">
          <q-card flat bordered>
            <q-card-section>
              <div class="text-caption text-grey">{{ stat.label }}</div>
              <div class="text-h5" :class="stat.class">{{ stat.count }}</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <template v-if="hasTasks">
        <TaskGroup
          title="Past due"
          :tasks="groups.pastDue"
          past-due
          demo-mode
          @refresh="refreshTasks"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
        <TaskGroup
          title="This week"
          :tasks="groups.thisWeek"
          demo-mode
          @refresh="refreshTasks"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
        <TaskGroup
          title="This month"
          :tasks="groups.thisMonth"
          demo-mode
          @refresh="refreshTasks"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
        <TaskGroup
          title="Later"
          :tasks="groups.later"
          demo-mode
          @refresh="refreshTasks"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
      </template>
      <div v-else class="column items-center q-pa-xl text-center">
        <q-icon :name="mdiBroom" size="48px" color="primary" />
        <div class="text-h6 q-mt-sm">Nothing due</div>
      </div>

      <q-card flat bordered class="q-mt-xl q-pa-lg text-center">
        <p class="text-h5 q-mb-md">Like what you see?</p>
        <p class="text-body1 q-mb-lg">
          Sign up to create your own houses, manage chores, and track tasks with your household.
        </p>
        <q-btn color="primary" label="Get started" @click="$router.push('/')" />
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useDemoData } from 'src/composables/useDemoData';
import TaskGroup from 'src/components/TaskGroup.vue';
import { groupByDue } from 'src/utils';
import { mdiBroom } from '@quasar/extras/mdi-v7';

const { demoUser, demoTasks, updateDemoTask, deleteDemoTask } = useDemoData();

const pendingTasks = computed(() => demoTasks.value.filter((task) => !task.completedAt));
const groups = computed(() => groupByDue(pendingTasks.value));
const hasTasks = computed(
  () =>
    groups.value.pastDue.length +
      groups.value.thisWeek.length +
      groups.value.thisMonth.length +
      groups.value.later.length >
    0
);
const stats = computed(() => [
  { label: 'Past due', count: groups.value.pastDue.length, class: 'text-negative' },
  { label: 'Due this week', count: groups.value.thisWeek.length, class: '' },
  { label: 'Due this month', count: groups.value.thisMonth.length, class: '' },
]);

const handleTaskUpdate = (taskId: string, completed: boolean, dueDate: string) => {
  updateDemoTask(taskId, completed, dueDate);
};

const handleTaskDelete = (taskId: string) => {
  deleteDemoTask(taskId);
};

const refreshTasks = () => {
  // Demo tasks update in place.
};
</script>
