<script setup lang="ts">
import { defineProps } from "vue";

interface Order {
  id: number;
  name: string;
  date_order: string;
  state: string;
  partner_id: [number, string] | null;
  amount_total: number;
}

const props = defineProps<{ orders: Order[]; onViewDetails: (order: Order) => void }>();
</script>

<template>
  <div class="overflow-x-auto bg-white shadow-md rounded-lg">
    <table class="min-w-full border border-gray-200">
      <thead>
        <tr class="bg-blue-500 text-white">
          <th class="border p-3 text-left">ID</th>
          <th class="border p-3 text-left">Cliente</th>
          <th class="border p-3 text-left">Fecha</th>
          <th class="border p-3 text-left">Estado</th>
          <th class="border p-3 text-left">Total</th>
          <th class="border p-3 text-left">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in props.orders" :key="order.id" class="hover:bg-gray-100">
          <td class="border p-3">{{ order.id }}</td>
          <td class="border p-3">{{ order.partner_id?.[1] || "Desconocido" }}</td>
          <td class="border p-3">{{ order.date_order }}</td>
          <td class="border p-3 capitalize">
            <span
              class="px-3 py-1 rounded-full text-white"
              :class="{
                'bg-green-500': order.state === 'sale',
                'bg-yellow-500': order.state === 'draft',
                'bg-red-500': order.state === 'cancel',
              }"
            >
              {{ order.state }}
            </span>
          </td>
          <td class="border p-3 font-bold">S/. {{ order.amount_total }}</td>
          <td class="border p-3">
            <button class="bg-blue-500 text-white px-3 py-1 rounded-lg" @click="props.onViewDetails(order)">
              Ver Detalles
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
