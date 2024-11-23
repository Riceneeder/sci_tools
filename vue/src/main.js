import { createApp } from 'vue'
import App from './App.vue'

import WsEvents from '@/js/ws_events'
import WsClient from '@/js/ws_client'
import API from '@/js/api'

import { OhVueIcon, addIcons } from "oh-vue-icons"
import { MdDownload, MdDelete, ViFileTypePdf, ViFileTypeMarkdown, SiGoogletranslate } from "oh-vue-icons/icons"
addIcons(MdDownload, MdDelete, ViFileTypePdf, ViFileTypeMarkdown, SiGoogletranslate)

const Url = "/";
const wsClient = new WsClient(Url);
wsClient.connect();

const app = createApp(App)
app.config.globalProperties.$wsEvents = WsEvents;
app.config.globalProperties.$wsClient = wsClient;
app.config.globalProperties.$apiClient = API;
app.component("v-icon", OhVueIcon)
app.mount('#app')

