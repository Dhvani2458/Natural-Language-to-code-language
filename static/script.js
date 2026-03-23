async function convertCode() {
    const input = document.getElementById("inputText").value;

    const response = await fetch("/convert", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: input })
    });

    const data = await response.json();
    const outputBox = document.getElementById("outputText");

    if (data.success) {
        outputBox.innerText = data.output;
    } else {
        outputBox.innerText = "❌ Error: " + data.output;
    }
}

function clearText() {
    document.getElementById("inputText").value = "";
    document.getElementById("outputText").innerText = "";
}