<script setup lang="ts">
import { ref, reactive } from "vue";
import Divider from "primevue/divider";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "primevue/usetoast";
import router from "@/router/index";

//
const toast = useToast();
const authStore = useAuthStore();
// state
const oldPassword = ref("");
const newPassword = ref("");
const reTypeNewPassword = ref("");
const errMsg = reactive({
  oldPassword: "",
  newPassword: "",
  reTypeNewPassword: "",
});
// methods
const validate = () => {
  errMsg.oldPassword = "";
  errMsg.newPassword = "";
  errMsg.reTypeNewPassword = "";

  if (oldPassword.value === "") errMsg.oldPassword = "Old password is empty";
  if (newPassword.value === "") errMsg.newPassword = "New passowrd is empty";
  if (reTypeNewPassword.value === "")
    errMsg.reTypeNewPassword = "Re type new password is empty";
  else if (reTypeNewPassword.value !== newPassword.value)
    errMsg.reTypeNewPassword = "Re type new password does not match";

  return !(
    errMsg.oldPassword ||
    errMsg.newPassword ||
    errMsg.reTypeNewPassword
  );
};
const submit = async () => {
  if (validate()) {
    const old_password = oldPassword.value;
    const new_password = newPassword.value;
    try {
      const response = await authStore.changePassword({
        old_password,
        new_password,
      });
      if (response.data > 0) {
        router.go();
        toast.add({
          severity: "success",
          summary: "Success",
          detail: "Update password success",
          life: 1000,
        });
      }
    } catch (error) {
      errMsg.oldPassword = "Old password is not correct";
    }
  }
};
</script>
<style lang="scss" scoped>
.error-msg {
  color: var(--red-500);
  background-color: var(--red-100);
  padding: 0.5rem 1rem;
  border-radius: 3px;
}
</style>
<template>
  <div class="w-full sm:w-30rem m-auto pt-5 formgrid grid">
    <div>
      <h3>
        Personal info: {{ authStore.first_name + " " + authStore.last_name }}
      </h3>
      <h4>Username: {{ authStore.username }}</h4>
      <h4>Email: {{ authStore.email }}</h4>
    </div>
    <Divider></Divider>
    <h4>Update password</h4>
    <div class="field col-12">
      <label for="">Old password</label>
      <Password
        v-model="oldPassword"
        :class="{ 'p-invalid': !!errMsg.oldPassword }"
        :feedback="false"
        class="w-full"
        inputClass="w-full"
      >
      </Password>
      <div class="error-msg" v-if="errMsg.oldPassword">
        {{ errMsg.oldPassword }}
      </div>
    </div>
    <div class="field col-12">
      <label for="">New password</label>
      <Password
        v-model="newPassword"
        :class="{ 'p-invalid': !!errMsg.newPassword }"
        :feedback="false"
        class="w-full"
        inputClass="w-full"
      >
      </Password>
      <div class="error-msg" v-if="errMsg.newPassword">
        {{ errMsg.newPassword }}
      </div>
    </div>
    <div class="field col-12">
      <label for="">Re-type new password</label>
      <Password
        v-model="reTypeNewPassword"
        :class="{ 'p-invalid': !!errMsg.reTypeNewPassword }"
        :feedback="false"
        class="w-full"
        inputClass="w-full"
      >
      </Password>
      <div class="error-msg" v-if="errMsg.reTypeNewPassword">
        {{ errMsg.reTypeNewPassword }}
      </div>
    </div>
    <div class="flex col-12 gap-2 flex-nowrap justify-content-end">
      <Button
        class="flex max-w-min"
        severity="secondary"
        label="Cancle"
        @click="router.push({ name: 'dashboard' })"
      />
      <Button
        class="flex max-w-min"
        severity="info"
        label="Save"
        @click="submit"
      />
    </div>
  </div>
</template>
