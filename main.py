import webview
import json
from datetime import datetime


class Browser:
    def __init__(self):
        self.tabs = [
            {
                "id": 1,
                "title": "New Tab",
                "url": None,
                "active": True
            }
        ]
        self.next_tab_id = 2
        self.current_tab_id = 1
        
        self.window = webview.create_window(
            "SuperFast Browser",
            html=self.get_html(),
            width=1400,
            height=900,
            min_size=(800, 600),
        )
        self.window.expose(self.navigate)
        self.window.expose(self.get_suggestions)
        self.window.expose(self.new_tab)
        self.window.expose(self.close_tab)
        self.window.expose(self.switch_tab)
        self.window.expose(self.load_page)

    def get_html(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SuperFast Browser</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f8f9fa;
            display: flex;
            flex-direction: column;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        
        /* Tabs Container */
        #tabs-container {
            background: #f3f3f3;
            border-bottom: 1px solid #dadce0;
            display: flex;
            align-items: center;
            height: 40px;
            padding: 0 8px;
            gap: 4px;
            overflow-x: auto;
            overflow-y: hidden;
            flex-shrink: 0;
            width: 100%;
        }
        
        #tabs-list {
            display: flex;
            gap: 4px;
            align-items: center;
            flex: 1;
            overflow-x: auto;
            overflow-y: hidden;
        }
        
        .tab {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 0 12px;
            height: 32px;
            background: #e8e8e8;
            border: 1px solid #ccc;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            transition: all 0.2s;
            max-width: 220px;
            min-width: 100px;
            user-select: none;
            flex-shrink: 0;
            white-space: nowrap;
        }
        
        .tab.active {
            background: white;
            border-bottom: 1px solid white;
            box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .tab:hover {
            background: #f0f0f0;
        }
        
        .tab.active:hover {
            background: white;
        }
        
        .tab-title {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 13px;
            color: #202124;
        }
        
        .tab.active .tab-title {
            font-weight: 500;
        }
        
        .tab-close {
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            border-radius: 2px;
            transition: background 0.2s;
            flex-shrink: 0;
        }
        
        .tab-close:hover {
            background: rgba(0, 0, 0, 0.1);
        }
        
        #new-tab-btn {
            width: 32px;
            height: 32px;
            border: none;
            background: transparent;
            cursor: pointer;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #5f6368;
            transition: all 0.2s;
            flex-shrink: 0;
            margin-left: auto;
        }
        
        #new-tab-btn:hover {
            background: rgba(0, 0, 0, 0.06);
        }
        
        /* Chrome-like navbar */
        #navbar {
            background: #f3f3f3;
            border-bottom: 1px solid #dadce0;
            padding: 10px 16px;
            display: flex;
            gap: 12px;
            align-items: center;
            height: 56px;
            flex-shrink: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .nav-btn {
            background: transparent;
            border: none;
            color: #5f6368;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            flex-shrink: 0;
        }
        
        .nav-btn:hover {
            background: rgba(0, 0, 0, 0.06);
        }
        
        .nav-btn:active {
            background: rgba(0, 0, 0, 0.1);
        }
        
        /* Search bar */
        #search-container {
            flex: 1;
            min-width: 200px;
            max-width: 600px;
            position: relative;
        }
        
        #url-input {
            width: 100%;
            padding: 9px 16px;
            border: 1px solid #dadce0;
            border-radius: 24px;
            font-size: 14px;
            background: white;
            transition: all 0.2s;
            color: #202124;
        }
        
        #url-input:hover {
            box-shadow: 0 1px 6px rgba(32, 33, 36, 0.08), 0 1px 0px rgba(0, 0, 0, 0.04);
        }
        
        #url-input:focus {
            outline: none;
            border-color: #dadce0;
            box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28), 0 1px 0px rgba(0, 0, 0, 0.08);
        }
        
        #suggestions {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border-radius: 8px;
            margin-top: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            max-height: 300px;
            overflow-y: auto;
            display: none;
            z-index: 1000;
            border: 1px solid #dadce0;
        }
        
        .suggestion-item {
            padding: 10px 16px;
            cursor: pointer;
            transition: background 0.15s;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
            color: #202124;
        }
        
        .suggestion-item:hover {
            background: #f9f9f9;
        }
        
        .suggestion-item:last-child {
            border-bottom: none;
        }
        
        .right-nav {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        #logo-btn {
            width: auto;
            padding: 0 12px;
            font-weight: 600;
            color: #1f2937;
            font-size: 14px;
        }
        
        #logo-btn:hover {
            background: rgba(31, 41, 55, 0.08);
        }
        
        /* Main content area */
        .content-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        #home-page {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: white;
            padding: 40px 20px;
            overflow-y: auto;
        }
        
        #home-page.hidden {
            display: none;
        }
        
        .logo {
            font-size: 92px;
            font-weight: 400;
            letter-spacing: 0;
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(90deg, #4285f4 0%, #ea4335 25%, #fbbc04 50%, #34a853 75%, #4285f4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .search-box-home {
            width: 90%;
            max-width: 584px;
            margin-bottom: 30px;
            position: relative;
        }
        
        .search-box-home input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #dadce0;
            border-radius: 24px;
            font-size: 16px;
            background: white;
            transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1), 0 1px 1px rgba(0, 0, 0, 0.05);
        }
        
        .search-box-home input:hover {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        .search-box-home input:focus {
            outline: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        .search-box-home #suggestions-home {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border-radius: 8px;
            margin-top: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            max-height: 300px;
            overflow-y: auto;
            display: none;
            z-index: 1000;
            border: 1px solid #dadce0;
        }
        
        .search-buttons {
            margin-bottom: 30px;
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .search-btn {
            padding: 10px 24px;
            border: 1px solid #f8f9fa;
            background: #f8f9fa;
            color: #3c4043;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }
        
        .search-btn:hover {
            box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
            background: #f8f9fa;
            border: 1px solid #dadce0;
            color: #202124;
        }
        
        .shortcuts-container {
            width: 100%;
            max-width: 700px;
            margin-top: 40px;
        }
        
        .shortcuts {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            padding: 0 20px;
        }
        
        .shortcut {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            text-decoration: none;
            color: #202124;
            transition: all 0.2s;
            padding: 12px;
            border-radius: 8px;
        }
        
        .shortcut:hover {
            background: rgba(0, 0, 0, 0.04);
        }
        
        .shortcut-icon {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            background: white;
            border: 1px solid #dadce0;
            transition: all 0.2s;
        }
        
        .shortcut:hover .shortcut-icon {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .shortcut-text {
            font-size: 12px;
            color: #5f6368;
            text-align: center;
        }
        
        .add-shortcut {
            background: #f0f0f0;
            border: 1px solid #e0e0e0;
        }
        
        .add-shortcut:hover {
            background: #e8e8e8;
        }
        
        .iframe-container {
            flex: 1;
            display: none;
            overflow: hidden;
        }
        
        .iframe-container.active {
            display: block;
        }
        
        iframe {
            width: 100%;
            height: 100%;
            border: none;
            display: block;
            background: white;
        }
        
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #dadce0;
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #bdc1c6;
        }
    </style>
</head>
<body>
    <!-- Tabs Container -->
    <div id="tabs-container">
        <div id="tabs-list"></div>
        <button id="new-tab-btn" onclick="createNewTab()" title="New Tab"><i class="fas fa-plus"></i></button>
    </div>
    
    <!-- Chrome-like Navigation Bar -->
    <div id="navbar">
        <button class="nav-btn" onclick="goBack()" title="Back"><i class="fas fa-arrow-left"></i></button>
        <button class="nav-btn" onclick="goForward()" title="Forward"><i class="fas fa-arrow-right"></i></button>
        <button class="nav-btn" onclick="reloadPage()" title="Reload"><i class="fas fa-redo"></i></button>
        
        <button class="nav-btn" id="logo-btn" onclick="goHome()" title="Home"><i class="fas fa-home"></i> Home</button>
        
        <div id="search-container">
            <input 
                id="url-input" 
                type="text" 
                placeholder="Search Google or type a URL"
                autocomplete="off"
            >
            <div id="suggestions"></div>
        </div>
        
        <div class="right-nav">
            <button class="nav-btn" title="Settings"><i class="fas fa-ellipsis-v"></i></button>
            <button class="nav-btn" title="Profile"><i class="fas fa-user-circle"></i></button>
        </div>
    </div>
    
    <!-- Content Area -->
    <div class="content-wrapper">
        <div id="home-page">
            <div class="logo">Google</div>
            
            <div class="search-box-home">
                <input 
                    id="home-search" 
                    type="text" 
                    placeholder="Search Google or type a URL"
                    autocomplete="off"
                >
                <div id="suggestions-home"></div>
            </div>
            
            <div class="search-buttons">
                <button class="search-btn" onclick="searchGoogle()"><i class="fas fa-search"></i> Google Search</button>
                <button class="search-btn" onclick="luckySearch()"><i class="fas fa-star"></i> I'm Feeling Lucky</button>
            </div>
            
            <div class="shortcuts-container">
                <div class="shortcuts" id="shortcuts">
                    <div class="shortcut" onclick="navigateTo('https://www.facebook.com')">
                        <div class="shortcut-icon" style="background: linear-gradient(135deg, #1877f2, #0a66c2);"><i class="fab fa-facebook-f" style="color: white; font-size: 24px;"></i></div>
                        <div class="shortcut-text">Facebook</div>
                    </div>
                    <div class="shortcut" onclick="navigateTo('https://www.youtube.com')">
                        <div class="shortcut-icon" style="background: #ff0000;"><i class="fab fa-youtube" style="color: white; font-size: 24px;"></i></div>
                        <div class="shortcut-text">YouTube</div>
                    </div>
                    <div class="shortcut" onclick="navigateTo('https://mail.google.com')">
                        <div class="shortcut-icon" style="background: #ea4335;"><i class="fas fa-envelope" style="color: white; font-size: 24px;"></i></div>
                        <div class="shortcut-text">Gmail</div>
                    </div>
                    <div class="shortcut" onclick="navigateTo('https://www.paypal.com')">
                        <div class="shortcut-icon" style="background: #003087;"><i class="fab fa-paypal" style="color: white; font-size: 24px;"></i></div>
                        <div class="shortcut-text">PayPal</div>
                    </div>
                    <div class="shortcut" onclick="navigateTo('https://chat.openai.com')">
                        <div class="shortcut-icon" style="background: #10a37f;"><i class="fas fa-brain" style="color: white; font-size: 24px;"></i></div>
                        <div class="shortcut-text">ChatGPT</div>
                    </div>
                    <div class="shortcut" onclick="addShortcut()">
                        <div class="shortcut-icon add-shortcut"><i class="fas fa-plus" style="font-size: 24px; color: #5f6368;"></i></div>
                        <div class="shortcut-text">Add shortcut</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="iframes-container"></div>
    </div>

    <script>
        let tabs = [{id: 1, title: "New Tab", url: null, active: true}];
        let nextTabId = 2;
        let currentTabId = 1;
        
        const urlInput = document.getElementById('url-input');
        const suggestionsDiv = document.getElementById('suggestions');
        const homeSearch = document.getElementById('home-search');
        const suggestionsHome = document.getElementById('suggestions-home');
        const homePage = document.getElementById('home-page');
        const iframesContainer = document.getElementById('iframes-container');
        const tabsList = document.getElementById('tabs-list');
        
        urlInput.focus();
        
        // Render tabs
        function renderTabs() {
            tabsList.innerHTML = '';
            tabs.forEach(tab => {
                const tabEl = document.createElement('div');
                tabEl.className = 'tab' + (tab.active ? ' active' : '');
                tabEl.innerHTML = `
                    <span class="tab-title">${tab.title}</span>
                    <span class="tab-close" onclick="closeTab(${tab.id}); event.stopPropagation();"><i class="fas fa-times" style="font-size: 12px;"></i></span>
                `;
                tabEl.onclick = () => switchTab(tab.id);
                tabsList.appendChild(tabEl);
            });
        }
        
        // Create new tab
        function createNewTab() {
            const newTab = {
                id: nextTabId++,
                title: "New Tab",
                url: null,
                active: false
            };
            tabs.forEach(t => t.active = false);
            tabs.push(newTab);
            currentTabId = newTab.id;
            newTab.active = true;
            renderTabs();
            renderContent();
            urlInput.value = '';
            urlInput.focus();
        }
        
        // Close tab
        function closeTab(tabId) {
            tabs = tabs.filter(t => t.id !== tabId);
            if (currentTabId === tabId) {
                if (tabs.length > 0) {
                    currentTabId = tabs[tabs.length - 1].id;
                    tabs.find(t => t.id === currentTabId).active = true;
                }
            }
            renderTabs();
            renderContent();
        }
        
        // Switch tab
        function switchTab(tabId) {
            tabs.forEach(t => t.active = false);
            const tab = tabs.find(t => t.id === tabId);
            if (tab) {
                tab.active = true;
                currentTabId = tabId;
                renderTabs();
                renderContent();
            }
        }
        
        // Render content
        function renderContent() {
            const currentTab = tabs.find(t => t.id === currentTabId);
            const iframes = document.querySelectorAll('iframe');
            iframes.forEach(iframe => iframe.parentElement.classList.remove('active'));
            
            if (!currentTab.url) {
                homePage.classList.remove('hidden');
                urlInput.value = '';
            } else {
                homePage.classList.add('hidden');
                let iframeContainer = document.querySelector(`[data-tab-id="${currentTab.id}"]`);
                if (!iframeContainer) {
                    iframeContainer = document.createElement('div');
                    iframeContainer.className = 'iframe-container';
                    iframeContainer.setAttribute('data-tab-id', currentTab.id);
                    const iframe = document.createElement('iframe');
                    iframe.src = currentTab.url;
                    iframe.style.display = 'block';
                    iframeContainer.appendChild(iframe);
                    iframesContainer.appendChild(iframeContainer);
                }
                iframeContainer.classList.add('active');
                urlInput.value = currentTab.url || '';
            }
        }
        
        // Navigation
        function doNavigate() {
            let query = urlInput.value.trim();
            if (!query) return;
            
            let target = parseURL(query);
            const currentTab = tabs.find(t => t.id === currentTabId);
            currentTab.url = target;
            try {
                currentTab.title = new URL(target).hostname;
            } catch (e) {
                currentTab.title = target.substring(0, 20);
            }
            renderTabs();
            renderContent();
            urlInput.value = '';
            suggestionsDiv.style.display = 'none';
            
            // Load page in webview
            window.pywebview.api.load_page(target);
        }
        
        function navigateTo(url) {
            const currentTab = tabs.find(t => t.id === currentTabId);
            currentTab.url = url;
            try {
                currentTab.title = new URL(url).hostname;
            } catch (e) {
                currentTab.title = url.substring(0, 20);
            }
            renderTabs();
            renderContent();
            
            // Load page in webview
            window.pywebview.api.load_page(url);
        }
        
        function searchGoogle() {
            let query = homeSearch.value.trim();
            if (!query) return;
            let target = 'https://www.google.com/search?q=' + encodeURIComponent(query);
            
            const currentTab = tabs.find(t => t.id === currentTabId);
            currentTab.url = target;
            currentTab.title = 'Google Search';
            renderTabs();
            renderContent();
            
            window.pywebview.api.load_page(target);
        }
        
        function luckySearch() {
            let query = homeSearch.value.trim();
            if (!query) query = 'random';
            let target = 'https://www.google.com/search?q=' + encodeURIComponent(query) + '&btnI=1';
            
            const currentTab = tabs.find(t => t.id === currentTabId);
            currentTab.url = target;
            currentTab.title = 'Google Search';
            renderTabs();
            renderContent();
            
            window.pywebview.api.load_page(target);
        }
        
        function parseURL(query) {
            if (!query.startsWith('http://') && !query.startsWith('https://')) {
                if (query.includes('.') && !query.includes(' ')) {
                    return 'https://' + query;
                } else {
                    return 'https://www.google.com/search?q=' + encodeURIComponent(query);
                }
            }
            return query;
        }
        
        function goHome() {
            const currentTab = tabs.find(t => t.id === currentTabId);
            currentTab.url = null;
            currentTab.title = 'New Tab';
            renderTabs();
            renderContent();
            urlInput.value = '';
            homeSearch.value = '';
            homeSearch.focus();
        }
        
        function goBack() {
            const currentTab = tabs.find(t => t.id === currentTabId);
            const iframeContainer = document.querySelector(`[data-tab-id="${currentTab.id}"]`);
            if (iframeContainer) {
                const iframe = iframeContainer.querySelector('iframe');
                iframe.contentWindow.history.back();
            }
        }
        
        function goForward() {
            const currentTab = tabs.find(t => t.id === currentTabId);
            const iframeContainer = document.querySelector(`[data-tab-id="${currentTab.id}"]`);
            if (iframeContainer) {
                const iframe = iframeContainer.querySelector('iframe');
                iframe.contentWindow.history.forward();
            }
        }
        
        function reloadPage() {
            const currentTab = tabs.find(t => t.id === currentTabId);
            if (currentTab.url) {
                const iframeContainer = document.querySelector(`[data-tab-id="${currentTab.id}"]`);
                if (iframeContainer) {
                    const iframe = iframeContainer.querySelector('iframe');
                    iframe.contentWindow.location.reload();
                }
            }
        }
        
        function addShortcut() {
            let url = prompt('Enter website URL:');
            if (url) {
                if (!url.startsWith('http')) url = 'https://' + url;
                navigateTo(url);
            }
        }
        
        // Suggestions
        urlInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            if (query.length > 1) {
                window.pywebview.api.get_suggestions(query).then(suggestions => {
                    if (suggestions.length > 0) {
                        suggestionsDiv.innerHTML = suggestions
                            .map(s => `<div class="suggestion-item" onclick="selectSuggestion('${s}')">${s}</div>`)
                            .join('');
                        suggestionsDiv.style.display = 'block';
                    }
                });
            } else {
                suggestionsDiv.style.display = 'none';
            }
        });
        
        homeSearch.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            if (query.length > 1) {
                window.pywebview.api.get_suggestions(query).then(suggestions => {
                    if (suggestions.length > 0) {
                        suggestionsHome.innerHTML = suggestions
                            .map(s => `<div class="suggestion-item" onclick="selectSuggestionHome('${s}')">${s}</div>`)
                            .join('');
                        suggestionsHome.style.display = 'block';
                    }
                });
            } else {
                suggestionsHome.style.display = 'none';
            }
        });
        
        function selectSuggestion(suggestion) {
            urlInput.value = suggestion;
            doNavigate();
        }
        
        function selectSuggestionHome(suggestion) {
            homeSearch.value = suggestion;
            searchGoogle();
        }
        
        // Keyboard shortcuts
        urlInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                doNavigate();
            }
        });
        
        homeSearch.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                searchGoogle();
            }
        });
        
        // Initial render
        renderTabs();
        renderContent();
    </script>
</body>
</html>"""

    def navigate(self, url):
        """Navigate to a URL"""
        pass

    def new_tab(self):
        """Create a new tab"""
        pass

    def close_tab(self, tab_id):
        """Close a tab"""
        pass

    def switch_tab(self, tab_id):
        """Switch to a different tab"""
        pass

    def load_page(self, url):
        """Load page in webview - loads the full page content"""
        try:
            self.window.load_url(url)
        except Exception as e:
            print(f"Error loading {url}: {e}")

    def get_suggestions(self, query):
        """Return smart suggestions based on query"""
        suggestions = []
        
        # Quick suggestions
        quick_sites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'github': 'https://www.github.com',
            'stack': 'https://www.stackoverflow.com',
            'mail': 'https://mail.google.com',
            'chat': 'https://chat.openai.com',
            'drive': 'https://drive.google.com',
            'docs': 'https://docs.google.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'reddit': 'https://www.reddit.com',
        }
        
        query_lower = query.lower()
        for key, url in quick_sites.items():
            if key.startswith(query_lower):
                suggestions.append(f"{key.capitalize()} - {url}")
        
        return suggestions[:5]


if __name__ == "__main__":
    app = Browser()
    webview.start()
