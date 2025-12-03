<template>
    <Dropdown :options="dropdownOptions" v-bind="$attrs">
        <template v-slot="{ open }">
            <button class="flex h-12 items-center rounded-md py-2 duration-300 ease-in-out" :class="isCollapsed
                ? 'w-auto px-0'
                : open
                    ? 'w-52 bg-white px-2 shadow-sm'
                    : 'w-52 px-2 hover:bg-gray-200'
                ">
                <GO1Logo class="size-2 flex-shrink-0 rounded" />
                <div class="flex flex-1 flex-col text-left duration-300 ease-in-out" :class="isCollapsed
                    ? 'ml-0 w-0 overflow-hidden opacity-0'
                    : 'ml-2 w-auto opacity-100'
                    ">
                    <div class="text-base font-medium leading-none text-gray-900">
                        {{ __('Vendor') }}
                       
                    </div>
                    <div class="mt-1 text-sm leading-none text-gray-700">
                        <!-- {{ user.full_name }}  -->
                
                        <span v-if="logged_users.data">
                            {{ logged_users.data }}
                        </span>
                        <span v-else>
                            {{ __('Administrator') }}
                        </span>
                    </div>
                </div>
                <div class="duration-300 ease-in-out" :class="isCollapsed
                    ? 'ml-0  overflow-hidden opacity-0'
                    : 'ml-2 w-4 opacity-100'
                    ">        
                    <FeatherIcon name="chevron-down" class="size-48 text-gray-600" aria-hidden="true" />
                </div>
            </button>
        </template>
    </Dropdown>
</template>
 
<script setup>
 
import GO1Logo from '@/components/Icons/GO1Logo.vue'
import { Dropdown,FeatherIcon,createResource } from 'frappe-ui'
import { computed, ref, markRaw, watch, onMounted } from 'vue'
import { session } from '@/data/session';

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
});
 
const __ = (text) => text;

const users = createResource({
    url: 'go1_vendor.apidata.get_test',
    cache: ['true']
});
users.fetch();
const logged_users = users;

console.log('user',logged_users) 
 
const sessionCheck = () => {
    if (session?.logout?.submit) {
        session.logout.submit();      
    }
};
const hasDeskAccess = ref(false)

const deskAccess = createResource({
    url: 'frappe.client.get_value',
    makeParams() {
        const u = session.user
        if (!u) return null
        return { doctype: 'User', filters: { name: u }, fieldname: 'user_type' }
    },
    onSuccess(data) {
        hasDeskAccess.value = data?.message?.user_type === 'System User'
        if (!hasDeskAccess.value && session.user === 'Administrator') {
            hasDeskAccess.value = true
        }
    },
    onError() {
        hasDeskAccess.value = session.user === 'Administrator'
    },
})

onMounted(() => {
    if (session.user && deskAccess.fetch) {
        deskAccess.fetch()
    }
})

watch(
    () => session.user,
    (u) => {
        if (u && deskAccess.fetch) {
            deskAccess.fetch()
        }
    },
    { immediate: true }
)

const supportItem = {
    icon: 'life-buoy',
    label: computed(() => __('Support')),
    onClick: () => null,
}

const deskItem = {
    icon: 'desk',
    label: computed(() => __('Switch to Desk')),
    onClick: () => {
        window.location.href = '/app'
    },
}

const dropdownOptions = computed(() => [
    {
        group: 'Manage',
        hideLabel: true,
        items: hasDeskAccess.value ? [supportItem, deskItem] : [supportItem],
    },
    {
        group: 'Others',
        hideLabel: true,
        items: [
            {
                icon: 'log-out',
                label: computed(() => __('Log out')),
                onClick: sessionCheck,
            },
        ],
    },
])
</script>
