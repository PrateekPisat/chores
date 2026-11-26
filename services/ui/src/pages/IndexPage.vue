<template>
  <q-page class="q-pa-md">
    <div class="page-wrap">
      <div class="text-h4">Hello {{ userStore.appUser.firstName }}</div>
      <p class="text-subtitle1 text-primary q-mb-lg">
        Let's get your tasks organized!
      </p>

      <div v-if="tasksStore.loading" class="row q-col-gutter-md">
        <div v-for="n in 3" :key="n" class="col-12 col-sm-4">
          <q-skeleton height="88px" />
        </div>
      </div>

      <template v-else>
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
          <TaskGroup title="Past due" :tasks="groups.pastDue" past-due @refresh="reload" />
          <TaskGroup title="This week" :tasks="groups.thisWeek" @refresh="reload" />
          <TaskGroup title="This month" :tasks="groups.thisMonth" @refresh="reload" />
          <TaskGroup title="Later" :tasks="groups.later" @refresh="reload" />
        </template>
        <div v-else class="column items-center q-pa-xl text-center">
          <q-icon :name="mdiBroom" size="48px" color="primary" />
          <div class="text-h6 q-mt-sm">Nothing due</div>
          <q-btn
            class="q-mt-md"
            color="primary"
            label="Tasks"
            :to="{ name: 'tasks', params: { userId: userStore.appUser.userId } }"
            :disable="!userStore.appUser.userId"
          />
        </div>
      </template>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { userUserStore } from 'src/stores/userStore';
import { taskStore } from 'src/stores/taskStore';
import TaskGroup from 'src/components/TaskGroup.vue';
import { groupByDue } from 'src/utils';
import { useAuth0 } from '@auth0/auth0-vue';
import { mdiBroom } from '@quasar/extras/mdi-v7';

const auth0 = useAuth0();
const userStore = userUserStore();
const tasksStore = taskStore();

onMounted(async () => {
  await userStore.syncUser(auth0.user.value);
  await reload();
});

async function reload() {
  if (!userStore.appUser.userId) {
    return;
  }
  await tasksStore.fetchTasks(userStore.appUser.userId);
}

const pendingTasks = computed(() => tasksStore.tasks.filter((task) => !task.completedAt));
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
</script>
