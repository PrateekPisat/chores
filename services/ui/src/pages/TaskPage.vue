<template>
  <q-page class="q-pa-md">
    <div class="page-wrap">
      <div class="text-h5 q-mb-md">Tasks</div>
      <q-tabs
        v-model="tab"
        align="left"
        active-color="primary"
        indicator-color="primary"
        narrow-indicator
      >
        <q-tab name="pending" label="Pending">
          <q-badge v-if="pendingTasks.length" color="negative" floating>
            {{ pendingTasks.length }}
          </q-badge>
        </q-tab>
        <q-tab name="completed" label="Completed">
          <q-badge v-if="completedTasks.length" color="primary" floating>
            {{ completedTasks.length }}
          </q-badge>
        </q-tab>
        <q-tab name="allTasks" label="All">
          <q-badge v-if="tasksStore.tasks.length" color="primary" floating>
            {{ tasksStore.tasks.length }}
          </q-badge>
        </q-tab>
      </q-tabs>

      <div v-if="tasksStore.loading" class="row q-col-gutter-md q-mt-md">
        <div v-for="n in 3" :key="n" class="col-12 col-sm-6">
          <q-skeleton height="140px" />
        </div>
      </div>

      <q-tab-panels v-else v-model="tab">
        <q-tab-panel name="pending" class="q-pa-none">
          <TaskGroup title="Past due" :tasks="pendingGroups.pastDue" past-due @refresh="fetchTasks" />
          <TaskGroup title="This week" :tasks="pendingGroups.thisWeek" @refresh="fetchTasks" />
          <TaskGroup title="This month" :tasks="pendingGroups.thisMonth" @refresh="fetchTasks" />
          <TaskGroup title="Later" :tasks="pendingGroups.later" @refresh="fetchTasks" />
          <div v-if="!pendingTasks.length" class="column items-center q-pa-xl text-center">
            <q-icon :name="mdiBroom" size="48px" color="primary" />
            <div class="text-h6 q-mt-sm">Nothing due</div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="completed" class="q-pa-none">
          <TaskGroup title="Earlier" :tasks="completedGroups.pastDue" @refresh="fetchTasks" />
          <TaskGroup title="This week" :tasks="completedGroups.thisWeek" @refresh="fetchTasks" />
          <TaskGroup title="This month" :tasks="completedGroups.thisMonth" @refresh="fetchTasks" />
          <TaskGroup title="Later" :tasks="completedGroups.later" @refresh="fetchTasks" />
          <div v-if="!completedTasks.length" class="text-subtitle1 text-grey q-pa-lg">
            No completed tasks.
          </div>
        </q-tab-panel>
        <q-tab-panel name="allTasks" class="q-pa-none">
          <TaskGroup title="Earlier" :tasks="allGroups.pastDue" past-due @refresh="fetchTasks" />
          <TaskGroup title="This week" :tasks="allGroups.thisWeek" @refresh="fetchTasks" />
          <TaskGroup title="This month" :tasks="allGroups.thisMonth" @refresh="fetchTasks" />
          <TaskGroup title="Later" :tasks="allGroups.later" @refresh="fetchTasks" />
          <div v-if="!tasksStore.tasks.length" class="column items-center q-pa-xl text-center">
            <q-icon :name="mdiBroom" size="48px" color="primary" />
            <div class="text-h6 q-mt-sm">Nothing due</div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-fab color="accent" icon="add" direction="up" aria-label="Chore actions">
        <q-fab-action
          color="accent"
          label="Create chore"
          :icon="mdiPlus"
          label-position="left"
          external-label
          @click="showDialog = true"
        />
        <q-fab-action
          color="accent"
          label="Distribute chore"
          :icon="mdiCallSplit"
          label-position="left"
          external-label
          @click="showDistributeDialog = true"
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
import { mdiBroom, mdiCallSplit, mdiPlus } from '@quasar/extras/mdi-v7';
import { computed, onMounted, ref } from 'vue';
import { taskStore } from 'src/stores/taskStore';
import CreateChoreDialog from 'src/components/CreateChoreDialog.vue';
import DistributeChoreDialog from 'src/components/DistributeChoreDialog.vue';
import TaskGroup from 'src/components/TaskGroup.vue';
import { groupByDue } from 'src/utils';

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

const tasksStore = taskStore();
const showDialog = ref(false);
const showDistributeDialog = ref(false);
const tab = ref('pending');

onMounted(async () => {
  await tasksStore.fetchTasks(props.userId);
});

const fetchTasks = async () => {
  showDistributeDialog.value = false;
  await tasksStore.fetchTasks(props.userId);
};

const pendingTasks = computed(() => tasksStore.tasks.filter((task) => !task.completedAt));
const completedTasks = computed(() => tasksStore.tasks.filter((task) => task.completedAt));
const pendingGroups = computed(() => groupByDue(pendingTasks.value));
const completedGroups = computed(() => groupByDue(completedTasks.value));
const allGroups = computed(() => groupByDue(tasksStore.tasks));
</script>
