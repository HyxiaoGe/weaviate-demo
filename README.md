# Weaviate Demo - Python 向量数据库学习项目

一个从入门到实战的 Weaviate 向量数据库完整学习项目。

## 📋 项目简介

本项目旨在通过渐进式的示例和实战项目，帮助你全面掌握 Weaviate 向量数据库的使用，从基础连接到生产级应用落地。

## 🎯 学习目标

- ✅ 掌握 Weaviate 核心概念（Schema、Vector、Class）
- ✅ 熟练使用各种查询方式（向量搜索、混合搜索、过滤）
- ✅ 理解向量数据库在 AI 应用中的作用
- ✅ 完成 4 个实战项目，具备生产环境落地能力

## 📁 项目结构

```
weaviate-demo/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python 依赖包
├── .env.example                 # 环境变量模板
├── config/
│   └── weaviate_config.py      # Weaviate 连接配置
│
├── 01-basics/                   # 第一阶段：基础入门
│   ├── 01_connection.py         # 连接 Weaviate
│   ├── 02_schema_creation.py    # 创建 Schema
│   ├── 03_data_import.py        # 数据导入
│   ├── 04_basic_query.py        # 基础查询
│   └── 05_vector_search.py      # 向量搜索
│
├── 02-intermediate/             # 第二阶段：进阶使用
│   ├── 01_batch_import.py       # 批量导入优化
│   ├── 02_hybrid_search.py      # 混合搜索（BM25 + Vector）
│   ├── 03_filters.py            # 复杂过滤条件
│   ├── 04_aggregation.py        # 聚合查询
│   └── 05_cross_reference.py    # 交叉引用关系
│
├── 03-advanced/                 # 第三阶段：高级特性
│   ├── 01_custom_vectors.py     # 自定义向量模型
│   ├── 02_multi_tenancy.py      # 多租户架构
│   ├── 03_backup_restore.py     # 备份与恢复
│   └── 04_monitoring.py         # 性能监控
│
├── 04-projects/                 # 第四阶段：实战项目
│   ├── semantic_search/         # 项目1：语义搜索引擎
│   │   ├── README.md
│   │   ├── app.py
│   │   └── data_indexing.py
│   ├── qa_system/               # 项目2：智能问答系统
│   │   ├── README.md
│   │   ├── qa_engine.py
│   │   └── knowledge_base.py
│   ├── recommendation/          # 项目3：推荐系统
│   │   ├── README.md
│   │   ├── recommender.py
│   │   └── user_profile.py
│   └── rag_chatbot/             # 项目4：RAG 聊天机器人
│       ├── README.md
│       ├── chatbot.py
│       ├── document_loader.py
│       └── chain.py
│
├── utils/                       # 工具模块
│   ├── __init__.py
│   ├── data_loader.py           # 数据加载工具
│   ├── embedding.py             # 向量化工具
│   └── logger.py                # 日志配置
│
├── data/                        # 示例数据
│   ├── movies.json              # 电影数据
│   ├── articles.txt             # 文章数据
│   └── products.csv             # 商品数据
│
└── tests/                       # 测试文件
    ├── test_connection.py
    └── test_schema.py
```

## 🚀 快速开始

### 1. 环境准备

确保你的开发服务器上 Weaviate 已通过 Docker 运行：

```bash
# 检查 Weaviate 是否运行
curl http://localhost:8080/v1/meta

# 如果未运行，使用 docker-compose 启动
docker-compose up -d
```

### 2. 安装依赖

```bash
# 克隆或创建项目目录
mkdir weaviate-demo && cd weaviate-demo

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置你的参数
nano .env
```

`.env` 文件示例：
```env
# Weaviate 连接配置
WEAVIATE_URL=http://localhost:8080

# 或使用本地模型（可选）
OLLAMA_API_ENDPOINT=http://localhost:11434
OLLAMA_MODEL=bge-m3
```

### 4. 运行第一个示例

```bash
# 测试连接
python 01-basics/01_connection.py

# 创建 Schema
python 01-basics/02_schema_creation.py

# 导入数据并进行向量搜索
python 01-basics/03_data_import.py
python 01-basics/05_vector_search.py
```

## 📚 学习路径

### 阶段一：基础入门（建议学习时间：1-2周）

**学习目标**：理解 Weaviate 核心概念，能够完成基本的增删改查操作

| 示例文件 | 学习内容 | 关键知识点 |
|---------|---------|-----------|
| `01_connection.py` | 连接 Weaviate | Client 初始化、健康检查 |
| `02_schema_creation.py` | 创建 Schema | Class、Property、Vectorizer |
| `03_data_import.py` | 数据导入 | Create、Update、Delete |
| `04_basic_query.py` | 基础查询 | Get、Where、Limit |
| `05_vector_search.py` | 向量搜索 | nearText、nearVector、距离计算 |

**实践项目**：构建一个电影信息检索系统
- 导入 1000+ 电影数据
- 实现按类型、年份筛选
- 实现自然语言搜索电影

---

### 阶段二：进阶使用（建议学习时间：2-3周）

**学习目标**：掌握高效的数据操作和复杂查询技巧

| 示例文件 | 学习内容 | 关键知识点 |
|---------|---------|-----------|
| `01_batch_import.py` | 批量导入 | Batch API、并发控制、错误处理 |
| `02_hybrid_search.py` | 混合搜索 | BM25 + Vector、Alpha 参数调优 |
| `03_filters.py` | 复杂过滤 | 多条件组合、地理位置过滤 |
| `04_aggregation.py` | 聚合查询 | Count、GroupBy、Meta 信息 |
| `05_cross_reference.py` | 交叉引用 | 关联关系、多跳查询 |

