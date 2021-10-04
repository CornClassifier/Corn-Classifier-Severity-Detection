function severity() {
    document.getElementById('severity').classList.add('active');
    document.getElementById('classify').classList.remove('active');

    document.getElementById('severity-result').classList.remove('hidden')
    document.getElementById('classify-result').classList.add('hidden')

    document.getElementById('upload-severity').classList.remove('hidden')
    document.getElementById('upload-classify').classList.add('hidden')

    document.getElementById('img-severe').classList.remove('hidden')
    document.getElementById('img-classify').classList.add('hidden')
}

function classify() {
    document.getElementById('classify').classList.add('active');
    document.getElementById('severity').classList.remove('active');

    document.getElementById('severity-result').classList.add('hidden')
    document.getElementById('classify-result').classList.remove('hidden')

    document.getElementById('upload-severity').classList.add('hidden')
    document.getElementById('upload-classify').classList.remove('hidden')

    document.getElementById('img-severe').classList.add('hidden')
    document.getElementById('img-classify').classList.remove('hidden')
}

function determineTab(tab_name) {
    if(tab_name == 'severe') {
        severity();
        console.log('severe');
    }

    else {
        classify();
        console.log('classify');
    }
}