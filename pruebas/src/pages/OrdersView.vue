<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { fetchOrders } from "../services/api";
import OrderTable from "../components/OrderTable.vue"; 

const searchQuery = ref("");
const sortColumn = ref<string | null>(null);
const sortOrder = ref<"asc" | "desc">("asc");
const currentPage = ref(1);
const itemsPerPage = 10;
const selectedOrder = ref<any | null>(null);

const { data: orders, isLoading, error } = useQuery({
  queryKey: ["orders"],
  queryFn: fetchOrders,
});

const filteredOrders = computed(() => {
  if (!orders.value) return [];

  const query = searchQuery.value.toLowerCase();
  return orders.value.filter((order: any) => {
    return Object.values(order).some((value: any) => {
      if (Array.isArray(value)) {
        return value.some((item) => String(item).toLowerCase().includes(query));
      }
      return String(value).toLowerCase().includes(query);
    });
  });
});

const sortedOrders = computed(() => {
  if (!filteredOrders.value.length || !sortColumn.value) return filteredOrders.value;

  return [...filteredOrders.value].sort((a, b) => {
    const aValue = a[sortColumn.value as keyof typeof a] || "";
    const bValue = b[sortColumn.value as keyof typeof b] || "";

    return sortOrder.value === "asc"
      ? String(aValue).localeCompare(String(bValue))
      : String(bValue).localeCompare(String(aValue));
  });
});

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return sortedOrders.value.slice(start, start + itemsPerPage);
});



const totalPages = computed(() => Math.ceil(filteredOrders.value.length / itemsPerPage));
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++; };
const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };

const viewOrderDetails = (order: any) => {
  selectedOrder.value = order;
};

const closeOrderDetails = () => {
  selectedOrder.value = null;
};
</script>

<template>
  <div class="p-6 max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-center text-blue-600">Órdenes de Venta</h1>

    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por cliente, estado, ID, etc..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition-all duration-300"
      />
    </div>

    <div v-if="isLoading" class="text-center text-gray-600 animate-pulse">Cargando órdenes...</div>
    <div v-else-if="error" class="text-center text-red-500">Error al cargar las órdenes.</div>

    <OrderTable v-else :orders="paginatedOrders" :onViewDetails="viewOrderDetails" />

    <div class="flex justify-between items-center mt-6">
      <button
        @click="prevPage"
        :disabled="currentPage === 1"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        Anterior
      </button>
      <span class="text-gray-700">Página {{ currentPage }} de {{ totalPages }}</span>
      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        Siguiente
      </button>
    </div>

    <div v-if="selectedOrder" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-2xl w-96 animate-fadeIn">
        <h2 class="text-2xl font-bold text-indigo-600 mb-4">Orden #{{ selectedOrder.id }}</h2>
        <p class="text-gray-700"><strong>Cliente:</strong> {{ selectedOrder.partner_id?.[1] || "Desconocido" }}</p>
        <p class="text-gray-700"><strong>Fecha:</strong> {{ selectedOrder.date_order }}</p>
        <p class="text-gray-700"><strong>Estado:</strong> {{ selectedOrder.state }}</p>
        <p class="text-gray-700"><strong>Total:</strong> S/. {{ selectedOrder.amount_total }}</p>
        <button
          class="mt-4 w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all duration-300"
          @click="closeOrderDetails"
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>