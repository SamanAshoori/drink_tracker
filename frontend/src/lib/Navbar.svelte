<script>
  export let currentPage;

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function setPage(name) {
    dispatch('route', name);
  }
</script>

<nav>
  <div class="nav-inner">
    <span class="nav-brand">Energy Drink Tracker<span class="accent">.</span></span>
    <div class="nav-links">
      <button class:active={currentPage === 'dashboard'} on:click={() => setPage('dashboard')}>Dashboard</button>
      <button class:active={currentPage === 'logger'} on:click={() => setPage('logger')}>Log Drink</button>
      <button class:active={currentPage === 'admin'} on:click={() => setPage('admin')}>Admin</button>
    </div>
  </div>
</nav>

<style>
  nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--bg-card);
    border-bottom: 1px solid #222;
    width: 100%;
  }

  .nav-inner {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
  }

  .nav-brand {
    font-family: 'Courier New', Courier, monospace;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-main);
    letter-spacing: -0.5px;
  }

  .accent {
    color: var(--accent-primary);
  }

  .nav-links {
    display: flex;
    gap: 0.25rem;
  }

  button {
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 0.4rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: var(--radius);
    transition: color 0.2s ease, background 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }

  button:hover {
    color: var(--text-main);
    background: #1a1a1a;
  }

  button.active {
    color: var(--accent-primary);
    background: rgba(0, 255, 65, 0.08);
  }

  @media (max-width: 480px) {
    .nav-brand {
      display: none;
    }
    .nav-links {
      width: 100%;
      justify-content: space-around;
    }
    button {
      padding: 0.4rem 0.6rem;
      font-size: 0.75rem;
    }
  }
</style>
