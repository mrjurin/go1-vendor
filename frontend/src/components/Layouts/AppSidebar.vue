<template>
  <div class="relative flex h-full flex-col justify-between transition-all bg-gray-50 duration-300 ease-in-out"
    :class="isSidebarCollapsed ? 'w-12' : 'w-[220px]'">
    <div class="head">
      <UserDropdown class="p-2" :isCollapsed="isSidebarCollapsed" />
    </div>
    <div class="p-2 ">
      <Button class="w-full justify-start text-gray-800 bg-white !block overflow-hidden" :variant="'ghost'" size="sm"
      @click="toggleNotifications">
        <template v-if="isSidebarCollapsed">
          <FeatherIcon class="w-4 text-black flex items-center" stroke="black" :stroke-width="1" name="bell" />
        </template>
        <template v-else>
          <div class="flex items-center">
            <div style="float: left">
              <FeatherIcon class="w-4 text-black" stroke="black" :stroke-width="1" name="bell" />
            </div>
            <span class="ml-2">Notificaton</span>
            
            <span v-if="unreadNotificationsCount" class="ml-auto bg-red-500 text-white text-2xs rounded-full h-4 w-4 flex items-center justify-center">
            {{ unreadNotificationsCount}}
            </span>
          </div>
        </template>
      </Button>
      <Notifications v-if="showNotifications" @close="showNotifications = false" class=" top-0 left-[220px]"  />
    </div>
    <div class="flex-1 overflow-y-auto p-2">
      <!-- Content here -->
      <Sidebarlink :isCollapsed="isSidebarCollapsed" />
    </div>

    <div class="m-2 flex flex-col gap-1">
      <Button class="w-full justify-start text-gray-800 bg-white !block overflow-hidden" @click="toggleSidebar"
        :variant="'ghost'" size="sm">
        <template v-if="isSidebarCollapsed">
          <CollapseSidebar class="w-4 text-black flex items-center"
            :class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }" />
        </template>
        <template v-else>
          <div class="flex items-center">
            <div style="float: left">
              <CollapseSidebar />
            </div>
            <span class="ml-2">Collapse</span>
          </div>          
        </template>
      </Button>
    </div>
  </div>
 
</template>

<script setup>
import { useStorage } from '@vueuse/core'
import UserDropdown from '@/components/UserDropdown.vue'
import Notifications from '@/components/Notifications.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import Sidebarlink from '@/components/Layouts/Sidebarlink.vue'
import { unreadNotificationsCount } from '@/data/notifications'
import { ref } from 'vue'

const isSidebarCollapsed = useStorage('isSidebarCollapsed', false)

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
const showNotifications = ref(false)

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
}
</script>
