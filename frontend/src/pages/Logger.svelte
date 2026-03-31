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

<div class="page">
  <div class="card password-card">
    <label>Session Password
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
              <small>{drink.caffeine_per_100ml}mg/100ml</small>
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
              <button class="log-btn" on:click={() => logDrink(drink)}>Log</button>
            </div>
          </li>
        {/each}
      </ul>
    {/if}
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
    margin-bottom: 1.5rem;
  }

  .password-card {
    border-left: 3px solid var(--accent-primary);
  }

  label {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
  }

  input {
    width: 100%;
    box-sizing: border-box;
    padding: 0.6rem 0.75rem;
    background: var(--bg-input);
    border: 1px solid #333;
    border-radius: var(--radius);
    color: var(--text-main);
    font-family: inherit;
    font-size: 0.9rem;
  }

  input:focus {
    outline: none;
    border-color: var(--accent-dim);
  }

  h2 {
    font-size: 1rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 1.25rem 0;
  }

  ul {
    padding: 0;
    list-style: none;
    margin: 0;
  }

  .drink-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #1a1a1a;
    gap: 1rem;
  }

  .drink-row:last-child {
    border-bottom: none;
  }

  .drink-info {
    flex: 1;
    min-width: 0;
  }

  .drink-info strong {
    display: block;
    color: var(--text-main);
    font-size: 0.95rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .drink-info small {
    color: var(--text-muted);
    font-size: 0.75rem;
  }

  .drink-actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-shrink: 0;
  }

  .currency-symbol {
    color: var(--text-muted);
    font-size: 0.9rem;
  }

  .price-input {
    width: 70px !important;
    padding: 0.4rem 0.5rem;
    text-align: right;
  }

  .log-btn {
    background: var(--accent-primary);
    color: black;
    border: none;
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    border-radius: var(--radius);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: opacity 0.2s;
    white-space: nowrap;
  }

  .log-btn:hover {
    opacity: 0.85;
  }

  @media (max-width: 500px) {
    .page {
      padding: 1.25rem 1rem;
    }
    .drink-info small {
      display: none;
    }
  }
</style>