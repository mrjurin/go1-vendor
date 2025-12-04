<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-gray-50">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto">
      <div class="mb-2 border-b p-4 flex justify-between items-center">
        <h1 class="text-xl font-semibold">Supplier Bill</h1>
        <div>
          <Button variant="solid" class="mr-3" @click="openMultiSelectDialog"
            >Get Items</Button
          >
          <Button type="submit" variant="solid" @click="saveSupplierInvoice"
            >Save</Button
          >
        </div>
      </div>
      <form class="p-4">
        <div class="grid grid-cols-4 gap-4">
          <template v-for="field in fields" :key="field.fieldname">
            <div>
              <label class="text-xs">{{ field.label }}</label>
              <component
                :is="getComponentType(field.fieldtype)"
                v-model="formData[field.fieldname]"
                class="w-full"
              />
            </div>
          </template>
        </div>
        <div class="mt-6">
          <h2 class="text-xs mb-2">Items</h2>
          <table class="min-w-full border">
            <thead class="bg-gray-100">
              <tr>
                <th
                  class="px-4 py-2 border text-left text-sm font-medium text-gray-600"
                >
                  <Checkbox
                    size="sm"
                    v-model="selectAll"
                    @change="toggleSelectAll"
                  />
                </th>

                <th
                  v-for="col in childTableColumns"
                  :key="col.fieldname"
                  class="px-4 py-2 border text-left text-xs font-medium text-gray-600"
                >
                  {{ col.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="childTableData.length === 0">
                <td
                  :colspan="childTableColumns.length + 1"
                  class="text-center text-gray-500 py-6"
                >
                  Get PO Items
                </td>
              </tr>
              <tr
                v-for="(row, index) in childTableData"
                :key="index"
                class="border-b border-gray-200 text-left"
              >
                <td class="px-4 py-2 text-left font-medium text-xs">
                  <input
                    type="checkbox"
                    v-model="selectedRows"
                    :value="index"
                    class="text-black rounded-sm"
                  />
                </td>

                <td
                  v-for="col in childTableColumns"
                  :key="col.fieldname"
                  class="border border-gray-300 p-2 text-xs"
                >
                  <template v-if="col.fieldname === 'qty'">
                    <input
                      type="number"
                      min="1"
                      :max="row.max_qty"
                      v-model="row[col.fieldname]"
                      @input="updateAmount(row)"
                      class="w-16 p-1 border-no rounded text-xs"
                    />
                  </template>
                  <template v-else-if="col.fieldname === 'amount'">
                    {{ row[col.fieldname] }}
                  </template>
                  <template v-else>
                    {{ row[col.fieldname] }}
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="p-3">
          <Button
            v-if="selectedRows.length > 0"
            variant="subtle"
            @click="deleteRows"
            class=""
            >Delete</Button
          >
        </div>
      </form>
    </div>
  </div>

  <Dialog v-model="dialogVisible">
    <template #body>
      <div class="p-5">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">
          Select Purchase Order
        </h2>
        <div class="overflow-x-auto">
          <table
            class="min-w-full border-collapse border border-gray-300 rounded-lg shadow-sm"
          >
            <thead class="bg-gray-100">
              <tr>
                <th
                  class="px-4 py-2 border text-left text-sm font-medium text-gray-600"
                >
                  <Checkbox
                    size="sm"
                    v-model="selectPoRecords"
                    @change="togglePoRecords"
                  />
                </th>
                <th
                  class="px-4 py-2 border text-left text-xs font-medium text-gray-600"
                >
                  Name
                </th>
                <th
                  class="px-4 py-2 border text-left text-xs font-medium text-gray-600"
                >
                  Schedule Date
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredPoRecords.length === 0">
                <td :colspan="3" class="text-center text-gray-500 py-6">
                  No Purchase Orders
                </td>
              </tr>
              <tr
                v-for="(po, index) in filteredPoRecords"
                :key="index"
                class="border-b border-gray-200 hover:bg-gray-50"
              >
                <td class="px-4 py-2 text-left font-medium text-xs">
                  <input
                    type="checkbox"
                    v-model="selectedPoRecords"
                    :value="po"
                    class="text-black rounded-sm"
                  />
                </td>
                <td class="border border-gray-300 p-3 text-xs">
                  {{ po.name }}
                </td>
                <td class="border border-gray-300 p-3 text-xs">
                  {{ po.schedule_date }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="flex justify-end mt-4">
          <Button variant="subtle" @click="appendSelectedItems"
            >Get Items</Button
          >
        </div>
      </div>
    </template>
  </Dialog>
  <Toast :message="toastMessage" :type="toastType" v-if="toastMessage" />
</template>

<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import {
  Checkbox,
  Button,
  DatePicker,
  Select,
  FormControl,
  FileUploader,
  Dialog,
} from 'frappe-ui'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Toast from '@/components/Toast.vue'

const router = useRouter()
const route = useRoute()
const fields = ref([])
const formData = ref({})
const childTableColumns = ref([])
const childTableData = ref([])
const selectAll = ref(false)
const selectPoRecords = ref(false)
const selectedRows = ref([])
const selectedPoRecords = ref([])
const dialogVisible = ref(false)
const poRecords = ref([])
const selectedcompany = ref()
const toastMessage = ref('')
const toastType = ref('')

const Poname = route.query.name

const toggleSelectAll = () => {
  selectAll.value = !selectAll.value

  if (selectAll.value) {
    selectedRows.value = childTableData.value.map((_, index) => index)
  } else {
    selectedRows.value = []
  }
}

const togglePoRecords = () => {
  if (selectPoRecords.value) {
    selectedPoRecords.value = [...poRecords.value]
  } else {
    selectedPoRecords.value = []
  }
}

const deleteRows = () => {
  childTableData.value = childTableData.value.filter(
    (_, index) => !selectedRows.value.includes(index)
  )
  selectAll.value = false
  selectedRows.value = []
}

const updateAmount = (row) => {
  if (row.qty > row.max_qty) {
    row.qty = row.max_qty
  }
  row.amount = row.qty * row.rate
  calculateTotals()
}

const filteredPoRecords = computed(() => {
  const existingPoNames = new Set(
    childTableData.value.map((item) => item.purchase_order_reference)
  )
  return poRecords.value.filter((po) => !existingPoNames.has(po.name))
})

async function fetchFields() {
  try {
    const response = await fetch(
      '/api/method/go1_vendor.api.fetch_supplier_invoice'
    )
    const data = await response.json()
    fields.value = data.message

    formData.value = fields.value.reduce((acc, field) => {
      if (field.fieldname === 'posting_date') {
        acc[field.fieldname] = new Date().toISOString().split('T')[0]
      } else {
        acc[field.fieldname] = ''
      }
      return acc
    }, {})

    await fetchSupplierDetails()
  } catch (error) {
    console.error('Error fetching fields:', error)
  }
}

async function fetchSupplierDetails() {
  try {
    const response = await fetch('/api/method/go1_vendor.api.get_test')
    const data = await response.json()

    if (data.message) {
      formData.value.supplier = data.message.name
      formData.value.supplier_name = data.message.supplier_name
    }
  } catch (error) {
    console.error('Error fetching supplier details:', error)
  }
}

async function fetchChildTableColumns() {
  try {
    const response = await fetch(
      '/api/method/go1_vendor.api.fetch_supplier_invoice_items'
    )
    const data = await response.json()
    childTableColumns.value = [
      ...data.message,
      {
        fieldname: 'purchase_order_reference',
        label: 'PO Reference',
        fieldtype: 'Data',
      },
      { fieldname: 'schedule_date', label: 'Required By', fieldtype: 'Date' },
    ]
  } catch (error) {
    console.error('Error fetching child table columns:', error)
  }
}

async function fetchPurchaseOrders() {
  try {
    const response = await fetch(
      `/api/method/go1_vendor.api.fetch_purchase_orders?supplier=${formData.value.supplier}`
    )
    const data = await response.json()
    poRecords.value = data.message
  } catch (error) {
    console.error('Error fetching purchase orders:', error)
  }
}

async function openMultiSelectDialog() {
  await fetchPurchaseOrders()
  dialogVisible.value = true
}

function getComponentType(fieldType) {
  const components = {
    Date: DatePicker,
    Data: FormControl,
    Attach: FileUploader,
  }
  return components[fieldType] || FormControl
}

async function appendSelectedItems() {
  const firstCompany = selectedPoRecords.value[0].company

  const isSameCompany = selectedPoRecords.value.every(
    (po) => po.company === firstCompany
  )

  if (!isSameCompany) {
    dialogVisible.value = false
    toastMessage.value = `All selected Purchase Orders must belong to the same company`
    toastType.value = 'error'
    return
  }

  const po_names = selectedPoRecords.value.map((record) => record.name)

  const response = await fetch(
    '/api/method/go1_vendor.api.get_purchase_order_items',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ po_names }),
    }
  )

  const result = await response.json()

  if (result.message && Array.isArray(result.message)) {
    const existingPo = new Set(
      childTableData.value.map((item) => item.purchase_order_reference)
    )

    const newItems = result.message
      .filter((item) => !existingPo.has(item.purchase_order_reference))
      .map((item) => ({
        ...item,
        max_qty: item.qty ?? 0,
      }))

    childTableData.value = [...childTableData.value, ...newItems]
    if (selectedPoRecords.value.length > 0) {
      selectedcompany.value = selectedPoRecords.value[0].company
    }
  }

  dialogVisible.value = false
}

