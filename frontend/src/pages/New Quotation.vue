<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-gray-50">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto">
      <div class="border-b flex justify-between items-center">
        <div class="flex items-center h-12 ml-3 text-lg font-semibold">
          Supplier Quotation
        </div>
        <Button
          variant="solid"
          theme="gray"
          size="sm"
          @click="createQuotation"
          class="mr-5"
          >Create Quotation</Button
        >
      </div>
      <slot />
      <div
        class="main-content justify-items-center grid grid-cols-1 py-10 overflow-auto"
      >
        <div
          class="grid grid-cols-1 content-start gap-3 m-2 w-11/12 bg-white border rounded-md pb-5"
        >
          <div class="grid grid-cols-1 p-3">
            <div
              class="grid grid-cols-2 md:grid-cols-3 gap-3 justify-items-stretch text-gray-800"
            >
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Supplier</span>
                <span class="text-sm font-semibold py-2">{{ supplier }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Date</span>
                <span class="text-sm font-semibold py-2">{{ dateValue }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Company</span>
                <span class="text-sm font-semibold py-2">{{ company }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Supplier Name</span>
                <span class="text-sm font-semibold py-2">{{
                  supplierName
                }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-gray-600 text-sm">Valid Till</span>
                <span class="text-sm font-semibold py-2">{{ validTill }}</span>
              </div>
            </div>
          </div>

          <!-- items -->
          <div class="grid grid-cols-1 p-3">
            <div class="w-full">
              <table
                class="w-full text-xs text-left whitespace-nowrap table-auto border border-gray-300"
              >
                <thead>
                  <tr class="bg-gray-100 border-b border-gray-300">
                    <th class="p-3 w-1/4 text-md font-normal text-left">
                      Item Code
                    </th>
                    <th class="p-3 w-1/6 text-md font-normal text-right">
                      Quantity
                    </th>
                    <th class="p-3 w-1/6 text-md font-normal text-center">
                      UOM
                    </th>
                    <th class="p-3 w-1/6 text-md font-normal text-center">
                      Rate
                    </th>
                    <th class="p-3 w-1/6 text-md font-normal text-right">
                      Amount
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(row, index) in itemValue"
                    :key="index"
                    class="border-b border-gray-200"
                  >
                    <td class="px-3 py-2 text-md font-medium text-left">
                      {{ row.item_code }}
                    </td>
                    <td class="px-3 py-2 text-md font-medium text-right">
                      {{ row.qty }}
                    </td>
                    <td class="px-3 py-2 text-md font-medium text-center">
                      {{ row.uom }}
                    </td>
                    <td class="px-3 py-2 text-md font-medium text-center">
                      <FormControl
                        class="w-20 text-center"
                        :type="'number'"
                        size="sm"
                        variant="subtle"
                        v-model.number="row.rate"
                        min="0"
                        @input="updateAmount(index)"
                      />
                    </td>
                    <td class="px-3 py-2 text-md font-medium text-right">
                      {{ row.amount }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- total -->
          <div class="grid grid-cols-1 px-6">
            <div class="grid grid-cols-1 gap-10 md:grid-cols-2">
              <div></div>
              <div class="flex flex-col w-full gap-3">
                <div class="flex justify-between items-center">
                  <span class="text-gray-800 ml-44 text-sm font-medium"
                    >Total</span
                  >
                  <span class="text-sm font-medium">{{ total }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Toast :message="toastMessage" :type="toastType" v-if="toastMessage" />
</template>

<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import { ref, onMounted } from 'vue'
import { createResource, FormControl } from 'frappe-ui'
import { useRoute, useRouter } from 'vue-router'
import Toast from '@/components/Toast.vue'

const router = useRouter()
const route = useRoute()
const rfqname = ref('')
const dateValue = ref('')
const validTill = ref('')
const supplier = ref('')
const supplierName = ref('')
const quotationNumber = ref('')
const total = ref(0)
const company = ref('')
const itemValue = ref([])

const toastMessage = ref('')
const toastType = ref('')

const quote = createResource({
  url: '/api/method/go1_vendor.api.get_rfq_details',
  params: { rfq_id: route.params.id },
  onSuccess(data) {
    if (data) {
      const rfqDetails = data.message
      const supplierDetails = data.supplier || {}
      company.value = rfqDetails.company
      dateValue.value = rfqDetails.transaction_date
      rfqname.value = rfqDetails.name
      supplierName.value = supplierDetails.supplier_name || '-'
      supplier.value = supplierDetails.name || '-'
      quotationNumber.value = ''
      itemValue.value = rfqDetails.items.map(
        ({ item_code, uom, qty, warehouse }) => ({
          item_code,
          uom,
          qty,
          rate: 0,
          amount: 0,
          warehouse,
        })
      )
      calculateValidTill(rfqDetails.transaction_date)
    }
  },
})

const calculateValidTill = (dateStr) => {
  if (!dateStr) return
  const date = new Date(dateStr)
  date.setMonth(date.getMonth() + 1)
  validTill.value = date.toISOString().split('T')[0]
}

const updateAmount = (index) => {
  const item = itemValue.value[index]
  item.amount = (item.rate * item.qty).toFixed(2)
  total.value = itemValue.value
    .reduce((sum, row) => sum + parseFloat(row.amount), 0)
    .toFixed(2)
}

const createQuotation = async () => {
  for (const item of itemValue.value) {
    if (!item.rate || item.rate <= 0) {
      toastMessage.value = `Enter a valid rate for item ${item.item_code}!`
      toastType.value = 'error'
      return
    }
  }
  console.log('itemValue.value', itemValue.value)
  const quotationData = {
    doctype: 'Supplier Quotation',
    supplier: supplier.value,
    transaction_date: dateValue.value,
    valid_till: validTill.value,
    total: total.value || 0,
    company: company.value,
    items: itemValue.value.map((item) => ({
      item_code: item.item_code,
      qty: item.qty,
      uom: item.uom,
      rate: item.rate,
      amount: item.amount,
      warehouse: item.warehouse,
      request_for_quotation: rfqname.value,
    })),
  }
  try {
    const response = await fetch('/api/resource/Supplier Quotation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token,
      },
      body: JSON.stringify(quotationData),
      credentials: 'include',
    })

    const result = await response.json()

    if (response.ok) {
      toastMessage.value = 'Quotation created successfully!'
      toastType.value = 'success'
      router.push('/supplier-quotation')
    }
  } catch (error) {
    toastMessage.value = 'Failed to create quotation.'
    toastType.value = 'error'
    console.error('Error creating quotation:', error)
  }
}

onMounted(() => {
  quote.fetch()
})
</script>
