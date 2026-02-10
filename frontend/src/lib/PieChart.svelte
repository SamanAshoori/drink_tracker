<script>
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";
    import { getColorForBrand } from "../../utils/colors.js";

    export let data = { labels: [], data: [] };

    let canvas;
    let chartInstance;

    // Transforms the data from our API into the format Chart.js expects
    function processData(rawData) {
        if (!rawData || !rawData.labels || rawData.labels.length === 0) {
            return { labels: [], datasets: [] };
        }

        return {
            labels: rawData.labels,
            datasets: [
                {
                    label: "Drinks Consumed",
                    data: rawData.data,
                    backgroundColor: rawData.labels.map(label => getColorForBrand(label)),
                    hoverOffset: 4, // Makes the hovered segment pop out slightly
                },
            ],
        };
    }

    onMount(() => {
        const ctx = canvas.getContext("2d");

        chartInstance = new Chart(ctx, {
            type: "pie",
            data: processData(data),
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top', // Display brand names above the chart
                    },
                },
            },
        });

        return () => {
            if (chartInstance) chartInstance.destroy();
        };
    });

    // Svelte reactivity: When the 'data' prop changes, update the chart
    $: if (chartInstance && data.labels && data.labels.length > 0) {
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
        margin-top: 1rem;
    }
</style>
