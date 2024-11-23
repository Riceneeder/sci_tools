<script setup>
import PublicFileListItem from './PublicFileListItem.vue';
const props = defineProps({
    files: Array,
})
</script>

<template>
    <n-list hoverable>
        <template #header>
            Public Files
        </template>
        <template v-for="file in props.files">
            <PublicFileListItem :fileName="file" />
        </template>
        <template v-if="props.files.length == 0">
            <n-empty size="tiny" description="空空如也" />
        </template>
    </n-list>
</template>