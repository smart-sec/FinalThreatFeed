"""
FinalThreatFeed - 开源威胁情报自动化搜集工具
主入口文件
"""

import sys
import asyncio
from src.core import CoreEngine
from src.process_csv import process_threat_csv 


def main():
    """主函数"""
    try:
        # 1. 创建核心引擎实例并运行情报抓取流水线
        engine = CoreEngine()
        print("[*] 开始执行威胁情报搜集任务...")
        asyncio.run(engine.run_pipeline())
        
        # 2. 抓取结束后，自动运行数据标准化和格式化处理
        print("\n[*] 搜集任务完成，开始处理和清洗 CSV 数据...")
        
        # 如果生成的文件路径有变化，可以在此处传入对应参数
        success = process_threat_csv()
        
        if success:
            print("[+] 所有任务成功运行完毕！")
        else:
            print("[-] CSV 数据处理阶段出现异常，请检查日志。")

    except KeyboardInterrupt:
        print("\n[!] 接收到退出信号，程序终止。")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] 运行中发生未捕获的错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()