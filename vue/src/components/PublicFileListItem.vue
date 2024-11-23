<script setup>
import { getCurrentInstance } from 'vue'
const props = defineProps({
    fileName: String
})
const appGlobalProperties = getCurrentInstance().appContext.config.globalProperties;
const apiClient = appGlobalProperties.$apiClient;

const deleteFile = (fileName) => {
    apiClient.Delete.public_file(fileName)
}

const downloadFile = (fileName) => {
    apiClient.Get.download_public_file(fileName)
}
</script>

<template>
    <n-list-item>
        <template #prefix>
            <v-icon name="vi-file-type-markdown" />
        </template>
        <n-thing :title="props.fileName" />
        <template #suffix>
            <n-button-group>
                <n-button text @click="() => downloadFile(props.fileName)">
                    <template #icon>
                        <v-icon name="md-download" fill="blue" />
                    </template>
                </n-button>
                <n-button text @click="() => deleteFile(props.fileName)">
                    <template #icon>
                        <v-icon name="md-delete" fill="red" />
                    </template>
                </n-button>
            </n-button-group>
        </template>
    </n-list-item>
</template>