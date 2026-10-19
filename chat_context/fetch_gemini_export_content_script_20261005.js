Title: Live Content

Description: Fetched live

Source: https://raw.githubusercontent.com/jujusharp/gemini-export/main/src/content/content_script.js

---

(function () {
    'use strict';

    // Added for Chrome Extension compatibility
    const GM_addStyle = (css) => {
        const style = document.createElement('style');
        style.innerText = css;
        document.head.appendChild(style);
    };

    // Listen for messages from the popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'TOGGLE_PANEL') {
            // Need to ensure UI is created first, though it should be by the timeout
            if (typeof togglePanel === 'function') {
                togglePanel();
                sendResponse({ status: 'success' });
            } else {
                console.warn('togglePanel function not found or UI not ready');
                sendResponse({ status: 'error', message: 'UI not ready' });
            }
        }
        // Return true if we want to sendResponse asynchronously, but here we are synchronous
    });

    window.GeminiExportBootstrap?.setupTrustedTypes?.();

    // --- HTML to Markdown 转换 ---
    let markdownConverter = null;

    function getMarkdownConverter() {
        if (markdownConverter) return markdownConverter;

        const factory = window.GeminiExportMarkdown?.createMarkdownConverter;
        if (typeof factory !== 'function') {
            console.warn('Gemini Export: markdown converter module not loaded.');
            return null;
        }

        markdownConverter = factory();
        return markdownConverter;
    }

    function cleanupMarkdown(text) {
        const converter = getMarkdownConverter();
        if (converter && typeof converter.cleanupMarkdown === 'function') {
            return converter.cleanupMarkdown(text);
        }
        if (!text) return '';
        return String(text).trim();
    }

    function htmlToMarkdown(element) {
        if (!element) return '';

        const converter = getMarkdownConverter();
        if (converter && typeof converter.htmlToMarkdown === 'function') {
            return converter.htmlToMarkdown(element);
        }

        return cleanupMarkdown(element.innerText?.trim() || '');
    }

    // --- Language & Translations ---
    const t = window.GeminiExportI18n?.getTranslations
        ? window.GeminiExportI18n.getTranslations({ language: navigator.language })
        : {};
    const currentPlatform = window.GeminiExportPlatforms?.detectPlatformFromLocation
        ? window.GeminiExportPlatforms.detectPlatformFromLocation(window.location)
        : { id: 'generic', label: 'Chat', defaultProjectName: 'AIChat', messageSelectors: {}, capabilities: { canvas: false } };

    const exportTimeout = 3000;
    const SCROLL_DELAY_MS = 1000;
    const MAX_SCROLL_ATTEMPTS = 300;
    const SCROLL_INCREMENT_FACTOR = 0.85;
    const SCROLL_STABILITY_CHECKS = 3;

    if (!window.__GEMINI_EXPORT_FORMAT) { window.__GEMINI_EXPORT_FORMAT = 'md'; }

    // --- 动态选择器配置 ---
    const DEFAULT_SELECTORS = { ...(currentPlatform.messageSelectors || {}) };

    const loadSelectorConfig = window.GeminiExportBootstrap?.loadSelectorConfig;
    let SELECTORS = typeof loadSelectorConfig === 'function'
        ? loadSelectorConfig(DEFAULT_SELECTORS, {
            storageKey: 'gemini_export_selectors',
            loadedLog: 'Gemini Export: 已加载自定义选择器',
            failedLog: 'Gemini Export: 加载自定义选择器失败'
        })
        : { ...DEFAULT_SELECTORS };

    // --- 脚本内部状态变量 ---
    let isScrolling = false;
    let collectedData = new Map();
    let scrollCount = 0;
    let noChangeCounter = 0;

    // --- UI 界面元素变量 ---
    let uiController = null;
    let anchorPanelController = null;
    let imageExporter = null;
    let exportPipeline = null;
    let exportHandlers = null;
    let exportDispatcher = null;
    let scrollEngine = null;
    let themeSyncController = null;

    // Previous panel vars removed

    // --- 辅助工具函数 ---
    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function startThemeSync() {
        if (!themeSyncController) {
            const factory = window.GeminiExportThemeSync?.createThemeSyncController;
            if (typeof factory !== 'function') {
                console.warn('Gemini Export: theme sync module not loaded.');
                return;
            }
            themeSyncController = factory();
        }

        if (typeof themeSyncController.startThemeSync === 'function') {
            themeSyncController.startThemeSync();
        }
    }

    function getCurrentTimestamp() {


