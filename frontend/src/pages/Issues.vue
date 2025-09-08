<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-gray-50">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto">
      <div class="mb-2 border-b py-3 px-5">
        <span>New Issue</span>
      </div>
      <!-- <AppHeader /> -->

      <!-- <slot /> -->
      <div class="main-content justify-items-center grid grid-cols-1 py-10 overflow-auto">
        <div class="grid grid-cols-1 content-start gap-3 m-2 w-11/12 bg-white border rounded-md">
          <div class="px-3 py-3 border-b">
            <div class="flex justify-between items-center">
              <span class="text-xl text-cyan-600 font-semibold">
                New Issue</span>
            </div>
          </div>
          <div class="grid grid-cols-1 p-3">
            <div class="mb-5 text-lg font-medium">
              <h1>Details:</h1>
            </div>
            <div class="grid grid-cols-3 gap-6 overflow-auto">
              <!-- <div class="p-5 border rounded-md w-11/12 "> -->
              <div class="text-gray-600">
                Subject
                <span class="text-red-600">*</span>
                <FormControl type="text" size="md" variant="subtle" placeholder="Subject" v-model="subject" class="" />
              </div>

              <FormControl v-if="!logged_users.data" type="select" size="md" variant="subtle" :options="customOption"
                label="Supplier" v-model="supplier" placeholder="Supplier" class="" />
              <FormControl type="select" size="md" :options="statusOptions" variant="subtle" placeholder="Status"
                label="Status" v-model="status" class="text-gray-1000 text-base" />
              <div class="text-gray-600">
                Issue Type
                <span class="text-red-600">*</span>
                <FormControl type="select" size="md" variant="subtle" :options="optionIssue" placeholder="Issue type"
                  v-model="issuetype" class="mb-3" />
              </div>
              <div class="text-gray-600">
                Priority
                <span class="text-red-600">*</span>
                <FormControl type="select" size="md" variant="subtle" :options="priorityOption" placeholder="Priority"
                  v-model="priority" class="mb-3" />
              </div>
            </div>
            <div class="text-gray-600">
              Description
              <span class="text-red-600">*</span>
              <Textarea class="h-[100px]" type="textarea" variant="subtle" size="md" placeholder="Description"
               v-model="description" />
            </div>
          </div>
          <div class="justify-end flex gap-4 p-3">
            <Button variant="subtle" theme="gray" size="md" label="Discard" @click="cancelEditing" />
            <Button variant="solid" theme="gray" size="md" label="Submit" @click="createIssue" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <Toast :message="toastMessage" :type="toastType" v-if="toastMessage" />
</template>
<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Toast from '@/components/Toast.vue'
import {
  Button,
  FormControl,
  Textarea,
  createResource,
} from 'frappe-ui'

const router = useRouter()

const subject = ref('')
const status = ref('Open')
const description = ref('')
const priority = ref('')
const supplier = ref('')
const customOption = ref([])
const priorityOption = ref([])
const issuetype = ref([])
const optionIssue = ref([])
const toastMessage = ref('')
const toastType = ref('')

const users = createResource({
  url: 'go1_vendor.apidata.get_test',
  cache: ['true'],
})
users.fetch()
const logged_users = users

watch(logged_users, (newLoggedUsers) => {
  if (newLoggedUsers.data) {
    supplier.value = newLoggedUsers.data;
  }
});

const breadcrumbsList = ref([
  { label: 'Issues', route: { name: 'Issues' } },
  { label: 'Create Issue', route: {} },
])

const statusOptions = [
  { label: 'Open', value: 'Open' },
  { label: 'Closed', value: 'Closed' },
  { label: 'Replied', value: 'Replied' },
  { label: 'On Hold', value: 'On Hold' },
  { label: 'Resolved', value: 'Resolved' },
]

const cancelEditing = () => {
  subject.value = ''
  status.value = ''
  description.value = ''
  supplier.value = ''
  priority.value = ''
  issuetype.value = ''
}

const createIssue = async () => {
  if(!subject.value){
    toastMessage.value = `Subject is Required`
    toastType.value = 'error'
    return
  }
  if(!issuetype.value){
    toastMessage.value = `Type is Required`
    toastType.value = 'error'
    return
  }
  if(!priority.value){
    toastMessage.value = `Priority is Required`
    toastType.value = 'error'
    return
  }
  if(!description.value){
    toastMessage.value = `Description is Required`
    toastType.value = 'error'
    return
  }  
  const issueData = {
    subject: subject.value,
    status: status.value,
    priority: priority.value,
    issue_type: issuetype.value,
    description: description.value,
    custom_supplier: supplier.value,
  }

  try {
    const response = await fetch('/api/resource/Issue', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(issueData),
    })

    if (!response.ok) throw new Error('Error creating issue')
    router.push({ name: 'IssuesList' })
  } catch (error) {
    console.error('Error creating issue:', error)
  }
}

const optionsSupplier = async () => {
  try {
    const response = await fetch('/api/resource/Supplier?fields=["name"]')
    if (!response.ok) throw new Error('Network response was not ok')

    const supplierdata = await response.json()
    customOption.value = supplierdata.data.map((user) => user.name) || []
  } catch (error) {
    console.error('Error fetching supplier:', error)
  }
}

const optionsIssueType = async () => {
  try {
    const response = await fetch('/api/resource/Issue Type?fields=["name"]')
    if (!response.ok) throw new Error('Network response was not ok')

    const issuetypedata = await response.json()
    optionIssue.value = issuetypedata.data.map((user) => user.name) || []
  } catch (error) {
    console.error('Error fetching IssueType:', error)
  }
}

const optionsPriority = async () => {
  try {
    const response = await fetch('/api/resource/Issue Priority?fields=["name"]')
    if (!response.ok) throw new Error('Network response was not ok')

    const prioritydata = await response.json()
    priorityOption.value = prioritydata.data.map((user) => user.name) || []
  } catch (error) {
    console.error('Error fetching priority:', error)
  }
}

watch(subject, (newSubject) => {
  breadcrumbsList.value[1].label = newSubject
})

onMounted(async () => {
  await optionsSupplier()
  await optionsPriority()
  await optionsIssueType()
})
</script>
