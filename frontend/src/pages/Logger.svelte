<script>
  import { onMount } from 'svelte';

  let drinks = [];

  onMount(async () => {
    const res = await fetch('http://127.0.0.1:8000/api/drinks');
    const data = await res.json();
    drinks = data.map(d => ({ ...d, log_price: 0.0 }));
  });

  async function logDrink(drink) {
    const payload = { 
      drink_id: drink.id,
      price_paid: drink.log_price
    };
    
    const res = await fetch('http://127.0.0.1:8000/api/consumptions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Logged " + drink.display_name);
    } else {
      alert("Error logging drink");
    }
  }
</script>

<div class="card">
  <h2>Log a Drink</h2>
  <p class="subtitle">Select a drink from your library to log it.</p>
  {#if drinks.length === 0}
    <p>No drinks found. Go to Admin to add some!</p>
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

<style>
  .card { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
  .subtitle { color: #666; margin-bottom: 1rem; }
  .drink-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
  .drink-actions { display: flex; align-items: center; gap: 5px; }
  .price-input { width: 70px; padding: 5px; margin: 0 !important; }
  button { background: #000; color: #fff; border: none; padding: 0.5rem 1rem; cursor: pointer; border-radius: 4px; }
  ul { padding-left: 0; list-style: none; }
</style>