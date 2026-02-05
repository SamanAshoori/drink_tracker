<script>
  import { onMount } from 'svelte';

  // State
  let brands = [];
  let drinks = [];
  let history = [];
  
  // Form Data
  let selectedBrandId = "";
  let flavour = "";
  let size = 330;
  let caffeine = 100;

  // Load data on startup
  onMount(async () => {
    await loadBrands();
    await loadDrinks();
    await loadHistory();
  });

  async function loadBrands() {
    const res = await fetch('http://127.0.0.1:8000/api/brands');
    brands = await res.json();
    // Default to first brand if available
    if (brands.length > 0) selectedBrandId = brands[0].id;
  }

  async function loadDrinks() {
    const res = await fetch('http://127.0.0.1:8000/api/drinks');
    drinks = await res.json();
  }

  async function handleSubmit() {
    const payload = {
      brand_id: parseInt(selectedBrandId),
      flavour: flavour,
      size_ml: size,
      caffeine_mg: caffeine
    };

    const res = await fetch('http://127.0.0.1:8000/api/drinks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      await loadDrinks(); // Refresh list
      flavour = ""; // Reset form slightly
    } else {
      alert("Error saving drink");
    }
  }

  async function loadHistory() {
    const res = await fetch('http://127.0.0.1:8000/api/consumptions');
    history = await res.json();
  }

  async function logDrink(drinkId) {
    const payload = { drink_id: drinkId };
    const res = await fetch('http://127.0.0.1.8000/api/consumptions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      await loadHistory();
    } else {
      alert("Error logging drink");
    }
    }
</script>

<main>
  <h1>Drink Manager</h1>

  <div class="card">
    <h2>Add New Drink</h2>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="row">
        <label>Brand:
          <select bind:value={selectedBrandId}>
            {#each brands as brand}
              <option value={brand.id}>{brand.name}</option>
            {/each}
          </select>
        </label>
      </div>
      
      <div class="row">
        <label>Flavour: <input type="text" bind:value={flavour} required placeholder="e.g. Tropical" /></label>
      </div>

      <div class="row">
        <label>Size (ml): <input type="number" bind:value={size} /></label>
        <label>Caffeine (mg): <input type="number" bind:value={caffeine} /></label>
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
          <li>
            <strong>{drink.display_name}</strong> 
            <small>({drink.caffeine_per_100ml}mg/100ml)</small>
            <button on:click={() => logDrink(drink.id)} style="margin-left: 1rem;">Log Drink</button>
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
            {entry.drink.display_name}
            <small> - {new Date(entry.timestamp).toLocaleString()}</small>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</main>

<style>
  main { max-width: 600px; margin: 0 auto; padding: 2rem; font-family: sans-serif; }
  .card { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
  .row { margin-bottom: 1rem; display: flex; gap: 1rem; }
  label { display: block; width: 100%; }
  input, select { width: 100%; padding: 0.5rem; margin-top: 0.25rem; }
  button { background: #000; color: #fff; border: none; padding: 0.75rem 1.5rem; cursor: pointer; border-radius: 4px; }
  ul { padding-left: 1.2rem; }
  li { margin-bottom: 0.5rem; }
</style>