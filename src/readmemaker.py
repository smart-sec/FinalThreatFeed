#!/usr/bin/env python3
"""
README生成器
根据feeds.yaml和实际拉取状态生成README.md文件，包含订阅列表和存活状态标识
"""

import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('README_Maker')

class READMEGenerator:
    def __init__(self, feeds_config_path: str, readme_path: str = 'README.md'):
        """
        初始化README生成器
        
        Args:
            feeds_config_path: feeds.yaml配置文件路径
            readme_path: 生成的README.md文件路径
        """
        self.feeds_config_path = feeds_config_path
        self.readme_path = readme_path
        self.feeds_data = []
        self.feed_status = {}
    
    def load_feeds_config(self):
        """加载feeds.yaml配置文件"""
        try:
            with open(self.feeds_config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            self.feeds_data = config.get('feeds', [])
            logger.info(f"Loaded {len(self.feeds_data)} feeds from {self.feeds_config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load feeds config: {e}")
            return False
    
    def set_feed_status(self, feed_status: Dict[str, str]):
        """
        设置feed状态，由core.py传递实际拉取结果
        
        Args:
            feed_status: 字典格式，键为feed名称，值为状态('alive', 'error', 'disabled')
        """
        self.feed_status = feed_status
        logger.info(f"Set status for {len(feed_status)} feeds")
    
    def generate_readme(self):
        """Generate README.md file"""
        logger.info("Generating README.md...")
        
        # Build README content
        content = []
        
        # Project title
        content.append("# FinalThreatFeed")
        content.append("")
        content.append("🚀 **High-Performance Open Source Threat Intelligence Aggregation Engine**")
        content.append("")
        
        # Project introduction
        content.append("## 📖 Project Introduction")
        content.append("")
        content.append("FinalThreatFeed is a modern threat intelligence (CTI) automated collection and fusion framework. It is designed based on high-performance asynchronous architecture to solve pain points such as difficulty in multi-source intelligence collection, format confusion, and data redundancy.")
        content.append("")
        content.append("Through a standardized data processing pipeline, FinalThreatFeed continuously extracts high-value data from global open-source intelligence sources, automatically completes cleaning, deduplication, and structuring processes, providing accurate and fresh threat intelligence support for enterprise security defense systems.")
        content.append("")
        
        # Core features
        content.append("### ✨ Core Features")
        content.append("")
        content.append("- ⚡ **High-Speed Asynchronous Architecture**: Built with Python Asyncio + HTTPX for high concurrency collection core, significantly improving data throughput efficiency.")
        content.append("- 🧩 **Full-Stack Format Compatibility**: Native support for mainstream intelligence formats such as MISP, CSV, Text, and RSS, easily breaking down data source format barriers.")
        content.append("- 🧹 **Intelligent Cleaning and Deduplication**: Built-in refined data governance algorithms automatically eliminate noise and duplicate data, ensuring high signal-to-noise ratio of intelligence.")
        content.append("- 🔄 **Full Lifecycle Management**: Automated intelligence aging and update mechanisms ensure the local intelligence library always stays up-to-date.")
        content.append("- 🛠️ **Flexible Extension Configuration**: YAML-based declarative configuration management, allowing quick access to new intelligence sources without coding.")
        content.append("- 🏷️ **Deep IOC Identification**: Automatically parse and classify key threat indicators such as IP, Domain, URL, enabling refined analysis.")
        content.append("- 🤖 **LLM-Powered Unstructured Data Processing**: Leverages Google Gemini API to extract IOCs from unstructured data sources like RSS feeds, enhancing intelligence coverage.")
        content.append("")
        # Update time
        content.append(f"> 🕒 **Last Update Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
        content.append("")

        
        # Subscription list
        content.append("## 📡 Feed Status Monitoring")
        content.append("")
        # Remove description column to keep the table concise
        content.append("| Status | Feed Name | Format Type | Source Address (URL) |")
        content.append("|:---:|---|:---:|---|")
        
        # Add subscription rows
        for feed in self.feeds_data:
            # Status indicator
            status = self.feed_status.get(feed['name'], 'disabled')
            if status == 'alive':
                status_emoji = '🟢'
            elif status == 'error':
                status_emoji = '🔴'
            else:
                status_emoji = '⚫'
            
            # Feed information
            name = feed['name']
            feed_type = feed['source_format']
            url = feed.get('url', '-')
            
            # Add row
            content.append(f"| {status_emoji} | **{name}** | `{feed_type}` | {url} |")
        
        content.append("")
        
        # Status explanation
        content.append("#### 📊 Status Legend")
        content.append("- 🟢 **Running Normally**: Successfully connected and obtained latest intelligence data")
        content.append("- 🔴 **Collection Error**: Connection timeout or source data format error")
        content.append("- ⚫ **Disabled**: Intelligence source not enabled in current configuration")
        content.append("")
        
        # LLM Technology Introduction
        content.append("## 🤖 LLM-Powered Intelligence Processing")
        content.append("")
        content.append("FinalThreatFeed integrates cutting-edge Large Language Model (LLM) technology to process unstructured threat intelligence data, particularly from RSS sources. Here's how it works:")
        content.append("")
        content.append("1. **Intelligent Content Extraction**: Uses Google Gemini API to analyze web content from RSS feeds and automatically extract IOCs (Indicators of Compromise).")
        content.append("2. **Advanced Data Cleaning**: Automatically removes evasion symbols like [.] or [at] and normalizes data to lowercase.")
        content.append("3. **Structured Output**: Converts unstructured text into standardized JSON format for seamless integration with the intelligence pipeline.")
        content.append("4. **Enhanced Coverage**: Expands intelligence sources beyond traditional structured formats to include rich unstructured data from security blogs, threat reports, and news sources.")
        content.append("")
        
        # Quick start
        content.append("## 🚀 Quick Start")
        content.append("")
        content.append("### 1. Environment Setup")
        content.append("```bash")
        content.append("pip install -r requirements.txt")
        content.append("```")
        content.append("")
        content.append("### 2. Start the Engine")
        content.append("```bash")
        content.append("python main.py")
        content.append("```")
        content.append("")
        
        # Configuration guide
        content.append("## ⚙️ Configuration Guide")
        content.append("")
        content.append("All intelligence sources are managed declaratively through `config/feeds.yaml`, supporting flexible custom extensions:")
        content.append("")
        content.append("```yaml")
        content.append("feeds:")
        # Use single quotes to prevent double quote escape issues
        content.append('  - name: "Feed Name"')
        content.append('    enabled: true')
        content.append('    url: "https://example.com/feed.csv"')
        content.append('    source_format: "csv"  # Supports csv, text, misp, rss')
        content.append('    description: "Brief feed description"')
        content.append('    # Different types of sources support specific advanced configuration parameters')
        content.append("```")
        content.append("")
        
        # Output paths
        content.append("## 📂 Data Output")
        content.append("")
        content.append("- `output/description.json`: **Intelligence Source Download Description**")
        content.append("- `output/collections.csv`: **Raw Collection Data** (incremental cache)")
        content.append("- `output/final_threat.csv`: **Final Intelligence Database** (cleaned, deduplicated, standardized high-value intelligence)")
        content.append("")
        
        # License
        content.append("## 📄 Open Source License")
        content.append("")
        content.append("This project follows the [MIT License](LICENSE) open source agreement.")
        content.append("")
        
        # Write to file
        try:
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
            logger.info(f"README.md generated at {self.readme_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write README.md: {e}")
            return False
    
    def run(self):
        """执行完整的生成流程"""
        if not self.load_feeds_config():
            return False
        
        # 确保feed_status不为空，如果为空（例如手动运行脚本时），填充默认状态
        if not self.feed_status:
            logger.warning("No feed status provided. Using default status.")
        
        # 补全状态
        for feed in self.feeds_data:
            if feed['name'] not in self.feed_status:
                if feed.get('enabled', False):
                    self.feed_status[feed['name']] = 'unknown'
                else:
                    self.feed_status[feed['name']] = 'disabled'
        
        return self.generate_readme()

if __name__ == "__main__":
    # 配置路径
    feeds_config = Path("config/feeds.yaml")
    readme_path = Path("README.md")
    
    # 创建生成器并运行
    generator = READMEGenerator(str(feeds_config), str(readme_path))
    if generator.run():
        logger.info("README generation completed successfully!")
    else:
        logger.error("README generation failed!")