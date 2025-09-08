<template>
    <div ref="target" class="absolute right-0 top-0 z-20 h-screen bg-white transition-all duration-300 ease-in-out"
        :style="{
            'box-shadow': '8px 0px 8px rgba(0, 0, 0, 0.1)',
            'max-width': '350px',
            'min-width': '350px'
        }">
        <div class="flex h-screen flex-col text-ink-gray-9">
            <div class="z-20 flex items-center justify-between border-b bg-white px-5 py-2.5">
                <div class="text-base font-medium">Notifications</div>
                <div class="flex gap-1">
                    <Tooltip text="Mark all as read">
                        <div>
                            <Button variant="ghost" @click="markAllAsRead">
                                <template #icon>
                                    <MarkAsDoneIcon class="h-4 w-4" />
                                </template>
                            </Button>
                        </div>
                    </Tooltip>
                    <Tooltip text="Close">
                        <div>
                            <Button variant="ghost" @click="$emit('close')">
                                <template #icon>
                                    <FeatherIcon name="x" class="h-4 w-4" />
                                </template>
                            </Button>
                        </div>
                    </Tooltip>
                </div>
            </div>

            <!-- Notifications List -->
            <div v-if="notifications.data?.length" class="divide-y divide-outline-gray-modals overflow-auto text-base">
                <div v-for="(n, index) in sort_notify" :key="index"
                    class="flex cursor-pointer items-start gap-2.5 px-4 py-2.5 hover:bg-surface-gray-2"
                    @click="markAsRead(n.name)">
                    <div class="mt-1 flex items-center gap-2.5">
                        <div v-if="n.read == 0" class=" w-1.5 h-1.5 rounded-full bg-gray-800"/>                      
                        <Avatar :label="n.from_user.name" size="lg" />
                    </div>
                    <div>
                        <div v-if="n.subject" v-html="n.subject" class="py-2 text-md font-bold"/>
                        <div v-if="n.notification_text" v-html="n.notification_text" />

                        <div class="text-sm text-ink-gray-1 mt-2">
                            {{ (timeAgo(n.creation)) }}
                        </div>
                    </div>
                </div>

                <!-- Load More Button -->
                <div v-if="notifications.data.length > visibleCount" class="flex border-t justify-center p-3">
                    <Button variant="outline" @click="loadMore">
                        {{ ('Load More') }}
                    </Button>
                </div>
            </div>

            <!-- No Notifications Message -->
            <div v-else class="flex flex-1 flex-col items-center justify-center gap-2">
                <NotificationsIcon class="h-20 w-20 text-ink-gray-2" />
                <div class="text-lg font-medium text-ink-gray-4">
                    No new notifications
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import MarkAsDoneIcon from '@/components/Icons/MarkAsDoneIcon.vue'
import NotificationsIcon from '@/components/Icons/NotificationsIcon.vue'
import { notifications, notificationsStore } from '@/data/notifications'
import { timeAgo } from '@/data/notifications'
import { ref, computed, onMounted } from 'vue'
import { Avatar } from 'frappe-ui'
const { mark_as_read, mark_doc_as_read } = notificationsStore()
const target = ref(null)

const visibleCount = ref(15)
defineEmits(['close'])


const sort_notify = computed(() => notifications.data?.slice(0, visibleCount.value) || [])


const loadMore = () => {
    visibleCount.value += 15
}

function markAsRead(doc) {   
    mark_doc_as_read(doc)
}

function markAllAsRead() {
    mark_as_read.reload()
}

onMounted(() => {
    notifications.reload()
})

</script>