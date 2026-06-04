<template>
  <div class="flex flex-col gap-5 p-6 bg-charcoal-800 rounded-xl border border-charcoal-700 shadow-xl w-full">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex flex-col">
        <span class="text-xs uppercase tracking-wider text-charcoal-400 font-bold">Team Workload</span>
        <span class="text-xs text-charcoal-300 font-medium">Active task allocations per Project Manager</span>
      </div>
      <!-- Legends -->
      <div class="hidden sm:flex items-center gap-3 text-[10px] uppercase font-bold text-charcoal-400">
        <div class="flex items-center gap-1">
          <span class="w-2.5 h-2.5 bg-gray-500 rounded"></span>
          <span>Todo</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2.5 h-2.5 bg-orange-500 rounded"></span>
          <span>In Progress</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2.5 h-2.5 bg-indigo-500 rounded"></span>
          <span>Review</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2.5 h-2.5 bg-emerald-500 rounded"></span>
          <span>Done</span>
        </div>
      </div>
    </div>

    <!-- Rows for PMs -->
    <div class="flex flex-col gap-4 max-h-60 overflow-y-auto custom-scrollbar pr-1">
      <div 
        v-for="pm in data" 
        :key="pm.name" 
        class="flex flex-col gap-1.5 p-2 rounded-lg hover:bg-charcoal-700/30 transition-colors duration-200"
      >
        <!-- Title and count -->
        <div class="flex items-center justify-between text-xs text-white font-semibold">
          <span class="truncate max-w-[150px] font-bold">{{ pm.name }}</span>
          <span class="text-[10px] text-charcoal-400">
            {{ pm.done }}/{{ pm.total }} Completed ({{ calculatePercentage(pm.done, pm.total) }}%)
          </span>
        </div>

        <!-- Stacked Progress Bar -->
        <div class="w-full bg-charcoal-900 h-3 rounded-full flex overflow-hidden">
          <div 
            v-if="pm.todo > 0" 
            :style="{ width: `${(pm.todo / pm.total) * 100}%` }" 
            class="h-full bg-gray-500 transition-all duration-500 ease-out" 
            title="Todo"
          ></div>
          <div 
            v-if="pm.in_progress > 0" 
            :style="{ width: `${(pm.in_progress / pm.total) * 100}%` }" 
            class="h-full bg-orange-500 transition-all duration-500 ease-out" 
            title="In Progress"
          ></div>
          <div 
            v-if="pm.review > 0" 
            :style="{ width: `${(pm.review / pm.total) * 100}%` }" 
            class="h-full bg-indigo-500 transition-all duration-500 ease-out" 
            title="Under Review"
          ></div>
          <div 
            v-if="pm.done > 0" 
            :style="{ width: `${(pm.done / pm.total) * 100}%` }" 
            class="h-full bg-emerald-500 transition-all duration-500 ease-out" 
            title="Completed"
          ></div>
        </div>

        <!-- Micro counts list under row on smaller screens -->
        <div class="flex gap-3 text-[10px] font-bold text-charcoal-400 mt-0.5">
          <span v-if="pm.todo > 0" class="text-gray-400">Todo: {{ pm.todo }}</span>
          <span v-if="pm.in_progress > 0" class="text-orange-400">Work: {{ pm.in_progress }}</span>
          <span v-if="pm.review > 0" class="text-indigo-400">Review: {{ pm.review }}</span>
          <span v-if="pm.done > 0" class="text-emerald-400">Done: {{ pm.done }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const calculatePercentage = (done, total) => {
  if (!total || total === 0) return 0
  return Math.round((done / total) * 100)
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}
</style>
