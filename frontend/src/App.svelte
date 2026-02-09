<script>
  import { onMount } from "svelte";
  import StackedChart from "./StackedChart.svelte";

  // State
  let brands = [];
  let drinks = [];
  let history = [];
  let stats = {
    total_ml: 0,
    total_caffeine: 0,
    total_count: 0,
    total_spent: 0.0,
  };
  let StackedData = []; // This will hold the data for the stacked chart

  async function loadStackedChart() {
    const res = await fetch("http://127.0.0.1:8000/api/charts/stacked");
    StackedData = await res.json();
  }

  // Form Data
  let selectedBrandId = "";
  let flavour = "";
  let size = 250;
  let caffeinedensity = 32; // Red Bull has ~32mg/100ml

  // Load data on startup
  onMount(async () => {
    await loadBrands();
    await loadDrinks();
    await loadHistory();
    await loadStats();
    await loadStackedChart();
  });

  async function loadBrands() {
    const res = await fetch("http://127.0.0.1:8000/api/brands");
    brands = await res.json();
    // Default to first brand if available
    if (brands.length > 0) selectedBrandId = brands[0].id;
  }

  async function loadDrinks() {
    const res = await fetch("http://127.0.0.1:8000/api/drinks");
    const rawData = await res.json();

    //add temp log price
    drinks = rawData.map((x) => ({ ...x, log_price: 0.0 }));
  }

  async function handleSubmit() {
    const payload = {
      brand_id: parseInt(selectedBrandId),
      flavour: flavour,
      size_ml: size,
      caffeine_per_100ml: caffeinedensity,
    };

    const res = await fetch("http://127.0.0.1:8000/api/drinks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      await loadDrinks(); // Refresh list
      flavour = ""; // Reset form slightly
    } else {
      alert("Error saving drink");
    }
  }

  async function loadHistory() {
    const res = await fetch("http://127.0.0.1:8000/api/consumptions");
    history = await res.json();
  }

  async function logDrink(drink) {
    const payload = {
      drink_id: drink.id,
      price_paid: drink.log_price || 0.0, // Use log_price if set, otherwise default to 0
    };
    const res = await fetch("http://127.0.0.1:8000/api/consumptions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      await loadHistory();
      await loadStats(); // Refresh stats
      await loadStackedChart(); // Refresh stacked chart
    } else {
      alert("Error logging drink");
    }
  }

  async function loadStats() {
    const res = await fetch("http://127.0.0.1:8000/api/stats");
    stats = await res.json();
  }
</script>

<main>
  <h1>Drink Manager</h1>

  <div class="card">
    <h2>Spending History</h2>
    {#if StackedData.length > 0}
      <StackedChart data={StackedData} />
    {:else}
      <p>No spending data available.</p>
    {/if}
  </div>

  <div class="card">
    <h2>Add New Drink</h2>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="row">
        <label
          >Brand:
          <select bind:value={selectedBrandId}>
            {#each brands as brand}
              <option value={brand.id}>{brand.name}</option>
            {/each}
          </select>
        </label>
      </div>

      <div class="row">
        <label
          >Flavour: <input
            type="text"
            bind:value={flavour}
            required
            placeholder="e.g. Tropical"
          /></label
        >
      </div>

      <div class="row">
        <label>Size (ml): <input type="number" bind:value={size} /></label>
        <label
          >Caffeine (mg/100ml): <input
            type="number"
            bind:value={caffeinedensity}
          /></label
        >
      </div>

      <button type="submit">Add Drink</button>
    </form>
  </div>

  <div class="card">
    <h2>Drink Library</h2>
    {#if drinks.length === 0}
      <p>No drinks found.</p>
    {:else}
      <ul>
        {#each drinks as drink}
          <li class="drink-row">
            <div class="drink-info">
              <strong>{drink.display_name}</strong>
              <small>({drink.caffeine_per_100ml}mg/100ml)</small>
            </div>

            <div class="drink-actions">
              <span class="currency-symbol">£</span>
              <input
                type="number"
                step="0.01"
                bind:value={drink.log_price}
                class="price-input"
                placeholder="0.00"
              />
              <button on:click={() => logDrink(drink)}>Log</button>
            </div>
          </li>
        {/each}
      </ul>
    {/if}
  </div>

  <div class="card">
    <h2>Consumption History</h2>
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

  <div class="card dashboard">
    <div class="stat">
      <h3>{stats.total_ml / 1000} L</h3>
      <p>Liquid Total</p>
    </div>
    <div class="stat">
      <h3>£{stats.total_spent.toFixed(2)}</h3>
      <p>Money Spent</p>
    </div>
    <div class="stat">
      <h3>{stats.drink_count}</h3>
      <p>Total Cans</p>
    </div>
  </div>
</main>

<style>
  main {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
    font-family: sans-serif;
  }
  .card {
    border: 1px solid #ddd;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
  }
  .row {
    margin-bottom: 1rem;
    display: flex;
    gap: 1rem;
  }
  label {
    display: block;
    width: 100%;
  }
  input,
  select {
    width: 100%;
    padding: 0.5rem;
    margin-top: 0.25rem;
  }
  button {
    background: #000;
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    border-radius: 4px;
  }
  ul {
    padding-left: 1.2rem;
  }
  li {
    margin-bottom: 0.5rem;
  }

  .drink-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #eee;
  }
  .drink-actions {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .price-input {
    width: 70px;
    padding: 5px;
    margin: 0 !important; /* Override global input margin */
  }
  .currency-symbol {
    font-weight: bold;
    color: #555;
  }
</style>
