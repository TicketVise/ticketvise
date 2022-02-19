import katex from 'katex'
import 'katex/dist/katex.min.css'

export const LatexPlugin = function() {
    return {
        toolbarItems: [
            {
                groupIndex: 0,
                itemIndex: 3,
                item: {
                    name: 'Formula',
                    tooltip: 'Insert formula block',
                    command: 'latex',
                    text: 'f',
                    className: 'toastui-editor-toolbar-icons',
                    style: { backgroundImage: 'none', color: 'red' }
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