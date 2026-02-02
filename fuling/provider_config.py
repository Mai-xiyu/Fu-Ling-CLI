"""
提供商配置管理
"""

import os
import click
from typing import Dict, Any
from .fuling_core import config, get_config

def configure_provider_interactive():
    """交互式配置AI提供商"""
    click.echo("🎯 配置AI提供商")
    click.echo("=" * 40)
    
    # 检查当前配置
    current_config = get_config()
    current_provider = current_config.get('model', {}).get('provider', 'local')
    current_model = current_config.get('model', {}).get('name', 'unknown')
    
    click.echo(f"当前提供商: {current_provider}")
    click.echo(f"当前模型: {current_model}")
    
    # 显示选项
    click.echo("\n可选提供商:")
    click.echo("  1. Moonshot (Kimi) - 推荐，中文优化")
    click.echo("  2. OpenAI - ChatGPT兼容")
    click.echo("  3. 本地模式 - 无需API密钥")
    click.echo("  4. 退出配置")
    
    while True:
        choice = click.prompt("\n请选择 (1-4)", type=int)
        
        if choice == 1:
            configure_moonshot()
            break
        elif choice == 2:
            configure_openai()
            break
        elif choice == 3:
            configure_local()
            break
        elif choice == 4:
            click.echo("配置取消")
            return
        else:
            click.echo("无效选择，请重试")

def configure_moonshot():
    """配置Moonshot提供商"""
    click.echo("\n🔧 配置Moonshot (Kimi)")
    click.echo("-" * 30)
    
    # 检查环境变量
    api_key = os.environ.get('MOONSHOT_API_KEY')
    
    if api_key:
        click.echo(f"✅ 检测到环境变量 MOONSHOT_API_KEY: {api_key[:8]}****")
        use_env = click.confirm("使用环境变量中的API密钥？", default=True)
    else:
        click.echo("⚠️  未检测到MOONSHOT_API_KEY环境变量")
        use_env = False
    
    if use_env:
        api_key = "${MOONSHOT_API_KEY}"
    else:
        api_key = click.prompt("请输入Moonshot API密钥", hide_input=True)
        if not api_key.startswith("${") and not api_key.endswith("}"):
            # 不是环境变量格式，询问是否保存到环境
            save_to_env = click.confirm("是否保存为环境变量？", default=False)
            if save_to_env:
                os.environ['MOONSHOT_API_KEY'] = api_key
                click.echo("✅ 已设置环境变量 MOONSHOT_API_KEY")
                api_key = "${MOONSHOT_API_KEY}"
    
    # 模型选择
    click.echo("\n可选模型:")
    click.echo("  1. kimi-k2-turbo-preview (推荐)")
    click.echo("  2. moonshot-v1-8k")
    click.echo("  3. moonshot-v1-32k")
    click.echo("  4. moonshot-v1-128k")
    
    model_choice = click.prompt("选择模型", type=int, default=1)
    
    models = {
        1: "kimi-k2-turbo-preview",
        2: "moonshot-v1-8k",
        3: "moonshot-v1-32k",
        4: "moonshot-v1-128k",
    }
    
    model_name = models.get(model_choice, "kimi-k2-turbo-preview")
    
    # 更新配置
    update_config = get_config()
    update_config['model'] = {
        "provider": "moonshot",
        "name": model_name,
        "api_key": api_key,
        "base_url": "https://api.moonshot.cn/v1",
        "temperature": 0.3,
        "max_tokens": 1000,
        "timeout": 30,
    }
    
    config.save_config(update_config)
    
    click.echo(f"\n✅ Moonshot配置完成")
    click.echo(f"   模型: {model_name}")
    click.echo(f"   API密钥: {'环境变量' if api_key.startswith('${') else '直接配置'}")
    
    # 测试连接
    if click.confirm("是否测试连接？", default=True):
        test_moonshot_connection(api_key if not api_key.startswith("${") else os.environ.get('MOONSHOT_API_KEY'))

def configure_openai():
    """配置OpenAI提供商"""
    click.echo("\n🔧 配置OpenAI")
    click.echo("-" * 30)
    
    # 检查环境变量
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if api_key:
        click.echo(f"✅ 检测到环境变量 OPENAI_API_KEY: {api_key[:8]}****")
        use_env = click.confirm("使用环境变量中的API密钥？", default=True)
    else:
        click.echo("⚠️  未检测到OPENAI_API_KEY环境变量")
        use_env = False
    
    if use_env:
        api_key = "${OPENAI_API_KEY}"
    else:
        api_key = click.prompt("请输入OpenAI API密钥", hide_input=True)
        if not api_key.startswith("${") and not api_key.endswith("}"):
            save_to_env = click.confirm("是否保存为环境变量？", default=False)
            if save_to_env:
                os.environ['OPENAI_API_KEY'] = api_key
                click.echo("✅ 已设置环境变量 OPENAI_API_KEY")
                api_key = "${OPENAI_API_KEY}"
    
    # 模型选择
    click.echo("\n可选模型:")
    click.echo("  1. gpt-3.5-turbo (经济)")
    click.echo("  2. gpt-4 (更智能)")
    click.echo("  3. gpt-4-turbo (最新)")
    click.echo("  4. 自定义模型")
    
    model_choice = click.prompt("选择模型", type=int, default=1)
    
    if model_choice == 1:
        model_name = "gpt-3.5-turbo"
    elif model_choice == 2:
        model_name = "gpt-4"
    elif model_choice == 3:
        model_name = "gpt-4-turbo"
    else:
        model_name = click.prompt("请输入模型名称", default="gpt-3.5-turbo")
    
    # 组织ID（可选）
    organization = click.prompt("组织ID (可选，按Enter跳过)", default="", show_default=False)
    
    # 更新配置
    update_config = get_config()
    update_config['model'] = {
        "provider": "openai",
        "name": model_name,
        "api_key": api_key,
        "base_url": "https://api.openai.com/v1",
        "organization": organization if organization else "",
        "temperature": 0.3,
        "max_tokens": 1000,
        "timeout": 30,
    }
    
    config.save_config(update_config)
    
    click.echo(f"\n✅ OpenAI配置完成")
    click.echo(f"   模型: {model_name}")
    click.echo(f"   API密钥: {'环境变量' if api_key.startswith('${') else '直接配置'}")
    
    # 测试连接
    if click.confirm("是否测试连接？", default=True):
        test_openai_connection(api_key if not api_key.startswith("${") else os.environ.get('OPENAI_API_KEY'))

