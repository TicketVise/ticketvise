import katex from 'katex'
import 'katex/dist/katex.min.css'

export const createFormulaButton = function(editor) {
    const button = document.createElement('button');

    button.className = 'toastui-editor-toolbar-icons last';
    button.style.backgroundImage = 'none';
    button.style.margin = '0';
    button.style.font = 'normal 1.21em KaTeX_Math,Times New Roman,serif';
    button.innerHTML = '<i>f</i>';
    button.type = "button"
    button.addEventListener('click', () => {
      // If nothing is selected, populate with simple formula.
      const [start, end] = editor.getSelection();
      if (start == end) {
        editor.replaceSelection("E=mc^2", start, end);
      }

      editor.exec('customBlock', { info: 'latex' });
    });

    return button;
}

export const LatexPlugin = function() {
    return {
        toHTMLRenderers: {
            latex(node) {
              const html = katex.renderToString(node.literal, {
                displayMode: true,
                output: 'html'
              });
        
              return [
                { type: 'openTag', tagName: 'div', outerNewLine: true },
                { type: 'html', content: html },
                { type: 'closeTag', tagName: 'div', outerNewLine: true }
              ];
            },
        }
    }
}