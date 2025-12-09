#!/usr/bin/env python3
"""
SMA参数优化脚本
对SMA均线交叉策略进行参数优化，找到最佳参数组合。
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backtest import BacktestEngine
from src.strategies import SMACrossover
from src.data import YahooFinanceLoader


def optimize_sma_for_symbol(symbol: str, data_loader: YahooFinanceLoader,
                             fast_range: range, slow_range: range):
    """
    对单个股票进行SMA参数优化。

    Args:
        symbol: 股票代码
        data_loader: 数据加载器
        fast_range: 快线周期范围
        slow_range: 慢线周期范围
    """
    print("\n" + "="*70)
    print(f"优化 {symbol} 的SMA参数")
    print("="*70)

    # 获取数据
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 1)

    print(f"加载数据：{start_date.date()} 到 {end_date.date()}...")
    data = data_loader.fetch_data(symbol, start_date, end_date)

    if data.empty:
        print(f"无法获取 {symbol} 的数据，跳过。")
        return None

    print(f"已加载 {len(data)} 条数据")

    # 计算参数组合数量
    total_combinations = len(fast_range) * len(slow_range)
    print(f"\n参数搜索空间:")
    print(f"  快线周期 (fast_period): {fast_range.start} - {fast_range.stop-1}")
    print(f"  慢线周期 (slow_period): {slow_range.start} - {slow_range.stop-1}")
    print(f"  总组合数: {total_combinations}")

    # 初始化回测引擎
    engine = BacktestEngine(
        initial_cash=100000.0,
        commission=0.001
    )

    # 添加优化策略（注意使用optstrategy）
    engine.add_optimization_strategy(
        SMACrossover,
        fast_period=fast_range,
        slow_period=slow_range,
        printlog=False  # 关闭日志以加快速度
    )

    # 添加数据
    engine.add_data(data, name=symbol)

    # 添加分析器
    engine.add_analyzers()

    # 运行优化
    print(f"\n开始优化（这可能需要几分钟）...")
    results = engine.run_optimization()

    # 转换为DataFrame便于分析
    df_results = pd.DataFrame([
        {
            'fast_period': r['params']['fast_period'],
            'slow_period': r['params']['slow_period'],
            'total_return': r['metrics'].get('total_return', 0),
            'sharpe_ratio': r['metrics'].get('sharpe_ratio', None),
            'max_drawdown': r['metrics'].get('max_drawdown', None),
            'total_trades': r['metrics'].get('total_trades', 0),
            'win_rate': r['metrics'].get('win_rate', 0),
            'final_value': r['metrics'].get('final_value', 0),
        }
        for r in results
    ])

    # 过滤有效结果（至少有交易）
    df_valid = df_results[df_results['total_trades'] > 0].copy()

    if df_valid.empty:
        print("\n警告：所有参数组合都没有产生交易！")
        return None

    print(f"\n有效结果数: {len(df_valid)} / {len(df_results)}")

    # 按不同指标排序
    print("\n" + "="*70)
    print(f"{symbol} - 优化结果")
    print("="*70)

    # 1. 按总回报率排序
    print("\n【Top 5 按总回报率】")
    top_return = df_valid.nlargest(5, 'total_return')
    print(top_return[['fast_period', 'slow_period', 'total_return',
                      'sharpe_ratio', 'win_rate', 'total_trades']].to_string(index=False))

    # 2. 按Sharpe Ratio排序（过滤掉None和负无穷）
    df_sharpe = df_valid[df_valid['sharpe_ratio'].notna()].copy()
    if not df_sharpe.empty:
        print("\n【Top 5 按Sharpe Ratio】")
        top_sharpe = df_sharpe.nlargest(5, 'sharpe_ratio')
        print(top_sharpe[['fast_period', 'slow_period', 'total_return',
                         'sharpe_ratio', 'win_rate', 'total_trades']].to_string(index=False))

    # 3. 按胜率排序
    print("\n【Top 5 按胜率】")
    top_winrate = df_valid.nlargest(5, 'win_rate')
    print(top_winrate[['fast_period', 'slow_period', 'total_return',
                       'sharpe_ratio', 'win_rate', 'total_trades']].to_string(index=False))

    # 推荐参数（综合考虑）
    print("\n" + "="*70)
    print("推荐参数")
    print("="*70)

    # 找到Sharpe Ratio最高且总回报为正的参数
    df_good = df_sharpe[df_sharpe['total_return'] > 0].copy()

    if not df_good.empty:
        best = df_good.nlargest(1, 'sharpe_ratio').iloc[0]
        print(f"\n最佳参数组合（Sharpe Ratio最高 + 正回报）:")
        print(f"  快线周期: {int(best['fast_period'])}")
        print(f"  慢线周期: {int(best['slow_period'])}")
        print(f"  总回报率: {best['total_return']:.2f}%")
        print(f"  Sharpe Ratio: {best['sharpe_ratio']:.3f}")
        print(f"  最大回撤: {best['max_drawdown']:.2f}%")
        print(f"  胜率: {best['win_rate']:.2f}%")
        print(f"  交易次数: {int(best['total_trades'])}")
    else:
        # 如果没有正回报的，就选回报率最高的
        best = df_valid.nlargest(1, 'total_return').iloc[0]
        print(f"\n最佳参数组合（回报率最高）:")
        print(f"  快线周期: {int(best['fast_period'])}")
        print(f"  慢线周期: {int(best['slow_period'])}")
        print(f"  总回报率: {best['total_return']:.2f}%")
        print(f"  Sharpe Ratio: {best['sharpe_ratio']}")
        print(f"  最大回撤: {best['max_drawdown']:.2f}%")
        print(f"  胜率: {best['win_rate']:.2f}%")
        print(f"  交易次数: {int(best['total_trades'])}")

    return df_valid


def main():
    """主函数：运行SMA参数优化"""
    print("\n" + "="*70)
    print("SMA均线交叉策略 - 参数优化")
    print("="*70)

    # 初始化数据加载器
    data_loader = YahooFinanceLoader()

    # 定义参数搜索范围
    # 快线周期：5-20（步长1）
    # 慢线周期：25-60（步长5）
    fast_range = range(5, 21)      # 5, 6, 7, ..., 20
    slow_range = range(25, 61, 5)  # 25, 30, 35, 40, 45, 50, 55, 60

    # 要优化的股票
    symbols = ['TSLA', 'QQQ']

    # 对每个股票运行优化
    all_results = {}
    for symbol in symbols:
        try:
            results = optimize_sma_for_symbol(symbol, data_loader, fast_range, slow_range)
            if results is not None:
                all_results[symbol] = results
        except Exception as e:
            print(f"\n优化 {symbol} 时出错: {e}")
            continue

    print("\n" + "="*70)
    print("优化完成！")
    print("="*70)

    # 可选：保存结果到CSV
    for symbol, df in all_results.items():
        output_file = f"optimization_results_{symbol}.csv"
        df.to_csv(output_file, index=False)
        print(f"\n{symbol} 的详细结果已保存到: {output_file}")


if __name__ == '__main__':
    main()
