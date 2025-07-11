<template>
  <Breadcrumbs :elements="breadcrumbsElements" />
  <div class="q-pa-sm">
    <q-toolbar>
      <q-toolbar-title>Your Tasks</q-toolbar-title>
    </q-toolbar>
    <div class="row q-gutter-md">
      <TaskCard
        :task="task"
        v-for="task in userTasks"
        :key="task.id"
        @update="fetchTasks"
      />
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
</template>
<script setup lang="ts">
import {
  mdiFileDocument,
  mdiHome,
  mdiPlus,
  mdiCallSplit,
} from '@quasar/extras/mdi-v7';
import { userUserStore } from 'src/stores/userStore';
import { computed, onMounted, ref } from 'vue';
import Breadcrumbs from 'src/components/BreadCrumbs.vue';
import { taskStore } from 'src/stores/taskStore';
import CreateChoreDialog from 'src/components/CreateChoreDialog.vue';
import DistributeChoreDialog from 'src/components/DistributeChoreDialog.vue';
import TaskCard from 'src/components/TaskCard.vue';

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

const userTasks = computed(() => {
  return tasksStore.tasks;
});

const fetchTasks = async () => {
  showDistributeDialog.value = false;
  await tasksStore.fetchTasks(props.userId);
};
</script>
