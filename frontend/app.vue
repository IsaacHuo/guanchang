<template>
  <div class="min-h-screen bg-slate-50 flex font-sans text-slate-800">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col fixed inset-y-0 shadow-xl z-20">
      <div class="h-16 flex items-center px-6 border-b border-slate-700 bg-slate-900">
        <h1 class="text-xl font-bold flex items-center tracking-wide">
          <span class="text-indigo-400 mr-2">✦</span><span class="text-white">Guan</span><span class="font-light text-slate-400">Chang</span>档案
        </h1>
      </div>
      <nav class="flex-1 overflow-y-auto py-6 px-4 space-y-2">
        <a href="#" @click.prevent="showSearchModal = false" :class="!showSearchModal ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'" class="flex items-center px-3 py-2.5 rounded-lg transition">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          全局大盘看板
        </a>
        <a href="#" @click.prevent="showSearchModal = true" :class="showSearchModal ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'" class="flex items-center px-3 py-2.5 rounded-lg transition">
          <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          官员库查询
        </a>
      </nav>
      <div class="px-4 py-4 text-xs text-slate-500 border-t border-slate-700 text-center">
        全自动图谱抽取系统 v1.0
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-64 min-h-screen">
      <header class="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between shadow-sm sticky top-0 z-10">
        <h2 class="text-xl font-medium text-slate-800">深度数据看板</h2>
        <div class="flex items-center space-x-4">
          <span class="flex h-3 w-3 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
          </span>
          <span class="text-sm font-medium text-indigo-600">全网数据监控中</span>
        </div>
      </header>

      <div class="p-8 space-y-6" v-show="!showSearchModal">
        <!-- Stats Top row -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-sm p-6 border border-slate-100 flex items-center">
            <div class="bg-indigo-50 p-3 rounded-lg"><svg class="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5V4H2v16h5m10 0v-5m0 5H7m10 0a2 2 0 002-2v-5a2 2 0 00-2-2H7a2 2 0 00-2 2v5a2 2 0 002 2m0 0v-5"></path></svg></div>
            <div class="ml-5">
              <p class="text-sm font-medium text-slate-500">已收录官员</p>
              <h3 class="text-2xl font-bold text-slate-800">{{ stats.officials ?? 0 }} <span class="text-sm font-normal text-slate-400 ml-1">人</span></h3>
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-sm p-6 border border-slate-100 flex items-center">
            <div class="bg-blue-50 p-3 rounded-lg"><svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg></div>
            <div class="ml-5">
              <p class="text-sm font-medium text-slate-500">职务节点数</p>
              <h3 class="text-2xl font-bold text-slate-800">{{ stats.positions ?? 0 }} <span class="text-sm font-normal text-slate-400 ml-1">职</span></h3>
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-sm p-6 border border-slate-100 flex items-center">
            <div class="bg-emerald-50 p-3 rounded-lg"><svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg></div>
            <div class="ml-5">
              <p class="text-sm font-medium text-slate-500">组织机构数</p>
              <h3 class="text-2xl font-bold text-slate-800">{{ stats.organizations ?? 0 }} <span class="text-sm font-normal text-slate-400 ml-1">处</span></h3>
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-sm p-6 border border-slate-100 flex items-center">
            <div class="bg-red-50 p-3 rounded-lg"><svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg></div>
            <div class="ml-5">
              <p class="text-sm font-medium text-slate-500">落马/违纪事件</p>
              <h3 class="text-2xl font-bold text-slate-800">{{ stats.events ?? 0 }} <span class="text-sm font-normal text-slate-400 ml-1">起</span></h3>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Recent Officials List -->
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 lg:col-span-1 flex flex-col h-[600px]">
            <div class="px-6 py-5 border-b border-slate-100">
              <h3 class="text-lg font-bold text-slate-800 tracking-wide">最近查处官员库</h3>
            </div>
            <div class="flex-1 overflow-y-auto p-4 space-y-3">
              <div v-for="official in officials" :key="official.name" @click="openProfile(official.name)" class="p-4 rounded-lg bg-slate-50 border border-slate-100 hover:shadow-md transition cursor-pointer hover:border-indigo-300">
                <div class="flex justify-between items-start mb-2">
                  <h4 class="font-bold text-indigo-900 text-lg">{{ official.name }}</h4>
                  <span v-if="official.investigations?.length > 0" class="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full font-medium">已落马</span>
                  <span v-else class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full font-medium">履历图谱</span>
                </div>
                <p class="text-xs text-slate-500 mb-2 font-medium">{{ official.gender }} | {{ official.birth_date || '年龄不详' }} {{ official.identifier ? '| '+official.identifier : '' }}</p>
                
                <div class="mt-3">
                  <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">曾任职务：</span>
                  <p class="text-sm text-slate-700 mt-1 line-clamp-2">
                     <span v-for="title in official.titles" class="mr-2 mb-1 inline-block text-xs bg-slate-200 text-slate-700 px-2 py-0.5 rounded">{{ title }}</span>
                  </p>
                </div>
              </div>
              <div v-if="officials.length === 0" class="text-center py-8 text-slate-500">
                 数据全自动化采集链路启动中...
              </div>
            </div>
          </div>

          <!-- Neo4j Graph View -->
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 lg:col-span-2 flex flex-col h-[600px]">
            <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center">
              <h3 class="text-lg font-bold text-slate-800 tracking-wide">Neo4j 共事关联分析图谱 
                 <span class="ml-3 text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-1 rounded-full">可拖拉缩放 · 点击人物节点查阅档案</span>
              </h3>
              <button @click="refreshData" class="flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-800 transition">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                手动更新大屏
              </button>
            </div>
            <div class="flex-1 w-full bg-slate-900 rounded-b-xl relative overflow-hidden" ref="chartContainer">
               <div ref="chartRef" class="w-full h-full absolute inset-0"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Search View -->
      <div class="p-8 space-y-6" v-show="showSearchModal">
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 class="text-xl font-bold text-slate-800 mb-4">全库搜索</h3>
          <div class="flex space-x-3 mb-6">
            <input type="text" v-model="searchQuery" @keyup.enter="searchOfficials" placeholder="输入官员姓名、职务或特征关键字..." class="flex-1 border border-slate-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
            <button @click="searchOfficials" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2.5 rounded-lg font-medium transition flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              搜索
            </button>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-600">
              <thead class="text-xs text-slate-700 uppercase bg-slate-50 border-b border-slate-200">
                <tr>
                  <th class="px-6 py-3 font-semibold">姓名/性别/年龄</th>
                  <th class="px-6 py-3 font-semibold">主要职务关联</th>
                  <th class="px-6 py-3 font-semibold">违纪事件</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="official in searchResults" :key="official.name" @click="openProfile(official.name)" class="border-b border-slate-100 hover:bg-slate-50 cursor-pointer">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="font-bold text-indigo-900 text-base mb-1 hover:text-indigo-600">{{ official.name }}</div>
                    <div class="text-slate-500 text-xs">{{ official.gender || '未知' }} | {{ official.birth_date || '年龄不详' }}</div>
                    <div v-if="official.identifier" class="text-slate-400 text-xs mt-1">{{ official.identifier }}</div>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex flex-wrap gap-1">
                      <span v-for="title in official.titles" :key="title" class="inline-block text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded">{{ title }}</span>
                      <span v-if="!official.titles || official.titles.length === 0" class="text-slate-400">无记录</span>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex flex-wrap gap-1">
                      <span v-for="event in official.investigations" :key="event" class="inline-block text-xs bg-red-50 text-red-700 px-2 py-1 rounded" :title="event">{{ event.substring(0, 20) }}{{ event.length > 20 ? '...' : '' }}</span>
                      <span v-if="!official.investigations || official.investigations.length === 0" class="text-green-600">正常履职</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="searchResults.length === 0 && hasSearched">
                  <td colspan="3" class="px-6 py-8 text-center text-slate-500">未找到匹配的官员档案记录</td>
                </tr>
                <tr v-if="searchResults.length === 0 && !hasSearched">
                  <td colspan="3" class="px-6 py-8 text-center text-slate-500">请输入关键字并开始搜索</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <!-- Profile Modal (Archive Style) -->
    <div v-if="showProfileModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex justify-center items-center p-4">
      <div class="bg-[#fdfbf6] rounded-sm shadow-2xl w-full max-w-4xl h-[85vh] flex flex-col relative border border-[#e5dfc5] overflow-hidden" 
           style="background-image: url('data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.8\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100\' height=\'100\' filter=\'url(%23noise)\' opacity=\'0.04\'/%3E%3C/svg%3E');">
        
        <!-- Top Tape/Sticker effect -->
        <div class="absolute -top-3 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-yellow-900/20 backdrop-blur-md rotate-[-2deg] shadow-sm z-10"></div>
        
        <!-- Header -->
        <div class="px-8 py-6 border-b-2 border-dashed border-[#dcd3b6] flex justify-between items-start relative bg-white/40">
          <div>
            <div class="text-[#8c7a52] text-xs font-bold tracking-[0.2em] mb-1">GUANCHANG ARCHIVES · NO.{{ String(Math.floor(Math.random() * 90000) + 10000) }}</div>
            <h2 class="text-3xl font-black text-[#2c2820] tracking-wider">{{ selectedProfile?.name }} <span class="text-lg font-medium text-[#7a6b4a] ml-2 font-serif">{{ selectedProfile?.gender }} | {{ selectedProfile?.birth_date || '年龄不详' }}</span></h2>
            <p class="text-[#8c7a52] text-sm mt-2 font-serif font-medium">{{ selectedProfile?.identifier || '无特定识别码' }}</p>
          </div>
          <button @click="showProfileModal = false" class="text-[#8c7a52] hover:text-[#5a4d31] transition rounded-full p-2 hover:bg-[#ebdca6]/50">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
          
          <!-- Stamp Effect -->
          <div v-if="selectedProfile?.events?.length > 0" class="absolute right-20 top-4 transform rotate-12 opacity-80 pointer-events-none">
            <div class="border-4 border-[#c81e1e] text-[#c81e1e] font-black text-2xl px-3 py-1 rounded-sm uppercase tracking-widest" style="box-shadow: inset 0 0 0 2px #c81e1e; font-family: 'STKaiti', serif;">
              已落马
            </div>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-8 grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Timeline View (Left 2 cols) -->
          <div class="md:col-span-2 relative">
            <h3 class="text-lg font-bold text-[#4a4230] mb-6 flex items-center border-b border-[#dcd3b6] pb-2">
              <svg class="w-5 h-5 mr-2 text-[#8c7a52]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              升迁与履历轨线
            </h3>
            
            <div class="relative border-l-2 border-[#dcd3b6] ml-3 pl-6 space-y-8 font-serif">
              <div v-for="(career, idx) in selectedProfile?.career" :key="idx" class="relative">
                <div class="absolute -left-[31px] mt-1 w-4 h-4 rounded-full border-2 border-[#fdfbf6] bg-[#8c7a52] shadow-sm"></div>
                <div class="bg-white/60 p-4 rounded shadow-sm border border-[#e1d8b9]">
                  <div class="text-[#8c7a52] text-xs font-bold mb-1 flex justify-between">
                    <span>{{ career.start_date || '未知年份' }} - {{ career.end_date || '至今' }}</span>
                  </div>
                  <h4 class="text-[#2c2820] font-bold text-base mb-1">{{ career.organization || '未知机构' }}</h4>
                  <p class="text-[#5a4d31] font-medium">{{ career.title }}</p>
                </div>
              </div>
              <div v-if="!selectedProfile?.career?.length" class="text-[#8c7a52]">暂无结构化履历记录。</div>
            </div>
          </div>

          <!-- Events and Tags (Right 1 col) -->
          <div class="space-y-6">
            <div v-if="selectedProfile?.events?.length > 0" class="bg-[#fffdfa] border-2 border-[#c81e1e]/20 p-5 rounded-sm relative shadow-sm">
              <div class="absolute top-0 left-0 w-1 h-full bg-[#c81e1e]"></div>
              <h3 class="text-[#c81e1e] font-black tracking-wider text-base mb-4 flex items-center">
                <svg class="w-4 h-4 mr-2 text-[#c81e1e]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                纪委/监察通报重点
              </h3>
              <ul class="space-y-3 font-serif">
                <li v-for="(evt, idx) in selectedProfile.events" :key="idx" class="text-[#5a4d31] text-sm leading-relaxed border-b border-[#c81e1e]/10 pb-3 last:border-0 last:pb-0">
                  <div class="text-[#c81e1e]/60 text-xs font-bold mb-1">{{ evt.date || '通报日期不详' }}</div>
                  {{ evt.description }}
                </li>
              </ul>
            </div>
            
            <div class="bg-white/40 border border-[#dcd3b6] p-5 rounded-sm shadow-sm">
               <h3 class="text-[#4a4230] font-bold text-sm tracking-wider mb-4">履历知识标签库</h3>
               <div class="flex flex-wrap gap-2">
                 <span v-for="title in selectedProfile?.career?.slice(0,6)" :key="title.title" class="px-2 py-1 bg-[#ebdca6]/30 text-[#5a4d31] text-xs font-bold rounded-sm border border-[#dcd3b6]">
                    {{ title.title.length > 5 ? title.title.substring(0,5)+'..' : title.title }}
                 </span>
                 <span v-if="selectedProfile?.events?.length > 0" class="px-2 py-1 bg-[#c81e1e]/10 text-[#c81e1e] text-xs font-bold rounded-sm border border-[#c81e1e]/30">落马人员</span>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, shallowRef, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
