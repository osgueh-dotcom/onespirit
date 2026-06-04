<template>
  <div v-if="warnings.length > 0" class="p-4 bg-brand-orange/10 border border-brand-orange/20 rounded-3xl select-none">
    <div class="flex items-start gap-3">
      <svg class="h-5 w-5 text-brand-orange shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
      </svg>
      <div>
        <h4 class="text-xs font-black text-brand-orange uppercase tracking-wider">Workflow Quality Audits ({{ warnings.length }} Warnings)</h4>
        <ul class="list-disc list-inside text-xs text-gray-300 font-semibold space-y-1.5 mt-2">
          <li v-for="(warn, idx) in warnings" :key="idx">{{ warn }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  warnings: {
    type: Array,
    required: true
  }
})
</script>
