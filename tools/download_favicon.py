import os
import yaml
import requests
from urllib.parse import urlparse
import time
from pathlib import Path
import json

class FaviconDownloader:
    def __init__(self, yaml_dir, save_dir):
        self.yaml_dir = yaml_dir
        self.save_dir = save_dir
        self.mapping_file = os.path.join(save_dir, 'favicon_mapping.json')
        self.domain_mapping = self.load_mapping()

    def load_mapping(self):
        """加载已存在的域名映射表"""
        if os.path.exists(self.mapping_file):
            try:
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("映射文件损坏，创建新的映射表")
                return {}
        return {}

    def save_mapping(self):
        """保存域名映射表"""
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump(self.domain_mapping, f, ensure_ascii=False, indent=2)

    def check_local_logo(self, logo):
        """检查本地是否存在logo文件"""
        if logo:
            logo_path = os.path.join(self.save_dir, logo)
            if os.path.exists(logo_path):
                return True
        return False

    def download_favicon(self, url, title, logo=None):
        """下载网站图标并保存"""
        try:
            domain = urlparse(url).netloc
            
            # 检查本地是否已存在配置的logo文件
            if self.check_local_logo(logo):
                print(f"跳过已存在的本地logo: {logo}")
                # 更新映射表
                self.domain_mapping[domain] = logo
                return
            
            # 检查域名是否已经下载过图标
            if domain in self.domain_mapping:
                print(f"跳过已存在的图标: {domain} -> {self.domain_mapping[domain]}")
                return
            
            # 构造favicon.im的URL
            favicon_url = f"https://favicon.im/{domain}?larger=true"
            
            # 发送请求获取图标
            response = requests.get(favicon_url)
            if response.status_code == 200:
                # 使用配置的logo名称或生成新的文件名
                filename = logo if logo else f"{title}.png"
                filepath = os.path.join(self.save_dir, filename)
                
                # 保存图标
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # 更新映射表
                self.domain_mapping[domain] = filename
                print(f"成功下载: {title} - {url}")
            else:
                print(f"下载失败: {title} - {url}, 状态码: {response.status_code}")
                
            # 添加短暂延迟，避免请求过快
            time.sleep(0.5)
            
        except Exception as e:
            print(f"处理出错: {title} - {url}, 错误: {str(e)}")

    def process_yaml_file(self, yaml_path):
        """处理单个YAML文件"""
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        for taxonomy in data:
            for category in taxonomy['list']:
                for tab in category['tabs']:
                    for link in tab['links']:
                        url = link['url']
                        title = link['title']
                        logo = link.get('logo')  # 获取logo配置，如果没有则为None
                        self.download_favicon(url, title, logo)

    def run(self):
        """运行下载器"""
        # 创建保存目录（如果不存在）
        Path(self.save_dir).mkdir(parents=True, exist_ok=True)
        
        # 处理所有YAML文件
        for file in os.listdir(self.yaml_dir):
            if file.endswith('.yml'):
                yaml_path = os.path.join(self.yaml_dir, file)
                print(f"处理文件: {yaml_path}")
                self.process_yaml_file(yaml_path)
        
        # 保存更新后的映射表
        self.save_mapping()

def main():
    # 配置路径
    yaml_dir = "data/Knowledge"  # YAML文件所在目录
    save_dir = "themes/WebStack-Hugo/static/assets/images/logos"  # 图标保存目录
    
    # 创建下载器实例并运行
    downloader = FaviconDownloader(yaml_dir, save_dir)
    downloader.run()

if __name__ == "__main__":
    main()