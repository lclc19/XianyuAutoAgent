#!/usr/bin/env python3
"""
测试Gemini集成的脚本
使用方法:
1. 复制 .env.gemini.example 为 .env
2. 填入您的 GEMINI_API_KEY
3. 运行: python test_gemini.py
"""

import os
import sys
import warnings
from dotenv import load_dotenv
from google import genai
from loguru import logger

# Suppress Pydantic warning about built-in 'any' function
warnings.filterwarnings("ignore", message=".*<built-in function any>.*")

def test_gemini_connection():
    """测试Gemini API连接"""
    # 加载环境变量
    load_dotenv()
    
    model_provider = os.getenv("MODEL_PROVIDER", "qwen").lower()
    
    if model_provider != "gemini":
        logger.error("MODEL_PROVIDER 未设置为 'gemini'，请检查 .env 文件")
        return False
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY 未设置，请在 .env 文件中配置")
        return False
    
    logger.info(f"使用模型提供商: {model_provider}")
    logger.info(f"模型名称: {os.getenv('MODEL_NAME', 'gemini-2.5-flash')}")
    
    try:
        # 初始化Gemini客户端
        client = genai.Client(api_key=api_key)
        
        # 测试简单对话
        logger.info("测试Gemini API连接...")
        
        # 使用系统提示和用户消息
        contents = "系统提示：你是一个友好的助手。\n\n用户：你好，请简单介绍一下自己"
        
        response = client.models.generate_content(
            model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
            contents=contents,
        )
        
        reply = response.text
        logger.success(f"Gemini API连接成功！")
        logger.debug(f"完整响应对象: {response}")
        
        if reply:
            logger.info(f"测试回复: {reply}")
        else:
            logger.warning("API返回了空响应，但连接成功")
        
        return True
        
    except Exception as e:
        logger.error(f"Gemini API连接失败: {e}")
        return False

def test_xianyu_bot():
    """测试XianyuReplyBot与Gemini的集成"""
    load_dotenv()
    
    try:
        from XianyuAgent import XianyuReplyBot
        
        logger.info("初始化XianyuReplyBot...")
        bot = XianyuReplyBot()
        
        # 测试生成回复
        test_item = "iPhone 15 Pro Max 256GB 原装未拆封"
        test_message = "这个手机能便宜点吗？"
        test_context = [
            {"role": "user", "content": "这个手机还在吗？"},
            {"role": "assistant", "content": "在的，全新未拆封"}
        ]
        
        logger.info(f"测试消息: {test_message}")
        reply = bot.generate_reply(test_message, test_item, test_context)
        logger.success(f"机器人回复: {reply}")
        
        return True
        
    except Exception as e:
        logger.error(f"XianyuReplyBot测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("开始测试Gemini集成")
    logger.info("=" * 50)
    
    # 测试基础连接
    if test_gemini_connection():
        logger.info("\n" + "=" * 50)
        logger.info("测试XianyuReplyBot集成")
        logger.info("=" * 50)
        
        # 测试机器人集成
        if test_xianyu_bot():
            logger.success("\n✅ 所有测试通过！Gemini已成功集成")
        else:
            logger.error("\n❌ XianyuReplyBot集成测试失败")
    else:
        logger.error("\n❌ Gemini API连接测试失败")
        logger.info("\n请检查：")
        logger.info("1. .env 文件中 MODEL_PROVIDER=gemini")
        logger.info("2. GEMINI_API_KEY 已正确设置")
        logger.info("3. MODEL_NAME 设置为有效的Gemini模型名称")