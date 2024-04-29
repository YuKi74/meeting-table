<template>
    <div>
        <div class="top">
            语言：
            <a-select
                placeholder="请选择"
                style="width: 120px"
                @change="changeLanguage"
            >
                <a-select-option
                    v-for="(key, value, index) in sets.language"
                    :key="index"
                    :value="value"
                >
                    {{ value }}
                </a-select-option>
            </a-select>
            样式风格：
            <a-select
                placeholder="请选择"
                style="width: 120px"
                @change="changeTheme"
            >
                <a-select-option
                    v-for="(key, value, index) in sets.theme"
                    :key="index"
                    :value="value"
                >
                    {{ value }}
                </a-select-option>
            </a-select>
        </div>

        <div>
            <monaco-editor
                ref="monaco"
                :opts="opts"
                :height="600"
                :connection="connection"
                :id="id"
                :content="content"
            />
        </div>
    </div>
</template>
<script>
import MonacoEditor from './MonacoEditor.vue';
import { Select } from 'ant-design-vue';
export default {
    props: ['connection', 'id', 'content'],
    components: {
        MonacoEditor,
        ASelect: Select,
        ASelectOption: Select.Option,
    },
    data() {
        return {
            sets: {
                language: {
                    apex: 'apex',
                    azcli: 'azcli',
                    bat: 'bat',
                    c: 'c',
                    clojure: 'clojure',
                    coffeescript: 'coffeescript',
                    cpp: 'cpp',
                    csharp: 'csharp',
                    csp: 'csp',
                    css: 'css',
                    dockerfile: 'dockerfile',
                    fsharp: 'fsharp',
                    go: 'go',
                    graphql: 'graphql',
                    handlebars: 'handlebars',
                    html: 'html',
                    ini: 'ini',
                    java: 'java',
                    javascript: 'javascript',
                    json: 'json',
                    kotlin: 'kotlin',
                    less: 'less',
                    lua: 'lua',
                    markdown: 'markdown',
                    msdax: 'msdax',
                    mysql: 'mysql',
                    'objective-c': 'objective-c',
                    pascal: 'pascal',
                    perl: 'perl',
                    pgsql: 'pgsql',
                    php: 'php',
                    plaintext: 'plaintext',
                    postiats: 'postiats',
                    powerquery: 'powerquery',
                    powershell: 'powershell',
                    pug: 'pug',
                    python: 'python',
                    r: 'r',
                    razor: 'razor',
                    redis: 'redis',
                    redshift: 'redshift',
                    ruby: 'ruby',
                    rust: 'rust',
                    sb: 'sb',
                    scheme: 'scheme',
                    scss: 'scss',
                    shell: 'shell',
                    sol: 'sol',
                    sql: 'sql',
                    st: 'st',
                    swift: 'swift',
                    tcl: 'tcl',
                    typescript: 'typescript',
                    vb: 'vb',
                    xml: 'xml',
                    yaml: 'yaml',
                },
                theme: {
                    vs: 'vs',
                    'vs-dark': 'vs-dark',
                    'hc-black': 'hc-black',
                },
            },
            opts: {
                value: '',
                theme: 'vs-dark',
                roundedSelection: false,
                autoIndent: true,
                unusualLineTerminators: 'off',
                language: 'javascript',
            },
        };
    },
    methods: {
        changeLanguage(val) {
            this.opts.language = val;
        },
        changeTheme(val) {
            this.opts.theme = val;
        },
    },
};
</script>
<style>
.top {
    background-color: var(--white);
    margin-left: 10px;
}
</style>
