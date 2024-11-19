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
