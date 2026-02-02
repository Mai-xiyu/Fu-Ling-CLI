"""
代码生成命令 - 基于AI生成代码
"""

import click

@click.command()
@click.argument('specification')
@click.option('--language', '-l', default='python', help='编程语言')
@click.option('--output', '-o', type=click.Path(), help='输出文件')
@click.option('--template', '-t', help='代码模板')
def generate(specification, language, output, template):
    """基于AI生成代码
    
    \b
    示例:
      ai generate "python function to add two numbers"
      ai generate "react button component" -l javascript
      ai generate "sql users table" -l sql -o schema.sql
      ai generate "fastapi endpoint for users" -t restapi
    """
    try:
        from ..core.ai import chat_completion
        
        # 构建提示
        prompt = f"生成{language}代码: {specification}"
        if template:
            prompt += f"\n使用模板: {template}"
        
        messages = [
            {
                "role": "system",
                "content": f"""你是一个专业的{language}开发专家。
                根据用户需求生成高质量、可运行的代码。
                只返回代码，不要解释，不要markdown格式。
                确保代码符合最佳实践和安全规范。"""
            },
            {"role": "user", "content": prompt}
        ]
        
        click.echo("🤖 正在生成代码...")
        
        # 获取AI生成的代码
        code = chat_completion(messages)
        
        # 清理代码（移除可能的markdown）
        if code.startswith('```'):
            lines = code.split('\n')
            if len(lines) >= 3:
                code = '\n'.join(lines[1:-1])
        
        # 输出结果
        if output:
            with open(output, 'w') as f:
                f.write(code)
            click.echo(f"✅ 代码已保存到: {output}")
        else:
            click.echo("\n" + "=" * 50)
            click.echo(f"📝 生成的{language}代码:")
            click.echo("=" * 50)
            click.echo(code)
            click.echo("=" * 50)
            
            # 提供使用建议
            click.echo("\n💡 使用建议:")
            click.echo(f"  保存到文件: ai generate \"{specification}\" -o output.{language}")
            click.echo(f"  直接运行: python -c \"{code[:100]}...\"")
        
    except Exception as e:
        click.echo(f"❌ 代码生成失败: {e}")

@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--focus', '-f', help='重点重构区域')
@click.option('--apply', is_flag=True, help='直接应用更改')
def refactor(file, focus, apply):
    """重构代码文件
    
    \b
    示例:
      ai refactor utils.py
      ai refactor api.py --focus "error handling"
      ai refactor main.py --apply  # 直接应用更改
    """
    try:
        # 读取文件
        with open(file, 'r') as f:
            original_code = f.read()
        
        from ..core.ai import chat_completion
        
        # 构建提示
        prompt = f"分析并重构以下{file}代码，提供改进建议:"
        if focus:
            prompt += f"\n重点关注: {focus}"
        
        prompt += f"\n\n代码:\n```\n{original_code[:2000]}\n```"
        
        messages = [
            {
                "role": "system",
                "content": """你是一个代码重构专家。
                分析代码并提供具体的重构建议。
                包括：代码质量、性能、可读性、安全性。
                提供具体的代码示例和解释。"""
            },
            {"role": "user", "content": prompt}
        ]
        
        click.echo(f"🔍 分析 {file}...")
        
        # 获取重构建议
        suggestions = chat_completion(messages)
        
        click.echo("\n" + "=" * 50)
        click.echo(f"📋 {file} 重构建议:")
        click.echo("=" * 50)
        click.echo(suggestions)
        click.echo("=" * 50)
        
        if apply:
            click.echo("\n⚠️  注意: --apply 选项需要手动实现")
            click.echo("   当前版本仅提供建议，不自动修改文件")
            click.echo("   请手动应用建议的更改")
        
        # 提供下一步建议
        click.echo("\n💡 下一步:")
        click.echo(f"   1. 查看具体建议")
        click.echo(f"   2. 手动应用需要的更改")
        click.echo(f"   3. 运行测试确保功能正常")
        click.echo(f"   4. 提交更改: git commit -m 'refactor: {file}'")
        
    except Exception as e:
        click.echo(f"❌ 代码重构失败: {e}")

# 注册到CLI
def register_commands(cli):
    """注册生成命令"""
    cli.add_command(generate)
    cli.add_command(refactor)