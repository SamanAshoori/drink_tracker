<script>
  import { onMount } from 'svelte';
  import StackedChart from '../lib/StackedChart.svelte';
  import PieChart from '../lib/PieChart.svelte';
  import Heatmap from '../lib/Heatmap.svelte';

  let history = [];
  let all_history = []
  let stats = { total_ml: 0, total_caffeine: 0, total_spent: 0, drink_count: 0 };
  let stackedData = [];
  let brandDistributionData = { labels: [], data: [] };
  let daily_caffine = 0;
  let selectedDate = new Date().toLocaleDateString('en-CA'); // YYYY-MM-DD format

  // 1. State for the toggle
  let groupBy = 'brand'; 

  onMount(async () => {
    // Pass selectedDate to get the initial daily caffeine amount
    await Promise.all([loadStats(), loadHistory(), getDailyCaffeine(selectedDate),loadAllHistory()]);
    // Load dynamic charts
    await refreshCharts();
  });

  async function refreshCharts(){
    // FIX: Using backticks (`) for string interpolation
    await Promise.all([loadStackedChart(), loadBrandDistribution(), loadAllHistory()]);
  }

  async function toggleGroup(newValue){
    if (groupBy === newValue) return;
    groupBy = newValue;
    
    // Clear data briefly to show "loading" state
    stackedData = [];
    brandDistributionData = { labels: [], data: [] };
    
    await refreshCharts();
  }

  async function loadStats() {
    const res = await fetch('/api/stats');
    stats = await res.json();
  }

  async function getDailyCaffeine(date) {
    const res = await fetch(`/api/stats/daily?date=${date}`);
    daily_caffine = await res.json();
  }


  // When the selectedDate changes, re-fetch the daily caffeine data
  $: if (selectedDate) {
      getDailyCaffeine(selectedDate);
  }

  $: progressPercentage = Math.min((daily_caffine / 400) * 100, 100);
  $: isOverLimit = daily_caffine > 400;

  async function loadHistory() {
    const res = await fetch('/api/consumptions/top_10');
    history = await res.json();
  }

  async function loadAllHistory() {
    const res = await fetch('/api/consumptions');
    all_history = await res.json();
  }

  async function loadStackedChart() {
    // FIX: Using backticks ` `
    const stackRes = await fetch(`/api/charts/stacked?group_by=${groupBy}`);
    stackedData = await stackRes.json();
  }

  async function loadBrandDistribution() {
    // FIX: Using backticks ` `
    const res = await fetch(`/api/charts/brand-distribution?group_by=${groupBy}`);
    brandDistributionData = await res.json();
  }
</script>

<main>
  <header>
    <h1>Energy Drink <span>Tracker</span>_</h1> 
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

  <div class="controls-row">
    <h2>Analytics</h2>
    
    <div class="toggle-pill">
      <button 
        class:active={groupBy === 'brand'} 
        on:click={() => toggleGroup('brand')}>
        Brand
      </button>
      <button 
        class:active={groupBy === 'flavour'} 
        on:click={() => toggleGroup('flavour')}>
        Flavour
      </button>
    </div>
  </div>
    
  <div class="charts-grid">
    <div class="card">
      <h2>Spending History</h2>
      {#if stackedData.length > 0} <StackedChart data={stackedData} /> {/if}
    </div>
    <div class="card">
      <h2>Distribution</h2>
      {#if brandDistributionData.labels && brandDistributionData.labels.length > 0}
        <PieChart data={brandDistributionData} />
      {/if}
    </div>
  </div> 

  <div class="card daily-limit-card">
    <div class="date-selector-container">
      <h2>Daily Limit</h2>
      <input type="date" bind:value={selectedDate} />
    </div>
    
    <div class="progress-bar-container">
      <div
        class="progress-bar-fill"
        style="width: {progressPercentage}%"
        class:over-limit={isOverLimit}
      ></div>
    </div>
    <p>{Math.round(daily_caffine)}mg / 400mg</p>
    <p>400mg is the current reccomendation of caffeine for an adult</p>
  </div>

  <div class="card heatmap-container">
    <Heatmap data={all_history} />
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
            <span class="date"> - {new Date(entry.consumed_at).toLocaleDateString('en-CA')}</span>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</main>

<style>
  /* --- LAYOUT --- */
  main {
    max-width: 900px;
    margin: 4rem auto;
    padding: 0 1.5rem;
  }

  header {
    margin-bottom: 3rem;
    border-bottom: 1px solid #222;
    padding-bottom: 1rem;
  }

  /* --- TYPOGRAPHY --- */
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
    margin: 0; /* Reset default margin */
  }

  /* --- CARDS --- */
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

  /* --- KPI STATS --- */
  .stats-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 3rem; /* More space before charts */
  }

  .stat-card {
    flex: 1;
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

  /* --- CONTROLS (THE TOGGLE) --- */
  .controls-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .toggle-pill {
    display: flex;
    background: var(--bg-card);
    border: 1px solid #333;
    border-radius: 20px;
    padding: 4px;
    gap: 4px;
  }

  .toggle-pill button {
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 6px 16px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: 16px;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .toggle-pill button:hover {
    color: white;
  }

  .toggle-pill button.active {
    background: var(--accent-primary);
    color: black;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
  }

  /* --- CHARTS GRID --- */
  .charts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; 
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  /* --- HEATMAP --- */
  .heatmap-container {
    margin-bottom: 2rem;
    display: flex;
    justify-content: center;
    overflow-x: auto;
  }

  /* --- HISTORY LIST --- */
  .history-card {
    text-align: center;
  }

  .history-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .history-list li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #222; /* Darker line */
    color: var(--text-main);
  }

  .drink-name {
    font-weight: 600;
  }

  .date {
    color: var(--text-muted);
    font-size: 0.9rem;
  }

  /* --- MOBILE --- */
  @media (max-width: 600px) {
    .charts-grid {
      grid-template-columns: 1fr;
    }
  }

  .daily-limit-card {
    margin-bottom: 3rem;
  }

  .daily-limit-card h2 {
    text-align: left;
    margin-bottom: 0; /* Reset */
  }

  .daily-limit-card p {
    margin-top: 1rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    text-align: center;
  }

  .date-selector-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .date-selector-container input[type="date"] {
    background-color: var(--bg-card);
    border: 1px solid #333;
    color: var(--text-main);
    padding: 0.5rem;
    border-radius: var(--radius);
    font-family: inherit;
  }

  .progress-bar-container {
    width: 100%;
    height: 12px;
    background-color: #222;
    border-radius: 6px;
    overflow: hidden;
  }

  .progress-bar-fill {
    height: 100%;
    background-color: var(--accent-primary);
    border-radius: 6px;
    transition: width 0.5s ease-in-out, background-color 0.5s ease;
  }

  .progress-bar-fill.over-limit {
    background-color: #e53e3e; /* Red */
    animation: pulse 1.5s infinite ease-in-out;
  }

  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(229, 62, 62, 0.5); }
    50% { box-shadow: 0 0 0 8px rgba(229, 62, 62, 0); }
  }
</style>