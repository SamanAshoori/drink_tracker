<script>
  import { onMount } from 'svelte';
  import StackedChart from '../lib/StackedChart.svelte';
  import PieChart from '../lib/PieChart.svelte';
  import Heatmap from '../lib/Heatmap.svelte';

  let history = [];
  let stats = { total_ml: 0, total_caffeine: 0, total_spent: 0, drink_count: 0 };
  let stackedData = [];
  let brandDistributionData = { labels: [], data: [] };

  onMount(async () => {
    await Promise.all([loadStats(), loadHistory(), loadStackedChart(), loadBrandDistribution()]);
  });

  async function loadStats() {
    const res = await fetch('/api/stats');
    stats = await res.json();
  }

  async function loadHistory() {
    const res = await fetch('/api/consumptions');
    history = await res.json();
  }

  async function loadStackedChart() {
    const stackRes = await fetch('/api/charts/stacked');
    stackedData = await stackRes.json();
  }

  async function loadBrandDistribution() {
    const res = await fetch('/api/charts/brand-distribution');
    brandDistributionData = await res.json();
  }
</script>

<main>
  <header>
    <h1>Drink<span>Tracker</span>_</h1> 
  </header>

  <div class="stats-row">
    <div class="card stat-card">
      <h3 class="stat-number">{(stats.total_caffeine / 1000).toFixed(2)}<span class="unit">g</span></h3>
      <p>Caffeine</p>
    </div>
    <div class="card stat-card">
      <h3 class="stat-number">£{stats.total_spent.toFixed(2)}</h3>
      <p>Spent</p>
    </div>
    <div class="card stat-card">
      <h3 class="stat-number">{stats.drink_count}</h3>
      <p>Cans</p>
    </div>
  </div>

  <div class="charts-grid">
    <div class="card">
      <h2>Spending History</h2>
      {#if stackedData.length > 0} <StackedChart data={stackedData} /> {/if}
    </div>
    <div class="card">
      <h2>Brand Distribution</h2>
      {#if brandDistributionData.labels && brandDistributionData.labels.length > 0}
        <PieChart data={brandDistributionData} />
      {/if}
    </div>
  </div> 

  <div class="card heatmap-container">
    <Heatmap data={history} />
  </div>  

  <div class="card history-card">
    <h2>Recent History</h2>
    {#if history.length === 0}
      <p>No drinks logged yet.</p>
    {:else}
      <ul class="history-list">
        {#each history as entry}
          <li>
            <span class="drink-name">{entry.drink_display_name}</span>
            <span class="date"> - {new Date(entry.consumed_at).toLocaleDateString()}</span>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</main>

<style>
  /* The Container */
  main {
    max-width: 900px; /* Slightly wider to fit side-by-side charts */
    margin: 4rem auto;
    padding: 0 1.5rem;
  }

  /* Header */
  header {
    margin-bottom: 3rem;
    border-bottom: 1px solid #222;
    padding-bottom: 1rem;
  }

  h1 {
    font-size: 2rem;
    color: white;
  }

  h1 span {
    color: var(--accent-primary);
  }

  h2 {
    font-size: 1rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1rem;
  }

  /* The Card Base */
  .card {
    background: var(--bg-card);
    border: var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }
  
  .card:hover {
    border-color: #333;
  }

  /* KPI ROW (One Line) */
  .stats-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-card {
    flex: 1; /* Makes them equal width */
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .stat-card p {
    color: var(--text-muted);
    text-transform: uppercase;
    font-size: 0.8rem;
    margin: 0;
  }

  .stat-number {
    font-size: 2rem;
    color: white;
    margin: 0 0 0.5rem 0;
  }

  .unit {
    font-size: 1rem;
    color: var(--accent-primary);
  }

  /* 5. CHARTS GRID (Side by Side) */
  .charts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Forces 50% split */
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  /* Heatmap */
  .heatmap-container {
    margin-bottom: 2rem;
    display: flex;
    justify-content: center;
  }

  /* History (Centered) */
  .history-card {
    text-align: center;
  }

  .history-list {
    list-style: none; /* Remove bullets */
    padding: 0;
    margin: 0;
  }

  .history-list li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #111;
    color: var(--text-main);
  }

  .drink-name {
    font-weight: 600;
  }

  .date {
    color: var(--text-muted);
    font-size: 0.9rem;
  }

  /* Mobile Responsive: Stack charts on small screens */
  @media (max-width: 600px) {
    .charts-grid {
      grid-template-columns: 1fr;
    }
  }
</style>