def configure_local():
    """配置本地模式"""
    click.echo("\n🔧 配置本地模式")
    click.echo("-" * 30)
    
    click.echo("本地模式无需API密钥，提供基础功能：")
    click.echo("  • 命令解释（本地知识库）")
    click.echo("  • 基础代码生成")
    click.echo("  • 命令建议")
    click.echo("  • 系统状态")
    
    # 更新配置
    update_config = get_config()
    update_config['model'] = {
        "provider": "local",
        "name": "local",
        "api_key": "",
        "temperature": 0.3,
        "max_tokens": 1000,
    }
    
    config.save_config(update_config)
    
    click.echo("\n✅ 本地模式配置完成")
    click.echo("💡 提示: 随时可以运行 'fl config provider' 切换为AI模式")

def test_moonshot_connection(api_key: str):
    """测试Moonshot连接"""
    if not api_key:
        click.echo("❌ 无法测试：API密钥为空")
        return
    
    click.echo("\n🔗 测试Moonshot连接...")
    
    try:
        import requests
        
        url = "https://api.moonshot.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "kimi-k2-turbo-preview",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10,
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            click.echo("✅ Moonshot连接测试成功")
        elif response.status_code == 401:
            click.echo("❌ API密钥无效")
        elif response.status_code == 429:
            click.echo("⚠️  请求频率超限")
        else:
            click.echo(f"❌ 连接测试失败: HTTP {response.status_code}")
            
    except Exception as e:
        click.echo(f"❌ 连接测试异常: {e}")

def test_openai_connection(api_key: str):
    """测试OpenAI连接"""
    if not api_key:
        click.echo("❌ 无法测试：API密钥为空")
        return
    
    click.echo("\n🔗 测试OpenAI连接...")
    
    try:
        import requests
        
        url = "https://api.openai.com/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            click.echo("✅ OpenAI连接测试成功")
        elif response.status_code == 401:
            click.echo("❌ API密钥无效")
        elif response.status_code == 429:
            click.echo("⚠️  请求频率超限")
        else:
            click.echo(f"❌ 连接测试失败: HTTP {response.status_code}")
            
    except Exception as e:
        click.echo(f"❌ 连接测试异常: {e}")

def show_provider_status():
    """显示提供商状态"""
    current_config = get_config()
    model_config = current_config.get('model', {})
    provider = model_config.get('provider', 'local')
    model_name = model_config.get('name', 'unknown')
    
    click.echo("📊 AI提供商状态")
    click.echo("=" * 40)
    
    click.echo(f"当前提供商: {provider}")
    click.echo(f"当前模型: {model_name}")
    
    # 检查API密钥
    if provider == 'moonshot':
        api_key = model_config.get('api_key', '')
        if api_key.startswith("${") and api_key.endswith("}"):
            env_var = api_key[2:-1]
            actual_key = os.environ.get(env_var)
            if actual_key:
                click.echo(f"API密钥: 环境变量 {env_var} ({actual_key[:8]}****)")
            else:
                click.echo(f"API密钥: ❌ 环境变量 {env_var} 未设置")
        elif api_key:
            click.echo(f"API密钥: 直接配置 ({api_key[:8]}****)")
        else:
            click.echo("API密钥: ❌ 未设置")
            
    elif provider == 'openai':
        api_key = model_config.get('api_key', '')
        if api_key.startswith("${") and api_key.endswith("}"):
            env_var = api_key[2:-1]
            actual_key = os.environ.get(env_var)
            if actual_key:
                click.echo(f"API密钥: 环境变量 {env_var} ({actual_key[:8]}****)")
            else:
                click.echo(f"API密钥: ❌ 环境变量 {env_var} 未设置")
        elif api_key:
            click.echo(f"API密钥: 直接配置 ({api_key[:8]}****)")
        else:
            click.echo("API密钥: ❌ 未设置")
            
    else:
        click.echo("API密钥: 本地模式无需API密钥")
    
    # 测试连接按钮
    click.echo("\n💡 操作:")
    click.echo("  运行 'fl config provider' 切换提供商")
    click.echo("  运行 'fl explain 命令' 测试功能")
    click.echo("  运行 'fl power' 查看详细状态")