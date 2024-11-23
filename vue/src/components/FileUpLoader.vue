<script setup>
import { getCurrentInstance } from 'vue'
const props = defineProps({
    fileType: String,
})
const appGlobalProperties = getCurrentInstance().appContext.config.globalProperties;
const apiClient = appGlobalProperties.$apiClient;
const customRequest = async ({ file }) => {
    const formData = new FormData();
    formData.append('file', file.file);
    await apiClient.Post.upload(props.fileType, formData)
}
</script>

<template>
    <n-upload multiple directory-dnd :custom-request="customRequest"
        :accept="props.fileType == 'md' ? '.md, .markdown' : '.pdf'">
        <n-upload-dragger>
            <n-text style="font-size: 16px">
                点击或者拖动文件到该区域来上传
            </n-text>
            <n-p depth="3" style="margin: 8px 0 0 0">
                允许上传的文件类型：{{ props.fileType == 'md' ? '.md, .markdown' : '.pdf' }}
            </n-p>
        </n-upload-dragger>
    </n-upload>
</template>
