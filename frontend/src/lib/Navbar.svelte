<script>
  export let currentPage;
  
  // A function to dispatch the change back to the parent
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function setPage(name) {
    dispatch('route', name);
  }
</script>

<nav>
  <button class:active={currentPage === 'dashboard'} on:click={() => setPage('dashboard')}>Dashboard</button>
  <button class:active={currentPage === 'logger'} on:click={() => setPage('logger')}>Log Drink</button>
  <button class:active={currentPage === 'admin'} on:click={() => setPage('admin')}>Admin</button>
</nav>

<style>
  nav {
    display: flex;
    justify-content: center;
    gap: 1rem;
    padding: 1rem;
    background: #eee;
    margin-bottom: 2rem;
    border-radius: 8px;
  }
  button {
    background: transparent;
    border: none;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-weight: bold;
    color: #666;
  }
  button.active {
    background: #fff;
    color: #000;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-radius: 4px;
  }
</style>