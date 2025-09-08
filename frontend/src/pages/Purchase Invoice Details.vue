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
          <router-link to="/supplier-invoice">
            <span class="ml-3">Supplier Invoices / {{ paramsvalue.id }}</span>
          </router-link>
        </div>
      </div>
      <slot />

      <div
        class="main-content justify-items-center grid grid-cols-1 py-10 overflow-auto"
      >
        <div
          class="grid grid-cols-1 content-start gap-3 m-2 w-11/12 bg-white border rounded-md"
        >
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
            <div
              class="grid grid-cols-2 md:grid-cols-3 gap-3 justify-items-stretch text-gray-800"
            >
              <div
                class="flex flex-col gap-1"
                v-for="(detail, index) in details"
                :key="index"
              >
                <span class="text-gray-600 text-sm">{{ detail.label }}</span>
                <span
                  class="text-sm font-semibold py-2"
                  v-html="detail.value"
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

          <div class="grid grid-cols-1 px-16 mb-4">
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
                <!-- <div class="flex justify-between items-center">
                  <span class="text-gray-800 text-sm font-medium">In Words</span>
                  <span class="text-sm font-medium w-3/5 text-right">{{ in_words }}</span>
                </div> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
// import AppHeader from '@/components/Layouts/AppHeader.vue';
import { ref, onMounted, computed, reactive, watch } from 'vue'
import { createResource, Badge } from 'frappe-ui'
import { useRouter, useRoute } from 'vue-router'

const name = ref('')
const datevalue = ref('')
const company = ref('')
const billing_details = ref('')
const billing_address = ref('')
const inputValue = ref('')
const itemValue = ref([])
const supplierValue = ref([])
const total = ref('')
const grand_total = ref('')
const rounded_total = ref('')
const total_taxes = ref('')
const in_words = ref('')
const shippingaddress = ref('')
const supplier = ref('')
const pocode = ref('')
const poreference = ref('')
const allowedcurrency = ref('')
const sup_address_line1 = ref('')
const field_filters = reactive({})
let paramsvalue = ref({})

const updateparams = () => {
  paramsvalue.value = route.params
  paramsvalue = paramsvalue.value
}

const quote = createResource({
  url: 'go1_vendor.apidata.get_purchaseinvoice',
  params: {
    field_filters: JSON.stringify(field_filters),
  },
  method: 'GET',
})

const route = useRoute()

const fetchQuoteDetails = async () => {
  try {
    const id = route.params.id
    const data = await quote.fetch()
    const QuotationDetails = data.find((item) => item.name === id)
    console.log('QuotationDetails', QuotationDetails)

    if (QuotationDetails) {
      allowedcurrency.value = QuotationDetails.currency
      itemValue.value = QuotationDetails.items || []
      supplierValue.value = QuotationDetails.taxes || []
      total.value = QuotationDetails.total
      name.value = QuotationDetails.name
      inputValue.value = QuotationDetails.status
      datevalue.value = QuotationDetails.posting_date
      company.value = QuotationDetails.company
      billing_details.value = QuotationDetails.billing_address_display
      billing_address.value = QuotationDetails.billing_address
      total_taxes.value = QuotationDetails.total_taxes_and_charges
      grand_total.value = QuotationDetails.grand_total
      rounded_total.value = QuotationDetails.rounded_total
      in_words.value = QuotationDetails.in_words
      shippingaddress.value = QuotationDetails.shipping_address
      supplier.value = QuotationDetails.supplier
      pocode.value = QuotationDetails.supplier_name
      poreference.value = QuotationDetails.bill_no
      sup_address_line1.value = QuotationDetails.sup_address_line1
    }
  } catch (error) {
    console.error('Error fetching order details:', error)
  }
}

// onMounted(fetchQuoteDetails);

const details = computed(() => [
  { label: 'Name', value: name.value },
  { label: 'Date', value: datevalue.value },
  { label: 'Company', value: company.value },
  // { label: 'Billing Details', value: billing_details.value },
  // { label: 'Billing Address', value: billing_address.value },
  { label: 'Status', value: inputValue.value },
  { label: 'Total Value', value: rounded_total.value },
  { label: 'Supplier Name', value: pocode.value },
  { label: 'Allowed Currency', value: allowedcurrency.value },
  { label: 'Supplier', value: supplier.value },
  { label: 'Shipping Address', value: shippingaddress.value },
  // { label: 'PO Reference', value: poreference.value },
  // { label: 'Supplier Address Line 1', value: sup_address_line1.value },
])

const getTheme = (inputValue) => {
  switch (inputValue) {
    case 'Paid':
      return 'green'
    case 'Completed':
      return 'blue'
    case 'Draft':
      return 'red'
    case 'Closed':
      return 'orange'
    default:
      return 'gray'
  }
}
onMounted(() => {
  fetchQuoteDetails()
  updateparams()
})
watch(
  () => route.fullPath,
  () => {
    updateparams()
  }
)
</script>
