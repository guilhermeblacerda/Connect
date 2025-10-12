document.addEventListener("DOMContentLoaded", () =>{
    
    const lines = document.querySelectorAll('.clickable_line');

    lines.forEach(line => {
        line.addEventListener('click', () => {
            const detail = line.querySelector('div');

            console.log('mfdoom');

        detail.classList.toggle('open_content');
        detail.classList.toggle('close_content');

        })
    })
})

