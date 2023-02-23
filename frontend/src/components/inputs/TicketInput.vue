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
    },
    staff: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  setup (_, { emit, expose }) {
    const editor = ref()

    let e = null

    onMounted(() => {
      e = new Editor({
        el: editor.value,
        minHeight: '300px',
        height: 'auto',
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
      },
      registerKeyUp: (staff) => {
        e.on('keyup', (editorType, ev) => {
          if (ev.key === '@') {
            const popup = document.createElement('ul')
            popup.classList = 'z-10 mt-1 max-h-60 overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm'
            const items = []
            for (const user of staff) {
              items.push(`
                <li class="select-none py-2 pl-3 pr-9 text-gray-900 cursor-pointer hover:bg-primary-50 w-full" data-value="${user.username}">
                  <div class="flex items-center" data-value="${user.username}">
                    <img src="${user.avatar}" alt="" class="h-6 w-6 flex-shrink-0 rounded-full" data-value="${user.username}">
                    <span class="ml-3 truncate" data-value="${user.username}">${user.name}</span>
                  </div>
                </li>
              `)
            }

            for (const item of items) {
              popup.innerHTML += item
            }

            popup.addEventListener('mousedown', (ev) => {
              const text = ev.target.dataset.value
              const [start, end] = e.getSelection()

              e.replaceSelection(`${text} `, [start[0], start[1] - 1], end)
            })

            e.addWidget(popup, 'bottom')
          }
        })
      }
    })

    return () => h('div', {
      ref: editor
    })
  }
}
</script>
