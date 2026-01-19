<template>
  <q-page padding class="demo-page">
    <!-- Demo Banner -->
    <q-banner class="bg-blue-2 text-primary q-mb-lg" rounded>
      <template v-slot:avatar>
        <q-icon name="info" color="primary" />
      </template>
      <div class="text-h6">Demo Mode</div>
      <div class="text-body2">
        You're viewing a demo version with sample data. No authentication
        required!
        <strong>All changes are temporary</strong> and won't be saved.
      </div>
      <template v-slot:action>
        <q-btn
          flat
          color="primary"
          label="Create an Account & Get Started"
          @click="$router.push('/')"
        />
      </template>
    </q-banner>

    <!-- Main Content -->
    <div>
      <p class="text-h3">Hello {{ demoUser.firstName }} 👋</p>
      <p class="text-subtitle1 text-weight-light q-pl-sm text-primary">
        Let's get your tasks organized!
      </p>
    </div>

    <!-- Tasks Past Due -->
    <div v-if="tasksPastDue.length" class="q-mt-lg">
      <p class="text-h5 text-negative">Tasks Past Due</p>
      <div class="row justify-center">
        <TaskCard
          v-for="task in tasksPastDue"
          :task="task"
          :completed="!!task.completedAt"
          :past-due="true"
          :key="task.id"
          @refresh="refreshTasks"
          :demo-mode="true"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
      </div>
    </div>
    <div v-else class="q-mt-lg">
      <p class="text-h5">Tasks Past Due</p>
      <p class="text-subtitle1 text-grey">No tasks past due. Great job!</p>
    </div>

    <!-- Pending Tasks This Week -->
    <div v-if="pendingTasksThisWeek.length" class="q-mt-lg">
      <p class="text-h5">Pending Tasks This Week</p>
      <div class="row justify-center">
        <TaskCard
          v-for="task in pendingTasksThisWeek"
          :task="task"
          :completed="!!task.completedAt"
          :key="task.id"
          @refresh="refreshTasks"
          :demo-mode="true"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
      </div>
    </div>
    <div v-else-if="!tasksPastDue.length" class="q-mt-lg">
      <p class="text-h5">Pending Tasks This Week</p>
      <p class="text-subtitle1 text-grey">No pending tasks for this week.</p>
    </div>

    <!-- Pending Tasks This Month -->
    <div v-if="pendingTasksThisMonth.length" class="q-mt-lg">
      <p class="text-h5 q-pt-md">Pending Tasks This Month</p>
      <div class="row justify-center">
        <TaskCard
          v-for="task in pendingTasksThisMonth"
          :task="task"
          :completed="!!task.completedAt"
          :key="task.id"
          @refresh="refreshTasks"
          :demo-mode="true"
          @update="handleTaskUpdate"
          @delete="handleTaskDelete"
        />
      </div>
    </div>
    <div
      v-else-if="!tasksPastDue.length && !pendingTasksThisWeek.length"
      class="q-mt-lg"
    >
      <p class="text-h5">Pending Tasks This Month</p>
      <p class="text-subtitle1 text-grey">No pending tasks for this month.</p>
    </div>

    <!-- Call to Action -->
    <div class="q-mt-xl q-mb-lg text-center">
      <q-card class="bg-grey-2 q-pa-lg" flat bordered>
        <p class="text-h5 q-mb-md">Like what you see?</p>
        <p class="text-body1 q-mb-lg">
          Sign up to create your own houses, manage chores, and track tasks with
          your family!
        </p>
        <q-btn
          color="primary"
          size="lg"
          label="Get Started"
          @click="$router.push('/')"
        />
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useDemoData } from 'src/composables/useDemoData';
import TaskCard from 'src/components/TaskCard.vue';
import { endOfWeek } from 'src/utils';

const { demoUser, demoTasks, updateDemoTask, deleteDemoTask } = useDemoData();

const pendingTasks = computed(() => {
  return demoTasks.value.filter((task) => !task.completedAt);
});

const tasksPastDue = computed(() => {
  const today = new Date();
  return pendingTasks.value.filter((task) => new Date(task.dueDate) < today);
});

const pendingTasksThisWeek = computed(() => {
  const today = new Date();
  const weekEndDate = endOfWeek(today);
  const startOfWeek = new Date(today.getFullYear(), today.getMonth(), 0);
  return pendingTasks.value.filter((task) => {
    return (
      new Date(task.dueDate) <= weekEndDate &&
      new Date(task.dueDate) >= startOfWeek &&
      !tasksPastDue.value.includes(task)
    );
  });
});

const pendingTasksThisMonth = computed(() => {
  const today = new Date();
  const monthEndDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  const weekEndDate = endOfWeek(today);
  return pendingTasks.value.filter((task) => {
    return (
      new Date(task.dueDate) <= monthEndDate &&
      new Date(task.dueDate) > weekEndDate &&
      !tasksPastDue.value.includes(task)
    );
  });
});

const handleTaskUpdate = (
  taskId: string,
  completed: boolean,
  dueDate: string
) => {
  updateDemoTask(taskId, completed, dueDate);
};

const handleTaskDelete = (taskId: string) => {
  deleteDemoTask(taskId);
};

const refreshTasks = () => {
  // In demo mode, tasks are already updated in-place
  // This is just for compatibility with the TaskCard component
};
</script>

<style scoped>
.demo-page {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
