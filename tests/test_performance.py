#!/usr/bin/env python3
"""
性能测试
"""

import pytest
import sys
import os
import time
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestPerformanceMonitor:
    """测试性能监控器"""
    
    def test_monitor_initialization(self):
        """测试监控器初始化"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        assert monitor.metrics == {}
        assert monitor.start_times == {}
    
    def test_start_stop_timer(self):
        """测试计时器"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 开始计时
        monitor.start_timer("test_operation")
        assert "test_operation" in monitor.start_times
        
        # 等待一小段时间
        time.sleep(0.01)
        
        # 停止计时
        elapsed = monitor.stop_timer("test_operation")
        assert elapsed > 0
        assert "test_operation" not in monitor.start_times
        
        # 验证指标记录
        assert "test_operation" in monitor.metrics
        assert len(monitor.metrics["test_operation"]) == 1
        assert monitor.metrics["test_operation"][0] == elapsed
    
    def test_stop_nonexistent_timer(self):
        """测试停止不存在的计时器"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 停止不存在的计时器应该返回0
        elapsed = monitor.stop_timer("nonexistent")
        assert elapsed == 0.0
    
    def test_record_metric(self):
        """测试记录指标"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 记录指标
        monitor.record_metric("test_metric", 1.5)
        monitor.record_metric("test_metric", 2.5)
        
        assert "test_metric" in monitor.metrics
        assert monitor.metrics["test_metric"] == [1.5, 2.5]
    
    def test_get_stats(self):
        """测试获取统计信息"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 记录一些数据
        monitor.record_metric("test", 1.0)
        monitor.record_metric("test", 2.0)
        monitor.record_metric("test", 3.0)
        
        stats = monitor.get_stats("test")
        
        assert stats["count"] == 3
        assert stats["total"] == 6.0
        assert stats["mean"] == 2.0
        assert stats["min"] == 1.0
        assert stats["max"] == 3.0
        assert stats["last"] == 3.0
    
    def test_get_stats_empty(self):
        """测试获取空指标的统计信息"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        stats = monitor.get_stats("nonexistent")
        assert stats == {}
    
    def test_get_all_stats(self):
        """测试获取所有统计信息"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 记录多个指标
        monitor.record_metric("metric1", 1.0)
        monitor.record_metric("metric2", 2.0)
        
        all_stats = monitor.get_all_stats()
        
        assert "metric1" in all_stats
        assert "metric2" in all_stats
        assert all_stats["metric1"]["mean"] == 1.0
        assert all_stats["metric2"]["mean"] == 2.0
    
    def test_reset(self):
        """测试重置"""
        from ai_cli.core.performance import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        # 记录一些数据
        monitor.record_metric("test", 1.0)
        monitor.start_timer("timer")
        
        # 重置
        monitor.reset()
        
        assert monitor.metrics == {}
        assert monitor.start_times == {}

class TestPerformanceDecorators:
    """测试性能装饰器"""
    
    def test_measure_performance_decorator(self):
        """测试性能测量装饰器"""
        from ai_cli.core.performance import measure_performance, PerformanceMonitor
        
        # 创建全局监控器
        from ai_cli.core.performance import monitor
        
        # 保存原始状态
        original_metrics = monitor.metrics.copy()
        
        @measure_performance("decorated_function")
        def test_function():
            time.sleep(0.01)
            return "result"
        
        # 调用函数
        result = test_function()
        assert result == "result"
        
        # 验证指标记录
        assert "decorated_function" in monitor.metrics
        assert len(monitor.metrics["decorated_function"]) == 1
        assert monitor.metrics["decorated_function"][0] > 0
        
        # 清理
        monitor.metrics = original_metrics
    
    def test_cache_result_decorator(self):
        """测试缓存结果装饰器"""
        from ai_cli.core.performance import cache_result
        
        call_count = 0
        
        @cache_result(ttl=1)  # 1秒缓存
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # 第一次调用
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # 第二次调用（应该使用缓存）
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # 调用次数不应增加
        
        # 不同参数（应该重新计算）
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2
    
    def test_cache_expiration(self):
        """测试缓存过期"""
        from ai_cli.core.performance import cache_result
        import time
        
        call_count = 0
        
        @cache_result(ttl=0.1)  # 0.1秒缓存
        def test_function():
            nonlocal call_count
            call_count += 1
            return call_count
        
        # 第一次调用
        result1 = test_function()
        assert result1 == 1
        
        # 立即再次调用（使用缓存）
        result2 = test_function()
        assert result2 == 1
        assert call_count == 1
        
        # 等待缓存过期
        time.sleep(0.2)
        
        # 再次调用（应该重新计算）
        result3 = test_function()
        assert result3 == 2
        assert call_count == 2

class TestProgressManager:
    """测试进度管理器"""
    
    @patch('ai_cli.core.performance.Progress')
    def test_progress_manager(self, mock_progress):
        """测试进度管理器"""
        from ai_cli.core.performance import ProgressManager
        
        # 模拟Progress
        mock_progress_instance = Mock()
        mock_progress.return_value = mock_progress_instance
        
        manager = ProgressManager()
        
        # 测试开始进度
        progress = manager.start_progress("测试任务")
        assert progress == mock_progress_instance
        assert manager.progress == mock_progress_instance
        
        # 测试添加任务
        mock_progress_instance.add_task.return_value = "task_id"
        task_id = manager.add_task("子任务", 100)
        assert task_id == "task_id"
        assert "子任务" in manager.task_ids
        
        # 测试更新任务
        manager.update_task("子任务", 50)
        mock_progress_instance.update.assert_called_with("task_id", advance=50)
        
        # 测试完成任务
        manager.complete_task("子任务")
        mock_progress_instance.update.assert_called_with("task_id", completed=100)
        
        # 测试停止进度
        manager.stop_progress()
        mock_progress_instance.stop.assert_called_once()
        assert manager.progress is None
        assert manager.task_ids == {}
    
    @patch('ai_cli.core.performance.Progress')
    def test_with_progress_decorator(self, mock_progress):
        """测试带进度显示的装饰器"""
        from ai_cli.core.performance import with_progress
        
        # 模拟Progress
        mock_progress_instance = Mock()
        mock_progress_instance.add_task.return_value = "task_id"
        mock_progress.return_value = mock_progress_instance
        
        @with_progress("测试任务")
        def test_function(progress=None):
            # 装饰器会传递progress参数
            assert progress is not None
            progress.update_task("测试任务", 50)
            return "result"
        
        # 调用函数
        result = test_function()
        assert result == "result"
        
        # 验证进度管理
        mock_progress_instance.start.assert_called_once()
        mock_progress_instance.stop.assert_called_once()

class TestSystemMetrics:
    """测试系统指标"""
    
    @patch('ai_cli.core.performance.psutil')
    def test_memory_usage_with_psutil(self, mock_psutil):
        """测试内存使用情况（有psutil）"""
        from ai_cli.core.performance import memory_usage
        
        # 模拟psutil
        mock_process = Mock()
        mock_memory_info = Mock()
        mock_memory_info.rss = 1024 * 1024 * 100  # 100MB
        mock_memory_info.vms = 1024 * 1024 * 200  # 200MB
        mock_process.memory_info.return_value = mock_memory_info
        mock_process.memory_percent.return_value = 50.0
        mock_psutil.Process.return_value = mock_process
        
        usage = memory_usage()
        
        assert usage["rss_mb"] == 100.0
        assert usage["vms_mb"] == 200.0
        assert usage["percent"] == 50.0
    
    @patch('ai_cli.core.performance.psutil', None)
    def test_memory_usage_without_psutil(self):
        """测试内存使用情况（无psutil）"""
        from ai_cli.core.performance import memory_usage
        
        usage = memory_usage()
        
        assert "error" in usage
        assert "psutil" in usage["error"]
    
    @patch('ai_cli.core.performance.psutil')
    def test_system_resources(self, mock_psutil):
        """测试系统资源"""
        from ai_cli.core.performance import system_resources
        
        # 模拟系统资源
        mock_psutil.cpu_percent.return_value = 25.0
        mock_psutil.cpu_count.return_value = 8
        
        mock_memory = Mock()
        mock_memory.total = 1024 * 1024 * 1024 * 16  # 16GB
        mock_memory.available = 1024 * 1024 * 1024 * 8  # 8GB
        mock_memory.percent = 50.0
        mock_psutil.virtual_memory.return_value = mock_memory
        
        mock_disk = Mock()
        mock_disk.total = 1024 * 1024 * 1024 * 500  # 500GB
        mock_disk.free = 1024 * 1024 * 1024 * 200  # 200GB
        mock_disk.percent = 60.0
        mock_psutil.disk_usage.return_value = mock_disk
        
        resources = system_resources()
        
        assert resources["cpu_percent"] == 25.0
        assert resources["cpu_count"] == 8
        assert resources["memory_total_gb"] == 16.0
        assert resources["memory_available_gb"] == 8.0
        assert resources["memory_percent"] == 50.0
        assert resources["disk_total_gb"] == 500.0
        assert resources["disk_free_gb"] == 200.0
        assert resources["disk_percent"] == 60.0
    
    @patch('ai_cli.core.performance.psutil', None)
    def test_system_resources_without_psutil(self):
        """测试系统资源（无psutil）"""
        from ai_cli.core.performance import system_resources
        
        resources = system_resources()
        
        assert "error" in resources
        assert "psutil" in resources["error"]

class TestPerformanceCommands:
    """测试性能命令"""
    
    @patch('ai_cli.core.performance.console')
    def test_show_performance_report(self, mock_console):
        """测试显示性能报告"""
        from ai_cli.core.performance import show_performance_report, monitor
        
        # 模拟控制台
        mock_print = Mock()
        mock_console.print = mock_print
        
        # 记录一些指标
        monitor.record_metric("test_metric", 1.0)
        
        # 显示报告
        show_performance_report()
        
        # 验证调用了打印
        assert mock_print.called
    
    @patch('ai_cli.core.performance.console')
    def test_show_system_resources(self, mock_console):
        """测试显示系统资源"""
        from ai_cli.core.performance import show_system_resources
        
        # 模拟控制台
        mock_print = Mock()
        mock_console.print = mock_print
        
        # 显示资源（可能失败，但不应抛出异常）
        show_system_resources()
        
        # 验证调用了打印
        assert mock_print.called

class TestPerformanceIntegration:
    """测试性能集成"""
    
    def test_optimize_startup(self):
        """测试启动优化"""
        from ai_cli.core.performance import optimize_startup
        
        metrics = optimize_startup()
        
        assert isinstance(metrics, dict)
        assert "import_times" in metrics
        assert "total_startup" in metrics
        
        import_times = metrics["import_times"]
        assert isinstance(import_times, dict)
        
        total_time = metrics["total_startup"]
        assert isinstance(total_time, float)
        assert total_time >= 0
    
    def test_performance_module_imports(self):
        """测试性能模块导入"""
        # 确保所有必要的模块可以导入
        modules = [
            "ai_cli.core.performance",
        ]
        
        for module_name in modules:
            try:
                __import__(module_name)
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")
        
        assert True

def test_performance_benchmark():
    """性能基准测试"""
    from ai_cli.core.performance import measure_performance, monitor
    
    # 保存原始状态
    original_metrics = monitor.metrics.copy()
    
    @measure_performance("benchmark_test")
    def benchmark_function():
        # 模拟一些工作
        total = 0
        for i in range(1000):
            total += i
        return total
    
    # 运行基准测试
    start_time = time.perf_counter()
    result = benchmark_function()
    end_time = time.perf_counter()
    
    elapsed = end_time - start_time
    assert elapsed < 0.1  # 应该在0.1秒内完成
    assert result == sum(range(1000))
    
    # 验证性能指标
    assert "benchmark_test" in monitor.metrics
    assert len(monitor.metrics["benchmark_test"]) == 1
    
    # 清理
    monitor.metrics = original_metrics

if __name__ == "__main__":
    # 直接运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))