const calculateTotals = () => {
  const total = childTableData.value.reduce(
    (sum, item) => sum + (item.amount || 0),
    0
  )
  formData.value.total = total
  formData.value.grand_total = total
  formData.value.rounded_total = Math.round(total)
}

const saveSupplierInvoice = async () => {
  calculateTotals()

  const supplierInvoiceData = {
    doctype: 'Supplier Invoice',
    supplier: formData.value.supplier,
    supplier_name: formData.value.supplier_name,
    posting_date: formData.value.posting_date,
    total: formData.value.total,
    grand_total: formData.value.grand_total,
    rounded_total: formData.value.rounded_total,
    bill_no: formData.value.bill_no,
    bill_date: formData.value.bill_date,
    company: selectedcompany.value,
    status: 'Draft',
    items: childTableData.value.map((item) => ({
      item_code: item.item_code,
      qty: item.qty,
      uom: item.uom,
      rate: item.rate,
      amount: item.amount,
      base_amount: item.amount,
      base_rate: item.rate,
      stock_qty: item.qty,
      purchase_order: item.purchase_order_reference,
    })),
  }

  try {
    const response = await fetch('/api/resource/Supplier Invoice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token,
      },
      body: JSON.stringify(supplierInvoiceData),
      credentials: 'include',
    })

    const result = await response.json()

    if (response.ok) {
      router.push('/supplier-invoice')
      console.log('Supplier Invoice saved successfully:', result)
    } else {
      console.error('Failed to save Supplier Invoice:', result)
    }
  } catch (error) {
    console.error('Error saving Supplier Invoice:', error)
  }
}
onMounted(async () => {
  await fetchFields()
  await fetchChildTableColumns()

  if (Poname) {
    await fetchPurchaseOrders()
    selectedPoRecords.value = poRecords.value.filter((po) => po.name === Poname)
    if (selectedPoRecords.value.length > 0) {
      await appendSelectedItems()
    }
  }
})
</script>

<style scoped>
.grid-cols-3 {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.overflow-x-auto {
  overflow-x: auto;
}

.min-w-full {
  min-width: 100%;
}

.border {
  border: 1px solid #ddd;
}

.bg-gray-100 {
  background-color: #edebeb;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.text-left {
  text-align: center;
}

.text-sm {
  font-size: 0.7rem;
}

.text-xs {
  font-size: 0.8rem;
}

.font-medium {
  font-weight: 500;
}

.text-gray-600 {
  color: #4a5568;
}

.border-b {
  border-bottom: 1px solid #e2e8f0;
}

.border-gray-200 {
  border-color: #edf2f7;
}

.text-black {
  color: black;
}

.rounded-sm {
  border-radius: 4px;
  width: 13px;
  height: 13px;
}

.w-15 {
  width: 4rem;
}

.p-3 {
  padding: 0.75rem;
}
</style>
