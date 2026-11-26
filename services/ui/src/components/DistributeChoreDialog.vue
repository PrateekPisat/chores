<template>
  <q-dialog
    :model-value="props.card"
    @before-show="beforeShow"
    @hide="$emit('close')"
  >
    <q-card style="width: 100%; max-width: 420px">
      <div class="q-pa-md">
        <q-form class="q-gutter-md">
          <div class="text-h6 q-mb-sm">Distribute a chore</div>
          <q-select
            filled
            v-model="choreId"
            :options="userChores"
            option-value="id"
            option-label="name"
            label="Chore"
            map-options
            emit-value
            :error-message="tasksStore.getErrors('choreId')"
            :error="!!tasksStore.getErrors('choreId')"
            @update:model-value="listUsers"
            @blur="tasksStore.checkCreateDistribution(selectedUserIds, choreId)"
          />
          <q-select
            filled
            multiple
            v-model="selectedUserIds"
            :options="users"
            option-value="userId"
            label="Users"
            :option-label="getLabel"
            map-options
            emit-value
            :error-message="tasksStore.getErrors('userIds')"
            :error="!!tasksStore.getErrors('userIds')"
            @blur="tasksStore.checkCreateDistribution(selectedUserIds, choreId)"
            v-show="choreId"
          >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section avatar>
                  <q-icon :name="mdiAccount" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ getLabel(scope.opt) }}</q-item-label>
                  <q-item-label caption>{{ scope.opt.email }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>

          <div class="row items-center">
            <q-btn flat label="Close" @click="emit('close')" />
            <q-space />
            <q-btn
              color="primary"
              :label="buttonLabel"
              @click="createOrUpdateDistribution(selectedUserIds, choreId)"
              :loading="tasksStore.loading"
              :disable="tasksStore.loading"
            />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { mdiAccount } from '@quasar/extras/mdi-v7';
import { Chore, taskStore } from 'src/stores/taskStore';
import { AppUser, userUserStore } from 'src/stores/userStore';
import { computed, Ref, ref } from 'vue';

const props = defineProps({
  card: {
    type: Boolean,
    default: false,
  },
  userId: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(['close']);

const tasksStore = taskStore();
const userStore = userUserStore();

const choreId: Ref<string> = ref('');
let users: Ref<AppUser[]> = ref([]);
const selectedUserIds: Ref<string[]> = ref([]);
const hasDistribution = ref(false);

async function beforeShow() {
  await tasksStore.listChores(props.userId);
}

async function listUsers() {
  users.value = await userStore.searchUser(null, choreId.value);
  const distribution = await tasksStore.getDistribution(choreId.value);
  const assigned = Array.isArray(distribution)
    ? []
    : (distribution.users ?? []).map((user: AppUser) => user.userId);
  selectedUserIds.value = assigned;
  hasDistribution.value = assigned.length > 0;
}

async function createOrUpdateDistribution(userIds: string[], choreId: string) {
  if (hasDistribution.value)
    await tasksStore.updateDistribution(userIds, choreId);
  else await tasksStore.createDistribution(userIds, choreId);
  emit('close');
}

function getLabel(user: AppUser): string {
  return `${user.firstName} ${user.lastName}`;
}

const userChores = computed((): Chore[] => {
  return tasksStore.chores;
});

const buttonLabel = computed((): string => {
  return hasDistribution.value ? 'Update Distribution' : 'Create Distribution';
});
</script>
