<script>
  let status = "Waiting for backend...";

  async function checkBackend() {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/brands');
      const data = await res.json();
      status = `Backend says: ${data.message}`;
    } catch (e) {
      status = "Error connecting to backend (is it running?)";
    }
  }
</script>

<main>
  <h1>Drink Tracker MVP</h1>
  <p>Frontend Status: <span style="color: green">Running</span></p>
  <p>Backend Status: <strong>{status}</strong></p>
  <button on:click={checkBackend}>Test Connection</button>
</main>

<style>
  main { font-family: sans-serif; text-align: center; padding: 2rem; }
  button { padding: 10px 20px; cursor: pointer; }
</style>