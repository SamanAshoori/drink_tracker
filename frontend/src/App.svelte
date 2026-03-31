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

<Navbar currentPage={page} on:route={handleRoute} />

<div class="page-content">
  {#if page === 'dashboard'}
    <Dashboard />
  {:else if page === 'logger'}
    <Logger />
  {:else if page === 'admin'}
    <Admin />
  {/if}
</div>

<style>
  .page-content {
    width: 100%;
  }
</style>