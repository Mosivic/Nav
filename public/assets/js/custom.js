// Tab 切换功能
$(document).ready(function() {
    $(document).on('click', '.tab-item', function(e) {
        e.preventDefault();
        const $this = $(this);
        const tabIndex = $this.data('tab');
        const $container = $this.closest('.tab-container');
        
        // 移除当前组内所有active类
        $container.find('.tab-item').removeClass('active');
        $container.find('.tab-content').removeClass('active');
        
        // 添加新的active类
        $this.addClass('active');
        $container.find(`.tab-content[data-tab="${tabIndex}"]`).addClass('active');
    });
});