const chartInstance = shallowRef(null)
const stats = ref({})
const officials = ref([])
const showSearchModal = ref(false)
const showProfileModal = ref(false)
const selectedProfile = ref(null)
const searchQuery = ref('')
const searchResults = ref([])
const hasSearched = ref(false)
let timer = null

const fetchStats = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/dashboard/stats')
    if(res.ok) stats.value = await res.json()
  } catch (err) {}
}

const fetchOfficialsList = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/officials/recent')
    if(res.ok) {
       const data = await res.json()
       officials.value = data.officials
    }
  } catch (err) {}
}
const searchOfficials = async () => {
  if (!searchQuery.value.trim()) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/officials/search?query_name=${encodeURIComponent(searchQuery.value)}`)
    if(res.ok) {
       const data = await res.json()
       searchResults.value = data.officials || []
       hasSearched.value = true
    }
  } catch (err) {}
}

const openProfile = async (name) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/officials/profile/${encodeURIComponent(name)}`)
    if(res.ok) {
       selectedProfile.value = await res.json()
       showProfileModal.value = true
    }
  } catch (err) {}
}

const fetchGraph = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/graph/network')
    if(res.ok) {
       const data = await res.json()
       renderChart(data)
    }
  } catch (err) {}
}

const refreshData = async () => {
  await Promise.all([fetchStats(), fetchOfficialsList(), fetchGraph()])
}

