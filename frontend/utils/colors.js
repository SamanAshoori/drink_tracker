// A map of brand names to specific, manually assigned colors.
// Keys should be lowercase to ensure case-insensitive matching.
const brandColorMap = {
    'purdeys': 'green',
    'red bull': '#00008B', // darkblue
    'celsius': '#EFEFEF',  // A light grey, as bright white is invisible on a white background
};

/**
 * Hashes a string to generate a consistent, but not predefined, color.
 * This is used as a fallback if a brand isn't in the brandColorMap.
 * @param {string} str The string to hash.
 * @returns {string} A hex color code.
 */
function stringToHashColor(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const c = (hash & 0x00ffffff).toString(16).toUpperCase();
    return "#" + "00000".substring(0, 6 - c.length) + c;
}

/**
 * Gets a color for a given brand name.
 * It first checks a predefined map for a specific color.
 * If not found, it generates a consistent color based on the brand name's hash.
 * @param {string} brandName - The name of the brand.
 * @returns {string} A CSS color string.
 */
export function getColorForBrand(brandName) {
    if (!brandName) {
        return '#CCCCCC'; // Return a default grey for undefined names
    }

    const specificColor = brandColorMap[brandName.toLowerCase()];
    return specificColor || stringToHashColor(brandName);
}