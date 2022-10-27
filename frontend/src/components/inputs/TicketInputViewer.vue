<script>
import { onMounted, ref, h } from 'vue'

import Prism from 'prismjs'

import Viewer from '@toast-ui/editor/dist/toastui-editor-viewer'
import '@toast-ui/editor/dist/toastui-editor.css'

import 'prismjs/themes/prism.css'
import '@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css'

import codeSyntaxHighlight from '@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight-all.js'
import {LatexPlugin} from './latex'

export default {
  props: {
    modelValue: {
      type: String,
      required: false,
      default: ''
    },
    content: {
      type: String,
      required: false,
      default: ''
    }
  },
  setup (props, { emit }) {
    const viewer = ref()

    onMounted(() => {
      const e = new Viewer({
        el: viewer.value,
        initialValue: props.content,
        usageStatistics: false,
        plugins: [[codeSyntaxHighlight, { highlighter: Prism }], LatexPlugin],
        events: {
          change: () => emit('update:modelValue', e.getMarkdown())
        },
      })
    })

    return () => h('div', {
      ref: viewer
    })
  }
}
</script>
