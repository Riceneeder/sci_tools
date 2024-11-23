<script setup>
import { ref, watchEffect, nextTick, getCurrentInstance } from "vue";

const appglobalProperties = getCurrentInstance().appContext.config.globalProperties;
const WsEvents = appglobalProperties.$wsEvents;
const wsClient = appglobalProperties.$wsClient;

const log = ref('🙆等待任务');
const logs = ref([]);
const logContainer = ref(null);

wsClient.on(WsEvents.LOG_MESSAGE, (message) => {
  logs.value.push(message.data);
  log.value = logs.value.join('\n');
});

watchEffect(() => {
  if (logs.value.length) {
    nextTick(() => {
      logContainer.value?.scrollTo({ position: "bottom", silent: true });
    });
  }
});
</script>

<template>
  <n-thing id="logs_area">
    <n-page-header subtitle="服务器返回的工作日志">
      <template #title>
        日志区域
      </template>
    </n-page-header>
    <n-log id="log" ref="logContainer" :log="log" trim />
  </n-thing>
</template>

<style scoped>
#logs_area {
    padding: 16px;
}
#log {
    background-color: rgba(0, 0, 0, 0.4);
    color: white;
    padding-left: 5px;
}
</style>