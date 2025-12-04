<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-gray-50">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto">
      <div class="border-b flex">
        <div
          v-if="paramsvalue && Object.keys(paramsvalue).length > 0"
          class="flex flex-1 items-center h-12"
        >
          <router-link to="/purchase-order">
            <span class="ml-3">Purchase Orders / {{ paramsvalue.id }}</span>
          </router-link>
        </div>
        <div class="p-2">
          <router-link
            :to="{ path: '/new-supplier-bill', query: { name: name } }"
          >
            <Button variant="solid" theme="gray" size="sm">New Bill</Button>
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
              <Badge
                :variant="'subtle'"
                :theme="getTheme(inputValue)"
                size="md"
                label="Badge"
              >
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
                <span class="text-gray-600 text-sm">Date</span>
                <span class="text-sm font-semibold py-2">{{ dateValue }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Required Date</span>
                <span class="text-sm font-semibold py-2">{{
                  requiredate
                }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Total Value</span>
                <span class="text-sm font-semibold py-2">{{ total }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Supplier</span>
                <span class="text-sm font-semibold py-2">{{ supplier }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Address</span>
                <span
                  class="text-sm font-semibold py-2"
                  v-html="addressLine1 + ',<br>' + addressLine2"
                ></span>
              </div>
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
                    class="p-3 text-md font-semibold text-center border border-gray-300"
                  >
                    UOM
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-right border border-gray-300"
                  >
                    Rate
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-center border border-gray-300"
                  >
                    Amount
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
                    class="px-3 py-2 text-md text-center font-medium border border-gray-300"
                  >
                    {{ row.uom }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-right font-medium border border-gray-300"
                  >
                    {{ row.rate }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-center font-medium border border-gray-300"
                  >
                    {{ row.amount }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="grid grid-cols-1 px-16">
            <div class="grid grid-cols-1 gap-10 md:grid-cols-2">
              <div></div>
              <div class="flex flex-col w-full gap-3">
                <div class="flex justify-between items-center">
                  <span class="text-gray-800 ml-15 text-sm font-medium"
                    >Total</span
                  >
                  <span class="text-sm font-medium">{{ total }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="supplierValue[0]" class="w-full overflow-x-auto p-3">
            <table
              class="w-full text-sm border-collapse border border-gray-300"
            >
              <thead class="bg-gray-100">
                <tr>
                  <th
                    class="p-3 text-md font-semibold text-left border border-gray-300"
                  >
                    Type
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-left border border-gray-300"
                  >
                    Account Head
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-right border border-gray-300"
                  >
                    Tax Rate
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-right border border-gray-300"
                  >
                    Amount
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-center border border-gray-300"
                  >
                    Total
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, index) in supplierValue"
                  :key="index"
                  class="border-b border-gray-300 odd:bg-gray-50"
                >
                  <td
                    class="px-3 py-2 text-md font-medium border border-gray-300"
                  >
                    {{ row.charge_type }}
                  </td>
                  <td
                    class="px-3 py-2 text-md font-medium border border-gray-300"
                  >
                    {{ row.account_head }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-right font-medium border border-gray-300"
                  >
                    {{ row.rate }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-right font-medium border border-gray-300"
                  >
                    {{ row.tax_amount }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-center font-medium border border-gray-300"
                  >
                    {{ row.total }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="grid grid-cols-1 px-16">
            <div class="grid ml-15 grid-cols-1 gap-10 md:grid-cols-2">
              <div></div>
              <div class="flex flex-col w-full gap-3">
                <div class="flex justify-between items-center">
                  <span class="text-gray-800 text-sm font-medium"
                    >Tax Amount</span
                  >
                  <span class="text-sm font-medium">{{ total_taxes }}</span>
                </div>
                <hr />
                <div class="flex justify-between items-center mt-3">
                  <span class="text-gray-800 text-sm font-medium"
                    >Grand Total</span
                  >
                  <span class="text-sm font-medium">{{ grand_total }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-800 text-sm font-medium"
                    >Rounded Total</span
                  >
                  <span class="text-sm font-medium">{{ rounded_total }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-800 text-sm font-medium"
                    >In Words</span
                  >
                  <span class="text-sm font-medium w-3/5 text-right">{{
                    in_words
                  }}</span>
                </div>
              </div>
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
                    Payment Term
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-left border border-gray-300"
                  >
                    Description
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-left border border-gray-300"
                  >
                    Due Date
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-right border border-gray-300"
                  >
                    Invoice Portion
                  </th>
                  <th
                    class="p-3 text-md font-semibold text-center border border-gray-300"
                  >
                    Payment Amount
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, index) in payments"
                  :key="index"
                  class="border-b border-gray-300 odd:bg-gray-50"
                >
                  <td
                    class="px-3 py-2 text-md font-medium border border-gray-300"
                  >
                    {{ row.payment_term }}
                  </td>
                  <td
                    class="px-3 py-2 text-md font-medium border border-gray-300"
                  >
                    {{ row.description }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-left font-medium border border-gray-300"
                  >
                    {{ row.due_date }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-right font-medium border border-gray-300"
                  >
                    {{ row.invoice_portion }}{{ '%' }}
                  </td>
                  <td
                    class="px-3 py-2 text-md text-center font-medium border border-gray-300"
                  >
                    {{ row.payment_amount }}
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
const name = ref('')
const dateValue = ref('')
const requiredate = ref('')
const inputValue = ref('')
const itemValue = ref([])
const supplierValue = ref([])
const payments = ref([])
const supplier = ref('')
const addressLine1 = ref('')
const addressLine2 = ref('')
const total = ref('')
const grand_total = ref('')
const rounded_total = ref('')
const in_words = ref('')
const total_taxes = ref('')
const field_filters = reactive({})
let paramsvalue = ref({})

const updateparams = () => {
  paramsvalue.value = route.params
  paramsvalue = paramsvalue.value
}

const quote = createResource({
  url: 'go1_vendor.apidata.get_purchaseorder',
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
    console.log('QuotationDetails', QuotationDetails)

    if (QuotationDetails) {
      name.value = QuotationDetails.name
      inputValue.value = QuotationDetails.status
      dateValue.value = QuotationDetails.transaction_date
      requiredate.value = QuotationDetails.transaction_date
      itemValue.value = QuotationDetails.items || []
      supplierValue.value = QuotationDetails.taxes || []
      payments.value = QuotationDetails.payments || []
      total.value = QuotationDetails.total
      grand_total.value = QuotationDetails.grand_total
      in_words.value = QuotationDetails.in_words
      rounded_total.value = QuotationDetails.rounded_total
      total_taxes.value = QuotationDetails.total_taxes_and_charges
      supplier.value = QuotationDetails.supplier
      addressLine1.value = QuotationDetails.supplier_address
      addressLine2.value = QuotationDetails.address_display
    }
  } catch (error) {
    console.error('Error fetching order details:', error)
  }
}

onMounted(() => {
  fetchQuoteDetails()
  updateparams()
})

const getTheme = (inputValue) => {
  const themes = {
    Paid: 'green',
    Completed: 'blue',
    Draft: 'red',
    Closed: 'orange',
  }
  return themes[inputValue] || 'gray'
}
watch(
  () => route.fullPath,
  () => {
    updateparams()
  }
)
</script>
