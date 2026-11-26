<template>
  <q-dialog
    :model-value="props.card"
    @hide="emit('close')"
    @before-show="beforeShow"
  >
    <q-card style="width: 100%; max-width: 420px">
      <div class="q-pa-md">
        <q-form class="q-gutter-md">
          <div class="text-h6">Edit House {{ props.house.name }}</div>
          <q-input
            filled
            v-model="name"
            label="House Name"
            @blur="houseStore.checkValidate(name)"
            :error-message="houseStore.getErrors('name')"
            :error="!!houseStore.getErrors('name')"
          />
          <q-list separator>
            <q-item v-for="user in members" :key="user.userId" class="q-my-xs">
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
              </q-item-section>

              <q-item-section side>
                <q-btn
                  flat
                  color="negative"
                  :icon="mdiAccountMinus"
                  @click="deleteMember()"
                />
              </q-item-section>
            </q-item>
          </q-list>
          <div class="row items-center">
            <q-btn label="Close" flat @click="emit('close')" />
            <q-space />
            <q-btn
              label="Delete"
              color="negative"
              flat
              @click="confirmDelete"
            />
            <q-btn
              label="Save"
              color="primary"
              class="q-ml-sm"
              @click="editHouse(name)"
              :disable="!!houseStore.getErrors('name')"
            />
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { House, userHouseStore } from 'src/stores/houseStore';
import { Ref, ref } from 'vue';
import { mdiAccountMinus } from '@quasar/extras/mdi-v7';
import { useQuasar } from 'quasar';
import { AppUser } from 'src/stores/userStore';

const props = defineProps({
  card: {
    type: Boolean,
    default: false,
  },
  house: {
    type: Object as () => House,
    required: true,
  },
  userId: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(['close', 'update']);
const houseStore = userHouseStore();
const $q = useQuasar();
const name: Ref<string> = ref(props.house.name);
const members: Ref<AppUser[]> = ref([]);

async function beforeShow() {
  members.value = await houseStore.getMembers(props.house.id);
}

async function editHouse(name: string) {
  await houseStore.editHouse(props.house.id, name).then(() => {
    emit('update');
    emit('close');
  });
}

function confirmDelete() {
  $q.dialog({
    title: 'Delete house',
    message: `Delete ${props.house.name}?`,
    cancel: true,
    persistent: true,
    ok: { label: 'Delete', color: 'negative' },
  }).onOk(() => {
    void deleteHouse();
  });
}

async function deleteHouse() {
  await houseStore.deleteHouse(props.house.id).then(() => {
    emit('update');
    emit('close');
  });
}

async function deleteMember() {
  await houseStore.deleteMember(props.house.id, props.userId);
  members.value = await houseStore.getMembers(props.house.id);
}
</script>
