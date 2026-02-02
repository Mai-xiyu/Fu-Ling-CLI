"""
团队协作功能 - 基础版本
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
import click

class TeamConfig:
    """团队配置管理"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "fuling"
        self.team_dir = self.config_dir / "team"
        self.team_config_file = self.team_dir / "config.json"
        self.shared_config_file = self.team_dir / "shared.json"
        
        # 创建目录
        self.team_dir.mkdir(parents=True, exist_ok=True)
    
    def init_team(self, team_name: str, description: str = "") -> bool:
        """初始化团队"""
        team_config = {
            "team_name": team_name,
            "description": description,
            "created_at": self._current_timestamp(),
            "members": [],
            "shared_configs": {},
            "team_id": self._generate_team_id(team_name),
        }
        
        try:
            with open(self.team_config_file, 'w', encoding='utf-8') as f:
                json.dump(team_config, f, indent=2, ensure_ascii=False)
            
            click.echo(f"✅ 团队 '{team_name}' 初始化成功")
            click.echo(f"   团队ID: {team_config['team_id']}")
            return True
            
        except Exception as e:
            click.echo(f"❌ 团队初始化失败: {e}")
            return False
    
    def join_team(self, team_config_path: str) -> bool:
        """加入团队（通过配置文件）"""
        try:
            # 读取团队配置
            with open(team_config_path, 'r', encoding='utf-8') as f:
                team_config = json.load(f)
            
            # 保存到本地
            with open(self.team_config_file, 'w', encoding='utf-8') as f:
                json.dump(team_config, f, indent=2, ensure_ascii=False)
            
            click.echo(f"✅ 已加入团队: {team_config.get('team_name', '未知')}")
            return True
            
        except Exception as e:
            click.echo(f"❌ 加入团队失败: {e}")
            return False
    
    def export_config(self, config_type: str = "theme") -> Optional[str]:
        """导出配置"""
        from .fuling_core import get_config
        
        try:
            config = get_config()
            
            if config_type == "theme":
                export_data = {
                    "type": "theme",
                    "theme": config.get('theme', {}),
                    "exported_at": self._current_timestamp(),
                }
            elif config_type == "model":
                export_data = {
                    "type": "model",
                    "model": config.get('model', {}),
                    "exported_at": self._current_timestamp(),
                }
            elif config_type == "all":
                export_data = {
                    "type": "all",
                    "config": config,
                    "exported_at": self._current_timestamp(),
                }
            else:
                click.echo(f"❌ 不支持的配置类型: {config_type}")
                return None
            
            # 保存到团队共享目录
            filename = f"{config_type}_config_{self._current_timestamp()}.json"
            export_path = self.team_dir / filename
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            click.echo(f"✅ 配置已导出: {export_path}")
            return str(export_path)
            
        except Exception as e:
            click.echo(f"❌ 导出配置失败: {e}")
            return None
    
    def import_config(self, config_path: str) -> bool:
        """导入配置"""
        from .fuling_core import config as config_manager
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            config_type = import_data.get('type', 'unknown')
            current_config = config_manager.load_config()
            
            if config_type == "theme":
                current_config['theme'] = import_data.get('theme', {})
            elif config_type == "model":
                current_config['model'] = import_data.get('model', {})
            elif config_type == "all":
                current_config = import_data.get('config', {})
            else:
                click.echo(f"❌ 不支持的配置类型: {config_type}")
                return False
            
            # 保存配置
            config_manager.save_config(current_config)
            
            click.echo(f"✅ 配置已导入: {config_type}")
            return True
            
        except Exception as e:
            click.echo(f"❌ 导入配置失败: {e}")
            return False
    
    def share_command(self, command: str, description: str = "") -> bool:
        """分享命令到团队"""
        try:
            # 读取现有共享配置
            shared_commands = self._load_shared_commands()
            
            # 添加新命令
            command_entry = {
                "command": command,
                "description": description,
                "shared_at": self._current_timestamp(),
                "shared_by": os.environ.get('USER', 'unknown'),
            }
            
            shared_commands.append(command_entry)
            
            # 保存
            with open(self.shared_config_file, 'w', encoding='utf-8') as f:
                json.dump({"commands": shared_commands}, f, indent=2, ensure_ascii=False)
            
            click.echo(f"✅ 命令已分享: {command}")
            return True
            
        except Exception as e:
            click.echo(f"❌ 分享命令失败: {e}")
            return False
    
    def list_shared_commands(self) -> List[Dict]:
        """列出共享命令"""
        return self._load_shared_commands()
    
    def team_status(self) -> Dict[str, Any]:
        """获取团队状态"""
        try:
            if not self.team_config_file.exists():
                return {"status": "no_team", "message": "未加入任何团队"}
            
            with open(self.team_config_file, 'r', encoding='utf-8') as f:
                team_config = json.load(f)
            
            shared_commands = self._load_shared_commands()
            
            return {
                "status": "active",
                "team_name": team_config.get('team_name', '未知'),
                "team_id": team_config.get('team_id', '未知'),
                "member_count": len(team_config.get('members', [])),
                "shared_command_count": len(shared_commands),
                "created_at": team_config.get('created_at', '未知'),
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _load_shared_commands(self) -> List[Dict]:
        """加载共享命令"""
        try:
            if not self.shared_config_file.exists():
                return []
            
            with open(self.shared_config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data.get('commands', [])
            
        except Exception:
            return []
    
    def _current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _generate_team_id(self, team_name: str) -> str:
        """生成团队ID"""
        import uuid
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, team_name))[:8]

