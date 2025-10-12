<template>
  <q-dialog
    :model-value="props.card"
    @before-show="beforeShow"
    @hide="$emit('close')"
  >
    <q-card>
      <div class="q-pa-md" style="min-width: 400px">
        <q-form class="q-m-sm">
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

          <q-btn
            class="full-width q-mt-md"
            color="primary"
            :label="buttonLabel"
            @click="createOrUpdateDistribution(selectedUserIds, choreId)"
            :loading="tasksStore.loading"
            :disable="tasksStore.loading"
          />
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

async function beforeShow() {
  await tasksStore.listChores(props.userId);
}

async function listUsers() {
  users.value = await userStore.searchUser(null, choreId.value);
  selectedUserIds.value = await tasksStore.getDistribution(choreId.value);
}

async function createOrUpdateDistribution(userIds: string[], choreId: string) {
  if (distributionExists.value)
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

const distributionExists = computed((): boolean => {
  return !!selectedUserIds.value;
});

const buttonLabel = computed((): string => {
  return distributionExists.value
    ? 'Update Distribution'
    : 'Create Distribution';
});
</script>
