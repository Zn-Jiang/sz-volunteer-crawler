# 志愿深圳志愿项目爬虫 / sz-volunteer-crawler

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)

基于逆向分析的志愿深圳志愿项目爬取与解密工具 🛠️  
A tool to crawl and decrypt Shenzhen volunteer project data using AES-CBC.

---

## 🚀 功能说明

- 自动获取动态密钥（key 和 sid）
- 使用 AES-CBC 解密服务器返回的加密数据
- 加密查询参数发起志愿项目查询请求
- 获取并输出志愿服务项目信息

---

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🔧 使用方法

```bash
python main.py
```

---

## 🔐 技术细节

- 解密方式：AES-CBC（密钥由接口返回，IV 从混淆数据中提取）
- 加密方式：AES-CBC（密钥为接口返回的 value，IV 为固定值）
- 前端逻辑逆向来源：https://www.sva.org.cn/SZWSLDPC/

---

## 📄 License

MIT License

> 本项目由 [Zn-Jiang](https://github.com/Zn-Jiang) 开发，欢迎自由使用、修改和分发（包括商业用途），只需保留本声明即可。

---

## ⚠️ 声明

本项目仅供学习与研究使用，请勿用于违反法律法规或侵犯网站服务条款的行为。
