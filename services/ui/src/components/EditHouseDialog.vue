<template>
  <q-dialog
    :model-value="props.card"
    @hide="emit('close')"
    @before-show="beforeShow"
  >
    <q-card class="my-card">
      <div class="q-pa-md" style="max-width: 400px">
        <q-form class="q-gutter-xs">
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
          <div class="q-mt-sm">
            <q-btn-group spread outline>
              <q-btn
                label="Save"
                type="submit"
                color="primary"
                flat
                @click="editHouse(name)"
                :disable="!!houseStore.getErrors('name')"
              />
              <q-btn
                :icon="mdiTrashCan"
                color="negative"
                flat
                @click="deleteHouse()"
              />
            </q-btn-group>
          </div>
        </q-form>
      </div>
    </q-card>
  </q-dialog>
</template>
<script setup lang="ts">
import { House, userHouseStore } from 'src/stores/houseStore';
import { Ref, ref } from 'vue';
import { mdiAccountMinus, mdiTrashCan } from '@quasar/extras/mdi-v7';
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
