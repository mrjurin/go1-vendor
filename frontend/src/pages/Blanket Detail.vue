<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-gray-50">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto">
      <div class="border-b flex">
        <div
          v-if="paramsvalue && Object.keys(paramsvalue).length > 0"
          class="flex justify-between items-center h-12"
        >
          <router-link to="/blanket-orders">
            <span class="ml-3">Blanket Order / {{ paramsvalue.id }}</span>
          </router-link>
        </div>
      </div>
      <!-- <AppHeader /> -->
      <slot />
      <!-- Passing dynamic 'id' to the handleButtonClick function -->
      <div
        class="main-content justify-items-center grid grid-cols-1 py-5 overflow-auto"
      >
        <div
          class="grid grid-cols-1 content-start gap-3 m-2 w-11/12 bg-white border rounded-md pb-5"
        >
          <!-- heading -->
          <div class="px-3 py-3 border-b">
            <div class="flex justify-between items-center">
              <span class="text-xl text-cyan-600 font-semibold">{{
                name
              }}</span>
              <Badge :variant="'subtle'" :theme="badgeTheme" size="md">
                {{ inputValue }}
              </Badge>
            </div>
          </div>

          <div class="grid grid-cols-1 p-3">
            <div class="mb-5 text-lg font-medium">
              <h1>Details:</h1>
            </div>
            <div
              class="grid grid-cols-2 md:grid-cols-3 gap-3 justify-items-stretch text-gray-800"
            >
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Name</span>
                <span class="text-sm font-semibold py-2">{{ name }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">From Date</span>
                <span class="text-sm font-semibold py-2">{{ dateValue }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">To Date</span>
                <span class="text-sm font-semibold py-2">{{
                  requiredate
                }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Order Type</span>
                <span class="text-sm font-semibold py-2">{{ ordertype }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Supplier</span>
                <span class="text-sm font-semibold py-2">{{ supplier }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Cpmpany</span>
                <span class="text-sm font-semibold py-2">{{ company }}</span>
              </div>
              <!-- <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Address</span>
                <span class="text-sm font-semibold py-2" v-html="addressLine1 + ',<br>' + addressLine2"></span>
              </div> -->
            </div>
          </div>

          <div class="w-full overflow-x-auto p-3">
            <table
              class="w-full text-sm border-collapse border border-gray-300"
            >
              <thead class="bg-gray-100">
                <tr>
                  <th
                    class="p-3 text-md font-semibold text-left border border-gray-300"
                  >
                    Item Code
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-left border border-gray-300"
                  >
                    Item Name
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-right border border-gray-300"
                  >
                    Quantity
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-right border border-gray-300"
                  >
                    Rate
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-center border border-gray-300"
                  >
                    Ordered Quantity
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, index) in itemValue"
                  :key="index"
                  class="border-b border-gray-300 odd:bg-gray-50"
                >
                  <td
                    class="px-3 py-2 text-md font-medium border border-gray-300"
                  >
                    {{ row.item_code }}
                  </td>
                  <td
                    class="px-3 py-2 text-md font-medium border border-gray-300"
                  >
                    {{ row.item_name }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-right font-medium border border-gray-300"
                  >
                    {{ row.qty }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-right font-medium border border-gray-300"
                  >
                    {{ row.rate }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-center font-medium border border-gray-300"
                  >
                    {{ row.ordered_qty }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
// import AppHeader from '@/components/Layouts/AppHeader.vue';
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { createResource, Badge, Button } from 'frappe-ui'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isSidebarCollapsed = ref(false)
const badgeTheme = ref('')
const name = ref('')
const dateValue = ref('')
const requiredate = ref('')
const inputValue = ref('')
const itemValue = ref([])
const supplier = ref('')
const ordertype = ref('')
const company = ref('')
const field_filters = reactive({})
let paramsvalue = ref({})

const updateparams = () => {
  paramsvalue.value = route.params
  paramsvalue = paramsvalue.value
}

const quote = createResource({
  url: 'go1_vendor.apidata.get_blanketorder',
  params: {
    field_filters: JSON.stringify(field_filters),
  },
  method: 'GET',
})
const fetchQuoteDetails = async () => {
  try {
    const id = route.params.id
    const data = await quote.fetch()
    const QuotationDetails = data.find((items) => items.name === id)
    console.log('b', QuotationDetails)

    if (QuotationDetails) {
      name.value = QuotationDetails.name
      // inputValue.value = QuotationDetails.status;
      dateValue.value = QuotationDetails.from_date
      requiredate.value = QuotationDetails.to_date
      ordertype.value = QuotationDetails.blanket_order_type
      company.value = QuotationDetails.company
      itemValue.value = QuotationDetails.items || []
      supplier.value = QuotationDetails.supplier
      inputValue.value = getStatusLabel(QuotationDetails.docstatus)
      badgeTheme.value = getStatusTheme(QuotationDetails.docstatus).theme
    }
  } catch (error) {
    console.error('Error fetching order details:', error)
  }
}

onMounted(() => {
  fetchQuoteDetails()
  updateparams()
})
const getStatusTheme = (docstatus) => {
  switch (parseInt(docstatus)) {
    case 0:
      return { theme: 'red' }
    case 1:
      return { theme: 'blue' }
    case 2:
      return { theme: 'green' }
    default:
      return { theme: 'gray' }
  }
}
const getStatusLabel = (docstatus) => {
  switch (parseInt(docstatus)) {
    case 0:
      return 'Draft'
    case 1:
      return 'Submitted'
    case 2:
      return 'Cancelled'
    default:
      return 'Unknown'
  }
}

watch(
  () => route.fullPath,
  () => {
    updateparams()
  }
)
</script>
