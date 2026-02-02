"""
性能监控和优化模块
"""

import time
import functools
import sys
import os
from typing import Dict, Any, Callable, Optional
from collections import defaultdict
import threading
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_times = {}
        self.lock = threading.Lock()
        
    def start_timer(self, name: str):
        """开始计时"""
        self.start_times[name] = time.perf_counter()
        
    def stop_timer(self, name: str) -> float:
        """停止计时并返回耗时"""
        if name not in self.start_times:
            return 0.0
            
        elapsed = time.perf_counter() - self.start_times[name]
        with self.lock:
            self.metrics[name].append(elapsed)
        del self.start_times[name]
        return elapsed
    
    def record_metric(self, name: str, value: float):
        """记录指标"""
        with self.lock:
            self.metrics[name].append(value)
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """获取统计信息"""
        if name not in self.metrics or not self.metrics[name]:
            return {}
            
        values = self.metrics[name]
        return {
            'count': len(values),
            'total': sum(values),
            'mean': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'last': values[-1] if values else 0,
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """获取所有指标的统计信息"""
        stats = {}
        for name in self.metrics:
            stats[name] = self.get_stats(name)
        return stats
    
    def reset(self):
        """重置所有指标"""
        with self.lock:
            self.metrics.clear()
            self.start_times.clear()

# 全局性能监控器
monitor = PerformanceMonitor()

def measure_performance(name: str):
    """性能测量装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            monitor.start_timer(name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = monitor.stop_timer(name)
                if elapsed > 0.1:  # 只记录耗时较长的操作
                    console.print(f"[dim]⏱️  {name}: {elapsed:.3f}s[/]")
        return wrapper
    return decorator

def show_performance_report():
    """显示性能报告"""
    stats = monitor.get_all_stats()
    
    if not stats:
        console.print("[dim]No performance data available[/]")
        return
    
    table = Table(title="Performance Report")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")
    table.add_column("Total", style="dim")
    table.add_column("Avg", style="yellow")
    table.add_column("Min", style="dim")
    table.add_column("Max", style="dim")
    table.add_column("Last", style="bold")
    
    for name, metric_stats in sorted(stats.items()):
        table.add_row(
            name,
            str(metric_stats['count']),
            f"{metric_stats['total']:.3f}s",
            f"{metric_stats['mean']:.3f}s",
            f"{metric_stats['min']:.3f}s",
            f"{metric_stats['max']:.3f}s",
            f"{metric_stats['last']:.3f}s",
        )
    
    console.print(table)

def optimize_startup():
    """优化启动性能"""
    
    startup_metrics = {}
    
    # 测量导入时间
    import_times = {}
    
    # 关键模块导入
    modules_to_import = [
        'click',
        'rich',
        'yaml',
        'ai_cli.core.config',
        'ai_cli.core.context',
    ]
    
    for module_name in modules_to_import:
        start = time.perf_counter()
        try:
            __import__(module_name)
            import_times[module_name] = time.perf_counter() - start
        except ImportError:
            import_times[module_name] = -1
    
    startup_metrics['import_times'] = import_times
    
    # 总启动时间
    total_startup = sum(t for t in import_times.values() if t > 0)
    startup_metrics['total_startup'] = total_startup
    
    return startup_metrics

class ProgressManager:
    """进度管理器"""
    
    def __init__(self):
        self.progress = None
        self.task_ids = {}
        
    def start_progress(self, title: str = "Processing..."):
        """开始进度显示"""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            transient=True,
        )
        self.progress.start()
        return self.progress
    
    def add_task(self, description: str, total: Optional[float] = 100) -> str:
        """添加任务"""
        if self.progress:
            task_id = self.progress.add_task(description, total=total)
            self.task_ids[description] = task_id
            return task_id
        return None
    
    def update_task(self, description: str, advance: float = 1):
        """更新任务进度"""
        if self.progress and description in self.task_ids:
            self.progress.update(self.task_ids[description], advance=advance)
    
    def complete_task(self, description: str):
        """完成任务"""
        if self.progress and description in self.task_ids:
            self.progress.update(self.task_ids[description], completed=100)
    
    def stop_progress(self):
        """停止进度显示"""
        if self.progress:
            self.progress.stop()
            self.progress = None
            self.task_ids.clear()

def with_progress(description: str):
    """带进度显示的装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            progress_mgr = ProgressManager()
            progress = progress_mgr.start_progress()
            task_id = progress_mgr.add_task(description)
            
            try:
                result = func(*args, **kwargs, progress=progress_mgr)
                progress_mgr.complete_task(description)
                return result
            finally:
                progress_mgr.stop_progress()
        return wrapper
    return decorator

def cache_result(ttl: int = 300):  # 5分钟缓存
    """缓存结果装饰器"""
    def decorator(func):
        cache = {}
        cache_times = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = (func.__name__, args, frozenset(kwargs.items()))
            
            current_time = time.time()
            
            # 检查缓存是否有效
            if key in cache:
                cache_time = cache_times[key]
                if current_time - cache_time < ttl:
                    console.print(f"[dim]📦 Using cached result for {func.__name__}[/]")
                    return cache[key]
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache[key] = result
            cache_times[key] = current_time
            
            return result
        
        return wrapper
    return decorator

def memory_usage() -> Dict[str, float]:
    """获取内存使用情况"""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # 常驻内存
            'vms_mb': memory_info.vms / 1024 / 1024,  # 虚拟内存
            'percent': process.memory_percent(),
        }
    except ImportError:
        return {'error': 'psutil not installed'}