**实践项目**：构建新闻文章检索和分析系统
- 导入 10000+ 新闻文章
- 实现混合搜索（关键词 + 语义）
- 统计分析（按时间、类别聚合）
- 相关文章推荐

---

### 阶段三：高级特性（建议学习时间：2周）

**学习目标**：深入理解架构，具备性能优化和运维能力

| 示例文件 | 学习内容 | 关键知识点 |
|---------|---------|-----------|
| `01_custom_vectors.py` | 自定义向量 | 自定义 Embedding 模型集成 |
| `02_multi_tenancy.py` | 多租户 | 数据隔离、租户管理 |
| `03_backup_restore.py` | 备份恢复 | 数据安全、迁移策略 |
| `04_monitoring.py` | 性能监控 | 指标采集、健康检查 |

**实践项目**：构建多用户 SaaS 知识库系统
- 多租户数据隔离
- 自定义领域模型（医疗、法律等）
- 数据备份自动化
- 监控告警系统

---

### 阶段四：实战项目（建议学习时间：3-4周）

选择一个或多个项目进行深入实践：

#### 项目1：语义搜索引擎 📝
**技术栈**：Weaviate + OpenAI Embeddings + FastAPI

**功能**：
- 支持自然语言查询的文档检索
- 搜索结果重排序
- 高亮显示匹配片段
- RESTful API 接口

**适用场景**：企业内部文档搜索、论文检索

---

#### 项目2：智能问答系统 🤖
**技术栈**：Weaviate + LangChain + OpenAI

**功能**：
- 基于知识库的精准问答
- RAG（检索增强生成）
- 答案来源追溯
- 多轮对话上下文

**适用场景**：客服机器人、技术文档助手

---

#### 项目3：个性化推荐系统 🎯
**技术栈**：Weaviate + 用户行为分析

**功能**：
- 基于内容的推荐
- 协同过滤 + 向量相似度
- 实时推荐更新
- A/B 测试支持

**适用场景**：电商推荐、内容推荐

---

#### 项目4：RAG 聊天机器人 💬（推荐）
**技术栈**：Weaviate + LangChain + Streamlit + OpenAI

**功能**：
- 上传文档构建知识库
- 与私有文档对话
- 流式回复
- 引用来源显示
- Web UI 界面

**适用场景**：企业知识助手、个人学习助手

## 🔧 核心技术点

### 1. 向量数据库基础
- **什么是向量/嵌入（Embedding）**：文本、图片等数据的数值化表示
- **向量检索原理**：通过计算向量间距离找到相似内容
- **ANN 算法**：HNSW（Hierarchical Navigable Small World）

### 2. Weaviate 核心概念
- **Class**：类似关系数据库的表，定义对象类型
- **Property**：对象的属性字段
- **Vectorizer**：将数据转换为向量的模块（text2vec-openai 等）
- **Module**：扩展功能（qna-openai、generative-openai 等）

### 3. Schema 设计最佳实践
```python
# 好的 Schema 设计示例
{
    "class": "Article",
    "description": "新闻文章",
    "vectorizer": "text2vec-openai",
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "description": "文章标题",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": False,  # 参与向量化
                    "vectorizePropertyName": False
                }
            }
        },
        {
            "name": "content",
            "dataType": ["text"],
            "description": "文章正文"
        },
        {
            "name": "publishDate",
            "dataType": ["date"],
            "description": "发布日期"
        },
        {
            "name": "category",
            "dataType": ["text"],
            "description": "文章分类",
            "moduleConfig": {
                "text2vec-openai": {
                    "skip": True  # 不参与向量化
                }
            }
        }
    ]
}
```

### 4. 批量导入优化
```python
# 使用 batch API 提高导入效率
with client.batch as batch:
    batch.batch_size = 100  # 每批次大小
    batch.dynamic = True     # 动态调整
    batch.timeout_retries = 3
    
    for item in data:
        batch.add_data_object(
            data_object=item,
            class_name="Article"
        )
```

### 5. 查询性能调优
- 使用合适的 `limit` 参数
- 利用 `where` 过滤器预筛选
- 选择合适的向量维度（768 vs 1536）
- 启用 HNSW 索引的 `ef` 参数调优

## 📖 推荐学习资源

- **官方文档**：https://weaviate.io/developers/weaviate
- **官方示例**：https://github.com/weaviate/weaviate-examples
- **向量检索原理**：https://weaviate.io/blog/vector-search-basics
- **HNSW 算法详解**：https://arxiv.org/abs/1603.09320

## ⚙️ Docker 部署配置

如果需要重新部署 Weaviate，可以使用以下 `docker-compose.yml`：

```yaml
version: '3.4'
services:
  weaviate:
    image: semitechnologies/weaviate:1.24.1
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-openai'
      ENABLE_MODULES: 'text2vec-openai,generative-openai'
      CLUSTER_HOSTNAME: 'node1'
    volumes:
      - weaviate_data:/var/lib/weaviate

volumes:
  weaviate_data:
```

启动命令：
```bash
docker-compose up -d
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📮 联系方式

如有问题，欢迎提 Issue 或联系维护者。

---

**Happy Learning! 🎉**

开始你的向量数据库之旅吧！