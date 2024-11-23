<script setup>
import FileList from './FileList.vue';
import PublicFileList from './PublicFileList.vue';
import { ref, getCurrentInstance } from "vue";

const appGlobalProperties = getCurrentInstance().appContext.config.globalProperties;
const WsEvents = appGlobalProperties.$wsEvents;
const wsClient = appGlobalProperties.$wsClient;
const apiClient = appGlobalProperties.$apiClient;

const pdfFiles = ref([]);
const markdownFiles = ref([]);
const publicFiles = ref([]);

const loadFiles = async (type) => {
    try {
        let res;
        switch (type) {
            case 'pdf':
                res = await apiClient.Get.pdf_list();
                pdfFiles.value = res.data;
                break;
            case 'markdown':
                res = await apiClient.Get.md_list();
                markdownFiles.value = res.data;
                break;
            case 'public':
                res = await apiClient.Get.public_list();
                publicFiles.value = res.data;
                break;
        }
    } catch (error) {
        console.error(`Error loading ${type} files:`, error);
    }
};

const init = async () => {
    await loadFiles('pdf');
    await loadFiles('markdown');
    await loadFiles('public');
};

init();

wsClient.on(WsEvents.PUBLIC_CHANGE, () => {
    loadFiles('public');
});
wsClient.on(WsEvents.PDF_CHANGE, () => {
    loadFiles('pdf');
});
wsClient.on(WsEvents.MD_CHANGE, () => {
    loadFiles('markdown');
});
</script>

<template>
    <n-thing id="files_area">
        <n-page-header subtitle="所有上传到服务器的文件">
            <template #title>
                文件区域
            </template>
        </n-page-header>
        <PublicFileList :files="publicFiles" />
        <FileList :files="pdfFiles" type="pdf" />
        <FileList :files="markdownFiles" type="md" />
    </n-thing>
</template>

<style scoped>
#files_area {
    padding: 16px;
}
</style>