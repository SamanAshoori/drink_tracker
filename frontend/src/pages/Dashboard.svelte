<script>
  import { onMount } from 'svelte';
  // Note the new path to lib
  import StackedChart from '../lib/StackedChart.svelte';

  let history = [];
  let stats = { total_ml: 0, total_spent: 0, drink_count: 0 };
  let weeklyData = [];
  let stackedData = [];

  onMount(async () => {
    await Promise.all([loadStats(), loadHistory(), loadCharts()]);
  });

  async function loadStats() {
    const res = await fetch('/api/stats');
    stats = await res.json();
  }

  async function loadHistory() {
    const res = await fetch('/api/consumptions');
    history = await res.json();
  }

  async function loadCharts() {
    const weekRes = await fetch('/api/charts/weekly');
    weeklyData = await weekRes.json();
    
    const stackRes = await fetch('/api/charts/stacked');
    stackedData = await stackRes.json();
  }
</script>

<div class="card dashboard">
  <div class="stat">
    <h3>{stats.total_ml / 1000} L</h3>
    <p>Liquid</p>
  </div>
  <div class="stat">
    <h3>£{stats.total_spent.toFixed(2)}</h3>
    <p>Spent</p>
  </div>
  <div class="stat">
    <h3>{stats.drink_count}</h3>
    <p>Cans</p>
  </div>
</div>

  <div class="card">
    <h2>Spending History</h2>
    {#if stackedData.length > 0} <StackedChart data={stackedData} /> {/if}
  </div>

<div class="card">
  <h2>Recent History</h2>
  {#if history.length === 0}
    <p>No drinks logged yet.</p>
  {:else}
    <ul>
      {#each history as entry}
        <li>
          {entry.drink_display_name}
          <small> - {new Date(entry.consumed_at).toLocaleString()}</small>
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .card { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
  .dashboard { display: flex; justify-content: space-around; text-align: center; background-color: #f9f9f9; }
  .stat h3 { font-size: 2rem; margin: 0; color: #333; }
  .stat p { margin: 0; color: #666; font-size: 0.9rem; }
  ul { padding-left: 1.2rem; }
  li { margin-bottom: 0.5rem; }
  /* Simple grid for charts on larger screens */
  @media (min-width: 768px) {
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  }
</style>