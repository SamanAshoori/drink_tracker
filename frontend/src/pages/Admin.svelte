<script>
  import { onMount } from 'svelte';

  let brands = [];
  let adminPassword = ""; // The key variable
  
  // Form Data
  let selectedBrandId = "";
  let flavour = "";
  let size = 250;
  let caffeinedensity = 32;

  onMount(async () => {
    const res = await fetch('/api/brands');
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

    const res = await fetch('/api/drinks', {
      method: 'POST',
      headers: { 
          'Content-Type': 'application/json',
          'x-admin-key': adminPassword // Send the password
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Drink Created Successfully!");
      flavour = ""; 
    } else if (res.status === 401) {
      alert("Wrong Admin Password!");
    } else {
      alert("Error creating drink");
    }
  }
</script>

<div class="page">
  <div class="card">
    <h2>Admin Access</h2>

    <div class="field">
      <label>Admin Password
        <input type="password" bind:value={adminPassword} placeholder="Enter secret key..." />
      </label>
    </div>

    <div class="divider"></div>

    <h3>Add New Drink</h3>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="field">
        <label>Brand
          <select bind:value={selectedBrandId}>
            {#each brands as brand}
              <option value={brand.id}>{brand.name}</option>
            {/each}
          </select>
        </label>
      </div>

      <div class="field">
        <label>Flavour
          <input type="text" bind:value={flavour} required placeholder="e.g. Tropical" />
        </label>
      </div>

      <div class="field-row">
        <label>Size (ml)
          <input type="number" bind:value={size} />
        </label>
        <label>Caffeine (mg/100ml)
          <input type="number" bind:value={caffeinedensity} />
        </label>
      </div>

      <button type="submit">Create Drink</button>
    </form>
  </div>
</div>

<style>
  .page {
    max-width: 960px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  .card {
    background: var(--bg-card);
    border: var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
  }

  h2 {
    font-size: 1rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 1.25rem 0;
  }

  h3 {
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 1.25rem 0;
  }

  .divider {
    border: none;
    border-top: 1px solid #222;
    margin: 1.5rem 0;
  }

  .field {
    margin-bottom: 1rem;
  }

  .field-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }

  label {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 0;
  }

  input, select {
    display: block;
    width: 100%;
    box-sizing: border-box;
    padding: 0.6rem 0.75rem;
    margin-top: 0.4rem;
    background: var(--bg-input);
    border: 1px solid #333;
    border-radius: var(--radius);
    color: var(--text-main);
    font-family: inherit;
    font-size: 0.9rem;
  }

  input:focus, select:focus {
    outline: none;
    border-color: var(--accent-dim);
  }

  select option {
    background: var(--bg-input);
  }

  button {
    background: var(--accent-primary);
    color: black;
    border: none;
    padding: 0.65rem 1.5rem;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    border-radius: var(--radius);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: opacity 0.2s;
    margin-top: 0.5rem;
  }

  button:hover {
    opacity: 0.85;
  }

  @media (max-width: 500px) {
    .page {
      padding: 1.25rem 1rem;
    }
    .field-row {
      grid-template-columns: 1fr;
    }
  }
</style>