<template>
  <q-page>
    <Breadcrumbs :elements="breadcrumbsElements" />
    <div>
      <q-tabs v-model="tab" class="text-accent" align="justify">
        <q-tab name="pending" :icon="mdiClockAlert" label="Pending" />
        <q-tab name="completed" :icon="mdiCalendarCheck" label="Completed" />
        <q-tab name="allTasks" :icon="mdiListBox" label="All Tasks" />
      </q-tabs>
    </div>
    <div class="q-pa-sm">
      <div v-if="tasksPastDue.length">
        <p class="text-h5 text-negative">Tasks Past Due</p>
        <div class="row justify-center">
          <TaskCard
            v-for="task in tasksPastDue"
            :task="task"
            :completed="!!task.completedAt"
            :past-due="true"
            :key="task.id"
            @update="tasksStore.fetchTasks(userStore.appUser.userId)"
          />
        </div>
      </div>
      <div v-else>
        <p class="text-subtitle1 text-grey">No {{ tabTitle }} for this week.</p>
      </div>

      <div v-if="thisWeek.length">
        <p class="text-h5 q-pt-md">{{ tabTitle }} This Week</p>
        <div class="row justify-center">
          <TaskCard
            v-for="task in thisWeek"
            :task="task"
            :completed="!!task.completedAt"
            :key="task.id"
            @update="tasksStore.fetchTasks(userStore.appUser.userId)"
          />
        </div>
      </div>
      <div v-else>
        <p class="text-subtitle1 text-grey">No {{ tabTitle }} for this week.</p>
      </div>

      <div v-if="thisMonth.length">
        <p class="text-h5 q-pt-md">{{ tabTitle }} This Month</p>
        <div class="row justify-center">
          <TaskCard
            v-for="task in thisMonth"
            :task="task"
            :completed="!!task.completedAt"
            :key="task.id"
            @update="tasksStore.fetchTasks(userStore.appUser.userId)"
          />
        </div>
      </div>
      <div v-else>
        <p class="text-subtitle1 text-grey">
          No {{ tabTitle }} for this month.
        </p>
      </div>

      <div v-if="remainingTasks.length">
        <p class="text-h5 q-pt-md">Remaining Tasks</p>
        <div class="row justify-center">
          <TaskCard
            v-for="task in remainingTasks"
            :task="task"
            :completed="!!task.completedAt"
            :key="task.id"
            @update="tasksStore.fetchTasks(userStore.appUser.userId)"
          />
        </div>
      </div>
    </div>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-fab
        color="accent"
        text-color="black"
        icon="keyboard_arrow_up"
        direction="up"
      >
        <q-fab-action
          color="amber"
          text-color="black"
          @click="showDialog = true"
          label="Create Chore"
          :icon="mdiPlus"
          label-position="left"
          external-label
        />
        <q-fab-action
          color="amber"
          text-color="black"
          label="Distribute Chore"
          @click="showDistributeDialog = true"
          :icon="mdiCallSplit"
          label-position="left"
          external-label
        />
      </q-fab>
    </q-page-sticky>

    <CreateChoreDialog
      :card="showDialog"
      :user-id="props.userId"
      @close="showDialog = false"
    />
    <DistributeChoreDialog
      :card="showDistributeDialog"
      :user-id="props.userId"
      @close="fetchTasks"
    />
  </q-page>
</template>
<script setup lang="ts">
import {
  mdiFileDocument,
  mdiHome,
  mdiPlus,
  mdiCallSplit,
  mdiClockAlert,
  mdiCalendarCheck,
  mdiListBox,
} from '@quasar/extras/mdi-v7';
import { userUserStore } from 'src/stores/userStore';
import { computed, onMounted, ref } from 'vue';
import Breadcrumbs from 'src/components/BreadCrumbs.vue';
import { taskStore } from 'src/stores/taskStore';
import CreateChoreDialog from 'src/components/CreateChoreDialog.vue';
import DistributeChoreDialog from 'src/components/DistributeChoreDialog.vue';
import TaskCard from 'src/components/TaskCard.vue';
import { endOfWeek } from 'src/utils';

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

const userStore = userUserStore();
const tasksStore = taskStore();
const showDialog = ref(false);
const showDistributeDialog = ref(false);
const tab = ref('pending');

const breadcrumbsElements = computed(() => [
  {
    label: 'Home',
    icon: mdiHome,
    to: '/',
  },
  {
    label: `${userStore.appUser.firstName}'s Tasks`,
    icon: mdiFileDocument,
  },
]);

onMounted(async () => {
  await tasksStore.fetchTasks(props.userId);
});

const fetchTasks = async () => {
  showDistributeDialog.value = false;
  await tasksStore.fetchTasks(props.userId);
};

const pendingTasks = computed(() => {
  return tasksStore.tasks.filter((task) => !task.completedAt);
});
const completedTasks = computed(() => {
  return tasksStore.tasks.filter((task) => task.completedAt);
});

const tasks = computed(() => {
  if (tab.value === 'pending') {
    return pendingTasks.value;
  } else if (tab.value === 'completed') {
    return completedTasks.value;
  } else {
    return tasksStore.tasks;
  }
});

const tasksPastDue = computed(() => {
  const today = new Date();
  return tasks.value.filter((task) => new Date(task.dueDate) < today);
});

const thisWeek = computed(() => {
  const today = new Date();
  const weekEndDate = endOfWeek(today);
  const startOfWeek = new Date(today.getFullYear(), today.getMonth(), 0);
  return tasks.value.filter((task) => {
    return (
      new Date(task.dueDate) <= weekEndDate &&
      new Date(task.dueDate) >= startOfWeek &&
      !tasksPastDue.value.includes(task)
    );
  });
});

const thisMonth = computed(() => {
  const today = new Date();
  const monthEndDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  const monthStartDate = new Date(today.getFullYear(), today.getMonth(), 1);
  return tasks.value.filter((task) => {
    return (
      new Date(task.dueDate) >= monthStartDate &&
      new Date(task.dueDate) <= monthEndDate &&
      !thisWeek.value.includes(task) &&
      !tasksPastDue.value.includes(task)
    );
  });
});

const remainingTasks = computed(() => {
  return tasks.value.filter(
    (task) =>
      !thisWeek.value.includes(task) &&
      !thisMonth.value.includes(task) &&
      !tasksPastDue.value.includes(task)
  );
});

const tabTitle = computed(() => {
  switch (tab.value) {
    case 'pending':
      return 'Pending Tasks';
    case 'completed':
      return 'Completed Tasks';
    case 'allTasks':
      return 'Tasks';
    default:
      return '';
  }
});
</script>