def team_cli():
    """团队CLI命令"""
    team = TeamConfig()
    
    click.echo("👥 符灵团队协作")
    click.echo("=" * 40)
    
    click.echo("\n📋 可用操作:")
    click.echo("  1. 初始化团队")
    click.echo("  2. 加入团队")
    click.echo("  3. 导出配置")
    click.echo("  4. 导入配置")
    click.echo("  5. 分享命令")
    click.echo("  6. 查看共享命令")
    click.echo("  7. 团队状态")
    click.echo("  8. 返回")
    
    choice = click.prompt("请选择", type=int)
    
    if choice == 1:
        team_name = click.prompt("团队名称")
        description = click.prompt("团队描述（可选）", default="", show_default=False)
        team.init_team(team_name, description)
        
    elif choice == 2:
        config_path = click.prompt("团队配置文件路径")
        team.join_team(config_path)
        
    elif choice == 3:
        click.echo("\n导出配置类型:")
        click.echo("  1. 主题配置")
        click.echo("  2. 模型配置")
        click.echo("  3. 全部配置")
        
        config_choice = click.prompt("选择", type=int)
        
        if config_choice == 1:
            team.export_config("theme")
        elif config_choice == 2:
            team.export_config("model")
        elif config_choice == 3:
            team.export_config("all")
            
    elif choice == 4:
        config_path = click.prompt("配置文件路径")
        team.import_config(config_path)
        
    elif choice == 5:
        command = click.prompt("要分享的命令")
        description = click.prompt("命令描述（可选）", default="", show_default=False)
        team.share_command(command, description)
        
    elif choice == 6:
        commands = team.list_shared_commands()
        if commands:
            click.echo("\n📜 共享命令列表:")
            for i, cmd in enumerate(commands, 1):
                click.echo(f"  {i}. {cmd['command']}")
                click.echo(f"     描述: {cmd.get('description', '无')}")
                click.echo(f"     分享者: {cmd.get('shared_by', '未知')}")
                click.echo()
        else:
            click.echo("📭 暂无共享命令")
            
    elif choice == 7:
        status = team.team_status()
        click.echo("\n📊 团队状态:")
        for key, value in status.items():
            click.echo(f"  {key}: {value}")
            
    else:
        click.echo("返回主菜单")