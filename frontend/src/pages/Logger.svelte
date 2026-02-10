<script>
  import { onMount } from 'svelte';

  let drinks = [];
  let adminPassword = ""; // Session password for logging

  onMount(async () => {
    const res = await fetch('/api/drinks');
    const data = await res.json();
    drinks = data.map(d => ({ ...d, log_price: 0.0 }));
  });

  async function logDrink(drink) {
    if (!adminPassword) {
        alert("Please enter the Admin Password at the top first.");
        return;
    }

    const payload = { 
      drink_id: drink.id,
      price_paid: drink.log_price
    };
    
    const res = await fetch('/api/consumptions', {
      method: 'POST',
      headers: { 
          'Content-Type': 'application/json',
          'x-admin-key': adminPassword // Send header
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Logged: " + drink.display_name);
    } else if (res.status === 401) {
      alert("Wrong Admin Password!");
    } else {
      alert("Error logging drink");
    }
  }
</script>

<div class="card password-card">
  <label>
      🔒 Session Password:
      <input type="password" bind:value={adminPassword} placeholder="Required to log drinks..." />
  </label>
</div>

<div class="card">
  <h2>Log a Drink</h2>
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

<style>
  .card { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
  .password-card { background-color: #f8f9fa; border-left: 5px solid #333; }
  .drink-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
  .drink-actions { display: flex; align-items: center; gap: 5px; }
  .price-input { width: 70px; padding: 5px; margin: 0 !important; }
  button { background: #000; color: #fff; border: none; padding: 0.5rem 1rem; cursor: pointer; border-radius: 4px; }
  ul { padding-left: 0; list-style: none; }
  input { padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
</style>