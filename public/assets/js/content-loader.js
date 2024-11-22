class ContentLoader {
    constructor() {
      this.currentType = 'main';
      this.container = document.getElementById('content-container');
      this.init();
    }
  
    init() {
      this.bindEvents();
      if (window.__INITIAL_DATA__ && window.__INITIAL_DATA__[this.currentType]) {
        this.renderContent(window.__INITIAL_DATA__[this.currentType]);
      }
    }
  
    bindEvents() {
      document.querySelectorAll('.content-tabs .tab-item').forEach(tab => {
        tab.addEventListener('click', (e) => {
          e.preventDefault();
          const type = e.target.dataset.type;
          if(this.currentType !== type) {
            document.querySelectorAll('.content-tabs .tab-item').forEach(t => 
              t.classList.remove('active'));
            e.target.classList.add('active');
            this.switchContent(type);
          }
        });
      });
    }
  
    switchContent(type) {
      this.container.style.opacity = 0;
      setTimeout(() => {
        if (window.__INITIAL_DATA__ && window.__INITIAL_DATA__[type]) {
          this.renderContent(window.__INITIAL_DATA__[type]);
          this.currentType = type;
          this.container.style.opacity = 1;
        }
      }, 200);
    }
  
    renderContent(data) {
      let html = '';
      data.forEach(section => {
        if (section.list) {
          section.list.forEach(item => {
            html += this.generateSectionHTML(item);
          });
        }
      });
      this.container.innerHTML = html;
      this.initComponents();
    }
  
    generateSectionHTML(section) {
      return `
        <div class="tab-container">
          <div class="d-flex flex-fill">
            <h4 class="text-gray text-lg mb-4">
              <i class="site-tag iconfont icon-tag icon-lg mr-1" id="${section.term}"></i>
              ${section.term}
            </h4>
            <div class="flex-fill"></div>
          </div>
          <div class="tabs-nav">
            ${this.generateTabsHTML(section.tabs)}
          </div>
          <div class="tab-contents">
            ${this.generateContentsHTML(section.tabs)}
          </div>
        </div>
      `;
    }
  
    generateTabsHTML(tabs) {
      if (!tabs || !Array.isArray(tabs)) return '';
      return tabs.map((tab, index) => `
        <a href="javascript:;" 
           class="tab-item ${index === 0 ? 'active' : ''}" 
           data-tab="${index}">${tab.name}</a>
      `).join('');
    }
  
    generateContentsHTML(tabs) {
      if (!tabs || !Array.isArray(tabs)) return '';
      return tabs.map((tab, index) => `
        <div class="tab-content ${index === 0 ? 'active' : ''}" data-tab="${index}">
          <div class="row">
            ${this.generateLinksHTML(tab.links)}
          </div>
        </div>
      `).join('');
    }
  
    generateLinksHTML(links) {
      if (!links || !Array.isArray(links)) return '';
      return links.map(link => `
        <div class="url-card col-6 col-sm-6 col-md-4 col-xl-5a col-xxl-6a">
          <div class="url-body default">
            <a href="${link.url}" 
               target="_blank" 
               class="card no-c mb-4" 
               data-toggle="tooltip" 
               data-placement="bottom" 
               title="${link.description}">
              <div class="card-body">
                <div class="url-content d-flex align-items-center">
                  <div class="url-img mr-2 d-flex align-items-center justify-content-center">
                    <img src="${window.logosPath}/${link.logo}" 
                         alt="${link.title}">
                  </div>
                  <div class="url-info flex-fill">
                    <div class="text-sm overflowClip_1">
                      <strong>${link.title}</strong>
                    </div>
                    <p class="overflowClip_1 m-0 text-muted text-xs">
                      ${link.description}
                    </p>
                  </div>
                </div>
              </div>
            </a>
            <a href="${link.url}" 
               class="togo text-center text-muted is-views" 
               data-toggle="tooltip" 
               data-placement="right" 
               title="直达" 
               rel="nofollow">
              <i class="iconfont icon-goto"></i>
            </a>
          </div>
        </div>
      `).join('');
    }
  
    initComponents() {
      if(isPC()) {
        $('[data-toggle="tooltip"]').tooltip({trigger: 'hover'});
      }
      this.initTabs();
    }
  
    initTabs() {
      document.querySelectorAll('.tab-container .tab-item').forEach(tab => {
        tab.addEventListener('click', (e) => {
          const container = e.target.closest('.tab-container');
          if(!container) return;
          
          const tabId = e.target.dataset.tab;
          container.querySelectorAll('.tab-item').forEach(t => 
            t.classList.remove('active'));
          container.querySelectorAll('.tab-content').forEach(c => 
            c.classList.remove('active'));
          
          e.target.classList.add('active');
          container.querySelector(`.tab-content[data-tab="${tabId}"]`)
            .classList.add('active');
        });
      });
    }
  }