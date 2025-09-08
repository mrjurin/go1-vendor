<template>
  <div
    v-if="visible"
    :class="toastClasses"
    class="fixed bottom-10 right-10 px-4 py-2 rounded-md shadow-lg transition-opacity duration-300"
  >
    {{ message }}
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue'

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'success',
  },
})

const visible = ref(false)

watchEffect(() => {
  if (props.message) {
    visible.value = true
    setTimeout(() => {
      visible.value = false
    }, 3000)
  }
})

const toastClasses = computed(() => ({
  'bg-green-500 text-white': props.type === 'success',
  'bg-red-500 text-white': props.type === 'error',
}))
</script>
