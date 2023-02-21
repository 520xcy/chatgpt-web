import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { LayuiVueResolver } from 'unplugin-vue-components/resolvers'
const vue = require('@vitejs/plugin-vue')


export default {
    plugins: [
        vue(),
        AutoImport({
            resolvers: [LayuiVueResolver()],
        }),
        Components({
            resolvers: [
                LayuiVueResolver({
                    /**
                     * 将样式与组件一起导入
                     *
                     * @default 'css'
                     */
                    // importStyle: boolean | 'css',
                    /**
                     * 是否解析图标
                     *
                     * @default false
                     */
                    resolveIcons: true,
                    /**
                     * 排除不需要自动导入的组件
                     * 
                     * eg: exclude: ['LayDocTable', /^LayDoc[A-Z]/,]
                     */
                    // exclude?: Array<string | RegExp>;
                }),
            ],
        }),
    ],
    build: {
        base: './',
        sourcemap: false,
        outDir: '../templates', //指定输出路径
        assetsDir: 'public', // 指定生成静态资源的存放路径
        // rollupOptions: {
        //     output: {
        //         manualChunks(id) {
        //             if (id.includes('node_modules')) {
        //                 const arr = id.toString().split('node_modules/')[1].split('/')
        //                 switch (arr[0]) {
        //                     case '@vue':
        //                     case '@layui/layui-vue':
        //                         return '_' + arr[0]
        //                         break
        //                     default:
        //                         return '__vendor'
        //                         break
        //                 }
        //             }
        //         }
        //     }
        // }
    },

}