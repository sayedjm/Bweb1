function toggleAbstract(key) {
    var abstractDiv = document.getElementById('abstract_' + key);
    abstractDiv.style.display = (abstractDiv.style.display === 'none') ? 'block' : 'none';
}