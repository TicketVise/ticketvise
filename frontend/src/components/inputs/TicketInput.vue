<script>
import { onMounted, ref, h } from 'vue'

import Prism from 'prismjs'

import Editor from '@toast-ui/editor'
import '@toast-ui/editor/dist/toastui-editor.css'

import 'prismjs/themes/prism.css'
import '@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight.css'

import codeSyntaxHighlight from '@toast-ui/editor-plugin-code-syntax-highlight/dist/toastui-editor-plugin-code-syntax-highlight-all.js'

import {LatexPlugin, createFormulaButton} from './latex'

export default {
  props: {
    modelValue: {
      type: String,
      required: false,
      default: ''
    }
  },
  setup (_, { emit, expose }) {
    const editor = ref()

    let e = null

    onMounted(() => {
      e = new Editor({
        el: editor.value,
        height: '300px',
        usageStatistics: false,
        initialEditType: 'wysiwyg',
        previewStyle: 'vertical',
        plugins: [[codeSyntaxHighlight, { highlighter: Prism }], LatexPlugin],
        events: {
          change: () => emit('update:modelValue', e.getMarkdown())
        },
        toolbarItems: [
          ['heading', 'bold', 'italic', 'strike'],
          ['hr', 'quote'],
          ['ul', 'ol', 'task', 'indent', 'outdent'],
          ['table', 'link'],
          ['code', 'codeblock']
        ]
      })

      e.insertToolbarItem({ groupIndex: 1, itemIndex: 2 }, {
        el: createFormulaButton(e),
        tooltip: 'Insert formula block',
        className: 'katex mathnormal',
      });
      
    })

    expose({
      setMarkdown: (markdown) => {
        e.setMarkdown(markdown)
      }
    })

    return () => h('div', {
      ref: editor
    })
  }
}
</script>
