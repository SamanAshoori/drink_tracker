<script>
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";
    import { getColorForBrand } from "../../utils/colors.js";

    export let data = [];

    let canvas;
    let chartInstance;

    // Helper to get the start of the week (Sunday) for a given date string
    function getWeekStartDate(dateString) {
        const date = new Date(dateString);
        const day = date.getDay();
        const diff = date.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
        return new Date(date.setDate(diff)).toISOString().split("T")[0];
    }

    // Transform backend data to Chart.js format
    function processData(rawData) {
        if (!rawData || rawData.length === 0)
            return { labels: [], datasets: [] };

        const weeklyData = {};

        // 1. Group by Week
        rawData.forEach((dailyEntry) => {
            const weekStart = getWeekStartDate(dailyEntry.date);
            if (!weeklyData[weekStart]) {
                weeklyData[weekStart] = { date: weekStart };
            }

            Object.keys(dailyEntry).forEach((key) => {
                if (key !== "date") {
                    if (!weeklyData[weekStart][key]) {
                        weeklyData[weekStart][key] = 0;
                    }
                    weeklyData[weekStart][key] += dailyEntry[key];
                }
            });
        });

        const chartData = Object.values(weeklyData).sort(
            (a, b) => new Date(a.date) - new Date(b.date)
        );

        // 2. Get Dates (X Axis)
        const labels = chartData.map((d) => d.date);

        // 3. Get Brand Names
        const keys = Object.keys(
            chartData.reduce((acc, curr) => ({ ...acc, ...curr }), {})
        ).filter((k) => k !== "date");

        // 4. Create Datasets
        const datasets = keys.map((key) => ({
            label: key,
            data: chartData.map((d) => d[key] || 0), // Use 0 if a brand isn't in a week
            backgroundColor: getColorForBrand(key),
            stack: "Stack 0",
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

                                return "Week Total: £" + sum.toFixed(2);
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
