import pandas as pd
from flask import Response
from core.config import CSV_FILE


def dashboard():
    return """
    <html>
    <head>
        <title>AI Emotion Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

       <style>
body {
    background:#0f172a;
    color:white;
    text-align:center;
    font-family:Arial;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
    margin-top: 20px;
}

canvas {
    background:#1e293b;
    padding:10px;
    border-radius:10px;
}
</style>

    </head>
    <body>

        <h2>🤖 Emotion Analytics Dashboard</h2>

        <div class="container">
            <canvas id="pie" width="220" height="220"></canvas>
            <canvas id="bar" width="420" height="240"></canvas>
        </div>

        <script>

        let pieChart = new Chart(document.getElementById('pie'), {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor:["#22c55e","#ef4444","#3b82f6","#facc15"]
                }]
            }
        });

        let barChart = new Chart(document.getElementById('bar'), {
            type: 'bar',
            data: {
                labels: [],
                datasets: []
            }
        });

        async function load(){

            // ===== PIE =====
            const res = await fetch('/stats');
            const data = await res.json();

            pieChart.data.labels = Object.keys(data);
            pieChart.data.datasets[0].data = Object.values(data);
            pieChart.update();

            // ===== BAR =====
            const res2 = await fetch('/timeline');
            const timeline = await res2.json();

            const labels = Object.keys(timeline);
            const emotions = Object.keys(timeline[labels[0]] || {});

            const datasets = emotions.map(e => ({
                label: e,
                data: labels.map(l => timeline[l][e] || 0)
            }));

            barChart.data.labels = labels;
            barChart.data.datasets = datasets;
            barChart.update();
        }

        setInterval(load, 3000);
        load();

        </script>
    </body>
    </html>
    """


# ================= APIs =================

def stats():
    try:
        df = pd.read_csv(CSV_FILE)
        return df["emotion"].value_counts().to_dict()
    except:
        return {}


def timeline():
    try:
        df = pd.read_csv(CSV_FILE)

        df['time'] = pd.to_datetime(df['time'])
        df['minute'] = df['time'].dt.strftime('%H:%M')

        grouped = df.groupby(['minute', 'emotion']).size().unstack(fill_value=0)
        grouped = grouped.tail(30)

        return grouped.to_dict()
    except:
        return {}
