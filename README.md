# FinalThreatFeed

🚀 **高性能开源威胁情报聚合引擎**

## 📖 项目简介

FinalThreatFeed 是一款现代化的威胁情报（CTI）自动化采集与融合框架。它基于高性能异步架构设计，旨在解决多源情报采集难、格式混乱、数据冗余等痛点。

通过标准化的数据处理管道，FinalThreatFeed 能够从全球开源情报源中持续汲取高价值数据，自动完成清洗、去重与结构化处理，为企业的安全防御体系提供精准、鲜活的威胁情报支撑。

### ✨ 核心特性

- ⚡ **极速异步架构**: 采用 Python Asyncio + HTTPX 构建高并发采集核心，大幅提升数据吞吐效率。
- 🧩 **全栈格式兼容**: 原生支持 MISP、CSV、Text 等主流情报格式，轻松打破数据源格式壁垒。
- 🧹 **智能清洗去重**: 内置精细化数据治理算法，自动剔除噪声与重复数据，确保情报的高信噪比。
- 🔄 **全生命周期管理**: 自动化的情报老化与更新机制，确保本地情报库始终保持最新状态。
- 🛠️ **灵活扩展配置**: 基于 YAML 的声明式配置管理，无需编码即可快速接入新的情报源。
- 🏷️ **深度 IOC 识别**: 自动解析并分类 IP、Domain、URL 等关键威胁指标，赋能精细化分析。

> 🕒 **最后更新时间:** `2026-02-14 01:28:37`

## 📡 订阅源状态监控

| 运行状态 | 情报源名称 | 格式类型 | 源地址 (URL) |
|:---:|---|:---:|---|
| 🟢 | **abuse.ch-SSL** | `csv` | https://sslbl.abuse.ch/blacklist/sslblacklist.csv |
| 🟢 | **Alienvault-IP-Reputation** | `csv` | https://reputation.alienvault.com/reputation.generic |
| 🔴 | **Phishtank** | `csv` | https://data.phishtank.com/data/online-valid.csv |
| ⚫ | **Tor_Exit_Nodes** | `text` | https://check.torproject.org/torbulkexitlist |
| 🟢 | **IPsum-l4** | `text` | https://raw.githubusercontent.com/stamparm/ipsum/master/levels/4.txt |
| 🟢 | **IPsum-l5** | `text` | https://raw.githubusercontent.com/stamparm/ipsum/master/levels/5.txt |
| 🟢 | **CIRCL OSINT Feed** | `misp` | https://www.circl.lu/doc/misp/feed-osint/ |
| 🟢 | **abuse.ch** | `misp` | https://threatfox.abuse.ch/downloads/misp |
| 🟢 | **abuse.ch-Bazaar** | `misp` | https://bazaar.abuse.ch/downloads/misp/ |
| 🟢 | **abuse.ch-URLhasus** | `misp` | https://urlhaus.abuse.ch/downloads/misp |
| 🟢 | **Botvrij.eu** | `misp` | https://www.botvrij.eu/data/feed-osint |

#### 📊 运行状态图例
- 🟢 **运行正常**: 成功连接并获取最新情报数据
- 🔴 **采集异常**: 连接超时或源数据格式错误
- ⚫ **已禁用**: 当前配置下未启用的情报源

## 🚀 快速开始

### 1. 环境准备
```bash
pip install -r requirements.txt
```

### 2. 启动引擎
```bash
python main.py
```

## ⚙️ 配置指南

所有情报源均通过 `config/feeds.yaml` 进行声明式管理，支持灵活的自定义扩展：

```yaml
feeds:
  - name: "Feed名称"
    enabled: true
    url: "[https://example.com/feed.csv](https://example.com/feed.csv)"
    source_format: "csv"  # 支持 csv, text, misp
    description: "简短的情报源描述"
    # 不同类型的源支持特定的高级配置参数
```

## 📂 数据产出

- `output/description.json`: **情报源下载描述**
- `output/collections.csv`: **原始采集数据** (增量缓存)
- `output/final_threat.csv`: **最终情报库** (已清洗、去重、标准化的全量高价值情报)

## 📄 开源协议

本项目遵循 [MIT License](LICENSE) 开源协议。
