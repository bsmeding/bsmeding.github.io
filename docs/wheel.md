# 🎡 Rat of Fortune

<div class="rat wrap md-typeset">

  <div class="rat actions">
    <button class="md-button md-button--primary" id="loadFromSiteBtn">Load names from site file</button>
    <span class="rat sep">or</span>
    <label class="md-button" for="fileInput">Upload names.txt</label>
    <input type="file" id="fileInput" accept=".txt" hidden>
  </div>

  <div class="rat grid">
    <div class="rat card">
      <h3>Participants</h3>
      <div id="namesArea" class="rat names"></div>
    </div>

    <div class="rat card wheel-card">
      <h3>Wheel</h3>

      <button class="md-button md-button--primary" id="spinBtn">🎰 Spin the Wheel</button>

      <div class="rat wheelbox">
        <div class="rat pointer" aria-hidden="true"></div>
        <canvas id="wheelCanvas" width="500" height="500"></canvas>
      </div>

      <div id="result" class="rat result" aria-live="polite"></div>
    </div>
  </div>
</div>
