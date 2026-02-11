
const brandColorMap = {
    'purdeys': 'green',
    'red bull': '#00008B', 
    'celsius': '#EFEFEF',  
};

function stringToHashColor(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const h = Math.abs(hash) % 360;
    return `hsl(${h}, 80%, 60%)`;
}

export function getColorForBrand(brandName) {
    if (!brandName) {
        return '#CCCCCC'; // Return a default grey for undefined names
    }

    const specificColor = brandColorMap[brandName.toLowerCase()];
    return specificColor || stringToHashColor(brandName);
}