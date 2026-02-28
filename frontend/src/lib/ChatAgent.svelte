<script>
  import { onMount, tick } from 'svelte';
  import Chart from 'chart.js/auto';

  let isOpen = false;
  let question = '';
  let loading = false;
  let messages = [];
  let messagesEl;

  // Suggestions shown when chat is empty
  const suggestions = [
    'What days of the week am I most active?',
    'How many times have I gotten a free drink?',
    'Which brand do I drink most?',
    'What\'s my average spend per drink?',
    'How much caffeine have I had this month?',
  ];

  function toggle() {
    isOpen = !isOpen;
  }

  async function scrollToBottom() {
    await tick();
    if (messagesEl) messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function ask(q = question.trim()) {
    if (!q || loading) return;
    question = '';
    messages = [...messages, { role: 'user', text: q }];
    loading = true;
    await scrollToBottom();

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      messages = [...messages, { role: 'assistant', ...data }];
    } catch {
      messages = [...messages, { role: 'assistant', type: 'text', answer: 'Something went wrong. Please try again.' }];
    }

    loading = false;
    await scrollToBottom();
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      ask();
    }
  }

  // Mount Chart.js inside a chart message bubble
  function mountChart(node, msg) {
    if (msg.type !== 'chart') return;
    const ctx = node.getContext('2d');
    const colors = [
      '#00ff41','#00cc33','#009926','#006619','#26a641',
      '#39d353','#6de087','#99edaa','#ccf6d4','#e5fbea',
    ];
    new Chart(ctx, {
      type: msg.chart_type || 'bar',
      data: {
        labels: msg.labels,
        datasets: [{
          label: msg.title || '',
          data: msg.data,
          backgroundColor: msg.chart_type === 'pie'
            ? msg.labels.map((_, i) => colors[i % colors.length])
            : '#00ff41',
          borderColor: msg.chart_type === 'pie' ? 'transparent' : '#00ff41',
          borderRadius: 4,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: msg.chart_type === 'pie', labels: { color: '#e0e0e0' } },
          title: { display: !!msg.title, text: msg.title, color: '#e0e0e0' },
        },
        scales: msg.chart_type === 'pie' ? {} : {
          x: { ticks: { color: '#666' }, grid: { color: '#1a1a1a' } },
          y: { ticks: { color: '#666' }, grid: { color: '#1a1a1a' } },
        },
      },
    });
  }
</script>

<!-- Floating button -->
<button class="fab" on:click={toggle} aria-label="Open chat agent">
  {#if isOpen}
    <span>✕</span>
  {:else}
    <span>AI</span>
  {/if}
</button>

<!-- Chat panel -->
{#if isOpen}
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Ask your data</span>
      <span class="panel-sub">Powered by Gemini</span>
    </div>

    <div class="messages" bind:this={messagesEl}>
      {#if messages.length === 0}
        <div class="empty-state">
          <p class="empty-hint">Try asking:</p>
          <div class="suggestions">
            {#each suggestions as s}
              <button class="suggestion-chip" on:click={() => ask(s)}>{s}</button>
            {/each}
          </div>
        </div>
      {/if}

      {#each messages as msg}
        {#if msg.role === 'user'}
          <div class="bubble user">{msg.text}</div>
        {:else}
          <div class="bubble assistant">
            {#if msg.type === 'text'}
              {msg.answer}
            {:else if msg.type === 'chart'}
              <p class="chart-title">{msg.title}</p>
              <div class="chart-wrap">
                <canvas use:mountChart={msg}></canvas>
              </div>
            {/if}
          </div>
        {/if}
      {/each}

      {#if loading}
        <div class="bubble assistant loading">
          <span></span><span></span><span></span>
        </div>
      {/if}
    </div>

    <div class="input-row">
      <input
        type="text"
        bind:value={question}
        on:keydown={handleKey}
        placeholder="Ask anything about your drinks..."
        disabled={loading}
      />
      <button class="send-btn" on:click={() => ask()} disabled={loading || !question.trim()}>
        ➜
      </button>
    </div>
  </div>
{/if}

<style>
  /* --- FAB --- */
  .fab {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--accent-primary);
    color: black;
    border: none;
    font-size: 0.85rem;
    font-weight: 800;
    cursor: pointer;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .fab:hover {
    transform: scale(1.08);
    box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
  }

  /* --- PANEL --- */
  .panel {
    position: fixed;
    bottom: 6rem;
    right: 2rem;
    width: 380px;
    max-height: 520px;
    background: #0a0a0a;
    border: 1px solid #222;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    z-index: 999;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
    overflow: hidden;
  }

  .panel-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #1a1a1a;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }

  .panel-title {
    font-weight: 700;
    color: white;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .panel-sub {
    font-size: 0.7rem;
    color: var(--accent-primary);
  }

  /* --- MESSAGES --- */
  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    scrollbar-width: thin;
    scrollbar-color: #222 transparent;
  }

  .empty-state {
    text-align: center;
    padding: 0.5rem 0;
  }

  .empty-hint {
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
  }

  .suggestion-chip {
    background: #111;
    border: 1px solid #2a2a2a;
    color: var(--text-muted);
    font-size: 0.72rem;
    padding: 0.35rem 0.7rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
  }

  .suggestion-chip:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  /* --- BUBBLES --- */
  .bubble {
    padding: 0.65rem 0.9rem;
    border-radius: 10px;
    font-size: 0.85rem;
    line-height: 1.5;
    max-width: 90%;
    word-break: break-word;
  }

  .bubble.user {
    background: var(--accent-primary);
    color: black;
    align-self: flex-end;
    font-weight: 500;
    border-radius: 10px 10px 2px 10px;
  }

  .bubble.assistant {
    background: #111;
    border: 1px solid #222;
    color: var(--text-main);
    align-self: flex-start;
    border-radius: 2px 10px 10px 10px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }

  /* --- LOADING DOTS --- */
  .bubble.loading {
    display: flex;
    gap: 5px;
    align-items: center;
    padding: 0.8rem 1rem;
  }

  .bubble.loading span {
    width: 7px;
    height: 7px;
    background: var(--accent-primary);
    border-radius: 50%;
    animation: dot-bounce 1.2s infinite ease-in-out;
  }

  .bubble.loading span:nth-child(2) { animation-delay: 0.2s; }
  .bubble.loading span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes dot-bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
  }

  /* --- CHART --- */
  .chart-title {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 0 0.5rem 0;
  }

  .chart-wrap {
    position: relative;
    height: 200px;
    width: 100%;
  }

  /* --- INPUT --- */
  .input-row {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem;
    border-top: 1px solid #1a1a1a;
  }

  .input-row input {
    flex: 1;
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    color: var(--text-main);
    padding: 0.55rem 0.75rem;
    font-size: 0.83rem;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s;
  }

  .input-row input:focus {
    border-color: var(--accent-primary);
  }

  .input-row input:disabled {
    opacity: 0.5;
  }

  .send-btn {
    background: var(--accent-primary);
    border: none;
    color: black;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: opacity 0.2s;
  }

  .send-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  /* --- MOBILE --- */
  @media (max-width: 600px) {
    .panel {
      right: 1rem;
      left: 1rem;
      width: auto;
      bottom: 5rem;
    }
    .fab {
      right: 1rem;
      bottom: 1rem;
    }
  }
</style>
