<script setup>
import { getCurrentInstance, ref } from 'vue'
import FileUpLoader from './FileUpLoader.vue';

const appGlobalProperties = getCurrentInstance().appContext.config.globalProperties;
const apiClient = appGlobalProperties.$apiClient;

/**
 * @enum {string}
 * @readonly
 */
const FunctionalArea = Object.freeze({
    MDTRANSLATE: 'MDTRANSLATE',
    SCI_PDF2MD: 'SCI_PDF2MD',
})

const selectedFunctionalArea = ref(FunctionalArea.MDTRANSLATE);
const translateOptions = ref({
    from: 'en',
    to: 'zh',
})

const submitTask = async () => {
    if (selectedFunctionalArea.value === FunctionalArea.MDTRANSLATE) {
        await apiClient.Post.mdtranslate(translateOptions.value.from, translateOptions.value.to);
    } else if (selectedFunctionalArea.value === FunctionalArea.SCI_PDF2MD) {
        await apiClient.Post.sci_pdf2md();
    }
}
</script>

<template>
    <n-thing id="functional_area">
        <n-page-header subtitle="上传和操作服务器的文件">
            <template #title>
                功能区域
            </template>
        </n-page-header>
        <n-flex vertical>
            <FileUpLoader v-if="selectedFunctionalArea === FunctionalArea.MDTRANSLATE" fileType="md" />
            <FileUpLoader v-else-if="selectedFunctionalArea === FunctionalArea.SCI_PDF2MD" fileType="pdf" />
            <n-flex justify="center">
                <n-radio-group v-model:value="selectedFunctionalArea" name="radiobuttongroup1">
                    <n-radio-button key="MDTRANSLATE" :value="FunctionalArea.MDTRANSLATE"
                        label="Markdown翻译"></n-radio-button>
                    <n-radio-button key="SCI_PDF2MD" :value="FunctionalArea.SCI_PDF2MD"
                        label="SCI论文PDF转Markdown"></n-radio-button>
                </n-radio-group>
            </n-flex>
            <n-thing>
                <template #header>
                    {{ selectedFunctionalArea === FunctionalArea.MDTRANSLATE ? 'Markdown翻译' : 'SCI论文PDF转Markdown' }}
                </template>
                <template #description>
                    <n-text>
                        {{ selectedFunctionalArea === FunctionalArea.MDTRANSLATE ?
                            '翻译Markdown文件夹下的所有文件，在公共文件夹生成对应.md文件' : '将所有上传的PDF转换合并成一个.md文件' }}
                    </n-text>
                </template>
                <n-input-group v-if="selectedFunctionalArea === FunctionalArea.MDTRANSLATE">
                    <n-input v-model="translateOptions.from" :defaultValue="translateOptions.from"
                        placeholder="源语言（默认en）" />
                    <n-button disabled>
                        <template #icon>
                            <v-icon name="si-googletranslate" />
                        </template>
                    </n-button>
                    <n-input v-model="translateOptions.to" :defaultValue="translateOptions.to"
                        placeholder="目标语言（默认zh）" />
                </n-input-group>
                <template #action>
                    <n-button @click="submitTask">提交任务</n-button>
                </template>
            </n-thing>
        </n-flex>
    </n-thing>

</template>

<style scoped>
#functional_area {
    padding: 16px;
}
</style>