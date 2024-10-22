saveButtons = document.querySelectorAll('.save-button')

saveButtons.forEach(button => {
    console.log(button)
    button.form.addEventListener('submit', e => {
        e.target.lastElementChild.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>'
    })
})