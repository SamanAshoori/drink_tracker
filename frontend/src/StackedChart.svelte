<script>
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    export let data = [];

    let canvas;
    let chartInstance;

    // Generate a consistent color from the drink name
    function stringToColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        const c = (hash & 0x00ffffff).toString(16).toUpperCase();
        return "#" + "00000".substring(0, 6 - c.length) + c;
    }

    // Transform backend data to Chart.js format
    function processData(rawData) {
        if (!rawData || rawData.length === 0)
            return { labels: [], datasets: [] };

        // 1. Get Dates (X Axis)
        // We assume rawData is like [{date: '2023-10-01', RedBull: 1.50}, ...]
        const labels = rawData.map((d) => d.date);

        // 2. Get Drink Names (Keys that are not 'date')
        // We look at the first row to determine what drinks exist
        const keys = Object.keys(rawData[0]).filter((k) => k !== "date");

        // 3. Create Datasets
        const datasets = keys.map((key) => ({
            label: key,
            data: rawData.map((d) => d[key]),
            backgroundColor: stringToColor(key),
            stack: "Stack 0", // Forces all bars into one column per day
        }));

        return { labels, datasets };
    }

    onMount(() => {
        const ctx = canvas.getContext("2d");

        chartInstance = new Chart(ctx, {
            type: "bar",
            data: processData(data),
            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false,
                },
                scales: {
                    x: { stacked: true },
                    y: {
                        stacked: true,
                        ticks: {
                            callback: function (value) {
                                return "£" + value;
                            },
                        },
                    },
                },
                plugins: {
                    tooltip: {
                        displayColors: true,
                        backgroundColor: "rgba(0,0,0,0.7)",

                        callbacks: {
                            // Format the individual rows (e.g., "Red Bull: £1.50")
                            label: function (context) {
                                let label = context.dataset.label || "";
                                if (label) {
                                    label += ": ";
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat("en-GB", {
                                        style: "currency",
                                        currency: "GBP",
                                    }).format(context.parsed.y);
                                }
                                return label;
                            },

                            footer: function (tooltipItems) {
                                let sum = 0;

                                // Because interaction mode is 'index', tooltipItems contains
                                // data for every drink on this day, not just the one you hovered.
                                tooltipItems.forEach(function (tooltipItem) {
                                    sum += tooltipItem.parsed.y;
                                });

                                return "Day Total: £" + sum.toFixed(2);
                            },
                        },
                    },
                },
            },
        });

        return () => {
            if (chartInstance) chartInstance.destroy();
        };
    });

    // Reactivity: Update chart when 'data' prop changes
    $: if (chartInstance && data.length > 0) {
        chartInstance.data = processData(data);
        chartInstance.update();
    }
</script>

<div class="chart-container">
    <canvas bind:this={canvas}></canvas>
</div>

<style>
    .chart-container {
        position: relative;
        height: 300px;
        width: 100%;
        margin-top: 2rem;
    }
</style>
