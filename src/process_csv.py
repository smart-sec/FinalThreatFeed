import pandas as pd
import re
import os
import logging

# 配置基础日志输出
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ThreatCSVProcessor:
    def __init__(self, input_file='output/final_threat.csv', output_file='output/labeled_threat_threat.csv'):
        self.input_file = input_file
        self.output_file = output_file
        self.allowed_types = ['domain', 'ip', 'ip-src', 'ip-dst', 'ip-dst|port', 'md5', 'sha1', 'sha256', 'url']
        self.output_columns = [
            'event_time', 'ioc_type', 'ioc_value', 'port',
            'threat_type1', 'threat_type2', 'threat_type3', 'confidence',
            'source_reference', 'tags'
        ]

    def _process_row(self, row):
        """处理单行数据的核心逻辑"""
        event_time = row.get('timestamp')
        ioc_value = row.get('value')
        row_type = row.get('type')
        feed_name = row.get('feed_name')
        comment = str(row.get('comment', '')) # 转换为字符串以防空值报错
        
        ioc_type = ''
        port = 0
        
        # 匹配 ioc_type
        if row_type == 'domain':
            ioc_type = 'Domain'
        elif row_type in ['ip', 'ip-dst', 'ip-src']:
            ioc_type = 'IPv4'
        elif row_type == 'ip-dst|port':
            ioc_type = 'IPv4'
            try:
                if '|' in str(ioc_value):
                    ioc_value, port_str = str(ioc_value).split('|', 1)
                    port = int(port_str)
            except ValueError:
                pass
        elif row_type == 'md5':
            ioc_type = 'Hash_md5'
        elif row_type == 'sha1':
            ioc_type = 'Hash_sha1'
        elif row_type == 'sha256':
            ioc_type = 'Hash_sha256'
        elif row_type == 'url':
            ioc_type = 'URL'

        threat_type1 = None
        threat_type2 = None
        threat_type3 = None
        confidence = 80
        source_reference = feed_name
        tags = ''
        
        # 根据 feed_name 设置不同的处理逻辑
        if feed_name == 'abuse.ch':
            threat_type1 = '失陷情报'
            threat_type2 = '远控'
            threat_type3 = '远控'
            confidence_match = re.search(r'confidence level: (\d+)%', comment)
            if confidence_match:
                conf_val = int(confidence_match.group(1))
                if 0 < conf_val < 80:
                    confidence = 60
                elif 80 <= conf_val < 99:
                    confidence = 80
                elif conf_val >= 99:
                    confidence = 99
            if comment:
                tags = comment.split(' ')[0]
                
        elif feed_name == 'abuse.ch-Bazaar':
            threat_type1 = '失陷情报'
            threat_type2 = '恶意软件'
            threat_type3 = '恶意软件'
            tags_match = re.search(r'\((.*?)\)', comment)
            if tags_match:
                tags = tags_match.group(1)

        elif feed_name == 'abuse.ch-URLhasus':
            threat_type1 = '失陷情报'
            threat_type2 = '远控'
            threat_type3 = '远控'
            tags_match = re.search(r'\((.*?)\)', comment)
            if tags_match:
                tags = tags_match.group(1)

        elif feed_name == 'abuse.ch-SSL':
            threat_type1 = '失陷情报'
            threat_type2 = '远控'
            threat_type3 = '远控'
            if comment:
                tags = comment.split(' ')[0]
        
        elif feed_name in ['Alienvault-IP-Reputation', 'CIRCL OSINT Feed', 'IPsum-l4', 'IPsum-l5']:
            threat_type1 = '攻击情报'
            threat_type2 = '傀儡机'
            threat_type3 = '傀儡机'

        elif feed_name == 'Phishtank':
            threat_type1 = '失陷情报'
            threat_type2 = '钓鱼'
            threat_type3 = '钓鱼'

        # 返回 Pandas Series，以便 apply 函数直接组装为 DataFrame
        return pd.Series([
            event_time, ioc_type, ioc_value, port,
            threat_type1, threat_type2, threat_type3, confidence,
            source_reference, tags
        ], index=self.output_columns)

    def run(self):
        """执行数据清洗和处理"""
        if not os.path.exists(self.input_file):
            logging.error(f"输入文件不存在: {self.input_file}")
            return False

        logging.info(f"正在读取文件: {self.input_file}")
        try:
            df = pd.read_csv(self.input_file)
            logging.info(f"原始数据行数: {len(df)}")

            # 筛选 type 列
            df_filtered = df[df['type'].isin(self.allowed_types)].copy()
            logging.info(f"筛选后数据行数: {len(df_filtered)}")

            if df_filtered.empty:
                logging.warning("没有符合条件的数据需要处理。")
                return True

            logging.info("正在进行数据转化处理...")
            # 使用 apply 替代 iterrows，提升运行效率和代码整洁度
            new_df = df_filtered.apply(self._process_row, axis=1)

            # 填充空值为 None 或空字符串 (Pandas 推荐空值转为空字典或留空，此处兼容原有逻辑)
            new_df = new_df.where(pd.notnull(new_df), None)

            # 确保输出目录存在
            os.makedirs(os.path.dirname(self.output_file) or '.', exist_ok=True)

            logging.info("正在写入新文件...")
            new_df.to_csv(self.output_file, index=False)
            logging.info(f"处理完成！新文件已保存为: {self.output_file}")
            logging.info(f"新文件最终行数: {len(new_df)}")
            return True

        except Exception as e:
            logging.error(f"处理 CSV 时发生错误: {str(e)}")
            return False

# 提供一个便捷的方法用于直接调用
def process_threat_csv(input_path='output/final_threat.csv', output_path='output/labeled_threat_threat.csv'):
    processor = ThreatCSVProcessor(input_file=input_path, output_file=output_path)
    return processor.run()

if __name__ == "__main__":
    # 支持脚本直接独立运行
    process_threat_csv()