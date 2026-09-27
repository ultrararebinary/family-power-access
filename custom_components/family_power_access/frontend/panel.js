class FamilyPowerAccessPanel extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) {
      return;
    }

    this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          min-height: 100%;
          color: var(--primary-text-color);
        }

        main {
          box-sizing: border-box;
          max-width: 60rem;
          margin: 0 auto;
          padding: 24px;
        }

        h1 {
          margin: 0;
          color: inherit;
        }

        @media (max-width: 600px) {
          main {
            padding: 16px;
          }
        }
      </style>
      <main>
        <h1>Hello World</h1>
      </main>
    `;
  }
}

if (!customElements.get("family-power-access-panel")) {
  customElements.define("family-power-access-panel", FamilyPowerAccessPanel);
}
