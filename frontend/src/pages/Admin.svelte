<script>
  import { onMount } from 'svelte';

  let brands = [];
  
  // Form Data
  let selectedBrandId = "";
  let flavour = "";
  let size = 250;
  let caffeinedensity = 32;

  onMount(async () => {
    const res = await fetch('http://127.0.0.1:8000/api/brands');
    brands = await res.json();
    if (brands.length > 0) selectedBrandId = brands[0].id;
  });

  async function handleSubmit() {
    const payload = {
      brand_id: parseInt(selectedBrandId),
      flavour: flavour,
      size_ml: size,
      caffeine_per_100ml: caffeinedensity
    };

    const res = await fetch('http://127.0.0.1:8000/api/drinks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Drink Created Successfully!");
      flavour = ""; // Reset
    } else {
      alert("Error creating drink");
    }
  }
</script>

<div class="card">
  <h2>Admin: Add New Drink</h2>
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
      <label>Caffeine (mg/100ml): <input type="number" bind:value={caffeinedensity} /></label>
    </div>

    <button type="submit">Create Drink</button>
  </form>
</div>

<style>
  .card { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
  .row { margin-bottom: 1rem; display: flex; gap: 1rem; }
  label { display: block; width: 100%; }
  input, select { width: 100%; padding: 0.5rem; margin-top: 0.25rem; }
  button { background: #000; color: #fff; border: none; padding: 0.75rem 1.5rem; cursor: pointer; border-radius: 4px; }
</style>