<template>
  <q-page padding>
    <div>
      <p class="text-h3">Hello {{ userStore.appUser.firstName }} 👋</p>
      <p class="text-subtitle1 text-weight-light q-pl-sm text-primary">
        Let's get your tasks organized!
      </p>
    </div>

    <div v-if="tasksPastDue.length">
      <p class="text-h5 text-negative">Tasks Past Due</p>
      <div class="row justify-center">
        <TaskCard
          v-for="task in tasksPastDue"
          :task="task"
          :completed="!!task.completedAt"
          :past-due="true"
          :key="task.id"
          @refresh="tasksStore.fetchTasks(userStore.appUser.userId)"
        />
      </div>
    </div>
    <div v-else>
      <p class="text-subtitle1 text-grey">No pending tasks for this week.</p>
    </div>

    <div v-if="pendingTasks.length">
      <p class="text-h5">Pending Tasks This Week</p>
      <div class="row justify-center">
        <TaskCard
          v-for="task in pendingTasksThisWeek"
          :task="task"
          :completed="!!task.completedAt"
          :key="task.id"
          @refresh="tasksStore.fetchTasks(userStore.appUser.userId)"
        />
      </div>
    </div>
    <div v-else>
      <p class="text-subtitle1 text-grey">No pending tasks for this week.</p>
    </div>

    <div v-if="pendingTasksThisMonth.length">
      <p class="text-h5 q-pt-md">Pending Tasks This Month</p>
      <div class="row justify-center">
        <TaskCard
          v-for="task in pendingTasksThisMonth"
          :task="task"
          :completed="!!task.completedAt"
          :key="task.id"
          @refresh="tasksStore.fetchTasks(userStore.appUser.userId)"
        />
      </div>
    </div>
    <div v-else>
      <p class="text-subtitle1 text-grey">No pending tasks for this month.</p>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
import { taskStore } from 'src/stores/taskStore';
import TaskCard from 'src/components/TaskCard.vue';
import { endOfWeek } from 'src/utils';
import { useAuth0 } from '@auth0/auth0-vue';
const auth0 = useAuth0();
const userStore = userUserStore();
const tasksStore = taskStore();

onMounted(async () => {
  await userStore.syncUser(auth0.user.value);
  await tasksStore.fetchTasks(userStore.appUser.userId);
});

const pendingTasks = computed(() => {
  return tasksStore.tasks.filter((task) => !task.completedAt);
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
  const monthStartDate = new Date(today.getFullYear(), today.getMonth(), 1);
  return pendingTasks.value.filter((task) => {
    return (
      new Date(task.dueDate) <= monthEndDate &&
      new Date(task.dueDate) >= monthStartDate &&
      !pendingTasksThisWeek.value.includes(task) &&
      !tasksPastDue.value.includes(task)
    );
  });
});
</script>