def system_resources() -> Dict[str, Any]:
    """获取系统资源信息"""
    resources = {}
    
    try:
        import psutil
        
        # CPU使用率
        resources['cpu_percent'] = psutil.cpu_percent(interval=0.1)
        resources['cpu_count'] = psutil.cpu_count()
        
        # 内存使用
        memory = psutil.virtual_memory()
        resources['memory_total_gb'] = memory.total / 1024 / 1024 / 1024
        resources['memory_available_gb'] = memory.available / 1024 / 1024 / 1024
        resources['memory_percent'] = memory.percent
        
        # 磁盘使用
        disk = psutil.disk_usage('/')
        resources['disk_total_gb'] = disk.total / 1024 / 1024 / 1024
        resources['disk_free_gb'] = disk.free / 1024 / 1024 / 1024
        resources['disk_percent'] = disk.percent
        
    except ImportError:
        resources['error'] = 'psutil not installed'
    
    return resources

def show_system_resources():
    """显示系统资源信息"""
    resources = system_resources()
    
    if 'error' in resources:
        console.print(f"[yellow]⚠ {resources['error']}[/]")
        console.print("[dim]Install psutil for detailed system metrics[/]")
        return
    
    table = Table(title="System Resources")
    table.add_column("Resource", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Status", style="bold")
    
    # CPU
    cpu_percent = resources['cpu_percent']
    cpu_status = "✅" if cpu_percent < 80 else "⚠" if cpu_percent < 95 else "❌"
    table.add_row("CPU Usage", f"{cpu_percent:.1f}%", cpu_status)
    
    # 内存
    mem_percent = resources['memory_percent']
    mem_status = "✅" if mem_percent < 80 else "⚠" if mem_percent < 95 else "❌"
    table.add_row(
        "Memory Usage", 
        f"{mem_percent:.1f}% ({resources['memory_available_gb']:.1f}GB free)",
        mem_status
    )
    
    # 磁盘
    disk_percent = resources['disk_percent']
    disk_status = "✅" if disk_percent < 80 else "⚠" if disk_percent < 95 else "❌"
    table.add_row(
        "Disk Usage",
        f"{disk_percent:.1f}% ({resources['disk_free_gb']:.1f}GB free)",
        disk_status
    )
    
    console.print(table)