<script setup lang="ts">
import { defineProps, onMounted, ref } from "vue";

interface Order {
  id: number;
  name: string;
  date_order: string;
  state: string;
  partner_id: [number, string] | null;
  amount_total: number;
}

const props = defineProps<{ orders: Order[]; onViewDetails: (order: Order) => void }>();

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);
};

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('es-PE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount);
};

const stateLabels: Record<string, string> = {
  'sale': 'Confirmado',
  'draft': 'Borrador',
  'cancel': 'Cancelado',
};

const isLoaded = ref(false);

onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true;
  }, 100);
});
</script>

<template>
  <div class="overflow-hidden bg-white shadow-xl rounded-xl border border-gray-200 transition-all duration-500 transform hover:shadow-2xl">
    <div class="relative overflow-hidden bg-gradient-to-r from-blue-600 to-indigo-700 p-6">
      <div class="absolute top-0 left-0 w-full h-full opacity-10">
        <div class="absolute top-0 left-0 w-20 h-20 bg-white rounded-full transform -translate-x-10 -translate-y-10"></div>
        <div class="absolute bottom-0 right-0 w-32 h-32 bg-white rounded-full transform translate-x-16 translate-y-16"></div>
      </div>
      <div class="relative">
        <h2 class="text-2xl font-bold text-white tracking-wide flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Órdenes de Venta
        </h2>
        <p class="text-blue-100 mt-1 opacity-80">
          {{ props.orders.length }} órdenes encontradas
        </p>
      </div>
    </div>

    <div class="relative overflow-x-auto">
      <div class="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-white to-transparent pointer-events-none z-10"></div>
      <div class="absolute left-0 top-0 bottom-0 w-8 bg-gradient-to-r from-white to-transparent pointer-events-none z-10"></div>
      
      <table class="min-w-full">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-200">
            <th class="py-4 px-6 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">ID</th>
            <th class="py-4 px-6 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
            <th class="py-4 px-6 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
            <th class="py-4 px-6 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Estado</th>
            <th class="py-4 px-6 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Total</th>
            <th class="py-4 px-6 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(order, index) in props.orders" 
            :key="order.id" 
            class="border-b border-gray-100 hover:bg-blue-50 transition-colors duration-300"
            :class="{'opacity-0 translate-y-4': !isLoaded, 'opacity-100 translate-y-0': isLoaded}" 
            :style="{
              transitionDelay: `${index * 70}ms`,
              transitionDuration: '500ms',
              transitionProperty: 'all'
            }"
          >
            <td class="py-4 px-6 text-gray-800 whitespace-nowrap">
              <span class="bg-blue-50 text-blue-700 py-1 px-3 rounded-lg font-medium">#{{ order.id }}</span>
            </td>
            <td class="py-4 px-6 text-gray-800 whitespace-nowrap">
              <div class="flex items-center">
                <div class="h-9 w-9 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold shadow-md">
                  {{ order.partner_id?.[1].charAt(0).toUpperCase() || "?" }}
                </div>
                <div class="ml-3">
                  <p class="font-medium">{{ order.partner_id?.[1] || "Desconocido" }}</p>
                </div>
              </div>
            </td>
            <td class="py-4 px-6 text-gray-600 whitespace-nowrap">
              {{ formatDate(order.date_order) }}
            </td>
            <td class="py-4 px-6 whitespace-nowrap">
              <span
                class="px-4 py-1.5 rounded-full text-xs font-semibold flex items-center w-fit"
                :class="{
                  'bg-green-100 text-green-700 border border-green-200': order.state === 'sale',
                  'bg-yellow-100 text-yellow-700 border border-yellow-200': order.state === 'draft',
                  'bg-red-100 text-red-700 border border-red-200': order.state === 'cancel',
                }"
              >
                <span class="w-2 h-2 rounded-full mr-2"
                  :class="{
                    'bg-green-500': order.state === 'sale',
                    'bg-yellow-500': order.state === 'draft',
                    'bg-red-500': order.state === 'cancel',
                  }"
                ></span>
                {{ stateLabels[order.state] || order.state }}
              </span>
            </td>
            <td class="py-4 px-6 font-bold text-gray-800 whitespace-nowrap">
              S/. {{ formatCurrency(order.amount_total) }}
            </td>
            <td class="py-4 px-6 whitespace-nowrap">
              <button 
                class="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition-all duration-300 transform hover:scale-105 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 flex items-center"
                @click="props.onViewDetails(order)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                Ver Detalles
              </button>
            </td>
          </tr>
          
          <tr v-if="props.orders.length === 0">
            <td colspan="6" class="py-8 text-center text-gray-500 italic">
              <div class="flex flex-col items-center justify-center space-y-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <p>No hay órdenes disponibles para mostrar</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="py-4 px-6 bg-gray-50 border-t border-gray-100 text-right">
      <p class="text-sm text-gray-500">
        Total registros: <span class="font-semibold text-blue-600">{{ props.orders.length }}</span>
      </p>
    </div>
  </div>
</template>