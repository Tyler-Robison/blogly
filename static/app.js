function randcolors(){
    const homepageDivs = document.querySelectorAll('.homepage-div')
    const divArray = Array.from(homepageDivs)

    for (let i = 0; i < divArray.length; i++){
        const color1 = Math.floor(Math.random() * 155);
        const color2 = Math.floor(Math.random() * 155);
        const color3 = Math.floor(Math.random() * 155);
        divArray[i].style.backgroundColor = `rgb(${color1}, ${color2}, ${color3})`
    }
}

randcolors()