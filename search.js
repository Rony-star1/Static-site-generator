function searchPosts() {
    let input = document.getElementById('searchInput');
    let filter = input.value.toUpperCase();
    let ul = document.getElementById('postList');
    let li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        let h3 = li[i].getElementsByTagName('h3')[0];
        let txtValue = h3.textContent || h3.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}
