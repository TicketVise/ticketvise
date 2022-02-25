import katex from 'katex'
import 'katex/dist/katex.min.css'

export const LatexPlugin = function() {
  // text-rendering: auto;
  // font: normal 1.21em KaTeX_Main,Times New Roman,serif;
  // line-height: 1.2;
  // text-indent: 0;
    return {
        toolbarItems: [
            {
                groupIndex: 1,
                itemIndex: 3,
                item: {
                    name: 'Formula',
                    tooltip: 'Insert formula block',
                    command: 'latex',
                    text: 'f',
                    className: 'katex mathnormal',
                    style: { backgroundImage: 'none', font: 'normal 1.21em KaTeX_Math,Times New Roman,serif' }
                }
            }
        ],
        toHTMLRenderers: {
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
        },
        markdownCommands: {
            latex: (payload, { tr, selection, schema }, dispatch) => {
              tr.insertText('$$latex\nE=mc^2\n$$');
              dispatch(tr);
              return true;
            },
          },
          wysiwygCommands: {
            latex: (payload, { tr, selection, schema }, dispatch) => {
                tr.insertText('$$latex\nE=mc^2\n$$');
                dispatch(tr);
                return true;
            },
          },
    }
}


// export const HTMLRenderer = {
//     latex(node) {
//       const html = katex.renderToString(node.literal, {
//         displayMode: false,
//         outpuyt: 'html'
//       });

//       return [
//         { type: 'openTag', tagName: 'div', outerNewLine: true },
//         { type: 'html', content: html },
//         { type: 'closeTag', tagName: 'div', outerNewLine: true }
//       ];
//     },
//   }