const renderChart = (data) => {
  if (!chartInstance.value && chartRef.value) {
    chartInstance.value = echarts.init(chartRef.value, 'dark') // Using dark theme for ECharts
  }
  if (!chartInstance.value) return

  const option = {
    backgroundColor: 'transparent',
    tooltip: { formatter: '{b}' },
    animationDurationUpdate: 2000,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: data.nodes.map(n => ({
          id: n.id,
          name: n.name || n.id,
          symbolSize: n.category === 'Official' ? 60 : (n.category === 'Position' ? 35 : (n.category === 'Event' ? 45 : 30)),
          category: n.category,
          itemStyle: {
            color: n.category === 'Official' ? '#818cf8' : 
                   (n.category === 'Event' ? '#f87171' : 
                   (n.category === 'Organization' ? '#34d399' : '#fbbf24')),
            shadowBlur: 20,
            shadowColor: n.category === 'Official' ? '#818cf8' : 'rgba(0,0,0,0)'
          }
        })),
        links: data.links.map(l => ({
          source: l.source,
          target: l.target,
          label: {
            show: true,
            formatter: l.label,
            fontSize: 9,
            color: '#94a3b8'
          },
          lineStyle: { color: '#475569', curveness: 0.2, width: 2 }
        })),
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}',
          color: '#e2e8f0',
          fontWeight: 'bold',
          fontSize: 14
        },
        force: {
          repulsion: 800,
          edgeLength: 120,
          gravity: 0.1,
          friction: 0.1
        }
      }
    ]
  };

  chartInstance.value.setOption(option);
  
  // Single click listener for nodes
  chartInstance.value.off('click');
  chartInstance.value.on('click', function(params) {
    if (params.dataType === 'node' && params.data.category === 'Official') {
      openProfile(params.data.id);
    }
  });
}

onMounted(() => {
  refreshData()
  
  window.addEventListener('resize', () => {
    chartInstance.value?.resize()
  })
  
  // 每 10 秒自动轮询一次，用来静默展示后台爬虫的工作进度
  timer = setInterval(refreshData, 10000)
})

onUnmounted(() => {
  if(timer) clearInterval(timer)
})
</script>
<style>
/* For deep customized dark theme scrollbar matching */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>