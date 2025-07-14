function plotCurves(data) {
    const maturities = data.maturities;

    const zc_trace = {
        x: maturities,
        y: data.zc_curve,
        type: 'scatter',
        name: 'Taux ZC (%)',
        line: { color: '#17BECF' }
    };

    const act_trace = {
        x: maturities,
        y: data.actuarial_curve,
        type: 'scatter',
        name: 'Taux Actuariel (%)',
        line: { color: '#FF7F0E' }
    };

    const layout = {
        title: '📈 Courbes Interpolées',
        xaxis: { title: 'Maturité (années)' },
        yaxis: { title: 'Taux (%)' }
    };

    Plotly.newPlot('rate-curves', [zc_trace, act_trace], layout);

    // Forward curve
    const fw = data.forwards;
    const fw_trace = {
        x: fw.end,
        y: fw.rates,
        type: 'scatter',
        name: 'Taux Forward (%)',
        line: { color: '#2ca02c' }
    };

    const fw_layout = {
        title: '📈 Courbe des Taux Forwards',
        xaxis: { title: 'À (années)' },
        yaxis: { title: 'Taux (%)' }
    };

    Plotly.newPlot('forward-curve', [fw_trace], fw_layout);
}

async function handleForm(url, formData) {
    const res = await fetch(url, {
        method: 'POST',
        body: formData
    });

    const data = await res.json();

    if (data.error) {
        alert(\"❌ \" + data.error);
    } else {
        plotCurves(data);
    }
}

document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    handleForm('/process_csv', formData);
});

document.getElementById('bam-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    handleForm('/process_bam', formData);
});
