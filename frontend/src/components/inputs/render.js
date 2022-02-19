import katex from 'katex'
import 'katex/dist/katex.min.css'


export const HTMLRenderer = {
    latex(node) {
      const html = katex.renderToString(node.literal, {
        displayMode: false,
        outpuyt: 'html'
      });

      return [
        { type: 'openTag', tagName: 'div', outerNewLine: true },
        { type: 'html', content: html },
        { type: 'closeTag', tagName: 'div', outerNewLine: true }
      ];
    },
  }