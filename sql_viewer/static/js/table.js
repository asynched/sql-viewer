function handleQueryClick() {
  const query = localStorage.getItem("sql-viewer:document") || ""
  postForm({
    location: window.location.pathname,
    parameters: [
      {
        name: 'query',
        value: query,
      }
    ]
  })
}

function postForm({ location, parameters, method = 'post' }) {
  const form = document.createElement('form')
  form.method = method
  form.action = location

  for (const { name, value } of parameters) {
    const hiddenField = document.createElement('input')

    hiddenField.type = 'hidden'
    hiddenField.name = name
    hiddenField.value = value

    form.appendChild(hiddenField)
  }

  document.body.appendChild(form)
  form.submit()
}

const editor = CodeMirror.fromTextArea(document.querySelector('textarea'), {
  lineNumbers: true,
  height: '100%',
  mode: 'sql',
  theme: 'dracula',
})

editor.setValue(localStorage.getItem("sql-viewer:document") || "")

editor.on("change", (editor) => {
  const line = editor.doc.children[0].lines.map(line => line.text).join('\n')
  localStorage.setItem("sql-viewer:document", line)
})