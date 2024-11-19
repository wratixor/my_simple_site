const upd_article = () => {
        input = document.getElementById('article');
        output = document.getElementById('p_article');
        output.innerHTML = input.value;
    }

const upd_img_t = () => {
        input = document.getElementById('curl_img_t');
        output = document.getElementById('p_curl_img_t');
        output.src = '/img/' + input.value
    }

const upd_img = () => {
        input = document.getElementById('curl_img');
        output = document.getElementById('p_curl_img');
        output.src = '/img/' + input.value
    }

const hidden_left = () => {
        left = document.getElementById('left_column');
        right = document.getElementById('right_column');
        left.style.setProperty('display', 'none');
        right.style.setProperty('width', '100%');
    }