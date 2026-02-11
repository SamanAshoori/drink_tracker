<script>
  export let data = []; // The raw list of consumptions from your database

  //Setup the date range (Last 365 days)
  let today = new Date();
  let dates = [];
  
  // Generate the last year of dates
  for (let i = 364; i >= 0; i--) {
    const d = new Date();
    d.setDate(today.getDate() - i);
    dates.push(d);
  }

  //Convert Date object to "YYYY-MM-DD" string for easy matching
  function formatDateKey(dateObj) {
    return dateObj.toLocaleDateString('en-CA'); // 'en-CA' outputs YYYY-MM-DD consistently
  }

  // Reactive: Aggregate the data into a Map { "2023-10-01": 5, ... }
  // This runs automatically whenever 'data' changes
  $: counts = data.reduce((acc, entry) => {
    // Assuming entry.consumed_at exists
    const dateKey = entry.consumed_at.split('T')[0]; // Extract YYYY-MM-DD
    acc[dateKey] = (acc[dateKey] || 0) + 1;
    return acc;
  }, {});

  // 4. Helper: Determine color based on count
  function getColor(count) {
    if (!count) return 'var(--color-level-0)';
    if (count === 1) return 'var(--color-level-1)';
    if (count === 2) return 'var(--color-level-2)';
    if (count === 3) return 'var(--color-level-3)';
    if (count === 4) return 'var(--color-level-4)';
    return 'var(--color-level-5)'; // 4 or more
  }
</script>

<div class="heatmap-container">
  <h2>Heatmap</h2>
  
  <div class="graph">
    {#each dates as date}
      {@const key = formatDateKey(date)}
      {@const count = counts[key] || 0}
      
      <div 
        class="day" 
        style="background-color: {getColor(count)}"
        title="{key}: {count} drinks"
      ></div>
    {/each}
  </div>
  
  <div class="legend">
    <span>Less</span>
    <div class="day" style="background-color: var(--color-level-0)"></div>
    <div class="day" style="background-color: var(--color-level-1)"></div>
    <div class="day" style="background-color: var(--color-level-2)"></div>
    <div class="day" style="background-color: var(--color-level-3)"></div>
    <span>More</span>
  </div>
</div>

<style>
  :root {
  --color-level-0: #222222; /* Black (Empty) */
  --color-level-1: #0e4429; /* Dim Forest */
  --color-level-2: #006d32; /* Standard Green */
  --color-level-3: #26a641; /* Apple Green */
  --color-level-4: #39d353; /* Bright Green */
  --color-level-5: #4aff73; /* Neon (Max Caffeine) */
  --square-size: 10px;
  --gap: 3px;
}

  .heatmap-container {
    width: 100%;
    margin-top: 1rem;
    overflow-x: auto; /* Scroll if it gets too wide on mobile */
  }

  .graph {
    display: grid;
    /* The Magic: 7 rows (Mon-Sun), flow columns automatically */
    grid-template-rows: repeat(7, var(--square-size)); 
    grid-auto-flow: column; 
    gap: var(--gap);
    height: calc(7 * (var(--square-size) + var(--gap)));
  }

  .day {
    width: var(--square-size);
    height: var(--square-size);
    border-radius: 2px;
    cursor: pointer;
  }

  .day:hover {
    outline: 1px solid rgba(0,0,0,0.5);
  }

  .legend {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    font-size: 0.8rem;
    color: #666;
    justify-content: flex-end;
  }

  .heatmap-container h2 {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 1.5rem; /* More space */
  }

  .legend span {
    display: none; 
  }
</style>