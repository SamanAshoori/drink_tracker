<script>
  import Navbar from './lib/Navbar.svelte';
  import Dashboard from './pages/Dashboard.svelte';
  import Logger from './pages/Logger.svelte';
  import Admin from './pages/Admin.svelte';

  // Default Page
  let page = 'dashboard';

  function handleRoute(event) {
    page = event.detail;
  }
</script>

<main>
  <h1>Drink Tracker</h1>
  
  <Navbar currentPage={page} on:route={handleRoute} />

  {#if page === 'dashboard'}
    <Dashboard />
  {:else if page === 'logger'}
    <Logger />
  {:else if page === 'admin'}
    <Admin />
  {/if}
</main>

<style>
  main { max-width: 800px; margin: 0 auto; padding: 2rem; font-family: sans-serif; }
  h1 { text-align: center; margin-bottom: 2rem; }
</style>