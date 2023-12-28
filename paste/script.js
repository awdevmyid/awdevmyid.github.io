CodeMirror.modeURL = 'https://cdn.jsdelivr.net/npm/codemirror@5.58.1/mode/%N/%N.js';

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("paste-wrapper").focus();

    let inFrame = window.location !== window.parent.location;
    editor = new CodeMirror(document.getElementById('paste-wrapper'), {
        lineNumbers: true,
        theme: 'one-dark',
        lineWrapping: true,
        readOnly: inFrame,
    });

    if (inFrame) {
        document.getElementById('defaultNav').style.display = 'none';
        document.getElementById('copyUrlNav').style.display = 'none';
        document.getElementById('iFrameNav').style.display = 'block';
    }

    if (l = new URLSearchParams(window.location.search).get('l')) {
        let lang = getModeMime(l);
        editor.setOption('mode', lang.mime);
        CodeMirror.autoLoadMode(editor, lang.mode);
        document.getElementById('langInput').value = l.toLowerCase();
    } else {
        document.getElementById('langInput').value = 'plain text';
    }

    let base64 = location.hash.substring(1);
    if (base64.length == 0) return;

    if (!fetch) {
        alert("This page is not supported by your browser");
        return;
    }

    fetch("data:application/octet-stream;base64," + base64).then(r => r.blob()).then(function (blob) {
        let fr = new FileReader();
        fr.onload = function () {
            let compressed = Array.from(new Uint8Array(fr.result));
            LZMA.decompress(compressed, function (text, error) {
                if (error) {
                    alert("Failed to decompress: " + error);
                    return;
                }

                editor.setValue(text);
            });
        };
        fr.readAsArrayBuffer(blob);
    });
});

function langInputChanged() {
    if (lang = getModeMime(document.getElementById('langInput').value)) {
        editor.setOption('mode', lang.mime);
        CodeMirror.autoLoadMode(editor, lang.mode);
        document.getElementById('langInput').value = lang.name.toLowerCase();
    } else {
        document.getElementById('langInput').value = 'plain text'
    }
}

function generateUrl() {
    let plaintext = editor.getValue();
    let lang = document.getElementById('langInput').value;
    console.log("Generating Url...")
    LZMA.compress(plaintext, 1, function (compressed, error) {
        if (error) {
            alert("Failed to compress: " + error);
            return;
        }

        let fr = new FileReader();
        fr.onload = function () {
            let base64 = fr.result.substring(fr.result.indexOf(",") + 1);
            let url = "https://" + location.host + location.pathname + "?l=" + lang + "#" + base64;
            console.log(url);

            showCopyNav(url);
        };

        fr.readAsDataURL(new Blob([new Uint8Array(compressed)]));
    });
}

function showCopyNav(url) {
    document.getElementById('defaultNav').style.display = 'none';
    document.getElementById('copyUrlNav').style.display = 'block';
    document.getElementById('copyUrl').value = url;
}

function copyUrl() {
    let copyText = document.getElementById('copyUrl');
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
    cancelUrl();
}

function cancelUrl() {
    document.getElementById('defaultNav').style.display = 'block';
    document.getElementById('copyUrlNav').style.display = 'none';
    document.getElementById('copyUrl').value = '';
}

function toggleLineWrap() {
    editor.setOption('lineWrapping', !editor.getOption('lineWrapping'));
}

function openInTab() {
    window.open(location);
}

function getModeMime(name) {
    name = name.toLowerCase();
    for (let i in CodeMirror.modeInfo) {
        if (CodeMirror.modeInfo[i].name.toLowerCase() === name)
            return CodeMirror.modeInfo[i];
    }

    return null;
}

