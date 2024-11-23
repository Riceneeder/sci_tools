<script setup>
import FunctionalArea from './components/FunctionalArea.vue';
import LogsArea from './components/LogsArea.vue';
import FilesArea from './components/FilesArea.vue';
</script>

<template>
    <n-split direction="horizontal" style="height: 100vh;" :max="0.55" :min="0.35">
        <template #1>
            <FilesArea />
        </template>
        <template #2>
            <LogsArea />
            <FunctionalArea />
        </template>
    </n-split>


</template>

<style scoped></style>
