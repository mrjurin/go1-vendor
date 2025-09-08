import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { computed, ref } from 'vue'
import { useDateFormat, useTimeAgo } from '@vueuse/core'

export const visible = ref(false)

export const notifications = createResource({
  url: 'go1_vendor.apidata.get_notifications',
  initialData: [],
  auto: true,
})
export const unreadNotificationsCount = computed(
  () => notifications.data?.filter((n) => !n.read).length || 0,
)

export const notificationsStore = defineStore('crm-notifications', () => {
  const mark_as_read = createResource({
    url: 'go1_vendor.apidata.mark_as_read',
    onSuccess: () => {
      mark_as_read.params = {}
      notifications.reload()
    },
  }) 

  function mark_doc_as_read(doc) { 
    mark_as_read.params = { doc: doc }
    mark_as_read.reload()
   
  }

  return {
    unreadNotificationsCount,
    mark_as_read,
    mark_doc_as_read,
    
  }
})

export function timeAgo(date) {
  return useTimeAgo(date).value
}
