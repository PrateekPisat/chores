<template>
  <q-dialog
    :model-value="props.card"
    @hide="emit('close')"
    @before-show="beforeShow"
  >
    <q-card>
      <div class="q-pa-md" style="max-width: 400px">
        <q-form class="q-m-xs">
          <div class="text-h6 q-mb-sm">
            Add Members to House {{ props.house.name }}
          </div>
          <q-input
            v-model="email"
            filled
            placeholder="Search"
            @keypress.enter.stop="searchUser"
            :error-message="userStore.getErrors('email')"
            :error="!!userStore.getErrors('email')"
          >
            <template v-slot:append>
              <q-icon :name="mdiAccountSearch" @click="searchUser" />
            </template>
          </q-input>
        </q-form>
        <q-list separator padding>
          <q-item v-for="user in users" :key="user.userId" class="q-my-xs">
            <q-item-section avatar>
              <q-avatar>
                <img :src="user.picture || ''" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label
                >{{ user.firstName }} {{ user.lastName }}</q-item-label
              >
              <q-item-label caption lines="1">{{ user.email }}</q-item-label>
              <q-item-label
                v-if="isExitingMember(user.email)"
                caption
                lines="2"
                class="text-warning"
              >
                User is already a member
              </q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-btn
                flat
                color="black"
                :icon="mdiPlus"
                :disabled="isExitingMember(user.email)"
                @click="addMembers(house, user)"
              />
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { House, userHouseStore } from 'src/stores/houseStore';
import { computed, Ref, ref } from 'vue';
import { mdiAccountSearch, mdiPlus } from '@quasar/extras/mdi-v7';
import { AppUser, userUserStore } from 'src/stores/userStore';

const props = defineProps({
  card: {
    type: Boolean,
    default: false,
  },
  house: {
    type: Object as () => House,
    required: true,
  },
});
const emit = defineEmits(['close', 'update']);
const userStore = userUserStore();
const houseStore = userHouseStore();
const email: Ref<string> = ref('');
const users: Ref<AppUser[]> = ref([]);
const existingMembers: Ref<AppUser[]> = ref([]);

async function beforeShow() {
  existingMembers.value = await houseStore.getMembers(props.house.id);
}

async function searchUser() {
  users.value = await userStore.searchUser(email.value, null);
}

async function addMembers(house: House, user: AppUser) {
  await houseStore.addMembers(house.id, [user.userId]);
  await searchUser();
  existingMembers.value = await houseStore.getMembers(props.house.id);
}

const existingMemberEmails = computed(() => {
  return existingMembers.value.map((member: AppUser) => member.email);
});

function isExitingMember(email: string): boolean {
  return existingMemberEmails.value.includes(email);
}
</script>
