/**
 * 主题切换JavaScript
 * 
 * 实现明暗主题切换功能，包括：
 * - localStorage持久化存储
 * - 系统主题偏好检测
 * - 平滑的主题切换动画
 */

class ThemeManager {
    constructor() {
        this.currentTheme = this.getTheme();
        this.init();
    }

    /**
     * 初始化主题
     */
    init() {
        this.applyTheme(this.currentTheme);
        this.setupEventListeners();
        
        // 延迟更新图标，确保DOM已完全加载
        requestAnimationFrame(() => {
            this.updateToggleIcon();
        });
    }

    /**
     * 获取当前主题
     * 优先级：localStorage > 系统偏好 > 默认浅色
     */
    getTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        return this.getSystemTheme() || 'light';
    }

    /**
     * 获取系统主题偏好
     */
    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
            return 'light';
        }
        return null;
    }

    /**
     * 切换主题
     */
    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    /**
     * 设置主题
     */
    setTheme(theme) {
        this.currentTheme = theme;
        this.saveTheme(theme);
        this.applyTheme(theme);
        this.updateToggleIcon();
        this.dispatchThemeEvent(theme);
    }

    /**
     * 保存主题到localStorage
     */
    saveTheme(theme) {
        localStorage.setItem('theme', theme);
    }

    /**
     * 应用主题到document
     */
    applyTheme(theme) {
        const html = document.documentElement;
        if (theme === 'light') {
            html.setAttribute('data-theme', 'light');
        } else {
            html.removeAttribute('data-theme');
        }
    }

    /**
     * 更新图标（在DOM加载后调用）
     */
    updateToggleIcon() {
        const toggleBtn = document.querySelector('.theme-toggle i');
        if (!toggleBtn) return;

        if (this.currentTheme === 'dark') {
            toggleBtn.classList.remove('fa-sun');
            toggleBtn.classList.add('fa-moon');
        } else {
            toggleBtn.classList.remove('fa-moon');
            toggleBtn.classList.add('fa-sun');
        }
    }

    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        const toggleBtn = document.querySelector('.theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleTheme());
        }

        this.setupSystemThemeListener();
    }

    /**
     * 监听系统主题变化
     */
    setupSystemThemeListener() {
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            const lightModeQuery = window.matchMedia('(prefers-color-scheme: light)');

            darkModeQuery.addEventListener('change', (e) => {
                if (!localStorage.getItem('theme')) {
                    this.setTheme('dark');
                }
            });

            lightModeQuery.addEventListener('change', (e) => {
                if (!localStorage.getItem('theme')) {
                    this.setTheme('light');
                }
            });
        }
    }

    /**
     * 触发主题切换事件
     */
    dispatchThemeEvent(theme) {
        const event = new CustomEvent('themechange', {
            detail: { theme }
        });
        document.dispatchEvent(event);
    }

    /**
     * 获取当前主题
     */
    getCurrentTheme() {
        return this.currentTheme;
    }

    /**
     * 重置主题
     */
    resetTheme() {
        localStorage.removeItem('theme');
        const systemTheme = this.getSystemTheme() || 'dark';
        this.setTheme(systemTheme);
    }
}

// 创建主题管理器实例
const themeManager = new ThemeManager();

// 导出到全局
window.themeManager = themeManager;
