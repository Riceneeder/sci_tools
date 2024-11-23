<script setup>
import {getCurrentInstance } from 'vue'
const props = defineProps({
    fileType: String,
    fileName: String
})
const appGlobalProperties = getCurrentInstance().appContext.config.globalProperties;
const apiClient = appGlobalProperties.$apiClient;

const deleteFile = (fileType, fileName) => {
    switch (fileType) {
        case 'md':
            apiClient.Delete.md_file(fileName)
            break;
        case 'pdf':
            apiClient.Delete.pdf_file(fileName)
            break;
    }
}

</script>

<template>
    <n-list-item>
        <template #prefix>
            <v-icon :name="props.fileType == 'md' ? 'vi-file-type-markdown' : 'vi-file-type-pdf'"/>
        </template>
        <n-thing :title="props.fileName" />
        <template #suffix>
            <n-button text @click="() => deleteFile(props.fileType, props.fileName)">
                <template #icon>
                    <v-icon name="md-delete" fill="red" />
                </template>
            </n-button>
        </template>
    </n-list-item>
</template>