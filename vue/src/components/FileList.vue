<script setup>
import FileListItem from './FileListItem.vue';
const props = defineProps({
    files: Array,
    type: String
})
</script>

<template>
    <n-list hoverable>
        <template #header>
            {{ props.type == 'md' ? 'Markdown Files' : 'PDF Files' }}
        </template>
        <template v-for="file in props.files">
            <FileListItem :fileType="props.type" :fileName="file" />
        </template>
        <template v-if="props.files.length == 0">
            <n-empty size="tiny" description="空空如也" />
        </template>
    </n-list>
</template>