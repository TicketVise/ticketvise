<template>
  <toast-editor v-if="!isViewer" :options="options" initialEditType="wysiwyg" previewStyle="tab" :initialValue="initialValue"
                ref="toastUIEditor"/>
  <toast-viewer v-else :options="options" :initialValue="initialValue" ref="toastUIEditor"/>
</template>

<script>
import {Editor, Viewer} from '@toast-ui/vue-editor';
import codeSyntaxHighlight from '@toast-ui/editor-plugin-code-syntax-highlight';
import hljs from 'highlight.js/lib/core';
import javascript from 'highlight.js/lib/languages/javascript';
import c from 'highlight.js/lib/languages/c-like';
import go from 'highlight.js/lib/languages/go';
import haskell from 'highlight.js/lib/languages/haskell';
import java from 'highlight.js/lib/languages/java';
import bash from 'highlight.js/lib/languages/bash';
import python from 'highlight.js/lib/languages/python';
import json from 'highlight.js/lib/languages/json';
import xml from 'highlight.js/lib/languages/xml';
import php from 'highlight.js/lib/languages/php';
import sql from 'highlight.js/lib/languages/sql';
import erlang from 'highlight.js/lib/languages/erlang';
import prolog from 'highlight.js/lib/languages/prolog';
import latex from 'highlight.js/lib/languages/latex';

import '@toast-ui/editor/dist/toastui-editor.css';
import '@toast-ui/editor/dist/toastui-editor-viewer.css';
import 'codemirror/lib/codemirror.css';
import 'highlight.js/styles/github.css';

hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('c', c);
hljs.registerLanguage('erlang', erlang);
hljs.registerLanguage('go', go);
hljs.registerLanguage('haskell', haskell);
hljs.registerLanguage('java', java);
hljs.registerLanguage('bash', bash);
hljs.registerLanguage('prolog', prolog);
hljs.registerLanguage('python', python);
hljs.registerLanguage('json', python);
hljs.registerLanguage('xml', python);
hljs.registerLanguage('php', php);
hljs.registerLanguage('sql', sql);
hljs.registerLanguage('latex', latex);

export default {
  name: "Editor",
  components: {
    "toast-editor": Editor,
    "toast-viewer": Viewer,
  },
  props: {
    isViewer: false,
    initialValue: "",
  },
  data() {
    return {
      replyEditor: "",
      staff: [],
      options: {
        usageStatistics: false,
        plugins: [[codeSyntaxHighlight, { hljs }]]
      }
    }
  },
  methods: {
    getContent() {
      return this.$refs.toastUIEditor.invoke('getMarkdown');
    },
    clear() {
      this.$refs.toastUIEditor.invoke('setMarkdown', '');
    }
  }
}
</script>

<style scoped>

</style>