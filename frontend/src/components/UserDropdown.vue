<template>
  <Dropdown :options="dropdownOptions" v-bind="$attrs">
    <template v-slot="{ open }">
      <button
        class="flex h-12 items-center rounded-md py-2 duration-300 ease-in-out"
        :class="
          isCollapsed
            ? 'w-auto px-0'
            : open
            ? 'w-52 bg-white px-2 shadow-sm'
            : 'w-52 px-2 hover:bg-gray-200'
        "
      >
        <GO1Logo class="size-2 flex-shrink-0 rounded" />
        <div
          class="flex flex-1 flex-col text-left duration-300 ease-in-out"
          :class="
            isCollapsed
              ? 'ml-0 w-0 overflow-hidden opacity-0'
              : 'ml-2 w-auto opacity-100'
          "
        >
          <div class="text-base font-medium leading-none text-gray-900">
            {{ __('Vendor Portal') }}
          </div>
          <div class="mt-1 text-sm leading-none text-gray-700">
            <!-- {{ user.full_name }}  -->

            <span>
              {{ logged_users.data }}
            </span>
          </div>
        </div>
        <div
          class="duration-300 ease-in-out"
          :class="
            isCollapsed
              ? 'ml-0  overflow-hidden opacity-0'
              : 'ml-2 w-4 opacity-100'
          "
        >
          <FeatherIcon
            name="chevron-down"
            class="size-48 text-gray-600"
            aria-hidden="true"
          />
        </div>
      </button>
    </template>
  </Dropdown>
</template>

<script setup>
import GO1Logo from '@/components/Icons/GO1Logo.vue'
import { Dropdown, FeatherIcon, createResource } from 'frappe-ui'
import { computed, ref, markRaw, onMounted } from 'vue'
import Apps from '@/components/App.vue'
import { session } from '@/data/session'

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

const __ = (text) => text

const users = createResource({
  url: 'go1_vendor.apidata.get_user',
  auto: true,
  transform: (data) => data,
})
const logged_users = users
const sessionCheck = () => {
  if (session?.logout?.submit) {
    session.logout.submit()
  }
}
const dropdownOptions = computed(() => {
  let options = [
    {
      group: 'Others',
      hideLabel: true,
      items: [
        {
          icon: 'log-out',
          label: __('Log out'),
          onClick: sessionCheck,
        },
      ],
    },
  ]

  if (logged_users.data == 'Administrator') {
    options.unshift({
      group: 'Manage',
      hideLabel: true,
      items: [
        {
          component: markRaw(Apps),
        },
      ],
    })
  }

  return options
})
</script>
