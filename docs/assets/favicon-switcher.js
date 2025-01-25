const setFavicon = (mode) => {
    const link = document.querySelector("link[rel~='icon']") || document.createElement("link")
    link.rel = "icon"
    link.href = mode === "dark" ? "/assets/favicon-light.png" : "/assets/favicon-dark.png"
    document.head.appendChild(link)
}

const updateFavicon = () => {
    const mode = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
    setFavicon(mode)
}

updateFavicon()

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", updateFavicon)